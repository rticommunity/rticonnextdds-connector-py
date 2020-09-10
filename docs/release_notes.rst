.. include:: vars.rst

.. _section-release-notes:

Release Notes
=============

Supported Platforms
~~~~~~~~~~~~~~~~~~~

*RTI Connector* works with Python 2.x and 3.x. It uses a native C library that
runs on most Windows, Linux and macOS platforms.

*RTI Connector* has been tested with Python 2.6+ and 3.6.8+ on the following systems:

    * Windows: Windows 7 and Windows 10
    * x86/x86_64 Linux: CentOS 6.1, 7.6, 8.0; Ubuntu 12.04, 18.04; SUSE 12, 15
    * ARM Linux (Raspberry Pi)
    * Mac: OS X 10.10.2, macOS 10.12.2, macOS 10.14

*RTI Connector* is supported in other languages in addition to Python, see the 
`main Connector
repository <https://github.com/rticommunity/rticonnextdds-connector>`__.

Version 1.1.0
~~~~~~~~~~~~~

What's New in 1.1.0
^^^^^^^^^^^^^^^^^^^

Sample state, instance state and view state can now be obtained in Connector
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

The SampleInfo class in Connector has been extended to provide access to the
sample state, view state and instance state fields. These new fields work the
same as the existing fields in the structure (in Connector for Python they are
the keys to the dictionary, in Connector for JavaScript they are the keys to the
JSON Object).

[RTI Issue ID CON-177]

Support for accessing the key values of disposed instances
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Support for disposing instances was added in RTI Connector version 1.0.0.
However, it was not possible to access the key values of the disposed instance.
This functionality is now available in the Python and JavaScript bindings.
When a disposed sample is received, the key values can be accessed.
The syntax for accessing these key values is the same as when the sample
contains valid data (i.e., using type-specific getters, or obtaining the entire
sample as an object). When the instance state is NOT_ALIVE_DISPOSED, only the
key values in the sample should be accessed.

[RTI Issue ID CON-188]

What's Fixed in 1.1.0
^^^^^^^^^^^^^^^^^^^^^

Support for loading multiple configuration files
""""""""""""""""""""""""""""""""""""""""""""""""

A Connector object now supports loading multiple files. This allows separating
the definition of types, QoS profiles, and domain participants into different
files:

.. testcode::

  c = rti.Connector("my_profiles.xml;my_types.xml;my_participants.xml", configName)

[RTI Issue ID CON-209]

Some larger integer values may have been corrupted by Connector's internal JSON parser
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

The internal JSON parser used in Connector failed to identify integer numbers
from double-precision floating-point numbers for certain values.
For example, if a number could not be represented as a 64-bit integer, the
parser may have incorrectly identified it as an integer, causing the value to
become corrupted. This problem has been resolved.

[RTI Issue ID CON-170]

Creating two instances of Connector resulted in a license error
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Under some circumstances, it was not possible to create two Connector objects.
The creation of the second Connector object failed due to a license error.
This issue affected all of the Connector APIs (Python, JavaScript).
This issue has been fixed.

[RTI Issue ID CON-163]

Creating a Connector instance with a participant_qos tag in the XML may have resulted in a license error
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

In some cases, if the XML configuration file of RTI Connector contained a
`<participant_qos>` tag within the definition of the DomainParticipant,
the creation of the Connector would fail with a "license not found" error.
This problem has been resolved.

[RTI Issue ID CON-214]

Version 1.0.0
~~~~~~~~~~~~~

1.0.0 is the first official release of *RTI Connector for Python* as well as
`RTI Connector for JavaScript <https://community.rti.com/static/documentation/connector/1.0.0/api/javascript/index.html>`__.

If you had access to previous experimental releases, this release makes the product
more robust, modifies most of APIs and adds new functionality. However the old 
APIs have been preserved for backward compatibility as much as possible.

*RTI Connector* 1.0.0 is built on `RTI Connext DDS 6.0.1 <https://community.rti.com/documentation/rti-connext-dds-601>`__.
