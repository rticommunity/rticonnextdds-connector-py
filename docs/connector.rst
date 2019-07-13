Using a Connector
=================

.. py:currentmodule:: rticonnextdds_connector

Import the *Connector* package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use the ``rticonnextdds_connector`` package, import it. For example::

   import rticonnextdds_connector as rti

Create a new *Connector*
~~~~~~~~~~~~~~~~~~~~~~~~

To create a new :class:`Connector`, pass an XML file and a configuration name::

   connector = rti.Connector("MyParticipantLibrary::Zero","ShapeExample.xml");

*Connector* uses The XML format of `RTI's XML-Based Application Creation <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/xml_application_creation/html_files/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted/index.htm#XMLBasedAppCreation/UnderstandingPrototyper/XMLTagsConfigEntities.htm%3FTocPath%3D5.%2520Understanding%2520XML-Based%2520Application%2520Creation%7C5.5%2520XML%2520Tags%2520for%2520Configuring%2520Entities%7C_____0>`__.

Delete a *Connector*
~~~~~~~~~~~~~~~~~~~~

To destroy all the *Connext DDS* entities that belong to a *Connector* previously
created, call :meth:`Connector.delete()`::

   connector = rti.Connector("MyParticipantLibrary::Zero","./ShapeExample.xml")
   ...
   ...
   connector.delete()


Reading and Writing Data
~~~~~~~~~~~~~~~~~~~~~~~~

Once you have created a ``Connector`` instance, :meth:`Connector.getOutput()`
returns the :class:`Output` that allows writing data, and :meth:`Connector.getInput()`
returns the :class:`Input` that allows reading data.

For more information see:

    * :ref:`Writing data (Output)`
    * :ref:`Reading data (Input)`

Class reference: Connector
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: rticonnextdds_connector.Connector
   :members:

