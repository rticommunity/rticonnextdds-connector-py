
.. py:currentmodule:: rticonnextdds_connector

Defining the DDS system in XML
==============================

*Connector* loads the definition of a DDS system from an XML configuration file
that includes the definition of domains, DomainParticipants, Topics, DataReaders
and DataWriters, data types and quality of service.

.. image:: static/xml_doc.png
    :align: center

*Connector* used the XML schema defined by RTI's
`XML-Based Application Creation <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/xml_application_creation/html_files/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted/index.htm>`__,
which can be loaded by the *Connext DDS* C, C++, Java and .NET APIs.

The following table summarizes the XML tags, the DDS concepts they define, and
how they are exposed in the *Connector* API:

.. list-table:: XML configuration tags
   :header-rows: 1

   * - XML tag
     - DDS Concept
     - Connector API
   * - *<types>*
     - *DDS data type* (the type associated with a *Topic*)
     - Types used by :class:`Output`\ s and :class:`Input`\ s
   * - *<domain_library>*, *<domain>*, *<register_type>*, and *<topic>*
     - *DDS Domain*, *Topic*
     - Defines the domain joined by a :class:`Connector` and the topics used by
       its :class:`Output`\ s and :class:`Input`\ s.
   * - *<domain_participant_library>* and *<domain_participant>*
     - *DomainParticipant*
     - Each :class:`Connector` instance loads a *<domain_participant>*. See :ref:`Loading a Connector`
   * - *<publisher>* and *<data_writer>*
     - *Publisher* and *DataWriter*
     - Each *<data_writer>* defines an :class:`Output`. See :ref:`Writing Data (Output)`
   * - *<subscriber>* and *<data_reader>*
     - *Subscriber* and *DataReader*
     - Each *<data_reader>* defines an :class:`Input`. See :ref:`Reading Data (Input)`
   * - *<qos_library>* and *<qos_profile>*
     - *Quality of service* (QoS)
     - Quality of service used to configure :class:`Connector`, :class:`Output`
       and :class:`Input`.

.. hint::

  For an example configuration file, see `ShapeExample.xml <https://github.com/rticommunity/rticonnextdds-connector-py/blob/master/examples/python/ShapeExample.xml>`__.

Data types
~~~~~~~~~~

The *<types>* tags defines the data types associated with the topics to be published
or subscribed to.

The following example defines a *ShapeType* with four members, *color*, *x*, *y*
and *shapesize*:

.. code-block:: xml

      <types>
        <struct name="ShapeType">
            <member name="color" type="string" stringMaxLength="128" key="true"/>
            <member name="x" type="int32"/>
            <member name="y" type="int32"/>
            <member name="shapesize" type="int32"/>
        </struct>
        ...
    </types>

Types are associated with topics, as explained in the next section, :ref:`Domain Library`.

.. hint::
    You can define your types in IDL and convert them to XML with `rtiddsgen <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/code_generator/html_files/RTI_CodeGenerator_UsersManual/index.htm#code_generator/UsersManual/UsersManual_Title.htm>`__.
    (for example, ``rtiddsgen -convertToXml MyTypes.idl``).

For more information about defining types, see
`Creating User Data Types with XML <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/Creating_User_Data_Types_with_Extensible.htm>`__
in the *Connext DDS Core Libraries User's Manual*.

For more information about accessing the data samples, see :ref:`Accessing the data`.

Domain library
~~~~~~~~~~~~~~

A domain library is a collection of domains. A domain specifies:

  * A `domain id <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/ChoosingDomainID.htm>`__
  * A set of registered types (from a subset of the types in *<types>*).
    A registered type can have a local name.
  * A set of `topics <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm>`__,
    which are used by data readers and data writers.

.. code-block:: xml

    <domain_library name="MyDomainLibrary">
        <domain name="MyDomain" domain_id="0">
            <register_type name="ShapeType" type_ref="ShapeType"/>
            <topic name="Square" register_type_ref="ShapeType"/>
            <topic name="Circle" register_type_ref="ShapeType"/>
        </domain>
    </domain_library>

For more information about the format of a domain library, see
`XML-Based Application Creation: Domain Library <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/xml_application_creation/html_files/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted/index.htm#XMLBasedAppCreation/UnderstandingPrototyper/DomainLibrary.htm#5.5.1_Domain_Library%3FTocPath%3D5.%2520Understanding%2520XML-Based%2520Application%>`__

Participant library
~~~~~~~~~~~~~~~~~~~

A domain participant joins a domain and contains publishers and subscribers,
which contain data writers and data readers, respectively.

