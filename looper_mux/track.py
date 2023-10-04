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
        self.__isPlaybackActive       = False
        self.__isRecordingInProgress  = False
        self.__context_provider       = context_provider

    def onInitScript(self):
        self.resetTrackParams()
        self.__view.updateSampleLength(self.__sample_length)
        self.setTrackVolume(fl_helper.MAX_VOLUME_LEVEL_VALUE)

    def getResampleMode(self):
        return self.__resample_mode

    def setLooperVolume(self, looper_volume):
        mixer.setTrackVolume(self.__mixer_track, looper_volume)

    def setTrackVolume(self, track_volume):
        self.__volume = track_volume
        plugins.setParamValue(track_volume, constants.PANOMATIC_VOLUME_PARAM_INDEX, self.__mixer_track, constants.TRACK_PANOMATIC_VOLUME_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.updateVolume()

    def getTrackVolume(self):
        return self.__volume

    def __setTrackVolumeActivation(self, track_volume_activation):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "T" + str(self.__track_number + 1) + "VA", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(track_volume_activation, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def clear(self, stop_recording = False):
        plugins.setParamValue(1, constants.AUGUSTUS_LOOP_PLUGIN_CLEAR_LOOP_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.setTrackVolume(fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.__view.setTrackClearState(self.__track_number, 1.0)

        self.__isPlaybackActive = False
        self.__view.setTrackPlaybackState(self.__track_number, self.__isPlaybackActive)

        if stop_recording == True:
            self.__isRecordingInProgress  = False
            self.__view.setTrackRecordingState(self.__track_number, self.__isRecordingInProgress)
            self.__setTrackVolumeActivation(1.0)
            self.setSampleLength(SampleLength.LENGTH_0)
        else:
            if False == self.__isRecordingInProgress:
                self.__setTrackVolumeActivation(1.0)
                self.setSampleLength(SampleLength.LENGTH_0)
            else:
                self.setSampleLength(self.__context_provider.getSampleLength())

    def resetTrackParams(self):
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

        self.__setRouting();

        self.setSampleLength(self.__sample_length, True)

    def setSampleLength(self, sample_length, unconditionally = False):

        if(sample_length != self.__sample_length or True == unconditionally):

            self.__isPlaybackActive = False
            self.__view.setTrackPlaybackState(self.__track_number, self.__isPlaybackActive)

            self.__view.setTrackSampleLength(self.__track_number, sample_length)

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

    def startRecording(self, sample_length, resample_mode):

        self.setSampleLength(sample_length)
        self.__setResampleMode(resample_mode)

        self.__setTrackVolumeActivation(0.0)

        plugins.setParamValue(1.0, constants.AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

        if ResampleMode.FROM_LOOPER_TO_TRACK == self.getResampleMode():

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

        elif ResampleMode.FROM_ALL_LOOPERS_TO_TRACK == self.getResampleMode():

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
        self.__isRecordingInProgress = True

        if self.getResampleMode() == ResampleMode.NONE:
            self.__view.setTrackRecordingState(self.__track_number, 1.0)
        else:
            self.clear()
            self.__view.setTrackResamplingState(self.__track_number, 1.0)

    def stopRecording(self):

        if self.__isRecordingInProgress == True:
            plugins.setParamValue(0.0, constants.AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, constants.TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX, midi.PIM_None, True)

            self.__setTrackVolumeActivation(1.0)

            if ResampleMode.FROM_LOOPER_TO_TRACK == self.getResampleMode():

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

            elif ResampleMode.FROM_ALL_LOOPERS_TO_TRACK == self.getResampleMode():

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

            if self.getResampleMode() == ResampleMode.NONE:
                self.__view.setTrackRecordingState(self.__track_number, 0.0)
            else:
                self.__view.setTrackResamplingState(self.__track_number, 0.0)

            self.__setResampleMode(ResampleMode.NONE)

            self.__isPlaybackActive = True
            self.__view.setTrackPlaybackState(self.__track_number, self.__isPlaybackActive)

            self.__isRecordingInProgress = False


    def isRecordingInProgress(self):
        return self.__isRecordingInProgress

    def updateStats(self):

        self.__view.setTrackPlaybackState(self.__track_number, self.__isPlaybackActive)
        self.__view.setTrackSampleLength(self.__track_number, self.__sample_length)

        self.__view.setTrackRecordingState(self.__track_number, 0.0)
        self.__view.setTrackResamplingState(self.__track_number, 0.0)
        self.__view.setTrackClearState(self.__track_number, 0.0)

        self.updateVolume()

    def updateVolume(self):
        self.__view.setTrackVolume(self.__track_number, self.__volume)

    def __setResampleMode(self, resample_mode):
        self.__resample_mode = resample_mode

    def __setRouting(self):
        mixer.setRouteTo(constants.MIC_ROUTE_CHANNEL, self.__mixer_track, 1)
        mixer.setRouteTo(constants.SYNTH_ROUTE_CHANNEL, self.__mixer_track, 1)

    def __removeRouting(self):
        mixer.setRouteTo(constants.MIC_ROUTE_CHANNEL, self.__mixer_track, 0)
        mixer.setRouteTo(constants.SYNTH_ROUTE_CHANNEL, self.__mixer_track, 0)

    def setRoutingLevel(self, routing_level):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "T" + str(self.__track_number + 1) + "M", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(routing_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "T" + str(self.__track_number + 1) + "S", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(routing_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def setInputSideChainLevel(self, sidechain_level):
        self.__view.setInputSideChainLevel(self.__track_number, sidechain_level)
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "M2L1T" + str(self.__track_number + 1) + "S", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "S2L1T" + str(self.__track_number + 1) + "S", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
