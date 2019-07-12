###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.	   #
# No duplications, whole or partial, manual or electronic, may be made		#
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.										 #
# This code contains trade secrets of Real-Time Innovations, Inc.			 #
###############################################################################

"""This package contains the Connector type and all other supporting types

To use this package, import it as follows:

.. code:: py

   import rticonnextdds_connector as rti

"""

import ctypes
import os
import sys
import weakref
import platform
import json

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
	"""A collection of data samples"""

	def __init__(self,input):
		self.input = input;

	def getLength(self):
		"""Gets the number of samples"""

		return int(rtin_RTIDDSConnector_getSamplesLength(self.input.connector.native,tocstring(self.input.name)));

	def getNumber(self, index, fieldName):
		"""Gets the value of a numeric field for a given sample index"""

		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		return rtin_RTIDDSConnector_getNumberFromSamples(self.input.connector.native,tocstring(self.input.name),index,tocstring(fieldName));

	def getBoolean(self, index, fieldName):
		"""Gets the value of a boolean field for a given sample index"""

		if type(index) is not int:
			raise ValueError("index must be an integer")
		if index < 0:
			raise ValueError("index must be positive")
		#Adding 1 to index because the C API was based on Lua where indexes start from 1
		index = index + 1
		return rtin_RTIDDSConnector_getBooleanFromSamples(self.input.connector.native,tocstring(self.input.name),index,tocstring(fieldName));

	def getString(self, index, fieldName):
		"""Gets the value of a string field for a given sample index"""

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
		"""Gets a dictionary with the values of all the fields for a given sample index"""

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
	"""A collection of meta-data"""

	def __init__(self,input):
		self.input = input;

	def getLength(self):
		"""Gets the number of samples"""

		return int(rtin_RTIDDSConnector_getInfosLength(self.input.connector.native,tocstring(self.input.name)));

	def isValid(self, index):
		"""Returns whether the data for a given sample index is valid"""

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
	"""Allows reading data for a Topic

	To get an input object, use :meth:`Connector.getInput()`.
	"""

	def __init__(self, connector, name):
		self.connector = connector;
		self.name = name;
		self.native= rtin_RTIDDSConnector_getReader(self.connector.native,tocstring(self.name))
		if self.native == None:
			raise ValueError("Invalid Subscription::DataReader name")
		self.samples = Samples(self);
		self.infos = Infos(self);

	def read(self):
		"""TODO: document this function"""

		rtin_RTIDDSConnector_read(self.connector.native,tocstring(self.name));

	def take(self):
		"""TODO: document this function"""

		rtin_RTIDDSConnector_take(self.connector.native,tocstring(self.name));

	def wait(self,timeout):
		return rtin_RTIDDSConnector_wait(self.connector.native,timeout);

class Instance:
	"""TODO: Instance"""

	def __init__(self, output):
		self.output = output;

	def setNumber(self, fieldName, value):
		"""TODO: document this function"""

		try:
			rtin_RTIDDSConnector_setNumberIntoSamples(self.output.connector.native,tocstring(self.output.name),tocstring(fieldName),value);
		except ctypes.ArgumentError as e:
			raise TypeError("field:{0} should be of type Numeric"\
				.format(fieldName))

	def setBoolean(self,fieldName, value):
		"""TODO: document this function"""

		try:
			rtin_RTIDDSConnector_setBooleanIntoSamples(self.output.connector.native,tocstring(self.output.name),tocstring(fieldName),value);
		except ctypes.ArgumentError as e:
			raise TypeError("field:{0} should be of type Boolean"\
				.format(fieldName))

	def setString(self, fieldName, value):
		"""TODO: document this function"""

		try:
			rtin_RTIDDSConnector_setStringIntoSamples(self.output.connector.native,tocstring(self.output.name),tocstring(fieldName),tocstring(value));
		except AttributeError | ctypes.ArgumentError as e:
			raise TypeError("field:{0} should be of type String"\
				.format(fieldName))

	def setDictionary(self,dictionary):
		"""TODO: document this function"""

		jsonStr = json.dumps(dictionary)
		rtin_RTIDDSConnector_setJSONInstance(self.output.connector.native,tocstring(self.output.name),tocstring(jsonStr));

	def getNative(self):
		"""TODO: document this function"""

		dynDataPtr = rtin_RTIDDSConnector_getNativeInstance(self.output.connector.native,tocstring(self.output.name));
		return dynDataPtr;


