'''
Created on Jan 24, 2022

@author: Dream Machines
'''

import midi
import plugins

from common import fl_helper
from input_controller.fx_parameter import FXParameter
from input_controller.fx_unit import FXUnit
from input_controller import constants
from input_controller.persistency import PersistencyItem
from input_controller.i_fx_preset_data_provider import IFXPresetDataProvider
from input_controller import common
from input_controller.midi_mapping import MidiMapping

class FXPreset(IFXPresetDataProvider):
    FXPreset_1    = 0
    FXPreset_2    = 1
    FXPreset_3    = 2
    FXPreset_4    = 3
    FXPreset_5    = 4
    FXPreset_6    = 5
    FXPreset_7    = 6
    FXPreset_8    = 7

    def __init__(self, context, fx_page_number, fx_number, view):
        self.__context = context
        self.__view = view
        self.__fx_page_number = fx_page_number
        self.__fx_number = fx_number
        self.__persistency_item = PersistencyItem(self.__context.params_first_storage_track_id + ( self.__fx_page_number * constants.NUMBER_OF_FX_IN_PAGE ) + self.__fx_number)
        self.__fx_parameters = { FXParameter.FXParameter_1: FXParameter(self.__context, FXParameter.FXParameter_1, view, self),
                                 FXParameter.FXParameter_2: FXParameter(self.__context, FXParameter.FXParameter_2, view, self),
                                 FXParameter.FXParameter_3: FXParameter(self.__context, FXParameter.FXParameter_3, view, self),
                                 FXParameter.FXParameter_4: FXParameter(self.__context, FXParameter.FXParameter_4, view, self),
                                 FXParameter.FXParameter_5: FXParameter(self.__context, FXParameter.FXParameter_5, view, self),
                                 FXParameter.FXParameter_6: FXParameter(self.__context, FXParameter.FXParameter_6, view, self),
                                 FXParameter.FXParameter_7: FXParameter(self.__context, FXParameter.FXParameter_7, view, self),
                                 FXParameter.FXParameter_8: FXParameter(self.__context, FXParameter.FXParameter_8, view, self) }

        self.__active_fx_unit = FXUnit.FX_UNIT_CUSTOM
        self.__initialized = False

    def onInitScript(self):

        if False == self.__initialized:

            self.__persistency_item.init()

            self.setActiveFXUnit(self.__persistency_item.getActiveFxUnit())
            self.__loadMidiMappingsFromPersistency()
            self.view_updateActiveFXUnit()

            for fx_parameter_id in self.__fx_parameters:
                self.__fx_parameters[fx_parameter_id].onInitScript()

            self.__initialized = True

    def update(self):
        self.__getParamsFromPlugins()
        self.__persistency_item.setActiveFxUnit(self.__active_fx_unit)
        self.__storeMidiMappingsToPersistency()
        self.__saveData()
        self.__applyParametersToPlugins()
        self.view_updateActiveFXUnit()

    def reset(self):
        self.__resetData()

    def setMidiMappings(self, midi_mappings):
        fx_parameter_number = 0
        for midi_mapping in midi_mappings:
            self.setMidiMapping(fx_parameter_number, midi_mapping)
            fx_parameter_number += 1

    def getMidiMappings(self):
        midi_mappings = []
        for fx_parameter in self.__fx_parameters:
            midi_mapping = self.__fx_parameters[fx_parameter].getMidiMapping()
            midi_mappings.append(midi_mapping)
        return midi_mappings

    def getMidiMappingsAsLists(self):
        midi_mappings = {}
        for fx_parameter in self.__fx_parameters:
            midi_mapping = self.__fx_parameters[fx_parameter].getMidiMapping()
            midi_mappings[self.__fx_parameters[fx_parameter].getFXParamId()] = midi_mapping.convertToList()
        return midi_mappings

    def setMidiMapping(self, fx_parameter_number, midi_mapping):
        self.__fx_parameters[fx_parameter_number].setMidiMapping(midi_mapping)
        self.view_updateFXParamsFromPlugins()

    def select(self):
        plugins.setParamValue(0.0, constants.PANOMATIC_VOLUME_PARAM_INDEX, self.__context.main_channel, constants.PRESET_CHANGE_PROTECTOR_PANOMATIC_SLOT_INDEX, midi.PIM_None, True)

        if not self.__areParametersLoaded():
            self.__loadData()

        self.__applyParametersToPlugins()
        self.__active_fx_unit = self.__persistency_item.getActiveFxUnit()
        self.__loadMidiMappingsFromPersistency()
        self.__view.selectFXPreset(self.__fx_number)
        self.view_updateActiveFXUnit()

        plugins.setParamValue(fl_helper.MAX_VOLUME_LEVEL_VALUE, constants.PANOMATIC_VOLUME_PARAM_INDEX, self.__context.main_channel, constants.PRESET_CHANGE_PROTECTOR_PANOMATIC_SLOT_INDEX, midi.PIM_None, True)

    def view_updateFXPresetAvailability(self):
        self.__view.setFXPresetAvailability(self.__fx_number, len(self.__persistency_item.getPluginParameters()) > 0)

    def view_updateFXParamsFromPlugins(self):
        for fx_param_id in self.__fx_parameters:
            self.__fx_parameters[fx_param_id].updateParamsFromPlugin()

    def view_updateActiveFXUnit(self):
        #print("view_updateActiveFXUnit: active_fx_unit - " + str(self.__active_fx_unit) + "; active_fx_unit - " + str(self.__fx_page_number) + "; fx_number - " + str(self.__fx_number))
        self.__view.setActiveFXUnit(self.__active_fx_unit)
        self.view_updateFXParamsFromPlugins()

    def setFXParameterLevel(self, fx_param_id, fx_param_level):
        self.__fx_parameters[fx_param_id].setLevel(fx_param_level)

    def getActiveFXUnit(self):
        return self.__active_fx_unit

    def setActiveFXUnit(self, active_fx_unit):
        self.__active_fx_unit = active_fx_unit

    def __areParametersLoaded(self):
        return len(self.__persistency_item.getPluginParameters()) != 0

    def __getParamsFromPlugins(self):
        self.__persistency_item.resetPluginParameters()

        parameters = {}

        parameters[constants.FX_ACTIVATION_STATE_SLOT_INDEX] = []

        for mixer_slot in range(10):

            parameters[mixer_slot] = []

            param_count = plugins.getParamCount(self.__context.fx1_channel, mixer_slot, True)

            for param_id in range(param_count):

                if mixer_slot == constants.MANIPULATOR_SLOT_INDEX and param_id > constants.MANIPULATOR_PARAMS_LIMIT:
                    break;

                if mixer_slot == constants.FINISHER_VOODOO_SLOT_INDEX and param_id > constants.FINISHER_VOODOO_PARAMS_LIMIT:
                    break;

                if mixer_slot == constants.FABFILTER_PRO_Q3_SLOT_INDEX and param_id > constants.FABFILTER_PRO_Q3_PARAMS_LIMIT:
                    break;

                param_value = plugins.getParamValue(param_id, self.__context.fx1_channel, mixer_slot, True)
                param_value_str = str(param_value)

                # param_name = plugins.getParamName(param_id, self.__context.fx1_channel, mixer_slot, True)
                # plugin_name = plugins.getPluginName(self.__context.fx1_channel, mixer_slot, True)
                # print("Get parameter: plugin name - " + plugin_name + ", param - " + param_name + \
                #       ", param_value - " + param_value_str + ", param_id - " + str(param_id) + \
                #       ", channel - " + str(self.__context.fx1_channel) + ", mixer_slot - " + str(mixer_slot))

                parameters[mixer_slot].append( param_value_str )


            parameter_id = fl_helper.findParameterByName(self.__context.main_channel, "E" + str(mixer_slot+1) + "_TO", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            fx_activation_state = plugins.getParamValue(parameter_id, self.__context.main_channel, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, True)
            parameters[constants.FX_ACTIVATION_STATE_SLOT_INDEX].append(str( fx_activation_state ))

            self.__persistency_item.setPluginParameters(parameters)

    def __applyParametersToPlugins(self):

        parameters = self.__persistency_item.getPluginParameters()

        for mixer_slot in parameters:

            for param_id, param_value_str in reversed(list(enumerate(parameters[mixer_slot]))):

                param_value = float(param_value_str)

                if mixer_slot == constants.FX_ACTIVATION_STATE_SLOT_INDEX:
                    #print("__applyParametersToPlugins: constants.FX_ACTIVATION_STATE_SLOT_INDEX mixer channel -" + str(self.__context.main_channel) + \
                    #", param_id - " + str(param_id) + ", param_value - " + str(param_value))
                    plugins.setParamValue(param_value, param_id, self.__context.main_channel, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
                else:

                    # plugin_name = plugins.getPluginName(self.__context.fx1_channel, mixer_slot, True)
                    # param_name = plugins.getParamName(param_id, self.__context.fx1_channel, mixer_slot, True)
                    #
                    # print("Apply parameter: plugin name - " + plugin_name + ", param - " + param_name + \
                    #       ", param_value - " + str(param_value) + ", param_id - " + str(param_id) + \
                    #       ", channel - " + str(self.__context.fx1_channel) + ", mixer_slot - " + str(mixer_slot))

                    plugins.setParamValue(param_value, param_id, self.__context.fx1_channel, mixer_slot, midi.PIM_None, True)

    def __loadMidiMappingsFromPersistency(self):
        midi_mappings = self.__persistency_item.getMidiMapping()

        print(f"loading {str(len(midi_mappings))} midi mappings from persistency - {midi_mappings}")

        if len(midi_mappings) == 0:
            for fx_parameter in self.__fx_parameters:
                self.__fx_parameters[fx_parameter].setMidiMapping(MidiMapping())
        else:
            for fx_parameter_id in midi_mappings:
                self.__fx_parameters[fx_parameter_id].setMidiMapping(MidiMapping.createFromList(midi_mappings[fx_parameter_id]))

    def __storeMidiMappingsToPersistency(self):
        midi_mappings = self.getMidiMappingsAsLists()
        print(f"storing {str(len(midi_mappings))} midi mappings from persistency - {midi_mappings}")
        self.__persistency_item.setMidiMapping(midi_mappings)

    def __loadData(self):
        self.__persistency_item.readFromStorage()

    def __saveData(self):
        self.__persistency_item.writeToStorage()

    def __resetData(self):
        self.__persistency_item.resetStorage()
