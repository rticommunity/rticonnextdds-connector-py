###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.	   #
# No duplications, whole or partial, manual or electronic, may be made		#
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.										 #
# This code contains trade secrets of Real-Time Innovations, Inc.			 #
###############################################################################

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
(bits, linkage) = platform.architecture()
osname = platform.system()
isArm = platform.uname()[4].startswith("arm")

def fromcstring(s):
	return s

def tocstring(s):
	return s

def tocstring3(s):
	try:
		return s.encode('utf8')
	except AttributeError as e:
		raise

def fromcstring3(s):
	try:
		return s.decode('utf8')
	except AttributeError as e:
		raise

class Error(Exception):
	"""An error in the *RTIConnext DDS Core*"""
	def __init__(self):
		Exception.__init__(self, "DDS Exception: " + _get_last_dds_error_message())


def _get_last_dds_error_message():
	error_msg = rtin_RTIDDSConnector_getLastErrorMessage()
	if error_msg:
		str_value = fromcstring(cast(error_msg, c_char_p).value)
		rtin_RTIDDSConnector_freeString(error_msg)
	else:
		str_value = ""
	return str_value

class _ReturnCode:
	ok = 0
	no_data = 11

def _check_retcode(retcode):
	if retcode != _ReturnCode.ok and retcode != _ReturnCode.no_data:
		raise Error

if sys.version_info[0] == 3 :
	tocstring = tocstring3
	fromcstring = fromcstring3


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
	else:
		print("platfrom not yet supported")
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
	else:
		print("platfrom not yet supported")

path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(path, "..", "rticonnextdds-connector/lib", arch)
libname = libname + "." + post
rti = ctypes.CDLL(os.path.join(path, libname), ctypes.RTLD_GLOBAL)

rtin_RTIDDSConnector_new = rti.RTIDDSConnector_new
rtin_RTIDDSConnector_new.restype = ctypes.c_void_p
rtin_RTIDDSConnector_new.argtypes = [ctypes.c_char_p,ctypes.c_char_p,ctypes.c_void_p]

rtin_RTIDDSConnector_delete = rti.RTIDDSConnector_delete
rtin_RTIDDSConnector_delete.restype = ctypes.c_void_p
rtin_RTIDDSConnector_delete.argtypes = [ctypes.c_void_p]

rtin_RTIDDSConnector_getWriter= rti.RTIDDSConnector_getWriter
rtin_RTIDDSConnector_getWriter.restype= ctypes.c_void_p
rtin_RTIDDSConnector_getWriter.argtypes=[ ctypes.c_void_p,ctypes.c_char_p ]

rtin_RTIDDSConnector_getReader= rti.RTIDDSConnector_getReader
rtin_RTIDDSConnector_getReader.restype= ctypes.c_void_p
rtin_RTIDDSConnector_getReader.argtypes=[ ctypes.c_void_p,ctypes.c_char_p ]

rtin_RTIDDSConnector_getNativeSample = rti.RTIDDSConnector_getNativeSample
rtin_RTIDDSConnector_getNativeSample.restype = ctypes.c_void_p
rtin_RTIDDSConnector_getNativeSample.argtypes=[ ctypes.c_void_p,ctypes.c_char_p, ctypes.c_int]

rtin_RTIDDSConnector_setNumberIntoSamples = rti.RTIDDSConnector_setNumberIntoSamples
rtin_RTIDDSConnector_setNumberIntoSamples.argtypes = [ctypes.c_void_p, ctypes.c_char_p,ctypes.c_char_p,ctypes.c_double]
rtin_RTIDDSConnector_setBooleanIntoSamples = rti.RTIDDSConnector_setBooleanIntoSamples
rtin_RTIDDSConnector_setBooleanIntoSamples.argtypes = [ctypes.c_void_p, ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int]
rtin_RTIDDSConnector_setStringIntoSamples = rti.RTIDDSConnector_setStringIntoSamples
rtin_RTIDDSConnector_setStringIntoSamples.argtypes = [ctypes.c_void_p, ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]
rtin_RTIDDSConnector_clearMember = rti.RTIDDSConnector_clearMember
rtin_RTIDDSConnector_clearMember.restype = ctypes.c_int
rtin_RTIDDSConnector_clearMember.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

rtin_RTIDDSConnector_write = rti.RTIDDSConnector_write
rtin_RTIDDSConnector_write.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

rtin_RTIDDSConnector_read = rti.RTIDDSConnector_read
rtin_RTIDDSConnector_read.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
rtin_RTIDDSConnector_take = rti.RTIDDSConnector_take
rtin_RTIDDSConnector_take.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

