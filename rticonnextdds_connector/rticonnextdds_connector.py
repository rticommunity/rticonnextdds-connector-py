#
# (c) 2019 Copyright, Real-Time Innovations.  All rights reserved.
# No duplications, whole or partial, manual or electronic, may be made
# without express written permission.  Any such copies, or revisions thereof,
# must display this notice unaltered.
# This code contains trade secrets of Real-Time Innovations, Inc.
#

"""This package contains the Connector type and all other supporting types

To use this package, import it as follows::

   import rticonnextdds_connector as rti

The entry point is the class :class:`Connector`, which creates :class:`Input`
and :class:`Output` objects.
"""

import ctypes
import os
import sys
import weakref
import platform
import json
from contextlib import contextmanager
from numbers import Number

from ctypes import *

def fromcstring(s):
	return s

def tocstring(s):
	return s

def tocstring3(s):
	if s is None:
		return None
	try:
		return s.encode('utf8')
	except AttributeError:
		raise

def fromcstring3(s):
	try:
		return s.decode('utf8')
	except AttributeError:
		raise

if sys.version_info[0] == 3:
	tocstring = tocstring3
	fromcstring = fromcstring3

def _move_native_string(native_str):
	"""Copies a natively-allocated string into a python string and returns the
	native memory"""
	python_str = fromcstring(cast(native_str, c_char_p).value)
	connector_binding.freeString(native_str)
	return python_str

class Error(Exception):
	"""An error in the *RTIConnext DDS Core*"""
	def __init__(self, message):
		Exception.__init__(self, message)

class TimeoutError(Error):
	"""A timeout error in operations that can block"""
	def __init__(self):
		Error.__init__(self, "DDS Timeout Error")

def _get_last_dds_error_message():
	error_msg = connector_binding.getLastErrorMessage()
	if error_msg:
		str_value = _move_native_string(error_msg)
	else:
		str_value = ""
	return str_value

class _ReturnCode:
	ok = 0
	timeout = 10
	no_data = 11

def _check_retcode(retcode):
	if retcode != _ReturnCode.ok and retcode != _ReturnCode.no_data:
		if retcode == _ReturnCode.timeout:
			raise TimeoutError
		else:
			raise Error("DDS Exception: " + _get_last_dds_error_message())

def _check_entity_creation(object, entity_name):
	if object is None:
		raise Error("Failed to create " + entity_name + ": "
			+ _get_last_dds_error_message())

# Definition of this class must match the RTI_Connector_AnyValueKind enum in ddsConnector.ifc
class _AnyValueKind:
	connector_none = 0
	connector_number = 1
	connector_boolean = 2
	connector_string = 3

