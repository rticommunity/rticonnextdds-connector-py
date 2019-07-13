Writing data (Output)
=====================

.. py:currentmodule:: rticonnextdds_connector

Getting the Output
~~~~~~~~~~~~~~~~~~

To write a data sample, first get a reference to the output port::

   output = connector.getOutput("MyPublisher::MySquareWriter")

:meth:`Connector.getOutput()` returns an :class:`Output` object.

Populating the data sample
~~~~~~~~~~~~~~~~~~~~~~~~~~

Then set the ``Output.instance`` fields. You can set them member by member::

   output.instance.setNumber("x", 1)
   output.instance.setNumber("y", 2)
   output.instance.setNumber("shapesize", 30)
   output.instance.setString("color", "BLUE")

Or using a dictionary::

   output.instance.setDictionary({"x":1, "y":2, "shapesize":30, "color":"BLUE"})

The name of each member corresponds to the type assigned to this output in XML.
For the previous example, this is a possible XML definition::

   <struct name="ShapeType">
		<member name="color" type="string" stringMaxLength="128" key="true" default="RED"/>
		<member name="x" type="long" />
		<member name="y" type="long" />
		<member name="shapesize" type="long" default="30"/>
	</struct>

See :class:`Instance` and See :ref:`Accessing the data` for more information.

Writing the data sample
~~~~~~~~~~~~~~~~~~~~~~~

To write the values you set in ``Output.instance`` call :meth:`Output.write()`::

   output.write()

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
