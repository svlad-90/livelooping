'''
Created on Oct 12, 2024

@author: Dream Machines
'''

import midi
import plugins
import mixer

from looper_mux import constants
from looper_mux import view
from looper_mux import repeater_constants
from common import fl_helper

class Repeater:

    def __init__(self, view):
        self.__mode = repeater_constants.RepeaterMode.MODE_OFF
        self.__length = repeater_constants.RepeaterLength.LENGTH_0
        self.__view = view
        self.__repeater_mixer_channel = constants.REPEATER_MIXER_CHANNEL
        self.__repeater_mixer_slot = constants.REPEATER_MIXER_SLOT
        self.__loopers_all_mixer_channel = constants.LOOPERS_ALL_CHANNEL
        self.__turnado_control_parameter_1 = constants.TURNADO_CONTROL_PARAMETER_1
        self.__turnado_trigger_parameter = 14

    def on_init_script(self):
        self.drop()

    def start_recording(self, length):
        self.__mode = repeater_constants.RepeaterMode.MODE_RECORDING
        self.__set_mic_routing(False)
        self.__set_length(length)
        self.__set_recording_status(True)
        self.__view.set_repeater_buttons_state(repeater_constants.RepeaterMode.MODE_RECORDING, length)

    def stop_recording(self):
        self.__mode = repeater_constants.RepeaterMode.MODE_PLAYBACK
        self.__set_mic_routing(True)
        self.__set_recording_status(False)
        self.__view.set_repeater_buttons_state(repeater_constants.RepeaterMode.MODE_PLAYBACK, self.__length)

    def drop(self):
        self.__mode = repeater_constants.RepeaterMode.MODE_OFF
        self.__set_mic_routing(False)
        self.__set_length(repeater_constants.RepeaterLength.LENGTH_0)
        self.__view.set_repeater_buttons_state(repeater_constants.RepeaterMode.MODE_OFF, self.__length)

    def set_playback_length(self, length):
        self.__set_length(length)
        self.__view.set_repeater_buttons_state(self.__mode, length)

    def get_mode(self):
        return self.__mode

    def get_length(self):
        return self.__length

    def __set_mic_routing(self, status):
        if status:
            mixer.setRouteToLevel(self.__repeater_mixer_channel, self.__loopers_all_mixer_channel, fl_helper.MAX_VOLUME_LEVEL_VALUE)
        else:
            mixer.setRouteToLevel(self.__repeater_mixer_channel, self.__loopers_all_mixer_channel, 0.0)

    def __set_length(self, length):
        self.__length = length
        if length == repeater_constants.RepeaterLength.LENGTH_0:
            self.__set_turnado_repeater_parameter(0.0)
        if length == repeater_constants.RepeaterLength.LENGTH_4:
            self.__set_turnado_repeater_parameter(0.05)
        if length == repeater_constants.RepeaterLength.LENGTH_2:
            self.__set_turnado_repeater_parameter(0.250)
        if length == repeater_constants.RepeaterLength.LENGTH_1:
            self.__set_turnado_repeater_parameter(0.375)
        if length == repeater_constants.RepeaterLength.LENGTH_1_2:
            self.__set_turnado_repeater_parameter(0.500)
        if length == repeater_constants.RepeaterLength.LENGTH_1_4:
            self.__set_turnado_repeater_parameter(0.625)
        if length == repeater_constants.RepeaterLength.LENGTH_1_8:
            self.__set_turnado_repeater_parameter(0.800)
        if length == repeater_constants.RepeaterLength.LENGTH_1_16:
            self.__set_turnado_repeater_parameter(1.000)
        if length == repeater_constants.RepeaterLength.LENGTH_1_32:
            self.__set_turnado_repeater_parameter(1.000)

    def __set_turnado_repeater_parameter(self, val):
        plugins.setParamValue(val, self.__turnado_control_parameter_1, self.__repeater_mixer_channel, self.__repeater_mixer_slot, midi.PIM_None, True)

    def __set_recording_status(self, status):
        plugins.setParamValue(status, self.__turnado_trigger_parameter, self.__repeater_mixer_channel, self.__repeater_mixer_slot, midi.PIM_None, True)