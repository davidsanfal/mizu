import PyKDL as kdl
import numpy as np
import serial
import math
import time
from serial.serialutil import SerialException
import pygame


SLEEP_TIME = 0.02


class MizuLeg(object):
    def __init__(self, direction, angle, name):
        self.name = name
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
        self.time = 0

    def step(self, length=500, height=120, y=300, z=-120, cicle=4, phase=0, direction=1):
        speed_down = int((cicle*0.75)/SLEEP_TIME)
        speed_up = int((cicle*0.25)/SLEEP_TIME)
        delta_z = height*math.sin(self.time + phase)
        x = (length/2) * math.cos(self.time + phase) * math.sin(self.angle)
        final_y = y + x * math.cos(math.pi/4)
        final_x = x
        if self.name == 1 or self.name == 3:
            final_x = (length/2) * math.cos(self.time + phase) * math.sin(self.angle)
            final_y = y + final_x * math.cos(self.angle)
        else:
            final_x = (length/2) * math.cos(self.time + phase) * math.cos(self.angle)
            final_y = y + final_x * math.sin(self.angle)
        delta_t = math.pi/speed_down if delta_z < 0 else math.pi/speed_up
        delta_z = 0 if delta_z < 0 else delta_z
        self.time += delta_t*direction*self.direction
        target_frame = kdl.Frame(kdl.Vector(final_x, final_y, delta_z + z))
        current_angles = kdl.JntArray(self.chain.getNrOfJoints())
        result_angles = kdl.JntArray(self.chain.getNrOfJoints())

        self.ik_solver.CartToJnt(current_angles, target_frame, result_angles)

        result_angles[0] = np.rad2deg(result_angles[0])
        result_angles[1] = np.rad2deg(result_angles[1])
        result_angles[2] = np.rad2deg(result_angles[2])

        return result_angles, delta_z


class Mizu(object):

    def __init__(self, port):
        self.arduino_conn = serial.Serial(port, 19200)

        self.leg_1 = MizuLeg(direction=1, angle=math.pi/4, name=1)
        self.leg_2 = MizuLeg(direction=-1, angle=-math.pi/4, name=2)
        self.leg_3 = MizuLeg(direction=-1, angle=math.pi/4, name=3)
        self.leg_4 = MizuLeg(direction=1, angle=-math.pi/4, name=4)

    def walk(self, joystick, length=300, height=100, y=300, z=-200, cicle=8, direction=1):
        self.leg_1.time = 0
        self.leg_2.time = 0
        self.leg_3.time = 0
        self.leg_4.time = 0
        symmetrical = False
        walking = True
        weight = -0
        while walking:
            for _ in pygame.event.get():
                pass
            if joystick.get_button(0):
                angles = []
                gap = (5, 4, 6, 7)
                if symmetrical:
                    gap = (0, 6, 4, 6)
                _angles, _z = self.leg_1.step(length, height, y + weight, z,
                                              cicle, (gap[0]*math.pi)/4, direction)
                if _z:
                    weight = 0
                angles += _angles
                _angles, _z = self.leg_2.step(length, height, y - weight, z,
                                              cicle, (gap[1]*math.pi)/4, direction)
                if _z:
                    weight = -0
                angles += _angles
                _angles, _z = self.leg_3.step(length, height, y - weight, z,
                                              cicle, (gap[2]*math.pi)/4, direction)
                if _z:
                    weight = -0
                angles += _angles
                _angles, _z = self.leg_4.step(length, height, y + weight, z,
                                              cicle, (gap[3]*math.pi)/4, direction)
                if _z:
                    weight = 0
                angles += _angles
                msg = [chr(190)]
                aux = []
                for angle in angles:
                    msg.append(chr(int(angle+90)))
                    aux.append(int(angle+90))
                msg.append(chr(192))
                print aux
                self.arduino_conn.write(bytearray(msg))
                time.sleep(SLEEP_TIME)
                walking = True

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
mizu = None
for i in range(20):
    try:
        mizu = Mizu('/dev/rfcomm%s' % i)
        print "connected in port: /dev/rfcomm%s" % i
        break
    except SerialException:
        pass
if mizu:
    mizu.walk(joystick)
