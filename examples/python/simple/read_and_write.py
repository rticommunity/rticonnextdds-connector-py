###############################################################################
# (c) 2005-2019 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

"""Read a sample and write a new one."""

from sys import path as sysPath
from os import path as osPath
filepath = osPath.dirname(osPath.realpath(__file__))
sysPath.append(filepath + "/../../../")
import rticonnextdds_connector as rti

with rti.open_connector("MyParticipantLibrary::MyParticipant", filepath + "/../ShapeExample.xml") as connector:

    dds_input = connector.get_input("MySubscriber::MySquareReader")
    dds_output = connector.get_output("MyPublisher::MySquareWriter")

    # This example reads a sample received from a remote publication, modifies
    # the data in it and writes it back out. We need to wait until we discover
    # the remote writer. We will internally match with the writer which we
    # have created above, but need an additional match.
    # total_matches = 0
    # while total_matches < 2:
    #     # wait_for_publications can return a negative value if we unmatch
    #     new_matches = dds_input.wait_for_publications(2000)
    #     if new_matches > 0:
    #         total_matches += new_matches

    for i in range(1, 5000):
        # Wait for data to arrive
        dds_input.wait(2000)
        # Take the data
        dds_input.take()
        for sample in dds_input.valid_data_iterator:
            # Obtain the dictionary of the sample
            dictionary = sample.get_dictionary()
            # Modify the data (x <-> y, color -> RED)
            # dictionary['x'], dictionary['y'] = dictionary['y'], dictionary['x']
            dictionary['color'] = "PURPLE" 
            dictionary['shapesize'] = dictionary['shapesize'] / 2
            dds_output.instance.set_dictionary(dictionary)
            dds_output.write()
            # Wait for all matched readers to acknowledge the sample
            dds_output.wait(2000)
