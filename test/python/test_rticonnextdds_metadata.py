###############################################################################
# (c) 2019 Copyright, Real-Time Innovations.  All rights reserved.            #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

import pytest,time,sys,os,ctypes
from collections import namedtuple
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
import rticonnextdds_connector as rti
from test_utils import *

Requester = namedtuple('Requester', 'writer reader')
Replier = namedtuple('Replier', 'writer reader')

class TestMetadata:
  """
  This class tests write with options and sample info
  """

  @pytest.fixture(scope="class")
  def requestreply_connector(self):
    xml_path = os.path.join(
      os.path.dirname(os.path.realpath(__file__)),
      "../xml/TestConnector.xml")

    participant_profile="MyParticipantLibrary::TestRequestReply"
    with rti.open_connector(participant_profile, xml_path) as rti_connector:
      yield rti_connector

  @pytest.fixture(scope="class")
  def requester(self, requestreply_connector):
    return Requester(
      writer=requestreply_connector.get_output("TestPublisher::RequestWriter"),
      reader=requestreply_connector.get_input("TestSubscriber::ReplyReader"))

  @pytest.fixture(scope="class")
  def replier(self, requestreply_connector):
    return Replier(
      writer=requestreply_connector.get_output("TestPublisher::ReplyWriter"),
      reader=requestreply_connector.get_input("TestSubscriber::RequestReader"))

  def test_bad_info_field(self, one_use_output, one_use_input):
    sample = send_data(one_use_output, one_use_input)
    with pytest.raises(rti.Error, match=r".*Unknown.*nonexistent.*") as excinfo:
      sample.info["nonexistent"]

  def test_timestamp(self, one_use_output, one_use_input):
    sample = send_data(one_use_output, one_use_input, source_timestamp=2)
    assert sample.info["valid_data"] == True
    assert sample.info["source_timestamp"] == 2
    assert sample.info["reception_timestamp"] > 2

  def test_large_timestamp(self, one_use_output, one_use_input):
    n = 9007199254740999 # Loses precission as a double
    sample = send_data(one_use_output, one_use_input, source_timestamp=n)
    assert sample.info["source_timestamp"] == n

    n = 2147483647999999999 # DDS_TIME_MAX (0x7fffffff seconds + 999999999 ns)
    sample = send_data(one_use_output, one_use_input, source_timestamp=n)
    assert sample.info["source_timestamp"] == n

    n = n + 1
    with pytest.raises(rti.Error, match=r".*timestamp is larger than DDS_TIME_MAX.*") as excinfo:
      send_data(one_use_output, one_use_input, source_timestamp=n)

  def test_sample_identity(self, one_use_output, one_use_input):
    sample_id = {
      "writer_guid": [10,30,1,66,0,0,29,180,0,0,0,1,128,0,0,3],
      "sequence_number": 10
    }
    related_sample_id = {
      "writer_guid": [11,30,1,66,0,0,29,180,0,0,0,1,128,0,0,34],
      "sequence_number": 2**63-1 # LLONG_MAX
    }

    sample = send_data(
      one_use_output,
      one_use_input,
      identity=sample_id,
      related_sample_identity=related_sample_id)

    assert sample.info["sample_identity"] == sample_id
    assert sample.info["related_sample_identity"] == related_sample_id

    short_guid = {"writer_guid": [111], "sequence_number": 212}
    expected_id = {"writer_guid": [111] + [0] * 15, "sequence_number": 212}
    sample = send_data(one_use_output, one_use_input, identity=short_guid)
    assert sample.info["sample_identity"] == expected_id

  def test_bad_guid(self, one_use_output):

    not_an_array = {"writer_guid": 3, "sequence_number": 10}
    with pytest.raises(rti.Error, match=r".*error parsing GUID.*") as excinfo:
      one_use_output.write(identity=not_an_array)

    too_long = {"writer_guid": [1] * 17, "sequence_number": 10}
    with pytest.raises(rti.Error, match=r".*octet array exceeds maximum length of 16.*") as excinfo:
      one_use_output.write(identity=too_long)

    bad_octet = {"writer_guid": [1] * 15 + [256], "sequence_number": 10}
    with pytest.raises(rti.Error, match=r".*invalid octet value; expected 0-255, got: 256.*") as excinfo:
      one_use_output.write(identity=bad_octet)

    bad_octet_type = {"writer_guid": [1] * 15 + ["Hi"], "sequence_number": 10}
    with pytest.raises(rti.Error, match=r".*invalid type in octet array, index: 15.*") as excinfo:
      one_use_output.write(identity=bad_octet_type)

  def test_dispose(self, one_use_output, one_use_input):
    one_use_output.instance["color"] = "RED"
    sample = send_data(one_use_output, one_use_input, action="write")
    assert sample.info["valid_data"] == True
    sample = send_data(one_use_output, one_use_input, action="dispose")
    assert sample.info["valid_data"] == False

  def test_unregister(self, one_use_output, one_use_input):
    one_use_output.instance["color"] = "RED"
    sample = send_data(one_use_output, one_use_input)
    assert sample.info["valid_data"] == True
    sample = send_data(one_use_output, one_use_input, action="unregister")
    assert sample.info["valid_data"] == False

  def test_bad_write_action(self, one_use_output):
    with pytest.raises(rti.Error, match=r".*error parsing action field.*") as excinfo:
      one_use_output.write(action="bad")

  def test_request_reply(self, requester, replier):

    request_id = {"writer_guid": [3]*16, "sequence_number": 10}
    requester.writer.instance['x'] = 10
    requester.writer.instance['y'] = 20
    request = send_data(
      requester.writer,
      replier.reader,
      identity=request_id)

    assert request.info['identity'] == request_id
    replier.writer.instance['x'] = request['y']
    replier.writer.instance['y'] = request['x']
    reply = send_data(
      replier.writer,
      requester.reader,
      related_sample_identity=request.info['identity'])

    assert reply.info['related_sample_identity'] == request_id

