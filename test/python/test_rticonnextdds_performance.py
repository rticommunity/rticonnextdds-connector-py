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
        the_input.wait_for_publications(5000)
        the_output.wait_for_subscriptions(5000)

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
        the_input.wait_for_publications(5000)
        the_output.wait_for_subscriptions(5000)

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
        the_input.wait_for_publications(5000)
        the_output.wait_for_subscriptions(5000)
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
