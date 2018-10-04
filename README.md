
rticonnextdds-connector: Python
========

### RTI Connector for Connext DDS
*RTI Connector* for Connext DDS is a quick and easy way to access the power and
functionality of [RTI Connext DDS](http://www.rti.com/products/index.html).
It is based on [XML Application Creation](https://community.rti.com/static/documentation/connext-dds/5.3.1/doc/manuals/connext_dds/xml_application_creation/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted.pdf) and Dynamic Data.

### Language Support

This repository is specific to Python, for other languages (python, lua, C) refer to the [main repository of connector.](https://github.com/rticommunity/rticonnextdds-connector)

We use ctypes to call our native functions; everything is hidden in a nice Python wrapper. We tested our Python implementation with both Python 2.7.14 and Python 3.6.3.

### Platform support
We are building our library for a few architectures only. Check them out [here](https://github.com/rticommunity/rticonnextdds-connector/tree/master/lib). If you need another architecture, please contact your RTI account manager or sales@rti.com.

If you want to check the version of the libraries, run the following command:

``` bash
strings librtiddsconnector.dylib | grep BUILD
```

### Threading model
The *Connector* Native API does not yet implement any mechanism for thread safety.
For now, the responsibility of protecting calls to the *Connector* is left to you. (In the future we may add thread safety in the native layer.)
In Python, you will have to protect the calls to the Connector if you are using different threads. For an example, see [Protecting calls to the Connector library](https://github.com/rticommunity/rticonnextdds-connector-py#protecting-calls-to-the-connector-library).

### Support
This is an experimental RTI product. As such, we offer support through the [RTI Community forum](https://community.rti.com/forums/technical-questions).

### Getting started with Python
Be sure you have Python. Then use pip to install the *Connector*:

``` bash
$ pip install rticonnextdds_connector
```

You can also clone the repository:

``` bash
$ git clone --recursive https://github.com/rticommunity/rticonnextdds-connector-py.git
```

### Available examples
You can find several sets of examples in this directory: [examples/python](examples/python)

 * **simple**: shows how to write samples and how to read/take.
 * **mixed**: various examples

### Protecting calls to the *Connector* library
As we explained above, you are responsible for protecting calls to *Connector*. There are many options in Python to do so; one is to use the ```threading``` package:

```py
...
...
import threading
sem = threading.Semaphore();
...
...
#acquire the semaphore
sem.acquire(True);
#call to connector APissem.acquire(True);
input.take();
numOfSamples = input.samples.getLength();
...
...
#release the semaphore
sem.release();
...
...

```

For more information on the threading Python packages, see the Python documentation [here](https://docs.python.org/2/library/threading.html).

### API overview
#### require the *Connector* library
If you want to use the `rticonnextdds_connector`, you have to import it:

```py
import rticonnextdds_connector as rti
```

#### instantiate a new *Connector*
To create a new *Connector* you have to pass an XML file and a configuration name. For more information on
the XML format, see the [XML App Creation guide](https://community.rti.com/static/documentation/connext-dds/5.3.1/doc/manuals/connext_dds/xml_application_creation/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted.pdf) or
have a look at the [ShapeExample.xml](examples/python/ShapeExample.xml) file included in this examples directory.  

```py
connector = rti.Connector("MyParticipantLibrary::Zero","./ShapeExample.xml");
```
#### delete a *Connector*
To destroy all the DDS entities that belong to a *Connector* previously created, call the ```delete``` function.

```py
connector = rti.Connector("MyParticipantLibrary::Zero","./ShapeExample.xml");
...
...
connector.delete();
```

#### write a sample
To write a sample, first get a reference to the output port:

```py
output = connector.getOutput("MyPublisher::MySquareWriter")
```

Then set the instance's fields:

```py
output.instance.setNumber("x", 1);
output.instance.setNumber("y", 2);
output.instance.setNumber("shapesize", 30);
output.instance.setString("color", "BLUE");
```

Then write:

```py
output.write();
```

#### set the instance's fields:
The content of an instance can be set by using a dictionary that matches the original type, or field by field.

* **Using a dictionary**:

```py
#assuming that sample is a dictionary containing
#an object of the same type of the output.instance:

output.instance.setDictionary(sample);
```

 * **Field by field**:

```py
output.instance.setNumber("y", 2);
```

The APIs to set an instance field by field are three: `setNumber(fieldName, number);` `setBoolean(fieldName, boolean);` and `setString(fieldName, string);`.

Nested fields can be accessed with the dot notation: `"x.y.z"`. Arrays or sequences can be accessed with square brakets: `"x.y[1].z"`. For more information on how to access
fields, see Section 6.4 *Data Access API* of the
[RTI Prototyper Getting Started Guide](https://community.rti.com/static/documentation/connext-dds/5.3.1/doc/manuals/connext_dds/prototyper/RTI_ConnextDDS_CoreLibraries_Prototyper_GettingStarted.pdf).


#### read/take data
To read/take samples, first get a reference to the input port:

```py
input = connector.getInput("MySubscriber::MySquareReader");
```

Then call the `read()` or `take()` API:

```py
input.read();
```

 or

```pu
 input.take();
```

The read/take operation can return multiple samples. So, we have to iterate on an array:

```py
    input.take();
    numOfSamples = input.samples.getLength();
    for j in range (1, numOfSamples+1):
        if input.infos.isValid(j):
            x = input.samples.getNumber(j, "x");
            y = input.samples.getNumber(j, "y");
            size = input.samples.getNumber(j, "shapesize");
            color = input.samples.getString(j, "color");
            toPrint = "Received x: " + repr(x) + " y: " + repr(y) + " size: " + repr(size) + " color: " + repr(color);
            print(toPrint);
}
```

#### access sample fields after a read/take
A `read()` or `take()` operation can return multiple samples. They are stored in an array. Every time you try to access a specific sample, you have to specify an index (j in the example below).

You can access the data by getting a copy in a dictionary object, or you can access each field individually:

 * **Using a dictionary**:

```py
 numOfSamples = input.samples.getLength();
 for j in range (1, numOfSamples+1):
     if input.infos.isValid(j):
         sample = input.samples.getDictionary(j);
         #print the whole sample
         print(sample);
         #or print a single element
         print(sample['x']);
 }
```

 * **Field by field**:

```py
 numOfSamples = input.samples.getLength();
 for j in range (1, numOfSamples+1):
     if input.infos.isValid(j):
         x = input.samples.getNumber(j, "x");
         y = input.samples.getNumber(j, "y");
         size = input.samples.getNumber(j, "shapesize");
         color = input.samples.getString(j, "color");
         toPrint = "Received x: " + repr(x) + " y: " + repr(y) + " size: " + repr(size) + " color: " + repr(color);
         print(toPrint);
 }
```

The APIs to access each field individually are three: `getNumber(indexm fieldName);` `getBoolean(index, fieldName);` and `getString(index, fieldName);`.

### License
With the sole exception of the contents of the "examples" subdirectory, all use of this product is subject to the RTI Software License Agreement included at the top level of this repository. Files within the "examples" subdirectory are licensed as marked within the file.

This software is an experimental ("pre-production") product. The Software is provided "as is," with no warranty of any type, including any warranty for fitness for any purpose. RTI is under no obligation to maintain or support the software. RTI shall not be liable for any incidental or consequential damages arising out of the use or inability to use the software.
