.. include:: vars.rst

.. _section-release-notes:

Release Notes
=============

Supported Platforms
--------------------

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

Version 2.0.0 (TODO Numebring)
------------------------------

What's New in 2.0.0
~~~~~~~~~~~~~~~~~~~

What's Fixed in 2.0.0
~~~~~~~~~~~~~~~~~~~~~

CON-163: Creating two instances of Connector resulted in a license error 
########################################################################

Under some circumstances, it was not possible to create two Connector objects.
The creation of the second Connector object failed due to a license error.
This issue affected all of the Connector APIs (Python, JavaScript).
This issue has been fixed.

CON-214: Creating a Connector instance with a participant_qos tag in the XML may have resulted in a license error
#################################################################################################################

In some cases, if the XML configuration file of RTI Connector contained a
`<participant_qos>` tag within the definition of the DomainParticipant,
the creation of the Connector would fail with a "license not found" error.
This problem has been resolved.

Version 1.0.0
-------------

1.0.0 is the first official release of *RTI Connector for Python* as well as
`RTI Connector for JavaScript <https://community.rti.com/static/documentation/connector/1.0.0/api/javascript/index.html>`__.

If you had access to previous experimental releases, this release makes the product
more robust, modifies most of APIs and adds new functionality. However the old 
APIs have been preserved for backward compatibility as much as possible.

*RTI Connector* 1.0.0 is built on `RTI Connext DDS 6.0.1 <https://community.rti.com/documentation/rti-connext-dds-601>`__.

