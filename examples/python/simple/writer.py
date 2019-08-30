###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

"""Samples's writer."""

from sys import path as sysPath
from os import path as osPath
from time import sleep
filepath = osPath.dirname(osPath.realpath(__file__))
sysPath.append(filepath + "/../../../")
import rticonnextdds_connector as rti

connector = rti.Connector("MyParticipantLibrary::MyParticipant",
                          filepath + "/../ShapeExample.xml")
outputDDS = connector.get_output("MyPublisher::MySquareWriter")

for i in range(1, 5):
    outputDDS.instance.set_number("x", i)
    outputDDS.instance.set_number("y", i*2)
    outputDDS.instance.set_number("shapesize", 30)
    outputDDS.instance.set_string("color", "BLUE")
    outputDDS.write()
    sleep(2)