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
  This class tests the iteration of Input Samples
  """
  @pytest.fixture(scope="class")
  def populatedInput(self, rtiOutputFixture, rtiInputFixture):
    """Class fixture that writes the test messages do they're available in the input

    """

    rtiInputFixture.expected_count = 4

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

    rtiOutputFixture.write(action="dispose")

    for i in range(1, 20):
      rtiInputFixture.read()
      if rtiInputFixture.samples.length == rtiInputFixture.expected_count:
        break
      time.sleep(.5)

    return rtiInputFixture

  def test_data_iterator(self, populatedInput):
    """Tests SampleIterator, Samples"""

    assert populatedInput.samples.length == populatedInput.expected_count

    count = 0
    for sample in populatedInput.samples:
      if count <= 2:
        assert sample.valid_data
        assert sample.get_number("x") == populatedInput.expected_values[count]
        assert sample.get_dictionary()["y"] == populatedInput.expected_values[count]
      else:
        assert not sample.valid_data
      count = count + 1
    assert count == populatedInput.expected_count

    assert populatedInput.samples[0].get_number("x") == populatedInput.expected_values[0]

    count = 0
    for i in range(populatedInput.samples.length):
      sample = populatedInput.samples[i]
      if count <= 2:
        assert sample.valid_data
        assert sample.get_number("x") == populatedInput.expected_values[i]
        assert sample.get_dictionary()["y"] == populatedInput.expected_values[i]
      else:
        assert not sample.valid_data
      count = count + 1
    assert count == populatedInput.expected_count

  def test_valid_data_iterator(self, populatedInput):
    """Tests Samples.valid_data_iterator"""

    assert populatedInput.samples.length == populatedInput.expected_count

    count = 0
    for sample in populatedInput.samples.valid_data_iter:
      assert sample.valid_data
      assert sample.get_number("x") == populatedInput.expected_values[count]
      assert sample.get_dictionary()["y"] == populatedInput.expected_values[count]
      count = count + 1

    assert count == populatedInput.expected_count - 1

  def test_no_data(self, populatedInput):
    populatedInput.take() # First take removes samples (they were read() before)
    populatedInput.take() # Second take returns no data, leaves samples empty
    assert populatedInput.samples.length == 0
    had_data = False
    for _ in populatedInput.samples:
      had_data = True
    assert not had_data
