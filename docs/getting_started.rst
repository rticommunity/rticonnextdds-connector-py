
.. py:currentmodule:: rticonnextdds_connector

Getting Started
===============

Installing RTI Connector for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure you have Python installed. Then use *pip* to install *RTI Connector*
as follows:

.. code:: bash

   $ pip install rticonnextdds_connector

You can also clone the repository:

.. code:: bash

   $ git clone --recursive https://github.com/rticommunity/rticonnextdds-connector-py.git

Running the examples
~~~~~~~~~~~~~~~~~~~~

To run the examples, first clone the repository as indicated in the previous section,
then run any of the python scripts in the ``examples/python`` directory:

.. code:: bash

    python examples/python/simple/reader.py

On another shell:

.. code:: bash

    python examples/python/simple/writer.py

This is how ``reader.py`` looks like:

.. literalinclude:: ../examples/python/simple/reader.py
    :lines: 19-


And this is ``writer.py``:

.. literalinclude:: ../examples/python/simple/writer.py
    :lines: 17-

To learn more about *RTI Connector* continue to the next section,
:ref:`Using a Connector`.

Supported Platforms
~~~~~~~~~~~~~~~~~~~

*RTI Connector* has been tested with Python 2.7.14 and 3.6.3.

*RTI Connector* uses a native C library. It has been tested on the following
platforms:

- Windows (64-bit Windows 10 with VS 2015 and 32-bit Windows 7 with VS 2017)
- Linux (64-bit CentOS 6.5 with gcc 4.8.2, 32-bit Ubuntu 16.04 gcc 5.4.0, and
- MacOS (Darwin 18 clang 10)

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