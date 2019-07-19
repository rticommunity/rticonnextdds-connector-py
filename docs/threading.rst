Threading model
===============

The *Connector* API does not implement any mechanism for
thread safety. Applications are responsible for protecting concurrent calls to
the Connector API. In Python, you will have to protect the calls to
*Connector* if you are using different threads.

The following section shows an example.

TODO: review, complete section

Protecting calls to *Connector*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example shows how to use the Python ``threading`` package to
protect calls to *Connector*, one of multiple ways to do so::

   import threading

   sem = threading.Semaphore()

   sem.acquire(True)

   # Use the Connector API
   input.take();
   sampleCount = input.samples.getLength()
   # ...

   sem.release()
   ...
   ...

