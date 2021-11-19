Reading Data (Input)
====================

.. py:currentmodule:: rticonnextdds_connector

.. testsetup:: *

   import rticonnextdds_connector as rti
   connector = rti.Connector("MyParticipantLibrary::MyParticipant", "ShapeExample.xml")


Getting the input
~~~~~~~~~~~~~~~~~

To read/take samples, first get a reference to the :class:`Input`:

.. testcode::

   input = connector.get_input("MySubscriber::MySquareReader")

:meth:`Connector.get_input()` returns a :class:`Input` object. This example
obtains the input defined by the ``<data_reader>`` named *MySquareReader* within
the ``<subscriber>`` named *MySubscriber*:

.. code-block:: xml

   <subscriber name="MySubscriber">
     <data_reader name="MySquareReader" topic_ref="Square" />
   </subscriber>

This ``<subscriber>`` is defined inside the ``<domain_participant>`` selected
to create this ``connector`` (see :ref:`Creating a new Connector`).

Reading or taking the data
~~~~~~~~~~~~~~~~~~~~~~~~~~

Call :meth:`Input.take()` to access and remove the samples::

   input.take()

or :meth:`Input.read()` to access the samples but leave them available for
a future ``read()`` or ``take()``::

   input.read()

The method :meth:`Input.wait()` can be used to identify when there is new data
available on a specific :class:`Input`. It will block until either the supplied
timeout expires (in which case it will raise a :class:`TimeoutError`) or until new
data is available::

  input.wait()

The method :meth:`Connector.wait()` has the same behavior as :meth:`Input.wait()`,
but will block until data is available on any of the :class:`Input` objects within
the :class:`Connector`::

  connector.wait()

Accessing the data samples
~~~~~~~~~~~~~~~~~~~~~~~~~~

After calling :meth:`Input.read()` or :meth:`Input.take()`, :attr:`Input.samples`
contains the data samples:

.. testcode::

   for sample in input.samples:
      if sample.valid_data:
         print(sample.get_dictionary())

:meth:`SampleIterator.get_dictionary()` retrieves all the fields of a sample.

Unless the :attr:`Samples.valid_data_iter` is used, it is necessary to check if the
sample contains valid data before accessing the fields. The only exception to this
rule is if the ``instance_state`` of the sample is ``"NOT_ALIVE_DISPOSED"``.
See :ref:`Accessing key values of disposed samples` for more information on this use
case.

If you don't need to access the meta-data (see :ref:`Accessing sample meta-data`),
the simplest way to access the data is to use :attr:`Samples.valid_data_iter` to skip
samples with invalid data:

.. testcode::

   for sample in input.samples.valid_data_iter:
      print(sample.get_dictionary())

It is also possible to access an individual sample:

.. testcode::

   if input.samples.length > 0:
      if input.samples[0].valid_data:
         print(input.samples[0].get_dictionary())

.. warning::
   All the methods described in this section return iterators to samples.
   Calling read/take again invalidates all iterators currently in
   use. For that reason, it is not recommended to store any iterator.

``get_dictionary()`` can receive a ``field_name`` to only return the fields of a
complex member. In addition to ``get_dictionary()``, you can get the values of
specific primitive fields using :meth:`SampleIterator.get_number()`,
:meth:`SampleIterator.get_boolean()` and :meth:`SampleIterator.get_string()`.
For example:

.. testcode::

   for sample in input.samples.valid_data_iter:
      x = sample.get_number("x") # or just sample["x"]
      y = sample.get_number("y")
      size = sample.get_number("shapesize")
      color = sample.get_string("color") # or just sample["color"]

See more information and examples in :ref:`Accessing the data`.

Accessing sample meta-data
~~~~~~~~~~~~~~~~~~~~~~~~~~

Every sample contains an associated *SampleInfo* with meta-information about
the sample:

.. testcode::

   for sample in input.samples:
      source_timestamp = sample.info["source_timestamp"]


See :meth:`SampleIterator.info` for the list of available meta-data fields.


*Connext DDS* can produce samples with invalid data, which contain meta-data only.
For more information about this, see `Valid Data Flag 
<https://community.rti.com/static/documentation/connext-dds/6.1.1/doc/manuals/connext_dds_professional/users_manual/index.htm#users_manual/AccessingManagingInstances.htm#Valid>`__
in the *RTI Connext DDS Core Libraries User's Manual*.
These samples indicate a change in the instance state. Samples with invalid data
still provide the following information:

* The :class:`SampleInfo`
* When an instance is disposed (``sample.info.get('instance_state')`` is
  ``'NOT_ALIVE_DISPOSED'``), the sample data contains the value of the key that
  has been disposed. You can access the key fields only. See
  :ref:`Accessing key values of disposed samples`.
  

Matching with a publication
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the method :meth:`Input.wait_for_publications()` to detect when a compatible
DDS publication is matched or stops matching. It returns the change in the number of
matched publications since the last time it was called::

   change_in_matches = input.wait_for_publications()

For example, if a new compatible publication is discovered within the specified
``timeout``, the function returns 1; if a previously matching publication
no longer matches, it returns -1.

You can obtain information about the existing matched publications with
:attr:`Input.matched_publication`:

.. testcode::

   matched_pubs = input.matched_publications
   for pub_info in matched_pubs:
      pub_name = pub_info['name']

Class reference: Input, Samples, SampleIterator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Input class
^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.Input
   :members:

Samples class
^^^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.Samples
   :members:

SampleIterator class
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.SampleIterator
   :members:


ValidSampleIterator class
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.ValidSampleIterator
   :members: