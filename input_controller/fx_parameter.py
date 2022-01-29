'''
Created on Jan 24, 2022

@author: Dream Machines
'''

import plugins

from common import fl_helper

from input_controller.i_fx_preset_data_provider import IFXPresetDataProvider
from input_controller import constants
from input_controller.midi_mapping import MidiMapping
from input_controller.fx_unit import FXUnit

class FXParameter:
    FXParameter_1 = 0
    FXParameter_2 = 1
    FXParameter_3 = 2
    FXParameter_4 = 3
    FXParameter_5 = 4
    FXParameter_6 = 5
    FXParameter_7 = 6
    FXParameter_8 = 7

    def __init__(self, context, fx_param_id, view, fx_preset_data_provider: IFXPresetDataProvider):
        self.__context = context
        self.__fx_param_level = 0.0
        self.__fx_param_id = fx_param_id
        self.__view = view
        self.__midi_mapping = MidiMapping()
        self.__fx_preset_data_provider = fx_preset_data_provider
        self.__initialized = False

    def getFXParamId(self):
        return self.__fx_param_id

    def getFLParamIndex(self, adjustable_plugin_slot_index, fx_param_id):

        if adjustable_plugin_slot_index == constants.FINISHER_VOODOO_SLOT_INDEX:
            if fx_param_id == FXParameter.FXParameter_1:
                return constants.FINISHER_VOODOO_VARIATION_1_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_2:
                return constants.FINISHER_VOODOO_VARIATION_2_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_3:
                return constants.FINISHER_VOODOO_VARIATION_3_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_4:
                return constants.FINISHER_VOODOO_VARIATION_4_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_5:
                return constants.INVALID_PARAM
            elif fx_param_id == FXParameter.FXParameter_6:
                return constants.INVALID_PARAM
            elif fx_param_id == FXParameter.FXParameter_7:
                return constants.INVALID_PARAM
            elif fx_param_id == FXParameter.FXParameter_8:
                return constants.FINISHER_VOODOO_EFFECT_PARAM_INDEX
        elif adjustable_plugin_slot_index == constants.MANIPULATOR_SLOT_INDEX:
            if fx_param_id == FXParameter.FXParameter_1:
                return constants.MANIPULATOR_FORMANT_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_2:
                return constants.MANIPULATOR_PITCH_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_3:
                return constants.MANIPULATOR_RATIO_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_4:
                return constants.MANIPULATOR_HARMONICS_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_5:
                return constants.MANIPULATOR_FM_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_6:
                return constants.MANIPULATOR_ALTERNATOR_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_7:
                return constants.MANIPULATOR_OCTAVE_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_8:
                return constants.MANIPULATOR_WETDRY_PARAM_INDEX
        else:
            # cusotm handler
            return self.__midi_mapping.getParameterId()

    def setMidiMapping(self, midi_mapping):
        self.__midi_mapping = midi_mapping

    def getMidiMapping(self):
        return self.__midi_mapping

    def setLevel(self, fx_param_level):

        adjustable_plugin_slot_index = FXUnit.activeFXUnitToAdjustablePluginSlotIndex(self.__fx_preset_data_provider.getActiveFXUnit())

        fl_param_id = constants.INVALID_PARAM

        if adjustable_plugin_slot_index != constants.NO_ADJUSTABLE_EFFECT_AVAILABLE:
            fl_param_id = self.getFLParamIndex(adjustable_plugin_slot_index, self.__fx_param_id)
        else:
            if self.__midi_mapping.isValid():
                adjustable_plugin_slot_index = self.__midi_mapping.getPluginNumber()
                fl_param_id = self.__midi_mapping.getParameterId()

        if fl_param_id != constants.INVALID_PARAM:
            plugins.setParamValue(fx_param_level, fl_param_id, self.__context.fx1_channel, adjustable_plugin_slot_index)
            self.__fx_param_level = fx_param_level
            self.__view.setFXParameterLevel(self.__fx_param_id, fx_param_level)

    def onInitScript(self):
        
        if False == self.__initialized:
            
            self.setLevel(self.__fx_param_level)
            self.__initialized = True

    def updateParamsFromPlugin(self):

        adjustable_plugin_slot_index = FXUnit.activeFXUnitToAdjustablePluginSlotIndex(self.__fx_preset_data_provider.getActiveFXUnit())

        fl_param_id = constants.INVALID_PARAM

        if adjustable_plugin_slot_index != constants.NO_ADJUSTABLE_EFFECT_AVAILABLE:
            fl_param_id = self.getFLParamIndex(adjustable_plugin_slot_index, self.__fx_param_id)
        else:
            if self.__midi_mapping.isValid():
                adjustable_plugin_slot_index = self.__midi_mapping.getPluginNumber()
                fl_param_id = self.__midi_mapping.getParameterId()

        if fl_param_id != constants.INVALID_PARAM:

            param_value = plugins.getParamValue(fl_param_id, self.__context.fx1_channel, adjustable_plugin_slot_index)

            if adjustable_plugin_slot_index == constants.MANIPULATOR_SLOT_INDEX or \
               adjustable_plugin_slot_index == constants.FABFILTER_PRO_Q3_SLOT_INDEX or \
               adjustable_plugin_slot_index == constants.FINISHER_VOODOO_SLOT_INDEX:
                    param_value = fl_helper.externalParamMapping(param_value)

            self.__fx_param_level = param_value
            self.__view.setFXParameterActivationStatus(self.__fx_param_id, 1)
        else:
            self.__fx_param_level = 0.0
            self.__view.setFXParameterActivationStatus(self.__fx_param_id, 0)

        self.__view.setFXParameterLevel(self.__fx_param_id, self.__fx_param_level)