class _ConnectorBinding:
	def __init__(self):
		(bits, _) = platform.architecture()
		osname = platform.system()
		isArm = platform.uname()[4].startswith("arm")
		additional_lib = None

		if "64" in bits:
			if "Linux" in osname:
				arch = "x64Linux2.6gcc4.4.5"
				libname = "librtiddsconnector"
				post = "so"
			elif "Darwin" in osname:
				arch = "x64Darwin16clang8.0"
				libname = "librtiddsconnector"
				post = "dylib"
			elif "Windows" in osname:
				arch = "x64Win64VS2013"
				libname = "rtiddsconnector"
				post = "dll"
				additional_lib = "msvcr120"
			else:
				raise RuntimeError("This platform ({0}) is not supported".format(osname))
		else:
			if isArm:
				arch = "armv6vfphLinux3.xgcc4.7.2"
				libname = "librtiddsconnector"
				post = "so"
			elif "Linux" in osname:
				arch = "i86Linux3.xgcc4.6.3"
				libname = "librtiddsconnector"
				post = "so"
			elif "Windows" in osname:
				arch = "i86Win32VS2010"
				libname = "rtiddsconnector"
				post = "dll"
				additional_lib = "msvcr100"
			else:
				raise RuntimeError("This platform ({0}) is not supported".format(osname))

		path = os.path.dirname(os.path.realpath(__file__))
		path = os.path.join(path, "..", "rticonnextdds-connector/lib", arch)

		# Load Visual C++ redistributable if available
		if additional_lib is not None:
			try:
				ctypes.cdll.LoadLibrary(os.path.join(path, additional_lib))
			except OSError:
				# Don't fail; try to load rtiddsconnector.dll anyway
				print("Warning: error loading " + additional_lib)

		libname = libname + "." + post
		self.library = ctypes.CDLL(os.path.join(path, libname), ctypes.RTLD_GLOBAL)

		self.new = self.library.RTI_Connector_new
		self.new.restype = ctypes.c_void_p
		self.new.argtypes = [ctypes.c_char_p,ctypes.c_char_p,ctypes.c_void_p]

		self.delete = self.library.RTI_Connector_delete
		self.delete.restype = ctypes.c_void_p
		self.delete.argtypes = [ctypes.c_void_p]

		self.getWriter= self.library.RTI_Connector_get_datawriter
		self.getWriter.restype= ctypes.c_void_p
		self.getWriter.argtypes=[ ctypes.c_void_p,ctypes.c_char_p ]

		self.getReader= self.library.RTI_Connector_get_datareader
		self.getReader.restype= ctypes.c_void_p
		self.getReader.argtypes=[ ctypes.c_void_p,ctypes.c_char_p ]

		self.getNativeSample = self.library.RTI_Connector_get_native_sample
		self.getNativeSample.restype = ctypes.c_void_p
		self.getNativeSample.argtypes=[ ctypes.c_void_p,ctypes.c_char_p, ctypes.c_int]

		self.setNumberIntoSamples = self.library.RTI_Connector_set_number_into_samples
		self.setNumberIntoSamples.restype = ctypes.c_int
		self.setNumberIntoSamples.argtypes = [ctypes.c_void_p, ctypes.c_char_p,ctypes.c_char_p,ctypes.c_double]

		self.setBooleanIntoSamples = self.library.RTI_Connector_set_boolean_into_samples
		self.setBooleanIntoSamples.restype = ctypes.c_int
		self.setBooleanIntoSamples.argtypes = [ctypes.c_void_p, ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int]

		self.setStringIntoSamples = self.library.RTI_Connector_set_string_into_samples
		self.setStringIntoSamples.restype = ctypes.c_int
		self.setStringIntoSamples.argtypes = [ctypes.c_void_p, ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]

		self.clearMember = self.library.RTI_Connector_clear_member
		self.clearMember.restype = ctypes.c_int
		self.clearMember.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

		self.write = self.library.RTI_Connector_write
		self.write.restype = ctypes.c_int
		self.write.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

		self.waitForAcknowledgments = self.library.RTI_Connector_wait_for_acknowledgments
		self.waitForAcknowledgments.restype = ctypes.c_int
		self.waitForAcknowledgments.argtypes = [ctypes.c_void_p, ctypes.c_int]

		self.read = self.library.RTI_Connector_read
		self.read.restype = ctypes.c_int
		self.read.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

		self.take = self.library.RTI_Connector_take
		self.take.restype = ctypes.c_int
		self.take.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

		self.wait = self.library.RTI_Connector_wait_for_data
		self.wait.restype = ctypes.c_int
		self.wait.argtypes = [ctypes.c_void_p, ctypes.c_int]

		self.wait_for_data = self.library.RTI_Connector_wait_for_data_on_reader
		self.wait_for_data.restype = ctypes.c_int
		self.wait_for_data.argtypes = [ctypes.c_void_p, ctypes.c_int]

		self.wait_for_matched_publication = self.library.RTI_Connector_wait_for_matched_publication
		self.wait_for_matched_publication.restype = ctypes.c_int
		self.wait_for_matched_publication.argtypes = [ctypes.c_void_p, ctypes.c_int, POINTER(ctypes.c_int)]

		self.wait_for_matched_subscription = self.library.RTI_Connector_wait_for_matched_subscription
		self.wait_for_matched_subscription.restype = ctypes.c_int
		self.wait_for_matched_subscription.argtypes = [ctypes.c_void_p, ctypes.c_int, POINTER(ctypes.c_int)]

		self.get_matched_subscriptions = self.library.RTI_Connector_get_matched_subscriptions
		self.get_matched_subscriptions.restype = ctypes.c_int
		self.get_matched_subscriptions.argtypes = [ctypes.c_void_p, POINTER(ctypes.c_char_p)]

		self.get_matched_publications = self.library.RTI_Connector_get_matched_publications
		self.get_matched_publications.restype = ctypes.c_int
		self.get_matched_publications.argtypes = [ctypes.c_void_p, POINTER(ctypes.c_char_p)]

		self.clear = self.library.RTI_Connector_clear
		self.clear.restype = ctypes.c_int
		self.clear.argtypes = [ctypes.c_void_p,ctypes.c_char_p]

		self.getBooleanFromInfos = self.library.RTI_Connector_get_boolean_from_infos
		self.getBooleanFromInfos.restype  = ctypes.c_int
		self.getBooleanFromInfos.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

		self.getJSONFromInfos = self.library.RTI_Connector_get_json_from_infos
		self.getJSONFromInfos.restype  = ctypes.c_int
		self.getJSONFromInfos.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]

		self.getSamplesCount = self.library.RTI_Connector_get_sample_count
		self.getSamplesCount.restype = ctypes.c_int
		self.getSamplesCount.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]

		self.getNumberFromSamples = self.library.RTI_Connector_get_number_from_sample
		self.getNumberFromSamples.restype = ctypes.c_int
		self.getNumberFromSamples.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

		self.getBooleanFromSamples = self.library.RTI_Connector_get_boolean_from_sample
		self.getBooleanFromSamples.restype = ctypes.c_int
		self.getBooleanFromSamples.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

		self.getStringFromSamples = self.library.RTI_Connector_get_string_from_sample
		self.getStringFromSamples.restype = ctypes.c_int
		self.getStringFromSamples.argtypes = [ctypes.c_void_p, POINTER(c_char_p), ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

		self.getAnyValueFromSamples = self.library.RTI_Connector_get_any_from_sample
		self.getAnyValueFromSamples.restype = ctypes.c_int
		self.getAnyValueFromSamples.argtypes = [ctypes.c_void_p, POINTER(c_double), POINTER(c_int), POINTER(c_char_p), POINTER(c_int), ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

		self.getAnyValueFromInfo = self.library.RTI_Connector_get_any_from_info
		self.getAnyValueFromInfo.restype = ctypes.c_int
		self.getAnyValueFromInfo.argtypes = [ctypes.c_void_p, POINTER(c_double), POINTER(c_int), POINTER(c_char_p), POINTER(c_int), ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

		self.getJSONSample = self.library.RTI_Connector_get_json_sample
		self.getJSONSample.restype = ctypes.c_int
		self.getJSONSample.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, POINTER(c_char_p)]

		self.getJSONMember = self.library.RTI_Connector_get_json_member
		self.getJSONMember.restype = ctypes.c_int
		self.getJSONMember.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, POINTER(c_char_p)]

		self.setJSONInstance = self.library.RTI_Connector_set_json_instance
		self.setJSONInstance.restype = ctypes.c_int
		self.setJSONInstance.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

		self.set_max_objects_per_thread = self.library.RTI_Connector_set_max_objects_per_thread
		self.set_max_objects_per_thread.restype = ctypes.c_int
		self.set_max_objects_per_thread.argtypes = [ctypes.c_int]

		self.getLastErrorMessage = self.library.RTI_Connector_get_last_error_message
		self.getLastErrorMessage.restype = POINTER(c_char)
		self.getLastErrorMessage.argtypes = []

		self.getNativeInstance = self.library.RTI_Connector_get_native_instance
		self.getNativeInstance.restype = ctypes.c_int
		self.getNativeInstance.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]

		self.freeString = self.library.RTI_Connector_free_string
		self.freeString.argtypes = [POINTER(c_char)]

		self.max_integer_as_double = 2**53

		# This API is only used internally to extend the testing capabilities of
		# Connector. It can be called from the unit tests (and for this reason isn't
		# directly exposed in any classes below) and is used to create various
		# test scenarios in the binding (where we have access to the full DDS API
		# giving us more flexibility).
		self._createTestScenario = self.library.RTI_Connector_create_test_scenario
		self._createTestScenario.restype = ctypes.c_int
		self._createTestScenario.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]

	def get_any_value(self, getter_function, connector, input_name, index, field_name):
		number_value = ctypes.c_double()
		bool_value = ctypes.c_int()
		string_value = ctypes.c_char_p()
		selection = ctypes.c_int()
		retcode = getter_function(
			connector,
			ctypes.byref(number_value),
			ctypes.byref(bool_value),
			ctypes.byref(string_value),
			ctypes.byref(selection),
			tocstring(input_name),
			index + 1,
			tocstring(field_name))
		_check_retcode(retcode)

		if retcode == _ReturnCode.no_data:
			return None

		if selection.value == _AnyValueKind.connector_number:
			return number_value.value
		elif selection.value == _AnyValueKind.connector_boolean:
			return bool_value.value
		elif selection.value == _AnyValueKind.connector_string:
			# A string can represent three different things:
			#  - An actual string value (handled in the except clause)
			#  - A json string; we parse it and convert it to a dictionary
			#  - An integer (larger than what number_value can represent precisely)
			#    the same json parser returns the integer
			python_string = _move_native_string(string_value)
			try:
				return json.loads(python_string)
			except ValueError:
				# This is the best way we have to detect that this is not a json
				# string or an integer
				return python_string
		else:
			# This shouldn't happen
			raise Error("Unexpected type returned by " + getter_function.__name__)

