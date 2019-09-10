###############################################################################
# (c) 2005-2019 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

"""Read a sample and write a new one.

This example reads a sample from a remote writer (either writer.py or rtishapesdemo),
modifies some of the fields in the data and writes it back out. To visualise what
is happening it is suggested to use rtishapesdemo:
Launch an instance of rtishapesdemo and subscribe to Squares.
In the same instance of rtishapesdemo publish Squares (with any color other than
Purple).
Run this example. You will see that we are modifying the position and color of
the received data.
"""

from sys import path as sysPath
from os import path as osPath
from time import sleep
filepath = osPath.dirname(osPath.realpath(__file__))
sysPath.append(filepath + "/../../../")
import rticonnextdds_connector as rti

with rti.open_connector("MyParticipantLibrary::MyParticipant", filepath + "/../ShapeExample.xml") as connector:

    dds_output = connector.get_output("MyPublisher::MySquareWriter")
    dds_input = connector.get_input("MySubscriber::MySquareReader")

    # This example reads a sample received from a remote publication, modifies
    # the data in it and writes it back out. We need to wait until we discover
    # the remote writer and reader. We do not explicitly check publication_name or
    # subscription_name of the matched entity to allow this example to work
    # with other DDS applications (e.g., rtishapesdemo)
    total_matches = 0
    while total_matches < 2:
        # wait_for_publications can return a negative value if we unmatch
        new_matches = dds_input.wait_for_publications(2000)
        if new_matches > 0:
            total_matches += new_matches
    for match in dds_input.get_matched_publications():
        print("Matched publications: %s" % match["name"])
    total_matches = 0
    while total_matches < 2:
        # wait_for_publications can return a negative value if we unmatch
        new_matches = dds_output.wait_for_subscriptions(2000)
        if new_matches > 0:
            total_matches += new_matches
    for match in dds_output.get_matched_subscriptions():
        print("Matched subscriptions: %s" % match["name"])

    for i in range(1, 500):
        # Wait for data to arrive
        dds_input.wait(2000)
        # Take the data
        dds_input.take()
        for sample in dds_input.valid_data_iterator:
            # We don't want to take our own samples
            if sample['color'] != "PURPLE":
                dictionary = sample.get_dictionary()
                # Modify the data (x <-> y, color -> purple)
                dictionary['x'], dictionary['y'] = dictionary['y'], dictionary['x']
                dictionary['color'] = "PURPLE" 
                dds_output.instance.set_dictionary(dictionary)
                dds_output.write()

    # Wait for all matched readers to acknowledge the sample
    dds_output.wait(2000)
