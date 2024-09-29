'''
Created on Feb 7, 2022

@author: Dream Machines
'''
import math

import midi
import plugins
import device

from looper_mux.resample_mode import ResampleMode
from looper_mux import constants
from common import fl_helper, global_constants
from looper_mux.sample_length import SampleLength
from looper_mux.track import Track
import common
from common import updateable

class View:
    def __init__(self):
        self.supported_sample_lengths = [
            SampleLength.LENGTH_1_64,
            SampleLength.LENGTH_1_32,
            SampleLength.LENGTH_1_16,
            SampleLength.LENGTH_1_8,
            SampleLength.LENGTH_1_4,
            SampleLength.LENGTH_1_2,
            SampleLength.LENGTH_1,
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

    def set_looper_volume(self, looper_index, looper_volume, forward_to_device):
        if forward_to_device:
            if looper_index == constants.Looper_1:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_LOOPER_VOLUME_1
                cc_number = constants.MIDI_CC_LOOPER_VOLUME_1
            elif looper_index == constants.Looper_2:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_LOOPER_VOLUME_2
                cc_number = constants.MIDI_CC_LOOPER_VOLUME_2
            elif looper_index == constants.Looper_3:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_LOOPER_VOLUME_3
                cc_number = constants.MIDI_CC_LOOPER_VOLUME_3
            elif looper_index == constants.Looper_4:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_LOOPER_VOLUME_4
                cc_number = constants.MIDI_CC_LOOPER_VOLUME_4

            device_value = int(looper_volume * fl_helper.MIDI_MAX_VALUE / fl_helper.MAX_VOLUME_LEVEL_VALUE)
    
            device.midiOutMsg(midi_id, channel, cc_number, device_value)

    def set_drop_fx_level(self, fx_level, midi_cc, midi_chan, forward_to_device):
        if forward_to_device:
            midi_id = midi.MIDI_CONTROLCHANGE
            value = int(fx_level * fl_helper.MIDI_MAX_VALUE)
            device.midiOutMsg(midi_id, midi_chan, midi_cc, value)

    def set_drop_btn_state(self, state):
        midi_id = midi.MIDI_CONTROLCHANGE
        channel = constants.MIDI_CH_DROP
        cc_number = constants.MIDI_CC_DROP
        value = int(state * fl_helper.MIDI_MAX_VALUE)
        device.midiOutMsg(midi_id, channel, cc_number, value)

    LOOPER_STATE_OFF      = 0
    LOOPER_STATE_PLAYING  = 66
    LOOPER_STATE_SELECTED = 90

    def set_looper_state(self, selected_looper, looper_state):

        if selected_looper == constants.Looper_1:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_LOOPER_1
            cc_number = constants.MIDI_CC_LOOPER_1
        elif selected_looper == constants.Looper_2:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_LOOPER_2
            cc_number = constants.MIDI_CC_LOOPER_2
        elif selected_looper == constants.Looper_3:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_LOOPER_3
            cc_number = constants.MIDI_CC_LOOPER_3
        elif selected_looper == constants.Looper_4:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_LOOPER_4
            cc_number = constants.MIDI_CC_LOOPER_4

        device.midiOutMsg(midi_id, channel, cc_number, looper_state)

    def set_sync_daw_transport_button_state(self, state):
        midi_id = midi.MIDI_CONTROLCHANGE
        channel = constants.MIDI_CH_SYNC_DAW_TRANSPORT
        cc_number = constants.MIDI_CC_SYNC_DAW_TRANSPORT
        value = state * fl_helper.MIDI_MAX_VALUE
        device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_clear_btn_state(self, state):

        midi_id = midi.MIDI_CONTROLCHANGE
        channel = constants.MIDI_CH_CLEAR
        cc_number = constants.MIDI_CC_CLEAR

        value = 0

        if state == updateable.DoubleClickTimeoutHandler.STATE_INITITAL:
            value = 0
        if state == updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_DONE:
            value = 25
        if state == updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_RELEASED:
            value = 13
        if state == updateable.DoubleClickTimeoutHandler.STATE_SECOND_CLICK_DONE:
            value = 1

        device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_extra_1_state(self, value, forward_to_device):
        if True == forward_to_device:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_EXTRA_1
            cc_number = constants.MIDI_CC_EXTRA_1

            normalized_value = int(value * fl_helper.MIDI_MAX_VALUE)
    
            device.midiOutMsg(midi_id, channel, cc_number, normalized_value)

    def set_track_volume(self, track_index, track_volume, forward_to_device):
        if True == forward_to_device:
            if track_index == constants.Track_1:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_VOLUME_1
                cc_number = constants.MIDI_CC_TRACK_VOLUME_1
            elif track_index == constants.Track_2:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_VOLUME_2
                cc_number = constants.MIDI_CC_TRACK_VOLUME_2
            elif track_index == constants.Track_3:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_VOLUME_3
                cc_number = constants.MIDI_CC_TRACK_VOLUME_3
            elif track_index == constants.Track_4:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_VOLUME_4
                cc_number = constants.MIDI_CC_TRACK_VOLUME_4
        
            value = int(track_volume * fl_helper.MIDI_MAX_VALUE / fl_helper.MAX_VOLUME_LEVEL_VALUE)
    
            device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_track_pan(self, track_index, pan, forward_to_device):
        if forward_to_device:
            if track_index == constants.Track_1:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_PAN_1
                cc_number = constants.MIDI_CC_TRACK_PAN_1
            elif track_index == constants.Track_2:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_PAN_2
                cc_number = constants.MIDI_CC_TRACK_PAN_2
            elif track_index == constants.Track_3:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_PAN_3
                cc_number = constants.MIDI_CC_TRACK_PAN_3
            elif track_index == constants.Track_4:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_PAN_4
                cc_number = constants.MIDI_CC_TRACK_PAN_4
        
            value = int(pan * fl_helper.MIDI_MAX_VALUE)
    
            device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_track_muted(self, track_index, track_muted):
        if track_index == constants.Track_1:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_MUTE_1
            cc_number = constants.MIDI_CC_TRACK_MUTE_1
        elif track_index == constants.Track_2:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_MUTE_2
            cc_number = constants.MIDI_CC_TRACK_MUTE_2
        elif track_index == constants.Track_3:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_MUTE_3
            cc_number = constants.MIDI_CC_TRACK_MUTE_3
        elif track_index == constants.Track_4:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_MUTE_4
            cc_number = constants.MIDI_CC_TRACK_MUTE_4
    
        value = fl_helper.MIDI_MAX_VALUE if track_muted else 0
        device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_looper_muted(self, looper_index, looper_muted):
        if looper_index == constants.Track_1:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_LOOPER_MUTE_1
            cc_number = constants.MIDI_CC_LOOPER_MUTE_1
        elif looper_index == constants.Track_2:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_LOOPER_MUTE_2
            cc_number = constants.MIDI_CC_LOOPER_MUTE_2
        elif looper_index == constants.Track_3:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_LOOPER_MUTE_3
            cc_number = constants.MIDI_CC_LOOPER_MUTE_3
        elif looper_index == constants.Track_4:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_LOOPER_MUTE_4
            cc_number = constants.MIDI_CC_LOOPER_MUTE_4
    
        value = fl_helper.MIDI_MAX_VALUE if looper_muted else 0
        device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_start_btn_state(self, value):
        midi_id = midi.MIDI_CONTROLCHANGE
        channel = constants.MIDI_CH_START
        cc_number = constants.MIDI_CC_START
        device_value = int(value * fl_helper.MIDI_MAX_VALUE)

        device.midiOutMsg(midi_id, channel, cc_number, device_value)

    def set_looper_side_chain_level(self, track_id, sidechain_level):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_L_S_CH", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

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

    def set_track_recording_state(self, track_index, recording_state):
        if track_index == constants.Track_1:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_RECORD_1
            cc_number = constants.MIDI_CC_TRACK_RECORD_1
        elif track_index == constants.Track_2:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_RECORD_2
            cc_number = constants.MIDI_CC_TRACK_RECORD_2
        elif track_index == constants.Track_3:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_RECORD_3
            cc_number = constants.MIDI_CC_TRACK_RECORD_3
        elif track_index == constants.Track_4:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_RECORD_4
            cc_number = constants.MIDI_CC_TRACK_RECORD_4

        device.midiOutMsg(midi_id, channel, cc_number, int(recording_state))

    def set_track_resampling_state(self, track_id, recording_state):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_Resampling", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(recording_state, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_track_clear_state(self, track_index, clear_state):
        # print("set_track_clear_state: track_index - " + str(track_index) + ", recording_state - " + str(clear_state))
        if track_index == constants.Track_1:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_CLEAR_1
            cc_number = constants.MIDI_CC_TRACK_CLEAR_1
        elif track_index == constants.Track_2:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_CLEAR_2
            cc_number = constants.MIDI_CC_TRACK_CLEAR_2
        elif track_index == constants.Track_3:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_CLEAR_3
            cc_number = constants.MIDI_CC_TRACK_CLEAR_3
        elif track_index == constants.Track_4:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_CLEAR_4
            cc_number = constants.MIDI_CC_TRACK_CLEAR_4
    
        value = int(clear_state * fl_helper.MIDI_MAX_VALUE)
        device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_clear_looper_btn_state(self, state):

        midi_id = midi.MIDI_CONTROLCHANGE
        channel = constants.MIDI_CH_CLEAR_LOOPER
        cc_number = constants.MIDI_CC_CLEAR_LOOPER

        value = 0

        if state == updateable.DoubleClickTimeoutHandler.STATE_INITITAL:
            value = 0
        if state == updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_DONE:
            value = 25
        if state == updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_RELEASED:
            value = 13
        if state == updateable.DoubleClickTimeoutHandler.STATE_SECOND_CLICK_DONE:
            value = 1

        device.midiOutMsg(midi_id, channel, cc_number, value)

    def update_sample_length(self, sample_length):

        duplicates_prevention = {}

        for i_sample_length in self.supported_sample_lengths:

            skip = False

            if i_sample_length == SampleLength.LENGTH_1_64:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_1_64
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_1_64
            elif i_sample_length == SampleLength.LENGTH_1_32:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_1_32
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_1_32
            elif i_sample_length == SampleLength.LENGTH_1_16:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_1_16
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_1_16
            elif i_sample_length == SampleLength.LENGTH_1_8:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_1_8
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_1_8
            elif i_sample_length == SampleLength.LENGTH_1_4:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_1_4
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_1_4
            elif i_sample_length == SampleLength.LENGTH_1_2:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_1_2
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_1_2
            elif i_sample_length == SampleLength.LENGTH_1:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_1
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_1
            elif i_sample_length == SampleLength.LENGTH_2 or i_sample_length == SampleLength.LENGTH_3:
                if duplicates_prevention.get(SampleLength.LENGTH_2, False) or \
                duplicates_prevention.get(SampleLength.LENGTH_3, False):
                    skip = True
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_2
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_2
            elif i_sample_length == SampleLength.LENGTH_4 or i_sample_length == SampleLength.LENGTH_6:
                if duplicates_prevention.get(SampleLength.LENGTH_4, False) or \
                duplicates_prevention.get(SampleLength.LENGTH_6, False):
                    skip = True
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_4
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_4
            elif i_sample_length == SampleLength.LENGTH_8 or i_sample_length == SampleLength.LENGTH_12:
                if duplicates_prevention.get(SampleLength.LENGTH_8, False) or \
                duplicates_prevention.get(SampleLength.LENGTH_12, False):
                    skip = True
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_8
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_8
            elif i_sample_length == SampleLength.LENGTH_16 or i_sample_length == SampleLength.LENGTH_24:
                if duplicates_prevention.get(SampleLength.LENGTH_16, False) or \
                duplicates_prevention.get(SampleLength.LENGTH_24, False):
                    skip = True
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_16
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_16
            elif i_sample_length == SampleLength.LENGTH_32 or i_sample_length == SampleLength.LENGTH_48:
                if duplicates_prevention.get(SampleLength.LENGTH_32, False) or \
                duplicates_prevention.get(SampleLength.LENGTH_48, False):
                    skip = True
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_32
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_32
            elif i_sample_length == SampleLength.LENGTH_64 or i_sample_length == SampleLength.LENGTH_96:
                if duplicates_prevention.get(SampleLength.LENGTH_64, False) or \
                duplicates_prevention.get(SampleLength.LENGTH_96, False):
                    skip = True
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_64
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_64
            elif i_sample_length == SampleLength.LENGTH_128:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_SAMPLE_LENGTH_128
                cc_number = constants.MIDI_CC_SAMPLE_LENGTH_128

            value = 0

            if sample_length == i_sample_length:
                value = 1 * fl_helper.MIDI_MAX_VALUE

            duplicates_prevention[i_sample_length] = value

            if not skip:
                device.midiOutMsg(midi_id, channel, cc_number, value)
    

    def set_tempo(self, tempo, forward_to_device):
        if True == forward_to_device:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TEMPO
            cc_number = constants.MIDI_CC_TEMPO
            value = int(( ( tempo - constants.MIN_TEMPO ) / ( constants.MAX_TEMPO - constants.MIN_TEMPO ) ) * fl_helper.MIDI_MAX_VALUE)
            device.midiOutMsg(midi_id, channel, cc_number, value)

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