connector_binding = _ConnectorBinding()

class _ConnectorOptions(ctypes.Structure):
	_fields_ = [("enable_on_data_event", c_int), ("one_based_sequence_indexing", c_int)]

#
# Public API
#

class Samples:
	"""Provides access to the data samples read by an Input (:attr:`Input.samples`)

	This class provides the special method ``__iter__`` to iterate over the data
	samples and ``__getitem__`` to access a specific sample by index. Both return
	the type :class:`SampleIterator`.

	The default iterator provides access to all the data samples retrieved by the
	most-recent call to :meth:`read()` or :meth:`take()`. Use :meth:`valid_data_iter`
	to access only samples with valid data.

	``Samples`` is the type of the property :attr:`Input.samples`.

	For more information and examples see :ref:`Accessing the data samples`.

	Special methods:
		* ``__getitem__`` gets a sample by index: ``input.samples[i]``
		* ``__iter__`` enables iteration: ``for s in input.samples: ...``
	"""

	def __init__(self,input):
		self.input = input

	def __getitem__(self, index):
		"""Gets an iterator to a sample in a specific index"""

		return SampleIterator(self.input, index)

	def __iter__(self):
		"""Iterates over the data samples"""

		return SampleIterator(self.input)

	@property
	def length(self):
		"""Returns the number of samples available

		:return: The number of samples available since the last time read/take was called
		"""

		return self.input.samples.getLength()

	@property
	def valid_data_iter(self):
		"""Returns an iterator to the data samples with valid data

		The iterator provides access to the data samples retrieved by the
		most-recent call to :meth:`Input.read()` or :meth:`Input.take()`, and
		skips samples with invalid data (meta-data only).

		To access all samples, including those with meta-data only,
		iterate over :attr:`Input.samples` directly.

		By using this iterator, it is not necessary to check if each sample
		contains valid data.

		:return: An iterator to the data samples with valid
		:rtype: :class:`ValidSampleIterator`
		"""
		return ValidSampleIterator(self.input)

	def getLength(self):
		c_value = ctypes.c_double()
		retcode = connector_binding.getSamplesCount(
				self.input.connector.native,
				tocstring(self.input.name),
				ctypes.byref(c_value))
		_check_retcode(retcode)
		return int(c_value.value)

	def getNumber(self, index, field_name):
		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")

		# Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		c_value = ctypes.c_double()
		retcode = connector_binding.getNumberFromSamples(
			self.input.connector.native,
			ctypes.byref(c_value),
			tocstring(self.input.name),
			index,
			tocstring(field_name))
		_check_retcode(retcode)

		if retcode == _ReturnCode.no_data:
			return None

		return c_value.value

	def getBoolean(self, index, field_name):
		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1

		c_value = ctypes.c_int()
		retcode = connector_binding.getBooleanFromSamples(
			self.input.connector.native,
			ctypes.byref(c_value),
			tocstring(self.input.name),
			index,
			tocstring(field_name))
		_check_retcode(retcode)

		if retcode == _ReturnCode.no_data:
			return None

		return c_value.value

	def getString(self, index, field_name):
		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")

		index = index + 1
		c_value = ctypes.c_char_p()
		retcode = connector_binding.getStringFromSamples(
			self.input.connector.native,
			ctypes.byref(c_value),
			tocstring(self.input.name),
			index,
			tocstring(field_name))
		_check_retcode(retcode)
		if retcode == _ReturnCode.no_data:
			return None

		return _move_native_string(c_value)

	def getDictionary(self, index, member_name = None):
		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")
		# Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		if member_name is None:
			native_json_str = ctypes.c_char_p()
			retcode = connector_binding.getJSONSample(
				self.input.connector.native,
				tocstring(self.input.name),
				index,
				ctypes.byref(native_json_str))
		elif not isinstance(member_name, str):
			raise ValueError("member_name must be a string")
		else:
			native_json_str = ctypes.c_char_p()
			retcode = connector_binding.getJSONMember(
				self.input.connector.native,
				tocstring(self.input.name),
				index,
				tocstring(member_name),
				ctypes.byref(native_json_str))
		_check_retcode(retcode)
		if retcode == _ReturnCode.no_data:
			return None
		return json.loads(_move_native_string(native_json_str))

	def getNative(self,index):
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		dynDataPtr = connector_binding.getNativeSample(self.input.connector.native,tocstring(self.input.name),index)
		return dynDataPtr

