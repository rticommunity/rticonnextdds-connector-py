###############################################################################
# (c) 2019 Copyright, Real-Time Innovations.  All rights reserved.            #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

import sys, os, pytest, threading, time

sys.path.append(os.path.dirname(os.path.realpath(__file__))+ "/../../")
import rticonnextdds_connector as rti

def open_test_connector(config_name):
    xml_path = os.path.join(
      os.path.dirname(os.path.realpath(__file__)),
      "../xml/TestConnector.xml")

    return rti.open_connector(config_name, xml_path)

def wait_for_data(input, count = 1, do_take = True):
  """Waits until input has count samples"""

  for i in range(1, 5):
    input.read()
    if input.sample_count == count:
      break
    input.wait(1000)

  assert input.sample_count == count
  if do_take:
    input.take()

def send_data(output, input, **kwargs):
  """Writes one sample with optional arguments (kwargs) and returns the sample
  received by the input"""

  output.write(**kwargs)
  wait_for_data(input)
  return input[0]
