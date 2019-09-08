###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

import pytest,sys,os,ctypes
sys.path.append(os.path.dirname(os.path.realpath(__file__))+ "/../../")
import rticonnextdds_connector as rti
from test_utils import open_test_connector, wait_for_data

class TestInput:
  """
  This class tests the correct instantiation of
  :class:`rticonnextdds_connector.Input` object.

  .. todo::

       * Move :func:`rticonnextdds_connector.Input.wait` to
         :class:`rticonnextdds_connector.Connector`

  """

  def test_invalid_DR(self,rtiConnectorFixture):
    """
    This test function ensures that a ValueError is raised if
    an incorrect DataReader name is passed to the
    Input constructor.

    :param rtiConnectorFixture: :func:`conftest.rtiConnectorFixture`
    :type rtiConnectorFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    """
    invalid_DR = "InvalidDR"
    with pytest.raises(rti.Error):
       rtiConnectorFixture.getInput(invalid_DR)

  def test_creation_DR(self,rtiInputFixture):
    """
    This function tests the correct instantiation of
    Input object.

    :param rtiInputFixture: :func:`conftest.rtiInputFixture`
    :type rtiInputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_
    """
    assert rtiInputFixture!=None and isinstance(rtiInputFixture,rti.Input) \
      and rtiInputFixture.name == "MySubscriber::MySquareReader" \
      and isinstance(rtiInputFixture.connector,rti.Connector) \
      and isinstance(rtiInputFixture.samples,rti.Samples) \
      and isinstance(rtiInputFixture.infos,rti.Infos)

  def test_reader_native_call(self, rtiInputFixture):
    get_topic = rti.connector_binding.library.DDS_DataReader_get_topicdescription
    get_topic.restype = ctypes.c_void_p
    get_topic.argtypes = [ctypes.c_void_p]
    topic = get_topic(rtiInputFixture.native)

    get_name = rti.connector_binding.library.DDS_TopicDescription_get_name
    get_name.restype = ctypes.c_char_p
    get_name.argtypes = [ctypes.c_void_p]
    assert rti.fromcstring(get_name(topic)) == "Square"

  def test_no_autoenable(self):
    with open_test_connector("MyParticipantLibrary::TestNoAutoenableSubscriber") as connector:
      output = connector.get_output("TestPublisher::TestWriter")
      connector.wait(1000) # TODO

      # The input is not enabled yet because the subscriber sets
      # autoenable_created_entities to false
      output.instance['x'] = 1
      output.write()

      # Connector enables the DataReader when it's first looked up
      input = connector.get_input("TestSubscriber::TestReader")
      connector.wait(1000) # TODO wait for discovery
      output.instance['x'] = 2
      output.write()

      # The input will receive only the second sample
      wait_for_data(input)
      assert input.sample_count == 1
      assert input[0]['x'] == 2
