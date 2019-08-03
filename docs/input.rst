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

:meth:`Connector.get_input()` returns a :class:`Input` object. This example,
obtains the input defined by the *data_reader* named *MySquareReader* within
the *subscriber* named *MySubscriber*::

   <subscriber name="MySubscriber">
     <data_reader name="MySquareReader" topic_ref="Square" />
   </subscriber>

This *publisher* is defined inside the *domain_participant* selected to create
this ``connector`` (see :ref:`Create a new *Connector*`).

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
through all the samples with valid data and calls :meth:`SampleIterator.get_dictionary()`
to retrieve all the fields in the sample:

.. testcode::

   for sample in input.valid_data_iterator:
      print(sample.get_dictionary())

*Connect DDS* can produce samples with invalid data, which contain meta-data only.
For more information about this see `Valid Data Flag <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/The_SampleInfo_Structure.htm#receiving_2076951295_727613>`__
in the *Connect DDS Core Libraries* User's Manual.

Use :meth:`Input.data_iterator` to also access samples that contain
meta-data only:

.. testcode::

   for sample in input.data_iterator:
      print(sample.getInfo())
      if sample.valid_data:
         print(sample.get_dictionary())

The class ``Input`` itself is iterable, so it is also possible to write
``for sample in input``, which is equivalent to ``for sample in input.data_iterator``.

It is possible to access an individual sample too:

.. testcode::

   if input.sample_count > 0:
      if input[0].valid_data:
         print(input[0].get_dictionary())

Note that the equivalent method :meth:`Input.get_sample()` is also available.

TODO: explain use-cases for getInfo() (not yet implemented)

Important: calling read/take again invalidates all iterators currently in
use. For that reason, it is not recommended to store the result of
``get_sample()``.

In addition to ``get_dictionary``, you can get the values of specific fields
using :meth:`SampleIterator.get_number()`, :meth:`SampleIterator.get_bool()` and
:meth:`SampleIterator.get_string()`, for example:

.. testcode::

   for sample in input.valid_data_iterator:
      x = sample.get_number("x") # or just sample["x"]
      y = sample.get_number("y")
      size = sample.get_number("shapesize")
      color = sample.get_string("color") # or just sample["color"]

See more information in :ref:`Accessing the data`.

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