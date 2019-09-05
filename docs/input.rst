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

This *subscriber* is defined inside the *domain_participant* selected to create
this ``connector`` (see :ref:`Create a new *Connector*`).

Matching with a Publication
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The method :meth:`Input.wait_for_publications()` can be used to detect when a compatible
DDS publication is matched or unmatched. It returns the change in the number of
matched publications since the last time it was called::

   change_in_matches = Input.wait_for_publications()

For example, if a new :class:`Output` was matched within the
specified ``timeout``, the function would return 1. If, at a later point, this :class:`Output`
left the network, a subsequent call to :meth:`Input.wait_for_publications()` would return
-1.
The optional ``timeout`` argument can be used to specify the maximum amount of time in
milliseconds to wait for a new match. If no match is found within the ``timeout``, :class:`TimeoutError`
is raised. By default the timeout is infinite.


In order to ascertain whether or not an :class:`Input` is matched with a specific :class:`Output`, you
should use the :meth:`Input.get_matched_publications()` method. This method returns a list
of the *Publication Names* of all of the matched :class:`Output`.

.. testcode::

   matched_outputs = input.get_matched_publications()

.. note::
    The list returned will contain the name of each matched publication.
    If one of them didn't specify a name, the list will contain a None element
    instead. In any case, the size of the list reflects the current number of
    matched publication.

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

Use :meth:`Input.data_iterator` to also access samples that contain
meta-data only (see next section, :ref:`Accessing the SampleInfo`):

.. testcode::

   for sample in input.data_iterator:
      # Access sample.info
      if sample.valid_data:
         print(sample.get_dictionary())

The class ``Input`` itself is iterable, so it is also possible to write
``for sample in input``, which is equivalent to ``for sample in input.data_iterator``.

It is possible to access an individual sample too:

.. testcode::

   if input.sample_count > 0:
      if input[0].valid_data:
         print(input[0].get_dictionary())

The method :meth:`Input.get_sample()` is also available; ``input[i]`` is equivalent
to ``input.get_sample(i)``.

.. warning::
   All the methods described in this section return iterators to samples.
   Calling read/take again invalidates all iterators currently in
   use. For that reason, it is not recommended to store any iterator.

``get_dictionary`` can receive a ``field_name`` to only return the fields of a
complex member. In addition to ``get_dictionary``, you can get the values of
specific primitive fields using :meth:`SampleIterator.get_number()`,
:meth:`SampleIterator.get_boolean()` and :meth:`SampleIterator.get_string()`,
for example:

.. testcode::

   for sample in input.valid_data_iterator:
      x = sample.get_number("x") # or just sample["x"]
      y = sample.get_number("y")
      size = sample.get_number("shapesize")
      color = sample.get_string("color") # or just sample["color"]

See more information in :ref:`Accessing the data`.

Accessing the SampleInfo
~~~~~~~~~~~~~~~~~~~~~~~~

*Connect DDS* can produce samples with invalid data, which contain meta-data only.
For more information about this see `Valid Data Flag <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/The_SampleInfo_Structure.htm#receiving_2076951295_727613>`__
in the *Connect DDS Core Libraries* User's Manual.

You can access a field of the sample meta-data, the *SampleInfo*, as follows:

.. testcode::

   for sample in input.data_iterator:
      source_timestamp = sample.info["source_timestamp"]


See :meth:`SampleIterator.info` for the list of meta-data fields available

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