# Deprecated: use SampleIterator.info
class Infos:
	def __init__(self,input):
		self.input = input

	def getLength(self):
		c_value = ctypes.c_double()
		retcode = connector_binding.getSamplesCount(
				self.input.connector.native,
				tocstring(self.input.name),
				ctypes.byref(c_value))
		_check_retcode(retcode)
		return c_value.value

	def isValid(self, index):
		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1

		c_value = ctypes.c_int()
		retcode = connector_binding.getBooleanFromInfos(
			self.input.connector.native,
			ctypes.byref(c_value),
			tocstring(self.input.name),
			index,
			tocstring('valid_data'))
		_check_retcode(retcode)
		if retcode == _ReturnCode.no_data:
			return None
		return c_value.value

	def getSampleIdentity(self, index):
		native_json_str = ctypes.c_char_p()
		retcode = connector_binding.getJSONFromInfos(
			self.input.connector.native,
			tocstring(self.input.name),
			index,
			tocstring('sample_identity'),
			ctypes.byref(native_json_str))
		_check_retcode(retcode)
		return json.loads(fromcstring(native_json_str))

	def getRelatedSampleIdentity(self, index):
		native_json_str = ctypes.c_char_p()
		retcode = connector_binding.getJSONFromInfos(
			self.input.connector.native,
			tocstring(self.input.name),
			index,
			tocstring('related_sample_identity'),
			ctypes.byref(native_json_str))
		_check_retcode(retcode)
		return json.loads(fromcstring(native_json_str))

class SampleInfo:
	"""The type of :attr:`SampleIterator.info`"""

	def __init__(self, input, index):
		self.input = input
		self.index = index

	def __getitem__(self, field_name):
		return connector_binding.get_any_value(
			getter_function = connector_binding.getAnyValueFromInfo,
			connector = self.input.connector.native,
			input_name = self.input.name,
			index = self.index,
			field_name = field_name)

