Other topics
============

Accessing the data
~~~~~~~~~~~~~~~~~~

.. py:currentmodule:: rticonnextdds_connector

The types you use to write or read data may included nested structs, sequences and
arrays of primitive types or structs, etc.

These types are defined in the XML following the format of
`RTI's XML-Based Application Creation <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/xml_application_creation/html_files/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted/index.htm#XMLBasedAppCreation/UnderstandingPrototyper/XMLTagsConfigEntities.htm%3FTocPath%3D5.%2520Understanding%2520XML-Based%2520Application%2520Creation%7C5.5%2520XML%2520Tags%2520for%2520Configuring%2520Entities%7C_____0>`__.

To access the data, :class:`Instance` and :class:`Samples` provide
setters and getters that expect a ``fieldName`` string. This section describes
the format of this string.

TODO: complete section

Accessing nested structs
^^^^^^^^^^^^^^^^^^^^^^^^

"x.y.z"

Accessing arrays and sequences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

"x[1]"

"x[1].z"

"x#"

Accessing unions
^^^^^^^^^^^^^^^^

"x.y"


Multi-threading
~~~~~~~~~~~~~~~

Threading model
^^^^^^^^^^^^^^^

The *Connector* API does not implement any mechanism for
thread safety. Applications are responsible for protecting concurrent calls to
the Connector API. In Python, you will have to protect the calls to
*Connector* if you are using different threads.

The following section shows an example.

TODO: review, complete section

Protecting calls to *Connector*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example shows how to use the Python ``threading`` package to
protect calls to *Connector*, one of multiple ways to do so::

   import threading

   sem = threading.Semaphore()

   sem.acquire(True)

   # Use the Connector API
   input.take();
   sampleCount = input.samples.getLength()
   # ...

   sem.release()
   ...
   ...

