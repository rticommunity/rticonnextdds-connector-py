Threading model
===============

.. py:currentmodule:: rticonnextdds_connector

.. testsetup:: *

   import rticonnextdds_connector as rti

Operations on the same :class:`Connector` instance or any contained :class:`Input`,
:class:`Output` are in general not protected for multi-threaded access. The only
exceptions are the following *wait* operations.

Thread-safe operations:
   * :meth:`Connector.wait` (wait for data on any ``Input``)
   * :meth:`Output.wait` (wait for acknowledgments)
   * :meth:`Output.wait_for_subscriptions`
   * :meth:`Input.wait` (wait for data on this ``Input``)
   * :meth:`Input.wait_for_publications`

These operations can block a thread while the same ``Connector`` is used in
a different thread.

.. note::

   Currently :meth:`Input.wait` and :meth:`Input.wait_for_publications` cannot
   be both called at the same time on the same ``Input`` instance.

.. note::

   :meth:`Output.write` can block the current thread under certain
   circumstances, but :meth:`Output.write` is not thread-safe.

All operations on **different** :class:`Connector` instances are thread-safe.

Applications can implement their own thread-safety mechanism around a ``Connector``
instance. The following section provides an example.

Protecting calls to *Connector*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example shows how to use the Python ``threading`` package to
protect calls to the same :class:`Connector`:

.. testcode::

   import threading

   connector = rti.Connector("MyParticipantLibrary::MyParticipant", "ShapeExample.xml")
   lock = threading.RLock()

   def read_thread():
      with lock: # Protect access to methods on the same Connector
         input = connector.get_input("MySubscriber::MySquareReader")

      input.wait() # wait outside the lock

      with lock: # Take the lock again
         input.take();
         for sample in input.valid_data_iterator:
            print(sample.get_dictionary())

   def write_thread():
      with lock: # Protect access to methods on the same Connector
         output = connector.get_output("MyPublisher::MySquareWriter")
         output.instance['x'] = 10
         output.write()

   # Spawn read_thread and write_thread...

