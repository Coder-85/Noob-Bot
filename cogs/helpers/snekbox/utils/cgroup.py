import logging
from pathlib import Path

from cogs.helpers.snekbox.config_pb2 import NsJailConfig

log = logging.getLogger(__name__)


def get_version(config: NsJailConfig) -> int:
    """
    Examine the filesystem and return the guessed cgroup version.

    Fall back to use_cgroupv2 in the NsJail config if either both v1 and v2 seem to be enabled,
    or neither seem to be enabled.
    """
    cgroup_mounts = (
        config.cgroup_mem_mount,
        config.cgroup_pids_mount,
        config.cgroup_net_cls_mount,
        config.cgroup_cpu_mount
    )
    v1_exists = any(Path(mount).exists() for mount in cgroup_mounts)

    controllers_path = Path(config.cgroupv2_mount, "cgroup.controllers")
    v2_exists = controllers_path.exists()

    config_version = 2 if config.use_cgroupv2 else 1

    if v1_exists and v2_exists:
        # Probably hybrid mode. Use whatever is set in the config.
        return config_version
    elif v1_exists:
        if config_version == 2:
            log.warning(
                "NsJail is configured to use cgroupv2, but only cgroupv1 was detected on the "
                "system. Either use_cgroupv2 or cgroupv2_mount is incorrect. Snekbox is unable "
                "to override use_cgroupv2. If NsJail has been configured to use cgroups, then "
                "it will fail. In such case, please correct the config manually."
            )
        return 1
    elif v2_exists:
        return 2
    else:
        log.warning(
            f"Neither the cgroupv1 controller mounts, nor {str(controllers_path)!r} exists. "
            "Either cgroup_xxx_mount and cgroupv2_mount are misconfigured, or all "
            "corresponding v1 controllers are disabled on the system. "
            "Falling back to the use_cgroupv2 NsJail setting."
        )
        return config_version


def init(config: NsJailConfig) -> int:
    """Determine the cgroup version, initialise the cgroups for NsJail, and return the version."""
    version = get_version(config)

    return version