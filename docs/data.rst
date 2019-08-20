Accessing the data
==================

.. py:currentmodule:: rticonnextdds_connector

.. testsetup:: *

   import rticonnextdds_connector as rti, time
   connector = rti.Connector("MyParticipantLibrary::DataAccessTest", "../test/xml/TestConnector.xml")
   output = connector.get_output("TestPublisher::TestWriter")
   input = connector.get_input("TestSubscriber::TestReader")
   output.instance.set_number("my_int_sequence[10]", 10)
   output.instance.set_number("my_point_sequence[10].x", 10)
   output.instance.set_number("my_optional_long", 10)
   output.instance.set_number("my_optional_point.x", 10)
   output.write()
   input.wait(2000)
   input.take()

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
            <member name="my_enum" type="nonBasic"  nonBasicTypeName= "Color" default="GREEN"/>
            <member name="my_boolean" type="boolean" />
            <member name="my_point" type="nonBasic"  nonBasicTypeName= "Point"/>
            <member name="my_union" type="nonBasic"  nonBasicTypeName= "MyUnion"/>
            <member name="my_int_sequence" sequenceMaxLength="10" type="int32"/>
            <member name="my_point_sequence" sequenceMaxLength="10" type="nonBasic"  nonBasicTypeName= "Point"/>
            <member name="my_point_array" type="nonBasic"  nonBasicTypeName= "Point" arrayDimensions="3"/>
            <member name="my_optional_point" type="nonBasic"  nonBasicTypeName= "Point" optional="true"/>
            <member name="my_optional_long" type="int32" optional="true"/>
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
        boolean my_boolean;
        string<512> my_string;
        Point my_point;
        MyUnion my_union;
        sequence<long, 10> my_int_sequence;
        sequence<Point, 10> my_point_sequence;
        Point my_point_array[3];
        @optional Point my_optional_point;
        @optional long my_optional_long;
    };

Note that you can get the XML definition of an IDL file with *rtiddsgen -convertToXml MyType.idl*.

We will refer to an ``Output`` named ``output`` and
``Input`` named ``input`` such that ``input.sample_count > 0``.

Using dictionaries vs accessing individual members
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In an Input or an Output you can access the data all at once, using a dictionary,
or member by member. Using a dictionary is usually more efficient if you intend
to access most or all of the data members of a large type.

In an Output, :meth:`Instance.set_dictionary` receives a dictionary with all or
some of the Output type members, and in an Input, :meth:`SampleIterator.get_dictionary`
retrieves all the members.

It is also possible to provide a ``member_name`` to :meth:`SampleIterator.get_dictionary` to obtain
a dictionary containing the fields of that nested member only.

On the other hand the methods described in the following section receive a
``field_name`` argument to get or set a specific member.

Accessing basic members (numbers, strings and booleans)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To set a field in an :class:`Output`, use the appropriate setter.

To set any numeric type, including enumerations:

.. testcode::

    output.instance.set_number("my_long", 2)
    output.instance.set_number("my_double", 2.14)
    output.instance.set_number("my_enum", 2)

To set booleans:

.. testcode::

    output.instance.set_boolean("my_boolean", True)

To set strings:

.. testcode::

    output.instance.set_string("my_string", "Hello, World!")


As an alternative to the previous setters, the special method ``__setitem__``
can be used as follows:

.. testcode::

    output.instance["my_double"] = 2.14
    output.instance["my_boolean"] = True
    output.instance["my_string"] = "Hello, World!"

In all cases, the type of the assigned value must be consistent with the type
of the field as defined in the configuration file.

Similarly, to get a field in a :class:`Input` sample, use the appropriate
getter: :meth:`SampleIterator.get_number()`, :meth:`SampleIterator.get_boolean()`,
:meth:`SampleIterator.get_string()`, or ``__getitem__``. ``get_string`` also works
with numeric fields, returning the number as a string. For example:

.. testcode::

    for sample in input.valid_data_iterator:
        value = sample.get_number("my_double")
        value = sample.get_boolean("my_boolean")
        value = sample.get_string("my_string")

        # or alternatively:
        value = sample["my_double"]
        value = sample["my_boolean"]
        value = sample["my_string"]

        # get number as string:
        value = sample.get_string("my_double")

Note that the typed getters and setters perform better than ``__setitem__``
and ``__getitem__`` in applications that write or read at high rates.
Also ``__setitem__`` or ``__getitem__`` shouldn't be used as an alternative
to ``get_dictionary`` or ``set_dictionary`` when the intention is to access
most of the fields of the sample (see previous section).


Accessing structs
^^^^^^^^^^^^^^^^^

To access a nested member, use ``.`` to identify the fully-qualified ``field_name``
and pass it to the corresponding setter or getter.

.. testcode::

    output.instance.set_number("my_point.x", 10)
    output.instance.set_number("my_point.y", 20)

    # alternatively:
    output.instance["my_point.x"] = 10
    output.instance["my_point.y"] = 20

It is possible to reset the value of a complex member back to its default:

.. testcode::

    output.instance.clear_member("my_point") # x and y are now 0

Structs in dictionaries are set as follows:

.. testcode::

    output.instance.set_dictionary({"my_point":{"x":10, "y":20}})

When an member of a struct is not set, it retains its previous value. If we run
the following code after the previous call to ``set_dictionary``:

.. testcode::

    output.instance.set_dictionary({"my_point":{"y":200}})

