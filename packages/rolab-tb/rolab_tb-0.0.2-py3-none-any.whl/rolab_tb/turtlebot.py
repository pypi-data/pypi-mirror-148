#!/usr/bin/env python3

"""
    SPDX-FileCopyrightText: 2022 Senne Van Baelen
    SPDX-License-Identifier: Apache-2.0

    Turtlebot class for connecting to a ROS bridge

    Author(s):    Senne Van Baelen
    Contact:      senne.vanbaelen@kuleuven.be
    Date created: 2021-02-14

    TODO:
      - (optional) mirgrate from sqlite3 to REDIS or Apache Arrow plasma
        store
      - should probably implement <https://stackoverflow.com/a/52301233>
"""

import sys
import os
import signal
import time
import json
import traceback
import asyncio
from enum import Enum
import threading
import sqlite3
import pathlib
import numpy as np
import websockets

#=====================================================================
# Configs
#=====================================================================


TB_LIMIT_LIN_VEL = 0.22         # m/s
TB_LIMIT_ANG_VEL = 2.84         # rad/s

# <https://github.com/ROBOTIS-GIT/OpenCR/blob/master/arduino/opencr_arduino/opencr/libraries/turtlebot3/examples/turtlebot3_burger/turtlebot3_core/turtlebot3_core_config.h#L64>
TB_TICK_TO_RAD = 0.001533981

CHANGE_ANG_VEL_DIR = False
QUERY_SLEEP_SEC = 0.005

D_CONFIG_DEFAULT = {
        "ws_host": "10.42.0.1",
        "ws_port": 9090,
        "msg-sub-dir": "msgs/sub/",
        "msg-pub-dir": "msgs/pub/",
        "sqlite-sensor-uri": "file:mem-sensor?mode=memory&cache=shared",
        "sqlite-control-uri": "file:mem-control?mode=memory&cache=shared",
        "tb_ttr": TB_TICK_TO_RAD
        }


class StatusMainProcess(Enum):

    """ status codes """

    RUNNING = 1
    WARNING = 2
    ERROR = 3

class StatusSensorMsgs(Enum):

    """ status codes """

    INITIALISING = 0
    REQUESTED = 1
    SUBSCRIBED = 2
    ERROR = 3

#=====================================================================
# General methods
#=====================================================================

def db_query_select(db_con, query, fetch_many=False,
                    as_json=False, print_warnings=True):

    """ query sqlite database """

    res = None

    try:
        db_cur = db_con.cursor()
        db_cur.execute(query)

        if fetch_many:
            res = db_cur.fetchall()
        else:
            res = db_cur.fetchone()[0]

        if as_json:
            res = json.loads(res)

    except sqlite3.OperationalError as err:
        if "database table is locked" in str(err):
            return db_query_select(db_con, query, fetch_many, as_json)
        if print_warnings:
            print(traceback.format_exc())
    except TypeError as err:
        if print_warnings:
            print(f"[WARN] (query_select) ignoring query '{query}' \
due to TypeError ({err})")
        # print(traceback.format_exc())

    # allow for stack clearance, if necessary
    # this also means that a single get query takes at least 0.005s
    time.sleep(QUERY_SLEEP_SEC)

    return res

def db_query_insert(db_con, query, input_tuple):

    """ query insert in sqlite db """

    try:
        db_cur = db_con.cursor()
        db_cur.execute(query, input_tuple)

    except sqlite3.OperationalError as err:
        if "database table is locked" in str(err):
            return db_query_insert(db_con, query, input_tuple)
        print(traceback.format_exc())
    except TypeError as err:
        print("[WARN] (query_insert) ignoring query due to TypeError", err)
        # print(traceback.format_exc())

    return None


def kill_all_threads():

    """ kill all treads """

    if os.name == 'nt':
        # pylint: disable=protected-access
        os._exit()
    else:
        os.kill(os.getpid(), signal.SIGINT)


