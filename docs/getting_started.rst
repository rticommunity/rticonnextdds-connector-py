
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

*RTI Connector* has been tested with Python 2.7.14 and 3.6.3.

*RTI Connector* uses a native C library that works on most Windows, Linux and
MacOS platforms. It has been tested on the following systems:

(TODO: clarify PAM)

- Windows: 64-bit Windows 10 with VS 2015 and 32-bit Windows 7 with VS 2017
- Linux: 64-bit CentOS 6.5 with gcc 4.8.2, 32-bit Ubuntu 16.04 gcc 5.4.0, and ARM Yocto Linux 2.0.3 with gcc 5.2.0
- MacOS: Darwin 18 with clang 10

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