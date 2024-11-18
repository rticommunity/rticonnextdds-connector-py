
.. py:currentmodule:: rticonnextdds_connector

Getting Started
===============

Installing RTI Connector for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install *RTI Connector for Python* with *pip*:

.. code:: bash

   $ pip install rticonnextdds-connector

The above command installs the latest version of *Connext* by default. To
install a specific version, use this command:

.. code-block:: console

   $ pip install rticonnextdds-connector==<version>

where ``<version>`` is any valid *Connext* version in the
`Release history <https://pypi.org/project/rticonnextdds-connector/#history>`__
at pypi.org.

And then run your *Connector* applications:

.. code:: bash

    $ python my_connector_app.py


Running the examples
~~~~~~~~~~~~~~~~~~~~

The examples are in the `examples/python <https://github.com/rticommunity/rticonnextdds-connector-py/tree/master/examples/python>`__
directory of the *RTI Connector* for Python GitHub repository.

In the simple example, ``writer.py`` periodically publishes data for a
*Square* topic, and ``reader.py`` subscribes to the topic and prints all the
data samples it receives.

Run the reader as follows:

.. code:: bash

    python examples/python/simple/reader.py

In another shell, run the writer:

.. code:: bash

    python examples/python/simple/writer.py

This is what ``reader.py`` looks like:

.. literalinclude:: ../examples/python/simple/reader.py
    :lines: 18-

And this is ``writer.py``:

.. literalinclude:: ../examples/python/simple/writer.py
    :lines: 18-

You can run the reader and the writer in any order, and you can run multiple
instances of each at the same time. You can also run any other *DDS* application
that publishes or subscribes to the *Square* topic. For example, you can use
`RTI Shapes Demo <https://www.rti.com/free-trial/shapes-demo>`__.