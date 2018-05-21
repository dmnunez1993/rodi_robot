#!/usr/bin/env python

from rospy import logdebug
from httplib import HTTPConnection

MAX_MIN_WHEEL_VELOCITY = 100

COMMAND_ENTRYPOINT = 3
SEE_ENTRYPOINT = 8


class Transport(object):
    def __init__(self, hostname='192.168.4.1', port='1234'):
        self.hostname = hostname
        self.port = port

    def send_command(self, params):
        request = "/" + "/".join(map(str, params))

        try:
            self.conn = HTTPConnection(
                self.hostname, port=self.port, timeout=0.1)
            self.conn.request("GET", request)
            response = self.conn.getresponse().read()
            self.conn.close()
            if len(response) == 0:
                return None
            return response
        except Exception as e:
            logdebug("the HTTP request " + request + " failed: " + str(e))
            return None

    def clamp_velocity(self, velocity):
        if velocity > MAX_MIN_WHEEL_VELOCITY:
            return MAX_MIN_WHEEL_VELOCITY
        if velocity < (-1) * MAX_MIN_WHEEL_VELOCITY:
            return (-1) * MAX_MIN_WHEEL_VELOCITY

        return velocity

    def move(self, left_wheel_speed, right_wheel_speed):
        self.send_command([
            COMMAND_ENTRYPOINT,
            self.clamp_velocity(left_wheel_speed),
            self.clamp_velocity(right_wheel_speed)
        ])

    def move_forward(self):
        self.send_command([COMMAND_ENTRYPOINT, 100, 100])

    def move_reverse(self):
        self.send_command([COMMAND_ENTRYPOINT, -100, -100])

    def move_left(self):
        self.send_command([COMMAND_ENTRYPOINT, -100, 100])

    def move_right(self):
        self.send_command([COMMAND_ENTRYPOINT, 100, -100])

    def stop(self):
        self.send_command([COMMAND_ENTRYPOINT, 0, 0])

    def see(self):
        return self.send_command([SEE_ENTRYPOINT])
