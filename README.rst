rticonnextdds-connector: Python
===============================

(return to
`rticonnextdds-connector <https://github.com/rticommunity/rticonnextdds-connector>`__)

RTI Connector for Connext DDS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*RTI Connector* for Connext DDS is a quick and easy way to access the
power and functionality of `RTI Connext
DDS <http://www.rti.com/products/index.html>`__. It is based on
`XML-Based Application
Creation <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/xml_application_creation/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted.pdf>`__
and Dynamic Data.

Language Support
~~~~~~~~~~~~~~~~

This repository is specific to Python. For other languages (lua, C,
etc.), refer to the `main Connector
repository <https://github.com/rticommunity/rticonnextdds-connector>`__.

We use ctypes to call our native functions; these details are hidden in
a Python wrapper. RTI tested its Python implementation with both Python
2.7.14 and Python 3.6.3.

Platform support
~~~~~~~~~~~~~~~~

Python *Connector* builds its library for `select
architectures <https://github.com/rticommunity/rticonnextdds-connector/tree/master/lib>`__.
If you need another architecture, please contact your RTI account
manager or sales@rti.com.

### Testing We tested on: \* For MacOS 64 bit : Darwin 18 clang 10 \*
For Windows 64 bit: Windows 10 64 bit VS2015 \* For Windows 32 bit:
Windows 7 32 bit VS2017 \* For Linux 64 bit: CentOS 6.5 gcc 4.8.2 \* For
Linux 32 bit: Ubuntu 16.04 gcc 5.4.0 \* For ARM: Yocto linux 2.0.3 gcc
5.2.0

Version of Connext
~~~~~~~~~~~~~~~~~~

To check the version of the libraries, run the following command. For
example:

.. code:: bash

   strings librtiddsconnector.dylib | grep BUILD

Threading model
~~~~~~~~~~~~~~~

The *Connector* Native API does not yet implement any mechanism for
thread safety. For now, the responsibility of protecting calls to the
*Connector* is left to you. (In future, thread safety may be added in
the native layer.) In Python, you will have to protect the calls to
*Connector* if you are using different threads. For an example, see
`Protecting calls to the Connector
library <https://github.com/rticommunity/rticonnextdds-connector-py#protecting-calls-to-the-connector-library>`__
below.

Support
~~~~~~~

*Connector* is an experimental RTI product. If you have questions, use
the `RTI Community
forum <https://community.rti.com/forums/technical-questions>`__.

Getting started with Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Be sure you have Python. Then use pip to install the *Connector*:

.. code:: bash

   $ pip install rticonnextdds_connector

You can also clone the repository:

.. code:: bash

   $ git clone --recursive https://github.com/rticommunity/rticonnextdds-connector-py.git

Available examples
~~~~~~~~~~~~~~~~~~

You can find several sets of examples in the
`examples/python <examples/python>`__ directory.

-  **simple**: shows how to write samples and how to read/take.
-  **mixed**: contains various examples.

Protecting calls to the *Connector* library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As explained above, you are responsible for protecting calls to
*Connector*. There are many options in Python to do so; one is to use
the ``threading`` package:

.. code:: py

   ...
   ...
   import threading
   sem = threading.Semaphore();
   ...
   ...
   #acquire the semaphore
   sem.acquire(True);
   #call to connector APissem.acquire(True);
   input.take();
   numOfSamples = input.samples.getLength();
   ...
   ...
   #release the semaphore
   sem.release();
   ...
   ...

For more information on the threading Python packages, see the `Python
documentation <https://docs.python.org/2/library/threading.html>`__.

API overview
~~~~~~~~~~~~

require the *Connector* library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use ``rticonnextdds_connector``, import it:

.. code:: py

   import rticonnextdds_connector as rti

instantiate a new *Connector*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a new *Connector*, pass an XML file and a configuration name.

.. code:: py

   connector = rti.Connector("MyParticipantLibrary::Zero","./ShapeExample.xml");

For more information on the XML format, see the `XML-Based Application
Creation
guide <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/xml_application_creation/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted.pdf>`__
or look at the `ShapeExample.xml <examples/python/ShapeExample.xml>`__
file included in this examples directory.

delete a *Connector*
^^^^^^^^^^^^^^^^^^^^

To destroy all the DDS entities that belong to a *Connector* previously
created, call the ``delete`` function.

