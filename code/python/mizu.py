import PyKDL as kdl
import numpy as np
import serial
import math
import time


SLEEP_TIME = 0.02


class MizuLeg(object):
    def __init__(self, direction, angle):
        segment_0 = kdl.Segment(kdl.Joint(kdl.Joint.RotZ), kdl.Frame(kdl.Vector(0, 37.95, 0)))
        segment_1 = kdl.Segment(kdl.Joint(kdl.Joint.RotX), kdl.Frame(kdl.Vector(0, 342, 0)))
        segment_2 = kdl.Segment(kdl.Joint(kdl.Joint.RotX), kdl.Frame(kdl.Vector(0, 0, -290)))
        self.chain = kdl.Chain()
        self.chain.addSegment(segment_0)
        self.chain.addSegment(segment_1)
        self.chain.addSegment(segment_2)
        self.ik_solver = kdl.ChainIkSolverPos_LMA(self.chain)
        self.direction = direction
        self.angle = angle

    def step(self, length=500, height=120, y=300, z=-120, cicle=4, phase=0, time=0, direction=1):
        speed_down = int((cicle*0.75)/SLEEP_TIME)
        speed_up = int((cicle*0.25)/SLEEP_TIME)
        while True:
            delta_z = height*math.sin(time + phase)
            x = (length/2) * math.cos(time + phase) * math.sin(math.pi/4)
            delta_t = math.pi/speed_down if delta_z < 0 else math.pi/speed_up
            delta_z = 0 if delta_z < 0 else delta_z
            t += delta_t*direction
            final_y = y + x * math.cos(math.pi/4)
            target_frame = kdl.Frame(kdl.Vector(x, final_y, delta_z + z))
            current_angles = kdl.JntArray(leg.getNrOfJoints())
            result_angles = kdl.JntArray(leg.getNrOfJoints())

            ik_solver.CartToJnt(current_angles, target_frame, result_angles)

            result_angles[0] = np.rad2deg(result_angles[0])
            result_angles[1] = np.rad2deg(result_angles[1])
            result_angles[2] = np.rad2deg(result_angles[2])
            time.sleep(sleep_time)
            msg = "(%i,%i,%i)" % (result_angles[0],
                                  result_angles[1],
                                  result_angles[2])
            arduino_conn.write(msg)
            print msg


class Mizu(object):

    def __init__(self):
        self.arduino_conn = serial.Serial('/dev/ttyUSB0', 115200)

        self.leg_1 = MizuLeg(direction=1, angle=math.pi/4)
        self.leg_2 = MizuLeg(direction=1, angle=-math.pi/4)
        self.leg_3 = MizuLeg(direction=-1, angle=math.pi/4)
        self.leg_4 = MizuLeg(direction=-1, angle=-math.pi/4)

    def walk(self, cicle=4, direction=1):
        t = 0
        length = 500
        height = 120
        y = 300
        z = -120
        sleep_time = 0.02

        while True:
            pass

    def step(self, length=500, height=120, y=300, z=-120, cicle=4, phase=0, direction=1):
        t = phase
        sleep_time = 0.02

        speed_down = int((cicle*0.75)/sleep_time)
        speed_up = int((cicle*0.25)/sleep_time)
        while True:
            delta_z = height*math.sin(t)
            x = (length/2) * math.cos(t) * math.sin(math.pi/4)
            delta_t = math.pi/speed_down if delta_z < 0 else math.pi/speed_up
            delta_z = 0 if delta_z < 0 else delta_z
            t += delta_t*direction
            final_y = y + x * math.cos(math.pi/4)
            target_frame = kdl.Frame(kdl.Vector(x, final_y, delta_z + z))
            current_angles = kdl.JntArray(leg.getNrOfJoints())
            result_angles = kdl.JntArray(leg.getNrOfJoints())

            ik_solver.CartToJnt(current_angles, target_frame, result_angles)

            result_angles[0] = np.rad2deg(result_angles[0])
            result_angles[1] = np.rad2deg(result_angles[1])
            result_angles[2] = np.rad2deg(result_angles[2])
            time.sleep(sleep_time)
            msg = "(%i,%i,%i)" % (result_angles[0],
                                  result_angles[1],
                                  result_angles[2])
            arduino_conn.write(msg)
            print msg

