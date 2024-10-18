'''
Created on Feb 7, 2022

@author: Dream Machines
'''

import midi
import plugins
import mixer
import device

from looper_mux import constants
from looper_mux.sample_length import SampleLength
from common import fl_helper, global_constants
from common import updateable    

class Track():

    RECORDING_STATE_OFF       = 0
    RECORDING_STATE_RECORDING = 1
    RECORDING_STATE_PLAYBACK  = 37

    def __init__(self, looper_number, track_number, mixer_channel, view, context_provider):
        self.__view = view
        self.__looper_number = looper_number
        self.__track_number = track_number
        self.__mixer_channel = mixer_channel
        self.__sample_length = SampleLength.LENGTH_0
        self.__volume = fl_helper.MAX_VOLUME_LEVEL_VALUE
        self.__hp_filter_level = fl_helper.MIN_LEVEL_VALUE
        self.__lp_filter_level = fl_helper.MAX_LEVEL_VALUE
        self.__recording_state = Track.RECORDING_STATE_OFF
        self.__context_provider = context_provider
        self.__is_gui_active = False
        self.__pan = global_constants.DEFAULT_PANOMATIC_PAN_LEVEL
        self.__selection_status = False
        self.__looper_fx_1_channel = self.__calculate_looper_fx_1_channel()

        action_click = lambda: \
            self.__view.set_track_clear_state(self.__track_number, True)
        
        action_release = lambda: \
            None
        
        action_delayed = lambda: \
            self.__view.set_track_clear_state(self.__track_number, False)

        self.__clear_track_handler = updateable.DelayedActionHandler(action_click,
                                                                     action_release,
                                                                     action_delayed,
                                                                     0.25)
        self.__context_provider.get_updateable_mux().add_updateable(self.__clear_track_handler)

    def on_init_script(self):
        self.reset_track_params()
        if self.__is_gui_active == True:
            self.__view.update_sample_length(self.__sample_length)
        self.set_track_volume(fl_helper.MAX_VOLUME_LEVEL_VALUE, True)
        self.set_track_hp_filter_level(fl_helper.MIN_LEVEL_VALUE, True)
        self.set_track_lp_filter_level(fl_helper.MAX_LEVEL_VALUE, True)
        self.set_track_pan(global_constants.DEFAULT_PANOMATIC_PAN_LEVEL, True)
        self.__view.set_track_clear_state(self.__track_number, 0.0)

    def __calculate_looper_fx1_mixer_channel(self):
        result = 0
        if self.__looper_number == constants.Looper_1:
            result = constants.LOOPER_1_FX_1_CHANNEL
        elif self.__looper_number == constants.Looper_2:
            result = constants.LOOPER_2_FX_1_CHANNEL
        elif self.__looper_number == constants.Looper_3:
            result = constants.LOOPER_3_FX_1_CHANNEL
        elif self.__looper_number == constants.Looper_4:
            result = constants.LOOPER_4_FX_1_CHANNEL
        return result

    def __calculate_looper_fx_1_channel(self):
        result = 0
        if self.__looper_number == constants.Looper_1:
            result = constants.LOOPER_1_FX_1_CHANNEL
        if self.__looper_number == constants.Looper_2:
            result = constants.LOOPER_2_FX_1_CHANNEL
        if self.__looper_number == constants.Looper_3:
            result = constants.LOOPER_3_FX_1_CHANNEL
        if self.__looper_number == constants.Looper_4:
            result = constants.LOOPER_4_FX_1_CHANNEL
        return result

    def set_looper_volume(self, looper_volume):
        # print("set_looper_volume: looper_volume - " + str(looper_volume))
        plugins.setParamValue(looper_volume, constants.PANOMATIC_VOLUME_PARAM_INDEX, self.__mixer_channel, constants.LOOPER_PANOMATIC_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_track_volume(self, track_volume, forward_to_device):
        self.__volume = track_volume
        plugins.setParamValue(track_volume, constants.PANOMATIC_VOLUME_PARAM_INDEX, self.__mixer_channel, constants.TRACK_PANOMATIC_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.__update_volume(forward_to_device)

    def set_track_hp_filter_level(self, hp_filter_level, forward_to_device):
        self.__hp_filter_level = hp_filter_level
        plugins.setParamValue(hp_filter_level != 0, constants.TRACK_FILTER_HP_R_ON_PARAMETER_INDEX, self.__mixer_channel, constants.TRACK_FILTER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(hp_filter_level, constants.TRACK_FILTER_HP_R_FREQ_PARAMETER_INDEX, self.__mixer_channel, constants.TRACK_FILTER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(hp_filter_level != 0, constants.TRACK_FILTER_HP_L_ON_PARAMETER_INDEX, self.__mixer_channel, constants.TRACK_FILTER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(hp_filter_level, constants.TRACK_FILTER_HP_L_FREQ_PARAMETER_INDEX, self.__mixer_channel, constants.TRACK_FILTER_SLOT_INDEX, midi.PIM_None, True)
        self.__update_hp_filter_level(forward_to_device)

    def set_track_lp_filter_level(self, lp_filter_level, forward_to_device):
        self.__lp_filter_level = lp_filter_level
        plugins.setParamValue(lp_filter_level != fl_helper.MAX_LEVEL_VALUE, constants.TRACK_FILTER_LP_R_ON_PARAMETER_INDEX, self.__mixer_channel, constants.TRACK_FILTER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(lp_filter_level, constants.TRACK_FILTER_LP_R_FREQ_PARAMETER_INDEX, self.__mixer_channel, constants.TRACK_FILTER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(lp_filter_level != fl_helper.MAX_LEVEL_VALUE, constants.TRACK_FILTER_LP_L_ON_PARAMETER_INDEX, self.__mixer_channel, constants.TRACK_FILTER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(lp_filter_level, constants.TRACK_FILTER_LP_L_FREQ_PARAMETER_INDEX, self.__mixer_channel, constants.TRACK_FILTER_SLOT_INDEX, midi.PIM_None, True)
        self.__update_lp_filter_level(forward_to_device)

    def get_track_volume(self):
        return self.__volume

    def clear(self, stop_recording=False):
        # print('Track:' + Track.clear.__name__ + ": stop_recording - " + str(stop_recording) + \
        #       ', looper_number - ' + str(self.__looper_number) + ',track_number - ' + str(self.__track_number))

        self.__clear_track_handler.click()

        if self.__recording_state == Track.RECORDING_STATE_RECORDING and stop_recording == True:
            self.stop_recording()

        plugins.setParamValue(1, constants.AUGUSTUS_LOOP_PLUGIN_CLEAR_LOOP_PARAM_INDEX,
                              self.__mixer_channel,
                              constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX,
                              midi.PIM_None, True)

        self.set_track_volume(fl_helper.MAX_VOLUME_LEVEL_VALUE, True)
        self.set_track_hp_filter_level(fl_helper.MIN_LEVEL_VALUE, True)
        self.set_track_lp_filter_level(fl_helper.MAX_LEVEL_VALUE, True)
        self.set_track_pan(global_constants.DEFAULT_PANOMATIC_PAN_LEVEL, True)

        if self.__recording_state == Track.RECORDING_STATE_PLAYBACK:
            self.__recording_state = Track.RECORDING_STATE_OFF
            if self.__is_gui_active == True:
                self.__view.set_track_recording_state(self.__track_number, self.__recording_state)
        elif self.__recording_state == Track.RECORDING_STATE_RECORDING:
            if stop_recording == True:
                self.__recording_state = Track.RECORDING_STATE_OFF
                if self.__is_gui_active == True:
                    self.__view.set_track_recording_state(self.__track_number, self.__recording_state)
                self.set_sample_length(SampleLength.LENGTH_0)
            else:
                if self.__recording_state != Track.RECORDING_STATE_RECORDING:
                    self.set_sample_length(SampleLength.LENGTH_0)
                else:
                    self.set_sample_length(self.__context_provider.get_sample_length())

        self.__clear_track_handler.release()

        self.set_track_selection_status(False)

    def reset_track_params(self):
        plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_TIME_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MIN_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_HOST_TEMPO_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_EFFECT_LEVEL_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_MASTER_FEEDBACK_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_DIGITAL_MODE_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_PITCH_INDEPENDENT_DELAY_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0 / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.33, constants.AUGUSTUS_LOOP_PLUGIN_SYNC_GROUP_MODE_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.1, constants.AUGUSTUS_LOOP_PLUGIN_LL_FEEDBACK_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.1, constants.AUGUSTUS_LOOP_PLUGIN_RR_FEEDBACK_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_SATURATION_ON_OFF_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

        # looper 1 is the source of the sidechain
        if self.__looper_number == constants.Looper_1:

            sidechain_filter_target_channel = constants.LOOPER_1_SIDECHAIN_FILTER_FIRST_CHANNEL + self.__track_number

            plugins.setParamValue(fl_helper.MAX_VOLUME_LEVEL_VALUE, constants.PEAK_CONTROLLER_BASE_PARAM_INDEX, sidechain_filter_target_channel, constants.LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(0.12, constants.PEAK_CONTROLLER_VOLUME_PARAM_INDEX, sidechain_filter_target_channel, constants.LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(constants.DEFAULT_TENSION_SIDECHAIN_LEVEL, constants.PEAK_CONTROLLER_TENSION_PARAM_INDEX, sidechain_filter_target_channel, constants.LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(constants.DEFAULT_DECAY_SIDECHAIN_LEVEL, constants.PEAK_CONTROLLER_DECAY_PARAM_INDEX, sidechain_filter_target_channel, constants.LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX, midi.PIM_None, True)

        self.set_sample_length(self.__sample_length, True)

    def set_sample_length(self, sample_length, unconditionally=False):

        if(sample_length != self.__sample_length or True == unconditionally):

            if sample_length != SampleLength.LENGTH_0:
                if(sample_length == SampleLength.LENGTH_128):
                    plugins.setParamValue((64 - 1.0) / 3599.0 , constants.AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                    plugins.setParamValue(64 / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                else:
                    plugins.setParamValue((sample_length - 1.0) / 3599.0 , constants.AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                    plugins.setParamValue(sample_length / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

                plugins.setParamValue(0.33, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(sample_length / 128.0, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

        self.__sample_length = sample_length

    def start_recording(self, sample_length):

        self.set_sample_length(sample_length)

        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

        if self.__recording_state != Track.RECORDING_STATE_PLAYBACK:
            plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_MASTER_FEEDBACK_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_LL_FEEDBACK_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_RR_FEEDBACK_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

        # important to have this statement here
        self.__recording_state = Track.RECORDING_STATE_RECORDING

        fl_helper.broadcast_midi_message(global_constants.LOOPER_MUX_MIDI_ID,
                                         global_constants.LOOPER_MUX_MIDI_CHAN,
                                         global_constants.LOOPER_MUX_START_RECORDING_MSG_DATA_1,
                                         global_constants.LOOPER_MUX_START_RECORDING_MSG_DATA_2)

        if self.__is_gui_active == True:
            self.__view.set_track_recording_state(self.__track_number, self.__recording_state)

    def stop_recording(self):

        if self.__recording_state == Track.RECORDING_STATE_RECORDING:
            plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

            if self.__is_gui_active == True:
                self.__view.set_track_recording_state(self.__track_number, Track.RECORDING_STATE_OFF)

            self.__recording_state = Track.RECORDING_STATE_PLAYBACK
            if self.__is_gui_active == True:
                self.__view.set_track_recording_state(self.__track_number, self.__recording_state)

            plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_MASTER_FEEDBACK_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(1.1, constants.AUGUSTUS_LOOP_PLUGIN_LL_FEEDBACK_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(1.1, constants.AUGUSTUS_LOOP_PLUGIN_RR_FEEDBACK_PARAM_INDEX, self.__mixer_channel, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def is_recording_in_progress(self):
        return self.__recording_state == Track.RECORDING_STATE_RECORDING

    def is_playback_in_progress(self):
        return self.__recording_state == Track.RECORDING_STATE_PLAYBACK

    def update_stats(self):
        if self.__is_gui_active == True:
            self.__view.set_track_recording_state(self.__track_number, self.__recording_state)

        self.__update_volume(True)
        self.__update_hp_filter_level(True)
        self.__update_lp_filter_level(True)
        self.__update_pan(True)

    def __update_volume(self, forward_to_device):
        if self.__is_gui_active == True:
            self.__view.set_track_volume(self.__track_number, self.__volume, forward_to_device)
            self.__view.set_track_muted(self.__track_number, self.__volume == 0)

    def __update_hp_filter_level(self, forward_to_device):
        if self.__is_gui_active == True:
            self.__view.set_hp_filter_level(self.__track_number, self.__hp_filter_level, forward_to_device)

    def __update_lp_filter_level(self, forward_to_device):
        if self.__is_gui_active == True:
            self.__view.set_lp_filter_level(self.__track_number, self.__lp_filter_level, forward_to_device)

    def __update_pan(self, forward_to_device):
        if self.__is_gui_active == True:
            self.__view.set_track_pan(self.__track_number, self.__pan, forward_to_device)

    def set_routing_level(self, routing_level):

        source_mixer_channel = constants.RECORDING_BUS_CHANNEL
        target_mixer_channel = self.__mixer_channel

        mixer.setRouteToLevel(source_mixer_channel, target_mixer_channel, routing_level)

    def set_gui_active(self, value):
        self.__is_gui_active = value
        
    def set_track_pan(self, pan, forward_to_device):
        self.__pan = pan
        plugins.setParamValue(pan, constants.PANOMATIC_PAN_PARAM_INDEX, self.__mixer_channel, constants.TRACK_PANOMATIC_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.__update_pan(forward_to_device)

    def __set_track_routing(self, source_channel, target_channel, routing_level):
        mixer.setRouteToLevel(source_channel, target_channel, routing_level)

    def set_track_selection_status(self, selection_status):
        self.__selection_status = selection_status

        if selection_status:
            self.__set_track_routing(self.__mixer_channel, constants.FX_UNIT_IN_CHANNEL, fl_helper.MAX_VOLUME_LEVEL_VALUE)
            self.__set_track_routing(self.__mixer_channel, self.__looper_fx_1_channel, 0)
        else:
            self.__set_track_routing(self.__mixer_channel, constants.FX_UNIT_IN_CHANNEL, 0)
            self.__set_track_routing(self.__mixer_channel, self.__looper_fx_1_channel, fl_helper.MAX_VOLUME_LEVEL_VALUE)
            
        self.__view.set_track_selection_status(self.__track_number, selection_status)

    def get_track_selection_status(self):
        return self.__selection_status