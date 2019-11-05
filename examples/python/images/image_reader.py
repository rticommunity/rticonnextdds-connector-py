###############################################################################
# (c) Copyright, Real-Time Innovations, 2019. All rights reserved.            #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

"""Reads images and displays them"""

from __future__ import print_function
from sys import path as sys_path
from os import path as os_path
import matplotlib.pyplot as plot
import matplotlib.animation as animation
import numpy

# Updating the system path is not required if you have pip-installed
# rticonnextdds-connector
file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")
import rticonnextdds_connector as rti


with rti.open_connector(
        config_name="MyParticipantLibrary::ImageSubParticipant",
        url=file_path + "/ImagesExample.xml") as connector:

    # Create a blank image
    fig = plot.figure()
    fig.canvas.set_window_title("No image received")
    blank_image = plot.imshow(numpy.zeros((40, 60, 3)), animated=True)

    input = connector.get_input("MySubscriber::ImageReader")

    def read_and_draw(_frame):
        """The animation function, called periodically in a set interval, reads the
        last image received and draws it"""

        # The Qos configuration guarantees we will only have the last sample;
        # we read (not take) so we can access it again in the next interval if
        # we don't receive a new one
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

            # Draw the image
            image = plot.imshow(structured_pixels)

            # Set the title of the image
            fig.canvas.set_window_title("Image received from " + sample["source"])
            return image,
        return blank_image, # when we haven't received any image

    # Create the animation and show
    ani = animation.FuncAnimation(fig, read_and_draw, interval=500, blit=True)

    # Show the image and block until the window is closed
    plot.show()
    print("Exiting...")
