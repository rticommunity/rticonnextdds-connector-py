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

The read/take operations populate ``Input.samples`` with the data samples that
are available, and ``Input.infos`` with the corresponding meta-samples. The
following example shows how to iterate over the data::

   input.take()
   sampleCount = input.samples.getLength()
   for j in range (0, sampleCount):
      if input.infos.isValid(j):
         x = input.samples.getNumber(j, "x")
         y = input.samples.getNumber(j, "y")
         size = input.samples.getNumber(j, "shapesize")
         color = input.samples.getString(j, "color")
         print("Received x: " + repr(x) + " y: " + repr(y) + " size: " + repr(size) + " color: " + color)

You can also use a dictionary to access a full data sample at once::

   sampleCount = input.samples.getLength();
   for j in range (0, sampleCount):
      if input.infos.isValid(j)
         sample = input.samples.getDictionary(j)

         # print the whole sample
         print(sample)

         # or print a single element
         print(sample['x'])
   }

*Connect DDS* can produce samples with invalid data, and applications should
check for that with :meth:`Infos.isValid()`. For more information about this
see `Valid Data Flag <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/The_SampleInfo_Structure.htm#receiving_2076951295_727613>`__
in the *Connect DDS Core Libraries* User's Manual.

The previous example shows how to access simple fields. For more complicated types,
see :ref:`Accessing the data`.

Class reference: Input, Samples, Infos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Input class
^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.Input
   :members:


Samples class
^^^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.Samples
   :members:


Infos class
^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.Infos
   :members: