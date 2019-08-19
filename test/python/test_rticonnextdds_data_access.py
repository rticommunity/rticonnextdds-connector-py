###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

import pytest,time,sys,os,ctypes
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
import rticonnextdds_connector as rti


class TestDataAccess:
  """
  This class tests the different ways to access data in Instance and SampleIterator,
  focusing on the filedName syntax.

  Tests can use the following fixtures:
      - test_output: for a clean output
      - test_input: for a clean input
      - populated_input: for an input with some data (the first sample contains
        the values of test_dictionary)
      - test_dictionary: for the dictionary used to populated the input
      - test_connector: to access the connector (most tests only need the
        inputs or outputs)

  Tests can also use the following utility methods:
      - wait_for_data
  """

  @pytest.fixture(scope="class")
  def test_connector(self):
    """Creates the connector shared among all the tests in this class"""

    xml_path = os.path.join(
      os.path.dirname(os.path.realpath(__file__)),
      "../xml/TestConnector.xml")

    participant_profile="MyParticipantLibrary::DataAccessTest"
    with rti.open_connector(participant_profile, xml_path) as rti_connector:
      yield rti_connector

  @pytest.fixture(scope="class")
  def test_dictionary(self):
    return {
      'my_long': 10,
      'my_double': 3.3,
      'my_optional_bool':True,
      'my_enum': 1,
      'my_string': 'hello',
      'my_point': {'x': 3, 'y': 4},
      'my_point_alias': {'x': 30, 'y': 40},
      'my_union': {'my_int_sequence': [10, 20, 30]},
      'my_int_union': {'my_long': 222},
      'my_point_sequence': [{'x': 10, 'y': 20}, {'x': 11, 'y': 21}],
      'my_int_sequence': [1, 2, 3],
      'my_point_array': [{'x': 0, 'y': 0}, {'x': 0, 'y': 0}, {'x': 0, 'y': 0}, {'x': 0, 'y': 0}, {'x': 5, 'y': 15}]}

  @pytest.fixture
  def test_output(self, test_connector):
    output = test_connector.get_output("TestPublisher::TestWriter2")
    output.clear_members()
    return output

  @pytest.fixture(scope="class")
  def test_input(self, test_connector):
    return test_connector.get_input("TestSubscriber::TestReader2")

  def wait_for_data(self, input, count = 1, do_take = True):
    """Waits until input has count samples"""

    for i in range(1, 5):
      input.read()
      if input.sample_count == count:
        break
      input.wait(1000)

    assert input.sample_count == count
    if do_take:
      input.take()

  @pytest.fixture(scope="class")
  def populated_input(self, test_connector, test_dictionary):
    """Writes a default sample and receives it at the input.
    Some tests use this default sample. Others may write different data and
    won't use this fixture
    """
    output = test_connector.get_output("TestPublisher::TestWriter")
    output.instance.set_dictionary(test_dictionary)
    output.write()

    test_input = test_connector.get_input("TestSubscriber::TestReader")
    self.wait_for_data(input = test_input, count = 1, do_take = True)

    assert test_input.sample_count == 1
    assert test_input[0].valid_data

    return test_input

  def test_numbers(self, populated_input):
    sample = populated_input[0]
    assert sample.get_number("my_long") == 10
    assert sample.get_number("my_double") == 3.3

  def test_numbers_as_strings(self, populated_input):
    sample = populated_input[0]
    assert sample.get_string("my_long") == "10"
    assert sample.get_string("my_double") == "3.3"

  def test_get_boolean(self, populated_input):
    sample = populated_input[0]
    assert sample.get_boolean("my_optional_bool") == True
    assert sample["my_optional_bool"] == True

  @pytest.mark.xfail
  def test_get_boolean_as_number(self, populated_input):
    sample = populated_input[0]
    assert sample.get_number("my_optional_bool") == 1

  def test_get_enum(self, populated_input):
    sample = populated_input[0]
    assert sample.get_number("my_enum") == 1

  def test_nested_struct(self, populated_input):
    sample = populated_input[0]
    assert sample.get_number("my_point.x") == 3
    assert sample.get_number("my_point.y") == 4

  def test_sequences(self, populated_input):
    sample = populated_input[0]
    assert sample.get_number("my_point_sequence[0].y") == 20
    assert sample.get_number("my_int_sequence[1]") == 2
    assert sample.get_number("my_point_sequence#") == 2
    assert sample.get_number("my_int_sequence#") == 3
    assert sample.get_number("my_point_array[4].x") == 5
    assert sample["my_point_sequence[0].y"] == 20
    assert sample["my_int_sequence[1]"] == 2
    assert sample["my_point_sequence#"] == 2
    assert sample["my_int_sequence#"] == 3
    assert sample["my_point_array[4].x"] == 5

  def test_output_sequences(self, test_output, test_input):
    test_output.instance.set_number("my_point_sequence[0].y", 20)
    test_output.instance["my_int_sequence[1]"] = 2
    test_output.instance["my_point_array[4].x"] = 5
    test_output.write()
    self.wait_for_data(test_input)

    sample = test_input[0]
    assert sample["my_point_sequence[0].y"] == 20
    assert sample["my_int_sequence[1]"] == 2
    assert sample["my_point_sequence#"] == 1
    assert sample["my_int_sequence#"] == 2
    assert sample["my_point_array[4].x"] == 5

  @pytest.mark.xfail
  def test_bad_sequence_access(self, populated_input):
    sample = populated_input[0]
    with pytest.raises(AttributeError) as excinfo:
      sample.get_number("my_point_sequence[9].y")
    with pytest.raises(AttributeError) as excinfo:
      sample.get_number("my_int_sequence[9]")

  def test_bad_member_name(self, populated_input):
    sample = populated_input[0]
    with pytest.raises(rti.Error, match=r".*Cannot find.*my_nonexistent_member.*") as excinfo:
      sample.get_number("my_nonexistent_member")

  def test_bad_member_syntax(self, populated_input):
    sample = populated_input[0]
    with pytest.raises(rti.Error) as excinfo:
      sample.get_number("my_point_sequence[9[.y")

  def test_bad_sequence_index(self, populated_input):
    sample = populated_input[0]
    with pytest.raises(rti.Error) as excinfo:
      sample.get_number("my_point_sequence[-1].y")

  def test_unions(self, populated_input):
    sample = populated_input[0]
    assert sample.get_number("my_union.my_int_sequence#") == 3
    assert sample.get_number("my_union.my_int_sequence[1]") == 20
    assert sample.get_number("my_int_union.my_long") == 222

  @pytest.mark.xfail
  def test_union_discriminator_value(self, populated_input):
    sample = populated_input[0]
    assert sample.get_number("my_int_union#") == 200
    assert sample.get_number("my_union#") == 2

  def test_union_selected_member(self, populated_input):
    sample = populated_input[0]
    assert sample.get_string("my_int_union#") == "my_long"
    assert sample.get_string("my_union#") == "my_int_sequence"
    assert sample["my_union#"] == "my_int_sequence"

  def test_change_union_member(self, test_output, test_input):
    test_output.instance.set_number("my_union.my_int_sequence[1]", 3)
    test_output.write()
    self.wait_for_data(test_input)
    sample = test_input[0]
    assert sample.get_string("my_union#") == "my_int_sequence"

    test_output.instance.set_number("my_union.my_long", 3)
    test_output.write()
    self.wait_for_data(test_input)

    sample = test_input[0]
    assert sample.get_string("my_union#") == "my_long"
    assert sample.get_number("my_union.my_long") == 3

  def test_set_optional(self, test_output, test_input):
    test_output.instance.set_number("my_optional_point.x", 101)
    test_output.instance["my_point_alias.x"] = 202
    test_output.write()
    self.wait_for_data(test_input)

    sample = test_input[0]
    assert sample.get_number("my_optional_point.x") == 101
    assert sample.get_number("my_point_alias.x") == 202

  def test_unset_optional_number(self, populated_input):
    sample = populated_input[0]
    assert sample.get_number("my_optional_long") is None
    assert sample["my_optional_long"] is None
    with pytest.raises(KeyError) as excinfo:
      value = sample.get_dictionary()['my_optional_long']

  def test_unset_optional_string(self, populated_input):
    sample = populated_input[0]
    assert sample.get_string("my_optional_long") is None

  def test_unset_optional_boolean(self, test_output, test_input):
    test_output.write()
    self.wait_for_data(test_input)
    assert test_input[0].get_boolean("my_optional_bool") is None

  def test_unset_complex_optional(self, populated_input):
    sample = populated_input[0]
    assert sample.get_number("my_optional_point.x") is None

  @pytest.mark.xfail
  def test_unset_complex_optional_dict2(self, populated_input):
    sample = populated_input[0]
    assert sample.get_number("my_optional_point.x") is None
    dictionary = sample.get_dictionary()
    # Due to CORE-9685 the previous call to get_number "initializes"
    # my_optional_point, so get_dictionary now incorrectly returns it
    assert not "my_optional_point" in dictionary

  def test_reset_optional_number(self, test_output, test_input):
    test_output.instance.set_number("my_optional_long", 33)
    test_output.instance.set_number("my_optional_long", None)
    test_output.write()
    self.wait_for_data(test_input)
    assert test_input[0].get_number("my_optional_long") is None
    assert not "my_optional_long" in test_input[0].get_dictionary()

  def test_reset_optional_boolean(self, test_output, test_input):
    test_output.instance.set_boolean("my_optional_bool", True)
    test_output.instance.set_boolean("my_optional_bool", None)
    test_output.write()
    self.wait_for_data(test_input)
    sample = test_input[0]
    assert sample.get_boolean("my_optional_bool") is None
    assert sample["my_optional_bool"] is None
    assert not "my_optional_bool" in sample.get_dictionary()

  def test_reset_complex_optional(self, test_output, test_input):
    test_output.instance.set_number("my_optional_point.x", 44)
    test_output.instance.set_number("my_point_alias.x", 55)
    test_output.instance.clear_member("my_optional_point")
    test_output.instance.clear_member("my_point_alias")
    test_output.write()
    self.wait_for_data(test_input)
    assert test_input[0].get_number("my_optional_point.x") is None
    assert test_input[0].get_number("my_point_alias.x") is None
    assert test_input[0]["my_optional_point.x"] is None

  def test_clear_complex_member(self, test_output, test_input):
    test_output.instance.set_number("my_point.x", 44)
    test_output.instance.clear_member("my_point")
    test_output.write()
    self.wait_for_data(test_input)
    assert test_input[0].get_number("my_point.x") == 0

  def test_clear_sequence(self, test_output, test_input):
    test_output.instance.set_number("my_union.my_int_sequence[2]", 10)
    test_output.instance.set_number("my_point.x", 3)
    test_output.instance.clear_member("my_union.my_int_sequence")
    test_output.write()

    self.wait_for_data(test_input)
    assert test_input[0].get_number("my_union.my_int_sequence#") == 0
    assert test_input[0].get_number("my_point.x") == 3

  def test_clear_with_dictionary(self, test_dictionary, test_output, test_input):
    """Tests using None in a dictionary to clear a member"""

    # Set non-default values
    test_output.instance.set_dictionary(test_dictionary)
    test_output.instance.set_boolean("my_optional_bool", True)

    # Reset members using None in a dictionary--optional members are set to None,
    # other members are initialized to their default value
    test_output.instance.set_dictionary({
      'my_optional_point': None,
      'my_optional_long': None,
      'my_point': None,
      'my_point_alias': None,
      'my_long': None,
      'my_optional_bool': None,
      'my_point_sequence': None,
      'my_string': None,
      'my_union': None,
      'my_enum': None,
    })
    test_output.write()
    self.wait_for_data(test_input)

    sample = test_input[0]
    assert sample.get_number("my_optional_point.x") is None
    assert sample.get_number("my_optional_long") is None
    assert sample.get_number("my_point.x") == 0
    assert sample.get_number("my_point.y") == 0
    assert sample.get_number("my_point_alias.x") is None
    assert sample.get_number("my_long") == 0
    assert sample.get_boolean("my_optional_bool") is None
    assert sample.get_number("my_point_sequence#") == 0
    assert sample.get_string("my_string") == ""
    assert sample["my_string"] == ""
    assert sample.get_string("my_union#") == "point"
    assert sample.get_number("my_enum") == 2
    assert sample.get_number("my_double") == test_dictionary['my_double']
    dictionary = sample.get_dictionary()
    print(dictionary)
    assert not "my_optional_bool" in dictionary
    assert not "my_optional_long" in dictionary
    assert not "my_point_alias" in dictionary
    assert not "my_optional_point" in dictionary

  def test_bad_clear_member(self, test_output):
    with pytest.raises(rti.Error) as excinfo:
      test_output.instance.clear_member("my_nonexistent_member")

  @pytest.mark.xfail
  def test_reset_sequence(self, test_output, test_input):
    test_output.instance.set_number("my_union.my_int_sequence[2]", 10)
    test_output.instance.set_number("my_point.x", 3)
    test_output.write()
    self.wait_for_data(test_input)

    assert test_input[0].get_number("my_point.x") == 3
    assert test_input[0].get_number("my_union.my_int_sequence#") == 3

    test_output.instance.set_dictionary({'my_int_sequence':[]})
    test_output.write()
    self.wait_for_data(test_input)

    sample = test_input[0]
    assert sample.get_number("my_int_sequence#") == 0

    # The other fields are unchanged:
    assert sample.get_number("my_point.x") == 3
    assert sample.get_number("my_point_sequence#") == 2

  def test_get_dictionary(self, populated_input):
    # populated_input[0] contains test_dictionary
    sample = populated_input[0]

    # Attempt to get_dictionary for non existent member
    with pytest.raises(rti.Error, match=r".*Cannot find.*IDoNotExist.*") as excinfo:
      sample.get_dictionary("IDoNotExist")

    # Attempt to get_dictionary for non-complex members
    with pytest.raises(rti.Error, match=r".*invalid TypeCode kind DDS_TK_LONG.*") as excinfo:
      sample.get_dictionary("my_long")
    with pytest.raises(rti.Error, match=r".*invalid TypeCode kind DDS_TK_DOUBLE.*") as excinfo:
      sample.get_dictionary("my_double")
    with pytest.raises(rti.Error, match=r".*invalid TypeCode kind DDS_TK_BOOLEAN.*") as excinfo:
      sample.get_dictionary("my_optional_bool")
    with pytest.raises(rti.Error, match=r".*invalid TypeCode kind DDS_TK_LONG.*") as excinfo:
      sample.get_dictionary("my_optional_long")
    with pytest.raises(rti.Error, match=r".*invalid TypeCode kind DDS_TK_STRING.*") as excinfo:
      sample.get_dictionary("my_string")
    with pytest.raises(rti.Error, match=r".*invalid TypeCode kind DDS_TK_ENUM.*") as excinfo:
      sample.get_dictionary("my_enum")
    # It is possible to use get_dictionary to access nested members, but the nested
    # member must be a complex type
    with pytest.raises(rti.Error, match=r".*invalid TypeCode kind DDS_TK_LONG.*") as excinfo:
      sample.get_dictionary("my_point.x")

    # Valid values for member_name
    the_point = sample.get_dictionary("my_point")
    assert the_point['x'] == 3 and the_point['y'] == 4
    the_point_alias = sample.get_dictionary("my_point_alias")
    assert the_point_alias['x'] == 30 and the_point_alias['y'] == 40
    the_union = sample.get_dictionary("my_union")
    assert the_union['my_int_sequence'] == [10, 20, 30]
    the_point_sequence = sample.get_dictionary("my_point_sequence")
    assert the_point_sequence == [{'x': 10, 'y': 20}, {'x': 11, 'y': 21}]
    the_point_sequence_1 = sample.get_dictionary("my_point_sequence[1]")
    assert the_point_sequence_1 == {'x': 10, 'y': 20}
    the_array = sample.get_dictionary("my_point_array")
    the_array_1 = sample.get_dictionary("my_point_array[1]")
    assert the_array_1 == {'x': 0, 'y': 0}

  def test_shrink_sequence(self, test_output, test_input, test_dictionary):
    """Tests that set_dictionary shrinks sequences when it receives a smaller one"""

    test_output.instance.set_number("my_int_sequence[2]", 10) # set length to 3
    test_output.instance.set_number("my_point_sequence[0].x", 11)
    test_output.instance.set_number("my_point_sequence[0].y", 12)
    test_output.instance.set_number("my_point_sequence[2].x", 10)
    test_output.instance.set_dictionary(
      {"my_point_array":[{'x': 10, 'y': 20}, {'x': 11, 'y': 21}, {'x': 12, 'y': 22}, {'x': 13, 'y': 23}, {'x': 14, 'y': 24}]})

    # Reduce sequences to 1, while arrays retain exiting values
    test_output.instance.set_dictionary({
      "my_int_sequence":[40],
      "my_point_sequence":[{"y":2}],
      "my_point_array":[{"x":100}, {"y":200}]})
    test_output.write()
    self.wait_for_data(test_input)

    sample = test_input[0]
    assert sample["my_int_sequence#"] == 1 # Length reduced
    assert sample["my_point_sequence#"] == 1 # Length reduced
    assert sample["my_int_sequence[0]"] == 40 # New value
    assert sample["my_point_sequence[0].y"] == 2 # New value
    assert sample["my_point_sequence[0].x"] == 0 # Doesn't retain previous value
    assert sample["my_point_array[0].x"] == 100 # New value
    assert sample["my_point_array[0].y"] == 20 # Retains value
    assert sample["my_point_array[4].x"] == 14 # Retains value


  def test_access_native_dynamic_data(self, populated_input):
    get_member_count = rti.connector_binding.library.DDS_DynamicData_get_member_count
    get_member_count.restype = ctypes.c_uint
    get_member_count.argtypes = [ctypes.c_void_p]
    count = get_member_count(populated_input[0].native)
    assert count > 0

  def test_input_performance(self, populated_input):
    num_iter = 1000
    sample = populated_input[0]

    start = time.time()
    for i in range (1, num_iter):
      v = sample.get_number("my_long")
    end = time.time()
    get_number_duration = end - start

    start = time.time()
    for i in range (1, num_iter):
      v = sample["my_long"]
    end = time.time()
    get_item_duration = end - start

    print("__getitem__ is {:2.2%} slower than get_number".format(
      (get_item_duration - get_number_duration) / get_number_duration))

  def test_output_performance(self, test_output):
    num_iter = 1000
    sample = test_output.instance

    start = time.time()
    for i in range (1, num_iter):
      sample.set_number("my_long", 10)
    end = time.time()
    get_number_duration = end - start

    start = time.time()
    for i in range (1, num_iter):
      sample["my_long"] = 10
    end = time.time()
    get_item_duration = end - start

    print("__setitem__ is {:2.2%} slower than set_number".format(
      (get_item_duration - get_number_duration) / get_number_duration))

