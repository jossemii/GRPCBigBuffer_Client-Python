# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='test.proto',
  package='test',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\ntest.proto\x12\x04test\"Z\n\x04Test\x12\n\n\x02t1\x18\x01 \x01(\x0c\x12\n\n\x02t2\x18\x02 \x01(\x0c\x12\x1b\n\x02t3\x18\x03 \x01(\x0b\x32\n.test.TestH\x00\x88\x01\x01\x12\x16\n\x02t4\x18\x04 \x03(\x0b\x32\n.test.TestB\x05\n\x03_t3b\x06proto3'
)




_TEST = _descriptor.Descriptor(
  name='Test',
  full_name='test.Test',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='t1', full_name='test.Test.t1', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='t2', full_name='test.Test.t2', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='t3', full_name='test.Test.t3', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='t4', full_name='test.Test.t4', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='_t3', full_name='test.Test._t3',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=20,
  serialized_end=110,
)

_TEST.fields_by_name['t3'].message_type = _TEST
_TEST.fields_by_name['t4'].message_type = _TEST
_TEST.oneofs_by_name['_t3'].fields.append(
  _TEST.fields_by_name['t3'])
_TEST.fields_by_name['t3'].containing_oneof = _TEST.oneofs_by_name['_t3']
DESCRIPTOR.message_types_by_name['Test'] = _TEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Test = _reflection.GeneratedProtocolMessageType('Test', (_message.Message,), {
  'DESCRIPTOR' : _TEST,
  '__module__' : 'test_pb2'
  # @@protoc_insertion_point(class_scope:test.Test)
  })
_sym_db.RegisterMessage(Test)


# @@protoc_insertion_point(module_scope)