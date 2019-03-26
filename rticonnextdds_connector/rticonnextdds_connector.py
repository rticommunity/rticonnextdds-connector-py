###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

import ctypes
import os
import sys
import weakref
import platform
import json

from ctypes import *
(bits, linkage)  = platform.architecture();
osname = platform.system();
isArm = platform.uname()[4].startswith("arm");

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
path = os.path.join(path, "..", "rticonnextdds-connector/lib", arch);
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

rtin_RTIDDSConnector_getNumberFromSamples = rti.RTIDDSConnector_getNumberFromSamples
rtin_RTIDDSConnector_getNumberFromSamples.restype = ctypes.c_double
rtin_RTIDDSConnector_getNumberFromSamples.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

rtin_RTIDDSConnector_getBooleanFromSamples = rti.RTIDDSConnector_getBooleanFromSamples
rtin_RTIDDSConnector_getBooleanFromSamples.restype = ctypes.c_int
rtin_RTIDDSConnector_getBooleanFromSamples.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

rtin_RTIDDSConnector_getStringFromSamples = rti.RTIDDSConnector_getStringFromSamples
rtin_RTIDDSConnector_getStringFromSamples.restype = POINTER(c_char)
rtin_RTIDDSConnector_getStringFromSamples.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]

rtin_RTIDDSConnector_getJSONSample = rti.RTIDDSConnector_getJSONSample
rtin_RTIDDSConnector_getJSONSample.restype = POINTER(c_char)
rtin_RTIDDSConnector_getJSONSample.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]

rtin_RTIDDSConnector_setJSONInstance = rti.RTIDDSConnector_setJSONInstance
rtin_RTIDDSConnector_setJSONInstance.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

rtin_RTIDDSConnector_getNativeInstance = rti.RTIDDSConnector_getNativeInstance
rtin_RTIDDSConnector_getNativeInstance.restype = ctypes.c_void_p
rtin_RTIDDSConnector_getNativeInstance.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

rtin_RTIDDSConnector_freeString = rti.RTIDDSConnector_freeString
rtin_RTIDDSConnector_freeString.argtypes = [POINTER(c_char)]

#Python Class Definition

class Samples:
	def __init__(self,input):
		self.input = input;

	def getLength(self):
		return int(rtin_RTIDDSConnector_getSamplesLength(self.input.connector.native,tocstring(self.input.name)));

	def getNumber(self, index, fieldName):
		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		return rtin_RTIDDSConnector_getNumberFromSamples(self.input.connector.native,tocstring(self.input.name),index,tocstring(fieldName));

	def getBoolean(self, index, fieldName):
		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		return rtin_RTIDDSConnector_getBooleanFromSamples(self.input.connector.native,tocstring(self.input.name),index,tocstring(fieldName));

	def getString(self, index, fieldName):
		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		theStrPtr = rtin_RTIDDSConnector_getStringFromSamples(self.input.connector.native,tocstring(self.input.name),index,tocstring(fieldName));
		theStr = fromcstring(cast(theStrPtr, c_char_p).value);
		rtin_RTIDDSConnector_freeString(theStrPtr);
		return theStr;

	def getDictionary(self,index):
		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		jsonStrPtr = rtin_RTIDDSConnector_getJSONSample(self.input.connector.native,tocstring(self.input.name),index);
		jsonStr = cast(jsonStrPtr, c_char_p).value
		myDict = json.loads(fromcstring(jsonStr))
		rtin_RTIDDSConnector_freeString((jsonStrPtr))
		return myDict;

	def getNative(self,index):
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		dynDataPtr = rtin_RTIDDSConnector_getNativeSample(self.input.connector.native,tocstring(self.input.name),index);
		return dynDataPtr;

