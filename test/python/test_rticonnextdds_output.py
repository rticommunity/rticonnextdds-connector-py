###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

import pytest,sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+ "/../../")
import rticonnextdds_connector as rti

class TestOutput:
  """
  This class tests the correct intantiation of
  :class:`rticonnextdds_connector.Output` object.
  """

  def test_invalid_DW(self,rtiConnectorFixture):
    """
    This test function ensures that a ``ValueError`` is raised if
    an incorrect DataWriter name is passed to the
    Output constructor.

    :param rtiConnectorFixture: :func:`conftest.rtiConnectorFixture`
    :type rtiConnectorFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    """
    invalid_DW = "InvalidDW"
    with pytest.raises(ValueError) as execinfo:
      op= rtiConnectorFixture.get_output(invalid_DW)
    print("\nException of type:"+str(execinfo.type)+ \
      "\nvalue:"+str(execinfo.value))

  def test_creation_DW(self,rtiOutputFixture):
    """
    This function tests the correct instantiation of
    Output object.

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_
    """
    assert isinstance(rtiOutputFixture,rti.Output) \
      and rtiOutputFixture.name == "MyPublisher::MySquareWriter" \
      and isinstance(rtiOutputFixture.connector,rti.Connector) \
      and isinstance(rtiOutputFixture.instance, rti.Instance)