class SampleIterator:
	"""Iterates and provides access to a data sample

	A SampleIterator provides access to the data received by an input.
	SampleIterator is the iterator type of :attr:`Input.samples`.

	See :ref:`Reading data (Input)`.

	Special methods:
		* ``__getitem__`` retrieves a field, see :ref:`Accessing the data`
		* ``__iter__`` enables iteration
		* ``__next__`` moves to the next sample
	"""

	def __init__(self, input, index = -1):
		self.input = input
		self.index = index
		self.length = input.samples.getLength()

	@property
	def valid_data(self):
		"""Returns whether this sample contains valid data

		If this returns ``False``, this object's getters cannot be called.
		"""

		return self.input.infos.isValid(self.index)

	@property
	def info(self):
		"""Provides access to this sample's meta-data

		The info object expects one of the **SampleInfo** field names::

			value = sample_it.info[field]

		Supported fields:

		* ``"source_timestamp"``, returns an integer representing nanoseconds
		* ``"reception_timestamp"``, returns an integer representing nanoseconds
		* ``"sample_identity"``, or ``"identity"`` returns a dictionary (see :meth:`Output.write`)
		* ``"related_sample_identity"`` returns a dictionary (see :meth:`Output.write`)
		* ``"valid_data"``, returns a boolean (equivalent to ``sample_it.valid_data``)

		These fields are documented in `The SampleInfo Structure <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/The_SampleInfo_Structure.htm#7.4.6_The_SampleInfo_Structure%3FTocPath%3DPart%25202%253A%2520Core%2520Concepts%7C7.%2520Receiving%2520Data%7C7.4%2520Using%2520DataReaders%2520to%2520Access%2520Data%2520(Read%2520%2526%2520Take)%7C7.4.6%2520The%2520SampleInfo%2520Structure%7C_____0>`__
		section in the *Connext DDS Core Libraries User's Manual*.
		"""
		return SampleInfo(self.input, self.index)

	def __getitem__(self, field_name):
		return connector_binding.get_any_value(
			getter_function = connector_binding.getAnyValueFromSamples,
			connector = self.input.connector.native,
			input_name = self.input.name,
			index = self.index,
			field_name = field_name)

	def get_dictionary(self, member_name = None):
		"""Gets a dictionary with the values of all the fields of this sample

		The dictionary keys are the field names and the dictionary values correspond
		to each field value. To see how nested types, sequences, and arrays are
		represented, see :ref:`Accessing the data`.

		:param str member_name: (Optional) The name of the complex member or field. The type of the member with name member_name must be an array, sequence, struct, value or union.
		:return: A dictionary containing all the fields of the sample, or if a member_name is supplied, all the fields or elements of that member.
		"""

		return self.input.samples.getDictionary(self.index, member_name)

	def get_number(self, field_name):
		"""Gets the value of a numeric field in this sample

		:param str field_name: The name of the field. See :ref:`Accessing the data`.
		:return: The numeric value for the field ``field_name``.
		"""

		return self.input.samples.getNumber(self.index, field_name)

	def get_boolean(self, field_name):
		"""Gets the value of a boolean field in this sample

		:param str field_name: The name of the field. See :ref:`Accessing the data`.
		:return: The boolean value for the field ``field_name``.
		"""

		return self.input.samples.getBoolean(self.index, field_name)

	def get_string(self, field_name):
		"""Gets the value of a string field in this sample

		:param str field_name: The name of the field. See :ref:`Accessing the data`.
		:return: The string value for the field ``field_name``.
		"""

		return self.input.samples.getString(self.index, field_name)

	@property
	def native(self):
		return self.input.samples.getNative(self.index)

	def __iter__(self):
		"""Enables iteration"""

		self.index = -1
		return self

	def __next__(self):
		"""Moves to the next sample"""

		if self.index + 1 < self.length:
			self.index = self.index + 1
			return self
		else:
			raise StopIteration

	def next(self):
		"""Moves to the next sample"""
		return self.__next__()

class ValidSampleIterator(SampleIterator):
	"""Iterates and provides access to data samples with valid data

	This iterator provides the same methods as :class:`SampleIterator`.

	See :meth:`Samples.valid_data_iter`.
	"""

	def __next__(self):
		while self.index + 1 < self.length and not self.input.infos.isValid(self.index + 1):
			self.index = self.index + 1

		return SampleIterator.__next__(self)

	def next(self):
		return self.__next__()

class Input:
	"""Allows reading data for a Topic

	To get an input object, use :meth:`Connector.get_input()`.

	Attributes:
		* ``connector`` (:class:`Connector`): The ``Connector`` that created this ``Input``
		* ``name`` (str): The name of this ``Output`` (the name used in :meth:`Connector.getOutput`)
		* ``native``: A native handle that allows accessing additional *Connext DDS* APIs in C.
	"""

	def __init__(self, connector, name):
		self.connector = connector
		self.name = name
		self.native = connector_binding.getReader(self.connector.native,tocstring(self.name))
		_check_entity_creation(self.native, "Input")
		self._samples = Samples(self)
		self.infos = Infos(self)

	def read(self):
		"""Access the samples received by this Input

		This operation performs the same operation as :meth:`take()` except that
		the samples remain accessible.
		"""

		_check_retcode(connector_binding.read(self.connector.native,tocstring(self.name)))

	def take(self):
		"""Accesses the sample received by this Input

		After calling this method, the samples are accessible from :attr:`samples`

		"""

		_check_retcode(connector_binding.take(self.connector.native,tocstring(self.name)))

	@property
	def samples(self):
		"""Allows iterating over the samples read by this input

		This container provides iterators to access the data samples retrieved
		by the most-recent call to :meth:`read()` or :meth:`take()`.

		:rtype: :class:`Samples`
		"""

		return self._samples

	def wait(self, timeout = None):
		"""Wait for this input to receive data.

		This method waits for the specified timeout for data to be received by
		this input.
		If the operation times out, it raises :class:`TimeoutError`.

		:param number timeout: The maximum time to wait in milliseconds. By default, infinite.
		"""
		if timeout is None:
			timeout = -1
		retcode = connector_binding.wait_for_data(self.native, timeout)
		_check_retcode(retcode)

	def wait_for_publications(self, timeout = None):
		"""Waits until this input matches or unmatches a compatible DDS subscription.

		If the operation times out, it will raise :class:`TimeoutError`.

		:param number timeout: The maximum time to wait in milliseconds. By default, infinite.

		:return: The change in the current number of matched outputs. If a positive number is returned, the input has matched with new publishers. If a negative number is returned the input has unmatched from an output. It is possible for multiple matches and/or unmatches to be returned (e.g., 0 could be returned, indicating that the input matched the same number of writers as it unmatched).

		"""
		if timeout is None:
			timeout = -1
		current_count_change = ctypes.c_int()
		retcode = connector_binding.wait_for_matched_publication(self.native, timeout, byref(current_count_change))
		_check_retcode(retcode)
		return current_count_change.value

	@property
	def matched_publications(self):
		"""Returns information about the matched publications

		This property returns a list where each element is a dictionary with
		information about a publication matched with this Input.

		Currently, the only key in the dictionaries is ``"name"``,
		containing the publication name. If a publication doesn't have name,
		the value for the key ``name`` is ``None``.

		Note that Connector Outputs are automatically assigned a name from the
		*data_writer name* in the XML configuration.
		"""
		native_json_str = ctypes.c_char_p()
		retcode = connector_binding.get_matched_publications(self.native, byref(native_json_str))
		_check_retcode(retcode)
		return json.loads(_move_native_string(native_json_str))

