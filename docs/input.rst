Reading data (Input)
====================

.. py:currentmodule:: rticonnextdds_connector

.. testsetup:: *

   import rticonnextdds_connector as rti
   connector = rti.Connector("MyParticipantLibrary::MyParticipant", "ShapeExample.xml");


Getting the input
~~~~~~~~~~~~~~~~~

To read/take samples, first get a reference to the :class:`Input`:

.. testcode::

   input = connector.get_input("MySubscriber::MySquareReader");

:meth:`Connector.get_input()` returns a :class:`Input` object.

Reading or taking the data
~~~~~~~~~~~~~~~~~~~~~~~~~~

Then call :meth:`Input.take()` to access and remove the samples::

   input.take()

or :meth:`Input.read()` to access the samples but leaving them available for
a future ``read()`` or ``take()``::

   input.read()

Accessing the data samples
~~~~~~~~~~~~~~~~~~~~~~~~~~

After calling the read/take operations there are several ways to access the
data samples. The simplest uses :meth:`Input.valid_data_iterator` to iterate
through all the samples with valid data and calls :meth:`SampleIterator.dictionary`
to retrieve all the fields in the sample:

.. testcode::

   for sample in input.valid_data_iterator:
      print(sample.dictionary)

*Connect DDS* can produce samples with invalid data, which contain meta-data only.
For more information about this see `Valid Data Flag <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/The_SampleInfo_Structure.htm#receiving_2076951295_727613>`__
in the *Connect DDS Core Libraries* User's Manual.

Use :meth:`Input.data_iterator` to also access samples that contain
meta-data only:

.. testcode::

   for sample in input.data_iterator:
      print(sample.getInfo())
      if sample.is_valid:
         print(sample.dictionary)

It is possible to access an individual sample too:

.. testcode::

   if input.sample_count > 0:
      if input.get_sample(0).is_valid:
         print(input.get_sample(0).dictionary)

TODO: explain use-cases for getInfo() (not yet implemented)

Important: calling read/take again invalidates all iterators currently in
use. For that reason, it is not recommended to store the result of
``get_sample()``.

In addition to ``getDictionary``, you can get the values of specific fields
using :meth:`SampleIterator.get_number()`, :meth:`SampleIterator.getBoolean()` and
:meth:`SampleIterator.get_string()`, for example:

.. testcode::

   for sample in input.valid_data_iterator:
      x = sample.get_number("x")
      y = sample.get_number("y")
      size = sample.get_number("shapesize")
      color = sample.get_string("color")
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