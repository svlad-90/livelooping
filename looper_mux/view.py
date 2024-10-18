'''
Created on Feb 7, 2022

@author: Dream Machines
'''
import math

import midi
import plugins
import device

from looper_mux import constants
from common import fl_helper, global_constants
from looper_mux.sample_length import SampleLength
from looper_mux.track import Track
import common
from common import updateable
from looper_mux import fx
from looper_mux.fx import FXBank, FXSlot
from looper_mux import repeater_constants

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
    LOOPER_STATE_SELECTED = 120

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

    def set_track_volume(self, track_id, track_volume, forward_to_device):
        if True == forward_to_device:
            if track_id == constants.Track_1:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_VOLUME_1
                cc_number = constants.MIDI_CC_TRACK_VOLUME_1
            elif track_id == constants.Track_2:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_VOLUME_2
                cc_number = constants.MIDI_CC_TRACK_VOLUME_2
            elif track_id == constants.Track_3:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_VOLUME_3
                cc_number = constants.MIDI_CC_TRACK_VOLUME_3
            elif track_id == constants.Track_4:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_VOLUME_4
                cc_number = constants.MIDI_CC_TRACK_VOLUME_4
        
            value = int(track_volume * fl_helper.MIDI_MAX_VALUE / fl_helper.MAX_VOLUME_LEVEL_VALUE)
    
            device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_track_pan(self, track_id, pan, forward_to_device):
        if forward_to_device:
            if track_id == constants.Track_1:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_PAN_1
                cc_number = constants.MIDI_CC_TRACK_PAN_1
            elif track_id == constants.Track_2:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_PAN_2
                cc_number = constants.MIDI_CC_TRACK_PAN_2
            elif track_id == constants.Track_3:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_PAN_3
                cc_number = constants.MIDI_CC_TRACK_PAN_3
            elif track_id == constants.Track_4:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_PAN_4
                cc_number = constants.MIDI_CC_TRACK_PAN_4
        
            value = int(pan * fl_helper.MIDI_MAX_VALUE)
    
            device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_hp_filter_level(self, track_id, hp_filter_level, forward_to_device):
        if forward_to_device:
            if track_id == constants.Track_1:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_1_HP_FILTER
                cc_number = constants.MIDI_CC_TRACK_1_HP_FILTER
            elif track_id == constants.Track_2:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_2_HP_FILTER
                cc_number = constants.MIDI_CC_TRACK_2_HP_FILTER
            elif track_id == constants.Track_3:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_3_HP_FILTER
                cc_number = constants.MIDI_CC_TRACK_3_HP_FILTER
            elif track_id == constants.Track_4:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_4_HP_FILTER
                cc_number = constants.MIDI_CC_TRACK_4_HP_FILTER
        
            value = int(hp_filter_level * fl_helper.MIDI_MAX_VALUE)
    
            device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_lp_filter_level(self, track_id, lp_filter_level, forward_to_device):
        if forward_to_device:
            if track_id == constants.Track_1:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_1_LP_FILTER
                cc_number = constants.MIDI_CC_TRACK_1_LP_FILTER
            elif track_id == constants.Track_2:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_2_LP_FILTER
                cc_number = constants.MIDI_CC_TRACK_2_LP_FILTER
            elif track_id == constants.Track_3:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_3_LP_FILTER
                cc_number = constants.MIDI_CC_TRACK_3_LP_FILTER
            elif track_id == constants.Track_4:
                midi_id = midi.MIDI_CONTROLCHANGE
                channel = constants.MIDI_CH_TRACK_4_LP_FILTER
                cc_number = constants.MIDI_CC_TRACK_4_LP_FILTER
        
            value = int(lp_filter_level * fl_helper.MIDI_MAX_VALUE)
    
            device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_track_muted(self, track_id, track_muted):
        if track_id == constants.Track_1:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_MUTE_1
            cc_number = constants.MIDI_CC_TRACK_MUTE_1
        elif track_id == constants.Track_2:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_MUTE_2
            cc_number = constants.MIDI_CC_TRACK_MUTE_2
        elif track_id == constants.Track_3:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_MUTE_3
            cc_number = constants.MIDI_CC_TRACK_MUTE_3
        elif track_id == constants.Track_4:
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

    def set_looper_side_chain_level(self, track_id, sidechain_level, forward_to_device):
        if track_id == constants.Track_1:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_SIDECHAIN_T1
            cc_number = constants.MIDI_CC_SIDECHAIN_T1
        elif track_id == constants.Track_2:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_SIDECHAIN_T2
            cc_number = constants.MIDI_CC_SIDECHAIN_T2
        elif track_id == constants.Track_3:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_SIDECHAIN_T3
            cc_number = constants.MIDI_CC_SIDECHAIN_T3
        elif track_id == constants.Track_4:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_SIDECHAIN_T4
            cc_number = constants.MIDI_CC_SIDECHAIN_T4

        value = int(sidechain_level * fl_helper.MIDI_MAX_VALUE)

        device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_track_recording_state(self, track_id, recording_state):
        if track_id == constants.Track_1:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_RECORD_1
            cc_number = constants.MIDI_CC_TRACK_RECORD_1
        elif track_id == constants.Track_2:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_RECORD_2
            cc_number = constants.MIDI_CC_TRACK_RECORD_2
        elif track_id == constants.Track_3:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_RECORD_3
            cc_number = constants.MIDI_CC_TRACK_RECORD_3
        elif track_id == constants.Track_4:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_RECORD_4
            cc_number = constants.MIDI_CC_TRACK_RECORD_4

        device.midiOutMsg(midi_id, channel, cc_number, int(recording_state))

    def set_track_clear_state(self, track_id, clear_state):
        # print("set_track_clear_state: track_id - " + str(track_id) + ", recording_state - " + str(clear_state))
        if track_id == constants.Track_1:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_CLEAR_1
            cc_number = constants.MIDI_CC_TRACK_CLEAR_1
        elif track_id == constants.Track_2:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_CLEAR_2
            cc_number = constants.MIDI_CC_TRACK_CLEAR_2
        elif track_id == constants.Track_3:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_TRACK_CLEAR_3
            cc_number = constants.MIDI_CC_TRACK_CLEAR_3
        elif track_id == constants.Track_4:
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

    def set_tension_side_chain_level(self, midi_channel, midi_cc, tension, forward_to_device):
        if forward_to_device:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = midi_channel
            cc_number = midi_cc
            value = int(tension * fl_helper.MIDI_MAX_VALUE)
            device.midiOutMsg(midi_id, channel, cc_number, value)


    def set_decay_side_chain_level(self, midi_channel, midi_cc, decay, forward_to_device):
        if forward_to_device:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = midi_channel
            cc_number = midi_cc
            value = int(decay * fl_helper.MIDI_MAX_VALUE)
            device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_track_selection_status(self, track_id, selection_status):
        midi_id = midi.MIDI_CONTROLCHANGE
        if track_id == constants.Track_1:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_SELECT_T1
            cc_number = constants.MIDI_CC_SELECT_T1
        elif track_id == constants.Track_2:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_SELECT_T2
            cc_number = constants.MIDI_CC_SELECT_T2
        elif track_id == constants.Track_3:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_SELECT_T3
            cc_number = constants.MIDI_CC_SELECT_T3
        elif track_id == constants.Track_4:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_SELECT_T4
            cc_number = constants.MIDI_CC_SELECT_T4

        value = int(selection_status * fl_helper.MIDI_MAX_VALUE)
        device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_fx_bank_status(self, bank_id, status):
        # print("set_fx_bank_status - bank_id - " + str(bank_id) + ", status - " + str(status))
        if bank_id == FXBank.BANK_1:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_BANK_1
            cc_number = constants.MIDI_CC_FX_BANK_1
        elif bank_id == FXBank.BANK_2:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_BANK_2
            cc_number = constants.MIDI_CC_FX_BANK_2
        elif bank_id == FXBank.BANK_3:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_BANK_3
            cc_number = constants.MIDI_CC_FX_BANK_3
        elif bank_id == FXBank.BANK_4:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_BANK_4
            cc_number = constants.MIDI_CC_FX_BANK_4
        elif bank_id == FXBank.BANK_5:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_BANK_5
            cc_number = constants.MIDI_CC_FX_BANK_5

        value = int(status * fl_helper.MIDI_MAX_VALUE)
        # print("set_fx_bank_status - midi_id - " + str(midi_id) + ", channel - " + str(channel) + ", cc_number - " + str(cc_number) + ", value - " + str(value))
        device.midiOutMsg(midi_id, channel, cc_number, value)

        if bank_id == FXBank.BANK_4:
            device.midiOutMsg(midi_id, channel, cc_number, value)
            device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_fx_slot_status(self, slot_id, status):
        # print("set_fx_bank_status - slot_id - " + str(slot_id) + ", status - " + str(status))
        if slot_id == FXSlot.SLOT_1:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_SLOT_1
            cc_number = constants.MIDI_CC_FX_SLOT_1
        elif slot_id == FXSlot.SLOT_2:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_SLOT_2
            cc_number = constants.MIDI_CC_FX_SLOT_2
        elif slot_id == FXSlot.SLOT_3:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_SLOT_3
            cc_number = constants.MIDI_CC_FX_SLOT_3
        elif slot_id == FXSlot.SLOT_4:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_SLOT_4
            cc_number = constants.MIDI_CC_FX_SLOT_4
        elif slot_id == FXSlot.SLOT_5:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_SLOT_5
            cc_number = constants.MIDI_CC_FX_SLOT_5
        elif slot_id == FXSlot.SLOT_6:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_SLOT_6
            cc_number = constants.MIDI_CC_FX_SLOT_6
        elif slot_id == FXSlot.SLOT_7:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_SLOT_7
            cc_number = constants.MIDI_CC_FX_SLOT_7
        elif slot_id == FXSlot.SLOT_8:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_SLOT_8
            cc_number = constants.MIDI_CC_FX_SLOT_8
        elif slot_id == FXSlot.SLOT_9:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_SLOT_9
            cc_number = constants.MIDI_CC_FX_SLOT_9
        elif slot_id == FXSlot.SLOT_10:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_SLOT_10
            cc_number = constants.MIDI_CC_FX_SLOT_10

        value = int(status * fl_helper.MIDI_MAX_VALUE)
        # print("set_fx_bank_status - midi_id - " + str(midi_id) + ", channel - " + str(channel) + ", cc_number - " + str(cc_number) + ", value - " + str(value))
        device.midiOutMsg(midi_id, channel, cc_number, value)

        if slot_id == FXSlot.SLOT_9:
            device.midiOutMsg(midi_id, channel, cc_number, value)
            device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_fx_dry_wet_level(self, dry_wet_level, forward_to_device):
        # print("set_fx_dry_wet_level - dry_wet_level - " + str(dry_wet_level) + ", forward_to_device - " + str(forward_to_device))
        if forward_to_device:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_DRY_WET
            cc_number = constants.MIDI_CC_FX_DRY_WET
            value = int(dry_wet_level * fl_helper.MIDI_MAX_VALUE)
            device.midiOutMsg(midi_id, channel, cc_number, value)

    def set_fx_extra_parameter_1_level(self, parameter_level, forward_to_device):
        # print("set_fx_dry_wet_level - dry_wet_level - " + str(dry_wet_level) + ", forward_to_device - " + str(forward_to_device))
        if forward_to_device:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_FX_EXTRA_PARAMETER_1
            cc_number = constants.MIDI_CC_FX_EXTRA_PARAMETER_1_RESET
            value = int(parameter_level * fl_helper.MIDI_MAX_VALUE)
            device.midiOutMsg(midi_id, channel, cc_number, value)

    REPEATER_COLOR_OFF              = 24
    REPEATER_COLOR_PLAYBACK         = 24
    REPEATER_COLOR_RECORDING_TARGET = 1
    REPEATER_COLOR_PLAYBACK_TARGET  = 48

    def set_repeater_buttons_state(self, repeater_mode, repeater_length):
        if repeater_mode == repeater_constants.RepeaterMode.MODE_OFF:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_4
            cc_number = constants.MIDI_CC_REPEATER_4
            value = View.REPEATER_COLOR_OFF
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_2
            cc_number = constants.MIDI_CC_REPEATER_2
            value = View.REPEATER_COLOR_OFF
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1
            cc_number = constants.MIDI_CC_REPEATER_1
            value = View.REPEATER_COLOR_OFF
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_2
            cc_number = constants.MIDI_CC_REPEATER_1_2
            value = View.REPEATER_COLOR_OFF
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_4
            cc_number = constants.MIDI_CC_REPEATER_1_4
            value = View.REPEATER_COLOR_OFF
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_8
            cc_number = constants.MIDI_CC_REPEATER_1_8
            value = View.REPEATER_COLOR_OFF
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_16
            cc_number = constants.MIDI_CC_REPEATER_1_16
            value = View.REPEATER_COLOR_OFF
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_32
            cc_number = constants.MIDI_CC_REPEATER_1_32
            value = View.REPEATER_COLOR_OFF
            device.midiOutMsg(midi_id, channel, cc_number, value)
        elif repeater_mode == repeater_constants.RepeaterMode.MODE_RECORDING:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_4
            cc_number = constants.MIDI_CC_REPEATER_4
            value = View.REPEATER_COLOR_OFF \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_4 \
            else View.REPEATER_COLOR_RECORDING_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_2
            cc_number = constants.MIDI_CC_REPEATER_2
            value = View.REPEATER_COLOR_OFF \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_2 \
            else View.REPEATER_COLOR_RECORDING_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1
            cc_number = constants.MIDI_CC_REPEATER_1
            value = View.REPEATER_COLOR_OFF \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_1 \
            else View.REPEATER_COLOR_RECORDING_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_2
            cc_number = constants.MIDI_CC_REPEATER_1_2
            value = View.REPEATER_COLOR_OFF \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_1_2 \
            else View.REPEATER_COLOR_RECORDING_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_4
            cc_number = constants.MIDI_CC_REPEATER_1_4
            value = View.REPEATER_COLOR_OFF \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_1_4 \
            else View.REPEATER_COLOR_RECORDING_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_8
            cc_number = constants.MIDI_CC_REPEATER_1_8
            value = View.REPEATER_COLOR_OFF \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_1_8 \
            else View.REPEATER_COLOR_RECORDING_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_16
            cc_number = constants.MIDI_CC_REPEATER_1_16
            value = View.REPEATER_COLOR_OFF \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_1_16 \
            else View.REPEATER_COLOR_RECORDING_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_32
            cc_number = constants.MIDI_CC_REPEATER_1_32
            value = View.REPEATER_COLOR_OFF \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_1_32 \
            else View.REPEATER_COLOR_RECORDING_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)
        elif repeater_mode == repeater_constants.RepeaterMode.MODE_PLAYBACK:
            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_4
            cc_number = constants.MIDI_CC_REPEATER_4
            value = View.REPEATER_COLOR_PLAYBACK \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_4 \
            else View.REPEATER_COLOR_PLAYBACK_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_2
            cc_number = constants.MIDI_CC_REPEATER_2
            value = View.REPEATER_COLOR_PLAYBACK \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_2 \
            else View.REPEATER_COLOR_PLAYBACK_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1
            cc_number = constants.MIDI_CC_REPEATER_1
            value = View.REPEATER_COLOR_PLAYBACK \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_1 \
            else View.REPEATER_COLOR_PLAYBACK_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_2
            cc_number = constants.MIDI_CC_REPEATER_1_2
            value = View.REPEATER_COLOR_PLAYBACK \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_1_2 \
            else View.REPEATER_COLOR_PLAYBACK_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_4
            cc_number = constants.MIDI_CC_REPEATER_1_4
            value = View.REPEATER_COLOR_PLAYBACK \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_1_4 \
            else View.REPEATER_COLOR_PLAYBACK_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_8
            cc_number = constants.MIDI_CC_REPEATER_1_8
            value = View.REPEATER_COLOR_PLAYBACK \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_1_8 \
            else View.REPEATER_COLOR_PLAYBACK_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_16
            cc_number = constants.MIDI_CC_REPEATER_1_16
            value = View.REPEATER_COLOR_PLAYBACK \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_1_16 \
            else View.REPEATER_COLOR_PLAYBACK_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)

            midi_id = midi.MIDI_CONTROLCHANGE
            channel = constants.MIDI_CH_REPEATER_1_32
            cc_number = constants.MIDI_CC_REPEATER_1_32
            value = View.REPEATER_COLOR_PLAYBACK \
            if not repeater_length == repeater_constants.RepeaterLength.LENGTH_1_32 \
            else View.REPEATER_COLOR_PLAYBACK_TARGET
            device.midiOutMsg(midi_id, channel, cc_number, value)
        