The value of ``my_point`` is now ``{"x":10, "y":200}``

It is possible to obtain the dictionary of a nested struct using
`SampleIterator.get_dictionary("member_name")`:

.. testcode::

   for sample in input.valid_data_iterator:
      point = sample.get_dictionary("my_point")

``member_name`` must be one of the following types: array, sequence,
struct, value or union. If not, the call to get_dictionary will fail:

.. testcode::

   # for sample in input.valid_data_iterator:
      # long = sample.get_dictionary("my_long") # ERROR, the_long is a basic type

Accessing arrays and sequences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``"field_name[index]"`` to access an element of a sequence or array,
where ``0 <= index < length``:

.. testcode::

    value = input[0].get_number("my_int_sequence[1]")
    value = input[0].get_number("my_point_sequence[2].y")

Another option is to use ``SampleIterator.get_dictionary("field_name")`` to obtain
a dictionary containing all of the elements of the array or sequence with name ``field_name``:

.. testcode::

    for sample in input.valid_data_iterator:
        the_point_sequence = sample.get_dictionary("my_point_sequence")

It is also possible to supply ``member_name`` as an element of an array (if the
type of the array is complex):

.. testcode::

   for sample in input.valid_data_iterator:
      point_element = sample.get_dictionary("my_point_sequence[1]")

In an Output, sequences are automatically resized:

.. testcode::

    output.instance.set_number("my_int_sequence[5]", 10) # length is now 6
    output.instance.set_number("my_int_sequence[4]", 9) # length still 6

You can clear a sequence:

.. testcode::

    output.instance.clear_member("my_int_sequence") # my_int_sequence is now empty

To get the length of a sequence in an Input sample:

.. testcode::

    length = input[0].get_number("my_int_sequence#")


In dictionaries, sequences and arrays are represented as lists. For example:

.. testcode::

    output.instance.set_dictionary({
        "my_int_sequence":[1, 2],
        "my_point_sequence":[{"x":1, "y":1}, {"x":2, "y":2}]})

Arrays have a constant length that can't be changed. When you don't set all the elements
of an array, the remaining elements retain their previous value. However, sequences
are always overwritten. See the following example:

.. testcode::

    output.instance.set_dictionary({
        "my_point_sequence":[{"x":1, "y":1}, {"x":2, "y":2}],
        "my_point_array":[{"x":1, "y":1}, {"x":2, "y":2}, {"x":3, "y":3}]})

    output.instance.set_dictionary({
        "my_point_sequence":[{"x":100}],
        "my_point_array":[{"x":100}, {"y":200}]})

After the second call to ``set_dictionary``, the contents of ``my_point_sequence``
are ``[{"x":100, "y":0}]``, but the contents of ``my_point_array`` are:
``[{"x":100, "y":1}, {"x":2, "y":200}, {"x":3, "y":3}]``.

Accessing optional members
^^^^^^^^^^^^^^^^^^^^^^^^^^

A optional member is a member that applications can decide to send or not as
part of every published sample. Therefore, optional members may have a value or not.
They are accessed the same way as non-optional members, except that ``None`` is
a possible value.

On an Input, any of the getters may return ``None`` if the field is optional:

.. testcode::

    if input[0].get_number("my_optional_long") is None:
        print("my_optional_long not set")

    if input[0].get_number("my_optional_point.x") is None:
        print("my_optional_point not set")

:meth:`SampleIterator.get_dictionary()` returns a dictionary that doesn't include unset
optional members.

To set an optional member on an Output:

.. testcode::

    output.instance.set_number("my_optional_long", 10)

If the type of the optional member is not primitive, when any of its members is
first set, the rest are initialized to their default values:

.. testcode::

    output.instance.set_number("my_optional_point.x", 10)

If ``my_optional_point`` was not previously set, the previous code also sets
``y`` to 0.

There are several ways to reset an optional member. If the type is primitive:

.. testcode::

    output.instance.set_number("my_optional_long", None) # Option 1
    output.instance.clear_member("my_optional_long") # Option 2

If the member type is complex:

.. testcode::

    output.instance.clear_member("my_optional_point")

Note that :meth:`Instance.set_dictionary()` doesn't clear those members that are
not specified; their value remains. For example:

.. testcode::

    output.instance.set_number("my_optional_long", 5)
    output.instance.set_dictionary({'my_double': 3.3, 'my_long': 4}) # my_optional_long is still 5

To clear a member, set it to ``None`` explicitly::

    output.instance.set_dictionary({'my_double': 3.3, 'my_long': 4, 'my_optional_long': None})


For more information about optional members in DDS, see the *Getting Started Guide
Addendum for Extensible Types*,
`section 3.2 Optional Members <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/getting_started_extras/html_files/RTI_ConnextDDS_CoreLibraries_GettingStarted_ExtensibleAddendum/index.htm#ExtensibleTypesAddendum/Optional_Members.htm#3.2_Optional_Members%3FTocPath%3D3.%2520Type%2520System%2520Enhancements%7C3.2%2520Optional%2520Members%7C_____0>`__. 

Accessing unions
^^^^^^^^^^^^^^^^

In an Output the union member is automatically selected when you set it:

.. testcode::

    output.instance.set_number("my_union.point.x", 10)

You can change it later:

.. testcode::

    output.instance.set_number("my_union.my_long", 10)

In an Input, you can obtain the selected member as a string::

    if input[0].get_string("my_union#") == "point":
        value = input[0].get_number("my_union.point")
