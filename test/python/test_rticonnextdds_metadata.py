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

  def test_sample_state(self, one_use_output, one_use_input):
    # Sample State can either be READ or NOT_READ
    one_use_output.write()
    one_use_input.wait(10000)
    one_use_input.read()
    # Since this is the first time we are calling read(), the state should be not read
    assert one_use_input.samples[0].info['sample_state'] == "NOT_READ"
    # Reading (or taking again) should change this state
    one_use_input.read()
    assert one_use_input.samples[0].info['sample_state'] == "READ"
    one_use_input.take()
    assert one_use_input.samples[0].info['sample_state'] == "READ"

  def test_instance_state(self, one_use_output, one_use_input):
    # Instance State can be ALIVE, NOT_ALIVE_DISPOSED or NOT_ALIVE_NO_WRITERS
    # A normal write() should result in an ALIVE instance state
    sample = send_data(one_use_output, one_use_input)
    assert sample.info['instance_state'] == "ALIVE"
    # Take the sample to remove it from the queue
    sample = send_data(one_use_output, one_use_input, action="dispose")
    assert sample.info['instance_state'] == "NOT_ALIVE_DISPOSED"
    one_use_input.take()
    sample = send_data(one_use_output, one_use_input, action="write")
    assert sample.info['instance_state'] == "ALIVE"
    one_use_input.take()
    sample = send_data(one_use_output, one_use_input, action="unregister")
    assert sample.info['instance_state'] == "NOT_ALIVE_NO_WRITERS"

  def test_view_state(self, one_use_output, one_use_input):
    # View State can be NEW or NOT NEW, and is per-instance
    one_use_output.instance["color"] = "Brown"
    one_use_output.write()
    one_use_input.wait(10000)
    one_use_input.take()
    # Since this is the first time we are calling read(), the state should be not read
    assert one_use_input.samples[0].info['view_state'] == "NEW"
    sample = send_data(one_use_output, one_use_input)
    assert sample.info['view_state'] == "NOT_NEW"
    one_use_output.instance["color"] = "Maroon"
    one_use_output.write()
    one_use_input.wait(10000)
    one_use_input.take()
    assert one_use_input.samples[0].info['view_state'] == "NEW"

  # Dispose an instance and check that we can obtain the key value
  def test_get_disposed_key_value(self, one_use_output, one_use_input):
    # Set the key field
    one_use_output.instance['color'] = "Yellow"
    # Also set some other non-key field
    one_use_output.instance['x'] = 1
    # Need to write() in order to register the instance
    sample = send_data(one_use_output, one_use_input)
    assert sample.info["valid_data"] == True
    assert sample.info['instance_state'] == "ALIVE"
    # Now we can dispose it
    sample = send_data(one_use_output, one_use_input, action="dispose")
    # Check invalid data + disposed
    assert sample.info['valid_data'] == False
    assert sample.info['instance_state'] == "NOT_ALIVE_DISPOSED"
    # Accessing the key field should provide us with the disposed instance
    assert sample.get_string("color") == "Yellow"
    # Also access it via __getitem__
    assert sample["color"] == "Yellow"
    # Any other fields should not be accessed
    # Accessing a nonexistent member should raise an error
    with pytest.raises(rti.Error, match=r".*Cannot find a member.*") as excinfo:
      nonExistentField = sample["IDontExist"]
    # It should be possible to obtain a dictionary of the sample. The only valid
    # field will be the key
    expected_dictionary = {
        "color": "Yellow",
        "x": 0,
        "y": 0,
        "shapesize": 0,
        "z": False
    }
    assert sample.get_dictionary() == expected_dictionary

  # Dispose a sample with multiple keys.
  # Uses this type:
  # struct MultipleKeyedShapeType {
  #     @key string<128> color;
  #     @key string<128> other_color;
  #     long x;
  #     @key long y;
  #     @key bool z;
  #     long shapesize;
  # };
  def test_get_disposed_key_values_multiple_keys(self, one_use_connector):
    the_output = one_use_connector.get_output("MyPublisher::MyMultipleKeyedSquareWriter")
    the_input = one_use_connector.get_input("MySubscriber::MyMultipleKeyedSquareReader")
    wait_for_discovery(the_output, the_input)

    # Set the sample
    the_output.instance['color'] = "Yellow" # key
    the_output.instance['other_color'] = "Green" # key
    the_output.instance['y'] = 9 # key
    the_output.instance['z'] = False # key
    the_output.instance['shapesize'] = 3 # not a key
    the_output.instance['x'] = 12 # not a key
    # Need to write() in order to register the instance
    sample = send_data(the_output, the_input)
    assert sample.info['valid_data'] == True
    assert sample.info['instance_state'] == "ALIVE"
    # Now we can dispose it
    sample = send_data(the_output, the_input, action="dispose")
    # Check invalid data + disposed
    assert sample.info['valid_data'] == False
    assert sample.info['instance_state'] == "NOT_ALIVE_DISPOSED"
    # Check that the key fields are correct
    assert sample.get_string("color") == "Yellow"
    assert sample["color"] == "Yellow"
    assert sample.get_string("other_color") == "Green"
    assert sample["other_color"] == "Green"
    assert sample.get_boolean("z") == False
    assert sample["z"] == False
    assert sample.get_number("y") == 9
    assert sample["y"] == 9
    # Also, can obtain the instance via dictionary
    expected_dictionary = {
        "color": "Yellow",
        "other_color": "Green",
        "y": 9,
        "x": 0,
        "shapesize": 0,
        "z": False
    }
    assert sample.get_dictionary() == expected_dictionary

  # Test getting the key values of a more complex disposed sample
  # Uses this type:
  # struct ShapeType {
  #     @key string<128> color;
  #     long x;
  #     long y;
  #     bool z;
  #     long shapesize;
  # };
  #
  # struct UnkeyedShapeType {
  #     string<128> color;
  #     long x;
  #     long y;
  #     bool z;
  #     long shapesize;
  # };
  #
  # struct NestedKeyedShapeType {
  #     @key UnkeyedShapeType keyed_shape;
  #     UnkeyedShapeType unkeyed_shape;
  #     @key ShapeType keyed_nested_member;
  #     @default(12) long unkeyed_toplevel_member;
  #     @default(4) @key long keyed_toplevel_member;
  # };
  def test_get_disposed_key_values_nested_keys(self, one_use_connector):
    the_input = one_use_connector.get_input("MySubscriber::MyNestedKeyedSquareReader")
    the_output = one_use_connector.get_output("MyPublisher::MyNestedKeyedSquareWriter")
    wait_for_discovery(the_output, the_input)
    # Set the sample
    the_output.instance["keyed_shape.color"] = "Black"
    the_output.instance["keyed_shape.x"] = 2
    the_output.instance["keyed_shape.y"] = 0
    the_output.instance["keyed_shape.shapesize"] = 100
    the_output.instance["keyed_shape.z"] = True
    the_output.instance["unkeyed_toplevel_member"] = 1
    # Do not set keyed_toplevel_member. Let the @default value be used
    the_output.instance["unkeyed_shape.shapesize"] = 100
    the_output.instance["keyed_nested_member.color"] = "White"
    the_output.instance["keyed_nested_member.x"] = 4
    # Write the sample and take it on the input
    sample = send_data(the_output, the_input)
    the_input.take()
    # Now we can dispose the instance
    sample = send_data(the_output, the_input, action="dispose")
    assert sample.info["valid_data"] == False
    assert sample.info["instance_state"] == "NOT_ALIVE_DISPOSED"
    assert sample["keyed_shape.x"] == 2
    assert sample["keyed_shape.y"] == 0
    assert sample["keyed_shape.shapesize"] == 100
    assert sample["keyed_shape.z"] == True
    assert sample["keyed_shape.color"] == "Black"
    assert sample["keyed_nested_member.color"] == "White"
    assert sample["keyed_toplevel_member"] == 4
    expected_dictionary = {
        "color": "",
        "z": False,
        "x": 0,
        "y": 0,
        "shapesize": 0
    }
    assert sample["unkeyed_shape"] == expected_dictionary
    assert sample.get_number("keyed_shape.x") == 2
    assert sample.get_number("keyed_shape.y") == 0
    assert sample.get_number("keyed_shape.shapesize") == 100
    assert sample.get_boolean("keyed_shape.z")== True
    assert sample.get_string("keyed_shape.color") == "Black"
    assert sample.get_string("keyed_nested_member.color") == "White"
    assert sample.get_number("keyed_toplevel_member") == 4
    assert sample["keyed_toplevel_member"] == 4
    # Obtain the entire sample as a dictionary
    expected_dictionary = {
        "keyed_shape": {
            "color": "Black",
            "x": 2,
            "y": 0,
            "shapesize": 100,
            "z": True
        },
        "unkeyed_shape": {
            "color": "",
            "x": 0,
            "y": 0,
            "shapesize": 0,
            "z": False
        },
        "keyed_nested_member": {
            "color": "White",
            "x": 0,
            "y": 0,
            "shapesize": 0,
            "z": False
        },
        "unkeyed_toplevel_member": 0,
        "keyed_toplevel_member": 4
    }
    assert sample.get_dictionary() == expected_dictionary
    # We can also obtain, as a dictionary, the complex keyed members
    expected_dictionary = {
        "color": "Black",
        "x": 2,
        "y": 0,
        "shapesize": 100,
        "z": True
    }
    assert sample.get_dictionary("keyed_shape") == expected_dictionary
    assert sample["keyed_shape"] == expected_dictionary
    expected_dictionary = {
        "color": "White",
        "x": 0,
        "y": 0,
        "shapesize": 0,
        "z": False
    }
    assert sample.get_dictionary("keyed_nested_member") == expected_dictionary
    assert sample["keyed_nested_member"] == expected_dictionary
    expected_dictionary = {
        "color": "",
        "x": 0,
        "y": 0,
        "shapesize": 0,
        "z": False
    }
    assert sample.get_dictionary("unkeyed_shape") == expected_dictionary
    assert sample["unkeyed_shape"] == expected_dictionary

  def test_accessing_keyed_values_using_iterators(self, one_use_output, one_use_input):
    one_use_output.instance["color"] = "Maroon"
    one_use_output.instance["x"] = 12
    # Send the sample
    send_data(one_use_output, one_use_input)
    one_use_input.take()
    # Now dispose the instance we just registered
    send_data(one_use_output, one_use_input, action="dispose")
    # There should be no data accessible using the valid_data_iter (dispose sample is invalid)
    had_data = False
    for sample in one_use_input.samples.valid_data_iter:
        had_data = True
    assert had_data == False
    # However, there should be one sample in data_iter
    for sample in one_use_input.samples:
        assert sample.info['instance_state'] == "NOT_ALIVE_DISPOSED"
        # We can still access the sample's fields, but only the key fields
        assert sample["color"] == "Maroon"

  # struct ShapeType {
  #     @key string<128> color;
  #     long x;
  #     long y;
  #     bool z;
  #     long shapesize;
  # };
  # struct ShapeTypeWithoutToplevelKeyType {
  #     @key ShapeType keyed_shape;
  #     ShapeType unkeyed_shape;
  # };
  def test_key_within_unkeyed_structure(self, one_use_connector):
    # Test the corner-case of unkeyed_shape.color. It is not a key (even though
    # it has the @key annotation)
    the_input = one_use_connector.get_input("MySubscriber::MySquareWithoutTopLevelKeyReader")
    the_output = one_use_connector.get_output("MyPublisher::MySquareWithoutTopLevelKeyWriter")
    # Wait for discovery
    wait_for_discovery(the_output, the_input)
    # Set some fields
    the_output.instance["keyed_shape.color"] = "Green"
    the_output.instance["unkeyed_shape.color"] = "Green"
    the_output.instance["keyed_shape.x"] = 12
    the_output.instance["unkeyed_shape.x"] = 12
    sample = send_data(the_output, the_input)
    the_input.take()
    # Dispose the instance
    sample = send_data(the_output, the_input, action="dispose")
    # Even though unkeyed_shape.color has the @key annotation, since the top level
    # structure is not keyed, that field is not either
    assert sample["unkeyed_shape.color"] == ""
    # The keyed_shape on the other hand does make up part of the key
    assert sample["keyed_shape.color"] == "Green"
