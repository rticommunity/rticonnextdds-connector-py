###############################################################################
# (c) 2005-2019 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

"""A simple reader application.

This example shows how to create a simple reader application using RTI Connector.
This script is written to receive data from the matching publication defined
in the writer.py script. It is also possible to receive data from rtishapesdemo
using this script.
"""

from sys import path as sysPath
from os import path as osPath
filepath = osPath.dirname(osPath.realpath(__file__))
sysPath.append(filepath + "/../../../")
import rticonnextdds_connector as rti

# The Connector object will be automatically deleted
with rti.open_connector("MyParticipantLibrary::MyParticipant", filepath + "/../ShapeExample.xml") as connector:

    # Waits until the_input matches with a publication named publication_name
    def wait_for_discovery(the_input, publication_name):
        print("Waiting to match with " + publication_name)
        matches = []
        while {'name': publication_name} not in matches:
            # wait_for_publications returns the change in matches since it was last called
            changes_in_matches = the_input.wait_for_publications(2000)
            if changes_in_matches > 0:
                # get_matched_publications returns a list of all matched writers
                matches = the_input.get_matched_publications()
        for match in matches:
            print("Matched with: %s" % match["name"])

    # Obtain the input which we use to receive data
    dds_input = connector.get_input("MySubscriber::MySquareReader")

    wait_for_discovery(dds_input, "MySquareWriter")

    for i in range(1, 500):
        # Wait for data to be available on the input
        dds_input.wait(2000)
        # Take the data, removing it from the queue
        dds_input.take()
        for sample in dds_input.valid_data_iterator:
            # There are a variety of methods available for obtaining the data:
            # 1. Index the sample using the field name
            x = sample['x']
            # 2. Obtain a dictionary of the sample using get_dictionary()
            the_dict = sample.get_dictionary()
            y = the_dict['y']
            color = the_dict['color']
            # 3. Obtain the value directly use the get_X APIs
            size = sample.get_number("shapesize")
            print("Received x: %d, y: %d, size: %d, color: %s" % (x, y, size, color))
