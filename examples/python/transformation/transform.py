###############################################################################
# (c) Copyright, Real-Time Innovations, 2019.  All rights reserved.           #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

"""Reads Squares, transforms them and writes them as Circles."""

from sys import path as sys_path
from os import path as os_path

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")
import rticonnextdds_connector as rti

with rti.open_connector(
    config_name = "MyParticipantLibrary::TransformationParticipant",
    url = file_path + "/../ShapeExample.xml") as connector:

    input = connector.get_input("MySubscriber::MySquareReader")
    output = connector.get_output("MyPublisher::MyCircleWriter")

    # Read data from the input, transform it and write it into the output
    print("Waiting for data...")
    while True:
        input.wait() # Wait for data in the input
        input.take()
        for sample in input.valid_data_iterator:
            data = sample.get_dictionary()

            data["x"], data["y"] = data["y"], data["x"]
            data["color"] = "RED"

            output.instance.set_dictionary(data)
            output.write()
