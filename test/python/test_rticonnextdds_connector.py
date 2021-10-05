###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

from platform import version
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
import rticonnextdds_connector as rti
import pytest

class TestConnector:
    """
    This class tests the correct instantiation of
    :class:`rticonnextdds_connector.Connector` object.
    """

    def test_invalid_xml_path(self):
        """
        This test function ensures that a ValueError is raised if
        an incorrect xml path is passed to the
        Connector constructor.
        """
        participant_profile = "MyParticipantLibrary::Zero"
        invalid_xml_path = "invalid/path/to/xml"
        with pytest.raises(rti.Error):
            rti.Connector(participant_profile, invalid_xml_path)

    def test_invalid_participant_profile(self):
        """
        This test function ensures that a ValueError is raised if
        an invalid participant profile name is passed to the
        Connector constructor.
        """
        invalid_participant_profile = "InvalidParticipantProfile"
        xml_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "../xml/TestConnector.xml")
        with pytest.raises(rti.Error):
            rti.Connector(invalid_participant_profile, xml_path)

    def test_ivalid_xml_profile(self):
        """
        This test function ensures that a ValueError is raised if
        an invalid xml file is passed to the
        Connector constructor.
        """
        participant_profile = "MyParticipantLibrary::Zero"
        invalid_xml = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   "../xml/InvalidXml.xml")
        with pytest.raises(rti.Error):
            rti.Connector(participant_profile, invalid_xml)

    def test_connector_creation(self, rtiConnectorFixture):
        """
        This function tests the correct instantiation of
        Connector object.
        """
        assert rtiConnectorFixture is not None and isinstance(
            rtiConnectorFixture, rti.Connector)

    def test_multiple_connector_creation(self):
        """
        This function tests the correct instantiation of multiple
        Connector objects in succession.
        """
        connectors = []
        xml_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "../xml/TestConnector.xml")
        participant_profile = "MyParticipantLibrary::Zero"
        for _ in range(0, 5):
            connectors.append(rti.Connector(participant_profile, xml_path))
        assert all(x is not None and isinstance(x, rti.Connector)
                   for x in connectors)

    def test_load_multiple_files(self):
        """
        Tests that it is possible to load two xml files using the url group syntax
        """
        xml_path1 = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 "../xml/TestConnector.xml")
        xml_path2 = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 "../xml/TestConnector2.xml")
        with rti.open_connector(
                config_name="MyParticipantLibrary2::MyParticipant2",
                url=xml_path1 + ';' + xml_path2) as connector:

            assert connector is not None
            output = connector.get_output("MyPublisher2::MySquareWriter2")
            assert output is not None

    def test_connector_creation_with_participant_qos(self):
        """
        Tests that a domain_participant defined in XML alonside participant_qos
        can be used to create a Connector object.
        """
        participant_profile = "MyParticipantLibrary::ConnectorWithParticipantQos"
        xml_path = os.path.join(os.path.dirname(
                os.path.realpath(__file__)),
                "../xml/TestConnector.xml")
        with rti.open_connector(
                config_name=participant_profile,
                url=xml_path) as connector:
            assert connector is not None

    def test_get_version(self):
        """
        version is a static method that can be can be called
        either before or after the creation of a Connector instance. It returns
        a string providing information about the versions of the native libraries
        in use, and the version of the API.
        """
        # Ensure that we can call version before creating a Connector instance
        version_string = rti.Connector.get_version()
        assert version_string is not None
        # The returned version should contain 4 pieces of information:
        # - the API version of Connector
        # - the build ID of core.1.0
        # - the build ID of dds_c.1.0
        # - the build ID of lua_binding.1.0
        assert bool(re.match("RTI Connector for Python, version (([0-9]\\.){2}[0-9]|unknown)", version_string, re.DOTALL)) == True
        assert bool(re.match(".*NDDSCORE_BUILD_([0-9]\\.){2}[0-9]_[0-9]{8}T[0-9]{6}Z", version_string, re.DOTALL)) == True
        assert bool(re.match(".*NDDSC_BUILD_([0-9]\\.){2}[0-9]_[0-9]{8}T[0-9]{6}Z", version_string, re.DOTALL)) == True
        assert bool(re.match(".*RTICONNECTOR_BUILD_([0-9]\\.){2}[0-9]_[0-9]{8}T[0-9]{6}Z", version_string, re.DOTALL)) == True

    def test_setting_max_objects_per_thread(self):
        """
        It should be possible to modify max_objects_per_thread
        """
        rti.Connector.set_max_objects_per_thread(2048)

    def test_connector_double_deletion(self):
        """Verify CON-200, that Connector does not segfault on double deletion"""
        participant_profile = "MyParticipantLibrary::ConnectorWithParticipantQos"
        xml_path = os.path.join(os.path.dirname(
                os.path.realpath(__file__)),
                "../xml/TestConnector.xml")
        with rti.open_connector(
                config_name=participant_profile,
                url=xml_path) as connector:
            assert connector is not None
            connector.close()
        # connector.close() will be called again here due to the with clause
