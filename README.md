
rticonnextdds-connector: Python
========

(return to [rticonnextdds-connector](https://github.com/rticommunity/rticonnextdds-connector))

### RTI Connector for Connext DDS
*RTI Connector* for Connext DDS is a quick and easy way to access the power and
functionality of [RTI Connext DDS](http://www.rti.com/products/index.html).
It is based on [XML-Based Application Creation](https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/xml_application_creation/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted.pdf) and Dynamic Data.


____
**Warning**: The Python *Connector* uses 0-based indexing for sequences since
v0.4.1. Previously sequences started at index 1. See *read/take data* more more
information.
____

### Language Support

This repository is specific to Python. For other languages (lua, C, etc.), refer to the [main *Connector* repository](https://github.com/rticommunity/rticonnextdds-connector).

We use ctypes to call our native functions; these details are hidden in a Python wrapper. RTI tested its Python implementation with both Python 2.7.14 and Python 3.6.3.

### Platform support
Python *Connector* builds its library for [select architectures](https://github.com/rticommunity/rticonnextdds-connector/tree/master/lib).
 If you need another architecture, please contact your RTI account manager or sales@rti.com.

 ### Testing
 We tested on:
 * For MacOS 64 bit : Darwin 18  clang 10
 * For Windows 64 bit: Windows 10 64 bit VS2015
 * For Windows 32 bit: Windows 7 32 bit VS2017
 * For Linux 64 bit: CentOS 6.5 gcc 4.8.2
 * For Linux 32 bit: Ubuntu 16.04 gcc 5.4.0
 * For ARM: Yocto linux 2.0.3 gcc 5.2.0

### Version of Connext
To check the version of the libraries, run the following command. For example:

``` bash
strings librtiddsconnector.dylib | grep BUILD
```

### Getting started with Python
Make sure you have Python installed. Then use pip to install the *Connector*:

``` bash
$ pip install rticonnextdds_connector
```

You can also clone the repository:

``` bash
$ git clone --recursive https://github.com/rticommunity/rticonnextdds-connector-py.git
```

### Available examples
You can find several examples in the [examples/python](examples/python) directory.
If you used pip to install, you will need to clone the repository to access
the examples as indicated above.

 * **simple**: shows how to write samples and how to read/take.
 * **mixed**: contains various examples.

### API Overview

The full documentation is available here (TODO: add link once available).

The following script shows how to publish a data sample on the *Square* topic,
as defined in [ShapeExample.xml](examples/python/ShapeExample.xml):

```py
import rticonnextdds_connector as rti

file_name = "ShapeExample.xml"
participant_name = "MyParticipantLibrary::MyParticipant"
with rti.open_connector(participant_name, file_name) as connector:
    output = connector.get_output("MyPublisher::MySquareWriter")

    # TODO: wait for match instead of slee
    sleep(2)

    output.instance.set_dictionary(
        {'x':30, 'y':100, 'shapesize':50, 'color':'ORANGE'})
    output.write()
```

The following script shows how to read data:

```py
import rticonnextdds_connector as rti

file_name = "ShapeExample.xml"
participant_name = "MyParticipantLibrary::MyParticipant"
with rti.open_connector(participant_name, file_name) as connector:

    dds_input = connector.get_input("MySubscriber::MySquareReader")
    # TODO: add synchronization
    for i in range(1, 500):
        dds_input.take()
        for sample in dds_input.valid_data_iterator:
            print(sample.dictionary)
```

### License
With the sole exception of the contents of the "examples" subdirectory, all use of this product is subject to the RTI Software License Agreement included at the top level of this repository. Files within the "examples" subdirectory are licensed as marked within the file.

This software is an experimental ("pre-production") product. The Software is provided "as is," with no warranty of any type, including any warranty for fitness for any purpose. RTI is under no obligation to maintain or support the software. RTI shall not be liable for any incidental or consequential damages arising out of the use or inability to use the software.

(return to [rticonnextdds-connector](https://github.com/rticommunity/rticonnextdds-connector))