rtin_RTIDDSConnector_wait = rti.RTIDDSConnector_wait
rtin_RTIDDSConnector_wait.restype = ctypes.c_int
rtin_RTIDDSConnector_wait.argtypes = [ctypes.c_void_p, ctypes.c_int]

rtin_RTIDDSConnector_getInfosLength = rti.RTIDDSConnector_getInfosLength
rtin_RTIDDSConnector_getInfosLength.restype = ctypes.c_double
rtin_RTIDDSConnector_getInfosLength.argtypes = [ctypes.c_void_p,ctypes.c_char_p]

rtin_RTIDDSConnector_clear = rti.RTIDDSConnector_clear
rtin_RTIDDSConnector_clear.argtypes = [ctypes.c_void_p,ctypes.c_char_p]


rtin_RTIDDSConnector_getBooleanFromInfos = rti.RTIDDSConnector_getBooleanFromInfos
rtin_RTIDDSConnector_getBooleanFromInfos.restype  = ctypes.c_int
rtin_RTIDDSConnector_getBooleanFromInfos.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

rtin_RTIDDSConnector_getJSONFromInfos = rti.RTIDDSConnector_getJSONFromInfos
rtin_RTIDDSConnector_getJSONFromInfos.restype  = ctypes.c_char_p
rtin_RTIDDSConnector_getJSONFromInfos.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

rtin_RTIDDSConnector_getSamplesLength = rti.RTIDDSConnector_getInfosLength
rtin_RTIDDSConnector_getSamplesLength.restype = ctypes.c_double
rtin_RTIDDSConnector_getSamplesLength.argtypes = [ctypes.c_void_p,ctypes.c_char_p]

rtin_RTIDDSConnector_getNumberFromSamples = rti.RTIDDSConnector_getNumberFromSamplesWithRetcode
rtin_RTIDDSConnector_getNumberFromSamples.restype = ctypes.c_int
rtin_RTIDDSConnector_getNumberFromSamples.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

rtin_RTIDDSConnector_getBooleanFromSamples = rti.RTIDDSConnector_getBooleanFromSamplesWithRetcode
rtin_RTIDDSConnector_getBooleanFromSamples.restype = ctypes.c_int
rtin_RTIDDSConnector_getBooleanFromSamples.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

