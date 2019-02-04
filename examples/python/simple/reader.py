###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

"""Samples's reader."""

from __future__ import print_function
from sys import path as sysPath
from os import path as osPath
from time import sleep
filepath = osPath.dirname(osPath.realpath(__file__))
sysPath.append(filepath + "/../../../")
import rticonnextdds_connector as rti



connector = rti.Connector("MyParticipantLibrary::Zero",
                          filepath + "/../ShapeExample.xml")
inputDDS = connector.getInput("MySubscriber::MySquareReader")

for i in range(1, 500):
    inputDDS.take()
    numOfSamples = inputDDS.samples.getLength()
    for j in range(0, numOfSamples):
        if inputDDS.infos.isValid(j):
            # This gives you a dictionary
            sample = inputDDS.samples.getDictionary(j)
            x = sample['x']
            y = sample['y']

            # Or you can just access the field directly
            size = inputDDS.samples.getNumber(j, "shapesize")
            color = inputDDS.samples.getString(j, "color")
            toPrint = "Received x: " + repr(x) + " y: " + repr(y) + \
                      " size: " + repr(size) + " color: " + repr(color)

            print(toPrint)
    sleep(2)
