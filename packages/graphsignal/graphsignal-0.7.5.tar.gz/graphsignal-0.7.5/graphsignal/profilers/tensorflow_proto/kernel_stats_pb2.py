# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: graphsignal/profilers/tensorflow_proto/kernel_stats.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n9graphsignal/profilers/tensorflow_proto/kernel_stats.proto\x12\x13tensorflow.profiler\"\xeb\x02\n\x0cKernelReport\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1c\n\x14registers_per_thread\x18\x02 \x01(\r\x12\x1a\n\x12static_shmem_bytes\x18\x03 \x01(\r\x12\x1b\n\x13\x64ynamic_shmem_bytes\x18\x04 \x01(\r\x12\x11\n\tblock_dim\x18\x05 \x03(\r\x12\x10\n\x08grid_dim\x18\x06 \x03(\r\x12\x19\n\x11total_duration_ns\x18\x07 \x01(\x04\x12\x17\n\x0fmin_duration_ns\x18\x08 \x01(\x04\x12\x17\n\x0fmax_duration_ns\x18\t \x01(\x04\x12#\n\x1bis_kernel_using_tensor_core\x18\n \x01(\x08\x12\"\n\x1ais_op_tensor_core_eligible\x18\x0b \x01(\x08\x12\x0f\n\x07op_name\x18\x0c \x01(\t\x12\x13\n\x0boccurrences\x18\r \x01(\r\x12\x15\n\roccupancy_pct\x18\x0e \x01(\x02\"C\n\rKernelStatsDb\x12\x32\n\x07reports\x18\x01 \x03(\x0b\x32!.tensorflow.profiler.KernelReportb\x06proto3')



_KERNELREPORT = DESCRIPTOR.message_types_by_name['KernelReport']
_KERNELSTATSDB = DESCRIPTOR.message_types_by_name['KernelStatsDb']
KernelReport = _reflection.GeneratedProtocolMessageType('KernelReport', (_message.Message,), {
  'DESCRIPTOR' : _KERNELREPORT,
  '__module__' : 'graphsignal.profilers.tensorflow_proto.kernel_stats_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.profiler.KernelReport)
  })
_sym_db.RegisterMessage(KernelReport)

KernelStatsDb = _reflection.GeneratedProtocolMessageType('KernelStatsDb', (_message.Message,), {
  'DESCRIPTOR' : _KERNELSTATSDB,
  '__module__' : 'graphsignal.profilers.tensorflow_proto.kernel_stats_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.profiler.KernelStatsDb)
  })
_sym_db.RegisterMessage(KernelStatsDb)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _KERNELREPORT._serialized_start=83
  _KERNELREPORT._serialized_end=446
  _KERNELSTATSDB._serialized_start=448
  _KERNELSTATSDB._serialized_end=515
# @@protoc_insertion_point(module_scope)
