'''
Created on Jan 24, 2022

@author: Dream Machines
'''

import midi
import plugins
import math

from common import fl_helper
from input_controller.fx_parameter import FxParameter
from input_controller.fx_unit import FxUnit
from input_controller import constants
from input_controller.persistency import PersistencyItem
from input_controller.i_fx_preset_data_provider import IFxPresetDataProvider
from input_controller.midi_mapping import MidiMapping

class FxPreset(IFxPresetDataProvider):
    fx_preset_1    = 0
    fx_preset_2    = 1
    fx_preset_3    = 2
    fx_preset_4    = 3
    fx_preset_5    = 4
    fx_preset_6    = 5
    fx_preset_7    = 6
    fx_preset_8    = 7

    def __init__(self, context, fx_page_number, fx_number, view):
        self.__context = context
        self.__view = view
        self.__fx_page_number = fx_page_number
        self.__fx_number = fx_number
        self.__persistency_item = PersistencyItem(self.__context.params_first_storage_track_id + ( self.__fx_page_number * constants.NUMBER_OF_FX_IN_PAGE ) + self.__fx_number)
        self.__fx_parameters = { FxParameter.FXParameter_1: FxParameter(self.__context, FxParameter.FXParameter_1, view, self),
                                 FxParameter.FXParameter_2: FxParameter(self.__context, FxParameter.FXParameter_2, view, self),
                                 FxParameter.FXParameter_3: FxParameter(self.__context, FxParameter.FXParameter_3, view, self),
                                 FxParameter.FXParameter_4: FxParameter(self.__context, FxParameter.FXParameter_4, view, self),
                                 FxParameter.FXParameter_5: FxParameter(self.__context, FxParameter.FXParameter_5, view, self),
                                 FxParameter.FXParameter_6: FxParameter(self.__context, FxParameter.FXParameter_6, view, self),
                                 FxParameter.FXParameter_7: FxParameter(self.__context, FxParameter.FXParameter_7, view, self),
                                 FxParameter.FXParameter_8: FxParameter(self.__context, FxParameter.FXParameter_8, view, self) }

        self.__active_fx_unit = FxUnit.FX_UNIT_CUSTOM
        self.__initialized = False

    def on_init_script(self):

        if False == self.__initialized:

            self.__persistency_item.init()

            self.set_active_fx_unit(self.__persistency_item.get_active_fx_unit())
            self.__load_midi_mappings_from_persistency()
            self.__load_turnado_patch_from_persistency()
            self.view_update_active_fx_unit()

            for fx_parameter_id in self.__fx_parameters:
                self.__fx_parameters[fx_parameter_id].on_init_script()

            self.__initialized = True

    def update(self):
        self.__get_params_from_plugins()
        self.__persistency_item.set_active_fx_unit(self.__active_fx_unit)
        self.__store_midi_mappings_to_persistency()
        self.__store_turnado_patch_to_persistency()
        self.__save_data()
        self.__apply_parameters_to_plugins()
        self.view_update_active_fx_unit()

    def reset(self):
        self.__reset_data()

    def set_midi_mappings(self, midi_mappings):
        fx_parameter_number = 0
        for midi_mapping in midi_mappings:
            self.set_midi_mapping(fx_parameter_number, midi_mapping)
            fx_parameter_number += 1

    def get_midi_mappings(self):
        midi_mappings = []
        for fx_parameter in self.__fx_parameters:
            midi_mapping = self.__fx_parameters[fx_parameter].get_midi_mapping()
            midi_mappings.append(midi_mapping)
        return midi_mappings

    def get_midi_mappings_as_lists(self):
        midi_mappings = {}
        for fx_parameter in self.__fx_parameters:
            midi_mapping = self.__fx_parameters[fx_parameter].get_midi_mapping()
            midi_mappings[self.__fx_parameters[fx_parameter].get_fx_param_id()] = midi_mapping.convert_to_list()
        return midi_mappings

    def set_midi_mapping(self, fx_parameter_number, midi_mapping):
        self.__fx_parameters[fx_parameter_number].set_midi_mapping(midi_mapping)
        self.view_update_fx_params_from_plugins()

    def select(self):
        plugins.setParamValue(0.0, constants.PANOMATIC_VOLUME_PARAM_INDEX, self.__context.main_channel, constants.PRESET_CHANGE_PROTECTOR_PANOMATIC_SLOT_INDEX, midi.PIM_None, True)

        if not self.__are_parameters_loaded():
            self.__load_data()

        self.__apply_parameters_to_plugins()
        self.__active_fx_unit = self.__persistency_item.get_active_fx_unit()
        self.__load_midi_mappings_from_persistency()
        self.__load_turnado_patch_from_persistency()
        self.__view.select_fx_preset(self.__fx_number)
        self.view_update_active_fx_unit()

        plugins.setParamValue(fl_helper.MAX_VOLUME_LEVEL_VALUE, constants.PANOMATIC_VOLUME_PARAM_INDEX, self.__context.main_channel, constants.PRESET_CHANGE_PROTECTOR_PANOMATIC_SLOT_INDEX, midi.PIM_None, True)

    def view_update_fx_preset_availability(self):
        self.__view.set_fx_preset_availability(self.__fx_number, len(self.__persistency_item.get_plugin_parameters()) > 0)

    def view_update_fx_params_from_plugins(self):
        for fx_param_id in self.__fx_parameters:
            self.__fx_parameters[fx_param_id].update_params_from_plugin()

    def view_update_active_fx_unit(self):
        #print("view_update_active_fx_unit: active_fx_unit - " + str(self.__active_fx_unit) + "; active_fx_unit - " + str(self.__fx_page_number) + "; fx_number - " + str(self.__fx_number))
        self.__view.set_active_fx_unit(self.__active_fx_unit)
        self.view_update_fx_params_from_plugins()

    def set_fx_parameter_level(self, fx_param_id, fx_param_level):
        self.__fx_parameters[fx_param_id].set_level(fx_param_level)

    def get_active_fx_unit(self):
        return self.__active_fx_unit

    def set_active_fx_unit(self, active_fx_unit):
        self.__active_fx_unit = active_fx_unit

    def __are_parameters_loaded(self):
        return len(self.__persistency_item.get_plugin_parameters()) != 0

    def __calculate_channel_id_from_channel_id_counter(self, channel_id_counter):
        channel_id = None

        if channel_id_counter == 0:
            channel_id = self.__context.fx2_channel
        elif channel_id_counter == 1:
            channel_id = self.__context.fx1_channel

        return channel_id

    def __get_params_from_plugins(self):
        self.__persistency_item.reset_plugin_parameters()

        parameters = {}

        parameters[constants.FX_ACTIVATION_STATE_CHANNEL_INDEX] = {}

        for channel_id_counter in range (constants.PERSISTENT_FX_CHANNELS_NUMBER):

            channel_id = self.__calculate_channel_id_from_channel_id_counter(channel_id_counter)

            parameters[constants.FX_ACTIVATION_STATE_CHANNEL_INDEX][channel_id_counter] = []

            parameters[channel_id] = {}

            for mixer_slot in range(constants.MAX_MIXER_SLOT):

                parameters[channel_id][mixer_slot] = []

                param_count = plugins.getParamCount(channel_id, mixer_slot, True)

                for param_id in range(param_count):

                    if channel_id == self.__context.fx1_channel:
                        if mixer_slot == constants.FX1_FABFILTER_PRO_Q3_SLOT_INDEX and param_id > constants.FABFILTER_PRO_Q3_PARAMS_LIMIT:
                            break;

                        if ( mixer_slot == constants.FX1_TURNADO_1_SLOT_INDEX or mixer_slot == constants.FX1_TURNADO_2_SLOT_INDEX \
                        or mixer_slot == constants.FX1_TURNADO_3_SLOT_INDEX ) and param_id > constants.TURNADO_PARAMS_LIMIT:
                            break;

                        if mixer_slot == constants.FX1_ENDLESS_SMILE_SLOT_INDEX and param_id > constants.ENDLESS_SMILE_PARAMS_LIMIT:
                            break;

                    elif channel_id == self.__context.fx2_channel:
                        if mixer_slot == constants.FX2_MANIPULATOR_SLOT_INDEX and param_id > constants.MANIPULATOR_PARAMS_LIMIT:
                            break;

                        if mixer_slot == constants.FX2_FINISHER_VOODOO_SLOT_INDEX and param_id > constants.FINISHER_VOODOO_PARAMS_LIMIT:
                            break;
    
                        if mixer_slot == constants.FX2_FABFILTER_PRO_Q3_SLOT_INDEX and param_id > constants.FABFILTER_PRO_Q3_PARAMS_LIMIT:
                            break;

                    param_value = plugins.getParamValue(param_id, channel_id, mixer_slot, True)
                    param_value_str = str(param_value)

                    # param_name = plugins.getParamName(param_id, channel_id, mixer_slot, True)
                    # plugin_name = plugins.getPluginName(channel_id, mixer_slot, True)
                    # print("Get parameter: plugin name - " + plugin_name + ", param - " + param_name + \
                    #       ", param_value - " + param_value_str + ", param_id - " + str(param_id) + \
                    #       ", channel - " + str(channel_id) + ", mixer_slot - " + str(mixer_slot))

                    parameters[channel_id][mixer_slot].append( param_value_str )

                parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "E" + str(channel_id_counter * constants.MAX_MIXER_SLOT + mixer_slot + 1) + "_TO", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
                fx_activation_state = plugins.getParamValue(parameter_id, self.__context.main_channel, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, True)
                parameters[constants.FX_ACTIVATION_STATE_CHANNEL_INDEX][channel_id_counter].append(str( fx_activation_state ))

                self.__persistency_item.set_plugin_parameters(parameters)

    def __apply_parameters_to_plugins(self):

        parameters = self.__persistency_item.get_plugin_parameters()

        # We should parse the activation state data first
        activation_state_data = { self.__context.fx1_channel : {}, self.__context.fx2_channel : {} }

        if constants.FX_ACTIVATION_STATE_CHANNEL_INDEX in parameters:
            activation_state_config = parameters[constants.FX_ACTIVATION_STATE_CHANNEL_INDEX]
            for channel_id_counter, channel_data in activation_state_config.items():
                for param_id, param_value_str in reversed(list(enumerate(channel_data))):
                    # Hack due to the fact that these parameters are not sequencial in the control surface.
                    # They go from 0 to 9 and then from 10 to 19
                    param_id_to_apply = param_id
                    if channel_id_counter == 0:
                        channel_id = self.__context.fx1_channel
                    elif channel_id_counter == 1:
                        channel_id = self.__context.fx2_channel

                    param_id_to_apply += 20 * channel_id_counter

                    # print("~~~ channel_id - " + str(channel_id) + ", param_id_to_apply - " + str(param_id_to_apply))      

                    param_value = float(param_value_str)

                    old_param_value = plugins.getParamValue(param_id_to_apply, self.__context.main_channel, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, True)
                    
                    if param_value != old_param_value:
                        plugins.setParamValue(param_value, param_id_to_apply, self.__context.main_channel, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
                    
                    param_id_normalized = param_id % constants.MAX_MIXER_SLOT
                    activation_state_data[channel_id][param_id_normalized] = param_value

        for channel_id, channel_data in parameters.items():

            # logic for application of the migrated data
            if channel_id == constants.INVALID_PARAM:
                channel_id = self.__context.fx2_channel

            if channel_id == constants.FX_ACTIVATION_STATE_CHANNEL_INDEX:
                # do nothing. It was already handled above
                pass
            else:
                for mixer_slot_id, mixer_slot_data in channel_data.items():
                    if activation_state_data[channel_id][mixer_slot_id] == 1.0:
                        for param_id, param_value_str in reversed(list(enumerate(mixer_slot_data))):
                            param_value = float(param_value_str)
                            
                            # print("channel_id - " + str(channel_id) + ", mixer_slot_id - " + str(mixer_slot_id) + ", param_id - " + str(param_id))
                            
                            # plugin_name = plugins.getPluginName(channel_id, mixer_slot_id, True)
                            #
                            # if param_id == 134 and plugin_name == "Turnado_2":
                            #     param_name = plugins.getParamName(param_id, channel_id, mixer_slot_id, True)
                            #
                            #     print("Apply parameter: plugin name - " + plugin_name + ", param - " + param_name + \
                            #           ", param_value - " + str(param_value) + ", param_id - " + str(param_id) + \
                            #           ", channel - " + str(channel_id) + ", mixer_slot_id - " + str(mixer_slot_id))
                            existing_param_value = plugins.getParamValue(param_id, channel_id, mixer_slot_id, True)
                            if existing_param_value != param_value:
                                plugins.setParamValue(param_value, param_id, channel_id, mixer_slot_id, midi.PIM_None, True)

    def __load_midi_mappings_from_persistency(self):
        midi_mappings = self.__persistency_item.get_midi_mapping()

        # print(f"loading {str(len(midi_mappings))} midi mappings from persistency - {midi_mappings}")

        if len(midi_mappings) == 0:
            for fx_parameter in self.__fx_parameters:
                self.__fx_parameters[fx_parameter].set_midi_mapping(MidiMapping())
        else:
            for fx_parameter_id in midi_mappings:
                self.__fx_parameters[fx_parameter_id].set_midi_mapping(MidiMapping.create_from_list(midi_mappings[fx_parameter_id]))

    def __store_midi_mappings_to_persistency(self):
        midi_mappings = self.get_midi_mappings_as_lists()
        # print(f"storing {str(len(midi_mappings))} midi mappings to persistency - {midi_mappings}")
        self.__persistency_item.set_midi_mapping(midi_mappings)

    def __load_turnado_patch_from_persistency(self):
        turnado_patch_id = self.__persistency_item.get_turnado_patch()

        if turnado_patch_id:
            self.__view.set_turnado_patch(turnado_patch_id)

    def __store_turnado_patch_to_persistency(self):
            self.__persistency_item.set_turnado_patch(self.__view.get_turnado_patch())

    def __load_data(self):
        self.__persistency_item.read_from_storage()

    def __save_data(self):
        self.__persistency_item.write_to_storage()

    def __reset_data(self):
        self.__persistency_item.reset_storage()
