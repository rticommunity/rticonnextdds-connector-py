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

class TestDataIterators:

  """
  This class tests the iteration of Input samples with data_iterator and
  valid_data_iterator
  """
  @pytest.fixture(scope="class")
  def populatedInput(self, rtiOutputFixture, rtiInputFixture):
    """Class fixture that writes the test messages do they're available in the input

    TODO: add an invalid-data sample (we may need to implement dispose() for
    that)

    """

    rtiInputFixture.expected_count = 3

    # Add extra element so that if the iterators fail and advance one element
    # too many, we can detect it in the zip's below
    rtiInputFixture.expected_values = [1.0, 2.0, 3.0, None]

    rtiOutputFixture.instance.set_dictionary(
      {"x":1, "y":1, "z":True, "color":"BLUE", "shapesize":5})
    rtiOutputFixture.write()

    rtiOutputFixture.instance.set_dictionary(
      {"x":2, "y":2, "z":False, "color":"RED", "shapesize":10})
    rtiOutputFixture.write()

    rtiOutputFixture.instance.set_dictionary(
      {"x":3, "y":3, "z":True, "color":"YELLOW", "shapesize":15})
    rtiOutputFixture.write()

    for i in range(1, 20):
      rtiInputFixture.read()
      if rtiInputFixture.sample_count == 3:
        break
      time.sleep(.5)

    return rtiInputFixture

  def test_data_iterator(self, populatedInput):
    """Tests Input.data_iterator"""

    assert populatedInput.sample_count == populatedInput.expected_count
    count = 0

    for sample in populatedInput.data_iterator:
      assert sample.valid_data
      assert sample.get_number("x") == populatedInput.expected_values[count]
      assert sample.get_dictionary()["y"] == populatedInput.expected_values[count]
      count = count + 1

    assert count == populatedInput.expected_count

    count = 0
    for sample in populatedInput:
      assert sample.valid_data
      assert sample.get_number("x") == populatedInput.expected_values[count]
      assert sample.get_dictionary()["y"] == populatedInput.expected_values[count]
      count = count + 1

    assert count == populatedInput.expected_count

  def test_valid_data_iterator(self, populatedInput):
    """Tests Input.valid_data_iterator"""

    assert populatedInput.sample_count == populatedInput.expected_count

    count = 0
    for sample in populatedInput.valid_data_iterator:
      assert sample.valid_data
      assert sample.get_number("x") == populatedInput.expected_values[count]
      assert sample.get_dictionary()["y"] == populatedInput.expected_values[count]
      count = count + 1

    assert count == populatedInput.expected_count