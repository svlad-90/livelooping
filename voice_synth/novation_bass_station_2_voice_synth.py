'''
Created on Oct 5, 2023

@author: Dream Machines
'''

import midi
import mixer
import plugins

from voice_synth import constants
from common import fl_helper
from _ast import Or

class NovationBassStation2VoiceSynth():

    def __init__(self):
        self.__initialized = False

    def on_init_script(self):

        if False == self.__initialized:
            print(NovationBassStation2VoiceSynth.on_init_script.__name__)

            try:
                # fl_helper.print_all_plugin_parameters(constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT)
                self.__initialized = True
            except Exception as e:
                print(NovationBassStation2VoiceSynth.on_init_script.__name__ + ": failed to initialize the script.")
                print(e)

    def reset_params(self):
            plugins.setParamValue(0, constants.CROSSFADE_LOOP_SYNTH_ATTACK_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            plugins.setParamValue(0.4 / 5, constants.CROSSFADE_LOOP_SYNTH_DECAY_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            plugins.setParamValue(0, constants.CROSSFADE_LOOP_SYNTH_SUSTAIN_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            plugins.setParamValue(0, constants.CROSSFADE_LOOP_SYNTH_RELEASE_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            plugins.setParamValue(0, constants.CROSSFADE_LOOP_SYNTH_LOOP_START_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            plugins.setParamValue(1, constants.CROSSFADE_LOOP_SYNTH_LOOP_END_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            plugins.setParamValue(0, constants.CROSSFADE_LOOP_SYNTH_SATURATION_AMOUNT_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            plugins.setParamValue(0, constants.CROSSFADE_LOOP_SYNTH_SATURATION_SHAPE_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            plugins.setParamValue(0, constants.CROSSFADE_LOOP_SYNTH_HARD_SYNC_CYCLE_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            plugins.setParamValue(0, constants.CROSSFADE_LOOP_SYNTH_HARD_SYNC_DETUNE_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            plugins.setParamValue(0, constants.CROSSFADE_LOOP_SYNTH_FEEDBACK_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)

    def on_midi_msg(self, event):

        self.on_init_script()

        event.handled = False

        # print("handled - " + str(event.handled) + "; "
        #       "timestamp - " + str(event.timestamp) + "; "
        #       "data1 - " + str(event.data1) + "; "
        #       "data2 - " + str(event.data2) + "; "
        #       "port - " + str(event.port) + "; "
        #       "note - " + str(event.note) + "; "
        #       "velocity - " + str(event.velocity) + "; "
        #       "pressure - " + str(event.pressure) + "; "
        #       "progNum - " + str(event.progNum) + "; "
        #       "controlNum - " + str(event.controlNum) + "; "
        #       "controlVal - " + str(event.controlVal) + "; "
        #       "pitchBend - " + str(event.pitchBend) + "; "
        #       "sysex - " + str(event.sysex) + "; "
        #       "isIncrement - " + str(event.isIncrement) + "; "
        #       "res - " + str(event.res) + "; "
        #       "inEv - " + str(event.inEv) + "; "
        #       "outEv - " + str(event.outEv) + "; "
        #       "midiId - " + str(event.midiId) + "; "
        #       "midiChan - " + str(event.midiChan) + "; "
        #       "midiChanEx - " + str(event.midiChanEx) + "; ")

        if event.midiId == 208:
            # print("Skip aftertouch!")
            event.handled = True
        elif ( event.data1 == constants.NOVATION_IGNORED_1 or
               event.data1 == constants.NOVATION_IGNORED_2 or
               event.data1 == constants.NOVATION_IGNORED_3 or
               event.data1 == constants.NOVATION_IGNORED_4 ) and event.midiId == 176:
            # print(f"Ignoring signal - {str(event.data1)}")
            event.handled = True
        elif event.data1 == constants.NOVATION_REC_PRESSED and event.midiId == 176:
            if event.data2 == constants.REC_ON:
                self.reset_params()
                plugins.setParamValue(1, constants.CROSSFADE_LOOP_SYNTH_RECORD_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
                parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "CFSR", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
                plugins.setParamValue(fl_helper.MAX_VOLUME_LEVEL_VALUE, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
                parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "CFSR_SR", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
                plugins.setParamValue(0, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
                mixer.muteTrack(constants.SYNTH_INPUT_ROUTE_CHANNEL, 1)
            if event.data2 == constants.REC_OFF:
                plugins.setParamValue(0, constants.CROSSFADE_LOOP_SYNTH_RECORD_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
                parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "CFSR", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
                plugins.setParamValue(0, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
                parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "CFSR_SR", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
                plugins.setParamValue(fl_helper.MAX_VOLUME_LEVEL_VALUE, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
                mixer.muteTrack(constants.SYNTH_INPUT_ROUTE_CHANNEL, 0)
            event.handled = True
        elif event.data1 == constants.NOVATION_ATTACK and event.midiId == 176:
            plugins.setParamValue(event.data2 / fl_helper.MIDI_MAX_VALUE / 5, constants.CROSSFADE_LOOP_SYNTH_ATTACK_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            event.handled = True
        elif event.data1 == constants.NOVATION_DECAY and event.midiId == 176:
            plugins.setParamValue(event.data2 / fl_helper.MIDI_MAX_VALUE / 5, constants.CROSSFADE_LOOP_SYNTH_DECAY_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            event.handled = True
        elif event.data1 == constants.NOVATION_SUSTAIN and event.midiId == 176:
            plugins.setParamValue(event.data2 / fl_helper.MIDI_MAX_VALUE, constants.CROSSFADE_LOOP_SYNTH_SUSTAIN_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            event.handled = True
        elif event.data1 == constants.NOVATION_RELEASE and event.midiId == 176:
            plugins.setParamValue(event.data2 / fl_helper.MIDI_MAX_VALUE, constants.CROSSFADE_LOOP_SYNTH_RELEASE_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            event.handled = True
        elif event.data1 == constants.NOVATION_MIXER_OSC_1 and event.midiId == 176:
            plugins.setParamValue(event.data2 / fl_helper.MIDI_MAX_VALUE, constants.CROSSFADE_LOOP_SYNTH_LOOP_START_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            event.handled = True
        elif event.data1 == constants.NOVATION_MIXER_OSC_2 and event.midiId == 176:
            plugins.setParamValue(event.data2 / fl_helper.MIDI_MAX_VALUE, constants.CROSSFADE_LOOP_SYNTH_LOOP_END_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            event.handled = True
        elif event.data1 == constants.NOVATION_DISTORTION and event.midiId == 176:
            plugins.setParamValue(event.data2 / fl_helper.MIDI_MAX_VALUE, constants.CROSSFADE_LOOP_SYNTH_SATURATION_AMOUNT_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            event.handled = True
        elif event.data1 == constants.NOVATION_OSC_FILTER_MODE and event.midiId == 176:
            plugins.setParamValue(event.data2 / fl_helper.MIDI_MAX_VALUE, constants.CROSSFADE_LOOP_SYNTH_SATURATION_SHAPE_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            event.handled = True
        elif event.data1 == constants.NOVATION_FILTERS_MOD_ENV_DEPTH and event.midiId == 176:
            plugins.setParamValue(event.data2 / fl_helper.MIDI_MAX_VALUE, constants.CROSSFADE_LOOP_SYNTH_HARD_SYNC_CYCLE_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            event.handled = True
        elif event.data1 == constants.NOVATION_FILTERS_LFO_2_DEPTH and event.midiId == 176:
            plugins.setParamValue(event.data2 / fl_helper.MIDI_MAX_VALUE, constants.CROSSFADE_LOOP_SYNTH_HARD_SYNC_DETUNE_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            event.handled = True
        elif event.data1 == constants.NOVATION_MIXER_EXT_RING_NOISE and event.midiId == 176:
            plugins.setParamValue(event.data2 / fl_helper.MIDI_MAX_VALUE, constants.CROSSFADE_LOOP_SYNTH_FEEDBACK_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            event.handled = True
        elif event.data1 == constants.NOVATION_MIXER_SUB_OSC and event.midiId == 176:
            plugins.setParamValue(event.data2 / fl_helper.MIDI_MAX_VALUE, constants.CROSSFADE_LOOP_SYNTH_VOLUME_PARAM_INDEX, constants.SYNTH_INPUT_ROUTE_CHANNEL, constants.CROSSFADE_LOOP_SYNTH_SLOT, midi.PIM_None, True)
            event.handled = True
        else:
            #print(f"Unhandled event - {str(event.data1)}!")
            pass
