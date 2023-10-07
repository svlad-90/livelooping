'''
Created on Jan 24, 2022

@author: Dream Machines
'''

import midi
import plugins

from input_controller.i_fx_preset_data_provider import IFxPresetDataProvider
from input_controller import constants
from input_controller.midi_mapping import MidiMapping
from input_controller.fx_unit import FxUnit

class FxParameter:
    FXParameter_1 = 0
    FXParameter_2 = 1
    FXParameter_3 = 2
    FXParameter_4 = 3
    FXParameter_5 = 4
    FXParameter_6 = 5
    FXParameter_7 = 6
    FXParameter_8 = 7

    def __init__(self, context, fx_param_id, view, fx_preset_data_provider: IFxPresetDataProvider):
        self.__context = context
        self.__fx_param_level = 0.0
        self.__fx_param_id = fx_param_id
        self.__view = view
        self.__midi_mapping = MidiMapping()
        self.__fx_preset_data_provider = fx_preset_data_provider
        self.__initialized = False

    def get_fx_param_id(self):
        return self.__fx_param_id

    def get_fl_param_index(self, adjustable_plugin_slot_index, fx_param_id):

        if adjustable_plugin_slot_index == constants.FINISHER_VOODOO_SLOT_INDEX:
            if fx_param_id == FxParameter.FXParameter_1:
                return constants.FINISHER_VOODOO_VARIATION_1_PARAM_INDEX
            elif fx_param_id == FxParameter.FXParameter_2:
                return constants.FINISHER_VOODOO_VARIATION_2_PARAM_INDEX
            elif fx_param_id == FxParameter.FXParameter_3:
                return constants.FINISHER_VOODOO_VARIATION_3_PARAM_INDEX
            elif fx_param_id == FxParameter.FXParameter_4:
                return constants.FINISHER_VOODOO_VARIATION_4_PARAM_INDEX
            elif fx_param_id == FxParameter.FXParameter_5:
                return constants.INVALID_PARAM
            elif fx_param_id == FxParameter.FXParameter_6:
                return constants.INVALID_PARAM
            elif fx_param_id == FxParameter.FXParameter_7:
                return constants.INVALID_PARAM
            elif fx_param_id == FxParameter.FXParameter_8:
                return constants.FINISHER_VOODOO_EFFECT_PARAM_INDEX
        elif adjustable_plugin_slot_index == constants.MANIPULATOR_SLOT_INDEX:
            if fx_param_id == FxParameter.FXParameter_1:
                return constants.MANIPULATOR_FORMANT_PARAM_INDEX
            elif fx_param_id == FxParameter.FXParameter_2:
                return constants.MANIPULATOR_PITCH_PARAM_INDEX
            elif fx_param_id == FxParameter.FXParameter_3:
                return constants.MANIPULATOR_RATIO_PARAM_INDEX
            elif fx_param_id == FxParameter.FXParameter_4:
                return constants.MANIPULATOR_HARMONICS_PARAM_INDEX
            elif fx_param_id == FxParameter.FXParameter_5:
                return constants.MANIPULATOR_FM_PARAM_INDEX
            elif fx_param_id == FxParameter.FXParameter_6:
                return constants.MANIPULATOR_ALTERNATOR_PARAM_INDEX
            elif fx_param_id == FxParameter.FXParameter_7:
                return constants.MANIPULATOR_OCTAVE_PARAM_INDEX
            elif fx_param_id == FxParameter.FXParameter_8:
                return constants.MANIPULATOR_WETDRY_PARAM_INDEX
        else:
            # cusotm handler
            return self.__midi_mapping.get_parameter_id()

    def set_midi_mapping(self, midi_mapping):
        self.__midi_mapping = midi_mapping

    def get_midi_mapping(self):
        return self.__midi_mapping

    def set_level(self, fx_param_level):

        adjustable_plugin_slot_index = FxUnit.active_fx_unit_to_adjustable_plugin_slot_index(self.__fx_preset_data_provider.get_active_fx_unit())

        fl_param_id = constants.INVALID_PARAM

        if adjustable_plugin_slot_index != constants.NO_ADJUSTABLE_EFFECT_AVAILABLE:
            fl_param_id = self.get_fl_param_index(adjustable_plugin_slot_index, self.__fx_param_id)
        else:
            if self.__midi_mapping.is_valid():
                adjustable_plugin_slot_index = self.__midi_mapping.get_plugin_number()
                fl_param_id = self.__midi_mapping.get_parameter_id()

        if fl_param_id != constants.INVALID_PARAM:
            plugins.setParamValue(fx_param_level, fl_param_id, self.__context.fx1_channel, adjustable_plugin_slot_index, midi.PIM_None, True)
            self.__fx_param_level = fx_param_level
            self.__view.set_fx_parameter_level(self.__fx_param_id, fx_param_level)

    def on_init_script(self):

        if False == self.__initialized:

            self.set_level(self.__fx_param_level)
            self.__initialized = True

    def update_params_from_plugin(self):

        adjustable_plugin_slot_index = FxUnit.active_fx_unit_to_adjustable_plugin_slot_index(self.__fx_preset_data_provider.get_active_fx_unit())

        fl_param_id = constants.INVALID_PARAM

        if adjustable_plugin_slot_index != constants.NO_ADJUSTABLE_EFFECT_AVAILABLE:
            fl_param_id = self.get_fl_param_index(adjustable_plugin_slot_index, self.__fx_param_id)
        else:
            if self.__midi_mapping.is_valid():
                adjustable_plugin_slot_index = self.__midi_mapping.get_plugin_number()
                fl_param_id = self.__midi_mapping.get_parameter_id()

        if fl_param_id != constants.INVALID_PARAM:
            param_value = plugins.getParamValue(fl_param_id, self.__context.fx1_channel, adjustable_plugin_slot_index, True)
            self.__fx_param_level = param_value
            self.__view.set_fx_parameter_activation_status(self.__fx_param_id, 1)
        else:
            self.__fx_param_level = 0.0
            self.__view.set_fx_parameter_activation_status(self.__fx_param_id, 0)

        self.__view.set_fx_parameter_level(self.__fx_param_id, self.__fx_param_level)