def quaternion_to_euler_angle_vectorized(q_w, q_x, q_y, q_z):

    """ convert IMU quaternion to euler angles (roll pitch yaw) """

    ysqr = q_y * q_y

    intm_0 = +2.0 * (q_w * q_x + q_y * q_z)
    intm_1 = +1.0 - 2.0 * (q_x * q_x + ysqr)
    x_euler = np.degrees(np.arctan2(intm_0, intm_1))

    intm_2 = +2.0 * (q_w * q_y - q_z * q_x)
    intm_2 = np.where(intm_2>+1.0,+1.0,intm_2)
    #t2 = +1.0 if t2 > +1.0 else t2

    intm_2 = np.where(intm_2<-1.0, -1.0, intm_2)
    #t2 = -1.0 if t2 < -1.0 else t2
    y_euler = np.degrees(np.arcsin(intm_2))

    intm_3 = +2.0 * (q_w * q_z + q_x * q_y)
    intm_4 = +1.0 - 2.0 * (ysqr + q_z * q_z)
    if CHANGE_ANG_VEL_DIR:
        z_euler = -np.degrees(np.arctan2(intm_3, intm_4))
    else:
        z_euler = np.degrees(np.arctan2(intm_3, intm_4))

    return x_euler, y_euler, z_euler


async def update_sensor_readings(ws_uri, subscribe_msgs, db_uri):

    """ async event loop for obtaining sensor data """

    db_con = sqlite3.connect(db_uri, uri=True, isolation_level=None)

    # db_con.cursor().execute("pragma journal_mode=wal;")

    try:
        async with websockets.connect(ws_uri) as websocket:
            for topic in subscribe_msgs:
                await websocket.send(json.dumps(subscribe_msgs[topic]))
            db_con.cursor().execute("""
INSERT INTO status VALUES (?, ?, ?);""",
                                        ("sensors",
                                         StatusSensorMsgs.REQUESTED.value,
                                         "Requested sensor subscribtions"
                                         ))

            while True:
                d_data = json.loads(await websocket.recv())
                try:
                    db_con.cursor().execute("""
INSERT INTO sensor_readings VALUES (?, ?);""",
                                            (d_data['topic'],
                                             json.dumps(d_data['msg'])))
                except sqlite3.OperationalError as err:
                    if "database table is locked" in str(err):
                        pass
                    else:
                        print(traceback.format_exc())
    except (ConnectionRefusedError, OSError,
            asyncio.exceptions.TimeoutError) as err:
        print("[ERROR] failed to connect to websocket server at ", end="")
        print(ws_uri)
        print(err)
        print("Make sure the Turlebot (+ websocket bridge) is running")
        print("Exiting...")
        kill_all_threads()


async def send_control_inputs(ws_uri, msgs, db_uri):

    """ async event loop for sending control inputs """

    db_con = sqlite3.connect(db_uri, uri=True, isolation_level=None)
    cmd_vel_template = msgs['cmd_vel']

    try:
        async with websockets.connect(ws_uri) as websocket:
            for topic in msgs:
                keys = ['op', 'type', 'topic']
                adv_msg = {x:msgs[topic][x] for x in keys}
                adv_msg['op'] = "advertise"
                await websocket.send(json.dumps(adv_msg))
            previous_input = None
            while True:
                try:
                    query = """
SELECT linear_vel, angular_vel FROM control_inputs
ORDER BY rowid DESC, angular_vel DESC LIMIT 1;"""
                    last_input = db_query_select(db_con, query,
                                                 fetch_many=True)
                    if last_input:
                        if last_input != previous_input:
                            cmd_vel_template['msg']['linear']['x'] = \
                                    last_input[0][0]
                            cmd_vel_template['msg']['angular']['z'] = \
                                    last_input[0][1]

                            previous_input = last_input
                            await websocket.send(json.dumps(cmd_vel_template))
                except sqlite3.OperationalError as err:
                    if "database table is locked" in str(err):
                        pass
                    else:
                        print(traceback.format_exc())

                time.sleep(0.01)

    except (ConnectionRefusedError, OSError,
            asyncio.exceptions.TimeoutError) as err:
        print("[ERROR] failed to connect to websocket server at ", end="")
        print(ws_uri)
        print("Make sure the Turlebot (+ websocket bridge) is running")
        print(err)
        print("Exiting...")
        kill_all_threads()


