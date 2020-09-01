###############################################################################
# (c) 2020 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

import pytest,time,sys,os,ctypes,json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
import rticonnextdds_connector as rti
from test_utils import send_data, wait_for_data, open_test_connector
import threading

# In order to be able to catch failures in threads, we need to wrap the
# threading.Thread class such that it re-raises exceptions
class RtiTestThread(threading.Thread):
    def __init__(self, target):
        threading.Thread.__init__(self, target=target)
        self.error = None

    def run(self):
        try:
            threading.Thread.run(self)
        except BaseException as e:
            self.error = e

    def join(self, timeout=None):
        super(RtiTestThread, self).join(timeout)
        if self.error is not None:
            raise self.error

class TestThreading:
  """
  Connector is not thread-safe, meaning that it is not supported to make concurrent
  calls to the native library. However, protecting these calls with a 3rd-party
  threading library  (such as Python's 'Threading') is supported. Here we test
  that this works as intended.
  """

  # In this test we create two Connector objects in separate threads. From one
  # of the connectors we create an input, from the other an output and check
  # that communication can occur.
  # In order to ensure we are testing for CON-163 bug, the XML file does not
  # contain a <participant_qos> tag.
  def test_creation_of_multiple_connectors(self):
    sem = threading.Semaphore()
    xml_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../xml/TestConnector3.xml")
    def outputThread():
        connector = None
        try:
            sem.acquire(True)
            connector = rti.Connector("MyParticipantLibrary::MyPubParticipant", xml_path)
            assert connector is not None
            the_output = connector.getOutput("MyPublisher::MySquareWriter")
            sem.release()
            assert the_output is not None
        finally:
            if connector is not None:
                connector.delete()

    def inputThread():
        connector = None
        try:
            sem.acquire(True)
            connector = rti.Connector("MyParticipantLibrary::MySubParticipant", xml_path)
            assert connector is not None
            the_input = connector.getInput("MySubscriber::MySquareReader")
            sem.release()
            assert the_input is not None

        finally:
            if connector is not None:
                connector.delete()

    input_thread = RtiTestThread(inputThread)
    output_thread = RtiTestThread(outputThread)
    input_thread.start()
    output_thread.start()
    input_thread.join(5000)
    output_thread.join(5000)
