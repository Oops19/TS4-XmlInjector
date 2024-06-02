#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


# XML Injector version 2
# by Scumbumbo @ MTS
#
# The detection module is used to turn off the DramaNode which is used to detect the absence
# of XML Injector.  By disabling that drama node the game will not alert players that they need
# to download XML Injector.
#
# This mod is intended as a standard for modder's to use as a shared library.  Please do not
# distribute any modifications anywhere other than the mod's main download site.  Modification
# suggestions and bug notices should be communicated to the maintainer, currently Scumbumbo at
# the Mod The Sims website - http://modthesims.info/member.php?u=7401825
#


import services
import sims4.log
from sims4.resources import Types

from xml_injector.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class Detection:
    DETECTION_DRAMA_NODE = 15419684579670968912

    @staticmethod
    def disable_drama_node(self):
        key = sims4.resources.get_resource_key(Detection.DETECTION_DRAMA_NODE, Types.DRAMA_NODE)
        drama_node = self.get(key)
        if drama_node is not None:
            sim_info_test = drama_node.pretests[0][0]
            sim_info_test.has_been_played = False
            sim_info_test.npc = True
            sim_info_test.is_active_sim = True
            log.info(f'Detection drama node has been disabled')


services.get_instance_manager(Types.DRAMA_NODE).add_on_load_complete(Detection().disable_drama_node)
