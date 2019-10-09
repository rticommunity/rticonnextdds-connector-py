###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

import pytest,time,sys,os,ctypes,json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
import rticonnextdds_connector as rti
from test_utils import send_data, wait_for_data, open_test_connector


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

    participant_profile="MyParticipantLibrary::DataAccessTest"
    with open_test_connector(participant_profile) as rti_connector:
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
      'my_point_array': [{'x': 0, 'y': 0}, {'x': 0, 'y': 0}, {'x': 0, 'y': 0}, {'x': 0, 'y': 0}, {'x': 5, 'y': 15}],
      'my_boolean': False,
      'my_int64': -18014398509481984,
      'my_uint64': 18014398509481984}

  @pytest.fixture
  def test_output(self, test_connector):
    output = test_connector.get_output("TestPublisher::TestWriter2")
    output.clear_members()
    return output

  @pytest.fixture(scope="class")
  def test_input(self, test_connector):
    return test_connector.get_input("TestSubscriber::TestReader2")

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
    wait_for_data(input = test_input, count = 1, do_take = True)

    assert test_input.samples.length == 1
    assert test_input.samples[0].valid_data

    return test_input

  def test_numbers(self, populated_input):
    sample = populated_input.samples[0]
    assert sample.get_number("my_long") == 10
    assert sample.get_number("my_double") == 3.3

  def test_numbers_as_strings(self, populated_input):
    sample = populated_input.samples[0]
    assert sample.get_string("my_long") == "10"
    assert sample.get_string("my_double") == "3.3"

  def test_get_boolean(self, populated_input):
    sample = populated_input.samples[0]
    assert sample.get_boolean("my_optional_bool") == True
    assert sample["my_optional_bool"] == True

  def test_get_boolean_as_number(self, populated_input):
    sample = populated_input.samples[0]
    assert sample.get_number("my_optional_bool") == 1

  def test_set_boolean_as_number(self, test_output, test_input):
    test_output.instance.set_number("my_optional_bool", 1)
    sample = send_data(test_output, test_input)
    assert sample["my_optional_bool"] == True

  def test_numeric_string(self, test_output, test_input):
    test_output.instance["my_string"] = "1234"
    sample = send_data(test_output, test_input)
    # A side effect of CON-139: __getitem__ automatically parses strings and
    # returns them as numbers if they represent a number
    assert sample["my_string"] == 1234

  def test_get_enum(self, populated_input):
    sample = populated_input.samples[0]
    assert sample.get_number("my_enum") == 1

  def test_nested_struct(self, populated_input):
    sample = populated_input.samples[0]
    assert sample.get_number("my_point.x") == 3
    assert sample.get_number("my_point.y") == 4

  def test_sequences(self, populated_input):
    sample = populated_input.samples[0]
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
    wait_for_data(test_input)

    sample = test_input.samples[0]
    assert sample["my_point_sequence[0].y"] == 20
    assert sample["my_int_sequence[1]"] == 2
    assert sample["my_point_sequence#"] == 1
    assert sample["my_int_sequence#"] == 2
    assert sample["my_point_array[4].x"] == 5

  def test_bad_sequence_access(self, populated_input):
    sample = populated_input.samples[0]
    assert sample.get_number("my_point_sequence[9].y") is None
    assert sample.get_number("my_int_sequence[9]") is None

  def test_bad_member_name(self, populated_input):
    sample = populated_input.samples[0]
    with pytest.raises(rti.Error, match=r".*Cannot find.*my_nonexistent_member.*") as excinfo:
      sample.get_number("my_nonexistent_member")

  def test_bad_member_syntax(self, populated_input):
    sample = populated_input.samples[0]
    with pytest.raises(rti.Error) as excinfo:
      sample.get_number("my_point_sequence[9[.y")

  def test_bad_sequence_index(self, populated_input):
    sample = populated_input.samples[0]
    with pytest.raises(rti.Error) as excinfo:
      sample.get_number("my_point_sequence[-1].y")

  def test_unions(self, populated_input):
    sample = populated_input.samples[0]
    assert sample.get_number("my_union.my_int_sequence#") == 3
    assert sample.get_number("my_union.my_int_sequence[1]") == 20
    assert sample.get_number("my_int_union.my_long") == 222

  def test_union_selected_member(self, populated_input):
    sample = populated_input.samples[0]
    assert sample.get_string("my_int_union#") == "my_long"
    assert sample.get_string("my_union#") == "my_int_sequence"
    assert sample["my_union#"] == "my_int_sequence"

  def test_change_union_member(self, test_output, test_input):
    test_output.instance.set_number("my_union.my_int_sequence[1]", 3)
    test_output.write()
    wait_for_data(test_input)
    sample = test_input.samples[0]
    assert sample.get_string("my_union#") == "my_int_sequence"

    test_output.instance.set_number("my_union.my_long", 3)
    test_output.write()
    wait_for_data(test_input)

    sample = test_input.samples[0]
    assert sample.get_string("my_union#") == "my_long"
    assert sample.get_number("my_union.my_long") == 3

  def test_set_optional(self, test_output, test_input):
    test_output.instance.set_number("my_optional_point.x", 101)
    test_output.instance["my_point_alias.x"] = 202
    test_output.write()
    wait_for_data(test_input)

    sample = test_input.samples[0]
    assert sample.get_number("my_optional_point.x") == 101
    assert sample.get_number("my_point_alias.x") == 202

  def test_unset_optional_number(self, populated_input):
    sample = populated_input.samples[0]
    assert sample.get_number("my_optional_long") is None
    assert sample["my_optional_long"] is None
    with pytest.raises(KeyError) as excinfo:
      value = sample.get_dictionary()['my_optional_long']

  def test_unset_optional_string(self, populated_input):
    sample = populated_input.samples[0]
    assert sample.get_string("my_optional_long") is None

  def test_unset_optional_boolean(self, test_output, test_input):
    test_output.write()
    wait_for_data(test_input)
    assert test_input.samples[0].get_boolean("my_optional_bool") is None

  def test_unset_complex_optional(self, populated_input):
    sample = populated_input.samples[0]
    assert sample.get_number("my_optional_point.x") is None

  def test_unset_complex_optional_dict2(self, populated_input):
    sample = populated_input.samples[0]
    assert sample.get_number("my_optional_point.x") is None
    dictionary = sample.get_dictionary()
    assert not "my_optional_point" in dictionary

  def test_reset_optional_number(self, test_output, test_input):
    test_output.instance.set_number("my_optional_long", 33)
    test_output.instance.set_number("my_optional_long", None)
    test_output.write()
    wait_for_data(test_input)
    assert test_input.samples[0].get_number("my_optional_long") is None
    assert not "my_optional_long" in test_input.samples[0].get_dictionary()

  def test_reset_optional_boolean(self, test_output, test_input):
    test_output.instance.set_boolean("my_optional_bool", True)
    test_output.instance.set_boolean("my_optional_bool", None)
    test_output.write()
    wait_for_data(test_input)
    sample = test_input.samples[0]
    assert sample.get_boolean("my_optional_bool") is None
    assert sample["my_optional_bool"] is None
    assert not "my_optional_bool" in sample.get_dictionary()

  def test_reset_complex_optional(self, test_output, test_input):
    test_output.instance.set_number("my_optional_point.x", 44)
    test_output.instance.set_number("my_point_alias.x", 55)
    test_output.instance.clear_member("my_optional_point")
    test_output.instance.clear_member("my_point_alias")
    test_output.write()
    wait_for_data(test_input)
    assert test_input.samples[0].get_number("my_optional_point.x") is None
    assert test_input.samples[0].get_number("my_point_alias.x") is None
    assert test_input.samples[0]["my_optional_point.x"] is None

  def test_clear_complex_member(self, test_output, test_input):
    test_output.instance.set_number("my_point.x", 44)
    test_output.instance.clear_member("my_point")
    test_output.write()
    wait_for_data(test_input)
    assert test_input.samples[0].get_number("my_point.x") == 0

  def test_clear_sequence(self, test_output, test_input):
    test_output.instance.set_number("my_union.my_int_sequence[2]", 10)
    test_output.instance.set_number("my_point.x", 3)
    test_output.instance.clear_member("my_union.my_int_sequence")
    test_output.write()

    wait_for_data(test_input)
    assert test_input.samples[0].get_number("my_union.my_int_sequence#") == 0
    assert test_input.samples[0].get_number("my_point.x") == 3

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
    wait_for_data(test_input)

    sample = test_input.samples[0]
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

    assert not "my_optional_bool" in dictionary
    assert not "my_optional_long" in dictionary
    assert not "my_point_alias" in dictionary
    assert not "my_optional_point" in dictionary

  def test_bad_clear_member(self, test_output):
    with pytest.raises(rti.Error) as excinfo:
      test_output.instance.clear_member("my_nonexistent_member")

  def test_reset_sequence(self, test_output, test_input):
    test_output.instance.set_number("my_union.my_int_sequence[2]", 10)
    test_output.instance.set_number("my_point.x", 3)
    test_output.instance["my_point_sequence[1].x"] = 44

    sample = send_data(test_output, test_input)
    assert sample.get_number("my_point.x") == 3
    assert sample.get_number("my_union.my_int_sequence#") == 3
    assert sample.get_number("my_point_sequence#") == 2

    test_output.instance.set_dictionary({'my_int_sequence':[]})

    sample = send_data(test_output, test_input)
    assert sample.get_number("my_int_sequence#") == 0
    # The other fields are unchanged:
    assert sample.get_number("my_point.x") == 3
    assert sample.get_number("my_point_sequence#") == 2

  def test_get_dictionary(self, populated_input):
    # populated_input.samples[0] contains test_dictionary
    sample = populated_input.samples[0]

    # Attempt to get_dictionary for non existent member
    with pytest.raises(rti.Error, match=r".*Cannot find.*IDoNotExist.*") as excinfo:
      sample.get_dictionary("IDoNotExist")

    # Attempt to get_dictionary for non-complex members
    with pytest.raises(rti.Error, match=r".*TypeCodeKind must be one of the following.*") as excinfo:
      sample.get_dictionary("my_long")
    with pytest.raises(rti.Error, match=r".*TypeCodeKind must be one of the following.*") as excinfo:
      sample.get_dictionary("my_double")
    with pytest.raises(rti.Error, match=r".*TypeCodeKind must be one of the following.*") as excinfo:
      sample.get_dictionary("my_optional_bool")
    with pytest.raises(rti.Error, match=r".*TypeCodeKind must be one of the following.*") as excinfo:
      sample.get_dictionary("my_optional_long")
    with pytest.raises(rti.Error, match=r".*TypeCodeKind must be one of the following.*") as excinfo:
      sample.get_dictionary("my_string")
    with pytest.raises(rti.Error, match=r".*TypeCodeKind must be one of the following.*") as excinfo:
      sample.get_dictionary("my_enum")
    # It is possible to use get_dictionary to access nested members, but the nested
    # member must be a complex type
    with pytest.raises(rti.Error, match=r".*TypeCodeKind must be one of the following.*") as excinfo:
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
    the_point_sequence_0 = sample.get_dictionary("my_point_sequence[0]")
    assert the_point_sequence_0 == {'x': 10, 'y': 20}
    the_array = sample.get_dictionary("my_point_array")
    the_array_0 = sample.get_dictionary("my_point_array[0]")
    assert the_array_0 == {'x': 0, 'y': 0}

    # Test get_dictionary with an unset optional
    unset_optional = sample.get_dictionary("my_optional_point")
    assert unset_optional is None

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
    wait_for_data(test_input)

    sample = test_input.samples[0]
    assert sample["my_int_sequence#"] == 1 # Length reduced
    assert sample["my_point_sequence#"] == 1 # Length reduced
    assert sample["my_int_sequence[0]"] == 40 # New value
    assert sample["my_point_sequence[0].y"] == 2 # New value
    assert sample["my_point_sequence[0].x"] == 0 # Doesn't retain previous value
    assert sample["my_point_array[0].x"] == 100 # New value
    assert sample["my_point_array[0].y"] == 20 # Retains value
    assert sample["my_point_array[4].x"] == 14 # Retains value

  def test_too_large_uint64_output(self, test_output):
    with pytest.raises(rti.Error, match=r".*value of my_uint64 is too large.*") as execinfo:
      test_output.instance.set_number("my_uint64", 9007199254740992)
    with pytest.raises(rti.Error, match=r".*value of my_int64 is too large.*") as execinfo:
      test_output.instance.set_number("my_int64", -9007199254740992)

  def verify_large_integer(self, output, input, number):
    with pytest.raises(rti.Error, match=r".*value of my_uint64 is too large.*") as execinfo:
      output.instance.set_number("my_uint64", number)
    with pytest.raises(rti.Error, match=r".*value of my_int64 is too large.*") as execinfo:
      output.instance.set_number("my_int64", -number)

    output.instance.set_dictionary({"my_uint64": number, "my_int64":-number})
    sample = send_data(output, input)
    dictionary = sample.get_dictionary()
    assert dictionary["my_uint64"] == number
    assert dictionary["my_int64"] == -number
    with pytest.raises(rti.Error, match=r".*value of my_uint64 is too large.*") as execinfo:
      sample.get_number("my_uint64")
    with pytest.raises(rti.Error, match=r".*value of my_int64 is too large.*") as execinfo:
      sample.get_number("my_int64")

  def test_large_uint64(self, test_output, test_input):
    max_int_get = 2**53 # 9007199254740992
    max_int_set = 2**53 - 1

    # largest integer allowed in set_number
    test_output.instance.set_number("my_uint64", max_int_set)
    test_output.instance.set_number("my_int64", -max_int_set)
    sample = send_data(test_output, test_input)
    assert sample.get_number("my_uint64") == max_int_set
    assert sample.get_number("my_int64") == -max_int_set

    # largest integer allowed in get_number; ok in set_dictionary, which
    # __setitem__ will also use
    test_output.instance["my_uint64"] = max_int_get
    test_output.instance.set_dictionary({"my_int64":-max_int_get})
    sample = send_data(test_output, test_input)
    assert sample.get_number("my_uint64") == max_int_get
    assert sample.get_number("my_int64") == -max_int_get

    # too large for get_number, but ok in get_dictionary
    self.verify_large_integer(test_output, test_input, max_int_get + 1)

    # 9007199254740999 -> 9007199254741000.0
    self.verify_large_integer(test_output, test_input, 9007199254740999)

    # largest long long
    self.verify_large_integer(test_output, test_input, 2**63 - 1)

  @pytest.mark.xfail(sys.platform.startswith("win"), reason="symbols not exported")
  def test_access_input_native_dynamic_data(self, populated_input):
    get_member_count = rti.connector_binding.library.DDS_DynamicData_get_member_count
    get_member_count.restype = ctypes.c_uint
    get_member_count.argtypes = [ctypes.c_void_p]
    count = get_member_count(populated_input.samples[0].native)
    assert count > 0

  @pytest.mark.xfail(sys.platform.startswith("win"), reason="symbols not exported")
  def test_access_output_native_dynamic_data(self, test_output, test_dictionary):
    test_output.instance.set_dictionary(test_dictionary)
    get_member_count = rti.connector_binding.library.DDS_DynamicData_get_member_count
    get_member_count.restype = ctypes.c_uint
    get_member_count.argtypes = [ctypes.c_void_p]
    count = get_member_count(test_output.instance.native)
    assert count > 0

  def test_input_performance(self, populated_input):
    num_iter = 1000
    sample = populated_input.samples[0]

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

    if get_number_duration:
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

    if get_number_duration > 0:
      print("__setitem__ is {:2.2%} slower than set_number".format(
        (get_item_duration - get_number_duration) / get_number_duration))

  def test_set_into_samples(self, test_output):
    """
    Test that the APIs to set data into samples behave as expected and raise the
    appropriate exceptions.
    """
    # Pass None as the field_name
    with pytest.raises(AttributeError) as excinfo:
      test_output.instance[None] = 5
    with pytest.raises(AttributeError) as excinfo:
      test_output.instance.set_boolean(None, True)
    with pytest.raises(AttributeError) as excinfo:
      test_output.instance.set_number(None, 42)
    with pytest.raises(AttributeError) as excinfo:
      test_output.instance.set_string(None, "Hello")

    # Try to set a number with a string
    with pytest.raises(TypeError) as excinfo:
      test_output.instance.set_number("my_long", "hihewrke")
    # Try to set a boolean with a string
    with pytest.raises(TypeError) as excinfo:
      test_output.instance.set_boolean("my_optional_bool", "hihewrke")

    # Pass non-existent field names
    with pytest.raises(rti.Error) as excinfo:
      test_output.instance["NonExistent"] = 1
    with pytest.raises(rti.Error) as excinfo:
      test_output.instance.set_number("NonExistent", 1)
    with pytest.raises(TypeError) as excinfo:
      test_output.instance.set_string("NonExistent", 1)
    with pytest.raises(rti.Error) as excinfo:
      test_output.instance.set_boolean("NonExistent", 1)

  def test_get_complex_with_getitem(self, populated_input):
    sample = populated_input.samples[0]

    point = sample["my_point"]
    # Structs converted to dict
    assert isinstance(point, dict)
    assert point['x'] == 3
    assert point['y'] == 4

    point_sequence = sample["my_point_sequence"]
    # Sequences converted to list
    assert isinstance(point_sequence, list)
    assert point_sequence[0] == {'x': 10, 'y': 20}
    assert point_sequence[1] == {'x': 11, 'y': 21}

    point_array = sample["my_point_array"]
    # Arrays converted to list
    assert isinstance(point_array, list)
    assert point_array[0] == {'x': 0, 'y': 0}
    assert point_array[4] == {'x': 5, 'y': 15}

    point_alias = sample["my_point_alias"]
    # Alias should be resolved (so in this case become a struct -> dict)
    assert isinstance(point_alias, dict)
    assert point_alias['x'] == 30
    assert point_alias['y'] == 40

    optional_point = sample["my_optional_point"]
    # Unset optional should return None
    assert optional_point is None

    union = sample["my_union"]
    # If no trailing '#' is supplied should obtain the union as a struct -> dict
    assert isinstance(union, dict)
    assert union == {'my_int_sequence': [10, 20, 30]}

    # It should not be possible to obtain complex members with get_number API,
    # though this should work with __getitem__ as shown above
    with pytest.raises(rti.Error) as excinfo:
      sample.get_number("my_point")
    # Test the same thing with get_boolean
    with pytest.raises(rti.Error) as excinfo:
      sample.get_boolean("my_point")
    # It should be possible to obtain complex members using get_string, but doing
    # this they will be of type 'str' as opposed to 'list' and 'dict'. They should
    # be in such a format that it is possible to convert them at a later point.
    point_str = sample.get_string("my_point")
    assert isinstance(point_str, str)
    assert isinstance(json.loads(point_str), dict)
    point_array_str = sample.get_string("my_point_array")
    assert isinstance(point_array_str, str)
    assert isinstance(json.loads(point_array_str), list)

  # Using the test_connector fixture as we want to get all 4 entities contained
  # within it
  def test_wait_for_data(self, test_connector):
    input1 = test_connector.get_input("TestSubscriber::TestReader")
    input2 = test_connector.get_input("TestSubscriber::TestReader2")
    output1 = test_connector.get_output("TestPublisher::TestWriter")
    output2 = test_connector.get_output("TestPublisher::TestWriter2")

    # Ensure matching between all entities occurs
    # TODO after merging CON-108
    with pytest.raises(rti.TimeoutError) as excinfo:
      input2.wait(2000)

    # All variations of wait_for_data will timeout
    with pytest.raises(rti.TimeoutError) as excinfo:
      test_connector.wait(500)
    with pytest.raises(rti.TimeoutError) as excinfo:
      input1.wait(500)
    with pytest.raises(rti.TimeoutError) as excinfo:
      input2.wait(500)

    # Now we write some data using output1 (which is matched with input1)
    output1.write()
    # Both the Connector-level wait and a wait on input1 should return
    test_connector.wait(5000)
    input1.wait(5000)
    # But a wait on input2 should timeout
    with pytest.raises(rti.TimeoutError) as excinfo:
      input2.wait(500)
    # Take the sample
    input1.take()

    # Now the same with output2
    output2.write()
    # Both the Connector-level wait and a wait on input2 should return
    test_connector.wait(-1)
    input2.wait(5000)
    # But a wait on input1 should timeout
    with pytest.raises(rti.TimeoutError) as excinfo:
      input1.wait(500)
    # Take the sample
    input2.take()

  def test_convert_from_string_in_dict(self, test_output, test_input, test_dictionary):
    test_output.instance.set_dictionary({
      'my_long': "10",
      'my_double': "3.3",
      'my_optional_bool':True,
      'my_enum': "1",
      'my_string': 'hello',
      'my_point': {'x': "3", 'y': "4"},
      'my_point_alias': {'x': "30", 'y': "40"},
      'my_union': {'my_int_sequence': ["10", "20", "30"]},
      'my_int_union': {'my_long': "222"},
      'my_point_sequence': [{'x': "10", 'y': 20}, {'x': "11", 'y': "21"}],
      'my_int_sequence': ["1", 2, 3],
      'my_point_array': [{'x': "0", 'y': 0}, {'x': 0, 'y': "0"}, {'x': 0, 'y': 0}, {'x': 0, 'y': 0}, {'x': 5, 'y': 15}],
      'my_boolean': False,
      'my_int64': "-18014398509481984",
      'my_uint64': "18014398509481984"
    })
    sample = send_data(test_output, test_input)
    assert sample.get_dictionary() == test_dictionary

  def test_bad_conversion_from_string_in_dict(self, test_output, test_dictionary):
    # For each numeric field, test that set_dictionary fails when the value we
    # try to set is a string that doesn't represent a number
    field_names = ["my_long", "my_int64", "my_double",
      "my_point_array[1].x", "my_int_sequence[1], my_enum"] # TODO: add "my_uint64" when CORE-9768 is fixed
    for name in field_names:
        with pytest.raises(rti.Error, match=r".*cannot convert field to string.*") as excinfo:
          test_output.instance.set_dictionary({name:"not a number"})
          print("Field " + name + " did not raise an exception")

  def test_error_in_dictionary(self, test_output, test_input):
    with pytest.raises(rti.Error) as excinfo:
      # sequence max length is 10
      test_output.instance.set_dictionary({"my_int_sequence":[10] * 11})
    # Make sure the previous error didn't corrupt the instance
    test_output.instance.set_dictionary({"my_int_sequence":[10] * 10})
    sample = send_data(test_output, test_input)
    assert sample["my_int_sequence"] == [10] * 10

  def test_error_in_dictionary2(self, test_output, test_input):
    with pytest.raises(rti.Error) as excinfo:
      # error parsing an element is different from error parsing sequence itself
      test_output.instance.set_dictionary({"my_point_sequence":[
        {"x": 1, "y":2}, {"x": 34, "bad":40}]})
    # Make sure the previous error didn't corrupt the instance
    test_output.instance.set_dictionary({"my_point_sequence":[
        {"x": 1, "y":2}, {"x": 34, "y":40}]})
    sample = send_data(test_output, test_input)
    assert sample["my_point_sequence[1].y"] == 40

  def test_clear_member_with_setitem(self, test_output, test_input):
    test_output.instance['my_optional_bool'] = None
    sample = send_data(test_output, test_input)
    assert sample['my_optional_bool'] is None

  def test_nested_syntax_in_dictionary(self, test_output, test_input):
    test_output.instance.set_dictionary({"my_point_sequence[2].y": 153})
    test_output.instance.set_dictionary({"my_point_sequence[2].x": 111})
    test_output.instance["my_point_sequence[3]"] = {"x":444, "y":555}
    sample = send_data(test_output, test_input)
    assert sample["my_point_sequence[2]"] == {"x":111, "y":153}
    assert sample["my_point_sequence[3]"] == {"x":444, "y":555}
