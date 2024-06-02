#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


# XML Injector version 2
# by Scumbumbo @ MTS
#
# The version module contains functions to test the XML Injector version and display a dialog
# for any mods that require a specific version of the injector.
#
# This mod is intended as a standard for modder's to use as a shared library.  Please do not
# distribute any modifications anywhere other than the mod's main download site.  Modification
# suggestions and bug notices should be communicated to the maintainer, currently Scumbumbo at
# the Mod The Sims website - http://modthesims.info/member.php?u=7401825
#


from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification

from xml_injector.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class Version:

    XML_INJECTOR_VERSION = 4
    MAX_REQUESTED_VERSION = XML_INJECTOR_VERSION
    SHOW_ERROR_DIALOG = False

    @staticmethod
    def get_version():
        return Version.XML_INJECTOR_VERSION

    @staticmethod
    def request_version(version, custom_error_dialog):
        if version > Version.XML_INJECTOR_VERSION:
            log.error(f'Version {version} of XML Injector required by snippet. Snippet may not load or operate correctly with XML Injector {Version.XML_INJECTOR_VERSION}.')
            if version > Version.MAX_REQUESTED_VERSION:
                Version.MAX_REQUESTED_VERSION = version

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def handle_event(event_data: S4CLZoneLateLoadEvent):
        if Version.XML_INJECTOR_VERSION < Version.MAX_REQUESTED_VERSION:
            CommonBasicNotification(
                'XML Injector Version',
                f'One of your installed mods require version {Version.MAX_REQUESTED_VERSION} of the XML Injector (version {Version.XML_INJECTOR_VERSION}). Please update the XML Injector.',
            ).show()
            # don't show message again
            Version.MAX_REQUESTED_VERSION = Version.XML_INJECTOR_VERSION
