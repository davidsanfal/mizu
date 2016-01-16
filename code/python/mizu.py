import PyKDL as kdl
import numpy as np
import serial
from time import sleep
from math import cos, sin, pi

arduino_conn = serial.Serial('/dev/ttyUSB0', 115200)

leg = kdl.Chain()

leg.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.RotZ),
                           kdl.Frame(kdl.Vector(0, 37.95, 0))))
leg.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.RotX),
                           kdl.Frame(kdl.Vector(0, 342, 0))))
leg.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.RotX),
                           kdl.Frame(kdl.Vector(0, 0, -290))))
ik_solver = kdl.ChainIkSolverPos_LMA(leg)

# 0.0 45.0 315.0
t = 0


def circle():
    t += pi/30
    x = 150*cos(t)
    y = 300 + 150*sin(t)
    target_frame = kdl.Frame(kdl.Vector(x, y, -90))
    current_angles = kdl.JntArray(leg.getNrOfJoints())
    result_angles = kdl.JntArray(leg.getNrOfJoints())

    ik_solver.CartToJnt(current_angles, target_frame, result_angles)

    result_angles[0] = np.rad2deg(result_angles[0])
    result_angles[1] = np.rad2deg(result_angles[1])
    result_angles[2] = np.rad2deg(result_angles[2])
    sleep(0.05)
    msg = "(%i,%i,%i)" % (result_angles[0],
                          result_angles[1],
                          result_angles[2])
    arduino_conn.write(msg)


def step(length=500, height=120, y=300, z=-120, cicle=4, phase=0, direction=1):
    t = phase
    sleep_time = 0.02

    speed_down = int((cicle*0.75)/sleep_time)
    speed_up = int((cicle*0.25)/sleep_time)
    while True:
        delta_z = height*sin(t)
        x = (length/2) * cos(t) * sin(pi/4)
        delta_t = pi/speed_down if delta_z < 0 else pi/speed_up
        delta_z = 0 if delta_z < 0 else delta_z
        t += delta_t*direction
        final_y = y + x * cos(pi/4)
        target_frame = kdl.Frame(kdl.Vector(x, final_y, delta_z + z))
        current_angles = kdl.JntArray(leg.getNrOfJoints())
        result_angles = kdl.JntArray(leg.getNrOfJoints())

        ik_solver.CartToJnt(current_angles, target_frame, result_angles)

        result_angles[0] = np.rad2deg(result_angles[0])
        result_angles[1] = np.rad2deg(result_angles[1])
        result_angles[2] = np.rad2deg(result_angles[2])
        sleep(sleep_time)
        msg = "(%i,%i,%i)" % (result_angles[0],
                              result_angles[1],
                              result_angles[2])
        arduino_conn.write(msg)
        print msg


def line():
    for x in range(-250, 250, 10):
        target_frame = kdl.Frame(kdl.Vector(x, 300, -90))
        current_angles = kdl.JntArray(leg.getNrOfJoints())
        result_angles = kdl.JntArray(leg.getNrOfJoints())

        ik_solver.CartToJnt(current_angles, target_frame, result_angles)

        result_angles[0] = np.rad2deg(result_angles[0])
        result_angles[1] = np.rad2deg(result_angles[1])
        result_angles[2] = np.rad2deg(result_angles[2])
        sleep(0.05)
        msg = "(%i,%i,%i)" % (result_angles[0],
                              result_angles[1],
                              result_angles[2])
        arduino_conn.write(msg)

    for x in range(250, -250, -10):
        target_frame = kdl.Frame(kdl.Vector(x, 300, -90))
        current_angles = kdl.JntArray(leg.getNrOfJoints())
        result_angles = kdl.JntArray(leg.getNrOfJoints())

        ik_solver.CartToJnt(current_angles, target_frame, result_angles)

        result_angles[0] = np.rad2deg(result_angles[0])
        result_angles[1] = np.rad2deg(result_angles[1])
        result_angles[2] = np.rad2deg(result_angles[2])
        sleep(0.05)
        msg = "(%i,%i,%i)" % (result_angles[0],
                              result_angles[1],
                              result_angles[2])
        arduino_conn.write(msg)

while True:
    step(length=500, height=120, y=300, z=-80, cicle=4, phase=pi/2, direction=1)
