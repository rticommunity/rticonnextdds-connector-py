###############################################################################
# (c) 2019 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

"""Simple Square writer"""

from sys import path as sys_path
from os import path as os_path
from os import getpid
from time import sleep
import numpy as np

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")

import rticonnextdds_connector as rti

def update_image(pixels, iteration):
    pixels.insert(0, pixels.pop())
    return pixels

with rti.open_connector(
    config_name = "MyParticipantLibrary::ImagePubParticipant",
    url = file_path + "/ImagesExample.xml") as connector:

    output = connector.get_output("MyPublisher::ImageWriter")

    print("Waiting for subscriptions...")
    output.wait_for_subscriptions()

    print("Writing...")

    # Identify the source of the image with the process id
    output.instance["source"] = "ImageWriter " + str(getpid())
    current_pixels = [int(x * 255) for x in np.sin(np.random.random(40 * 60 * 3))]
    for i in range(1, 100):
        # Write images with different orientations
        if i % 10 != 0:
            output.instance.set_dictionary({"resolution":{"height":40, "width":60}})
        else:
            output.instance.set_dictionary({"resolution":{"height":60, "width":40}})

        # Create a new image
        current_pixels = update_image(current_pixels, i)
        output.instance.set_dictionary({"pixels":current_pixels})

        output.write()
        sleep(.5) # Write at a rate of one sample every 1 seconds, for ex.

    print("Exiting...")
    output.wait() # Wait for all subscriptions to receive the data before exiting