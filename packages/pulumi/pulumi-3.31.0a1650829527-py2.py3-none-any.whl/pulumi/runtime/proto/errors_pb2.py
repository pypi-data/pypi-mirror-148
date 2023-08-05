# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: errors.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="errors.proto",
    package="pulumirpc",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=b'\n\x0c\x65rrors.proto\x12\tpulumirpc"1\n\nErrorCause\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x12\n\nstackTrace\x18\x02 \x01(\tb\x06proto3',
)


_ERRORCAUSE = _descriptor.Descriptor(
    name="ErrorCause",
    full_name="pulumirpc.ErrorCause",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="message",
            full_name="pulumirpc.ErrorCause.message",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="stackTrace",
            full_name="pulumirpc.ErrorCause.stackTrace",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=27,
    serialized_end=76,
)

DESCRIPTOR.message_types_by_name["ErrorCause"] = _ERRORCAUSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ErrorCause = _reflection.GeneratedProtocolMessageType(
    "ErrorCause",
    (_message.Message,),
    {
        "DESCRIPTOR": _ERRORCAUSE,
        "__module__": "errors_pb2"
        # @@protoc_insertion_point(class_scope:pulumirpc.ErrorCause)
    },
)
_sym_db.RegisterMessage(ErrorCause)


# @@protoc_insertion_point(module_scope)
