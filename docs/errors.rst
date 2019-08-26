Error Handling
===============

When an error is from the any of the internal RTI Connext DDS APIs, the Python
Connector will raise an ``rticonnextdds_connector.Error`` excpetion.

When an error is detected, the last error message from the middleware is obtained
and printed to stdout.

Other errors may be raised as ``TypeError``, ``ValueError``, ``AttributeError`` or other
built-in Python exceptions.
