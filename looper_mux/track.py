'''
Created on Feb 7, 2022

@author: Dream Machines
'''

import midi
import plugins
import mixer

from looper_mux import constants
from looper_mux.sample_length import SampleLength
from looper_mux.resample_mode import ResampleMode
from common import fl_helper

class Track():

    def __init__(self, looper_number, track_number, mixer_track, view, context_provider):
        self.__view                   = view
        self.__looper_number          = looper_number
        self.__track_number           = track_number
        self.__mixer_track            = mixer_track
        self.__sample_length          = SampleLength.LENGTH_0
        self.__resample_mode          = ResampleMode.NONE
        self.__volume                 = fl_helper.MAX_VOLUME_LEVEL_VALUE
        self.__is_playback_active       = False
        self.__is_recording_in_progress  = False
        self.__context_provider       = context_provider

    def on_init_script(self):
        self.reset_track_params()
        self.__view.update_sample_length(self.__sample_length)
        self.set_track_volume(fl_helper.MAX_VOLUME_LEVEL_VALUE)

    def get_resample_mode(self):
        return self.__resample_mode

    def set_looper_volume(self, looper_volume):
        mixer.setTrackVolume(self.__mixer_track, looper_volume)

    def set_track_volume(self, track_volume):
        self.__volume = track_volume
        plugins.setParamValue(track_volume, constants.PANOMATIC_VOLUME_PARAM_INDEX, self.__mixer_track, constants.TRACK_PANOMATIC_VOLUME_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.update_volume()

    def get_track_volume(self):
        return self.__volume

    def __set_track_volume_activation(self, track_volume_activation):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "T" + str(self.__track_number + 1) + "VA", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(track_volume_activation, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def clear(self, stop_recording = False):
        plugins.setParamValue(1, constants.AUGUSTUS_LOOP_PLUGIN_CLEAR_LOOP_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.set_track_volume(fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.__view.set_track_clear_state(self.__track_number, 1.0)

        self.__is_playback_active = False
        self.__view.set_track_playback_state(self.__track_number, self.__is_playback_active)

        if stop_recording == True:
            self.__is_recording_in_progress  = False
            self.__view.set_track_recording_state(self.__track_number, self.__is_recording_in_progress)
            self.__set_track_volume_activation(1.0)
            self.set_sample_length(SampleLength.LENGTH_0)
        else:
            if False == self.__is_recording_in_progress:
                self.__set_track_volume_activation(1.0)
                self.set_sample_length(SampleLength.LENGTH_0)
            else:
                self.set_sample_length(self.__context_provider.get_sample_length())

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

        # looper 1 is the source of the sidechain
        if self.__looper_number == constants.Looper_1:
            plugins.setParamValue(fl_helper.MAX_VOLUME_LEVEL_VALUE, constants.PEAK_CONTROLLER_BASE_PARAM_INDEX, self.__mixer_track, constants.LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(0.12, constants.PEAK_CONTROLLER_VOLUME_PARAM_INDEX, self.__mixer_track, constants.LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(0.85, constants.PEAK_CONTROLLER_TENSION_PARAM_INDEX, self.__mixer_track, constants.LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(0.5, constants.PEAK_CONTROLLER_DECAY_PARAM_INDEX, self.__mixer_track, constants.LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX, midi.PIM_None, True)

        self.__set_routing();

        self.set_sample_length(self.__sample_length, True)

    def set_sample_length(self, sample_length, unconditionally = False):

        if(sample_length != self.__sample_length or True == unconditionally):

            self.__is_playback_active = False
            self.__view.set_track_playback_state(self.__track_number, self.__is_playback_active)

            self.__view.set_track_sample_length(self.__track_number, sample_length)

            if(sample_length == SampleLength.LENGTH_1):
                plugins.setParamValue((1.0 - 1.0) / 3599.0 , constants.AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(1.0 / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(0.33, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(1.0/128.0, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            elif(sample_length == SampleLength.LENGTH_2):
                plugins.setParamValue((2.0 - 1.0) / 3599.0 , constants.AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(2.0 / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(0.33, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(2.0/128.0, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            elif(sample_length == SampleLength.LENGTH_4):
                plugins.setParamValue((4.0 - 1.0) / 3599.0 , constants.AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(4.0 / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(0.33, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(4.0/128.0, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            elif(sample_length == SampleLength.LENGTH_8):
                plugins.setParamValue((8.0 - 1.0) / 3599.0 , constants.AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(8.0 / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(0.33, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(8.0/128.0, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            elif(sample_length == SampleLength.LENGTH_16):
                plugins.setParamValue((16.0 - 1.0) / 3599.0 , constants.AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(16.0 / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(0.33, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(16.0/128.0, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            elif(sample_length == SampleLength.LENGTH_32):
                plugins.setParamValue((32.0 - 1.0) / 3599.0 , constants.AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(32.0 / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(0.33, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(32.0/128.0, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            elif(sample_length == SampleLength.LENGTH_64):
                plugins.setParamValue((64.0 - 1.0) / 3599.0 , constants.AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(64.0 / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(0.33, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(64.0/128.0, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
            elif(sample_length == SampleLength.LENGTH_128):
                plugins.setParamValue((64.0 - 1.0) / 3599.0 , constants.AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(64.0 / 3600.0, constants.AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(0.33, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
                plugins.setParamValue(128.0/128.0, constants.AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

        self.__sample_length = sample_length

    def start_recording(self, sample_length, resample_mode):

        self.set_sample_length(sample_length)
        self.__set_resample_mode(resample_mode)

        self.__set_track_volume_activation(0.0)

        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

        if ResampleMode.FROM_LOOPER_TO_TRACK == self.get_resample_mode():

            if self.__looper_number == constants.Looper_1:
                mixer.setRouteTo(constants.LOOPER_1_CHANNEL, constants.LOOPER_ALL_CHANNEL, 0)
                mixer.setRouteTo(self.__mixer_track, constants.LOOPER_1_FX_1_CHANNEL, 0)
                mixer.setRouteTo(constants.LOOPER_1_CHANNEL, self.__mixer_track, 1)
            elif self.__looper_number == constants.Looper_2:
                mixer.setRouteTo(constants.LOOPER_2_CHANNEL, constants.LOOPER_ALL_CHANNEL, 0)
                mixer.setRouteTo(self.__mixer_track, constants.LOOPER_2_FX_1_CHANNEL, 0)
                mixer.setRouteTo(constants.LOOPER_2_CHANNEL, self.__mixer_track, 1)
            elif self.__looper_number == constants.Looper_3:
                mixer.setRouteTo(constants.LOOPER_3_CHANNEL, constants.LOOPER_ALL_CHANNEL, 0)
                mixer.setRouteTo(self.__mixer_track, constants.LOOPER_3_FX_1_CHANNEL, 0)
                mixer.setRouteTo(constants.LOOPER_3_CHANNEL, self.__mixer_track, 1)
            elif self.__looper_number == constants.Looper_4:
                mixer.setRouteTo(constants.LOOPER_4_CHANNEL, constants.LOOPER_ALL_CHANNEL, 0)
                mixer.setRouteTo(self.__mixer_track, constants.LOOPER_4_FX_1_CHANNEL, 0)
                mixer.setRouteTo(constants.LOOPER_4_CHANNEL, self.__mixer_track, 1)

            mixer.setRouteTo(self.__mixer_track, constants.LOOPER_ALL_FX_1_CHANNEL, 1)

        elif ResampleMode.FROM_ALL_LOOPERS_TO_TRACK == self.get_resample_mode():

            if self.__looper_number == constants.Looper_1:
                mixer.setRouteTo(self.__mixer_track, constants.LOOPER_1_FX_1_CHANNEL, 0)
            elif self.__looper_number == constants.Looper_2:
                mixer.setRouteTo(self.__mixer_track, constants.LOOPER_2_FX_1_CHANNEL, 0)
            elif self.__looper_number == constants.Looper_3:
                mixer.setRouteTo(self.__mixer_track, constants.LOOPER_3_FX_1_CHANNEL, 0)
            elif self.__looper_number == constants.Looper_4:
                mixer.setRouteTo(self.__mixer_track, constants.LOOPER_4_FX_1_CHANNEL, 0)

            mixer.setRouteTo(constants.LOOPER_ALL_CHANNEL, constants.LOOPER_ALL_FX_1_CHANNEL, 0)
            mixer.setRouteTo(constants.LOOPER_ALL_CHANNEL, self.__mixer_track, 1)
            mixer.setRouteTo(self.__mixer_track, constants.LOOPER_ALL_FX_1_CHANNEL, 1)

        # important to have this statement here
        self.__is_recording_in_progress = True

        if self.get_resample_mode() == ResampleMode.NONE:
            self.__view.set_track_recording_state(self.__track_number, 1.0)
        else:
            self.clear()
            self.__view.set_track_resampling_state(self.__track_number, 1.0)

    def stop_recording(self):

        if self.__is_recording_in_progress == True:
            plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

            self.__set_track_volume_activation(1.0)

            if ResampleMode.FROM_LOOPER_TO_TRACK == self.get_resample_mode():

                mixer.setRouteTo(self.__mixer_track, constants.LOOPER_ALL_FX_1_CHANNEL, 0)

                if self.__looper_number == constants.Looper_1:
                    mixer.setRouteTo(constants.LOOPER_1_CHANNEL, self.__mixer_track, 0)
                    mixer.setRouteTo(self.__mixer_track, constants.LOOPER_1_FX_1_CHANNEL, 1)
                    mixer.setRouteTo(constants.LOOPER_1_CHANNEL, constants.LOOPER_ALL_CHANNEL, 1)
                elif self.__looper_number == constants.Looper_2:
                    mixer.setRouteTo(constants.LOOPER_2_CHANNEL, self.__mixer_track, 0)
                    mixer.setRouteTo(self.__mixer_track, constants.LOOPER_2_FX_1_CHANNEL, 1)
                    mixer.setRouteTo(constants.LOOPER_2_CHANNEL, constants.LOOPER_ALL_CHANNEL, 1)
                elif self.__looper_number == constants.Looper_3:
                    mixer.setRouteTo(constants.LOOPER_3_CHANNEL, self.__mixer_track, 0)
                    mixer.setRouteTo(self.__mixer_track, constants.LOOPER_3_FX_1_CHANNEL, 1)
                    mixer.setRouteTo(constants.LOOPER_3_CHANNEL, constants.LOOPER_ALL_CHANNEL, 1)
                elif self.__looper_number == constants.Looper_4:
                    mixer.setRouteTo(constants.LOOPER_4_CHANNEL, self.__mixer_track, 0)
                    mixer.setRouteTo(self.__mixer_track, constants.LOOPER_4_FX_1_CHANNEL, 1)
                    mixer.setRouteTo(constants.LOOPER_4_CHANNEL, constants.LOOPER_ALL_CHANNEL, 1)

            elif ResampleMode.FROM_ALL_LOOPERS_TO_TRACK == self.get_resample_mode():

                mixer.setRouteTo(self.__mixer_track, constants.LOOPER_ALL_FX_1_CHANNEL, 0)
                mixer.setRouteTo(constants.LOOPER_ALL_CHANNEL, self.__mixer_track, 0)

                if self.__looper_number == constants.Looper_1:
                    mixer.setRouteTo(self.__mixer_track, constants.LOOPER_1_FX_1_CHANNEL, 1)
                elif self.__looper_number == constants.Looper_2:
                    mixer.setRouteTo(self.__mixer_track, constants.LOOPER_2_FX_1_CHANNEL, 1)
                elif self.__looper_number == constants.Looper_3:
                    mixer.setRouteTo(self.__mixer_track, constants.LOOPER_3_FX_1_CHANNEL, 1)
                elif self.__looper_number == constants.Looper_4:
                    mixer.setRouteTo(self.__mixer_track, constants.LOOPER_4_FX_1_CHANNEL, 1)

                mixer.setRouteTo(constants.LOOPER_ALL_CHANNEL, constants.LOOPER_ALL_FX_1_CHANNEL, 1)

            if self.get_resample_mode() == ResampleMode.NONE:
                self.__view.set_track_recording_state(self.__track_number, 0.0)
            else:
                self.__view.set_track_resampling_state(self.__track_number, 0.0)

            self.__set_resample_mode(ResampleMode.NONE)

            self.__is_playback_active = True
            self.__view.set_track_playback_state(self.__track_number, self.__is_playback_active)

            self.__is_recording_in_progress = False


    def is_recording_in_progress(self):
        return self.__is_recording_in_progress

    def update_stats(self):

        self.__view.set_track_playback_state(self.__track_number, self.__is_playback_active)
        self.__view.set_track_sample_length(self.__track_number, self.__sample_length)

        self.__view.set_track_recording_state(self.__track_number, 0.0)
        self.__view.set_track_resampling_state(self.__track_number, 0.0)
        self.__view.set_track_clear_state(self.__track_number, 0.0)

        self.update_volume()

    def update_volume(self):
        self.__view.set_track_volume(self.__track_number, self.__volume)

    def __set_resample_mode(self, resample_mode):
        self.__resample_mode = resample_mode

    def __set_routing(self):
        mixer.setRouteTo(constants.MIC_ROUTE_CHANNEL, self.__mixer_track, 1)
        mixer.setRouteTo(constants.SYNTH_ROUTE_CHANNEL, self.__mixer_track, 1)

    def __remove_routing(self):
        mixer.setRouteTo(constants.MIC_ROUTE_CHANNEL, self.__mixer_track, 0)
        mixer.setRouteTo(constants.SYNTH_ROUTE_CHANNEL, self.__mixer_track, 0)

    def set_routing_level(self, routing_level):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "T" + str(self.__track_number + 1) + "M", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(routing_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "T" + str(self.__track_number + 1) + "S", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(routing_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_input_side_chain_level(self, sidechain_level):
        self.__view.set_input_side_chain_level(self.__track_number, sidechain_level)
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "M2L1T" + str(self.__track_number + 1) + "S", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "S2L1T" + str(self.__track_number + 1) + "S", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