def get_json_msgs(subdir, json_sub_msgs=None):

    """ collect subscribe messages from json files """

    # resolve subdir relative to this file directory
    fpath = pathlib.Path(__file__).parent.resolve()
    subdir_abs = pathlib.Path(fpath, subdir)

    if not json_sub_msgs:
        json_sub_msgs = {}

    pathlist = pathlib.Path(subdir_abs).glob('*.json')
    for path in pathlist:
        filename = path.stem
        with open(str(path), encoding='utf-8') as json_file:
            data = json.load(json_file)
            json_sub_msgs[filename] = data

    return json_sub_msgs


def loop_in_thread(ws_uri, msgs, db_uri):

    """ asyncio loop in separate thread """

    first_key = next(iter(msgs))

    if 'op' in msgs[first_key]:
        if msgs[first_key]['op'] == "subscribe":
            event_loop_sub = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop_sub)
            event_loop_sub.run_until_complete(
                    update_sensor_readings(ws_uri, msgs, db_uri))
        elif msgs[first_key]['op'] == "publish":
            event_loop_pub = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop_pub)
            event_loop_pub.run_until_complete(
                    send_control_inputs(ws_uri, msgs, db_uri))
        else:
            print("[ERROR] operation " + str(msgs[first_key]['op']) + " \
not recognised")

    else:
        print("[ERROR] failed to initiate thread since messages do not \
contain an operation type (op)")


#=====================================================================
# Main class
#=====================================================================

