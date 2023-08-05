# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/grid/messages/association_messages.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# syft absolute
from syft.proto.core.common import (
    common_object_pb2 as proto_dot_core_dot_common_dot_common__object__pb2,
)
from syft.proto.core.io import address_pb2 as proto_dot_core_dot_io_dot_address__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n.proto/grid/messages/association_messages.proto\x12\x12syft.grid.messages\x1a%proto/core/common/common_object.proto\x1a\x1bproto/core/io/address.proto"\xbb\x02\n\x1dSendAssociationRequestMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x0e\n\x06source\x18\x03 \x01(\t\x12\x0e\n\x06target\x18\x04 \x01(\t\x12\'\n\x08reply_to\x18\x05 \x01(\x0b\x32\x15.syft.core.io.Address\x12Q\n\x08metadata\x18\x06 \x03(\x0b\x32?.syft.grid.messages.SendAssociationRequestMessage.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\xd3\x02\n ReceiveAssociationRequestMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12T\n\x08metadata\x18\x03 \x03(\x0b\x32\x42.syft.grid.messages.ReceiveAssociationRequestMessage.MetadataEntry\x12\x10\n\x08response\x18\x04 \x01(\t\x12\'\n\x08reply_to\x18\x05 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x0e\n\x06source\x18\x06 \x01(\t\x12\x0e\n\x06target\x18\x07 \x01(\t\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\xcc\x01\n RespondAssociationRequestMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x10\n\x08response\x18\x03 \x01(\t\x12\x0e\n\x06source\x18\x04 \x01(\t\x12\x0e\n\x06target\x18\x05 \x01(\t\x12\'\n\x08reply_to\x18\x06 \x01(\x0b\x32\x15.syft.core.io.Address"\xae\x01\n\x1cGetAssociationRequestMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x16\n\x0e\x61ssociation_id\x18\x03 \x01(\x05\x12\'\n\x08reply_to\x18\x04 \x01(\x0b\x32\x15.syft.core.io.Address"\x8f\x02\n\x1dGetAssociationRequestResponse\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12O\n\x07\x63ontent\x18\x02 \x03(\x0b\x32>.syft.grid.messages.GetAssociationRequestResponse.ContentEntry\x12&\n\x07\x61\x64\x64ress\x18\x03 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x0e\n\x06source\x18\x04 \x01(\t\x12\x0e\n\x06target\x18\x05 \x01(\t\x1a.\n\x0c\x43ontentEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\x97\x01\n\x1dGetAssociationRequestsMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\'\n\x08reply_to\x18\x04 \x01(\x0b\x32\x15.syft.core.io.Address"\xf6\x02\n\x1eGetAssociationRequestsResponse\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12V\n\x07\x63ontent\x18\x02 \x03(\x0b\x32\x45.syft.grid.messages.GetAssociationRequestsResponse.metadata_container\x12&\n\x07\x61\x64\x64ress\x18\x04 \x01(\x0b\x32\x15.syft.core.io.Address\x1a\xac\x01\n\x12metadata_container\x12\x65\n\x08metadata\x18\x01 \x03(\x0b\x32S.syft.grid.messages.GetAssociationRequestsResponse.metadata_container.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\xb1\x01\n\x1f\x44\x65leteAssociationRequestMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x16\n\x0e\x61ssociation_id\x18\x03 \x01(\x05\x12\'\n\x08reply_to\x18\x04 \x01(\x0b\x32\x15.syft.core.io.Addressb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "proto.grid.messages.association_messages_pb2", globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _SENDASSOCIATIONREQUESTMESSAGE_METADATAENTRY._options = None
    _SENDASSOCIATIONREQUESTMESSAGE_METADATAENTRY._serialized_options = b"8\001"
    _RECEIVEASSOCIATIONREQUESTMESSAGE_METADATAENTRY._options = None
    _RECEIVEASSOCIATIONREQUESTMESSAGE_METADATAENTRY._serialized_options = b"8\001"
    _GETASSOCIATIONREQUESTRESPONSE_CONTENTENTRY._options = None
    _GETASSOCIATIONREQUESTRESPONSE_CONTENTENTRY._serialized_options = b"8\001"
    _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER_METADATAENTRY._options = None
    _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER_METADATAENTRY._serialized_options = (
        b"8\001"
    )
    _SENDASSOCIATIONREQUESTMESSAGE._serialized_start = 139
    _SENDASSOCIATIONREQUESTMESSAGE._serialized_end = 454
    _SENDASSOCIATIONREQUESTMESSAGE_METADATAENTRY._serialized_start = 407
    _SENDASSOCIATIONREQUESTMESSAGE_METADATAENTRY._serialized_end = 454
    _RECEIVEASSOCIATIONREQUESTMESSAGE._serialized_start = 457
    _RECEIVEASSOCIATIONREQUESTMESSAGE._serialized_end = 796
    _RECEIVEASSOCIATIONREQUESTMESSAGE_METADATAENTRY._serialized_start = 407
    _RECEIVEASSOCIATIONREQUESTMESSAGE_METADATAENTRY._serialized_end = 454
    _RESPONDASSOCIATIONREQUESTMESSAGE._serialized_start = 799
    _RESPONDASSOCIATIONREQUESTMESSAGE._serialized_end = 1003
    _GETASSOCIATIONREQUESTMESSAGE._serialized_start = 1006
    _GETASSOCIATIONREQUESTMESSAGE._serialized_end = 1180
    _GETASSOCIATIONREQUESTRESPONSE._serialized_start = 1183
    _GETASSOCIATIONREQUESTRESPONSE._serialized_end = 1454
    _GETASSOCIATIONREQUESTRESPONSE_CONTENTENTRY._serialized_start = 1408
    _GETASSOCIATIONREQUESTRESPONSE_CONTENTENTRY._serialized_end = 1454
    _GETASSOCIATIONREQUESTSMESSAGE._serialized_start = 1457
    _GETASSOCIATIONREQUESTSMESSAGE._serialized_end = 1608
    _GETASSOCIATIONREQUESTSRESPONSE._serialized_start = 1611
    _GETASSOCIATIONREQUESTSRESPONSE._serialized_end = 1985
    _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER._serialized_start = 1813
    _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER._serialized_end = 1985
    _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER_METADATAENTRY._serialized_start = (
        407
    )
    _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER_METADATAENTRY._serialized_end = (
        454
    )
    _DELETEASSOCIATIONREQUESTMESSAGE._serialized_start = 1988
    _DELETEASSOCIATIONREQUESTMESSAGE._serialized_end = 2165
# @@protoc_insertion_point(module_scope)
