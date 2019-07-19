###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################


"""Samples's writer."""

from sys import path as sysPath
from os import path as osPath
from time import sleep
filepath = osPath.dirname(osPath.realpath(__file__))
sysPath.append(filepath + "/../../../")
import rticonnextdds_connector as rti

connector = rti.Connector("MyParticipantLibrary::MyParticipant",
                          filepath + "/../Mixed.xml")
outputDDS = connector.get_output("MyPublisher::MySquareWriter")

for i in range(1, 500):
    """We clear the instance associated to this output
    otherwise the sample will have the values set in the
    previous iteration"""
    outputDDS.clear_members()

    # Here an example on how to set the members of a sequence of complex types
    outputDDS.instance.set_number("innerStruct[1].x", i)
    outputDDS.instance.set_number("innerStruct[2].x", i+1)

    # Here an example on how to set a string
    outputDDS.instance.set_string("color", "BLUE")

    # Here an example on how to set a number
    outputDDS.instance.set_number("x", i)

    """Here we are going to set the elements of a sequence.
    - the sequence was declared with maxSize 30
    - we will always set two elements and..
    - ... the third element only half of the time

    If you open rtiddsspy you will see that the length is
    automatically set to the right value."""
    outputDDS.instance.set_number("aOctetSeq[1]", 42)
    outputDDS.instance.set_number("aOctetSeq[2]", 43)

    if i % 2 == 0:
        outputDDS.instance.set_number("aOctetSeq[3]", 44)
    # Now we write the sample
    outputDDS.write()
    sleep(2)