class Turtlebot():

    """ Turtlebot base class """

    def __init__(self, d_user_config=None):

        """ turtlebot constructor, and the defaut config will be merged with
            the config dict argument, to avoid unset values
        """

        self._config = D_CONFIG_DEFAULT
        self.db_con_sensor = None
        self.db_con_control = None
        self._pose = {
                "init_from_tb_odom": {
                    "x": None,
                    "y": None,
                    "th": None
                    },
                "current_from_tb_odom": {
                    "x": None,
                    "y": None,
                    "th": None
                    }
                }
        if d_user_config:
            self._config = {**self._config, **d_user_config}

        self._config['sub-msgs'] = \
                get_json_msgs(self._config['msg-sub-dir'])
        self._config['pub-msgs'] = \
                get_json_msgs(self._config['msg-pub-dir'])

        self._config['ws_uri'] = "ws://" + self._config['ws_host'] + ":" + \
                str(self._config['ws_port'])

        # in-memory DB
        # <https://docs.python.org/3/library/sqlite3.html>
        # <https://stackoverflow.com/a/3172950>
        # <https://charlesleifer.com/blog/going-fast-with-sqlite-and-python/>

        self.__create_sensor_listener_tread()
        self.__create_control_thread()
        self.__await_sensor_stream()
        self.set_control_inputs(0,0)

    def __create_sensor_listener_tread(self):

        self.db_con_sensor = sqlite3.connect(
                        self._config['sqlite-sensor-uri'],
                        uri=True, isolation_level=None)
        self.db_con_sensor.cursor().execute("""
CREATE TABLE sensor_readings (topic TEXT, msg TEXT);""")
        self.db_con_sensor.cursor().execute("""
CREATE TABLE status (process TEXT, code INTEGER , msg TEXT);""")
        self.db_con_sensor.cursor().execute("""
INSERT INTO status VALUES (?, ?, ?);""",
                                        ("main",
                                         StatusMainProcess.RUNNING.value,
                                         "Program initiated"
                                         ))
        self.db_con_sensor.cursor().execute("""
INSERT INTO status VALUES (?, ?, ?);""",
                                        ("sensors",
                                         StatusSensorMsgs.INITIALISING.value,
                                         "Initialising sensos consumer"
                                         ))


        # self.db_con.commit() # autocommit is on

        thread = threading.Thread(target=loop_in_thread,
                                  args=(self._config['ws_uri'],
                                       self._config['sub-msgs'],
                                       self._config['sqlite-sensor-uri'] ))

        thread.daemon = True
        thread.start()

    def __create_control_thread(self):

        self.db_con_control = sqlite3.connect(
                        self._config['sqlite-control-uri'],
                        uri=True, isolation_level=None)
        self.db_con_control.cursor().execute("""
CREATE TABLE control_inputs (linear_vel REAL, angular_vel REAL);""")

        thread = threading.Thread(target=loop_in_thread,
                                 args=(self._config['ws_uri'],
                                 self._config['pub-msgs'],
                                 self._config['sqlite-control-uri'] ))

        thread.daemon = True
        thread.start()

    def __await_sensor_stream(self, sleep=0.05, timeout=5):

        """ Wait until turtlebot is accepting sensor data and ready to
            send message to the ROS bridge """

        print("[INFO] initialising sensor stream...")

        for topic in self._config['sub-msgs']:
            t_start = time.time()
            while True:
                if time.time() - t_start > timeout:
                    print(f"[WARN] timeout reached when trying to get \
data from topic '{topic}'. Got 'None', which will likely propagate to \
API 'getters' related to this topic")
                    break
                query = f"SELECT msg FROM sensor_readings WHERE topic \
== '{topic}' ORDER BY rowid DESC LIMIT 1;"
                res = db_query_select(self.db_con_sensor, query,
                                      as_json=True,
                                      print_warnings=False)
                if res:
                    if topic == "odom":
                        orientation = res['pose']['pose']['orientation']
                        _, _, z_eul = \
                                quaternion_to_euler_angle_vectorized(
                                        float(orientation['w']),
                                        float(orientation['x']),
                                        float(orientation['y']),
                                        float(orientation['z']))
                        self._pose['init_from_tb_odom']['x'] = \
                            res['pose']['pose']['position']['x']
                        self._pose['init_from_tb_odom']['y'] = \
                            res['pose']['pose']['position']['y']
                        self._pose['init_from_tb_odom']['th'] = z_eul

                    break
                time.sleep(sleep)

        self.db_con_sensor.cursor().execute("""
INSERT INTO status VALUES (?, ?, ?);""",
                                        ("sensors",
                                         StatusSensorMsgs.SUBSCRIBED.value,
                                         "Subscribed to sensors"
                                         ))
        print("[INFO] Go!")

    @classmethod
    def __check_control_limits(cls, lin_vel, ang_vel,
                               lin_vel_max=TB_LIMIT_LIN_VEL,
                               ang_vel_max=TB_LIMIT_ANG_VEL):

        """ check control limits """

        if np.abs(lin_vel) > lin_vel_max:
            print(f"[WARN] linear velocity control limit exceeded \
    ({lin_vel_max} m/s). Setting to maximum...")
            lin_vel = np.sign(lin_vel)*lin_vel_max
        if np.abs(ang_vel) > ang_vel_max:
            print(f"[WARN] angular velocity control limit exceeded \
    ({ang_vel_max} rad/s). Setting to maximum...")
            ang_vel = np.sign(ang_vel)*ang_vel_max

        return lin_vel, ang_vel

    def get_tick_to_rad(self):

        """ returns tick to radians conversion factor
        """

        return self._config['tb_ttr']

    def get_imu(self):

        """ get IMU sensor reading
           <http://docs.ros.org/en/lunar/api/sensor_msgs/html/msg/Imu.html>
        """

        query = """
SELECT msg FROM sensor_readings
WHERE topic == 'imu'
ORDER BY rowid DESC LIMIT 1;"""

        return db_query_select(self.db_con_sensor, query, as_json=True)

    def get_imu_angle(self):

        """ get IMU euler angle in degrees """

        query = """
SELECT msg FROM sensor_readings
WHERE topic == 'imu'
ORDER BY rowid DESC LIMIT 1;"""

        d_res = db_query_select(self.db_con_sensor, query, as_json=True)
        if d_res:
            _, _, z_eul = quaternion_to_euler_angle_vectorized(
                    float(d_res['orientation']['w']),
                    float(d_res['orientation']['x']),
                    float(d_res['orientation']['y']),
                    float(d_res['orientation']['z']))
            return z_eul

        print("[WARN] failed to derive IMU angle from quaternion")
        print("[WARN] Query result = None")

        return None

    # def get_cmd_vel(self):

        # """ @Deprecated get current cmd_vel reading """

        # query = """
