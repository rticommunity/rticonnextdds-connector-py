Threading model
===============

.. py:currentmodule:: rticonnextdds_connector

.. testsetup:: *

   import rticonnextdds_connector as rti

RTI Connector only allows the concurrent use of different :class:`Connector`
instances. Method calls to the same :class:`Connector` instance or any of its contained
entities are not thread safe, and the application is responsible to protect them
if they're used concurrently.

Protecting calls to *Connector*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example shows how to use the Python ``threading`` package to
protect calls to the same :class:`Connector`:

.. testcode::

   import threading

   connector = rti.Connector("MyParticipantLibrary::MyParticipant", "ShapeExample.xml")
   lock = threading.RLock()

   def read_thread():
      with lock: # Protect access to ALL methods on the same Connector
         input = connector.get_input("MySubscriber::MySquareReader")
         input.take();
         for sample in input.valid_data_iterator:
            print(sample.get_dictionary())

   def write_thread():
      with lock: # Protect access to ALL methods on the same Connector
         output = connector.get_output("MyPublisher::MySquareWriter")
         output.instance['x'] = 10
         output.write()

   # Spawn read_thread and write_thread...

