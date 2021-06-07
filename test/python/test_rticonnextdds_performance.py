###############################################################################
# (c) 2020 Copyright, Real-Time Innovations.  All rights reserved.            #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

import pytest,sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+ "/../../")
import rticonnextdds_connector as rti
from test_utils import *
import ctypes

# iterations is configured by passing `--iterations <>` on the command line.
# By default, pytest captures the stdout. Supply -s to view the results.

# These tests currently take around 25 minutes to run with 100 iterations.
# They were added to help verify performance of another product, connextdds-py.
# If you want to run them, remove this decorator.
# Maybe once CON-42 is implemented we can run them by default.
@pytest.mark.skip(reason="Takes too long to run these tests, remove this line and run manually")
class TestPerformance:
    """
    This class tests the performance of Connector
    """

    # The use-case of setting a sequence in Connector is slow, and likely will
    # be until we implement CON-42.
    # Here we time how long it takes to set a sequence element by element.
    def test_set_sequence_element_by_element(self, one_use_connector, iterations):
        # Get the input and output which communicate using the performance test type
        the_input = one_use_connector.get_input("MySubscriber::PerformanceTestReader")
        the_output = one_use_connector.get_output("MyPublisher::PerformanceTestWriter")

        # Wait for discovery between the entities
        wait_for_discovery(the_output, the_input)

        # Set each element of the sequence separately
        total_time = 0
        for i in range(0, iterations):
            start_time = time.time()
            for i in range (0, 600000):
                the_output.instance['myOctSeq[%d]' % (i)] = 2
            total_time += (time.time() - start_time)
        average_time = total_time / iterations
        print("Average time setting element-by-element: " + str(average_time))
        # Average time setting element-by-element: 2.9646800351142883

    # The use-case of setting a sequence in Connector is slow, and likely will
    # be until we implement CON-42.
    # Here we time how long it takes to set a sequence from a Python list.
    # i.e., output.instance['myOctSeq'] = [1, 2, 3, 4, 5, ....]
    def test_set_sequence_from_list(self, one_use_connector, iterations):
        # Get the input and output which communicate using the performance test type
        the_input = one_use_connector.get_input("MySubscriber::PerformanceTestReader")
        the_output = one_use_connector.get_output("MyPublisher::PerformanceTestWriter")

        # Wait for discovery between the entities
        wait_for_discovery(the_output, the_input)

        # Create a python list which contains 600000 and set the sequence from it
        total_time = 0
        average_time = 0
        myOctSeq = [0]
        for i in range (1, 600000):
            myOctSeq.append(i)

        for i in range (0, iterations):
            start_time = time.time()
            the_output.instance['myOctSeq'] = myOctSeq
            total_time += (time.time() - start_time)
        average_time = total_time / iterations
        print("Average time setting entire list in one go: " + str(average_time))
        # Note to self Average time: 6.60276771068573

    # The use-case of obtaining a dictionary containing a sequence in Connector
    # is slow, and likely will be until we implement CON-42.
    # Here we have a sequence with 600000 elements. We time how long it takes to
    # obtain this sequence as a Python list
    def test_get_sequence(self, one_use_connector, iterations):
        # Get the input and output which communicate using the performance test type
        the_input = one_use_connector.get_input("MySubscriber::PerformanceTestReader")
        the_output = one_use_connector.get_output("MyPublisher::PerformanceTestWriter")

        # Wait for discovery between the entities
        wait_for_discovery(the_output, the_input)
        # Set the sample on the writer (the performance of this operation is tested
        # in the test_set_sequence test)
        the_output.instance['myOctSeq[599999]'] = 2
        # Write the sample and receive it on the input
        sample = send_data(the_output, the_input)

        # Now we can test the performance. We time how long it takes to retrieve the
        # sequence as a dictionary, repeat x times and take the average
        total_time = 0
        for i in range (0, iterations):
            start_time = time.time()
            myOctSeq = sample['myOctSeq']
            total_time += (time.time() - start_time)
        average_time = total_time / iterations
        print("Average time to get sequence as a list: " + str(average_time))
        # Note to self Average time: 0.20733366489410401

    # Use the workaround of calling into the native DynamicData APIs directly.
    # We do not run this test on Windows as we would need an entire Connext
    # DDS Pro installation due to the symbols not being exported
    @pytest.mark.xfail(sys.platform.startswith("win"), reason="symbols not exported")
    def test_get_sequence_native(self, one_use_connector, iterations):
        # Get the input and output which communicate using the performance test type
        the_input = one_use_connector.get_input("MySubscriber::PerformanceTestReader")
        the_output = one_use_connector.get_output("MyPublisher::PerformanceTestWriter")
        # Wait for discovery between the entities
        wait_for_discovery(the_output, the_input)

        # We need to use the following native API:
        # DDS_ReturnCode_t DDS_DynamicData_set_octet_array(
        #       DDS_DynamicData *,
        #       const char *,
        #       DDS_DynamicDataMemberId,
        #       DDS_UnisgnedLong
        #       const DDS_Octet *)
        DDS_DynamicData_set_octet_array = rti.connector_binding.library.DDS_DynamicData_set_octet_array
        DDS_DynamicData_set_octet_array.restype = ctypes.c_int
        DDS_DynamicData_set_octet_array.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long, ctypes.c_ulong, ctypes.c_void_p]

        # Create Python list for what we are going to set
        myOctSeq = [b'f'] * 600000
        # Get native handle
        native_dynamic_data = the_output.instance.native
        # Get length as ctype
        array_length = ctypes.c_ulong(len(myOctSeq))
        # Define ctype
        in_array_type = ctypes.c_char * len(myOctSeq)
        # Create instance of new type
        in_array = in_array_type(*myOctSeq)
        total_time = 0
        for i in range (0, iterations):
            start_time = time.time()
            DDS_DynamicData_set_octet_array(
                    ctypes.cast(native_dynamic_data, ctypes.c_void_p),
                    'myOctSeq'.encode("utf8"),
                    0,
                    array_length,
                    ctypes.byref(in_array))
            total_time += (time.time() - start_time)
        average_time = total_time / iterations

        print("Average time to set a sequence using native Dynamic Data APIs: " + str(average_time))


    # Use the workaround of calling into the native DynamicData APIs directly.
    # We do not run this test on Windows as we would need an entire Connext
    # DDS Pro installation due to the symbols not being exported
    @pytest.mark.xfail(sys.platform.startswith("win"), reason="symbols not exported")
    def test_set_sequence_native(self, one_use_connector, iterations):
        # Get the input and output which communicate using the performance test type
        the_input = one_use_connector.get_input("MySubscriber::PerformanceTestReader")
        the_output = one_use_connector.get_output("MyPublisher::PerformanceTestWriter")
        # Wait for discovery between the entities
        wait_for_discovery(the_output, the_input)
        # Set the sample on the writer (the performance of this operation is tested
        # in the test_set_sequence test)
        the_output.instance['myOctSeq[599999]'] = 2
        # Write the sample and receive it on the input
        sample = send_data(the_output, the_input)

        # We need to use the following native API:
        # DDS_ReturnCode_t DDS_DynamicData_get_octet_array(
        #       DDS_DynamicData * self,
        #       DDS_Octet *array,
        #       DDS_UnsignedLong *length,
        #       const char *name,
        #       DDS_DynamicDataMemberId member_id)
        DDS_DynamicData_get_octet_array = rti.connector_binding.library.DDS_DynamicData_get_octet_array
        DDS_DynamicData_get_octet_array.restype = ctypes.c_int
        DDS_DynamicData_get_octet_array.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_ulong]

        # First creates an unsigned long for the sequence length
        array_length = ctypes.c_ulong(600000)
        # Now define a type that we will use to store the result
        in_array_type = ctypes.c_char * 600000
        # Create an instance of that type
        in_array = in_array_type()
        # Call the Native API
        total_time = 0
        for i in range (0, iterations):
            start_time = time.time()
            DDS_DynamicData_get_octet_array(
                    ctypes.cast(sample.native, ctypes.c_void_p),
                    ctypes.byref(in_array),
                    ctypes.byref(array_length),
                    'myOctSeq'.encode("utf8"),
                    0)
            total_time += (time.time() - start_time)
        average_time = total_time / iterations
        print("Average time to obtain a sequence using native Dynamic Data APIs: " + str(average_time))