class Instance:
	"""A data sample

		``Instance`` is the type of ``Output.instance`` and is the object that
		is published.

		An Instance has an associated DDS Type, specified in the XML configuration,
		and it allows setting the values for the fields of the DDS Type.

		Attributes:
			* ``output`` (:class:`Output`): The ``Output`` that owns this ``Instance``.

		Special methods:
			* ``__setitem__``, see :ref:`Accessing the data`.
	"""

	def __init__(self, output):
		self.output = output

	def clear_member(self, field_name):
		"""Resets a member to its default value

		The effect is the same as that of :meth:`Output.clear_members()` except
		that only one member is cleared.

		:param str field_name: The name of the field. It can be a complex member or a primitive member. See :ref:`Accessing the data`.
		"""

		retcode = connector_binding.clearMember(
			self.output.connector.native,
			tocstring(self.output.name),
			tocstring(field_name))
		_check_retcode(retcode)

	def __setitem__(self, field_name, value):
		"""Sets the value of field_name

		:param str field_name: The name of the field. See :ref:`Accessing the data`.
		:param number value: A numeric, boolean or string value or ``None`` to unset an optional member.

		The type of the argument must correspond with the type of the field as defined
		in the configuration file.

		This is an alternative to :meth:`set_number`, :meth:`set_string` and :meth:`set_boolean`
		"""
		if field_name is None:
			raise AttributeError("field_name cannot be None")

		if isinstance(value, Number):
			if (value < connector_binding.max_integer_as_double):
				self.set_number(field_name, value)
			else:
				# Work around set_number int-to-double conversion
				self.set_dictionary({field_name:value})
		elif isinstance(value, str):
			self.set_string(field_name, value)
		elif isinstance(value, bool):
			self.set_boolean(field_name, value)
		elif isinstance(value, dict) or isinstance(value, list):
			self.set_dictionary({field_name:value})
		elif value is None:
			self.clear_member(field_name)
		else:
			raise TypeError("'{0}' is not a valid type for 'value'".format(type(value).__name__))

	def set_number(self, field_name, value):
		"""Sets a numeric field

		:param str field_name: The name of the field. See :ref:`Accessing the data`.
		:param number value: A numeric value or ``None`` to unset an optional member
		"""

		if field_name is None:
			raise AttributeError("field_name cannot be None")
		elif value is None:
			self.clear_member(field_name)
		else:
			try:
				_check_retcode(connector_binding.setNumberIntoSamples(
					self.output.connector.native,
					tocstring(self.output.name),
					tocstring(field_name),
					value))
			except ctypes.ArgumentError:
				raise TypeError("value for field '{0}' must be of a numeric type"\
					.format(field_name))

	# Deprecated: use set_number
	def setNumber(self, field_name, value):
		self.set_number(field_name, value)

	def set_boolean(self, field_name, value):
		"""Sets a Boolean field

		:param str field_name: The name of the field. See :ref:`Accessing the data`.
		:param number value: ``True`` or ``False``, or ``None`` to unset an optional member
		"""

		if field_name is None:
			raise AttributeError("field_name cannot be None")
		elif value is None:
			self.clear_member(field_name)
		else:
			try:
				_check_retcode(connector_binding.setBooleanIntoSamples(
						self.output.connector.native,
						tocstring(self.output.name),
						tocstring(field_name),
						value))
			except ctypes.ArgumentError:
				raise TypeError("value for field '{0}' must be of type bool"\
					.format(field_name))

	# Deprecated: use set_boolean
	def setBoolean(self, field_name, value):
		self.set_boolean(field_name, value)

	def set_string(self, field_name, value):
		"""Sets a string field

		:param str field_name: The name of the field. See :ref:`Accessing the data`.
		:param str value: The string value or ``None`` to unset an optional member
		"""

		if field_name is None:
			raise AttributeError("field_name cannot be None")
		elif value is None:
			self.clear_member(field_name)
		else:
			try:
				_check_retcode(connector_binding.setStringIntoSamples(
					self.output.connector.native,
					tocstring(self.output.name),
					tocstring(field_name),
					tocstring(value)))
			except (AttributeError, ctypes.ArgumentError):
				raise TypeError("value for field '{0}' must be of type str"\
					.format(field_name))

	# Deprecated: use set_string
	def setString(self, field_name, value):
		self.set_string(field_name, value)

	def set_dictionary(self, dictionary):
		"""Sets the member values specified in a dictionary

		The dictionary keys are the member names of the Output's type,
		and the dictionary values are the values for those members.

		This method sets the values of those member that are explicitly specified
		in the dictionary. Any member that is not specified in the dictionary
		retains its previous value.

		To clear members that are not in the dictionary, you can call
		:meth:`Output.clear_members()` before this method. You can also
		explicitly set any value in the dictionary to ``None`` to set that member
		to its default value.

		:param dict dictionary: The dictionary containing the keys (member names) and values (values for the members)
		"""

		jsonStr = json.dumps(dictionary)
		_check_retcode(connector_binding.setJSONInstance(
			self.output.connector.native,
			tocstring(self.output.name),
			tocstring(jsonStr)))

	# Deprecated: use set_dictionary
	def setDictionary(self, dictionary):
		self.set_dictionary(dictionary)

	@property
	def native(self):
		"""Obtains the native C object

		This allows accessing additional *Connext DDS* APIs in C.
		"""

		dynamic_data_pointer = ctypes.c_void_p()
		retcode = connector_binding.getNativeInstance(
			self.output.connector.native,
			tocstring(self.output.name),
			ctypes.byref(dynamic_data_pointer))
		_check_retcode(retcode)
		return dynamic_data_pointer

	# Deprecated: use native property
	def getNative(self):
		return self.native


