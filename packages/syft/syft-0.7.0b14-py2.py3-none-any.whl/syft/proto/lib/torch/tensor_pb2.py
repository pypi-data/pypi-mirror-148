# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/lib/torch/tensor.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# syft absolute
from syft.proto.lib.torch import device_pb2 as proto_dot_lib_dot_torch_dot_device__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1cproto/lib/torch/tensor.proto\x12\x0esyft.lib.torch\x1a\x1cproto/lib/torch/device.proto"\xe1\x02\n\x0fProtobufContent\x12\r\n\x05shape\x18\x01 \x03(\x03\x12\x16\n\x0e\x63ontents_uint8\x18\x10 \x03(\r\x12\x15\n\rcontents_int8\x18\x11 \x03(\x05\x12\x16\n\x0e\x63ontents_int16\x18\x12 \x03(\x05\x12\x16\n\x0e\x63ontents_int32\x18\x13 \x03(\x05\x12\x16\n\x0e\x63ontents_int64\x18\x14 \x03(\x03\x12\x18\n\x10\x63ontents_float16\x18\x15 \x03(\x02\x12\x18\n\x10\x63ontents_float32\x18\x16 \x03(\x02\x12\x18\n\x10\x63ontents_float64\x18\x17 \x03(\x01\x12\x15\n\rcontents_bool\x18\x18 \x03(\x08\x12\x16\n\x0e\x63ontents_qint8\x18\x19 \x03(\x11\x12\x17\n\x0f\x63ontents_quint8\x18\x1a \x03(\r\x12\x17\n\x0f\x63ontents_qint32\x18\x1b \x03(\x11\x12\x19\n\x11\x63ontents_bfloat16\x18\x1c \x03(\x02"\x88\x01\n\nTensorData\x12\x14\n\x0cis_quantized\x18\x01 \x01(\x08\x12\r\n\x05scale\x18\x02 \x01(\x01\x12\x12\n\nzero_point\x18\x03 \x01(\x05\x12\x14\n\nproto_data\x18\x04 \x01(\x0cH\x00\x12\x14\n\narrow_data\x18\x05 \x01(\x0cH\x00\x12\r\n\x05\x64type\x18\x06 \x01(\tB\x06\n\x04\x64\x61ta"j\n\x0bTensorProto\x12\x0e\n\x06tensor\x18\x01 \x01(\x0c\x12\x15\n\rrequires_grad\x18\x02 \x01(\x08\x12\x0c\n\x04grad\x18\x03 \x01(\x0c\x12&\n\x06\x64\x65vice\x18\x04 \x01(\x0b\x32\x16.syft.lib.torch.Deviceb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "proto.lib.torch.tensor_pb2", globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _PROTOBUFCONTENT._serialized_start = 79
    _PROTOBUFCONTENT._serialized_end = 432
    _TENSORDATA._serialized_start = 435
    _TENSORDATA._serialized_end = 571
    _TENSORPROTO._serialized_start = 573
    _TENSORPROTO._serialized_end = 679
# @@protoc_insertion_point(module_scope)
