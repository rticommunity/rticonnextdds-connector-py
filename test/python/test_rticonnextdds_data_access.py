###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

import pytest,time,sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
import rticonnextdds_connector as rti

class TestDataAccess:

  """
  This class tests the different ways to access data in Instance and SampleIterator,
  focusing on the filedName syntax
  """
  @pytest.fixture(scope="class")
  def populatedInput(self):
    """Class fixture that writes the test messages do they're available in the input
    """

    xml_path = os.path.join(
      os.path.dirname(os.path.realpath(__file__)),
      "../xml/TestConnector.xml")

    participant_profile="MyParticipantLibrary::DataAccessTest"
    with rti.open_connector(participant_profile, xml_path) as rti_connector:
      output = rti_connector.get_output("TestPublisher::TestWriter")

      output.instance.set_dictionary({
        'my_long': 10,
        'my_double': 3.3,
        'my_enum': 1,
        'my_string': 'hello',
        'my_point': {'x': 3, 'y': 4},
        'my_union': {'my_int_sequence': [10, 20, 30]},
        'my_int_union': {'my_long': 222},
        'my_point_sequence': [{'x': 10, 'y': 20}, {'x': 11, 'y': 21}],
        'my_int_sequence': [1, 2, 3],
        'my_array': [{'x': 0, 'y': 0}, {'x': 0, 'y': 0}, {'x': 0, 'y': 0}, {'x': 0, 'y': 0}, {'x': 5, 'y': 15}]})
      output.write()

      output.clear_members()
      output.instance.set_number("my_optional.x", 101)
      output.write()

      input = rti_connector.get_input("TestSubscriber::TestReader")

      for i in range(1, 20):
        input.read()
        if input.sample_count == 2:
          break
        time.sleep(.5)

      assert input.sample_count == 2
      assert input[0].valid_data
      assert input[1].valid_data

      yield input

  def test_numbers(self, populatedInput):
    sample = populatedInput[0]
    assert sample.get_number("my_long") == 10
    assert sample.get_number("my_double") == 3.3

  def test_get_enum(self, populatedInput):
    sample = populatedInput[0]
    assert sample.get_number("my_enum") == 1

  def test_nested_struct(self, populatedInput):
    sample = populatedInput[0]
    assert sample.get_number("my_point.x") == 3
    assert sample.get_number("my_point.y") == 4

  def test_sequences(self, populatedInput):
    sample = populatedInput[0]
    assert sample.get_number("my_point_sequence[1].y") == 20
    assert sample.get_number("my_int_sequence[2]") == 2
    assert sample.get_number("my_point_sequence#") == 2
    assert sample.get_number("my_int_sequence#") == 3
    assert sample.get_number("my_array[5].x") == 5

  @pytest.mark.xfail
  def test_bad_sequence_access(self, populatedInput):
    sample = populatedInput[0]
    with pytest.raises(AttributeError) as execinfo:
      sample.get_number("my_point_sequence[10].y")
    with pytest.raises(AttributeError) as execinfo:
      sample.get_number("my_int_sequence[10]")

  @pytest.mark.xfail
  def test_bad_member_access(self, populatedInput):
    sample = populatedInput[0]
    with pytest.raises(AttributeError) as execinfo:
      sample.get_number("my_nonexistent_member")

  def test_unions(self, populatedInput):
    sample = populatedInput[0]
    assert sample.get_number("my_union.my_int_sequence#") == 3
    assert sample.get_number("my_union.my_int_sequence[2]") == 20
    assert sample.get_number("my_int_union.my_long") == 222

  @pytest.mark.xfail
  def test_union_discriminator_value(self, populatedInput):
    sample = populatedInput[0]
    assert sample.get_number("my_int_union#") == 200
    assert sample.get_number("my_union#") == 2

  def test_union_selected_member(self, populatedInput):
    sample = populatedInput[0]
    assert sample.get_string("my_int_union#") == "my_long"
    assert sample.get_string("my_union#") == "my_int_sequence"

  def test_set_optional(self, populatedInput):
    sample = populatedInput[1]
    assert sample.get_number("my_optional.x") == 101

  @pytest.mark.xfail
  def test_unset_optional(self, populatedInput):
    sample = populatedInput[0]
    assert sample.get_number("my_optional_int") == None

  @pytest.mark.xfail
  def test_unset_complex_optional(self, populatedInput):
    sample = populatedInput[0]
    assert sample.get_number("my_optional.x") == None
