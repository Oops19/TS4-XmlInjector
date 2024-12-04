#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


# XML Injector version 2
# by Scumbumbo @ MTS
#
# The snippet module defines the tuning classes to load the XmlInjector snippet XML.  Once
# the tuning has been loaded by the game, the _tuning_loaded_callback invokes the functions
# in the add_to_tuning module to process the affordance additions.
#
# This mod is intended as a standard for modder's to use as a shared library.  Please do not
# distribute any modifications anywhere other than the mod's main download site.  Modification
# suggestions and bug notices should be communicated to the maintainer, currently Scumbumbo at
# the Mod The Sims website - http://modthesims.info/member.php?u=7401825
#

# ----------
# September 5th, 2019 patch broke some of the injections. Per the guidance of Deaderpool, the patch changed how ImmutableSlots can be accessed, such that, for example, "entry['object_selection']" needs to be "entry.object_selection"
# This appears to be the cause of some injections not working.
# I've made changes in the _tuning_loaded_callback method to reflect this and verified most injections working again, since Scumbumbo was not around to fix it (a few were not explicitly tested, but are assumed to be working).
# In keeping with the requested official distribution channels, I'm posting the fixed version in the comments of the mod's official page on Mod The Sims website.
# - Triplis
# ----------

# source file: snippet.py - split into object_selection.py and xml_injector.py


import services
from xml_injector.modinfo import ModInfo
from objects.definition_manager import DefinitionManager
from sims4.tuning.tunable import AutoFactoryInit, HasTunableSingletonFactory, Tunable, TunableList, TunableReference, TunableVariant, TunableEnumEntry
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from tag import Tag


log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class ObjectSelection(TunableVariant):
    # object_list variant
    class _ObjectList(HasTunableSingletonFactory, AutoFactoryInit):
        FACTORY_TUNABLES = {
            'object_list': TunableList(
                description='A list of objects to add the interactions to',
                tunable=Tunable(
                    description='Reference to an object tuning instance',
                    tunable_type=int,
                    default=None)
            )
        }

        def get_objects(self):
            # Get the object tunings for each of the objects in the object list
            # from the DefinitionManager
            definition_manager = services.definition_manager()
            obj_list = []
            for obj_id in self.object_list:
                # get() on the DefinitionManager will return an object definition,
                # to get an actual tuning by ID, we need to call the super()
                tun = super(DefinitionManager, definition_manager).get(obj_id)
                if tun:
                    if hasattr(tun, '_super_affordances'):
                        obj_list.append(tun)
            return obj_list

    # objects_with_affordance variant
    class _ObjectsWithAffordance(HasTunableSingletonFactory, AutoFactoryInit):
        FACTORY_TUNABLES = {
            'affordance': TunableReference(
                description='Reference to an interaction tuning instance',
                manager=services.affordance_manager(),
                class_restrictions=('SuperInteraction',),
                allow_none=False,
                pack_safe=True)
        }

        def get_objects(self):
            # Iterate through all object tunings from the DefinitionManager
            # and return those that contain the referenced affordance
            definition_manager = services.definition_manager()
            obj_list = []
            for tun in definition_manager._tuned_classes.values():
                if hasattr(tun, '_super_affordances') and self.affordance in tun._super_affordances:
                    obj_list.append(tun)
            return obj_list

    # objects_matching_name variant
    class _ObjectsMatchingName(HasTunableSingletonFactory, AutoFactoryInit):
        FACTORY_TUNABLES = {
            'partial_name': Tunable(
                description='A string specifying the partial name of objects to select',
                tunable_type=str,
                default=None)
        }

        def get_objects(self):
            # Iterate through all object tunings from the DefinitionManager
            # and return those whose name contains the partial_name
            obj_list = []
            if not isinstance(self.partial_name, str):
                log.error('Tuning error, missing or invalid partial_name')
            else:
                definition_manager = services.definition_manager()
                for tun in definition_manager._tuned_classes.values():
                    if hasattr(tun, '__name__') and self.partial_name in tun.__name__:
                        obj_list.append(tun)
            return obj_list

    # objects_with_tag variant
    class _ObjectsWithTag(HasTunableSingletonFactory, AutoFactoryInit):
        FACTORY_TUNABLES = {
            'tag': TunableEnumEntry(
                description='A tag to search for object selection.',
                tunable_type=Tag,
                default=Tag.INVALID)
        }

        def get_objects(self):
            obj_set = set()
            definition_manager = services.definition_manager()
            definition_manager.refresh_build_buy_tag_cache(refresh_definition_cache=False)
            for defn in definition_manager.get_definitions_for_tags_gen((self.tag,)):
                obj_set.add(defn.cls)
            return list(obj_set)

    # Create a variant for the object_selection
    def __init__(self, **kwargs):
        super().__init__(
            object_list=ObjectSelection._ObjectList.TunableFactory(),
            objects_with_affordance=ObjectSelection._ObjectsWithAffordance.TunableFactory(),
            objects_matching_name=ObjectSelection._ObjectsMatchingName.TunableFactory(),
            objects_with_tag=ObjectSelection._ObjectsWithTag.TunableFactory(),
            default=None,
            **kwargs)
