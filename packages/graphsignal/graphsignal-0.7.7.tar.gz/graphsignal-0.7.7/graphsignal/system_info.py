import logging
import os
import sys
import platform
import socket
import re

from graphsignal.proto import profiles_pb2
from graphsignal import version

logger = logging.getLogger('graphsignal')

OS_LINUX = (sys.platform.startswith('linux'))
OS_DARWIN = (sys.platform == 'darwin')
OS_WIN = (sys.platform == 'win32')

version_regexp = re.compile('^(\\d+)\\.?(\\d+)?\\.?(\\d+)?')


def parse_semver(semver_proto, version):
    version_match = version_regexp.match(str(version))
    if version_match is not None:
        groups = version_match.groups()
        if groups[0] is not None:
            semver_proto.major = int(groups[0])
        if groups[1] is not None:
            semver_proto.minor = int(groups[1])
        if groups[2] is not None:
            semver_proto.patch = int(groups[2])


def compare_semver(semver_proto, version):
    semver_int = semver_proto.major * 1e6 + \
        semver_proto.minor * 1e3 + semver_proto.patch
    version_int = version[0] * 1e6 + version[1] * 1e3 + version[2]
    if semver_int < version_int:
        return -1
    if semver_int > version_int:
        return 1
    else:
        return 0


def _read_run_env():
    run_env = profiles_pb2.RunEnvironment()

    try:
        run_env.platform = sys.platform
        run_env.machine = platform.machine()
        if not OS_WIN:
            run_env.os_name = os.uname().sysname
            run_env.os_version = os.uname().release
        run_env.runtime = profiles_pb2.RunEnvironment.Runtime.PYTHON
        run_env.runtime_version.major = sys.version_info.major
        run_env.runtime_version.minor = sys.version_info.minor
        run_env.runtime_version.patch = sys.version_info.micro
        run_env.runtime_impl = platform.python_implementation()
        parse_semver(run_env.profiler_version, version.__version__)
    except BaseException:
        logger.error(
            'Error reading run environment information',
            exc_info=True)

    return run_env


cached_run_env = _read_run_env()
