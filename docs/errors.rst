Error Handling
===============

.. py:currentmodule:: rticonnextdds_connector

*Connector* reports internal errors in *RTI Connext DDS* by raising an
:class:`rticonnextdds_connector.Error`. This exception may contain a description
of the error.

A subclass, :class:`TimeoutError`, indicates that an operation that can block
has timed out.

Other errors may be raised as ``TypeError``, ``ValueError``, ``AttributeError``,
or other built-in Python exceptions.

Class reference: Error, TimeoutError
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Error class
^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.Error
   :members:


TimeoutError class
^^^^^^^^^^^^^^^^^^

.. autoclass:: rticonnextdds_connector.TimeoutError
   :members:
