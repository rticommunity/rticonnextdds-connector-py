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

    dds_input.wait_for_match()
    print("match found 1")
    dds_input.wait_for_match()
    print("match found 2")
    dds_input.wait_for_match()
    print("match found 3")

    sleep(2)
