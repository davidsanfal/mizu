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


def step():
    t = 0
    for x in range(-250, 250, 25):
        z = -120 + 120*sin(t)
        t += pi/20
        target_frame = kdl.Frame(kdl.Vector(x, 300, z))
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

    for x in range(250, -250, -25):
        target_frame = kdl.Frame(kdl.Vector(x, 300, -120))
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
    step()