#   def test_sample_state(self, one_use_output, one_use_input):
#     # Sample State can either be DDS_READ_SAMPLE_STATE or DDS_NOT_READ_SAMPLE_STATE
#     sample = send_data(one_use_output, one_use_input)
#     # Since this is the first time we are calling read(), the state should be not read
#     assert sample.info['sample_state'] == "DDS_NOT_READ_SAMPLE_STATE"
#     # Reading (or taking again) should change this state
#     one_use_input.read()
#     assert input.samples[0].info['sample_state'] == "DDS_READ_SAMPLE_STATE"
#     one_use_input.take()
#     assert input.samples[0].info['sample_state'] == "DDS_READ_SAMPLE_STATE"

  def test_instance_state(self, one_use_output, one_use_input):
    # Instance State can be ALIVE, DISPOSED or NO WRITERS
    # A normal write() should result in an ALIVE instance state
    sample = send_data(one_use_output, one_use_input)
    print(sample.info['instance_state'])
    assert sample.info['instance_state'] == "DDS_ALIVE_INSTANCE_STATE"
    # Take the sample to remove it from the queue
    one_use_input.take()
    sample = send_data(one_use_output, one_use_input, action="dispose")
    assert sample.info['instane_state'] == "DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE"
    one_use_input.take()
    sample = send_data(one_use_output, one_use_input, action="unregister")
    assert sample.info['instane_state'] == "DDS_NOT_ALIVE_NO_WRITERS_INSTANCE_STATE"
    one_use_input.take()

#   def test_view_state(Self, one_use_output, one_use_input):
    # View State can be NEW or NOT NEW

    # switch(state) {
    # case DDS_NEW_VIEW_STATE:
    #     str = "DDS_NEW_VIEW_STATE";
    #     break;
    # case DDS_NOT_NEW_VIEW_STATE:
    #     str = "DDS_NOT_NEW_VIEW_STATE";
