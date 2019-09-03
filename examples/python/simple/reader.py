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


with rti.open_connector("MyParticipantLibrary::MyParticipant", filepath + "/../ShapeExample.xml") as connector:

    dds_input = connector.get_input("MySubscriber::MySquareReader")

    for i in range(1, 500):
        dds_input.take()
        for sample in dds_input.valid_data_iterator:
                # You can get all the fields in a get_dictionary()
                data = sample.get_dictionary()
                x = data['x']
                y = data['y']

                # Or you can access the field individually
                size = sample.get_number("shapesize")
                color = sample.get_string("color")
                print("Received x: " + repr(x) + " y: " + repr(y) + \
                        " size: " + repr(size) + " color: " + repr(color))

        sleep(2)