class Output:
	"""Allows writting data for a DDS Topic

	To obtain an Output, use :meth:`Connector.getOutput()`.

	Use the attribute ``instance`` to set the values of the data sample you want
	to write. For example::

		output.instance.setNumber("x", 1)
		output.instance.setNumber("y", 2)
		output.instance.setNumber("shapesize", 30)
		output.instance.setString("color", "BLUE")

	The members of ``instance`` are pre-defined in the XML configuration. In the previous
	example, the type is defined as::

		<types>
		  <struct name="ShapeType" extensibility="extensible">
		    <member name="color" stringMaxLength="128" id="0" type="string" key="true" default="RED"/>
			<member name="x" id="1" type="long" />
			<member name="y" id="2" type="long" />
			<member name="shapesize" id="3" type="long" default="30"/>
		   </struct>
		</types>

	If the name of the member you try to access doesn't exist, TODO: raise exception.

	After that, call :meth:`write()` to publish the instance::

		output.write()

	To publish a new data sample, modify ``instance`` (call :meth:`clear_members()`
	if you need to start from scratch) and call ``write()`` again.

	Attributes:
		* ``instance`` (:class:`Instance`): The data that is written when :meth:`write()` is called.
		* ``native``: A native handle that allows accessing additional *Connext DDS* APIs in C.
		* ``name`` (str): The name of this ``Output`` (the name used in :meth:`Connector.getOutput`)

	"""

	def __init__(self, connector, name):
		self.connector = connector;
		self.name = name;
		self.native= rtin_RTIDDSConnector_getWriter(self.connector.native,tocstring(self.name))
		if self.native ==None:
			raise ValueError("Invalid Publication::DataWriter name")
		self.instance = Instance(self);

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
			return rtin_RTIDDSConnector_write(self.connector.native,tocstring(self.name), tocstring(jsonStr));
		else:
			return rtin_RTIDDSConnector_write(self.connector.native,tocstring(self.name), None);

	def clear_members(self):
		"""Resets the values of the members of this ``Output.instance``

		If the member is defined with the ``default`` attribute, it gets that value.
		Otherwise numbers are set to 0, and strings are set to empty. Sequences
		are cleared.

		For example, if this ``Output``'s type is `ShapeType` (from the previous 
		example), then ``clear_members()`` sets `color` to "RED", `shapesize`
		to 30, and `x` and `y` to 0.
		"""

		return rtin_RTIDDSConnector_clear(self.connector.native,tocstring(self.name));

class Connector:
	"""Loads a configuration and creates its Inputs and Outputs

	A ``Connector`` instance loads a configuration from an XML document. For example::

		connector = rti.Connector("MyParticipantLibrary::MyParticipant", "MyExample.xml")

	This example loads the domain_participant called Zero defined in the file
	ShapeExample.xml::

		<domain_participant_library name="MyParticipantLibrary">
		  <domain_participant name="MyParticipant" domain_ref="MyDomainLibrary::MyDomain">
		    ...
		  </domain_participant>
		</domain_participant_library>

	*Connector* uses The XML format of `RTI's XML-Based Application Creation <https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds/xml_application_creation/html_files/RTI_ConnextDDS_CoreLibraries_XML_AppCreation_GettingStarted/index.htm#XMLBasedAppCreation/UnderstandingPrototyper/XMLTagsConfigEntities.htm%3FTocPath%3D5.%2520Understanding%2520XML-Based%2520Application%2520Creation%7C5.5%2520XML%2520Tags%2520for%2520Configuring%2520Entities%7C_____0>`__.

	After creating it, the ``Connector``'s Inputs can be used to read data, and
	the Outputs to write. See :meth:`getInput()` and :meth:`getOutput()`.

	An application can create multiple ``Connector`` instances for the same or
	different configurations.

	A ``Connector`` instance must be deleted with :meth:`delete()`.

	:param str configName: The configuration to load. 	The ``configName`` format is ``"LibraryName::ParticipantName"``, where ``LibraryName`` is the ``name`` attribute of a ``<domain_participant_library>`` tag, and ``ParticipantName`` is the ``name`` attribute of a ``<domain_participant>`` tag inside the library.
	:param str url: An URL locating the XML document. The ``url`` can be a file path (for example, ``'/tmp/my_dds_config.xml'``) or a string containing the full XML document with the following format ``'str://"<dds>...</dds>"'``)

	"""

	def __init__(self, configName, url):
		self.native = rtin_RTIDDSConnector_new(tocstring(configName), tocstring(url), None)
		if self.native == None:
			raise ValueError("Invalid participant profile, xml path or xml profile")

	def delete(self):
		"""Frees all the resources created by this Connector instance"""

		rtin_RTIDDSConnector_delete(self.native);

	def getOutput(self, outputName):
		"""Returns the :class:`Output` named ``outputName``

		``outputName`` identifies a ``<data_writer>`` tag in the
		configuration loaded by this ``Connector``. For example, the following code::

			connector = rti.Connector("MyParticipantLibrary::MyParticipant", "MyExample.xml")
			connector.getOutput("MyPublisher::MyWriter")


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

		:param str outputName: The name of a the ``data_writer`` to load, with the format ``"PublisherName::DataWriterName"``.
		:return: The Output if it exists, or else it raises ``ValueError``.
		:rtype: :class:`Output`

		"""

		return Output(self,outputName);

	def getInput(self, inputName):
		"""Returns the :class:`Input` named ``inputName``

		``inputName`` identifies a ``<data_reader>`` tag in the
		configuration loaded by this ``Connector``. For example, the following code::

			connector = rti.Connector("MyParticipantLibrary::MyParticipant", "MyExample.xml")
			connector.getInput("MySubscriber::MyReader")


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

		:param str inputName: The name of a the ``data_reader`` to load, with the format ``"SubscriberName::DataReaderName"``.
		:return: The Input if it exists, or else it raises ``ValueError``.
		:rtype: :class:`Input`

		"""

		return Input(self, inputName);

	def wait(self,timeout):
		"""TODO: document this function"""

		return rtin_RTIDDSConnector_wait(self.native,timeout);
