Writing Data (Output)
=====================

.. py:currentmodule:: rticonnextdds_connector


.. testsetup:: *

   import rticonnextdds_connector as rti
   connector = rti.Connector("MyParticipantLibrary::MyParticipant", "ShapeExample.xml")

Getting the Output
~~~~~~~~~~~~~~~~~~

To write a data sample, first look up an :class:`Output`:

.. testcode::

   output = connector.get_output("MyPublisher::MySquareWriter")

:meth:`Connector.get_output()` returns an :class:`Output` object. This example 
obtains the output defined by the ``<data_writer>`` named *MySquareWriter* within
the ``<publisher>`` named *MyPublisher*:

.. code-block:: xml

   <publisher name="MyPublisher">
     <data_writer name="MySquareWriter" topic_ref="Square" />
   </publisher>

This ``<publisher>`` is defined inside the ``<domain_participant>`` selected to create
this ``connector`` (see :ref:`Creating a new Connector`).

Populating the data sample
~~~~~~~~~~~~~~~~~~~~~~~~~~

Then set the ``output.instance`` fields. You can set them member by member:

.. testcode::

   output.instance.set_number("x", 1)
   output.instance.set_number("y", 2)
   output.instance.set_number("shapesize", 30)
   output.instance.set_string("color", "BLUE")

Or using a dictionary:

.. testcode::

   output.instance.set_dictionary({"x":1, "y":2, "shapesize":30, "color":"BLUE"})

The name of each member corresponds to the type assigned to this output in XML.
For example:

.. code-block:: xml

   <struct name="ShapeType">
     <member name="color" type="string" stringMaxLength="128" key="true" default="RED"/>
     <member name="x" type="long" />
     <member name="y" type="long" />
     <member name="shapesize" type="long" default="30"/>
    </struct>

See :class:`Instance` and :ref:`Accessing the data` for more information.

Writing the data sample
~~~~~~~~~~~~~~~~~~~~~~~

To write the values you set in ``output.instance``, call :meth:`Output.write()`::

   output.write()

If the ``<datawriter_qos>`` is set up for reliable communication, you can use
:meth:`Output.wait()` to block until all matching reliable *Subscribers*
acknowledge reception of the data sample::

    output.wait()

The write method can receive several options. For example, to
write with a specific timestamp:

.. testcode::

  output.write(source_timestamp=100000)

It is also possible to dispose or unregister an instance:

.. testcode::

  output.write(action="dispose")
  output.write(action="unregister")

In these two cases, only the *key* fields in the ``output.instance`` are relevant
when determining the instance that is disposed or unregistered.

See :meth:`Output.write` for more information on the supported parameters.

Matching with a subscription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before writing, you can use the method :meth:`Output.wait_for_subscriptions()` to
detect when a compatible DDS subscription is matched or stops matching. It returns
the change in the number of matched subscriptions since the last time it was called::

   change_in_matches = output.wait_for_subscriptions()

For example, if a new compatible subscription is discovered within the specified
``timeout``, the function returns 1; if a previously matching subscription
no longer matches (for example, due to the application being closed), it returns -1.

You can obtain information about the currently matched subscriptions with
:attr:`Output.matched_subscriptions`:

.. testcode::

   matched_subs = output.matched_subscriptions
   for sub_info in matched_subs:
    sub_name = sub_info['name']

Class reference: Output, Instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Output class
^^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.Output
   :members:

Instance class
^^^^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.Instance
   :members:
