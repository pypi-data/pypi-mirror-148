#!/usr/bin/python
from cloudshell.shell.flows.configuration.basic_flow import AbstractConfigurationFlow
from cloudshell.shell.flows.utils.networking_utils import UrlParser

from cloudshell.nvidia.onyx.command_actions.system_actions import SystemActions
from cloudshell.nvidia.onyx.helpers.exceptions import NvidiaSaveRestoreException


class NvidiaConfigurationFlow(AbstractConfigurationFlow):
    STARTUP_CONFIG_NAME = "startup_config"
    STARTUP_LOCATION = "nvram:startup_config"
    REMOTE_PROTOCOLS = ["ftp", "tftp", "scp"]
    DEFAULT_CONFIG_NAME = ""
    ACTIVE_CONFIG_NAME = "active"

    def __init__(self, cli_handler, resource_config, logger):
        super().__init__(logger, resource_config)
        self._cli_handler = cli_handler

    @property
    def _file_system(self):
        return ""

    def _save_flow(self, folder_path, configuration_type, vrf_management_name=None):
        """Execute flow which save selected file to the provided destination.

        :param folder_path: destination path where file will be saved
        :param configuration_type: source file, which will be saved
        :param vrf_management_name: Virtual Routing and Forwarding Name
        :return: saved configuration file name
        """
        if not configuration_type.endswith("-config"):
            configuration_type += "-config"

        if configuration_type not in ["running-config"]:
            raise NvidiaSaveRestoreException(
                "Device doesn't support saving '{}' configuration type".format(
                    configuration_type
                ),
            )

        url = UrlParser().parse_url(folder_path)
        scheme = url.get("scheme")
        avail_protocols = self.REMOTE_PROTOCOLS
        if scheme and scheme not in avail_protocols:
            raise NvidiaSaveRestoreException(
                f"Unsupported protocol type {scheme}."
                f"Available protocols: {avail_protocols}"
            )
        with self._cli_handler.get_cli_service(
            self._cli_handler.config_mode
        ) as config_session:
            save_action = SystemActions(config_session, self._logger)
            if scheme:
                save_action.upload(
                    self.ACTIVE_CONFIG_NAME,
                    folder_path,
                    vrf=vrf_management_name,
                )

    def _restore_flow(
        self, path, configuration_type, restore_method, vrf_management_name
    ):
        """Execute flow which save selected file to the provided destination.

        :param path: the path to the configuration file, including the configuration
            file name
        :param restore_method: the restore method to use when restoring the
            configuration file. Possible Values are append and override
        :param configuration_type: the configuration type to restore.
            Possible values are startup and running
        :param vrf_management_name: Virtual Routing and Forwarding Name
        """
        if "-config" not in configuration_type:
            configuration_type += "-config"

        with self._cli_handler.get_cli_service(
            self._cli_handler.config_mode
        ) as config_session:
            restore_action = SystemActions(config_session, self._logger)
            url = UrlParser().parse_url(path)
            scheme = url.get("scheme")
            filename = url.get("filename", self.DEFAULT_CONFIG_NAME)
            avail_protocols = self.REMOTE_PROTOCOLS + [self._file_system]
            if scheme not in avail_protocols:
                raise NvidiaSaveRestoreException(
                    f"Unsupported protocol type {scheme}."
                    f"Available protocols: {avail_protocols}"
                )
            if "startup" in configuration_type:
                raise NvidiaSaveRestoreException(
                    "Nvidia Onyx doesn't have startup configuration"
                )

            restore_action.download(path)
            if restore_method == "override":
                restore_action.override_running(filename=filename)
            else:
                restore_action.generate_txt_config(filename=filename)
                restore_action.apply_txt_config(filename=filename)
                restore_action.delete_config(filename)
                restore_action.delete_config(f"{filename}.txt")
