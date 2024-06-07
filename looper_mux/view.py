'''
Created on Feb 7, 2022

@author: Dream Machines
'''
import math

import midi
import plugins

from looper_mux.resample_mode import ResampleMode
from looper_mux import constants
from common import fl_helper
from looper_mux.sample_length import SampleLength

class View:
    def __init__(self):
        self.supported_sample_lengths = [SampleLength.LENGTH_1,
                                  SampleLength.LENGTH_2,
                                  SampleLength.LENGTH_3,
                                  SampleLength.LENGTH_4,
                                  SampleLength.LENGTH_6,
                                  SampleLength.LENGTH_8,
                                  SampleLength.LENGTH_12,
                                  SampleLength.LENGTH_16,
                                  SampleLength.LENGTH_24,
                                  SampleLength.LENGTH_32,
                                  SampleLength.LENGTH_48,
                                  SampleLength.LENGTH_64,
                                  SampleLength.LENGTH_96,
                                  SampleLength.LENGTH_128]

    def set_shift_pressed_state(self, shift_pressed):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "Shift", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(shift_pressed, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.reset_toggle_flags()

    def set_looper_volume(self, looper_volume):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "Volume", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(looper_volume, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.reset_toggle_flags()

    def set_looper_activation_status(self, looper_id, looper_volume):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "Looper_" + str(looper_id + 1) + "_AS", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0 if looper_volume == 0.0 else 1.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_drop_intencity(self, drop_intencity):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "Drop FX", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(drop_intencity, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.reset_toggle_flags()

    def select_looper(self, selected_looper):

        for i in range(4):
            value = 0.0
            if i == selected_looper:
                value = 1.0

            parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "Looper " + str(i + 1), constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(value, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

        self.reset_toggle_flags()

    def clear(self):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "Clear all", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def __clear_off(self):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "Clear all", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def __clear_tracks_off(self):
        for i in range(constants.Track_4 + 1):
            parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(i + 1) + "_Clear", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(0.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_track_volume(self, track_index, track_volume):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_index + 1) + "_Volume", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(track_volume, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.reset_toggle_flags()

    def _p(self, value):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "Play", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(value, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.reset_toggle_flags()

    def set_looper_side_chain_level(self, track_id, sidechain_level):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_L_S_CH", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.reset_toggle_flags()

    def set_resample_mode(self, resample_mode):

        resample_looper = 0.0
        resample_all_loopers = 0.0

        if resample_mode == ResampleMode.NONE:
            resample_looper = 0.0
            resample_all_loopers = 0.0
        elif resample_mode == ResampleMode.FROM_LOOPER_TO_TRACK:
            resample_looper = 1.0
            resample_all_loopers = 0.0
        elif resample_mode == ResampleMode.FROM_ALL_LOOPERS_TO_TRACK:
            resample_looper = 0.0
            resample_all_loopers = 1.0

        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "Resample selected looper", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(resample_looper, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "Resample all loopers", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(resample_all_loopers, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

        self.reset_toggle_flags()

    def set_track_recording_state(self, track_id, recording_state):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_Recording", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(recording_state, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

        self.reset_toggle_flags()

    def set_track_resampling_state(self, track_id, recording_state):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_Resampling", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(recording_state, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

        self.reset_toggle_flags()

    def set_track_clear_state(self, track_id, recording_state):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_Clear", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(recording_state, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_track_playback_state(self, track_id, recording_state):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_Playback", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(recording_state, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

        self.reset_toggle_flags()

    def reset_toggle_flags(self):
        self.__clear_off()
        self.__clear_tracks_off()

    def update_sample_length(self, sample_length):
        for i_sample_length in self.supported_sample_lengths:
            parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "Length_" + str(i_sample_length), constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)

            value = 0

            if(sample_length == i_sample_length):
                value = 1

            plugins.setParamValue(value, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_tempo(self, tempo):
        tempo_hundred = int(tempo) // 100
        tempo_dozens = (tempo % 100) // 10
        tempo_units = (tempo % 10)

        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "TH", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(tempo_hundred / 10, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "TD", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(tempo_dozens / 10, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "TU", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(tempo_units / 10, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_track_sample_length(self, track_id, sample_length):
        sample_length_hundred = int(sample_length) // 100
        sample_length_dozens = (sample_length % 100) // 10
        sample_length_units = (sample_length % 10)

        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "H", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sample_length_hundred / 10, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "D", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sample_length_dozens / 10, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "U", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sample_length_units / 10, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_turnado_dictator_level(self, turnado_dictator_level):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T_D", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(turnado_dictator_level, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_turnado_dry_wet_level(self, turnado_dry_wet_level):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T_DW", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(turnado_dry_wet_level, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def switch_to_next_turnado_preset(self):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T_Next_Preset", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def switch_to_prev_turnado_preset(self):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T_Previous_Preset", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_tension_side_chain_level(self, track_id, sidechain_level):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_ST", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_decay_side_chain_level(self, track_id, sidechain_level):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_SD", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_prolonged_record_length_mode(self, status):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "x1.5 length", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(status, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