class Infos:
	def __init__(self,input):
		self.input = input;

	def getLength(self):
		return int(rtin_RTIDDSConnector_getInfosLength(self.input.connector.native,tocstring(self.input.name)));

	def isValid(self, index):
		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		return rtin_RTIDDSConnector_getBooleanFromInfos(self.input.connector.native,tocstring(self.input.name),index,tocstring('valid_data'));

	def getSampleIdentity(self, index):
		jsonStr = rtin_RTIDDSConnector_getJSONFromInfos(self.input.connector.native,tocstring(self.input.name),index,tocstring('sample_identity'))
		return json.loads(fromcstring(jsonStr))

	def getRelatedSampleIdentity(self, index):
		jsonStr = rtin_RTIDDSConnector_getJSONFromInfos(self.input.connector.native,tocstring(self.input.name),index,tocstring('related_sample_identity'))
		return json.loads(fromcstring(jsonStr))

class Input:
	def __init__(self, connector, name):
		self.connector = connector;
		self.name = name;
		self.native= rtin_RTIDDSConnector_getReader(self.connector.native,tocstring(self.name))
		if self.native == None:
			raise ValueError("Invalid Subscription::DataReader name")
		self.samples = Samples(self);
		self.infos = Infos(self);

	def read(self):
		rtin_RTIDDSConnector_read(self.connector.native,tocstring(self.name));

	def take(self):
		rtin_RTIDDSConnector_take(self.connector.native,tocstring(self.name));

	def wait(self,timeout):
		return rtin_RTIDDSConnector_wait(self.connector.native,timeout);

class Instance:
	def __init__(self, output):
		self.output = output;

	def setNumber(self, fieldName, value):
		try:
			rtin_RTIDDSConnector_setNumberIntoSamples(self.output.connector.native,tocstring(self.output.name),tocstring(fieldName),value);
		except ctypes.ArgumentError as e:
			raise TypeError("field:{0} should be of type Numeric"\
				.format(fieldName))

	def setBoolean(self,fieldName, value):
		try:
			rtin_RTIDDSConnector_setBooleanIntoSamples(self.output.connector.native,tocstring(self.output.name),tocstring(fieldName),value);
		except ctypes.ArgumentError as e:
			raise TypeError("field:{0} should be of type Boolean"\
				.format(fieldName))

	def setString(self, fieldName, value):
		try:
			rtin_RTIDDSConnector_setStringIntoSamples(self.output.connector.native,tocstring(self.output.name),tocstring(fieldName),tocstring(value));
		except AttributeError | ctypes.ArgumentError as e:
			raise TypeError("field:{0} should be of type String"\
				.format(fieldName))

	def setDictionary(self,dictionary):
		jsonStr = json.dumps(dictionary)
		rtin_RTIDDSConnector_setJSONInstance(self.output.connector.native,tocstring(self.output.name),tocstring(jsonStr));

	def getNative(self):
		dynDataPtr = rtin_RTIDDSConnector_getNativeInstance(self.output.connector.native,tocstring(self.output.name));
		return dynDataPtr;


class Output:
	def __init__(self, connector, name):
		self.connector = connector;
		self.name = name;
		self.native= rtin_RTIDDSConnector_getWriter(self.connector.native,tocstring(self.name))
		if self.native ==None:
			raise ValueError("Invalid Publication::DataWriter name")
		self.instance = Instance(self);

	def write(self, options=None):
		if options is not None:
			if isinstance(options, (dict)):
				jsonStr = json.dumps(options)
			else:
				jsonStr = options
			return rtin_RTIDDSConnector_write(self.connector.native,tocstring(self.name), tocstring(jsonStr));
		else:
			return rtin_RTIDDSConnector_write(self.connector.native,tocstring(self.name), None);

	def clear_members(self):
		return rtin_RTIDDSConnector_clear(self.connector.native,tocstring(self.name));

class Connector:
	def __init__(self, configName, fileName):
		self.native = rtin_RTIDDSConnector_new(tocstring(configName), tocstring(fileName),None);
		if self.native == None:
			raise ValueError("Invalid participant profile, xml path or xml profile")

	def delete(self):
		rtin_RTIDDSConnector_delete(self.native);

	def getOutput(self, outputName):
		return Output(self,outputName);

	def getInput(self, inputName):
		return Input(self, inputName);

	def wait(self,timeout):
		return rtin_RTIDDSConnector_wait(self.native,timeout);
