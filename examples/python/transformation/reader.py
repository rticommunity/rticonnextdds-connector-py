###############################################################################
# (c) 2019 Copyright, Real-Time Innovations.  All rights reserved.            #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

"""Reads and prints the Circle topic"""

from __future__ import print_function
from sys import path as sys_path
from os import path as os_path

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")

import rticonnextdds_connector as rti

with rti.open_connector(
        config_name="MyParticipantLibrary::CircleSubParticipant",
        url=file_path + "/../ShapeExample.xml") as connector:

    input = connector.get_input("MySubscriber::MyCircleReader")

    for i in range(1, 500):
        input.wait() # wait for data on this input
        input.take()
        for sample in input.samples.valid_data_iter:
            print("Received circle: " + str(sample.get_dictionary()))
