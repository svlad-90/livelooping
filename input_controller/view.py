'''
Created on Jan 24, 2022

@author: Dream Machines
'''

import midi
import plugins

from common import fl_helper
from input_controller import constants
from input_controller.fx_unit import FxUnit

class View:

    def __init__(self, context):
        self.__context = context
        print(self.__context.device_name + ': ' + View.__init__.__name__)

    def set_shift_pressed_state(self, shift_pressed):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "Shift", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(shift_pressed, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.reset_toggle_flags()

    def reset_toggle_flags(self):
        pass

    def select_fx_page(self, preset_fx_page_id):
        for i in range(4):
            value = 0.0
            if i == preset_fx_page_id:
                value = 1.0

            parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "Page " + str(i + 1), constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(value, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

        self.reset_toggle_flags()

    def select_fx_preset(self, preset_fx_id):
        for i in range(8):
            value = 0.0
            if i == preset_fx_id:
                value = 1.0

            parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "FX" + str(i + 1), constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(value, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

        self.reset_toggle_flags()

    def set_delete_mode(self, delete_mode):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "Delete mode", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(delete_mode, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_save_mode(self, save_mode):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "Save mode", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(save_mode, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_midi_mapping_save_mode(self, midi_mapping_save_mode):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "Midi mapping save mode", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(midi_mapping_save_mode, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_volume(self, synth_volume):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "Volume", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(synth_volume, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_fx_level(self, fx_level):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "FX level", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(fx_level, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_fx_preset_availability(self, fx_preset_id, preset_availability):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "FX_" + str(fx_preset_id + 1) + "_A", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(preset_availability, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_fx_parameter_level(self, fx_param_id, fx_level):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "FXP" + str(fx_param_id + 1), constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(fx_level, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_fx_parameter_activation_status(self, fx_param_id, activation_status):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "FX_P_" + str(fx_param_id + 1) + "_A", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(activation_status, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_turnado_dry_wet_level(self, turnado_dry_wet_level):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "T_Dry/Wet", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(turnado_dry_wet_level, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_turnado_dictator_level(self, turnado_dictator_level):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "T_Dictator", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(turnado_dictator_level, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def switch_to_next_turnado_preset(self):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "T_Next_Preset", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def switch_to_prev_turnado_preset(self):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "T_Previous_Preset", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def switch_active_fx_unit_to_next_preset(self):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "FX_U_Next_Preset", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def switch_active_fx_unit_to_prev_preset(self):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "FX_U_Prev_Preset", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def turnado_off(self, off_value):
        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "T_Off", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(off_value, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_active_fx_unit(self, active_fx_unit):

        manipulator_value = 0.0
        voodoo_finisher_value = 0.0
        custom_value = 0.0

        if active_fx_unit == FxUnit.FX_UNIT_MANIPULATOR:
            manipulator_value = 1.0
        elif active_fx_unit == FxUnit.FX_UNIT_FINISHER_VOODOO:
            voodoo_finisher_value = 1.0
        elif active_fx_unit == FxUnit.FX_UNIT_CUSTOM:
            custom_value = 1.0

        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "AFX_Manipulator", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(manipulator_value, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "AFX_Voodoo_Finisher", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(voodoo_finisher_value, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

        parameter_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "AFX_Custom", constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(custom_value, parameter_id, self.__context.main_channel, constants.SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