.. code:: py

   connector = rti.Connector("MyParticipantLibrary::Zero","./ShapeExample.xml");
   ...
   ...
   connector.delete();

write a sample
^^^^^^^^^^^^^^

To write a sample, first get a reference to the output port:

.. code:: py

   output = connector.getOutput("MyPublisher::MySquareWriter")

Then set the instance’s fields:

.. code:: py

   output.instance.setNumber("x", 1);
   output.instance.setNumber("y", 2);
   output.instance.setNumber("shapesize", 30);
   output.instance.setString("color", "BLUE");

Then write:

.. code:: py

   output.write();

set the instance’s fields:
^^^^^^^^^^^^^^^^^^^^^^^^^^

The content of an instance can be set by using a dictionary that matches
the original type, or field by field.

-  **Using a dictionary**:

.. code:: py

   #assuming that sample is a dictionary containing
   #an object of the same type of the output.instance:

   output.instance.setDictionary(sample);

-  **Field by field**:

.. code:: py

   output.instance.setNumber("y", 2);

The following APIs set an instance field by field:
``setNumber(fieldName, number);`` ``setBoolean(fieldName, boolean);``
and ``setString(fieldName, string);``.

Nested fields can be accessed with the dot notation ``"x.y.z"``. Arrays
or sequences can be accessed with square brakets: ``"x.y[1].z"``. For
more information on how to access fields, see the “Data Access API”
section of the `RTI Prototyper Getting Started
Guide <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/prototyper/RTI_ConnextDDS_CoreLibraries_Prototyper_GettingStarted.pdf>`__.

read/take data
^^^^^^^^^^^^^^

To read/take samples, first get a reference to the input port:

.. code:: py

   input = connector.getInput("MySubscriber::MySquareReader");

Then call the ``read()`` or ``take()`` API:

.. code:: py

   input.read();

or

.. code:: pu

    input.take();

The read/take operation can return multiple samples. Therefore, you must
iterate on an array:

.. code:: py

       input.take();
       numOfSamples = input.samples.getLength();
       for j in range (1, numOfSamples+1):
           if input.infos.isValid(j):
               x = input.samples.getNumber(j, "x");
               y = input.samples.getNumber(j, "y");
               size = input.samples.getNumber(j, "shapesize");
               color = input.samples.getString(j, "color");
               toPrint = "Received x: " + repr(x) + " y: " + repr(y) + " size: " + repr(size) + " color: " + repr(color);
               print(toPrint);
   }

access sample fields after a read/take
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A ``read()`` or ``take()`` operation can return multiple samples. They
are stored in an array. Every time you try to access a specific sample,
you have to specify an index (j in the example below).

You can access the data by getting a copy in a dictionary object, or you
can access each field individually:

-  **Using a dictionary**:

.. code:: py

    numOfSamples = input.samples.getLength();
    for j in range (1, numOfSamples+1):
        if input.infos.isValid(j):
            sample = input.samples.getDictionary(j);
            #print the whole sample
            print(sample);
            #or print a single element
            print(sample['x']);
    }

-  **Field by field**:

.. code:: py

    numOfSamples = input.samples.getLength();
    for j in range (1, numOfSamples+1):
        if input.infos.isValid(j):
            x = input.samples.getNumber(j, "x");
            y = input.samples.getNumber(j, "y");
            size = input.samples.getNumber(j, "shapesize");
            color = input.samples.getString(j, "color");
            toPrint = "Received x: " + repr(x) + " y: " + repr(y) + " size: " + repr(size) + " color: " + repr(color);
            print(toPrint);
    }

The following APIs access the samples field by field:
``getNumber(indexm fieldName);`` ``getBoolean(index, fieldName);`` and
``getString(index, fieldName);``.

License
~~~~~~~

With the sole exception of the contents of the “examples” subdirectory,
all use of this product is subject to the RTI Software License Agreement
included at the top level of this repository. Files within the
“examples” subdirectory are licensed as marked within the file.

This software is an experimental (“pre-production”) product. The
Software is provided “as is,” with no warranty of any type, including
any warranty for fitness for any purpose. RTI is under no obligation to
maintain or support the software. RTI shall not be liable for any
incidental or consequential damages arising out of the use or inability
to use the software.

(return to
`rticonnextdds-connector <https://github.com/rticommunity/rticonnextdds-connector>`__)
