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
from looper_mux.resample_mode import ResampleMode
from common import fl_helper, global_constants
from common import updateable


class Track():

    RECORDING_STATE_OFF       = 0
    RECORDING_STATE_RECORDING = 1
    RECORDING_STATE_PLAYBACK  = 37

    def __init__(self, looper_number, track_number, mixer_track, view, context_provider):
        self.__view = view
        self.__looper_number = looper_number
        self.__track_number = track_number
        self.__mixer_track = mixer_track
        self.__sample_length = SampleLength.LENGTH_0
        self.__resample_mode = ResampleMode.NONE
        self.__volume = fl_helper.MAX_VOLUME_LEVEL_VALUE
        self.__recording_state = Track.RECORDING_STATE_OFF
        self.__context_provider = context_provider
        self.__is_gui_active = False
        self.__pan = global_constants.DEFAULT_PANOMATIC_PAN_LEVEL

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
        self.set_track_pan(global_constants.DEFAULT_PANOMATIC_PAN_LEVEL, True)
        self.__view.set_track_clear_state(self.__track_number, 0.0)

    def get_resample_mode(self):
        return self.__resample_mode

    def set_looper_volume(self, looper_volume):
        # print("set_looper_volume: looper_volume - " + str(looper_volume))
        plugins.setParamValue(looper_volume, constants.PANOMATIC_VOLUME_PARAM_INDEX, self.__mixer_track, constants.LOOPER_PANOMATIC_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_track_volume(self, track_volume, forward_to_device):
        self.__volume = track_volume
        plugins.setParamValue(track_volume, constants.PANOMATIC_VOLUME_PARAM_INDEX, self.__mixer_track, constants.TRACK_PANOMATIC_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.__update_volume(forward_to_device)

    def get_track_volume(self):
        return self.__volume

    def __set_track_volume_activation(self, track_volume_activation):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "T" + str(self.__track_number + 1) + "VA", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(track_volume_activation, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def __set_resample_audio_routing_level(self, param_name, param_value):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, param_name, constants.RESAMPLING_AUDIO_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(param_value, parameter_id, constants.MASTER_CHANNEL, constants.RESAMPLING_AUDIO_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def clear(self, stop_recording=False):
        # print('Track:' + Track.clear.__name__ + ": stop_recording - " + str(stop_recording) + \
        #       ', looper_number - ' + str(self.__looper_number) + ',track_number - ' + str(self.__track_number))

        self.__clear_track_handler.click()

        if self.__recording_state == Track.RECORDING_STATE_RECORDING and stop_recording == True:
            self.stop_recording()

        plugins.setParamValue(1, constants.AUGUSTUS_LOOP_PLUGIN_CLEAR_LOOP_PARAM_INDEX,
                              self.__mixer_track,
                              constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX,
                              midi.PIM_None, True)

        self.set_track_volume(fl_helper.MAX_VOLUME_LEVEL_VALUE, True)
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
                self.__set_track_volume_activation(1.0)
                self.set_sample_length(SampleLength.LENGTH_0)
            else:
                if self.__recording_state != Track.RECORDING_STATE_RECORDING:
                    self.__set_track_volume_activation(1.0)
                    self.set_sample_length(SampleLength.LENGTH_0)
                else:
                    self.set_sample_length(self.__context_provider.get_sample_length())

        self.__clear_track_handler.release()

    def __reset_routing(self):
        for track_number in range(0, 4):
            self.__set_resample_audio_routing_level("L" + str(self.__looper_number + 1) + "T" + str(track_number + 1) + "_FX1", constants.DEFAULT_AUDIO_ROUTING_LEVEL)
            self.__set_resample_audio_routing_level("L" + str(self.__looper_number+ 1) + "T" + str(track_number + 1) + "_LA", 0.0)

        self.__set_resample_audio_routing_level("L" + str(self.__looper_number + 1) + "_LA", constants.DEFAULT_AUDIO_ROUTING_LEVEL)
        self.__set_resample_audio_routing_level("L" + str(self.__looper_number + 1) + "_RBF", 0.0)
        self.__set_resample_audio_routing_level("LA_FX1", constants.DEFAULT_AUDIO_ROUTING_LEVEL)
        self.__set_resample_audio_routing_level("LA_RBF", 0.0)

    def reset_track_params(self):
        plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_TIME_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MIN_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_HOST_TEMPO_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_EFFECT_LEVEL_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_MASTER_FEEDBACK_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_DIGITAL_MODE_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_PITCH_INDEPENDENT_DELAY_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0 / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.33, constants.AUGUSTUS_LOOP_PLUGIN_SYNC_GROUP_MODE_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.1, constants.AUGUSTUS_LOOP_PLUGIN_LL_FEEDBACK_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.1, constants.AUGUSTUS_LOOP_PLUGIN_RR_FEEDBACK_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_SATURATION_ON_OFF_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.__reset_routing()

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
                    plugins.setParamValue((64 - 1.0) / 3599.0 , constants.AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                    plugins.setParamValue(64 / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                else:
                    plugins.setParamValue((sample_length - 1.0) / 3599.0 , constants.AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                    plugins.setParamValue(sample_length / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

                plugins.setParamValue(0.33, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(sample_length / 128.0, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

        self.__sample_length = sample_length

    def start_recording(self, sample_length, resample_mode):

        self.set_sample_length(sample_length)
        self.__set_resample_mode(resample_mode)

        self.__set_track_volume_activation(0.0)

        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

        if ResampleMode.FROM_LOOPER_TO_TRACK != ResampleMode.NONE:
            if ResampleMode.FROM_LOOPER_TO_TRACK == self.get_resample_mode():
                for looper_number in range(0, 4):
                    for track_number in range(0, 4):
                        if looper_number != self.__looper_number:
                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_FX1", constants.DEFAULT_AUDIO_ROUTING_LEVEL)
                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_LA", 0.0)
                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_ALA", 0.0)
                        else:
                            if track_number == self.__track_number:
                                self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_FX1", 0.0)
                                self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_LA", constants.DEFAULT_AUDIO_ROUTING_LEVEL)
                                self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_ALA", 0.0)
                            else:
                                self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_FX1", constants.DEFAULT_AUDIO_ROUTING_LEVEL)
                                self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_LA", 0.0)
                                self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_ALA", 0.0)

                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "_LA", 0.0)
                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "_RBF", constants.DEFAULT_AUDIO_ROUTING_LEVEL)

            elif ResampleMode.FROM_ALL_LOOPERS_TO_TRACK == self.get_resample_mode():
                for looper_number in range(0, 4):
                    for track_number in range(0, 4):
                        if looper_number != self.__looper_number:
                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_FX1", constants.DEFAULT_AUDIO_ROUTING_LEVEL)
                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_LA", 0.0)
                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_ALA", 0.0)
                        else:
                            if track_number == self.__track_number:
                                self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_FX1", 0.0)
                                self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_LA", 0.0)
                                self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_ALA", constants.DEFAULT_AUDIO_ROUTING_LEVEL)
                            else:
                                self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_FX1", constants.DEFAULT_AUDIO_ROUTING_LEVEL)
                                self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_LA", 0.0)
                                self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_ALA", 0.0)

                self.__set_resample_audio_routing_level("LA_FX1", 0.0)
                self.__set_resample_audio_routing_level("LA_RBF", constants.DEFAULT_AUDIO_ROUTING_LEVEL)

        if self.__recording_state != Track.RECORDING_STATE_PLAYBACK:
            plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_MASTER_FEEDBACK_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_LL_FEEDBACK_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_RR_FEEDBACK_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

        # important to have this statement here
        self.__recording_state = Track.RECORDING_STATE_RECORDING

        fl_helper.broadcast_midi_message(global_constants.LOOPER_MUX_MIDI_ID,
                                         global_constants.LOOPER_MUX_MIDI_CHAN,
                                         global_constants.LOOPER_MUX_START_RECORDING_MSG_DATA_1,
                                         global_constants.LOOPER_MUX_START_RECORDING_MSG_DATA_2)

        if self.get_resample_mode() == ResampleMode.NONE:
            if self.__is_gui_active == True:
                self.__view.set_track_recording_state(self.__track_number, self.__recording_state)
        else:
            self.clear()
            if self.__is_gui_active == True:
                self.__view.set_track_resampling_state(self.__track_number, self.__recording_state)

    def stop_recording(self):

        if self.__recording_state == Track.RECORDING_STATE_RECORDING:
            plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

            self.__set_track_volume_activation(1.0)

            if ResampleMode.FROM_LOOPER_TO_TRACK != ResampleMode.NONE:
                if ResampleMode.FROM_LOOPER_TO_TRACK == self.get_resample_mode():
                    for looper_number in range(0, 4):
                        for track_number in range(0, 4):
                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_FX1", constants.DEFAULT_AUDIO_ROUTING_LEVEL)
                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_LA", 0.0)
                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_ALA", 0.0)
    
                    self.__set_resample_audio_routing_level("L" + str(self.__looper_number + 1) + "_LA", constants.DEFAULT_AUDIO_ROUTING_LEVEL)
                    self.__set_resample_audio_routing_level("L" + str(self.__looper_number + 1) + "_RBF", 0.0)
    
                elif ResampleMode.FROM_ALL_LOOPERS_TO_TRACK == self.get_resample_mode():
                    for looper_number in range(0, 4):
                        for track_number in range(0, 4):
                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_FX1", constants.DEFAULT_AUDIO_ROUTING_LEVEL)
                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_LA", 0.0)
                            self.__set_resample_audio_routing_level("L" + str(looper_number + 1) + "T" + str(track_number + 1) + "_ALA", 0.0)
    
                    self.__set_resample_audio_routing_level("LA_FX1", constants.DEFAULT_AUDIO_ROUTING_LEVEL)
                    self.__set_resample_audio_routing_level("LA_RBF", 0.0)
    
            if self.get_resample_mode() == ResampleMode.NONE:
                if self.__is_gui_active == True:
                    self.__view.set_track_recording_state(self.__track_number, Track.RECORDING_STATE_OFF)
            else:
                if self.__is_gui_active == True:
                    self.__view.set_track_resampling_state(self.__track_number, 0.0)

            self.__set_resample_mode(ResampleMode.NONE)

            self.__recording_state = Track.RECORDING_STATE_PLAYBACK
            if self.__is_gui_active == True:
                self.__view.set_track_recording_state(self.__track_number, self.__recording_state)

            plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_MASTER_FEEDBACK_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(1.1, constants.AUGUSTUS_LOOP_PLUGIN_LL_FEEDBACK_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(1.1, constants.AUGUSTUS_LOOP_PLUGIN_RR_FEEDBACK_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def is_recording_in_progress(self):
        return self.__recording_state == Track.RECORDING_STATE_RECORDING

    def is_playback_in_progress(self):
        return self.__recording_state == Track.RECORDING_STATE_PLAYBACK

    def update_stats(self):
        if self.__is_gui_active == True:
            self.__view.set_track_recording_state(self.__track_number, self.__recording_state)
            self.__view.set_track_resampling_state(self.__track_number, 0.0)

        self.__update_volume(True)
        self.__update_pan(True)

    def __update_volume(self, forward_to_device):
        if self.__is_gui_active == True:
            self.__view.set_track_volume(self.__track_number, self.__volume, forward_to_device)
            self.__view.set_track_muted(self.__track_number, self.__volume == 0)

    def __update_pan(self, forward_to_device):
        if self.__is_gui_active == True:
            self.__view.set_track_pan(self.__track_number, self.__pan, forward_to_device)

    def __set_resample_mode(self, resample_mode):
        self.__resample_mode = resample_mode

    def set_routing_level(self, routing_level):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "T" + str(self.__track_number + 1), constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(routing_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_gui_active(self, value):
        self.__is_gui_active = value
        
    def set_track_pan(self, pan, forward_to_device):
        self.__pan = pan
        plugins.setParamValue(pan, constants.PANOMATIC_PAN_PARAM_INDEX, self.__mixer_track, constants.TRACK_PANOMATIC_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.__update_pan(forward_to_device)