class Output:
	"""Allows writting data for a DDS Topic

	Attributes:
		* ``instance`` (:class:`Instance`): The data that is written when :meth:`write()` is called.
		* ``connector`` (:class:`Connector`): The Connector that created this Output
		* ``name`` (str): The name of this ``Output`` (the name used in :meth:`Connector.getOutput`)
		* ``native``: A native handle that allows accessing additional *Connext DDS* APIs in C.

	See `Writing Data (Output)`.
	"""

	def __init__(self, connector, name):
		self.connector = connector
		self.name = name
		self.native= connector_binding.getWriter(self.connector.native,tocstring(self.name))
		_check_entity_creation(self.native, "Output")
		self.instance = Instance(self)

	def write(self, **kwargs):
		"""Publishes the values of the current ``instance``

		Note that after writing it, ``instance``'s values remain
		unchanged. If for the next write you need to start from scratch, use
		:meth:`clear_members()`

		This method can also *dispose* or *unregister* an instance by passing
		the argument ``action="dispose"`` or ``action="unregister"``. In these
		two cases, only the ``instance`` *key* members are required.

		This method receives a number of optional parameters, a subset of those
		documented in the `Writing Data section <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/Writing_Data.htm?Highlight=DDS_WriteParams_t>`__.
		of the *Connext DDS Core Libraries* User's Manual.

		The supported parameters are:

		:param action str: One of ``"write"`` (default), ``"dispose"`` or ``"unregister"``
		:param integer source_timestamp: The source timestamp, an integer representing the total number of nanoseconds
		:param dict identity: A dictionary containing the keys ``"writer_guid"`` (a list of 16 bytes) and ``"sequence_number"`` (an integer) that uniquely identifies this sample.
		:param dict related_sample_identity: Used for request-reply communications. It has the same format as ``identity``

		For example::

			output.write(
				identity={"writer_guid":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], "sequence_number":1},
				timestamp=1000000000)

		The write method can block under multiple circumstances (see
		*Blocking During a write()* in the *Connext DDS Core Libraries* User's
		Manual). If the blocking time exceeds the *max_blocking_time*, this
		method raises :class:`TimeoutError`.
		"""

		if len(kwargs) > 0:
			json_str = tocstring(json.dumps(kwargs))
		else:
			json_str = None

		retcode = connector_binding.write(
			self.connector.native,
			tocstring(self.name),
			json_str)
		_check_retcode(retcode)

	def wait(self, timeout=None):
		"""Waits until all matching reliable subscriptions have acknowledged all
		the samples that have been currently written.

		This method only waits if this output is configured with a reliable *datawriter_qos*.

		If the operation times out, it raises :class:`TimeoutError`.

		:param number timeout: The maximum time to wait in milliseconds. By default, infinite.
		"""

		if timeout is None:
			timeout = -1
		retcode = connector_binding.waitForAcknowledgments(self.native, timeout)
		_check_retcode(retcode)

	def wait_for_subscriptions(self, timeout = None):
		"""Waits until the number of matched DDS subscription changes

		This method waits until new compatible subscriptions are discovered or
		existing subscriptions no longer match.

		:param number timeout: The maximum time to wait in milliseconds. By default, infinite.
		:return: The change in the current number of matched outputs. If a positive number is returned, the input has matched with new publishers. If a negative number is returned the input has unmatched from an output. It is possible for multiple matches and/or unmatches to be returned (e.g., 0 could be returned, indicating that the input matched the same number of writers as it unmatched).

		This method raises :class:`TimeoutError` if the ``timeout`` elapses.

		"""
		if timeout is None:
			timeout = -1
		current_count_change = ctypes.c_int()
		retcode = connector_binding.wait_for_matched_subscription(self.native, timeout, byref(current_count_change))
		_check_retcode(retcode)
		return current_count_change.value

	@property
	def matched_subscriptions(self):
		"""Returns information about the matched subscriptions

		This property returns a list where each element is a dictionary with
		information about a subscription matched with this Output.

		Currently, the only key in the dictionaries is ``"name"``,
		containing the subscription name. If a subscription doesn't have name,
		the value is ``None``.

		Note that Connector Inputs are automatically assigned a name from the
		*data_reader name* in the XML configuration.
		"""

		native_json_str = ctypes.c_char_p()
		retcode = connector_binding.get_matched_subscriptions(self.native, byref(native_json_str))
		_check_retcode(retcode)
		return json.loads(_move_native_string(native_json_str))

	def clear_members(self):
		"""Resets the values of the members of this ``Output.instance``

		If the member is defined with the ``default`` attribute in the configuration
		file, it gets that value. Otherwise numbers are set to 0, and strings
		are set to empty. Sequences are cleared. Optional members are set to ``None``.

		For example, if this ``Output``'s type is `ShapeType` (from the previous
		example), then ``clear_members()`` sets `color` to "RED", `shapesize`
		to 30, and `x` and `y` to 0.
		"""

		retcode = connector_binding.clear(self.connector.native,tocstring(self.name))
		_check_retcode(retcode)

