Accessing the data
==================

.. py:currentmodule:: rticonnextdds_connector

.. testsetup:: *

   import rticonnextdds_connector as rti, time
   connector = rti.Connector("MyParticipantLibrary::DataAccessTest", "../test/xml/TestConnector.xml")
   output = connector.get_output("TestPublisher::TestWriter")
   input = connector.get_input("TestSubscriber::TestReader")
   output.write()
   time.sleep(10)

The types you use to write or read data may included nested structs, sequences and
arrays of primitive types or structs, etc.

These types are defined in the XML following the format of
`RTI's XML-Based Application Creation <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/xml_application_creation/html_files/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted/index.htm#XMLBasedAppCreation/UnderstandingPrototyper/XMLTagsConfigEntities.htm%3FTocPath%3D5.%2520Understanding%2520XML-Based%2520Application%2520Creation%7C5.5%2520XML%2520Tags%2520for%2520Configuring%2520Entities%7C_____0>`__.

To access the data, :class:`Instance` and :class:`SampleIterator` provide
setters and getters that expect a ``fieldName`` string. This section describes
the format of this string.

We will use the following type definition of MyType::

    <types>
        <enum name="Color">
            <enumerator name="RED"/>
            <enumerator name="GREEN"/>
            <enumerator name="BLUE"/>
        </enum>
        <struct name= "Point">
            <member name="x" type="int32"/>
            <member name="y" type="int32"/>
        </struct>
        <union name="MyUnion">
            <discriminator type="nonBasic" nonBasicTypeName="Color"/>
            <case>
              <caseDiscriminator value="RED"/>
              <member name="point" type="nonBasic"  nonBasicTypeName= "Point"/>
            </case>
            <case>
              <caseDiscriminator value="GREEN"/>
              <member name="my_long" type="int32"/>
            </case>
        </union>
        <struct name= "MyType">
            <member name="my_long" type="int32"/>
            <member name="my_double" type="float64"/>
            <member name="my_enum" type="nonBasic"  nonBasicTypeName= "Color"/>
            <member name="my_point" type="nonBasic"  nonBasicTypeName= "Point"/>
            <member name="my_union" type="nonBasic"  nonBasicTypeName= "MyUnion"/>
            <member name="my_int_sequence" sequenceMaxLength="10" type="int32"/>
            <member name="my_point_sequence" sequenceMaxLength="10" type="nonBasic"  nonBasicTypeName= "Point"/>
            <member name="my_array" type="nonBasic"  nonBasicTypeName= "Point" arrayDimensions="5"/>
            <member name="my_optional" type="nonBasic"  nonBasicTypeName= "Point" optional="true"/>
        </struct>
    </types>

Which corresponds to the following IDL definition::

    enum Color {
        RED,
        GREEN,
        BLUE
    };

    struct Point {
        long x;
        long y;
    };

    union MyUnion switch(Color) {
        case RED: Point point;
        case GREEN: string<512> my_string;
    };

    struct MyType {
        long my_long;
        double my_double;
        Color my_enum;
        string<512> my_string;
        Point my_point;
        MyUnion my_union;
        sequence<long, 10> my_int_sequence;
        sequence<Point, 10> my_point_sequence;
        Point my_array[5];
        @optional Point my_optional;
    };

Note that you can get the XML definition of an IDL file with *rtiddsgen -convertToXml MyType.idl*.

We will refer to an ``Output`` named ``output`` and
``Input`` named ``input`` such that ``input.sample_count > 0``.

Accessing nested members
^^^^^^^^^^^^^^^^^^^^^^^^

The "." notation allows accessing a nested field, for example:

.. testcode::

    output.instance.set_number("my_point.x", 10)

Accessing arrays and sequences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``[index]`` after a the name of a sequence or an array member to access an
element:

.. testcode::

    value = input[0].get_number("my_int_sequence[1]")
    value = input[0].get_number("my_point_sequence[2].y")

In an Output, sequences are automatically resized:

.. testcode::

    output.instance.set_number("my_int_sequence[1]", 10)

For a non-primitive sequence:

.. testcode::

    output.instance.set_number("my_sequence[1].x", 10)

To get the length of a sequence (Input only):

.. testcode::

    length = input[0].get_number("my_sequence#")

Accessing unions
^^^^^^^^^^^^^^^^

In an Output the union member is automatically selected when you set it:

.. testcode::

    output.instance.set_string("my_union.my_string", "hello")

You can change it later:

.. testcode::

    output.instance.set_number("my_union.my_long", 10)

In an Input, you can obtain the selected member::

    if input[0].get_string("my_union#") == "point":
        value = input[0].get_number("my_union.point")
