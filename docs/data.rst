Accessing the data
==================

.. py:currentmodule:: rticonnextdds_connector

.. testsetup:: *

   import rticonnextdds_connector as rti, time
   connector = rti.Connector("MyParticipantLibrary::DataAccessTest", "../test/xml/TestConnector.xml")
   output = connector.get_output("TestPublisher::TestWriter")
   input = connector.get_input("TestSubscriber::TestReader")
   output.instance.set_number("my_int_sequence[9]", 10)
   output.instance.set_number("my_point_sequence[9].x", 10)
   output.instance.set_number("my_optional_long", 10)
   output.instance.set_number("my_optional_point.x", 10)
   output.write()
   input.wait(2000)
   input.take()

The types you use to write or read data may included nested structs, sequences and
arrays of primitive types or structs, etc.

These types are defined in XML, as described in :ref:`Data Types`.

To access the data, :class:`Instance` and :class:`SampleIterator` provide
setters and getters that expect a ``fieldName`` string. This section describes
the format of this string.

We will use the following type definition of MyType:

.. code-block:: xml

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

The above XML corresponds to the following IDL definition:

.. code-block:: idl

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

.. hint::
    You can get the XML definition of an IDL file with ``rtiddsgen -convertToXml MyType.idl``.

We will refer to an Output named ``output`` and
an Input named ``input`` such that ``input.samples.length > 0``.

Using dictionaries vs. accessing individual members
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For an Input or Output, you can access the data all at once by using a dictionary,
or member by member. Using a dictionary is usually more efficient if you intend
to access most or all of the data members of a large type.

In an Output, :meth:`Instance.set_dictionary` receives a dictionary with all or
some of the Output type members. In an Input, :meth:`SampleIterator.get_dictionary`
retrieves all the members.

It is also possible to provide a ``member_name`` to
:meth:`SampleIterator.get_dictionary` to obtain
a dictionary that only contains the fields of that nested member.

The methods described in the following section receive a
``field_name`` argument to get or set a specific member.

Accessing basic members (numbers, strings and booleans)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To set a field in an :class:`Output`, use the appropriate setter.

To set any numeric type, including enumerations:

.. testcode::

    output.instance.set_number("my_long", 2)
    output.instance.set_number("my_double", 2.14)
    output.instance.set_number("my_enum", 2)

.. warning::
    The range of values for a numeric field is determined by the type
    used to define that field in the configuration file. However, ``set_number`` and
    ``get_number`` can't handle 64-bit integers (*int64* and *uint64*)
    whose absolute values are larger than 2^53. This is a *Connector* limitation
    due to the use of *double* as an intermediate representation.

    When ``set_number`` or ``get_number`` detect this situation, they will raise
    an :class:`Error`. ``get_dictionary`` and ``set_dictionary`` do not have this
    limitation and can handle any 64-bit integer.
    An ``Instance``'s ``__setitem__`` method doesn't have
    this limitation either, but ``SampleIterator``'s ``__getitem__`` does.

To set booleans:

.. testcode::

    output.instance.set_boolean("my_boolean", True)

To set strings:

.. testcode::

    output.instance.set_string("my_string", "Hello, World!")


As an alternative to the setters mentioned above, you can use the special
method ``__setitem__`` as follows:

.. testcode::

    output.instance["my_double"] = 2.14
    output.instance["my_boolean"] = True
    output.instance["my_string"] = "Hello, World!"

In all cases, the type of the assigned value must be consistent with the type
of the field, as defined in the configuration file.

Similarly, to get a field in an :class:`Input` sample, use the appropriate
getter: :meth:`SampleIterator.get_number()`, :meth:`SampleIterator.get_boolean()`,
:meth:`SampleIterator.get_string()`, or ``__getitem__``. ``get_string`` also works
with numeric fields, returning the number as a string. For example:

.. testcode::

    for sample in input.samples.valid_data_iter:
        value = sample.get_number("my_double")
        value = sample.get_boolean("my_boolean")
        value = sample.get_string("my_string")

        # or alternatively:
        value = sample["my_double"]
        value = sample["my_boolean"]
        value = sample["my_string"]

        # get number as string:
        value = sample.get_string("my_double")


.. note::
    The typed getters and setters perform better than ``__setitem__``
    and ``__getitem__`` in applications that write or read at high rates.
    We also recommend ``get_dictionary`` or ``set_dictionary`` over ``__setitem__``
    or ``__getitem__`` when accessing all or most of the fields of a sample
    (see previous section).

.. note::
    If a field ``my_string``, defined as a string in the configuration file,
    contains a value that can be interpreted as a number, ``sample["my_string"]``
    returns a number, not a string.

Accessing structs
^^^^^^^^^^^^^^^^^

To access a nested member, use ``.`` to identify the fully qualified ``field_name``
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

It is possible to obtain the dictionary of a nested struct:

.. testcode::

   for sample in input.samples.valid_data_iter:
      point = sample.get_dictionary("my_point")

``member_name`` must be one of the following types: array, sequence,
struct, value or union. If not, the call to ``get_dictionary()`` will fail::

   for sample in input.samples.valid_data_iter:
      try:
        long = sample.get_dictionary("my_long")
      except rti.Error:
        print("ERROR, my_long is a basic type")

It is also possible to obtain the dictionary of a struct using the ``__getitem__``
operator:

.. testcode::

    for sample in input.samples.valid_data_iter:
        point = sample["my_point"]
        # point is a dict

The same limitations described in
:ref:`Accessing basic members (numbers, strings and booleans)`
about using ``__getitem__`` apply here.

