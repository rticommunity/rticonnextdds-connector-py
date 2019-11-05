###############################################################################
# (c) 2019 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

"""Publishes random images"""

from sys import path as sys_path
from os import path as os_path
from os import getpid
from time import sleep
import numpy as np, random

# Updating the system path is not required if you have pip-installed
# rticonnextdds-connector
file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")
import rticonnextdds_connector as rti

def random_rgb():
    """Generate a random RGB pixel"""
    return [int(255*random.random()), int(255*random.random()), int(255*random.random())]

def generate_random_image(size):
    """Generate a random flat list of pixels of 3 different colors"""
    random_colors = [random_rgb() for i in range(3)]
    pixels = np.array([random.choice(random_colors) for i in range(size)])
    return pixels.reshape(-1).tolist() # Flatten out and convert to list

def update_image(pixels, _iteration):
    """Shift 3 elements (one pixel)"""
    return pixels[3:] + pixels[:3]

with rti.open_connector(
        config_name="MyParticipantLibrary::ImagePubParticipant",
        url=file_path + "/ImagesExample.xml") as connector:

    output = connector.get_output("MyPublisher::ImageWriter")

    # Identify the source of the image with the process id
    output.instance["source"] = "ImageWriter " + str(getpid())
    current_pixels = generate_random_image(40 * 60)

    print("Writing...")
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

    # Note: we don't call output.wait() because this output is configured
    # with best-effort reliability, and therefore it won't wait for acknowledgments
    print("Exiting...")
