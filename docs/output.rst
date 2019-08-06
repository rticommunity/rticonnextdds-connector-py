Writing data (Output)
=====================

.. py:currentmodule:: rticonnextdds_connector


.. testsetup:: *

   import rticonnextdds_connector as rti
   connector = rti.Connector("MyParticipantLibrary::MyParticipant", "ShapeExample.xml");

Getting the Output
~~~~~~~~~~~~~~~~~~

To write a data sample, first get a reference to the output port:

.. testcode::

   output = connector.get_output("MyPublisher::MySquareWriter")

:meth:`Connector.get_output()` returns an :class:`Output` object. This example,
obtains the output defined by the *data_writer* named *MySquareWriter* within
the *publisher* named *MyPublisher*::

   <publisher name="MyPublisher">
     <data_writer name="MySquareWriter" topic_ref="Square" />
   </publisher>

This *publisher* is defined inside the *domain_participant* selected to create
this ``connector`` (see :ref:`Create a new *Connector*`).

Populating the data sample
~~~~~~~~~~~~~~~~~~~~~~~~~~

Then set the ``Output.instance`` fields. You can set them member by member:

.. testcode::

   output.instance.set_number("x", 1)
   output.instance.set_number("y", 2)
   output.instance.set_number("shapesize", 30)
   output.instance.set_string("color", "BLUE")

Or using a dictionary:

.. testcode::

   output.instance.set_dictionary({"x":1, "y":2, "shapesize":30, "color":"BLUE"})

The name of each member corresponds to the type assigned to this output in XML.
For example::

   <struct name="ShapeType">
     <member name="color" type="string" stringMaxLength="128" key="true" default="RED"/>
     <member name="x" type="long" />
     <member name="y" type="long" />
     <member name="shapesize" type="long" default="30"/>
    </struct>

See :class:`Instance` and :ref:`Accessing the data` for more information.

Writing the data sample
~~~~~~~~~~~~~~~~~~~~~~~

To write the values you set in ``Output.instance`` call :meth:`Output.write()`::

   output.write()

If the *datawriter_qos* is reliable, you can use :meth:`Output.wait()`
to block until all matching reliable subscribers acknowledge the reception of the
data sample::

    output.wait()

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