Accessing arrays and sequences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``"field_name[index]"`` to access an element of a sequence or array,
where ``0 <= index < length``:

.. testcode::

    value = input.samples[0].get_number("my_int_sequence[1]")
    value = input.samples[0].get_number("my_point_sequence[2].y")

You can get the length of a sequence:

.. testcode::

    length = input.samples[0].get_number("my_int_sequence#")

Another option is to use ``SampleIterator.get_dictionary("field_name")`` to obtain
a dictionary containing all of the elements of the array or sequence with name ``field_name``:

.. testcode::

    for sample in input.samples.valid_data_iter:
        point_sequence = sample.get_dictionary("my_point_sequence") # or sample["my_point_sequence"]
        # point_sequence is a list

You can also get a specific element as a dictionary (if the element type is complex):

.. testcode::

   for sample in input.samples.valid_data_iter:
      point_element = sample.get_dictionary("my_point_sequence[1]")

In an Output, sequences are automatically resized:

.. testcode::

    output.instance.set_number("my_int_sequence[5]", 10) # length is now 6
    output.instance.set_number("my_int_sequence[4]", 9) # length still 6

To clear a sequence:

.. testcode::

    output.instance.clear_member("my_int_sequence") # my_int_sequence is now empty

In dictionaries, sequences and arrays are represented as lists. For example:

.. testcode::

    output.instance.set_dictionary({
        "my_int_sequence":[1, 2],
        "my_point_sequence":[{"x":1, "y":1}, {"x":2, "y":2}]})

Arrays have a constant length that can't be changed. If you don't set all the elements
of an array, the remaining elements retain their previous value. However, sequences
are always overwritten. See the following example:

.. testcode::

    output.instance.set_dictionary({
        "my_point_sequence":[{"x":1, "y":1}, {"x":2, "y":2}],
        "my_point_array":[{"x":1, "y":1}, {"x":2, "y":2}, {"x":3, "y":3}]})

    output.instance.set_dictionary({
        "my_point_sequence":[{"x":100}],
        "my_point_array":[{"x":100}, {"y":200}]})

After the second call to ``set_dictionary()``, the contents of ``my_point_sequence``
are ``[{"x":100, "y":0}]``, but the contents of ``my_point_array`` are
``[{"x":100, "y":1}, {"x":2, "y":200}, {"x":3, "y":3}]``.

Accessing optional members
^^^^^^^^^^^^^^^^^^^^^^^^^^

An optional member is a member that applications can decide to send or not as
part of every published sample. Therefore, optional members may or may not have
a value. They are accessed the same way as non-optional members, except that
``None`` is a possible value.

On an Input, any of the getters may return ``None`` if the field is optional:

.. testcode::

    if input.samples[0].get_number("my_optional_long") is None:
        print("my_optional_long not set")

    if input.samples[0].get_number("my_optional_point.x") is None:
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
`Optional Members <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds_professional/extensible_types_guide/index.htm#extensible_types/Optional_Members.htm>`__.

Accessing unions
^^^^^^^^^^^^^^^^

In an Output, the union member is automatically selected when you set it:

.. testcode::

    output.instance.set_number("my_union.point.x", 10)

You can change it later:

.. testcode::

    output.instance.set_number("my_union.my_long", 10)

In an Input, you can obtain the selected member as a string:

.. testcode::

    if input.samples[0].get_string("my_union#") == "point":
        value = input.samples[0].get_number("my_union.point.x")

The ``__getitem__`` operator can be used to obtain unions:

.. testcode::

    for sample in input.samples.valid_data_iter:
        union = sample["my_union"]
        # union is a dict

The type returned by the operator is a dict for unions.

The same limitations described in
:ref:`Accessing basic members (numbers, strings and booleans)`
about using ``__getitem__`` apply here.

Accessing key values of disposed samples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using :meth:`Output.write`, an :class:`Output` can write data, or dispose or 
unregister an instance.
Depending on which of these operations is performed, the ``instance_state`` of the
received sample will be ``'ALIVE'``, ``'NOT_ALIVE_NO_WRITERS'`` or ``'NOT_ALIVE_DISPOSED'``.
If the instance was disposed, this ``instance_state`` will be ``'NOT_ALIVE_DISPOSED'``.
In this state, it is possible to access the key fields of the instance that was disposed.

.. note::
    :attr:`SampleInfo.valid_data` will be false when the :attr:`SampleInfo.instance_state`
    is ``'NOT_ALIVE_DISPOSED'``. In this situation it's possible to access the
    key fields in the received sample.

The key fields can be accessed as follows:

.. testcode::

    # The output and input are using the following type:
    # struct ShapeType {
    #     @key string<128> color;
    #     long x;
    #     long y;
    #     long shapesize;
    # }

    output.instance["x"] = 4
    output.instance["color"] = "Green"
    # Assume that some data associated with this instance has already been sent
    output.write(action="dispose")
    input.wait()
    input.take()
    sample = input.samples[0]

    if sample.info["instance_state"] == "NOT_ALIVE_DISPOSED":
        # sample.info.get('valid_data') will be false in this situation
        # Only the key-fields should be accessed
        color = sample["color"] # 'Green'
        # The fields 'x','y' and 'shapesize' cannot be retrieved because they're
        # not part of the key
        # You can also call get_dictionary() to get all of the key fields.
        # Again, only the key fields returned within the dictionary should
        # be accessed.
        key_values = sample.get_dictionary() # { "color": "Green", "x": 0, "y": 0, "shapesize": 0 }

.. warning::
    When the sample has an instance state of ``'NOT_ALIVE_DISPOSED'`` only the
    key fields should be accessed.