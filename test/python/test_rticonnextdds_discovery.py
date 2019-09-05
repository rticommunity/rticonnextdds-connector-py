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
  def discovery_connector_no_entity_names(self):
    xml_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "../xml/TestConnector.xml")
    participant_profile="MyParticipantLibrary::DiscoveryTestNoEntityName"

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
    matches = discovery_reader_only_input.get_matched_publications()
    assert len(matches) == 0

    # We should timeout if we attempt to wait for a match
    with pytest.raises(rti.TimeoutError) as excinfo:
      change_in_matches = discovery_reader_only_input.wait_for_publications(1)
      assert change_in_matches == 0

  def test_no_matches_output(self, discovery_writer_only_output):
    # We should not match with any outputs at this point
    matches = discovery_writer_only_output.get_matched_subscriptions()
    assert len(matches) == 0

    # We should timeout if we attempt to wait for a match
    with pytest.raises(rti.TimeoutError) as excinfo:
      change_in_matches = discovery_writer_only_output.wait_for_subscriptions(1)

  def test_simple_matching(self, discovery_connector):
    the_input = discovery_connector.get_input("MySubscriber::MyReader")
    the_output = discovery_connector.get_output("MyPublisher::MyWriter")

    # Both the input and output should match each other (and nothing else)
    change_in_matches = the_input.wait_for_publications(2000)
    matches = the_input.get_matched_publications()
    assert change_in_matches == 1
    assert isinstance(matches, list)
    assert {'name': 'MyWriter'} in matches
    change_in_matches = the_output.wait_for_subscriptions(2000)
    matches = the_output.get_matched_subscriptions()
    assert change_in_matches == 1
    assert isinstance(matches, list)
    assert {'name': 'MyReader'} in matches

  def test_multiple_inputs(self, discovery_connector, discovery_reader_only_input):
    the_output = discovery_connector.get_output("MyPublisher::MyWriter")

    total_matches = 0
    # the_output should match two inputs, the one from discovery_reader_only_input
    # and the one defined within discovery_connector
    while total_matches < 2:
      total_matches += the_output.wait_for_subscriptions(3000)
    assert total_matches == 2

    # Calling again to wait_for_subscriptions should timeout
    with pytest.raises(rti.TimeoutError) as excinfo:
      the_output.wait_for_subscriptions(1000)

    matches = the_output.get_matched_subscriptions()
    assert {'name': 'MyReader'} in matches
    assert {'name': 'TestReader'} in matches

  def test_multiple_outputs(self, discovery_connector, discovery_writer_only_output):
    the_input = discovery_connector.get_input("MySubscriber::MyReader")

    total_matches = 0
    # the_input should match two outpouts, the one from discovery_writer_only_output
    # and the one defined within discovery_connector
    while total_matches < 2:
      total_matches += the_input.wait_for_publications(3000)
    assert total_matches == 2

    # Calling again to wait_for_publications should timeout
    with pytest.raises(rti.TimeoutError) as excinfo:
      the_input.wait_for_publications(1000)

    matches = the_input.get_matched_publications()
    assert {'name': 'MyWriter'} in matches
    assert {'name': 'TestWriter'} in matches

  # Even though we are going to use the discovery_reader_only_input, don't use the
  # pytest fixture as we want to control the deletion of it from within the
  # test function
  def test_unmatched_input(self, discovery_writer_only_output):
    # To begin with, no matching occurs
    assert len(discovery_writer_only_output.get_matched_subscriptions()) == 0

    # Create the Connector object containing the matching input
    reader_connector = rti.Connector(
        "MyParticipantLibrary::DiscoveryTestReaderOnly",
        os.path.join(os.path.dirname(os.path.realpath(__file__)),"../xml/TestConnector.xml"))
    the_input = reader_connector.get_input("TestSubscriber::TestReader")
    assert the_input is not None

    # Check that matching occurs
    change_in_matches = discovery_writer_only_output.wait_for_subscriptions(5000)
    assert change_in_matches == 1
    matches = discovery_writer_only_output.get_matched_subscriptions()
    assert {'name': 'TestReader'} in matches
    change_in_matches = the_input.wait_for_publications(5000)
    assert change_in_matches == 1
    matches = the_input.get_matched_publications()
    assert {'name': 'TestWriter'} in matches

    # If we now delete the reader_connector object which we created above, they
    # will unmatch
    reader_connector.close()
    change_in_matches = discovery_writer_only_output.wait_for_subscriptions(5000)
    assert change_in_matches == -1
    matches = discovery_writer_only_output.get_matched_subscriptions()
    assert len(matches) == 0

  # Even though we are going to use the discovery_writer_only_output, don't use the
  # pytest fixture as we want to control the deletion of it from within the
  # test function
  def test_unmatched_output(self, discovery_reader_only_input):
    # To begin with, no matching occurs
    assert len(discovery_reader_only_input.get_matched_publications()) == 0

    # Create the Connector object containing the matching input
    writer_connector = rti.Connector(
        "MyParticipantLibrary::DiscoveryTestWriterOnly",
        os.path.join(os.path.dirname(os.path.realpath(__file__)),"../xml/TestConnector.xml"))
    the_output = writer_connector.get_output("TestPublisher::TestWriter")
    assert the_output is not None

    # Check that matching occurs
    change_in_matches = discovery_reader_only_input.wait_for_publications()
    assert change_in_matches == 1
    matches = discovery_reader_only_input.get_matched_publications()
    assert {'name': 'TestWriter'} in matches
    change_in_matches = the_output.wait_for_subscriptions(5000)
    assert change_in_matches == 1
    matches = the_output.get_matched_subscriptions()
    assert {'name': 'TestReader'} in matches

    # If we now delete the reader_connector object which we created above, they
    # will unmatch
    writer_connector.close()
    change_in_matches = discovery_reader_only_input.wait_for_publications(5000)
    assert change_in_matches == -1
    matches = discovery_reader_only_input.get_matched_publications()
    assert len(matches) == 0

  def test_empty_entity_names(self, discovery_connector_no_entity_names):
    the_output = discovery_connector_no_entity_names.get_output("MyPublisher::MyWriter")
    # Ensure that the entities match
    change_in_subs = the_output.wait_for_subscriptions(5000)
    assert change_in_subs == 1

    # Get the entity names from the matched subscriptions
    matched_subs = the_output.get_matched_subscriptions()
    # The entity names set in the input are empty
    assert matched_subs == [{'name': ''}]

  def test_no_entity_names(self, discovery_writer_only_output):
    # We call the _createTestScenario API to create a remote matching reader which
    # will not set any entity name.
    retcode = rti.connector_binding._createTestScenario(
      discovery_writer_only_output.connector.native,
      0, # RTI_Connector_testScenario_createReader
      discovery_writer_only_output.native)
    assert retcode == 0

    # Wait to match with the new reader
    discovery_writer_only_output.wait_for_subscriptions(5000)
    # Check that we can handle getting entity_name when it is NULL
    matches = discovery_writer_only_output.get_matched_subscriptions()
    assert isinstance(matches, list)
    assert len(matches) == 1
    assert isinstance(matches[0], dict)
    assert matches[0]['name'] is None

    # It is not necessary to delete the entites created by the call to createTestScenario
    # since they were all created from the same DomainParticipant as discovery_writer_only_output
    # which will have delete_contained_entities called on it.
