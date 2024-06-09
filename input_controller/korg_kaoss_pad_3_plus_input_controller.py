'''
Created on Jan 24, 2022

@author: Dream Machines
'''

import time

import transport
import midi
import device
import plugins
import mixer

from input_controller import constants
from input_controller.device_type import DeviceType
from input_controller.view import View
from input_controller.fx_preset_page import FxPresetPage
from input_controller.fx import Fx
from input_controller.fx_preset import FxPreset
from input_controller.fx_unit import FxUnit
from input_controller.fx_parameter import FxParameter
from input_controller.i_midi_mapping_input_client import IMidiMappingInputClient
from input_controller.midi_mapping_input_dialog import MidiMappingInputDialog
from common import fl_helper, global_constants


class KorgKaossPad3PlusInputController(IMidiMappingInputClient):

    def __init__(self, context):
        print(context.device_name + ': ' + KorgKaossPad3PlusInputController.__init__.__name__)

        self.__context = context
        self.__view = View(context)
        self.__initialized = False
        self.__shift_pressed = False
        self.__selected_fx_preset_page = FxPresetPage.fx_preset_page_1
        self.__fx_preset_pages = { FxPresetPage.fx_preset_page_1: FxPresetPage(self.__context, FxPresetPage.fx_preset_page_1, self.__view),
                                   FxPresetPage.fx_preset_page_2: FxPresetPage(self.__context, FxPresetPage.fx_preset_page_2, self.__view),
                                   FxPresetPage.fx_preset_page_3: FxPresetPage(self.__context, FxPresetPage.fx_preset_page_3, self.__view),
                                   FxPresetPage.fx_preset_page_4: FxPresetPage(self.__context, FxPresetPage.fx_preset_page_4, self.__view) }
        self.__is_save_mode = False
        self.__is_delete_mode = False
        self.__is_midi_mapping_save_mode = False
        self.__fxs = { Fx.FX_1: Fx(self.__context, Fx.FX_1, self.__view),
                      Fx.FX_2: Fx(self.__context, Fx.FX_2, self.__view),
                      Fx.FX_3: Fx(self.__context, Fx.FX_3, self.__view),
                      Fx.FX_4: Fx(self.__context, Fx.FX_4, self.__view),
                      Fx.FX_5: Fx(self.__context, Fx.FX_5, self.__view),
                      Fx.FX_6: Fx(self.__context, Fx.FX_6, self.__view),
                      Fx.FX_7: Fx(self.__context, Fx.FX_7, self.__view),
                      Fx.FX_8: Fx(self.__context, Fx.FX_8, self.__view),
                      Fx.FX_9: Fx(self.__context, Fx.FX_9, self.__view),
                      Fx.FX_10: Fx(self.__context, Fx.FX_10, self.__view),
                      Fx.FX_11: Fx(self.__context, Fx.FX_11, self.__view),
                      Fx.FX_12: Fx(self.__context, Fx.FX_12, self.__view),
                      Fx.FX_13: Fx(self.__context, Fx.FX_13, self.__view),
                      Fx.FX_14: Fx(self.__context, Fx.FX_14, self.__view),
                      Fx.FX_15: Fx(self.__context, Fx.FX_15, self.__view),
                      Fx.FX_16: Fx(self.__context, Fx.FX_16, self.__view),
                      Fx.FX_17: Fx(self.__context, Fx.FX_17, self.__view),
                      Fx.FX_18: Fx(self.__context, Fx.FX_18, self.__view),
                      Fx.FX_19: Fx(self.__context, Fx.FX_19, self.__view),
                      Fx.FX_20: Fx(self.__context, Fx.FX_20, self.__view), }

        self.__buttons_last_press_time = {}

        self.__fx_level = 1.0

        self.__turnado_dry_wet_level = 0.0
        self.__turnado_dictator_level = 0.0
        self.__turnado_is_off = True
        self.__midi_loop_started = False
        self.__should_start_midi_loop = False
        self.__midi_mapping_input_dialog = None

        self.__save_from_preset_page_id = None
        self.__save_from_preset_id = None

        self.__stashed_sidechain_values = []

        self.__interraction_with_screen_active = False
        self.__shift_touch_action_considered = False
        self.__sc_loopers_mode = False

    def on_init_script(self, event):

        if False == self.__initialized:

            print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.on_init_script.__name__)

            # try:
            for preset_page_id in self.__fx_preset_pages:
                self.__fx_preset_pages[preset_page_id].on_init_script()

            if False == self.__midi_loop_started and True == self.__should_start_midi_loop:
                pass
                # old_event_data = event.data1
                # event.data1 = constants.MIDI_CC_INTERNAL_LOOP
                # device.repeatMidiEvent(event, 16, 16)
                # event.data1 = old_event_data
                # self.__midi_loop_started = True

            # fl_helper.print_all_plugin_parameters(self.__context.fx1_channel, constants.FX1_FABFILTER_PRO_Q3_SLOT_INDEX)

            self.reset()

            self.__initialized = True

            # except Exception as e:
            #    print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.on_init_script.__name__ + ": failed to initialize the script.")
            #    print(e)

    def action_on_double_click(self, pressed_button, action):
        pressed_time = time.time()

        if not pressed_button in self.__buttons_last_press_time.keys():
            self.__buttons_last_press_time[pressed_button] = 0

        if (pressed_time - self.__buttons_last_press_time[pressed_button]) < 0.5:
            # double click
            self.__buttons_last_press_time.clear()
            self.__buttons_last_press_time[pressed_button] = 0
            action()
        else:
            self.__buttons_last_press_time.clear()
            self.__buttons_last_press_time[pressed_button] = pressed_time

    def is_save_mode(self):
        return self.__is_save_mode

    def is_delete_mode(self):
        return self.__is_delete_mode

    def set_save_mode(self, save_mode):
        # print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.set_save_mode.__name__ + ": save mode - " + str(save_mode))
        self.__is_save_mode = save_mode
        self.__view.set_save_mode(save_mode)

        if True == save_mode:
            self.__save_from_preset_page_id = self.__selected_fx_preset_page
            self.__save_from_preset_id = self.get_selected_fx_preset_id()
        else:
            self.__save_from_preset_page_id = None
            self.__save_from_preset_id = None

        if True == save_mode and True == self.is_delete_mode():
            self.set_delete_mode(False)

    def set_delete_mode(self, delete_mode):
        # print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.set_delete_mode.__name__ + ": save mode - " + str(delete_mode))
        self.__is_delete_mode = delete_mode
        self.__view.set_delete_mode(delete_mode)

        if True == delete_mode and True == self.is_save_mode():
            self.set_save_mode(False)

    def is_midi_mapping_save_mode(self):
        return self.__is_midi_mapping_save_mode

    def set_midi_mapping_save_mode(self, midi_mapping_save_mode):
        # print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.set_midi_mapping_save_mode.__name__ + ": midi mapping save mode - " + str(midi_mapping_save_mode))

        if True == midi_mapping_save_mode:
            self.__midi_mapping_input_dialog = MidiMappingInputDialog([self.__context.fx1_channel, self.__context.fx2_channel], self)
            self.__fx_preset_pages[self.__selected_fx_preset_page].set_active_fx_unit(FxUnit.FX_UNIT_CUSTOM)
        else:
            self.__midi_mapping_input_dialog = None

        self.__is_midi_mapping_save_mode = midi_mapping_save_mode
        self.__view.set_midi_mapping_save_mode(midi_mapping_save_mode)

    def select_fx_page(self, preset_fx_page_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.select_fx_page.__name__ + ": fx page id - " + str(preset_fx_page_id))
        self.__selected_fx_preset_page = preset_fx_page_id;
        self.__fx_preset_pages[self.__selected_fx_preset_page].select(not self.is_save_mode())

        self.set_fx_level(self.__fx_level, True)
        self.__reset_panomatic()
        self.__set_sc_loopers_mode(False)

    def set_shift_pressed_state(self, shift_pressed):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.set_shift_pressed_state.__name__ + ": shift pressed - " + str(shift_pressed))
        self.__view.set_shift_pressed_state(shift_pressed)
        self.__shift_pressed = shift_pressed

        if(True == shift_pressed):
            self.action_on_double_click(constants.MIDI_CC_SHIFT, self.randomize_turnado)

    def randomize_turnado(self):
        print(self.__context.device_name + ': ' + self.randomize_turnado.__name__)
        plugins.setParamValue(0.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__context.fx3_channel, constants.TURNADO_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__context.fx3_channel, constants.TURNADO_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__context.fx3_channel, constants.TURNADO_SLOT_INDEX, midi.PIM_None, True)
        self.__restore_params()

    def get_shift_pressed_state(self):
        return self.__shift_pressed

    def select_fx_preset_on_the_visible_page(self, preset_fx_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.select_fx_preset_on_the_visible_page.__name__ + ": selected page - " + \
              str(self.__selected_fx_preset_page) + ", selected FX - " + str(preset_fx_id))
        self.__fx_preset_pages[self.__selected_fx_preset_page].select_fx_preset(preset_fx_id)

        self.set_fx_level(self.__fx_level, True)

        self.__reset_panomatic()
        self.__set_sc_loopers_mode(False)

    def update_fx_preset(self, fx_preset_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.update_fx_preset.__name__)

        if self.is_save_mode() and self.__save_from_preset_page_id != None and self.__save_from_preset_id != None:
            self.__fx_preset_pages[self.__selected_fx_preset_page]\
            .set_midi_mappings(fx_preset_id, self.__fx_preset_pages[self.__save_from_preset_page_id]\
            .get_midi_mappings(self.__save_from_preset_id))
            self.__fx_preset_pages[self.__selected_fx_preset_page]\
            .set_active_fx_unit_custom(fx_preset_id, self.__fx_preset_pages[self.__save_from_preset_page_id]\
            .get_active_fx_unit_custom(self.__save_from_preset_id))

        self.__fx_preset_pages[self.__selected_fx_preset_page].update_fx_preset(fx_preset_id)

    def reset_fx_preset(self, fx_preset_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.reset_fx_preset.__name__)
        self.__fx_preset_pages[self.__selected_fx_preset_page].reset_fx_preset(fx_preset_id)

    def set_volume(self, synth_volume):
        mixer.setTrackVolume(self.__context.fx3_channel, synth_volume)
        self.__view.set_volume(synth_volume)

    def set_fx_level(self, fx_level, force=False):
        for fx_id in self.__fxs:
            self.__fxs[fx_id].set_fx_level(fx_level, force)
        self.__view.set_fx_level(fx_level)
        self.__fx_level = fx_level

    def set_fx_parameter_level(self, fx_parameter_id, effect_level):
        self.__fx_preset_pages[self.__selected_fx_preset_page].set_fx_parameter_level(fx_parameter_id, effect_level)

    def get_selected_fx_preset_id(self):
        return self.__fx_preset_pages[self.__selected_fx_preset_page].get_selected_fx_preset_id()

    def set_turnado_dry_wet_level(self, turnado_dry_wet_level):
        self.__turnado_dry_wet_level = turnado_dry_wet_level
        plugins.setParamValue(self.__turnado_dry_wet_level, constants.TURNADO_DRY_WET_PARAM_INDEX, self.__context.fx3_channel, constants.TURNADO_SLOT_INDEX, midi.PIM_None, True)

        if turnado_dry_wet_level == 0.0:
            self.__turnado_is_off = True
        else:
            self.__turnado_is_off = False

        self.__view.set_turnado_dry_wet_level(turnado_dry_wet_level)
        self.__view.turnado_off(turnado_dry_wet_level == 0.0)

    def set_turnado_dictator_level(self, turnado_dictator_level):
        self.__turnado_dictator_level = turnado_dictator_level
        plugins.setParamValue(self.__turnado_dictator_level, constants.TURNADO_DICTATOR_PARAM_INDEX, self.__context.fx3_channel, constants.TURNADO_SLOT_INDEX, midi.PIM_None, True)

        self.__view.set_turnado_dictator_level(turnado_dictator_level)

    def switch_to_next_turnado_preset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.switch_to_next_turnado_preset.__name__)
        plugins.nextPreset(self.__context.fx3_channel, constants.TURNADO_SLOT_INDEX, True)
        self.__restore_params()

        self.__view.switch_to_next_turnado_preset()

    def switch_to_prev_turnado_preset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.switch_to_prev_turnado_preset.__name__)
        plugins.prevPreset(self.__context.fx3_channel, constants.TURNADO_SLOT_INDEX, True)
        self.__restore_params()

        self.__view.switch_to_prev_turnado_preset()

    def turnado_on_off(self):
        self.__turnado_is_off = not self.__turnado_is_off

        if self.__turnado_is_off == False:
            if self.__turnado_dry_wet_level != 0.0:
                val = self.__turnado_dry_wet_level
            else:
                val = 1.0
        else:
            val = 0.0

        print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.turnado_on_off.__name__ + ": turnado fx level - " + str(val))

        plugins.setParamValue(val, constants.TURNADO_DRY_WET_PARAM_INDEX, self.__context.fx3_channel, constants.TURNADO_SLOT_INDEX, midi.PIM_None, True)

        self.__view.turnado_off(val == 0.0)
        self.__view.set_turnado_dry_wet_level(val)

    def __restore_params(self):
        plugins.setParamValue(self.__turnado_dictator_level, constants.TURNADO_DICTATOR_PARAM_INDEX, self.__context.fx3_channel, constants.TURNADO_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(self.__turnado_dry_wet_level, constants.TURNADO_DRY_WET_PARAM_INDEX, self.__context.fx3_channel, constants.TURNADO_SLOT_INDEX, midi.PIM_None, True)

    def __select_fx_preset(self, preset_fx_page_id, preset_fx_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.__select_FxPreset__name__ + ": selected page - " + \
              str(preset_fx_page_id) + ", selected FX - " + str(preset_fx_id))
        self.__fx_preset_pages[preset_fx_page_id].select_fx_preset(preset_fx_id)

        self.set_fx_level(self.__fx_level, True)

    def change_active_fx_unit(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.change_active_fx_unit.__name__)
        self.__fx_preset_pages[self.__selected_fx_preset_page].change_active_fx_unit()
        self.set_fx_level(self.__fx_level, True)

    def switch_active_fx_unit_to_prev_preset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.switch_active_fx_unit_to_prev_preset.__name__)

        active_fx_unit = self.__fx_preset_pages[self.__selected_fx_preset_page].get_active_fx_unit()

        if active_fx_unit == FxUnit.FX_UNIT_MANIPULATOR:
            plugins.prevPreset(self.__context.fx2_channel, constants.FX2_MANIPULATOR_SLOT_INDEX, True)
        elif active_fx_unit == FxUnit.FX_UNIT_FINISHER_VOODOO:
            current_program = plugins.getParamValue(constants.FINISHER_VOODOO_MODE_PARAM_INDEX, self.__context.fx2_channel, constants.FX2_FINISHER_VOODOO_SLOT_INDEX, True) * constants.FINISHER_VOODOO_MODE_NUMBER

            target_program = current_program - 1

            if target_program < -0.5:
                target_program = constants.FINISHER_VOODOO_MODE_NUMBER

            print("target_program - " + str(target_program))

            plugins.setParamValue(target_program / constants.FINISHER_VOODOO_MODE_NUMBER, constants.FINISHER_VOODOO_MODE_PARAM_INDEX, self.__context.fx2_channel, constants.FX2_FINISHER_VOODOO_SLOT_INDEX, midi.PIM_None, True)

        self.__view.switch_active_fx_unit_to_prev_preset()

        self.__fx_preset_pages[self.__selected_fx_preset_page].view_update_fx_params_from_plugins()

    def switch_active_fx_unit_to_next_preset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.switch_active_fx_unit_to_next_preset.__name__)

        active_fx_unit = self.__fx_preset_pages[self.__selected_fx_preset_page].get_active_fx_unit()

        if active_fx_unit == FxUnit.FX_UNIT_MANIPULATOR:
            plugins.nextPreset(self.__context.fx2_channel, constants.FX2_MANIPULATOR_SLOT_INDEX, True)
        elif active_fx_unit == FxUnit.FX_UNIT_FINISHER_VOODOO:
            current_program = plugins.getParamValue(constants.FINISHER_VOODOO_MODE_PARAM_INDEX, self.__context.fx2_channel, constants.FX2_FINISHER_VOODOO_SLOT_INDEX, True) * constants.FINISHER_VOODOO_MODE_NUMBER

            target_program = current_program + 1

            if target_program > constants.FINISHER_VOODOO_MODE_NUMBER + 0.5:
                target_program = 0

            print("target_program - " + str(target_program))

            plugins.setParamValue(target_program / constants.FINISHER_VOODOO_MODE_NUMBER, constants.FINISHER_VOODOO_MODE_PARAM_INDEX, self.__context.fx2_channel, constants.FX2_FINISHER_VOODOO_SLOT_INDEX, midi.PIM_None, True)

        self.__view.switch_active_fx_unit_to_next_preset()

        self.__fx_preset_pages[self.__selected_fx_preset_page].view_update_fx_params_from_plugins()

    def __reset_sidechain(self):
        try:
            self.__set_input_side_chain_level(constants.Track_1, constants.DEFAULT_INPUT_SIDECHAIN_LEVEL)
            self.__set_input_side_chain_level(constants.Track_2, constants.DEFAULT_INPUT_SIDECHAIN_LEVEL)
            self.__set_input_side_chain_level(constants.Track_3, constants.DEFAULT_INPUT_SIDECHAIN_LEVEL)
            self.__set_input_side_chain_level(constants.Track_4, constants.DEFAULT_INPUT_SIDECHAIN_LEVEL)
            self.__stashed_sidechain_values.clear()
        except:
            pass

    def __stash_unstash_sidechain(self):
        # print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.__stash_unstash_sidechain.__name__)
        if len(self.__stashed_sidechain_values) == 4:
            for index, unstash_value in enumerate(self.__stashed_sidechain_values):
                # print("unstash_value - " + str(unstash_value))
                self.__set_input_side_chain_level(index, unstash_value)
            self.__stashed_sidechain_values.clear()
        else:
            for index in range(4):
                stash_value = self.__get_input_side_chain_level(index)
                # print("stash_value - " + str(stash_value))
                self.__stashed_sidechain_values.append(stash_value)
                self.__set_input_side_chain_level(index, constants.DEFAULT_INPUT_SIDECHAIN_LEVEL)

    def reset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.reset.__name__)

        self.__selected_fx_preset_page = FxPresetPage.fx_preset_page_1
        self.select_fx_page(self.__selected_fx_preset_page)
        self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_1)

        self.__is_save_mode = False
        self.__view.set_save_mode(self.__is_save_mode)

        self.__is_delete_mode = False
        self.__view.set_delete_mode(self.__is_delete_mode)

        self.set_turnado_dictator_level(0.0)
        self.set_turnado_dry_wet_level(constants.DEFAULT_TURNADO_DRY_WET_LEVEL)

        self.set_fx_level(1.0, True)
        self.set_volume(fl_helper.MAX_VOLUME_LEVEL_VALUE)

        self.__reset_sidechain()
        self.__set_sc_loopers_mode(False)

    def midi_loop(self):
        # print(self.__context.device_name + ': ' + KorgKaossPad3PlusInputController.midi_loop.__name__)
        pass

    def midi_mapping_input_done(self, fx_parameter_number, midi_mapping):
        self.__fx_preset_pages[self.__selected_fx_preset_page].set_midi_mapping(fx_parameter_number, midi_mapping)
        self.set_midi_mapping_save_mode(False)

    def midi_mapping_input_cancelled(self):
        self.set_midi_mapping_save_mode(False)

    def __set_input_side_chain_level(self, track_id, sidechain_level):
        self.__view.set_input_side_chain_level(track_id, sidechain_level)

        knob_prefix = ""

        if self.__context.device_type == DeviceType.MIC:
            knob_prefix = "M2L1T"
        elif self.__context.device_type == DeviceType.SYNTH:
            knob_prefix = "S2L1T"

        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, knob_prefix + str(track_id + 1) + "S", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def __get_input_side_chain_level(self, track_id):
        knob_prefix = ""

        if self.__context.device_type == DeviceType.MIC:
            knob_prefix = "M2L1T"
        elif self.__context.device_type == DeviceType.SYNTH:
            knob_prefix = "S2L1T"

        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, knob_prefix + str(track_id + 1) + "S", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        return plugins.getParamValue(parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, True)

    def __reset_panomatic(self):
        plugins.setParamValue(constants.PANOMATIC_DEFAULT_PAN_LEVEL, constants.PANOMATIC_PAN_PARAM_INDEX, self.__context.fx3_channel, constants.INPUT_CONTROLLER_PANOMATIC_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(constants.PANOMATIC_DEFAULT_VOLUME_LEVEL, constants.PANOMATIC_VOLUME_PARAM_INDEX, self.__context.fx3_channel, constants.INPUT_CONTROLLER_PANOMATIC_SLOT_INDEX, midi.PIM_None, True)

    def __turn_off_scene(self):
        self.__fx_preset_pages[self.__selected_fx_preset_page].turn_off_scene(self.get_selected_fx_preset_id())

    def __jump_to_next_scene(self):
        self.__fx_preset_pages[self.__selected_fx_preset_page].jump_to_next_scene(self.get_selected_fx_preset_id())

    def __jump_to_previous_scene(self):
        self.__fx_preset_pages[self.__selected_fx_preset_page].jump_to_previous_scene(self.get_selected_fx_preset_id())

    def __set_sc_loopers_mode(self, value):
        if self.__sc_loopers_mode != value:
            parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, self.__context.loopers_sc_ctrl_name, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(1 if value else 0, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
            self.__view.set_vocal_loopers_sc(1 if value else 0)
            self.__sc_loopers_mode = value

    def __get_sc_loopers_mode(self):
        return self.__sc_loopers_mode

    def on_midi_msg(self, event):

        # fl_helper.print_midi_event(event)

        event.handled = False

        self.on_init_script(event)

        if True == self.__midi_loop_started and constants.MIDI_CC_INTERNAL_LOOP == event.data1:
            self.midi_loop()
        else:
            if True == self.is_midi_mapping_save_mode():
                if event.data1 == constants.MIDI_CC_ENTER_SAVE_MODE and self.get_shift_pressed_state():
                    action = lambda self = self: (self.set_midi_mapping_save_mode(not self.is_midi_mapping_save_mode()), \
                                                   self.set_save_mode(False), \
                                                   self.set_delete_mode(False))
                    self.action_on_double_click(constants.MIDI_CC_ENTER_SAVE_MODE + constants.ENTER_MIDI_MAPPING_SAVE_MODE_SHIFT, action)
                elif event.data1 == constants.MIDI_CC_SHIFT:
                    self.set_shift_pressed_state(event.data2 == fl_helper.MIDI_MAX_VALUE)
                else:
                    if self.__midi_mapping_input_dialog:
                        self.__midi_mapping_input_dialog.on_midi_msg(event)
            else:
                if True == fl_helper.is_kp3_program_change_event(event):
                    self.__stash_unstash_sidechain()
                elif event.data1 == constants.MIDI_CC_EFFECTS_PAGE_1 and self.get_shift_pressed_state():
                    self.select_fx_page(FxPresetPage.fx_preset_page_1)
                elif event.data1 == constants.MIDI_CC_EFFECTS_PAGE_2 and self.get_shift_pressed_state():
                    self.select_fx_page(FxPresetPage.fx_preset_page_2)
                elif event.data1 == constants.MIDI_CC_EFFECTS_PAGE_3 and self.get_shift_pressed_state():
                    self.select_fx_page(FxPresetPage.fx_preset_page_3)
                elif event.data1 == constants.MIDI_CC_EFFECTS_PAGE_4 and self.get_shift_pressed_state():
                    self.select_fx_page(FxPresetPage.fx_preset_page_4)
                elif event.data1 == constants.MIDI_CC_SHIFT:
                    self.set_shift_pressed_state(event.data2 == fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_ENTER_SAVE_MODE and self.get_shift_pressed_state():
                    self.set_save_mode(not self.is_save_mode())

                    action = lambda self = self: (self.set_midi_mapping_save_mode(not self.is_midi_mapping_save_mode()), \
                                                   self.set_save_mode(False))
                    self.action_on_double_click(constants.MIDI_CC_ENTER_SAVE_MODE + constants.ENTER_MIDI_MAPPING_SAVE_MODE_SHIFT, action)
                elif event.data1 == constants.MIDI_CC_ENTER_DELETE_MODE and self.get_shift_pressed_state():
                    self.set_delete_mode(not self.is_delete_mode())
                elif event.data1 == constants.MIDI_CC_PREV_ACTIVE_FX_UNIT_PRESET and self.get_shift_pressed_state():
                    self.switch_active_fx_unit_to_prev_preset()
                elif event.data1 == constants.MIDI_CC_NEXT_ACTIVE_FX_UNIT_PRESET and self.get_shift_pressed_state():
                    self.switch_active_fx_unit_to_next_preset()
                elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_1 and True == self.get_shift_pressed_state():
                    self.__set_input_side_chain_level(constants.Track_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_2 and True == self.get_shift_pressed_state():
                    self.__set_input_side_chain_level(constants.Track_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_3 and True == self.get_shift_pressed_state():
                    self.__set_input_side_chain_level(constants.Track_3, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_4 and True == self.get_shift_pressed_state():
                    self.__set_input_side_chain_level(constants.Track_4, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_NEXT_SCENE and True == self.get_shift_pressed_state():
                    if False == self.__shift_touch_action_considered:
                        self.__jump_to_next_scene()
                        self.__shift_touch_action_considered = True
                elif event.data1 == constants.MIDI_CC_PREV_SCENE and True == self.get_shift_pressed_state():
                    if False == self.__shift_touch_action_considered:
                        self.__jump_to_previous_scene()
                        self.__shift_touch_action_considered = True
                elif event.data1 == constants.MIDI_CC_TURN_OFF_SCENE and True == self.get_shift_pressed_state():
                    if False == self.__shift_touch_action_considered:
                        self.__turn_off_scene()
                        self.__shift_touch_action_considered = True
                elif event.data1 == constants.MIDI_CC_SC_LOOPERS_MODE and True == self.get_shift_pressed_state():
                    if False == self.__shift_touch_action_considered:
                        self.__set_sc_loopers_mode(not self.__get_sc_loopers_mode())
                        self.__shift_touch_action_considered = True
                elif event.data1 == constants.MIDI_CC_EFFECT_1 and self.is_delete_mode():
                    self.reset_fx_preset(FxPreset.fx_preset_1)
                    self.set_delete_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_1)
                elif event.data1 == constants.MIDI_CC_EFFECT_2 and self.is_delete_mode():
                    self.reset_fx_preset(FxPreset.fx_preset_2)
                    self.set_delete_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_2)
                elif event.data1 == constants.MIDI_CC_EFFECT_3 and self.is_delete_mode():
                    self.reset_fx_preset(FxPreset.fx_preset_3)
                    self.set_delete_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_3)
                elif event.data1 == constants.MIDI_CC_EFFECT_4 and self.is_delete_mode():
                    self.reset_fx_preset(FxPreset.fx_preset_4)
                    self.set_delete_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_4)
                elif event.data1 == constants.MIDI_CC_EFFECT_5 and self.is_delete_mode():
                    self.reset_fx_preset(FxPreset.fx_preset_5)
                    self.set_delete_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_5)
                elif event.data1 == constants.MIDI_CC_EFFECT_6 and self.is_delete_mode():
                    self.reset_fx_preset(FxPreset.fx_preset_6)
                    self.set_delete_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_6)
                elif event.data1 == constants.MIDI_CC_EFFECT_7 and self.is_delete_mode():
                    self.reset_fx_preset(FxPreset.fx_preset_7)
                    self.set_delete_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_7)
                elif event.data1 == constants.MIDI_CC_EFFECT_8 and self.is_delete_mode():
                    self.reset_fx_preset(FxPreset.fx_preset_8)
                    self.set_delete_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_8)
                elif event.data1 == constants.MIDI_CC_EFFECT_1 and self.is_save_mode():
                    self.update_fx_preset(FxPreset.fx_preset_1)
                    self.set_save_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_1)
                elif event.data1 == constants.MIDI_CC_EFFECT_2 and self.is_save_mode():
                    self.update_fx_preset(FxPreset.fx_preset_2)
                    self.set_save_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_2)
                elif event.data1 == constants.MIDI_CC_EFFECT_3 and self.is_save_mode():
                    self.update_fx_preset(FxPreset.fx_preset_3)
                    self.set_save_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_3)
                elif event.data1 == constants.MIDI_CC_EFFECT_4 and self.is_save_mode():
                    self.update_fx_preset(FxPreset.fx_preset_4)
                    self.set_save_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_4)
                elif event.data1 == constants.MIDI_CC_EFFECT_5 and self.is_save_mode():
                    self.update_fx_preset(FxPreset.fx_preset_5)
                    self.set_save_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_5)
                elif event.data1 == constants.MIDI_CC_EFFECT_6 and self.is_save_mode():
                    self.update_fx_preset(FxPreset.fx_preset_6)
                    self.set_save_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_6)
                elif event.data1 == constants.MIDI_CC_EFFECT_7 and self.is_save_mode():
                    self.update_fx_preset(FxPreset.fx_preset_7)
                    self.set_save_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_7)
                elif event.data1 == constants.MIDI_CC_EFFECT_8 and self.is_save_mode():
                    self.update_fx_preset(FxPreset.fx_preset_8)
                    self.set_save_mode(False)
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_8)
                elif event.data1 == constants.MIDI_CC_EFFECT_1 and not self.get_shift_pressed_state():
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_1)
                elif event.data1 == constants.MIDI_CC_EFFECT_2 and not self.get_shift_pressed_state():
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_2)
                elif event.data1 == constants.MIDI_CC_EFFECT_3 and not self.get_shift_pressed_state():
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_3)
                elif event.data1 == constants.MIDI_CC_EFFECT_4 and not self.get_shift_pressed_state():
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_4)
                elif event.data1 == constants.MIDI_CC_EFFECT_5 and not self.get_shift_pressed_state():
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_5)
                elif event.data1 == constants.MIDI_CC_EFFECT_6 and not self.get_shift_pressed_state():
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_6)
                elif event.data1 == constants.MIDI_CC_EFFECT_7 and not self.get_shift_pressed_state():
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_7)
                elif event.data1 == constants.MIDI_CC_EFFECT_8 and not self.get_shift_pressed_state():
                    self.select_fx_preset_on_the_visible_page(FxPreset.fx_preset_8)
                elif event.data1 == constants.MIDI_CC_FX_LEVEL and self.get_shift_pressed_state():
                    self.set_fx_level(event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_TURNADO_DRY_WET and self.get_shift_pressed_state():
                    self.set_turnado_dry_wet_level(event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_TURNADO_DICTATOR:
                    self.set_turnado_dictator_level(event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_1:
                    self.set_fx_parameter_level(FxParameter.FXParameter_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_2:
                    self.set_fx_parameter_level(FxParameter.FXParameter_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_3:
                    self.set_fx_parameter_level(FxParameter.FXParameter_3, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_4:
                    self.set_fx_parameter_level(FxParameter.FXParameter_4, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_5:
                    self.set_fx_parameter_level(FxParameter.FXParameter_5, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_6:
                    self.set_fx_parameter_level(FxParameter.FXParameter_6, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_7:
                    self.set_fx_parameter_level(FxParameter.FXParameter_7, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_8:
                    self.set_fx_parameter_level(FxParameter.FXParameter_8, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_SYNTH_VOLUME:
                    self.set_volume((event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
                elif event.data1 == constants.MIDI_CC_TURNADO_NEXT_PRESET and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                    self.switch_to_next_turnado_preset()
                elif event.data1 == constants.MIDI_CC_TURNADO_PREV_PRESET and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                    self.switch_to_prev_turnado_preset()
                elif event.data1 == constants.MIDI_CC_TURNADO_ON_OFF and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                    self.turnado_on_off()
                elif event.data1 == constants.MIDI_CC_CHANGE_ACTIVE_FX_UNIT and not self.get_shift_pressed_state() and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                    self.change_active_fx_unit()
                elif event.data1 == constants.MIDI_CC_CHANGE_ACTIVE_FX_UNIT and self.get_shift_pressed_state() and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                    self.reset()
                elif event.data1 == constants.MIDI_CC_SCREEN_TOUCH_SCREEN_ACTION and event.data2 == 0:
                    # begin of interaction with the touchscreen
                    self.__interraction_with_screen_active = False
                    self.__shift_touch_action_considered = False
                elif event.data1 == constants.MIDI_CC_SCREEN_TOUCH_SCREEN_ACTION and event.data2 == 127:
                    # end of interaction with the touchscreen
                    self.__interraction_with_screen_active = True
                elif event.midiId == global_constants.LOOPER_MUX_MIDI_ID and \
                event.midiChan == global_constants.LOOPER_MUX_MIDI_CHAN and \
                event.data1 == global_constants.LOOPER_MUX_START_RECORDING_MSG_DATA_1 and \
                event.data2 == global_constants.LOOPER_MUX_START_RECORDING_MSG_DATA_2:
                    self.__set_sc_loopers_mode(False)

        event.handled = True

    def on_refresh(self, flags):
        if True == self.__initialized:
            if (flags & 256) != 0:
                if(False == transport.isPlaying()):
                    self.__reset_sidechain()
                    self.__set_sc_loopers_mode(False)