# SELECT msg FROM sensor_readings
# WHERE topic == 'cmd_vel'
# ORDER BY rowid DESC LIMIT 1;"""

        # return db_query_select(self.db_con_sensor, query, as_json=True)

    def get_sensor_state(self):

        """ get current sensor state reading """

        query = """
SELECT msg FROM sensor_readings
WHERE topic == 'sensor_state'
ORDER BY rowid DESC LIMIT 1;"""

        return db_query_select(self.db_con_sensor, query, as_json=True)

    def get_odom(self):

        """ get current built-in odometry computation """

        query = """
SELECT msg FROM sensor_readings
WHERE topic == 'odom'
ORDER BY rowid DESC LIMIT 1;"""

        return db_query_select(self.db_con_sensor, query, as_json=True)

    def get_pose_from_odom(self):

        """ get current built-in odometry computation, corrected based on
            starting point """

        query = """
SELECT msg FROM sensor_readings
WHERE topic == 'odom'
ORDER BY rowid DESC LIMIT 1;"""

        res = db_query_select(self.db_con_sensor, query, as_json=True)
        th_cur = self.get_imu_angle()
        th_init = self._pose['init_from_tb_odom']['th']
        pos = res['pose']['pose']['position']

        self._pose['current_from_tb_odom']['x'] = pos['x'] - \
                self._pose['init_from_tb_odom']['x']
        self._pose['current_from_tb_odom']['y'] = pos['y'] - \
                self._pose['init_from_tb_odom']['y']
        theta = th_cur - th_init
        theta = (theta + 180) % 360 - 180
        # theta = theta/180*np.pi
        self._pose['current_from_tb_odom']['th'] = theta
        # alternative:
               # np.arctan2(np.sin(th_cur - th_init ),
                          # np.cos(th_cur - th_init))

        return self._pose['current_from_tb_odom']

    def get_scan(self):

        """ get current lidar scan reading """

        query = """
SELECT msg FROM sensor_readings
WHERE topic == 'scan'
ORDER BY rowid DESC LIMIT 1;"""

        return db_query_select(self.db_con_sensor, query, as_json=True)


    def get_encoder_thicks(self):

        """ derive encoder thicks from sensor state """

        res = None

        query = """
SELECT msg FROM sensor_readings
WHERE topic == 'sensor_state'
ORDER BY rowid DESC LIMIT 1;"""

        sensor_state = db_query_select(self.db_con_sensor, query,
                                       as_json=True)
        if sensor_state:
            res = {"left": sensor_state['left_encoder'],
                   "right": sensor_state['right_encoder']
                   }

        return res

    def set_control_inputs(self, lin_vel, ang_vel):

        """ set control inputs (in database) """

        lin_vel, ang_vel = self.__check_control_limits(lin_vel, ang_vel)

        if CHANGE_ANG_VEL_DIR:
            ang_vel = -ang_vel

        query = "INSERT INTO control_inputs VALUES (?, ?);"
        val_tup = (float(lin_vel), float(ang_vel))
        db_query_insert(self.db_con_control, query, val_tup)

    def stop_moving(self):

        """ Set robot input back to zero """

        self.set_control_inputs(0,0)

    def stop(self):

        """ close connections and threads (brute force) """

        self.set_control_inputs(0,0)
        print("[INFO] closing all connections, exiting gracefully. Bye!")
        time.sleep(1)
        sys.exit()


# ==================================================
# Main
# ==================================================

if __name__ == '__main__':

    # test

    tb = Turtlebot()
    try:
        # print(json.dumps((tb.config), sort_keys=True, indent=2))
        # while True:
            # tb.get_imu()
            # tb.get_imu_angle()
            # tb.get_sensor_state()
            # tb.get_odom()
        # print(tb.get_odom())
        print(tb.get_scan())
        tb.set_control_inputs(0.08, 0)
        # time.sleep(2.5)
        # tb.set_control_inputs(0.05, 0.5)
        # time.sleep(2.5)
        # tb.set_control_inputs(0.05, 0)
        time.sleep(5)
        print(tb.get_pose_from_odom())
        tb.stop()
    except KeyboardInterrupt:
        tb.stop()
