###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

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
        Tests that a domain_participant defined in XML alongside participant_qos
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

    def test_native_library_version_getter(self):
        """
        native_library_version is a static method that can be can be called
        either before or after the creation of a Connector instance. It
        returns a structure containing the release of the native libraries.
        """
        # Ensure that we can call native_library_version before creating an
        # instance of Connector
        native_library_version = rti.Connector.native_library_version()
        assert native_library_version is not None
        assert isinstance(native_library_version, rti.ConnectorVersion)

        # The returned version should contain a major, minor, release and revision
        # field
        assert isinstance(native_library_version.major, int)
        assert isinstance(native_library_version.minor, int)
        assert isinstance(native_library_version.release, int)
        assert isinstance(native_library_version.revision, int)

        # Create an instance of Connector and call the method again
        participant_profile = "MyParticipantLibrary::ConnectorWithParticipantQos"
        xml_path = os.path.join(os.path.dirname(
                os.path.realpath(__file__)),
                "../xml/TestConnector.xml")
        with rti.open_connector(
                config_name=participant_profile,
                url=xml_path) as connector:
            assert connector is not None
            native_library_version2 = connector.native_library_version()
            assert native_library_version2 is not None
            assert isinstance(native_library_version2, rti.ConnectorVersion)

        # Check that the str() method converts the ConnectorVersion class
        # into the correct format (e.g., 6.1.0.0)
        version_str = str(native_library_version)
        assert bool(re.match("[0-9]\\.[0-9]\\.[0-9]\\.[0-9]", version_str)) == True

    def test_version_getter(self):
        """
        Connector.version is a static method that can be can be called
        either before or after the creation of a Connector instance. It
        returns a structure containing information about the release of Connector
        in use.
        """
        # Ensure that we can call native_library_version before creating an
        # instance of Connector
        version = rti.Connector.version()
        assert version is not None
        assert isinstance(version, rti.ConnectorVersion)

        # The returned version should contain a major, minor, release and revision
        # field
        assert isinstance(version.major, int)
        assert isinstance(version.minor, int)
        assert isinstance(version.release, int)
        assert isinstance(version.revision, int)

        # Create an instance of Connector and call the method again
        participant_profile = "MyParticipantLibrary::ConnectorWithParticipantQos"
        xml_path = os.path.join(os.path.dirname(
                os.path.realpath(__file__)),
                "../xml/TestConnector.xml")
        with rti.open_connector(
                config_name=participant_profile,
                url=xml_path) as connector:
            assert connector is not None
            version2 = connector.version()
            assert version2 is not None
            assert isinstance(version2, rti.ConnectorVersion)

        # Check that the str() method converts the ConnectorVersion class
        # into the correct format (e.g., "1.1.0.0")
        version_str = str(version)
        assert bool(re.match("[0-9]\\.[0-9]\\.[0-9]\\.[0-9]", version_str)) == True

    def test_build_string_getter(self):

        """
        Connector.native_build_string is a static method that can be can be called
        either before or after the creation of a Connector instance. It
        returns a string containing information about the release of native
        libraries being used by Connector.
        """
        build_str = rti.Connector.native_library_build_string()
        assert build_str is not None
        assert isinstance(build_str, str)

        # Create an instance of Connector and call the method again
        participant_profile = "MyParticipantLibrary::ConnectorWithParticipantQos"
        xml_path = os.path.join(os.path.dirname(
                os.path.realpath(__file__)),
                "../xml/TestConnector.xml")
        with rti.open_connector(
                config_name=participant_profile,
                url=xml_path) as connector:
            assert connector is not None
            build_str2 = rti.Connector.native_library_build_string()
            assert build_str2 is not None
            assert isinstance(build_str2, str)
