###############################################################################
# (c) 2005-2019 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

from sys import path as sysPath
from os import path as osPath
filepath = osPath.dirname(osPath.realpath(__file__))
sysPath.append(filepath + "/../../../")
import rticonnextdds_connector as rti

with rti.open_connector("MyParticipantLibrary::MyOutputParticipant", filepath + "/../ShapeExample.xml") as connector:

    # Waits until the_output matches with a subscription named subscription_name
    def wait_for_discovery(the_output, subscription_name):
        print("Waiting to match with " + subscription_name)
        matches = []
        while {'name': subscription_name} not in matches:
            # wait_for_publications returns the change in matches since it was last called
            changes_in_matches = the_output.wait_for_subscriptions(2000)
            if changes_in_matches > 0:
                # get_matched_publications returns a list of all matched writers
                matches = the_output.get_matched_subscriptions()
        for match in matches:
            print("Matched with: %s" % match["name"])

    dds_output = connector.get_output("MyPublisher::MySquareWriter")

    # Wait for discovery to occur
    wait_for_discovery(dds_output, "MySquareReader")

    for i in range(1, 500):
        print("Writing sample %d" % i)
        # We can set the data into the sample in a variety of ways:
        # 1. Indexing it directly:
        dds_output.instance['x'] = i
        dds_output.instance['shapesize'] = 30
        # 2. Using the set_X APIs:
        dds_output.instance.set_number("y", i*2)
        dds_output.instance.set_string("color", "BLUE")
        # Write the data using the write() API
        dds_output.write()
        # Wait for all the matched subscriptions to acknowledge the sample
        dds_output.wait(2000)