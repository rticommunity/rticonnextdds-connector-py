###############################################################################
# (c) 2019 Copyright, Real-Time Innovations.  All rights reserved.            #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

import pytest,time,sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
import rticonnextdds_connector as rti
from test_utils import *

class TestDiscovery:
  """
  This class tests discovery between Connector entities.
  All the fixtures use scope-level of "function" to prevent unwanted interaction
  between tests.
  The entities used in the tests are defined in a different domain to those
  in other tests for the same reason.
  """

  @pytest.fixture(scope="function")
  def discovery_connector(self):
    xml_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "../xml/TestConnector.xml")
    participant_profile="MyParticipantLibrary::DiscoveryTest"

    with rti.open_connector(participant_profile, xml_path) as rti_connector:
        yield rti_connector

  @pytest.fixture(scope="function")
  def discovery_reader_only_connector(self):
    xml_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "../xml/TestConnector.xml")
    participant_profile="MyParticipantLibrary::DiscoveryTestReaderOnly"

    with rti.open_connector(participant_profile, xml_path) as rti_connector:
        yield rti_connector

  @pytest.fixture(scope="function")
  def discovery_writer_only_connector(self):
    xml_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "../xml/TestConnector.xml")
    participant_profile="MyParticipantLibrary::DiscoveryTestWriterOnly"

    with rti.open_connector(participant_profile, xml_path) as rti_connector:
        yield rti_connector

  @pytest.fixture(scope="function")
  def discovery_reader_only_input(self, discovery_reader_only_connector):
    return discovery_reader_only_connector.get_input("TestSubscriber::TestReader")

  @pytest.fixture(scope="function")
  def discovery_writer_only_output(self, discovery_writer_only_connector):
    return discovery_writer_only_connector.get_output("TestPublisher::TestWriter")

  def test_no_matches_input(self, discovery_reader_only_input):
    # We should not match with any outputs at this point
    matches = discovery_reader_only_input.get_matched_outputs()
    assert matches is None

    # We should timeout if we attempt to wait for a match
    with pytest.raises(rti.TimeoutError) as excinfo:
      change_in_matches = discovery_reader_only_input.wait_for_match(1)
      assert change_in_matches == 0

  def test_no_matches_output(self, discovery_writer_only_output):
    # We should not match with any outputs at this point
    matches = discovery_writer_only_output.get_matched_inputs()
    assert matches is None

    # We should timeout if we attempt to wait for a match
    with pytest.raises(rti.TimeoutError) as excinfo:
      change_in_matches = discovery_writer_only_output.wait_for_match(1)
      assert change_in_matches == 0

  def test_simple_matching(self, discovery_connector):
    the_input = discovery_connector.get_input("MySubscriber::MyReader")
    the_output = discovery_connector.get_output("MyPublisher::MyWriter")

    # Both the input and output should match each other (and nothing else)
    change_in_matches = the_input.wait_for_match(2000)
    matches = the_input.get_matched_outputs()
    assert change_in_matches == 1
    assert isinstance(matches, list)
    assert {'name': 'MyWriter'} in matches
    change_in_matches = the_output.wait_for_match(2000)
    matches = the_output.get_matched_inputs()
    assert change_in_matches == 1
    assert isinstance(matches, list)
    assert {'name': 'MyReader'} in matches

  def test_multiple_inputs(self, discovery_connector, discovery_reader_only_input):
    the_output = discovery_connector.get_output("MyPublisher::MyWriter")

    total_matches = 0
    # the_output should match two inputs, the one from discovery_reader_only_input
    # and the one defined within discovery_connector
    while total_matches < 2:
      total_matches += the_output.wait_for_match(3000)
    assert total_matches == 2

    # Calling again to wait_for_match should timeout
    with pytest.raises(rti.TimeoutError) as excinfo:
      the_output.wait_for_match(1000)

    matches = the_output.get_matched_inputs()
    assert {'name': 'MyReader'} in matches
    assert {'name': 'TestReader'} in matches

  def test_multiple_outputs(self, discovery_connector, discovery_writer_only_output):
    the_input = discovery_connector.get_input("MySubscriber::MyReader")

    total_matches = 0
    # the_input should match two outpouts, the one from discovery_writer_only_output
    # and the one defined within discovery_connector
    while total_matches < 2:
      total_matches += the_input.wait_for_match(3000)
    assert total_matches == 2

    # Calling again to wait_for_match should timeout
    with pytest.raises(rti.TimeoutError) as excinfo:
      the_input.wait_for_match(1000)

    matches = the_input.get_matched_outputs()
    assert {'name': 'MyWriter'} in matches
    assert {'name': 'TestWriter'} in matches

  # Even though we are going to use the discovery_reader_only_input, don't use the
  # pytest fixture as we want to control the deletion of it from within the
  # test function
  def test_unmatched_input(self, discovery_writer_only_output):
    # To begin with, no matching occurs
    assert None is discovery_writer_only_output.get_matched_inputs()

    # Create the Connector object containing the matching input
    reader_connector = rti.Connector(
        "MyParticipantLibrary::DiscoveryTestReaderOnly",
        os.path.join(os.path.dirname(os.path.realpath(__file__)),"../xml/TestConnector.xml"))
    the_input = reader_connector.get_input("TestSubscriber::TestReader")
    assert the_input is not None

    # Check that matching occurs
    change_in_matches = discovery_writer_only_output.wait_for_match()
    assert change_in_matches == 1
    matches = discovery_writer_only_output.get_matched_inputs()
    assert {'name': 'TestReader'} in matches
    change_in_matches = the_input.wait_for_match()
    assert change_in_matches == 1
    matches = the_input.get_matched_outputs()
    assert {'name': 'TestWriter'} in matches

    # If we now delete the reader_connector object which we created above, they
    # will unmatch
    reader_connector.close()
    change_in_matches = discovery_writer_only_output.wait_for_match()
    assert change_in_matches == -1
    matches = discovery_writer_only_output.get_matched_inputs()
    assert matches is None

  # Even though we are going to use the discovery_writer_only_output, don't use the
  # pytest fixture as we want to control the deletion of it from within the
  # test function
  def test_unmatched_output(self, discovery_reader_only_input):
    # To begin with, no matching occurs
    assert None is discovery_reader_only_input.get_matched_outputs()

    # Create the Connector object containing the matching input
    writer_connector = rti.Connector(
        "MyParticipantLibrary::DiscoveryTestWriterOnly",
        os.path.join(os.path.dirname(os.path.realpath(__file__)),"../xml/TestConnector.xml"))
    the_output = writer_connector.get_output("TestPublisher::TestWriter")
    assert the_output is not None

    # Check that matching occurs
    change_in_matches = discovery_reader_only_input.wait_for_match()
    assert change_in_matches == 1
    matches = discovery_reader_only_input.get_matched_outputs()
    assert {'name': 'TestWriter'} in matches
    change_in_matches = the_output.wait_for_match()
    assert change_in_matches == 1
    matches = the_output.get_matched_inputs()
    assert {'name': 'TestReader'} in matches

    # If we now delete the reader_connector object which we created above, they
    # will unmatch
    writer_connector.close()
    change_in_matches = discovery_reader_only_input.wait_for_match()
    assert change_in_matches == -1
    matches = discovery_reader_only_input.get_matched_outputs()
    assert matches is None
