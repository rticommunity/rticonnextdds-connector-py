Using a Connector
=================

.. py:currentmodule:: rticonnextdds_connector

Import the *Connector* package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use the ``rticonnextdds_connector`` package, import it. For example:

.. testcode::

   import rticonnextdds_connector as rti

Create a new *Connector*
~~~~~~~~~~~~~~~~~~~~~~~~

To create a new :class:`Connector`, pass an XML file and a configuration name:

.. testcode::

   connector = rti.Connector("MyParticipantLibrary::MyParticipant", "ShapeExample.xml");

*Connector* uses The XML format of `RTI's XML-Based Application Creation <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/xml_application_creation/html_files/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted/index.htm#XMLBasedAppCreation/UnderstandingPrototyper/XMLTagsConfigEntities.htm%3FTocPath%3D5.%2520Understanding%2520XML-Based%2520Application%2520Creation%7C5.5%2520XML%2520Tags%2520for%2520Configuring%2520Entities%7C_____0>`__.

See an example here: `ShapeExample.xml <https://github.com/rticommunity/rticonnextdds-connector-py/blob/master/examples/python/ShapeExample.xml>`__.

When you create a ``Connector``, the DDS *DomainParticipant* you select and all
its contained entities (*Topics*, *Subscribers*, *DataReaders*, *Publishers*, *DataWriters*)
are created.

For more information about the DDS entities, see `Part 2 - Core Concepts <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/PartCoreConcepts.htm#partcoreconcepts_4109331811_915546%3FTocPath%3DPart%25202%253A%2520Core%2520Concepts%7C_____0>`__
from the *RTI Connext DDS Core Libraries User's Manual*.

Closing a *Connector*
~~~~~~~~~~~~~~~~~~~~~

To destroy all the DDS entities that belong to a *Connector* previously
created, call :meth:`Connector.close()`:

.. testcode::

   connector = rti.Connector("MyParticipantLibrary::MyParticipant","./ShapeExample.xml")
   # ...
   connector.close()

Alternatively, you can use the :meth:`open_connector` resource manager to open
and automatically close the connector:

.. testcode::

   with rti.open_connector("MyParticipantLibrary::MyParticipant", "ShapeExample.xml") as connector:
      # Use connector
      input = connector.get_input("MySubscriber::MySquareReader");

Reading and Writing Data
~~~~~~~~~~~~~~~~~~~~~~~~

Once you have created a ``Connector`` instance, :meth:`Connector.get_output()`
returns the :class:`Output` that allows writing data, and :meth:`Connector.get_input()`
returns the :class:`Input` that allows reading data.

For more information see:

    * :ref:`Writing data (Output)`
    * :ref:`Reading data (Input)`

Class reference: Connector
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: rticonnextdds_connector.Connector
   :members:

.. autofunction:: rticonnextdds_connector.open_connector