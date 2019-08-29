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
from test_utils import *


class TestMetadata:
  """
  This class tests write with options and sample info
  """

  def test_bad_info_field(self, one_use_output, one_use_input):
    sample = send_data(one_use_output, one_use_input)
    with pytest.raises(rti.Error, match=r".*Unknown.*nonexistent.*") as excinfo:
      sample.info["nonexistent"]

  def test_timestamp(self, one_use_output, one_use_input):
    sample = send_data(one_use_output, one_use_input, source_timestamp=2)
    assert sample.info["source_timestamp"] == 2
    assert sample.info["reception_timestamp"] != 2 and sample.info["reception_timestamp"] > 0

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
