Connext DDS features
====================

.. py:currentmodule:: rticonnextdds_connector

Because *RTI Connector* is a simplified API, it provides access to a subset of the
features in *RTI Connext DDS*.

In addition to the functionality described in the rest of this documentation, this
section summarizes the support that *Connector* provides for some notable
*Connext DDS* features.

General features
~~~~~~~~~~~~~~~~

.. list-table:: General Features
   :widths: 7 5 25
   :header-rows: 1

   * - Feature
     - Level of support
     - Notes
   * - `Quality of Service (QoS) <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/RTI_ConnextDDS_CoreLibraries_QoS_Reference_Guide.pdf>`__
     - Partial
     - Most QoS policies are supported because they can be configured in XML, but those that are
       designed to be mutable can't be changed in *Connector*. QoS policies that require
       a supporting API may have limited or no support.

       A few examples of QoS policies that are fully supported in *Connector*:

        * Reliability
        * Durability
        * History
        * Ownership

       A few examples of QoS policies that are supported but can't be changed in
       *Connector* even though they are mutable by design and changeable in other APIs:

        * Partition
        * Lifespan
        * Ownership Strength
        * Property and User Data
        * Time-Based Filter

       A few examples of QoS policies that have limited support because they require
       a supporting API that is not available in *Connector*:

        * Batch - fully supported except that manual flushing is not available
        * Entity Factory - *autoenable_created_entities* can be set to *false* only for a *subscriber*, in
          order to enable an `Input` only when :meth:`Connector.get_input` is called.
        * Property - Properties can be set in XML, but they can't be looked up in *Connector*
        
        `Topic Qos <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/Setting_Topic_QosPolicies.htm>`__ is not supported in *Connector*. Use DataReader QoS and DataWriter QoS directly.
   * - `Entity Statuses <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/Statuses.htm>`__
     - Partial
     - Only :meth:`Input.wait` (data available), :meth:`Input.wait_for_publications`, and :meth:`Output.wait_for_subscriptions` are supported.
   * - `Managing Data Instances <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/Managing_Data_Instances__Working_with_Ke.htm>`__
     - Partial
     - It is possible to dispose or unregister an instance (see :meth:`Output.write`), and instances are automatically registered when first written, but on the ``Input`` side, the instance status is not currently exposed. Instance handles are not exposed.
   * - `Application Acknowledgment <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/Application_Acknowledgment.htm>`__
     - Partial
     - *DDS_APPLICATION_AUTO_ACKNOWLEDGMENT_MODE* is supported. If enabled, when a call to :meth:`Input.take` or :meth:`Input.read` is followed by another call, the second one automatically acknowledges the samples read in the first one.

       *DDS_APPLICATION_EXPLICIT_ACKNOWLEDGMENT_MODE* is not supported.
   * - `Request-Reply <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/PartRequestReplyPattern.htm>`__
     - Partial
     - The correlation between two samples can be established at the application level:

            * The *Requester* application writes by calling :meth:`Output.write` with the parameter ``identity=A`` (the *request* sample)
            * The *Replier* application receives the *request* sample, obtains the ``identity`` (A),  from ":attr:`SampleIterator.info` and writes a new sample with ``related_sample_identity=A`` (the *reply* sample)
            * The *Requester* application receives the *reply* sample, and correlates the ``related_sample_identity`` from :attr:`SampleIterator.info` with the ``identity`` it used in the first step.

   * - `Topic Queries <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/TopicQueries.htm#23._Topic_Queries>`__
     - Partial
     - ``Input`` doesn't have the API to create a *TopicQuery*, but in the configuration file a *data_writer* can enable support for *TopicQuery* so other *Connext DDS Subscribers* can query the *Connector Publisher*.
   * - `Zero Copy Transfer Over Shared Memory <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/SendingLDZeroCopy.htm>`__
     - Not supported
     - Only available in C and C++.
   * - `Built-in Topics <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/builtintopics.htm>`__
     - Not supported
     - API not available.
   * - `Transport Plugins <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/transports.htm>`__
     - Partial
     - The built-in transports can be configured in XML, but add-ons cannot be loaded (see next).
   * - Add-on Libraries 
       (such as `Monitoring <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/PartMonitoringLib.htm>`__, 
       `Security Plugins <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/dds_security/html_files/RTI_SecurityPlugins_GettingStarted/index.htm>`__ )
     - Not supported
     - *Connector* currently cannot load dynamically linked add-on libraries.

