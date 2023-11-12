'''
Created on Jan 27, 2022

@author: Dream Machines
'''

import plugins

from input_controller.midi_mapping import MidiMapping
from input_controller import constants

MIDI_CC_PREVIOUS_ITEM         = 36
MIDI_CC_NEXT_ITEM             = 37
MIDI_CC_SELECT                = 38
MIDI_CC_EXIT                  = 39

MIDI_CC_1              = 49
MIDI_CC_2              = 50
MIDI_CC_3              = 51
MIDI_CC_4              = 52
MIDI_CC_5              = 53
MIDI_CC_6              = 54
MIDI_CC_7              = 55
MIDI_CC_8              = 56

MSG_PREFIX = "MIDI mapping input dialog"

class MidiMappingInputDialog:

    STATE_IDLE                          = 0
    STATE_SELECT_FX_PARAMETER_NUMBER    = 1
    STATE_SELECT_PLUGIN_NUMBER          = 2
    STATE_SELECT_PLUGIN_PARAMETER_ID    = 3
    STATE_FINAL                         = 4

    def __init__(self, plugins_mixer_channel, midi_mapping_input_client):
        self.__plugins_mixer_channel = plugins_mixer_channel
        self.__midi_mapping_input_client = midi_mapping_input_client
        self.__state = MidiMappingInputDialog.STATE_IDLE
        self.__selected_fx_parameter_number = constants.INVALID_PARAM
        self.__selected_plugin_number = 0
        self.__selected_parameter_id = 0

        if self.__state == MidiMappingInputDialog.STATE_IDLE:
            self.__state = MidiMappingInputDialog.STATE_SELECT_FX_PARAMETER_NUMBER
            print(MSG_PREFIX + " >>> Please, enter fx parameter number.")

    def on_midi_msg(self, event):

        if self.__state == MidiMappingInputDialog.STATE_SELECT_FX_PARAMETER_NUMBER:
            if event.data1 == MIDI_CC_1 or\
            event.data1 == MIDI_CC_2 or\
            event.data1 == MIDI_CC_3 or\
            event.data1 == MIDI_CC_4 or\
            event.data1 == MIDI_CC_5 or\
            event.data1 == MIDI_CC_6 or\
            event.data1 == MIDI_CC_7 or\
            event.data1 == MIDI_CC_8:
                self.__selected_fx_parameter_number = event.data1 - MIDI_CC_1
                print(MSG_PREFIX + " >>> Fx parameter number '" + str(self.__selected_fx_parameter_number) + "' was selected")
                self.__state = MidiMappingInputDialog.STATE_SELECT_PLUGIN_NUMBER
                print(MSG_PREFIX + " >>> Please, select the target plugin")

                self.__selected_plugin_number = constants.MIN_PLUGIN_NUMBER
                plugin_name = plugins.getPluginName(self.__plugins_mixer_channel, self.__selected_plugin_number, True)
                print(MSG_PREFIX + " >>> Current cursor position is - #" + str(self.__selected_plugin_number) + f" '{plugin_name}'")
            elif event.data1 == MIDI_CC_EXIT:
                print(MSG_PREFIX + " >>> Operation was cancelled.")
                self.__midi_mapping_input_client.midi_mapping_input_cancelled()
                self.__state = MidiMappingInputDialog.STATE_FINAL
        elif self.__state == MidiMappingInputDialog.STATE_SELECT_PLUGIN_NUMBER:
            if event.data1 == MIDI_CC_NEXT_ITEM and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                self.__selected_plugin_number = self.__selected_plugin_number + 1

                if self.__selected_plugin_number > constants.MAX_PLUGIN_NUMBER:
                    self.__selected_plugin_number = constants.MIN_PLUGIN_NUMBER

                plugin_name = plugins.getPluginName(self.__plugins_mixer_channel, self.__selected_plugin_number, True)
                print(MSG_PREFIX + " >>> Current cursor position is - #" + str(self.__selected_plugin_number) + f" '{plugin_name}'")
            elif event.data1 == MIDI_CC_PREVIOUS_ITEM and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                self.__selected_plugin_number = self.__selected_plugin_number - 1

                if self.__selected_plugin_number < constants.MIN_PLUGIN_NUMBER:
                    self.__selected_plugin_number = constants.MAX_PLUGIN_NUMBER

                plugin_name = plugins.getPluginName(self.__plugins_mixer_channel, self.__selected_plugin_number, True)
                print(MSG_PREFIX + " >>> Current cursor position is - #" + str(self.__selected_plugin_number) + f" '{plugin_name}'")
            elif event.data1 == MIDI_CC_SELECT and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                plugin_name = plugins.getPluginName(self.__plugins_mixer_channel, self.__selected_plugin_number, True)
                print(MSG_PREFIX + " >>> Plugin #" + str(self.__selected_plugin_number) + f" '{plugin_name}' was selected")
                self.__state = MidiMappingInputDialog.STATE_SELECT_PLUGIN_PARAMETER_ID

                print(MSG_PREFIX + " >>> Please, select the target parameter")

                self.__selected_parameter_id = 0
                parameter_name = plugins.getParamName(self.__selected_parameter_id, self.__plugins_mixer_channel, self.__selected_plugin_number, True)
                print(MSG_PREFIX + " >>> Current cursor position is - #" + str(self.__selected_parameter_id) + f" '{parameter_name}'")

            elif event.data1 == MIDI_CC_EXIT and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                print(MSG_PREFIX + " >>> Operation was cancelled.")
                self.__state = MidiMappingInputDialog.STATE_FINAL
                self.__midi_mapping_input_client.midi_mapping_input_cancelled()
            elif event.data1 == MIDI_CC_6 and self.__midi_mapping_input_client.get_shift_pressed_state():
                print(MSG_PREFIX + " >>> Mapping was deleted.")
                self.__midi_mapping_input_client.midi_mapping_input_done(self.__selected_fx_parameter_number, MidiMapping())
        elif self.__state == MidiMappingInputDialog.STATE_SELECT_PLUGIN_PARAMETER_ID:
            if event.data1 == MIDI_CC_NEXT_ITEM and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                param_count = plugins.getParamCount(self.__plugins_mixer_channel, self.__selected_plugin_number, True)
                self.__selected_parameter_id = self.__selected_parameter_id + 1

                if self.__selected_parameter_id >= param_count:
                    self.__selected_parameter_id = 0

                parameter_name = plugins.getParamName(self.__selected_parameter_id, self.__plugins_mixer_channel, self.__selected_plugin_number, True)
                print(MSG_PREFIX + " >>> Current cursor position is - #" + str(self.__selected_parameter_id) + f" '{parameter_name}'")
            elif event.data1 == MIDI_CC_PREVIOUS_ITEM and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                param_count = plugins.getParamCount(self.__plugins_mixer_channel, self.__selected_plugin_number, True)
                self.__selected_parameter_id = self.__selected_parameter_id - 1

                if self.__selected_parameter_id < 0:
                    self.__selected_parameter_id = param_count - 1

                parameter_name = plugins.getParamName(self.__selected_parameter_id, self.__plugins_mixer_channel, self.__selected_plugin_number, True)
                print(MSG_PREFIX + " >>> Current cursor position is - #" + str(self.__selected_parameter_id) + f" '{parameter_name}'")
            elif event.data1 == MIDI_CC_SELECT and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                parameter_name = plugins.getParamName(self.__selected_parameter_id, self.__plugins_mixer_channel, self.__selected_plugin_number, True)
                print(MSG_PREFIX + " >>> Parameter #" + str(self.__selected_parameter_id) + f" '{parameter_name}' was selected")
                midi_mapping = MidiMapping(self.__selected_plugin_number,
                                           self.__selected_parameter_id)
                self.__midi_mapping_input_client.midi_mapping_input_done(self.__selected_fx_parameter_number, midi_mapping)
                self.__state = MidiMappingInputDialog.STATE_FINAL
            elif event.data1 == MIDI_CC_EXIT and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                print(MSG_PREFIX + " >>> Operation was cancelled.")
                self.__midi_mapping_input_client.midi_mapping_input_cancelled()
                self.__state = MidiMappingInputDialog.STATE_FINAL
            elif event.data1 == MIDI_CC_6 and self.__midi_mapping_input_client.get_shift_pressed_state():
                print(MSG_PREFIX + " >>> Mapping was deleted.")
                self.__midi_mapping_input_client.midi_mapping_input_done(self.__selected_fx_parameter_number, midi_mapping())