class Connector:
	"""Loads a configuration and creates its Inputs and Outputs

	A ``Connector`` instance loads a configuration from an XML document. For example::

		connector = rti.Connector("MyParticipantLibrary::MyParticipant", "MyExample.xml")

	After creating it, the ``Connector``'s Inputs can be used to read data, and
	the Outputs to write. See :meth:`get_input()` and :meth:`get_output()`.

	An application can create multiple ``Connector`` instances for the same or
	different configurations.

	A ``Connector`` instance must be deleted with :meth:`close()`.

	:param str config_name: The configuration to load. 	The ``config_name`` format is ``"LibraryName::ParticipantName"``, where ``LibraryName`` is the ``name`` attribute of a ``<domain_participant_library>`` tag, and ``ParticipantName`` is the ``name`` attribute of a ``<domain_participant>`` tag inside the library.
	:param str url: An URL locating the XML document. The ``url`` can be a file path (for example, ``'/tmp/my_dds_config.xml'``) or a string containing the full XML document with the following format ``'str://"<dds>...</dds>"'``)

	"""

	def __init__(self, config_name, url):
		# enable data event (default), 0-based seq indexing
		options = _ConnectorOptions(
			enable_on_data_event = 1,
			one_based_sequence_indexing = 0)
		self.native = connector_binding.new(
			tocstring(config_name),
			tocstring(url),
			ctypes.byref(options))
		_check_entity_creation(self.native, "Connector")

	def close(self):
		"""Frees all the resources created by this Connector instance"""

		connector_binding.delete(self.native)

	# Deprecated: use close()
	def delete(self):
		connector_binding.delete(self.native)

	def get_output(self, output_name):
		"""Returns the :class:`Output` named ``output_name``

		``output_name`` identifies a ``<data_writer>`` tag in the
		configuration loaded by this ``Connector``. For example, the following code::

			connector = rti.Connector("MyParticipantLibrary::MyParticipant", "MyExample.xml")
			connector.get_output("MyPublisher::MyWriter")


		Loads the ``Output`` in this example XML::

			<domain_participant_library name="MyParticipantLibrary">
			  <domain_participant name="MyParticipant" domain_ref="MyDomainLibrary::MyDomain">
			  	<publisher name="MyPublisher">
			  	  <data_writer name="MyWriter" topic_ref="MyTopic"/>
			  	  ...
			  	</publisher>
			  	...
			  </domain_participant>
			  ...
			<domain_participant_library>

		:param str output_name: The name of a the ``data_writer`` to load, with the format ``"PublisherName::DataWriterName"``.
		:return: The Output if it exists, or else it raises ``ValueError``.
		:rtype: :class:`Output`

		"""

		return Output(self, output_name)

	# Deprecated: use get_output
	def getOutput(self, output_name):
		return self.get_output(output_name)

	def get_input(self, input_name):
		"""Returns the :class:`Input` named ``input_name``

		``input_name`` identifies a ``<data_reader>`` tag in the
		configuration loaded by this ``Connector``. For example, the following code::

			connector = rti.Connector("MyParticipantLibrary::MyParticipant", "MyExample.xml")
			connector.get_input("MySubscriber::MyReader")

		Loads the ``Output`` in this example XML::

			<domain_participant_library name="MyParticipantLibrary">
			  <domain_participant name="MyParticipant" domain_ref="MyDomainLibrary::MyDomain">
			  	<subscriber name="MySubscriber">
			  	  <data_reader name="MyReader" topic_ref="MyTopic"/>
			  	  ...
			  	</subscriber>
			  	...
			  </domain_participant>
			  ...
			<domain_participant_library>

		:param str input_name: The name of a the ``data_reader`` to load, with the format ``"SubscriberName::DataReaderName"``.
		:return: The Input if it exists, or else it raises ``ValueError``.
		:rtype: :class:`Input`

		"""

		return Input(self, input_name)

	# Deprecated: use get_input()
	def getInput(self, input_name):
		return self.get_input(input_name)

	def wait(self,timeout = None):
		"""Waits for data to be received on any input

		If the operation times out, it raises :class:`TimeoutError`.

		:param number timeout: The maximum to wait in milliseconds. By default, infinite.
		"""

		if timeout is None:
			timeout = -1
		retcode = connector_binding.wait(self.native,timeout)
		_check_retcode(retcode)

	@staticmethod
	def set_max_objects_per_thread(value):
		"""Allows increasing the number of Connector instances that can be created

		The default value is 1024. If your application creates more than eight
		``Connector`` instances approximately, you may have to increase this
		value.

		This operation can only be called before creating any ``Connector``
		instance.

		See `SYSTEM_RESOURCE_LIMITS QoS Policy <https://community.rti.com/static/documentation/connext-dds/6.0.0/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_UsersManual/index.htm#UsersManual/SYSTEM_RESOURCE_LIMITS_QoS.htm>`__
		in the *RTI Connext DDS* User's Manual.

		:param number value: The value for *max_objects_per_thread*
		"""
		_check_retcode(connector_binding.set_max_objects_per_thread(value))

@contextmanager
def open_connector(config_name, url):
	"""A resource manager that creates and deletes a Connector

	It takes the sames arguments as the :class:`Connector` class::

		with rti.open_connector("MyParticipantLibrary::MyParticipant","./ShapeExample.xml") as connector:
			input = connector.get_input("SubscriberName::DataReaderName")
			# ...
		# connector closed after with block exits
	"""

	connector = Connector(config_name, url)
	try:
		yield connector
	finally:
		connector.close()
