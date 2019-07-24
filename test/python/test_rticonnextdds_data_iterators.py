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

    assert populatedInput.sample_count == 3

    for sample, i in zip(populatedInput.data_iterator, range(1, 10)):
      assert sample.valid_data
      assert sample.get_number("x") == i
      assert sample.get_dictionary()["y"] == i

    for sample, i in zip(populatedInput, range(1, 10)):
      assert sample.valid_data
      assert sample.get_number("x") == i
      assert sample.get_dictionary()["y"] == i

  def test_valid_data_iterator(self, populatedInput):
    """Tests Input.valid_data_iterator"""

    assert populatedInput.sample_count == 3

    for sample, i in zip(populatedInput.valid_data_iterator, range(1, 10)):
      assert sample.valid_data
      assert sample.get_number("x") == i
      assert sample.get_dictionary()["y"] == i
