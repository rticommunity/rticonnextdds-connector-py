###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

"""Reads images and saves them into a file"""

from __future__ import print_function
from sys import path as sys_path
from os import path as os_path
from time import sleep
import matplotlib.pyplot as plot
import matplotlib
import numpy

# Updating the system path is not required if you have pip-installed
# rticonnextdds-connector
file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")
import rticonnextdds_connector as rti

matplotlib.use('Agg') # Non-GUI backend

with rti.open_connector(
        config_name="MyParticipantLibrary::ImageSubParticipant",
        url=file_path + "/ImagesExample.xml") as connector:

    # Create a blank image
    fig = plot.figure()
    blank_image = plot.imshow(numpy.zeros((40, 60, 3)))

    input = connector.get_input("MySubscriber::ImageReader")

    while True:
        input.read()
        for sample in input.samples.valid_data_iter:
            # Get the received pixels (a linear sequence)
            raw_pixels = numpy.array(sample["pixels"])

            # Convert the linear sequence of pixels into an Height x Width x 3
            # matrix of RGB pixels that we can draw with imgshow
            image_dim = (
                int(sample["resolution.height"]),
                int(sample["resolution.width"]),
                3)
            structured_pixels = raw_pixels.reshape(image_dim)

            # Draw and save the image
            image = plot.imshow(structured_pixels)
            plot.savefig('image.png')

            sleep(.5) # Poll every half second
