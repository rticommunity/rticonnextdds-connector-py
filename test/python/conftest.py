###############################################################################
# (c) 2005-2019 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

import sys, os, pytest, threading, time

sys.path.append(os.path.dirname(os.path.realpath(__file__))+ "/../../")
import rticonnextdds_connector as rti

"""
This module contains pytest fixtures used for testing connector code.
"""

@pytest.fixture(scope="session")
def rtiConnectorFixture(request):
  """
  This `pytest fixture <https://pytest.org/latest/fixture.html>`_
  creates a session-scoped :class:`rticonnextdds_connector.Connector` object
  which is returned everytime this fixture method is referred.
  The initialized Connector object is cleaned up at the end
  of a testing session.

  ``MyParticipantLibrary::Zero`` `participant
  <https://community.rti.com/static/documentation/connext-dds/5.2.3/doc/api/connext_dds/api_cpp2/classdds_1_1domain_1_1DomainParticipant.html>`_
  profile in ``test/xml/TestConnector.xml`` `application profile
  <https://community.rti.com/rti-doc/510/ndds.5.1.0/doc/pdf/RTI_CoreLibrariesAndUtilities_XML_AppCreation_GettingStarted.pdf>`_
  is used for initializing the Connector object.

  :param request: builtin pytest request fixture
  :type request: `pytest.FixtureRequest <https://pytest.org/latest/builtin.html>`_
  :returns: session-scoped Connector for testing
  :rtype: :class:`rticonnextdds_connector.Connector`

  """
  xml_path= os.path.join(os.path.dirname(os.path.realpath(__file__)),
    "../xml/TestConnector.xml")
  participant_profile="MyParticipantLibrary::Zero"
  rti_connector = rti.Connector(participant_profile,xml_path)

  def cleanup():
    rti_connector.close()

  request.addfinalizer(cleanup)
  return rti_connector

@pytest.fixture(scope="session")
def rtiInputFixture(rtiConnectorFixture):
  """
  This `pytest fixture <https://pytest.org/latest/fixture.html>`_
  creates a session-scoped :class:`rticonnextdds_connector.Input` object
  which is returned everytime this fixture method is referred.
  The initialized Input object is cleaned up at the end
  of a testing session.

  ``MySubscriber::MySquareReader`` `datareader
  <https://community.rti.com/static/documentation/connext-dds/5.2.3/doc/api/connext_dds/api_cpp2/classdds_1_1sub_1_1DataReader.html>`_ in
  ``test/xml/TestConnector.xml`` `application profile
  <https://community.rti.com/rti-doc/510/ndds.5.1.0/doc/pdf/RTI_CoreLibrariesAndUtilities_XML_AppCreation_GettingStarted.pdf>`_
  is used for initializing the Input object.

  :param rtiConnectorFixture: :func:`rtiConnectorFixture`
  :type rtiConnectorFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_
  :returns: session-scoped Input object for testing
  :rtype: :class:`rticonnextdds_connector.Input`

  """

  return rtiConnectorFixture.get_input("MySubscriber::MySquareReader")

@pytest.fixture(scope="session")
def rtiOutputFixture(rtiConnectorFixture):
  """
  This `pytest fixture <https://pytest.org/latest/fixture.html>`_
  creates a session-scoped :class:`rticonnextdds_connector.Output` object
  which is returned everytime this fixture method is referred.
  The initialized Output object is cleaned up at the end
  of a testing session.

  ``MyPublisher::MySquareWriter``  `datawriter
  <https://community.rti.com/static/documentation/connext-dds/5.2.3/doc/api/connext_dds/api_cpp2/classdds_1_1pub_1_1DataWriter.html>`_ in
  ``test/xml/TestConnector.xml``  `application profile
  <https://community.rti.com/rti-doc/510/ndds.5.1.0/doc/pdf/RTI_CoreLibrariesAndUtilities_XML_AppCreation_GettingStarted.pdf>`_
  is used for initializing the Output object.

  :param rtiConnectorFixture: :func:`rtiConnectorFixture`
  :type rtiConnectorFixture: `pytest.fixture  <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_
  :returns: session-scoped Output object for testing
  :rtype: :class:`rticonnextdds_connector.Output`
  """

  return rtiConnectorFixture.getOutput("MyPublisher::MySquareWriter")

@pytest.fixture
def one_use_connector(request):
    """Creates a Connector only for one test. Use this when
       the test can't reuse a previously created connector"""

    xml_path = os.path.join(
      os.path.dirname(os.path.realpath(__file__)),
      "../xml/TestConnector.xml")

    participant_profile="MyParticipantLibrary::Zero"
    with rti.open_connector(participant_profile, xml_path) as rti_connector:
      yield rti_connector

@pytest.fixture
def one_use_output(one_use_connector):
  return one_use_connector.get_output("MyPublisher::MySquareWriter")

@pytest.fixture
def one_use_input(one_use_connector):
  return one_use_connector.get_input("MySubscriber::MySquareReader")
