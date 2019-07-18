Reading data (Input)
====================

.. py:currentmodule:: rticonnextdds_connector

Getting the input
~~~~~~~~~~~~~~~~~

To read/take samples, first get a reference to the :class:`Input`::

   input = connector.getInput("MySubscriber::MySquareReader");

:meth:`Connector.getInput()` returns a :class:`Input` object.

Reading or taking the data
~~~~~~~~~~~~~~~~~~~~~~~~~~

Then call :meth:`Input.take()` to access and remove the samples:

   input.take()

or :meth:`Input.read()` to access the samples but leaving them available for
a future ``read()`` or ``take()``::

   input.take()

Accessing the data samples
~~~~~~~~~~~~~~~~~~~~~~~~~~

After calling the read/take operations there are several ways to access the
data samples. The simplest uses :meth:`Input.getValidDataIterator()` to iterate
through all the samples with valid data and calls :meth:`SampleIterator.getDictionary()`
to retrieve all the fields in the sample::

   for sample in input.getValidDataIterator():
      print(sample.getDictionary())

*Connect DDS* can produce samples with invalid data, which contain meta-data only.
For more information about this see `Valid Data Flag <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/The_SampleInfo_Structure.htm#receiving_2076951295_727613>`__
in the *Connect DDS Core Libraries* User's Manual.

Use :meth:`Input.getDataIterator()` to also access samples that contain 
meta-data only::

   for sample in input.getDataIterator():
      print(sample.getInfo())
      if sample.isValid():
         print(sample.getDictionary())

It is possible to access an individual sample too::

   if input.getSampleCount() > 0:
      if input.getSample(0).isValid():
         print(input.getSample(0).getDictionary())

TODO: explain use-cases for getInfo() (not yet implemented)

Important: calling read/take again invalidates all iterators currently in
use. For that reason, it is not recommended to store the result of
``getSample()``.

In addition to ``getDictionary``, you can get the values of specific fields
using :meth:`SampleIterator.getNumber()`, :meth:`SampleIterator.getBoolean()` and
:meth:`SampleIterator.getString()`, for example::

   for sample in input.getValidDataIterator():
      x = sample.getNumber("x")
      y = sample.getNumber("y")
      size = sample.getNumber("shapesize")
      color = sample.getString("color")
      print("Received x: " + repr(x) + " y: " + repr(y) + " size: " + repr(size) + " color: " + color)

The previous example shows how to access simple fields. For more complicated types,
see :ref:`Accessing the data`.

Class reference: Input, SampleIterator, ValidSampleIterator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Input class
^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.Input
   :members:


SampleIterator class
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.SampleIterator
   :members:


ValidSampleIterator class
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.ValidSampleIterator
   :members: