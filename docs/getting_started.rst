
.. py:currentmodule:: rticonnextdds_connector

Getting Started
===============

Installing RTI Connector for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two ways to obtain *RTI Connector* for Python. You can install it with
*pip*:

.. code:: bash

   $ pip install rticonnextdds_connector

And then run your *RTI Connector* applications:

.. code:: bash

    $ python my_connector_app.py

You can also clone the repository and run the examples directly without installing
*RTI Connector*:

.. code:: bash

   $ git clone --recursive https://github.com/rticommunity/rticonnextdds-connector-py.git

In order to gain access to the examples, clone the github repository.

Running the examples
~~~~~~~~~~~~~~~~~~~~

The examples are located in the `examples/python <https://github.com/rticommunity/rticonnextdds-connector-py/tree/master/examples/python>`__
directory of the *RTI Connector for Python* GitHub repository.

In the simple example, `writer.py` periodically publishes data for a
*Square* topic, and `reader.py` subscribes to the topic and prints all the
data samples it receives.

Run the reader as follows:

.. code:: bash

    python examples/python/simple/reader.py

And, in another shell, run the writer:

.. code:: bash

    python examples/python/simple/writer.py

This is how ``reader.py`` looks like:

.. literalinclude:: ../examples/python/simple/reader.py
    :lines: 18-

And this is ``writer.py``:

.. literalinclude:: ../examples/python/simple/writer.py
    :lines: 18-

You can run the reader and the writer in any order, and you can run multiple
instances of each at the same time. You can also run any other *DDS* application
that publishes or subscribes to the *Square* topic. For example, you can use
`RTI Shapes Demo <https://www.rti.com/free-trial/shapes-demo>`__.

To learn more about *RTI Connector* continue to the next section,
:ref:`Using a Connector`.

Supported Platforms
~~~~~~~~~~~~~~~~~~~

*RTI Connector* works with Python 2.x and 3.x. It uses a native C library that
runs on most Windows, Linux and MacOS platforms.

*RTI Connector* has been tested with Python 2.6+ and 3.6.8+ on the following systems:

    * Windows: Windows 7 and Windows 10
    * x86/x86_64 Linux: CentOS 6.1, 7.6, 8.0; Ubuntu 12.04, 18.04; SUSE 12, 15
    * ARM Linux (Raspberry Pi)
    * Mac: OS X 10.10.2, macOS 10.12.2, macOS 10.14

(TODO: link to main Connector landing page)

*RTI Connector* is supported in other languages in addition to Python, see
`main Connector
repository <https://github.com/rticommunity/rticonnextdds-connector>`__.

License
~~~~~~~

With the sole exception of the contents of the “examples” subdirectory,
all use of this product is subject to the RTI Software License Agreement
included at the top level of this repository. Files within the
“examples” subdirectory are licensed as marked within the file.

(TODO: final license)