rtin_RTIDDSConnector_getStringFromSamples = rti.RTIDDSConnector_getStringFromSamplesWithRetcode
rtin_RTIDDSConnector_getStringFromSamples.restype = ctypes.c_int
rtin_RTIDDSConnector_getStringFromSamples.argtypes = [ctypes.c_void_p, POINTER(c_char_p), ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

rtin_RTIDDSConnector_getAnyValueFromSamples = rti.RTIDDSConnector_getAnyValueFromSamples
rtin_RTIDDSConnector_getAnyValueFromSamples.restype = ctypes.c_int
rtin_RTIDDSConnector_getAnyValueFromSamples.argtypes = [ctypes.c_void_p, POINTER(c_double), POINTER(c_int), POINTER(c_char_p), POINTER(c_int), ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

rtin_RTIDDSConnector_getJSONSample = rti.RTIDDSConnector_getJSONSample
rtin_RTIDDSConnector_getJSONSample.restype = POINTER(c_char)
rtin_RTIDDSConnector_getJSONSample.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]

rtin_RTIDDSConnector_setJSONInstance = rti.RTIDDSConnector_setJSONInstance
rtin_RTIDDSConnector_setJSONInstance.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

rtin_RTIDDSConnector_getLastErrorMessage = rti.RTIDDSConnector_getLastErrorMessage
rtin_RTIDDSConnector_getLastErrorMessage.restype = POINTER(c_char)
rtin_RTIDDSConnector_getLastErrorMessage.argtypes = []

rtin_RTIDDSConnector_getNativeInstance = rti.RTIDDSConnector_getNativeInstance
rtin_RTIDDSConnector_getNativeInstance.restype = ctypes.c_void_p
rtin_RTIDDSConnector_getNativeInstance.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

rtin_RTIDDSConnector_freeString = rti.RTIDDSConnector_freeString
rtin_RTIDDSConnector_freeString.argtypes = [POINTER(c_char)]

#Python Class Definition

class Samples:
	def __init__(self,input):
		self.input = input

	def getLength(self):
		return int(rtin_RTIDDSConnector_getSamplesLength(self.input.connector.native,tocstring(self.input.name)))

	def getNumber(self, index, field_name):
		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")

		# Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		c_value = ctypes.c_double()
		retcode = rtin_RTIDDSConnector_getNumberFromSamples(
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
		retcode = rtin_RTIDDSConnector_getBooleanFromSamples(
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
		retcode = rtin_RTIDDSConnector_getStringFromSamples(
			self.input.connector.native,
			ctypes.byref(c_value),
			tocstring(self.input.name),
			index,
			tocstring(field_name))
		_check_retcode(retcode)
		if retcode == _ReturnCode.no_data:
			return None

		str_value = fromcstring(cast(c_value, c_char_p).value)
		rtin_RTIDDSConnector_freeString(c_value)

		return str_value

	def getDictionary(self, index):
		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		jsonStrPtr = rtin_RTIDDSConnector_getJSONSample(self.input.connector.native,tocstring(self.input.name),index)
		jsonStr = cast(jsonStrPtr, c_char_p).value
		myDict = json.loads(fromcstring(jsonStr))
		rtin_RTIDDSConnector_freeString((jsonStrPtr))
		return myDict

	def getNative(self,index):
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		dynDataPtr = rtin_RTIDDSConnector_getNativeSample(self.input.connector.native,tocstring(self.input.name),index)
		return dynDataPtr


class Infos:
	def __init__(self,input):
		self.input = input

	def getLength(self):
		return int(rtin_RTIDDSConnector_getInfosLength(self.input.connector.native,tocstring(self.input.name)))

	def isValid(self, index):
		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		return rtin_RTIDDSConnector_getBooleanFromInfos(self.input.connector.native,tocstring(self.input.name),index,tocstring('valid_data'))

	def getSampleIdentity(self, index):
		jsonStr = rtin_RTIDDSConnector_getJSONFromInfos(self.input.connector.native,tocstring(self.input.name),index,tocstring('sample_identity'))
		return json.loads(fromcstring(jsonStr))

	def getRelatedSampleIdentity(self, index):
		jsonStr = rtin_RTIDDSConnector_getJSONFromInfos(self.input.connector.native,tocstring(self.input.name),index,tocstring('related_sample_identity'))
		return json.loads(fromcstring(jsonStr))

class SampleIterator:
	"""Iterates and provides access to a data sample

	A SampleIterator provides access to the data recieved by an input.
	SampleIterators are returned by :meth:`Input.data_iterator()`,
	and :meth:`Input.get_sample()`; :meth:`Input.valid_data_iterator()` returns
	a subclass, :class:`ValidSampleIterator`.

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

	def __getitem__(self, field_name):
		number_value = ctypes.c_double()
		bool_value = ctypes.c_int()
		string_value = ctypes.c_char_p()
		selection = ctypes.c_int()
		retcode = rtin_RTIDDSConnector_getAnyValueFromSamples(
			self.input.connector.native,
			ctypes.byref(number_value),
			ctypes.byref(bool_value),
			ctypes.byref(string_value),
			ctypes.byref(selection),
			tocstring(self.input.name),
			self.index + 1,
			tocstring(field_name))
		_check_retcode(retcode)

		if retcode == _ReturnCode.no_data:
			return None

		if selection.value == 1:
			return number_value.value
		elif selection.value == 2:
			return bool_value.value
		elif selection.value == 3:
			python_str_value = fromcstring(cast(string_value, c_char_p).value)
			rtin_RTIDDSConnector_freeString(string_value)
			return python_str_value
		else:
			return None

	def get_dictionary(self):
		"""Gets a dictionary with the values of all the fields of this sample

		The dictionary keys are the field names and the dictionary values correspond
		to each field value. To see how nested types, sequences, and arrays are
		represented, see :ref:`Accessing the data`.

		:return: A dictionary containing all the fields of the sample.
		"""

		return self.input.samples.getDictionary(self.index)

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

	See :meth:`Input.valid_data_iterator`.
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
		self.native = rtin_RTIDDSConnector_getReader(self.connector.native,tocstring(self.name))
		if self.native is None:
			raise ValueError("Invalid Subscription::DataReader name")
		self.samples = Samples(self)
		self.infos = Infos(self)

	def read(self):
		"""Access the samples received by this Input

		This operation performs the same operation as :meth:`take()` except that
		the samples remain accessible.
		"""

		rtin_RTIDDSConnector_read(self.connector.native,tocstring(self.name))

	def take(self):
		"""Accesses the sample received by this Input

		After calling this method, the samples are accessible with
		:attr:`data_iterator`, :attr:`valid_data_iterator`, 
		or :meth:`get_sample()`.

		"""

		rtin_RTIDDSConnector_take(self.connector.native,tocstring(self.name))

	def wait(self,timeout):
		return rtin_RTIDDSConnector_wait(self.connector.native,timeout)

	def __getitem__(self, index):
		"""Equivalent to :meth:`get_sample()`"""

		return SampleIterator(self, index)

	@property
	def sample_count(self):
		"""Returns the number of samples available

		:return: The number of samples available since the last time read/take was called
		"""

		return self.samples.getLength()

	def get_sample(self, index):
		"""Returns an iterator to the sample in a given index

		Important: Calling :meth:`read()` or :meth:`take()` invalidates
		all iterators previously returned.

		The `Input` class also provides ``__getitem__``, making it possible to
		interchangeably write ``input[i]`` or ``input.get_sample(i)``

		:param number index: A zero-based index, less than :attr:`sample_count`.

		:return: An iterator that accesses the sample in the position indicated by ``index``.
		:rtype: :class:`SampleIterator`
		"""
		return SampleIterator(self, index)

	def __iter__(self):
		"""Equivalent to :attr:`data_iterator` """

		return SampleIterator(self)

	@property
	def data_iterator(self):
		"""Returns an iterator to the data samples

		The iterator provides access to all the data samples retrieved by the
		most-recent call to :meth:`read()` or :meth:`take()`.

		This iterator may return samples with invalid data. Use :attr:`valid_data_iterator`
		to access only samples with valid data.

		The `Input` class also provides ``__iter__``, making it possible to 
		interchangeably write ``for sample in input`` or 
		``for sample in input.data_iterator``.

		:return: An iterator to the samples
		:rtype: :class:`SampleIterator`
		"""
		return SampleIterator(self)

	@property
	def valid_data_iterator(self):
		"""Returns an iterator to the data samples with valid data

		The iterator provides access to the data samples retrieved by the
		most-recent call to :meth:`read()` or :meth:`take()`, and skips samples
		with invalid data (meta-data only).

		To access all samples, including those with meta-data only,
		use :attr:`data_iterator`

		By using this iterator, it is not necessary to check if each sample
		contains valid data.

		:return: An iterator to the data samples with valid
		:rtype: :class:`ValidSampleIterator`
		"""
		return ValidSampleIterator(self)

class Instance:
	"""A data sample

		Instance is the type of :class:`Output`.instance and is the object that
		is published.

		An Instance has an associated DDS Type, specified in the XML configuration,
		and it allows setting the values for the fields of the DDS Type.

		Attributes:
			* ``output`` (:class:`Output`): The ``Output`` that owns this ``Instance``.

		Special methods:
			* ``__setitem__``, see `:ref:`Accessing the data`.
	"""

	def __init__(self, output):
		self.output = output

	def clear_member(self, field_name):
		"""Resets a member to its default value

		The effect is the same as that of :meth:`Output.clear_members()` except
		that only one member is cleared.

		:param str field_name: The name of the field. It can be a complex member or a primitive member. See :ref:`Accessing the data`.
		"""

		retcode = rtin_RTIDDSConnector_clearMember(
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
		if isinstance(value, Number):
			self.set_number(field_name, value)
		elif isinstance(value, str):
			self.set_string(field_name, value)
		elif isinstance(value, bool):
			self.set_boolean(field_name, value)
		# elif isinstance(value, dict):
		# 	self.set_dictionary(field_name, value)
		else:
			raise TypeError("'{0}' is not a valid type for 'value'".format(type(value).__name__))

	def set_number(self, field_name, value):
		"""Sets a numeric field

		:param str field_name: The name of the field. See :ref:`Accessing the data`.
		:param number value: A numeric value or ``None`` to unset an optional member
		"""

		if value is None:
			self.clear_member(field_name)
		else:
			try:
				rtin_RTIDDSConnector_setNumberIntoSamples(
					self.output.connector.native,
					tocstring(self.output.name),
					tocstring(field_name),
					value)
			except ctypes.ArgumentError as e:
				raise TypeError("value for field '{0}' must be of a numeric type"\
					.format(field_name))

	# Deprecated: use set_number
	def setNumber(self, field_name, value):
		self.set_number(field_name, value)

	def set_boolean(self,field_name, value):
		"""Sets a Boolean field

		:param str field_name: The name of the field. See :ref:`Accessing the data`.
		:param number value: ``True`` or ``False``, or ``None`` to unset an optional member
		"""

		if value is None:
			self.clear_member(field_name)
		else:
			try:
				rtin_RTIDDSConnector_setBooleanIntoSamples(
						self.output.connector.native,
						tocstring(self.output.name),
						tocstring(field_name),
						value)
			except ctypes.ArgumentError as e:
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

		if value is None:
			self.clear_member(field_name)
		else:
			try:
				rtin_RTIDDSConnector_setStringIntoSamples(
					self.output.connector.native,
					tocstring(self.output.name),
					tocstring(field_name),
					tocstring(value))
			except AttributeError | ctypes.ArgumentError as e:
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
		rtin_RTIDDSConnector_setJSONInstance(self.output.connector.native,tocstring(self.output.name),tocstring(jsonStr))

	# Deprecated: use set_dictionary
	def setDictionary(self, dictionary):
		self.set_dictionary(dictionary)

	@property
	def native(self):
		"""Obtains the native C object

		This allows accessing additional *Connect DDS* APIs in C.
		"""

		dynDataPtr = rtin_RTIDDSConnector_getNativeInstance(self.output.connector.native,tocstring(self.output.name))
		return dynDataPtr

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
		self.native= rtin_RTIDDSConnector_getWriter(self.connector.native,tocstring(self.name))
		if self.native ==None:
			raise ValueError("Invalid Publication::DataWriter name")
		self.instance = Instance(self)

	def write(self, options=None):
		"""Publishes the values of the current``instance``

		Note that after writing the current ``instance``, its values remain
		unchanged. If for the next write you need to start from scratch, use
		:meth:`clear_members()`

		"""

		if options is not None:
			if isinstance(options, (dict)):
				jsonStr = json.dumps(options)
			else:
				jsonStr = options
			return rtin_RTIDDSConnector_write(self.connector.native,tocstring(self.name), tocstring(jsonStr))
		else:
			return rtin_RTIDDSConnector_write(self.connector.native,tocstring(self.name), None)

	def clear_members(self):
		"""Resets the values of the members of this ``Output.instance``

		If the member is defined with the ``default`` attribute, it gets that value.
		Otherwise numbers are set to 0, and strings are set to empty. Sequences
		are cleared. Optional members are set to ``None``.

		For example, if this ``Output``'s type is `ShapeType` (from the previous 
		example), then ``clear_members()`` sets `color` to "RED", `shapesize`
		to 30, and `x` and `y` to 0.
		"""

		return rtin_RTIDDSConnector_clear(self.connector.native,tocstring(self.name))

class Connector:
	"""Loads a configuration and creates its Inputs and Outputs

	A ``Connector`` instance loads a configuration from an XML document. For example::

		connector = rti.Connector("MyParticipantLibrary::MyParticipant", "MyExample.xml")

	After creating it, the ``Connector``'s Inputs can be used to read data, and
	the Outputs to write. See :meth:`get_input()` and :meth:`get_output()`.

	An application can create multiple ``Connector`` instances for the same or
	different configurations.

	A ``Connector`` instance must be deleted with :meth:`close()`.

	:param str configName: The configuration to load. 	The ``configName`` format is ``"LibraryName::ParticipantName"``, where ``LibraryName`` is the ``name`` attribute of a ``<domain_participant_library>`` tag, and ``ParticipantName`` is the ``name`` attribute of a ``<domain_participant>`` tag inside the library.
	:param str url: An URL locating the XML document. The ``url`` can be a file path (for example, ``'/tmp/my_dds_config.xml'``) or a string containing the full XML document with the following format ``'str://"<dds>...</dds>"'``)

	"""

	def __init__(self, configName, url):
		self.native = rtin_RTIDDSConnector_new(tocstring(configName), tocstring(url), None)
		if self.native is None:
			raise ValueError("Invalid participant profile, xml path or xml profile")

	def close(self):
		"""Frees all the resources created by this Connector instance"""

		rtin_RTIDDSConnector_delete(self.native)

	# Deprecated: use close()
	def delete(self):
		rtin_RTIDDSConnector_delete(self.native)

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

	def wait(self,timeout):
		"""TODO: document this function"""

		return rtin_RTIDDSConnector_wait(self.native,timeout)

@contextmanager
def open_connector(configName, url):
	"""A resource manager that creates and deletes a Connector

	It takes the sames arguments as the :class:`Connector` class::

		with rti.open_connector("MyParticipantLibrary::MyParticipant","./ShapeExample.xml") as connector:
			input = connector.get_input("SubscriberName::DataReaderName")
			# ...
		# connector closed after with block exits
	"""

	connector = Connector(configName, url)
	try:
		yield connector
	finally:
		connector.close()