Features related to sending data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Features Related to Sending Data
   :widths: 7 5 25
   :header-rows: 1

   * - Feature
     - Level of support
     - Notes
   * - `Waiting for Acknowledgments <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/WaitingForAcksDataWriter.htm#6.3.11_Waiting_for_Acknowledgments_in_a_DataWriter>`__
     - Supported
     - See :meth:`Output.wait`.
   * - `Coherent Sets <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/WritingCoherentSetsSample.htm#6.3.10_Writing_Coherent_Sets_of_DDS_Data_Samples>`__
     - Not supported
     - API not available.
   * - `Flow Controllers <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/FlowControllers__DDS_Extension_.htm>`__
     - Partial
     - Most functionality is available via XML QoS configuration.
   * - `Asserting Liveliness Manually <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/Asserting_Liveliness.htm>`__
     - Not supported
     - API not available.
   * - `Collaborative DataWriters <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/Config_Collaborative_DWs.htm>`__
     - Limited
     - The virtual GUID can be set per writer in XML, but not per sample.

Features related to receiving data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Features Related to Receiving Data
   :widths: 7 5 25
   :header-rows: 1

   * - Feature
     - Level of support
     - Notes
   * - `Content-Filtered Topics <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/ContentFilteredTopics.htm>`__
     - Partial
     - `Configurable in XML <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/xml_application_creation/html_files/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted/index.htm#XMLBasedAppCreation/UnderstandingPrototyper/CreatingContentFilters.htm>`__  but it can't be modified after creation
   * - `Sample Info <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/The_SampleInfo_Structure.htm#7.4.6_The_SampleInfo_Structure>`__
     - Partial
     - See :attr:`SampleIterator.info`
   * - `Query Conditions <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/ReadConditions_and_QueryConditions.htm#4.6.7.2_QueryConditions>`__
     - Not supported
     - API not available
   * - `Group-Ordered Access <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/BeginEndGroupOrderedAccess.htm#>`__
     - Not supported
     - API not available
   * - `Waiting for Historical Data <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/Waiting_for_Historical_Data.htm>`__
     - Not supported
     - API not available

Features related to the type system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Features Related to the Type System
   :widths: 7 5 25
   :header-rows: 1

   * - Feature
     - Level of support
     - Notes
   * - `DDS type system <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/Introduction_to_the_Type_System.htm>`__
     - Supported
     - *Connector* can use any DDS type. Types are defined in XML.
   * - `Type extensibility <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/getting_started_extras/html_files/RTI_ConnextDDS_CoreLibraries_GettingStarted_ExtensibleAddendum/index.htm#ExtensibleTypesAddendum/Type_Safety_and_System_Evolution.htm>`__
     - Supported
     - *Connector* supports type extensibility, including mutable types in the XML definition of types. It also supports type-consistency enforcement  
       and sample-assignability enforcement; these checks are performed by the *RTI Connext DDS* Core.
   * - `Optional members <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/getting_started_extras/html_files/RTI_ConnextDDS_CoreLibraries_GettingStarted_ExtensibleAddendum/index.htm#ExtensibleTypesAddendum/Optional_Members.htm>`__
     - Supported
     - See :ref:`Accessing optional members`.
   * - `Default values <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/getting_started_extras/html_files/RTI_ConnextDDS_CoreLibraries_GettingStarted_ExtensibleAddendum/index.htm#ExtensibleTypesAddendum/DefaultValue.htm>`__
     - Supported
     -  For example, to declare a default value for a member::

            <struct name= "MyType" extensibility="mutable">
                <!-- ... -->
                <member name="my_int" type="int32" default="20" />
            </struct>

        Now the value for *my_int* when you call :meth:`Output.write` without
        setting it explicitly is 20. And when you receive a data sample in an
        ``Input`` from a *Publisher* whose type is compatible, but doesn't have the
        field *my_int*, the value you receive will be 20.

   * - `Unbounded data <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/Sequences.htm>`__
     - Supported
     -  To declare an unbounded sequence or string, set its max length to *-1*::

            <struct name= "MyType">
             <member name="my_unbounded_int_sequence" sequenceMaxLength="-1" type="int32"/>
             <member name="my_bounded_int_sequence" sequenceMaxLength="10" type="int32"/>
            </struct>

        For any ``Output`` using a topic for a type with unbounded members, set the
        following in the ``<property>`` QoS policy::

            <datawriter_qos>
             <!-- ... -->
             <property>
              <value>
               <element>
                <name>
                 dds.data_writer.history.memory_manager.fast_pool.pool_buffer_max_size
                </name>
                <value>4096</value>
               </element>
              </value>
             </property>
            </datawriter_qos>

        The value *4096* is a threshold that indicates *Connext DDS* should allocate
        memory dynamically for data samples that exceed that size. For samples below
        that threshold, memory comes from pre-allocated buffers.

        If the unbounded member is a *key*, then in any ``Input`` that uses the type,
        set the following::

            <datareader_qos>
             <!-- ... -->
             <property>
              <value>
               <element>
                <name>
                 dds.data_reader.history.memory_manager.fast_pool.pool_buffer_max_size
                </name>
                <value>4096</value>
               </element>
              </value>
             </property>
            <datareader_qos>

   * - `FlatData Language Binding <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/SendingLDFlatData.htm>`__
     - Not supported
     - However, an ``Input`` can receive data published by other *Connext DDS* applications that use FlatData.