class TestInstance:
  """
  This class tests the correct invocation of functions on
  :class:`rticonnextdds_connector.Instance` object.

  .. todo::

       * No Exception is thrown when a non-existent field is
         accessed. ``AttributeError`` must be propagated
         to the user when a non-existent field is accessed with
         :func:`rticonnextdds_connector.Instance.setNumber`,
         :func:`rticonnextdds_connector.Instance.setString`,
         and :func:`rticonnextdds_connector.Instance.setBoolean`.
         ``KeyError`` must be propagated for
         :func:`rticonnextdds_connector.Instance.setDictionary`
         when setting the Instance object using a dictionary
         with non-existent fields
       * An Instance object can be set with a dictionary containing
         inconsistent value types for existing field-names with
         :func:`rticonnextdds_connector.Instance.setDictionary`.
         A ``TypeError`` should be propagated to users when appropriate
         and implicit type conversion doesn't make sense.

  """

  def test_instance_creation(self,rtiOutputFixture):
    """
    This function tests that an Instance object is correctly
    initialized.

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    """
    assert rtiOutputFixture.instance!=None and \
      isinstance(rtiOutputFixture.instance, rti.Instance)

  def test_setNumber_on_nonexistent_field(self,rtiOutputFixture):
    """
    This function tests that an ``AttributeError`` is raised when
    :func:`rticonnextdds_connector.Instance.setNumber` is called
    on a non-existent field name.

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    .. note:: This test is marked to fail as this case is not handled yet.

    """
    non_existent_field="invalid_field"
    with pytest.raises(rti.Error) as execinfo:
      rtiOutputFixture.instance.setNumber(non_existent_field,1)

  def test_setString_on_nonexistent_field(self,rtiOutputFixture):
    """
    This function tests that an ``AttributeError`` is raised when
    :func:`rticonnextdds_connector.Instance.setString` is called
    on a non-existent field name.

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    .. note:: This test is marked to fail as this case is not handled yet.

    """
    non_existent_field="invalid_field"
    with pytest.raises(rti.Error) as execinfo:
      rtiOutputFixture.instance.set_string(non_existent_field,"1")

  def test_setBoolean_on_nonexistent_field(self,rtiOutputFixture):
    """
    This function tests that an ``AttributeError`` is raised when
    :func:`rticonnextdds_connector.Instance.setBoolean` is called
    on a non-existent field name.

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    .. note:: This test is marked to fail as this case is not handled yet.

    """
    non_existent_field="invalid_field"
    with pytest.raises(rti.Error) as execinfo:
      rtiOutputFixture.instance.set_boolean(non_existent_field,True)

  def test_setDictionary_with_nonexistent_fields(self,rtiOutputFixture):
    """
    This function tests that a ``KeyError`` is raised when
    :func:`rticonnextdds_connector.Instance.setDictionary` is called
    with a dictionary containing non-existent field names.

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    .. note:: This test is marked to fail as this case is not handled yet.

    """
    invalid_dictionary= {"non_existent_field":"value"}
    with pytest.raises(rti.Error, match=r".*non_existent_field*") as execinfo:
      rtiOutputFixture.instance.set_dictionary(invalid_dictionary)

  @pytest.mark.xfail
  # Implicit type conversion from Boolean to number
  def test_setNumber_with_Boolean(self,rtiOutputFixture):
    """
    This function tests that a ``TypeError`` is raised when
    :func:`rticonnextdds_connector.Instance.setNumber` is called
    with a Boolean value

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    .. note:: This test is marked to fail as a Boolean value is
       implicitly type converted to a Number.

    """

    with pytest.raises(rti.Error) as execinfo:
      rtiOutputFixture.instance.set_number("x", True)

  def test_setNumber_with_String(self,rtiOutputFixture):
    """
    This function tests that a ``TypeError`` is raised when
    :func:`rticonnextdds_connector.Instance.setNumber` is called
    with a String value

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    """
    number_field="x"
    with pytest.raises(TypeError) as execinfo:
      rtiOutputFixture.instance.set_number(number_field,"str")
    print("\nException of type:"+str(execinfo.type)+ \
      "\nvalue:"+str(execinfo.value))

  def test_setNumber_with_Dictionary(self,rtiOutputFixture):
    """
    This function tests that a ``TypeError`` is raised when
    :func:`rticonnextdds_connector.Instance.setNumber` is called
    with a Dictionary value

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    """
    number_field="x"
    with pytest.raises(TypeError) as execinfo:
      rtiOutputFixture.instance.set_number(number_field,{"x":1})
    print("\nException of type:"+str(execinfo.type)+ \
      "\nvalue:"+str(execinfo.value))

  def test_setString_with_Boolean(self,rtiOutputFixture):
    """
    This function tests that a ``TypeError`` is raised when
    :func:`rticonnextdds_connector.Instance.setString` is called
    with a Boolean value

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    """
    string_field="color"
    with pytest.raises(TypeError) as execinfo:
      rtiOutputFixture.instance.set_string(string_field,True)
    print("\nException of type:"+str(execinfo.type)+ \
      "\nvalue:"+str(execinfo.value))

  def test_setString_with_Number(self,rtiOutputFixture):
    """
    This function tests that a ``TypeError`` is raised when
    :func:`rticonnextdds_connector.Instance.setString` is called
    with a Number value

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    """
    string_field="color"
    with pytest.raises(TypeError) as execinfo:
      rtiOutputFixture.instance.setString(string_field,55.55)
    print("\nException of type:"+str(execinfo.type)+ \
      "\nvalue:"+str(execinfo.value))

  def test_setString_with_Dictionary(self,rtiOutputFixture):
    """
    This function tests that a ``TypeError`` is raised when
    :func:`rticonnextdds_connector.Instance.setString` is called
    with a Dictionary value

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    """
    string_field="color"
    with pytest.raises(TypeError) as execinfo:
      rtiOutputFixture.instance.set_string(string_field,{"color":1})
    print("\nException of type:"+str(execinfo.type)+ \
      "\nvalue:"+str(execinfo.value))


  def test_setBoolean_with_String(self,rtiOutputFixture):
    """
    This function tests that a ``TypeError`` is raised when
    :func:`rticonnextdds_connector.Instance.setBoolean` is called
    with a String value

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    """
    boolean_field="z"
    with pytest.raises(TypeError) as execinfo:
      rtiOutputFixture.instance.set_boolean(boolean_field,"str")
    print("\nException of type:"+str(execinfo.type)+ \
      "\nvalue:"+str(execinfo.value))

  # Implicit type conversion from number to Boolean
  def test_setBoolean_with_Number(self,rtiOutputFixture):
    """
    This function tests that a ``TypeError`` is raised when
    :func:`rticonnextdds_connector.Instance.setBoolean` is called
    with a Number value

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    .. note:: This test is marked to fail as a Number value is implicitly converted to a
       Boolean value

    """
    boolean_field="z"
    with pytest.raises(TypeError) as execinfo:
      rtiOutputFixture.instance.setBoolean(boolean_field,55.55)
    print("\nException of type:"+str(execinfo.type)+ \
      "\nvalue:"+str(execinfo.value))

  def test_setBoolean_with_Dictionary(self,rtiOutputFixture):
    """
    This function tests that a ``TypeError`` is raised when
    :func:`rticonnextdds_connector.Instance.setBoolean` is called
    with a Dictionary value

    :param rtiOutputFixture: :func:`conftest.rtiOutputFixture`
    :type rtiOutputFixture: `pytest.fixture <https://pytest.org/latest/builtin.html#_pytest.python.fixture>`_

    """
    boolean_field="z"
    with pytest.raises(TypeError) as excinfo:
      rtiOutputFixture.instance.set_boolean(boolean_field,{"color":1})


  def test_wait_for_acknowledgments(self, rtiOutputFixture):
    rtiOutputFixture.write()
    rtiOutputFixture.wait()
    rtiOutputFixture.wait(1) # Should return immediately

  def test_write(self, rtiOutputFixture):
    """
    This function tests that :func:`rticonnectdds_connector.Output.write` call
    fails (and an exception is raised) under a variety of circumstances.
    """
    rtiOutputFixture.instance["color"] = "1"
    rtiOutputFixture.write()
    rtiOutputFixture.instance["color"] = "2"
    rtiOutputFixture.write()
    rtiOutputFixture.instance["color"] = "3"
    # Exception will be raised as we are about to hit max_instances
    with pytest.raises(rti.Error) as excinfo:
      rtiOutputFixture.write()


  def test_write_with_params(self, one_use_output):

    related_id_long = {
      "writer_guid": {"value": [10, 30, 1, 66, 0, 0, 29, 180, 0, 0, 0, 1, 128, 0, 0, 3]},
      "sequence_number": {"high": 0, "low": 1}
    }
    one_use_output.write(identity=related_id_long)

    related_id_short = {
      "writer_guid": [10, 30, 1, 66, 0, 0, 29, 180, 0, 0, 0, 1, 128, 0, 0, 3],
      "sequence_number": 2**53
    }

    one_use_output.write(source_timestamp=100)
    one_use_output.write(related_sample_identity=related_id_short)
    one_use_output.write(
      source_timestamp=100,
      related_sample_identity=related_id_long,
      identity=related_id_short)

    # sequence number must increase
    with pytest.raises(rti.Error):
      one_use_output.write(identity=related_id_short)

    # nonexistent parameter
    with pytest.raises(rti.Error, match=r".*invalid_param.*") as execinfo:
      one_use_output.write(invalid_param="invalid")

    # invalid format
    with pytest.raises(rti.Error, match=r".*error parsing related_sample_identity.*") as execinfo:
      one_use_output.write(related_sample_identity="invalid")
    with pytest.raises(rti.Error, match=r".*error parsing identity.*") as execinfo:
      one_use_output.write(identity="invalid")
    with pytest.raises(rti.Error, match=r".*error parsing source_timestamp.*") as execinfo:
      one_use_output.write(source_timestamp=3.4)