Each :class:`Connector` instance created by your application is associated with a
*<domain_participant>*, as explained in :ref:`Loading a Connector`.

Data writers and data readers are associated with a domain participant and to a
topic. In *Connector*, each *<data_writer>* tag defines an :class:`Output`, as described in
:ref:`Writing data (Output)`; and each *<data_reader>* tag defines an :class:`Input`,
as described in :ref:`Reading data (Input)`.

.. code-block:: xml

    <domain_participant_library name="MyParticipantLibrary">
        <domain_participant name="MyPubParticipant" domain_ref="MyDomainLibrary::MyDomain">
            <publisher name="MyPublisher">
                <data_writer name="MySquareWriter" topic_ref="Square" />
            </publisher>
        </domain_participant>

        <domain_participant name="MySubParticipant" domain_ref="MyDomainLibrary::MyDomain">
            <subscriber name="MySubscriber">
                <data_reader name="MySquareReader" topic_ref="Square" />
            </subscriber>
        </domain_participant>
    </domain_participant_library>

For more information about the format of a participant library, see
`XML-Based Application Creation: Participant Library <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/xml_application_creation/html_files/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted/index.htm>`__

Quality of service
~~~~~~~~~~~~~~~~~~

All DDS entities have an associated `quality of service (Qos) <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/QosPolicies.htm>`__.
There are several ways to configure it.

You can define a Qos profile and make it the default. The following example
configures all data readers and data writers with reliable and transient-local Qos:

.. code-block:: xml

    <qos_library name="MyQosLibrary">
        <qos_profile name="MyQosProfile" is_default_qos="true">
            <datareader_qos>
                <reliability>
                    <kind>RELIABLE_RELIABILITY_QOS</kind>
                </reliability>
                <durability>
                    <kind>TRANSIENT_LOCAL_DURABILITY_QOS</kind>
                </durability>
            </datareader_qos>
            <datawriter_qos>
                <reliability>
                    <kind>RELIABLE_RELIABILITY_QOS</kind>
                </reliability>
                <durability>
                    <kind>TRANSIENT_LOCAL_DURABILITY_QOS</kind>
                </durability>
            </datawriter_qos>
        </qos_profile>
        ...
    </qos_library>

You can define the Qos for each individual entity:

.. code-block:: xml

    <domain_participant name="MyPubParticipant" domain_ref="MyDomainLibrary::MyDomain">
        <participant_qos> ... </participant_qos>
        <publisher name="MyPublisher">
            <publisher_qos> ... </publisher_qos>
            <data_writer name="MySquareWriter" topic_ref="Square">
                <datawriter_qos>
                    <reliability>
                        <kind>RELIABLE_RELIABILITY_QOS</kind>
                    </reliability>
                    <durability>
                        <kind>TRANSIENT_LOCAL_DURABILITY_QOS</kind>
                    </durability>
                </datawriter_qos>
            </data_writer>
        </publisher>
        ...
    </domain_participant>

Or you can use profiles and override or define additional Qos policies for each
entity:

.. code-block:: xml

    <domain_participant name="MyPubParticipant" domain_ref="MyDomainLibrary::MyDomain">
        <participant_qos base_name="MyQosLibrary::MyQosProfile">
            <!-- override or configure additional Qos policies -->
        </participant_qos>
        <publisher name="MyPublisher">
            <publisher_qos base_name="MyQosLibrary::MyQosProfile">
                <!-- override or configure additional Qos policies -->
            </publisher_qos>
            <data_writer name="MySquareWriter" topic_ref="Square">
                <datawriter_qos base_name="MyQosLibrary::MyQosProfile">
                    <!-- override or configure additional Qos policies -->
                </datawriter_qos>
            </data_writer>
        </publisher>
    </domain_participant>

In all cases, you can specify a built-in profile as the value for the *base_name*
attribute. For example, you can use *BuiltinQosLib::Generic.StrictReliable*
instead of defining the reliability policy yourself:

.. code-block:: xml

    <qos_library name="MyQosLibrary">
        <qos_profile name="MyQosProfile"
                     base_name="BuiltinQosLib::Generic.StrictReliable"
                     is_default_qos="true">
            <datareader_qos>
                <durability>
                    <kind>TRANSIENT_LOCAL_DURABILITY_QOS</kind>
                </durability>
            </datareader_qos>
            <datawriter_qos>
                <durability>
                    <kind>TRANSIENT_LOCAL_DURABILITY_QOS</kind>
                </durability>
            </datawriter_qos>
        </qos_profile>
        ...
    </qos_library>

You can read more in the *Connext DDS Core Libraries User's Manual*, `Configuring Qos profiles in XML <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/XMLConfiguration.htm>`__.