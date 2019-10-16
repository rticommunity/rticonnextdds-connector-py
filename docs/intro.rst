
.. py:currentmodule:: rticonnextdds_connector

Introduction to RTI Connector
=============================

RTI Connext DDS
~~~~~~~~~~~~~~~

Connext DDS is a software connectivity framework for real-time distributed
applications. It uses the publish-subscribe communications model to make
data distribution efficient and robust. At its core Connext DDS is the world's
leading ultra-high performance, distributed networking databus.

RTI Connext DDS provides programming APIs in C, C++, Java, and .NET.

.. note::

    This documentation assumes you are already familiar with the basic DDS concepts.
    You can learn about DDS in the *Core Libraries Getting Started Guide*,
    *Core Libraries User's Manual*, and the *Connext DDS* API documentation for C,
    C++, Java and .NET. These documents are available at the
    `RTI Community portal <https://community.rti.com/documentation>`__

RTI Connector
~~~~~~~~~~~~~

Connector is a family of simplified APIs that allow publishing and subscribing
to the Connext DDS Databus in other programming languages, such as Python
and JavaScript.

In *Connector*, the DDS entities and their data types and quality of service are
defined in XML. Applications instantiate a ``Connector`` object to load an
XML file and create all the entities that allow publishing and subscribing to data.

*Connector* uses the XML format of `RTI's XML-Based Application Creation <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/xml_application_creation/html_files/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted/index.htm#XMLBasedAppCreation/UnderstandingPrototyper/XMLTagsConfigEntities.htm%3FTocPath%3D5.%2520Understanding%2520XML-Based%2520Application%2520Creation%7C5.5%2520XML%2520Tags%2520for%2520Configuring%2520Entities%7C_____0>`__.
All *Connext DDS* language APIs can load XML files with the same format.

.. image:: static/overview.png
    :align: center

In *Connector*, there are three basic entities: ``Connector``, ``Input``
and ``Output``:

.. list-table:: Connector entities
   :header-rows: 1

   * - *Connector* entity
     - Related DDS entity
     - Related XML tag
   * - :ref:`Connector <Loading a Connector>`
     - DomainParticipant
     - *<domain_participant>*
   * - :ref:`Output <Writing Data (Output)>`
     - DataWriter
     - *<data_writer>*
   * - :ref:`Input <Reading Data (Input)>`
     - DataReader
     - *<data_reader>*

The three entities can be configured with *Quality of Service*.

A ``Connector`` is associated to a *domain*.

Each ``Input`` and ``Output`` is associated to a *topic*, which has a concrete *data type*.

How to read this documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First learn how to install *Connector* and run the examples in :ref:`Getting Started`.

:ref:`Loading a Connector`, :ref:`Writing Data (Output)`, and :ref:`Reading Data (Input)`
walk you through the API and explain how to use it. These sections include
examples and detailed type and function documentation.

:ref:`Advanced Topics` explains the type system, and the different ways to
access the data; the threading model; and how errors are reported.

If you want to know whether a *Connext DDS* feature is supported in *Connector*,
and how to use it, see :ref:`Connext DDS Features`.

If you're looking for a specific class or function, see the :ref:`genindex`.
