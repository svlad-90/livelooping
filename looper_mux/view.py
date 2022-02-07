'''
Created on Feb 7, 2022

@author: Dream Machines
'''
import math

import plugins

from looper_mux.resample_mode import ResampleMode
from looper_mux import constants
from looper_mux.track import Track
from common import fl_helper

class View:
    def setShiftPressedState(self, shift_pressed):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "Shift", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(shift_pressed, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
        
    def setLooperVolume(self, looper_volume):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "Volume", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(looper_volume, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
    
    def setLooperActivationStatus(self, looper_id, looper_volume):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "Looper_" + str(looper_id + 1) + "_AS", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0 if looper_volume == 0.0 else 1.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
    
    def setDropIntencity(self, drop_intencity):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "Drop FX", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(drop_intencity, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
        
    def selectLooper(self, selected_looper):
        
        for i in range(4):
            value = 0.0
            if i == selected_looper:
                value = 1.0
            
            parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "Looper " + str(i + 1), constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(value, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()
        
    def clear(self):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "Clear all", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
    def __clearOff(self):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "Clear all", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
    def __clearTracksOff(self):
        for i in range(constants.Track_4 + 1):
            parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T" + str(i + 1) + "_Clear", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(0.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
    
    def setTrackVolume(self, track_index, track_volume):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T" + str(track_index + 1) + "_Volume", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(track_volume, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
    
    def setPlay(self, value):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "Play", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(value, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
    
    def setInputSideChainLevel(self, track_id, sidechain_level):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_Sidechain", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
    
    def setLooperSideChainLevel(self, track_id, sidechain_level):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_L_S_CH", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
    
    def setResampleMode(self, resample_mode):
        
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
        
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "Resample selected looper", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(resample_looper, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "Resample all loopers", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(resample_all_loopers, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()
        
    def setTrackRecordingState(self, track_id, recording_state):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_Recording", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(recording_state, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()
        
    def setTrackResamplingState(self, track_id, recording_state):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_Resampling", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(recording_state, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()
    
    def setTrackClearState(self, track_id, recording_state):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_Clear", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(recording_state, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
    
    def setTrackPlaybackState(self, track_id, recording_state):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "_Playback", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(recording_state, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()
    
    def resetToggleFlags(self):
        self.__clearOff()
        self.__clearTracksOff()
        
    def updateSampleLength(self, sample_length):
        
        for i in range(8):
            i_sample_length = int(math.pow(2, i))
            parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "Length_" + str(i_sample_length), constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            
            value = 0
            
            if(sample_length == i_sample_length):
                value = 1
                
            plugins.setParamValue(value, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
     
    def setTempo(self, tempo):
        tempo_hundred = int(tempo) // 100
        tempo_dozens = (tempo % 100) // 10
        tempo_units = (tempo % 10)
        
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "TH", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(tempo_hundred / 10, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "TD", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(tempo_dozens / 10, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "TU", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(tempo_units / 10, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
    def setTrackSampleLength(self, track_id, sample_length):
        sample_length_hundred = int(sample_length) // 100
        sample_length_dozens = (sample_length % 100) // 10
        sample_length_units = (sample_length % 10)
        
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "H", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sample_length_hundred / 10, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "D", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sample_length_dozens / 10, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "U", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sample_length_units / 10, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
    
    def setTurnadoDictatorLevel(self, turnado_dictator_level):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T_D", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(turnado_dictator_level, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setTurnadoDryWetLevel(self, turnado_dry_wet_level):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T_DW", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(turnado_dry_wet_level, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
    
    def switchToNextTurnadoPreset(self):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T_Next_Preset", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def switchToPrevTurnadoPreset(self):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "T_Previous_Preset", constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, parameter_id, constants.MASTER_CHANNEL, constants.LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)