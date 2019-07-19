###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

"""Reader using the wait call."""

from __future__ import print_function
from sys import path as sysPath
from os import path as osPath
from time import sleep
filepath = osPath.dirname(osPath.realpath(__file__))
sysPath.append(filepath + "/../../../")
import rticonnextdds_connector as rti

connector = rti.Connector("MyParticipantLibrary::MyParticipant",
                          filepath + "/../Mixed.xml")
inputDDS = connector.get_input("MySubscriber::MySquareReader")

for i in range(1, 500):
    timeout = -1
    print("Calling wait with a timeout of " + repr(timeout))
    ret = connector.wait(timeout)
    print("The wait returned " + repr(ret))
    inputDDS.take()
    numOfSamples = inputDDS.samples.getLength()
    for j in range(0, numOfSamples):
        if inputDDS.infos.isValid(j):
            """There are two alternative way to access the sample...
            1) get it as a dictionary and then access the field in the
            standard python way:"""
            sample = inputDDS.samples.getDictionary(j)
            x = sample['x']
            color = sample['color']

            # 2) access each single field with the connector API:
            x = inputDDS.samples.getNumber(j, "x")
            color = inputDDS.samples.getString(j, "color")

            # This is how you get the size of a seqence:
            seqLength = inputDDS.samples.getNumber(j, "aOctetSeq#")
            print("Received a sequence with " + repr(seqLength) + " elements")

            # Print the sample
            print(sample)
    sleep(2)
