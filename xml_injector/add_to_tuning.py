#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


# XML Injector version 2
# by Scumbumbo @ MTS
#
# Functions in the add_to_tuning module are called by the snippet's _tuning_loaded_callback
# in order to process the addition of affordances to the various game objects.
#
# This mod is intended as a standard for modder's to use as a shared library.  Please do not
# distribute any modifications anywhere other than the mod's main download site.  Modification
# suggestions and bug notices should be communicated to the maintainer, currently Scumbumbo at
# the Mod The Sims website - http://modthesims.info/member.php?u=7401825
#


import services
from objects.definition_manager import DefinitionManager

from satisfaction.satisfaction_tracker import SatisfactionTracker
from sims4.collections import FrozenAttributeDict

from xml_injector.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class AddToTuning:
    OBJECT_SIM = 14965  # The instance ID for the object_sim tuning
    TESTING = False  # If testing then allow adding multiple copies of affordance to _super_affordances

    @staticmethod
    def add_super_affordances_to_objects(object_selection, sa_list):
        for tuning in object_selection.get_objects():
            if hasattr(tuning, '_super_affordances'):
                sa_to_add_list = []
                for sa in sa_list:
                    if AddToTuning.TESTING or sa not in tuning._super_affordances:
                        sa_to_add_list.append(sa)
                if len(sa_to_add_list) > 0:
                    log.info(f'  {tuning}: adding super_affordances to objects: {sa_to_add_list}')
                    try:
                        log.info(f'  {tuning.__name__}: adding super_affordances to objects: {sa_to_add_list.__name__}')  # TODO
                    except:
                        pass
                    tuning._super_affordances += tuple(sa_to_add_list)

    @staticmethod
    def add_super_affordances_to_sims(sa_list):
        definition_manager = services.definition_manager()
        object_sim = super(DefinitionManager, definition_manager).get(AddToTuning.OBJECT_SIM)
        sa_to_add_list = []
        for sa in sa_list:
            if AddToTuning.TESTING or sa not in object_sim._super_affordances:
                sa_to_add_list.append(sa)
        if len(sa_to_add_list) > 0:
            log.info(f'  {object_sim}: adding super_affordances to sims: {sa_to_add_list}')
            object_sim._super_affordances += tuple(sa_to_add_list)

    @staticmethod
    def add_super_affordances_to_phones(sa_list):
        definition_manager = services.definition_manager()
        object_sim = super(DefinitionManager, definition_manager).get(AddToTuning.OBJECT_SIM)
        sa_to_add_list = []
        for sa in sa_list:
            if AddToTuning.TESTING or sa not in object_sim._phone_affordances:
                sa_to_add_list.append(sa)
        if len(sa_to_add_list) > 0:
            log.info(f'  phones: adding super_affordances to phones: {sa_to_add_list}')
            object_sim._phone_affordances += tuple(sa_to_add_list)

    @staticmethod
    def add_super_affordances_to_relpanel(sa_list):
        definition_manager = services.definition_manager()
        object_sim = super(DefinitionManager, definition_manager).get(AddToTuning.OBJECT_SIM)
        sa_to_add_list = []
        for sa in sa_list:
            if AddToTuning.TESTING or sa not in object_sim._relation_panel_affordances:
                sa_to_add_list.append(sa)
        if len(sa_to_add_list) > 0:
            log.info(f'  relpanel: adding super_affordances to relpanel: {sa_to_add_list}')
            object_sim._relation_panel_affordances += tuple(sa_to_add_list)

    @staticmethod
    def add_mixer_to_affordance_list(affordance_lists_list, mixer_list):
        for affordance_list in affordance_lists_list:
            mixers_to_add_list = []
            for mixer in mixer_list:
                if AddToTuning.TESTING or mixer not in affordance_list.value:
                    mixers_to_add_list.append(mixer)
            if len(mixers_to_add_list) > 0:
                log.info(f'  {affordance_list}: adding mixer interactions: {mixers_to_add_list}')
                affordance_list.value += tuple(mixers_to_add_list)

    @staticmethod
    def add_to_loot_actions(loot_actions, loot_action_variant_list):
        log.info(f'  {loot_actions}: adding loot actions: {loot_action_variant_list}')
        saved_loot_actions = loot_actions.loot_actions
        loot_actions.loot_actions += loot_action_variant_list
        try:
            loot_actions._validate_recursion()
        except RecursionError:
            log.error(f' Added loot actions create a recursion, this would throw exceptions when used in game.')
            log.error(f' Loot action changes reverted')
            loot_actions.loot_actions = saved_loot_actions

    @staticmethod
    def add_to_random_loot_actions(random_loot_actions, random_loot_actions_list):
        log.info(f'  {random_loot_actions}: adding random loot actions: {random_loot_actions_list}')
        saved_loot_actions = random_loot_actions.random_loot_actions
        random_loot_actions.random_loot_actions += random_loot_actions_list
        try:
            random_loot_actions._validate_recursion()
        except RecursionError:
            log.error(f' Added random loot actions create a recursion, this would throw exceptions when used in game.')
            log.error(f' Random loot action changes reverted')
            random_loot_actions.random_loot_actions = saved_loot_actions

    @staticmethod
    def add_states_to_objects(object_selection, new_state_component):
        for tuning in object_selection.get_objects():
            if hasattr(tuning, '_components') and hasattr(tuning._components, 'state'):
                state_component = tuning._components.state
                if new_state_component.states:
                    log.info(f'  {tuning}: adding states to objects: {new_state_component.states}')
                    state_component._tuned_values = state_component._tuned_values.clone_with_overrides(
                        states=state_component._tuned_values.states + new_state_component.states)
                if new_state_component.state_triggers:
                    log.info(f'  {tuning}: adding state_triggers to objects: {new_state_component.state_triggers}')
                    state_component._tuned_values = state_component._tuned_values.clone_with_overrides(
                        state_triggers=state_component._tuned_values.state_triggers + new_state_component.state_triggers)

    @staticmethod
    def add_name_component_to_objects(object_selection, name_component):
        for tuning in object_selection.get_objects():
            if hasattr(tuning, '_components') and hasattr(tuning._components, 'name'):
                if tuning._components.name is None:
                    log.info(f'  {tuning}: adding name component to objects: {name_component._tuned_values}')
                    tuning._components = tuning._components.clone_with_overrides(name=name_component)
                else:
                    log.error(f' {tuning}: already has name component, cannot add')

    @staticmethod
    def add_object_relationships_to_objects(object_selection, object_relationships_component):
        for tuning in object_selection.get_objects():
            if hasattr(tuning, '_components') and hasattr(tuning._components, 'object_relationships'):
                if tuning._components.object_relationships is None:
                    log.info(f'  {tuning}: adding object_relationships component to objects: {object_relationships_component._tuned_values}')
                    tuning._components = tuning._components.clone_with_overrides(
                        object_relationships=object_relationships_component)
                else:
                    log.error(f' {tuning}: already has object_relationships component, cannot add')

    @staticmethod
    def add_lock_aware_interactions_to_lockable_objects(object_selection, sa_list):
        # For adding to the "locked" set of interactions on a computer (or any other future lockable objects like them)
        for tuning in object_selection.get_objects():
            if hasattr(tuning, '_components') and hasattr(tuning._components, 'object_locking_component'):
                sa_to_add_list = []
                for sa in sa_list:
                    if AddToTuning.TESTING or sa not in sa_to_add_list:
                        sa_to_add_list.append(sa)
                if len(sa_to_add_list) > 0:
                    log.info(f'  {tuning}: adding super_affordances to lockable objects: {sa_to_add_list}')
                    tuning._components.object_locking_component._tuned_values = tuning._components.object_locking_component._tuned_values.clone_with_overrides(
                        super_affordances=frozenset(tuning._components.object_locking_component._tuned_values.super_affordances.union(frozenset(sa_to_add_list))))

    @staticmethod
    def add_buffs_to_trait(trait, buffs_list):
        log.info(f'  {trait}: adding buffs to traits: {[b.buff_type for b in buffs_list]}')
        trait.buffs += buffs_list

    @staticmethod
    def add_satisfaction_store_rewards(rewards_list):
        for reward in rewards_list:
            log.info(f'adding satisfaction store rewards: {reward}')
        SatisfactionTracker.SATISFACTION_STORE_ITEMS = FrozenAttributeDict(
            {**dict(SatisfactionTracker.SATISFACTION_STORE_ITEMS), **rewards_list})

    @staticmethod
    def add_purchase_list_options_to_interactions(sa_list, purchase_list_options_list):
        sa_to_add_to_list = []
        for sa in sa_list:
            if sa is not None and hasattr(sa, 'purchase_list_option'):
                sa_to_add_to_list.append(sa)
        if len(sa_to_add_to_list) > 0:
            pl_option_to_add_to_list = []
            for pl_option in purchase_list_options_list:
                if pl_option is not None:
                    pl_option_to_add_to_list.append(pl_option)
            if len(pl_option_to_add_to_list) > 0:
                log.info(f'  {sa_to_add_to_list}: super_affordances adding purchase_list_options: {pl_option_to_add_to_list}')
                for sa_to_add_to in sa_to_add_to_list:
                    sa_to_add_to.purchase_list_option += tuple(pl_option_to_add_to_list)

    @staticmethod
    def add_picker_dialog_categories_to_interactions(sa_list, picker_dialog_categories_list):
        sa_to_add_to_list = []
        for sa in sa_list:
            if sa is not None and hasattr(sa, 'picker_dialog'):
                sa_to_add_to_list.append(sa)
        if len(sa_to_add_to_list) > 0:
            pd_cat_to_add_to_list = []
            for pd_cat in picker_dialog_categories_list:
                if pd_cat is not None:
                    pd_cat_to_add_to_list.append(pd_cat)
            if len(pd_cat_to_add_to_list) > 0:
                log.info(f'  {sa_to_add_to_list}: super_affordances adding picker dialog categories to interactions: {pd_cat_to_add_to_list}')
                for sa_to_add_to in sa_to_add_to_list:
                    pd_cat_to_add_dup_validated = []
                    for pd_cat in pd_cat_to_add_to_list:
                        if pd_cat not in sa_to_add_to.picker_dialog._tuned_values.categories:
                            pd_cat_to_add_dup_validated.append(pd_cat)
                    if len(pd_cat_to_add_dup_validated) > 0:
                        sa_to_add_to.picker_dialog._tuned_values = sa_to_add_to.picker_dialog._tuned_values.clone_with_overrides(
                            categories=sa_to_add_to.picker_dialog._tuned_values.categories + tuple(pd_cat_to_add_dup_validated))
                    else:
                        log.info(f'  {sa_to_add_to}: skipped, categories to add were found to be duplicates')
