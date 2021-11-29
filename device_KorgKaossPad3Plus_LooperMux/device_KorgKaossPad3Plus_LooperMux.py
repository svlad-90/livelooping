# name=device_KorgKaossPad3Plus_LooperMux
device_name="device_KorgKaossPad3Plus_LooperMux"
print(device_name + ': started')

# python imports
import math
import time

# FL imports
import transport
import mixer
import plugins

# internal imports 
from common import fl_helper

# MIDI CC
MIDI_CC_SHIFT               = 95
MIDI_CC_PLAY_STOP           = 56
MIDI_CC_TEMPO               = 94
MIDI_CC_LOOPER_1            = 49
MIDI_CC_LOOPER_2            = 50
MIDI_CC_LOOPER_3            = 51
MIDI_CC_LOOPER_4            = 52
MIDI_CC_LOOPER_VOLUME       = 93
MIDI_CC_TRACK_VOLUME_1      = 70
MIDI_CC_TRACK_VOLUME_2      = 71
MIDI_CC_TRACK_VOLUME_3      = 72
MIDI_CC_TRACK_VOLUME_4      = 73
MIDI_CC_TRACK_SIDECHAIN_1   = 74
MIDI_CC_TRACK_SIDECHAIN_2   = 75
MIDI_CC_TRACK_SIDECHAIN_3   = 76
MIDI_CC_TRACK_SIDECHAIN_4   = 77
MIDI_CC_CLEAR_LOOPER        = 55
MIDI_CC_SAMPLE_LENGTH_1     = 49
MIDI_CC_SAMPLE_LENGTH_2     = 50
MIDI_CC_SAMPLE_LENGTH_4     = 51
MIDI_CC_SAMPLE_LENGTH_8     = 52
MIDI_CC_SAMPLE_LENGTH_16    = 53
MIDI_CC_SAMPLE_LENGTH_32    = 54
MIDI_CC_SAMPLE_LENGTH_64    = 55
MIDI_CC_SAMPLE_LENGTH_128   = 56

MIDI_CC_RESAMPLE_MODE_FROM_LOOPER_TO_TRACK      = 53
MIDI_CC_RESAMPLE_MODE_FROM_ALL_LOOPERS_TO_TRACK = 54

MIDI_CC_TRACK_1_CLEAR       = 36
MIDI_CC_TRACK_2_CLEAR       = 37
MIDI_CC_TRACK_3_CLEAR       = 38
MIDI_CC_TRACK_4_CLEAR       = 39

MIDI_CC_TRACK_1_SAMPLING    = 36
MIDI_CC_TRACK_2_SAMPLING    = 37
MIDI_CC_TRACK_3_SAMPLING    = 38
MIDI_CC_TRACK_4_SAMPLING    = 39

MIDI_CC_TURNADO_DICTATOR    = 94
MIDI_CC_TURNADO_RANDOMIZE   = 95

# ROUTING
MASTER_CHANNEL               = 0
MASTER_FX_1_CHANNEL          = 2
MIC_ROUTE_CHANNEL            = 4
SYNTH_ROUTE_CHANNEL          = 8
LOOPER_ALL_FX_1_CHANNEL      = 13
LOOPER_ALL_CHANNEL           = 14

LOOPER_1_FX_1_CHANNEL        = 18
LOOPER_2_FX_1_CHANNEL        = 26
LOOPER_3_FX_1_CHANNEL        = 34
LOOPER_4_FX_1_CHANNEL        = 42

LOOPER_1_CHANNEL             = 16
LOOPER_2_CHANNEL             = 24
LOOPER_3_CHANNEL             = 32
LOOPER_4_CHANNEL             = 40

LOOPER_1_INITIAL_TRACK_CHANNEL = 19
LOOPER_2_INITIAL_TRACK_CHANNEL = 27
LOOPER_3_INITIAL_TRACK_CHANNEL = 35
LOOPER_4_INITIAL_TRACK_CHANNEL = 43

# CONSTANTS
TEMPO_JOG_ROTATION_THRESHOLD = 5

KP3_PLUS_ABCD_PRESSED        = 100
KP3_PLUS_ABCD_RELEASED       = 64

# MASTER MIXER SLOT INDICES
MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX = 0
LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX = 1

# MIXER SLOT INDICES
TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX    = 0
TRACK_PANOMATIC_VOLUME_PLUGIN_MIXER_SLOT_INDEX = 8
LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX  = 7
LOOPER_ALL_ENDLESS_SMILE_SLOT_INDEX            = 8

LOOPER_TURNADO_SLOT_INDEX                      = 0

# PLUGIN PARAMETERS

PEAK_CONTROLLER_BASE_PARAM_INDEX = 0
PEAK_CONTROLLER_VOLUME_PARAM_INDEX = 1
PEAK_CONTROLLER_TENSION_PARAM_INDEX = 2
PEAK_CONTROLLER_DECAY_PARAM_INDEX = 3

AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX = 0
AUGUSTUS_LOOP_PLUGIN_DELAY_TIME_PARAM_INDEX = 1
AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MIN_PARAM_INDEX = 2
AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX = 3
AUGUSTUS_LOOP_PLUGIN_LL_FEEDBACK_PARAM_INDEX = 5
AUGUSTUS_LOOP_PLUGIN_RR_FEEDBACK_PARAM_INDEX = 11
AUGUSTUS_LOOP_PLUGIN_MASTER_FEEDBACK_PARAM_INDEX = 12
AUGUSTUS_LOOP_PLUGIN_PITCH_INDEPENDENT_DELAY_PARAM_INDEX = 16
AUGUSTUS_LOOP_PLUGIN_EFFECT_LEVEL_PARAM_INDEX = 22
AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX = 31
AUGUSTUS_LOOP_PLUGIN_HOST_TEMPO_PARAM_INDEX = 33
AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX = 34
AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX = 35
AUGUSTUS_LOOP_PLUGIN_CLEAR_LOOP_PARAM_INDEX = 49
AUGUSTUS_LOOP_PLUGIN_SATURATION_ON_OFF_PARAM_INDEX = 55
AUGUSTUS_LOOP_PLUGIN_DELAY_INTERIA_MODE_PARAM_INDEX = 57
AUGUSTUS_LOOP_PLUGIN_DIGITAL_MODE_PARAM_INDEX = 59
AUGUSTUS_LOOP_PLUGIN_SYNC_GROUP_MODE_PARAM_INDEX = 71

ENDLESS_SMILE_PLUGIN_INTENSITY_PARAM_INDEX = 0

PANOMATIC_VOLUME_PARAM_INDEX = 1

TURNADO_DICTATOR_PARAM_INDEX  = 8
TURNADO_RANDOMIZE_PARAM_INDEX = 10

class SampleLength:
    LENGTH_0 = 0
    LENGTH_1 = 1
    LENGTH_2 = 2
    LENGTH_4 = 4
    LENGTH_8 = 8
    LENGTH_16 = 16
    LENGTH_32 = 32
    LENGTH_64 = 64
    LENGTH_128 = 128
    
class ResampleMode:
    NONE = -1
    FROM_LOOPER_TO_TRACK = 0
    FROM_ALL_LOOPERS_TO_TRACK = 1

class Track():

    Track_1    = 0
    Track_2    = 1
    Track_3    = 2
    Track_4    = 3

    def __init__(self, looper_number, track_number, mixer_track, view):
        self.__view                  = view
        self.__looper_number         = looper_number
        self.__track_number          = track_number
        self.__mixer_track           = mixer_track
        self.__sample_length         = SampleLength.LENGTH_0
        self.__resample_mode         = ResampleMode.NONE
        self.__volume                = fl_helper.MAX_VOLUME_LEVEL_VALUE
        self.__isPlaybackActive      = False
        self.__isRecordingInProgress = False

    def onInitScript(self):
        self.resetTrackParams()
        self.__view.updateSampleLength(self.__sample_length)
        self.setTrackVolume(fl_helper.MAX_VOLUME_LEVEL_VALUE)

    def getResampleMode(self):
        return self.__resample_mode
    
    def __setResampleMode(self, resample_mode):
        self.__resample_mode = resample_mode

    def setLooperVolume(self, looper_volume):
        mixer.setTrackVolume(self.__mixer_track, looper_volume)

    def setTrackVolume(self, track_volume):
        self.__volume = track_volume
        plugins.setParamValue(track_volume, PANOMATIC_VOLUME_PARAM_INDEX, self.__mixer_track, TRACK_PANOMATIC_VOLUME_PLUGIN_MIXER_SLOT_INDEX)
        self.updateVolume()
    
    def getTrackVolume(self):
        return self.__volume
    
    def __setTrackVolumeActivation(self, track_volume_activation):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "T" + str(self.__track_number + 1) + "VA", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(track_volume_activation, parameter_id, MASTER_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def clear(self):
        plugins.setParamValue(1, AUGUSTUS_LOOP_PLUGIN_CLEAR_LOOP_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        self.setTrackVolume(fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.__view.setTrackClearState(self.__track_number, 1.0)
        
        self.__isPlaybackActive = False
        self.__view.setTrackPlaybackState(self.__track_number, self.__isPlaybackActive)
        
        if False == self.__isRecordingInProgress:
            self.__setTrackVolumeActivation(1.0)
            self.setSampleLength(SampleLength.LENGTH_0)

    def resetTrackParams(self):
        plugins.setParamValue(0.0, AUGUSTUS_LOOP_PLUGIN_DELAY_TIME_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(0, AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MIN_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, AUGUSTUS_LOOP_PLUGIN_HOST_TEMPO_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, AUGUSTUS_LOOP_PLUGIN_EFFECT_LEVEL_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, AUGUSTUS_LOOP_PLUGIN_MASTER_FEEDBACK_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, AUGUSTUS_LOOP_PLUGIN_DIGITAL_MODE_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, AUGUSTUS_LOOP_PLUGIN_PITCH_INDEPENDENT_DELAY_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0 / 3600.0, AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.33, AUGUSTUS_LOOP_PLUGIN_SYNC_GROUP_MODE_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.1, AUGUSTUS_LOOP_PLUGIN_LL_FEEDBACK_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.1, AUGUSTUS_LOOP_PLUGIN_RR_FEEDBACK_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, AUGUSTUS_LOOP_PLUGIN_SATURATION_ON_OFF_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)

        # looper 1 is the source of the sidechain
        if self.__looper_number == Looper.Looper_1:
            plugins.setParamValue(fl_helper.MAX_VOLUME_LEVEL_VALUE, PEAK_CONTROLLER_BASE_PARAM_INDEX, self.__mixer_track, LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX)
            plugins.setParamValue(0.12, PEAK_CONTROLLER_VOLUME_PARAM_INDEX, self.__mixer_track, LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX)
            plugins.setParamValue(0.85, PEAK_CONTROLLER_TENSION_PARAM_INDEX, self.__mixer_track, LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX)
            plugins.setParamValue(0.5, PEAK_CONTROLLER_DECAY_PARAM_INDEX, self.__mixer_track, LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX)

        self.__setRouting();

        self.setSampleLength(self.__sample_length, True)

    def setSampleLength(self, sample_length, unconditionally = False):

        if(sample_length != self.__sample_length or True == unconditionally):
            
            self.__isPlaybackActive = False
            self.__view.setTrackPlaybackState(self.__track_number, self.__isPlaybackActive)
            
            self.__view.setTrackSampleLength(self.__track_number, sample_length)
            
            if(sample_length == SampleLength.LENGTH_1):
                plugins.setParamValue((1.0 - 1.0) / 3599.0 , AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(1.0 / 3600.0, AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(0.33, AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(1.0/128.0, AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
            elif(sample_length == SampleLength.LENGTH_2):
                plugins.setParamValue((2.0 - 1.0) / 3599.0 , AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(2.0 / 3600.0, AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(0.33, AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(2.0/128.0, AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
            elif(sample_length == SampleLength.LENGTH_4):
                plugins.setParamValue((4.0 - 1.0) / 3599.0 , AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(4.0 / 3600.0, AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(0.33, AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(4.0/128.0, AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
            elif(sample_length == SampleLength.LENGTH_8):
                plugins.setParamValue((8.0 - 1.0) / 3599.0 , AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(8.0 / 3600.0, AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(0.33, AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(8.0/128.0, AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
            elif(sample_length == SampleLength.LENGTH_16):
                plugins.setParamValue((16.0 - 1.0) / 3599.0 , AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(16.0 / 3600.0, AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(0.33, AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(16.0/128.0, AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
            elif(sample_length == SampleLength.LENGTH_32):
                plugins.setParamValue((32.0 - 1.0) / 3599.0 , AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(32.0 / 3600.0, AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(0.33, AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(32.0/128.0, AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
            elif(sample_length == SampleLength.LENGTH_64):
                plugins.setParamValue((64.0 - 1.0) / 3599.0 , AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(64.0 / 3600.0, AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(0.33, AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(64.0/128.0, AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
            elif(sample_length == SampleLength.LENGTH_128):
                plugins.setParamValue((64.0 - 1.0) / 3599.0 , AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(64.0 / 3600.0, AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(0.33, AUGUSTUS_LOOP_PLUGIN_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
                plugins.setParamValue(128.0/128.0, AUGUSTUS_LOOP_PLUGIN_BEATS_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)

        self.__sample_length = sample_length

    def startRecording(self, sample_length, resample_mode):
        
        self.setSampleLength(sample_length)
        self.__setResampleMode(resample_mode)
        
        self.__setTrackVolumeActivation(0.0)

        plugins.setParamValue(1.0, AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)

        if ResampleMode.FROM_LOOPER_TO_TRACK == self.getResampleMode():
            
            if self.__looper_number == Looper.Looper_1:
                mixer.setRouteTo(LOOPER_1_CHANNEL, LOOPER_ALL_CHANNEL, 0)
                mixer.setRouteTo(self.__mixer_track, LOOPER_1_FX_1_CHANNEL, 0)
                mixer.setRouteTo(LOOPER_1_CHANNEL, self.__mixer_track, 1)
            elif self.__looper_number == Looper.Looper_2:
                mixer.setRouteTo(LOOPER_2_CHANNEL, LOOPER_ALL_CHANNEL, 0)
                mixer.setRouteTo(self.__mixer_track, LOOPER_2_FX_1_CHANNEL, 0)
                mixer.setRouteTo(LOOPER_2_CHANNEL, self.__mixer_track, 1)
            elif self.__looper_number == Looper.Looper_3:
                mixer.setRouteTo(LOOPER_3_CHANNEL, LOOPER_ALL_CHANNEL, 0)
                mixer.setRouteTo(self.__mixer_track, LOOPER_3_FX_1_CHANNEL, 0)
                mixer.setRouteTo(LOOPER_3_CHANNEL, self.__mixer_track, 1)
            elif self.__looper_number == Looper.Looper_4:
                mixer.setRouteTo(LOOPER_4_CHANNEL, LOOPER_ALL_CHANNEL, 0)
                mixer.setRouteTo(self.__mixer_track, LOOPER_4_FX_1_CHANNEL, 0)
                mixer.setRouteTo(LOOPER_4_CHANNEL, self.__mixer_track, 1)
                
            mixer.setRouteTo(self.__mixer_track, LOOPER_ALL_FX_1_CHANNEL, 1)
            
        elif ResampleMode.FROM_ALL_LOOPERS_TO_TRACK == self.getResampleMode():
            
            if self.__looper_number == Looper.Looper_1:
                mixer.setRouteTo(self.__mixer_track, LOOPER_1_FX_1_CHANNEL, 0)
            elif self.__looper_number == Looper.Looper_2:
                mixer.setRouteTo(self.__mixer_track, LOOPER_2_FX_1_CHANNEL, 0)
            elif self.__looper_number == Looper.Looper_3:
                mixer.setRouteTo(self.__mixer_track, LOOPER_3_FX_1_CHANNEL, 0)
            elif self.__looper_number == Looper.Looper_4:
                mixer.setRouteTo(self.__mixer_track, LOOPER_4_FX_1_CHANNEL, 0)
            
            mixer.setRouteTo(LOOPER_ALL_CHANNEL, LOOPER_ALL_FX_1_CHANNEL, 0)
            mixer.setRouteTo(LOOPER_ALL_CHANNEL, self.__mixer_track, 1)
            mixer.setRouteTo(self.__mixer_track, LOOPER_ALL_FX_1_CHANNEL, 1)

        if self.getResampleMode() == ResampleMode.NONE:
            self.__view.setTrackRecordingState(self.__track_number, 1.0)
        else:
            self.__view.setTrackResamplingState(self.__track_number, 1.0)
                 
        self.__isRecordingInProgress = True

    def stopRecording(self):
        
        if self.__isRecordingInProgress == True:
            plugins.setParamValue(0.0, AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
    
            self.__setTrackVolumeActivation(1.0)
    
            if ResampleMode.FROM_LOOPER_TO_TRACK == self.getResampleMode():
                
                mixer.setRouteTo(self.__mixer_track, LOOPER_ALL_FX_1_CHANNEL, 0)
                
                if self.__looper_number == Looper.Looper_1:
                    mixer.setRouteTo(LOOPER_1_CHANNEL, self.__mixer_track, 0)
                    mixer.setRouteTo(self.__mixer_track, LOOPER_1_FX_1_CHANNEL, 1)
                    mixer.setRouteTo(LOOPER_1_CHANNEL, LOOPER_ALL_CHANNEL, 1)
                elif self.__looper_number == Looper.Looper_2:
                    mixer.setRouteTo(LOOPER_2_CHANNEL, self.__mixer_track, 0)
                    mixer.setRouteTo(self.__mixer_track, LOOPER_2_FX_1_CHANNEL, 1)
                    mixer.setRouteTo(LOOPER_2_CHANNEL, LOOPER_ALL_CHANNEL, 1)
                elif self.__looper_number == Looper.Looper_3:
                    mixer.setRouteTo(LOOPER_3_CHANNEL, self.__mixer_track, 0)
                    mixer.setRouteTo(self.__mixer_track, LOOPER_3_FX_1_CHANNEL, 1)
                    mixer.setRouteTo(LOOPER_3_CHANNEL, LOOPER_ALL_CHANNEL, 1)
                elif self.__looper_number == Looper.Looper_4:
                    mixer.setRouteTo(LOOPER_4_CHANNEL, self.__mixer_track, 0)
                    mixer.setRouteTo(self.__mixer_track, LOOPER_4_FX_1_CHANNEL, 1)
                    mixer.setRouteTo(LOOPER_4_CHANNEL, LOOPER_ALL_CHANNEL, 1)
                
            elif ResampleMode.FROM_ALL_LOOPERS_TO_TRACK == self.getResampleMode():
                
                mixer.setRouteTo(self.__mixer_track, LOOPER_ALL_FX_1_CHANNEL, 0)
                mixer.setRouteTo(LOOPER_ALL_CHANNEL, self.__mixer_track, 0)
                
                if self.__looper_number == Looper.Looper_1:
                    mixer.setRouteTo(self.__mixer_track, LOOPER_1_FX_1_CHANNEL, 1)
                elif self.__looper_number == Looper.Looper_2:
                    mixer.setRouteTo(self.__mixer_track, LOOPER_2_FX_1_CHANNEL, 1)
                elif self.__looper_number == Looper.Looper_3:
                    mixer.setRouteTo(self.__mixer_track, LOOPER_3_FX_1_CHANNEL, 1)
                elif self.__looper_number == Looper.Looper_4:
                    mixer.setRouteTo(self.__mixer_track, LOOPER_4_FX_1_CHANNEL, 1)
                
                mixer.setRouteTo(LOOPER_ALL_CHANNEL, LOOPER_ALL_FX_1_CHANNEL, 1)
            
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

    def __setRouting(self):
        mixer.setRouteTo(MIC_ROUTE_CHANNEL, self.__mixer_track, 1)
        mixer.setRouteTo(SYNTH_ROUTE_CHANNEL, self.__mixer_track, 1)

    def __removeRouting(self):
        mixer.setRouteTo(MIC_ROUTE_CHANNEL, self.__mixer_track, 0)
        mixer.setRouteTo(SYNTH_ROUTE_CHANNEL, self.__mixer_track, 0)

    def setRoutingLevel(self, routing_level):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "T" + str(self.__track_number + 1) + "M", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(routing_level, parameter_id, MASTER_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "T" + str(self.__track_number + 1) + "S", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(routing_level, parameter_id, MASTER_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setInputSideChainLevel(self, sidechain_level):
        self.__view.setInputSideChainLevel(self.__track_number, sidechain_level)
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "M2L1T" + str(self.__track_number + 1) + "S", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, MASTER_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "S2L1T" + str(self.__track_number + 1) + "S", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, MASTER_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def updateVolume(self):
        self.__view.setTrackVolume(self.__track_number, self.__volume)

class Looper():
    Looper_1    = 0
    Looper_2    = 1
    Looper_3    = 2
    Looper_4    = 3

    def __init__(self, looper_number, initial_mixer_track, view):
        self.__view = view
        self.__looper_number = looper_number
        self.__INITIAL_TRACK_CHANNEL__ = initial_mixer_track
        self.__tracks = { Track.Track_1: Track(looper_number, Track.Track_1,
                                               initial_mixer_track + Track.Track_1,
                                                   self.__view),
                          Track.Track_2: Track(looper_number, Track.Track_2,
                                               initial_mixer_track + Track.Track_2,
                                                   self.__view),
                          Track.Track_3: Track(looper_number, Track.Track_3,
                                               initial_mixer_track + Track.Track_3,
                                                   self.__view),
                          Track.Track_4: Track(looper_number, Track.Track_4,
                                               initial_mixer_track + Track.Track_4,
                                                   self.__view) }
        self.__looper_volume = fl_helper.MAX_VOLUME_LEVEL_VALUE
        self.__isTurnadoTurnedOn = False
        
        self.__looper_channel = 0
        self.__turnado_dictator_level = 0
        
        if self.__looper_number == Looper.Looper_1:
            self.__looper_channel = LOOPER_1_CHANNEL
        elif self.__looper_number == Looper.Looper_2:
            self.__looper_channel = LOOPER_2_CHANNEL
        elif self.__looper_number == Looper.Looper_3:
            self.__looper_channel = LOOPER_3_CHANNEL
        elif self.__looper_number == Looper.Looper_4:
            self.__looper_channel = LOOPER_4_CHANNEL
        
        self.__sidechainLevels       = { Track.Track_1 : 0.0, 
                                         Track.Track_2 : 0.0,
                                         Track.Track_3 : 0.0,
                                         Track.Track_4 : 0.0 }

    def onInitScript(self):
        for track_id in self.__tracks:
            self.__tracks[track_id].onInitScript()
        
        if self.__looper_number != Looper.Looper_1:
            for track_id in self.__tracks:
                self.setLooperSideChainLevel(track_id, 0.0)

    def getResampleMode(self, track_id):
        return self.__tracks[track_id].getResampleMode()

    def getLooperNumber(self):
        return self.__looper_number

    def getTracks(self):
        return self.__tracks

    def getTrack(self, track_number):
        return self.__tracks.get(track_number)

    def setLooperVolume(self, looper_volume):
        self.__looper_volume = looper_volume
        self.__view.setLooperVolume(looper_volume)
        for track_id in self.__tracks:
            self.__tracks[track_id].setLooperVolume(self.__looper_volume)

    def setTrackVolume(self, track_id, track_volume):
        self.__tracks.get(track_id).setTrackVolume(track_volume)

    def getTrackVolume(self, track_id):
        return self.__tracks.get(track_id).getTrackVolume()

    def clearLooper(self):
        self.setLooperVolume(fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.setTurnadoDictatorLevel(0.0)
        for track_id in self.__tracks:
            self.__tracks[track_id].clear()
            self.__tracks[track_id].resetTrackParams()
            self.__tracks[track_id].setInputSideChainLevel(0.0)
        
        if self.__looper_number != Looper.Looper_1:
            for track_id in self.__tracks:
                self.setLooperSideChainLevel(track_id, 0.0)

    def clearTrack(self, track_id):
            self.__tracks[track_id].clear()

    def startRecordingTrack(self, track_id, sample_length, resample_mode):
        self.__tracks[track_id].startRecording(sample_length, resample_mode)

    def stopRecordingTrack(self, track_id):
        
        if self.__tracks[track_id].getResampleMode() == ResampleMode.FROM_LOOPER_TO_TRACK:
            # turn off the volume of all the tracks of the looper, except the one for which recording is over
            for track_id_it in self.__tracks:
                if track_id_it != track_id:
                    self.__tracks[track_id_it].setTrackVolume(0.0)
                else:
                    self.__tracks[track_id_it].setTrackVolume(fl_helper.MAX_VOLUME_LEVEL_VALUE)
            self.setTurnadoDictatorLevel(0.0)
                    
        self.__tracks[track_id].stopRecording()

    def setInputSideChainLevel(self, track_id, sidechain_level):
        self.__tracks[track_id].setInputSideChainLevel(sidechain_level)
    
    def setLooperSideChainLevel(self, track_id, sidechain_level):
        self.__sidechainLevels[track_id] = sidechain_level
        
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "L1SCT" + str(track_id + 1), MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, MASTER_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.__view.setLooperSideChainLevel(track_id, sidechain_level)
    
    def updateTracksStats(self):
        for track_id in self.__tracks:
            self.__tracks[track_id].updateStats()
    
    def updateLooperStats(self):
        self.__view.setLooperVolume(self.__looper_volume)
        self.__view.setResampleFXLevel(self.__turnado_dictator_level)
        
        if self.__looper_number != Looper.Looper_1:
            for track_id, sidechain_value in self.__sidechainLevels.items():
                self.__view.setLooperSideChainLevel(track_id, sidechain_value)
        else:
            for track_id, sidechain_value in self.__sidechainLevels.items():
                self.__view.setLooperSideChainLevel(track_id, 0.0)     
        
    def isTrackRecordingInProgress(self, track_id):
        return self.__tracks[track_id].isRecordingInProgress()
    
    def stopAllRecordings(self):
        for track_id in self.__tracks:
            if self.__tracks[track_id].isRecordingInProgress():
                self.__tracks[track_id].stopRecording()

    def setTurnadoDictatorLevel(self, turnado_dictator_level):        
        plugins.setParamValue(turnado_dictator_level, TURNADO_DICTATOR_PARAM_INDEX, self.__looper_channel, LOOPER_TURNADO_SLOT_INDEX)

        self.__turnado_dictator_level = turnado_dictator_level

        if self.__isTurnadoTurnedOn == False and turnado_dictator_level != 0.0:
            parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "L_" + str(self.__looper_number + 1) + "_TUR_A", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(1.0, parameter_id, MASTER_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            self.__isTurnadoTurnedOn = True
        elif self.__isTurnadoTurnedOn == True and turnado_dictator_level == 0.0:
            parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "L_" + str(self.__looper_number + 1) + "_TUR_A", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(0.0, parameter_id, MASTER_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            self.__isTurnadoTurnedOn = False
            
        self.__view.setResampleFXLevel(turnado_dictator_level)
    
    def randomizeTurnado(self):
        print(device_name + ': ' + Looper.randomizeTurnado.__name__)
        plugins.setParamValue(0.0, TURNADO_RANDOMIZE_PARAM_INDEX, self.__looper_channel, LOOPER_TURNADO_SLOT_INDEX)
        plugins.setParamValue(1.0, TURNADO_RANDOMIZE_PARAM_INDEX, self.__looper_channel, LOOPER_TURNADO_SLOT_INDEX)
        plugins.setParamValue(0.0, TURNADO_RANDOMIZE_PARAM_INDEX, self.__looper_channel, LOOPER_TURNADO_SLOT_INDEX)
       
class PressedSamplerButton:
    NONE      = -1;
    A_PRESSED = 0;
    B_PRESSED = 1;
    C_PRESSED = 2;
    D_PRESSED = 3;        

class KorgKaossPad3Plus_LooperMux:

    def __init__(self, view):
        self.__view = view
        self.__shift_pressed = False
        self.__pressed_sampler_buttons = set()
        self.__last_pressed_sampler_button = PressedSamplerButton.NONE
        self.__selected_looper = Looper.Looper_1
        self.__loopers = { Looper.Looper_1: Looper(Looper.Looper_1,
                                                   LOOPER_1_INITIAL_TRACK_CHANNEL,
                                                   self.__view),
                           Looper.Looper_2: Looper(Looper.Looper_2,
                                                   LOOPER_2_INITIAL_TRACK_CHANNEL,
                                                   self.__view),
                           Looper.Looper_3: Looper(Looper.Looper_3,
                                                   LOOPER_3_INITIAL_TRACK_CHANNEL,
                                                   self.__view),
                           Looper.Looper_4: Looper(Looper.Looper_4,
                                                   LOOPER_4_INITIAL_TRACK_CHANNEL,
                                                   self.__view) }
        self.__initialized = False
        self.__resample_mode = ResampleMode.NONE
        self.__buttons_last_press_time = {}

    def onInitScript(self):

        if False == self.__initialized:
            print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.onInitScript.__name__)

            try:
                for looper_id in self.__loopers:
                    self.__loopers[looper_id].onInitScript()
                mixer.setRouteTo(MIC_ROUTE_CHANNEL, MASTER_FX_1_CHANNEL, 1)
                mixer.setRouteTo(SYNTH_ROUTE_CHANNEL, MASTER_FX_1_CHANNEL, 1)
                self.__initialized = True
                self.clear()
                self.__view.setTempo(mixer.getCurrentTempo() / 1000.0)
                self.setSampleLength(SampleLength.LENGTH_1)
                self.setResampleMode(ResampleMode.NONE)
            except Exception as e:
                print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.onInitScript.__name__ + ": failed to initialize the script.")
                print(e)

    def isPlaying(self):
        return transport.isPlaying()

    def playStop(self):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.playStop.__name__)

        looper.clear()

        if transport.isPlaying():
            transport.stop()
            self.__view.setPlay(False)
        else:
            transport.start()
            self.__view.setPlay(True)

    def setTempo(self, tempo):
        targetTempo = tempo - tempo % 50
        currentTempo = mixer.getCurrentTempo() / 100.0
        if math.fabs( int(currentTempo/10) - int(targetTempo/10) ) >= TEMPO_JOG_ROTATION_THRESHOLD:
            jogRotation = int( targetTempo - currentTempo )
            print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.setTempo.__name__ + ": target tempo: " + str(targetTempo) + ", current tempo: " + str(currentTempo) + ", jog rotation: " + str(jogRotation))
            transport.globalTransport( 105, jogRotation )
            self.__view.setTempo(targetTempo / 10.0)

    def setShiftPressedState(self, shift_pressed):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.setShiftPressedState.__name__ + ": shift pressed - " + str(shift_pressed))

        view.setShiftPressedState(shift_pressed)

        self.__shift_pressed = shift_pressed

        if(True == shift_pressed):
            self.actionOnDoubleClick(MIDI_CC_SHIFT, self.__loopers[self.__selected_looper].randomizeTurnado)

    def getShiftPressedState(self):
        return self.__shift_pressed

    def addPressedSamplerButton(self, pressed_sampler_button):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.addPressedSamplerButton.__name__ + ": added sampler button - " + str(pressed_sampler_button))
        self.__pressed_sampler_buttons.add(pressed_sampler_button)
        self.__last_pressed_sampler_button = pressed_sampler_button

    def removePressedSamplerButton(self, released_sampler_button):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.addPressedSamplerButton.__name__ + ": removed sampler button - " + str(released_sampler_button))
        self.__pressed_sampler_buttons.remove(released_sampler_button)
        
        if self.__last_pressed_sampler_button == released_sampler_button:
            self.__last_pressed_sampler_button = PressedSamplerButton.NONE

    def selectLooper(self, selected_looper):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.selectLooper.__name__ + ": selected looper - " + str(selected_looper))
        
        if selected_looper != self.__selected_looper:
            
            self.__loopers[self.__selected_looper].stopAllRecordings()
            
            self.__selected_looper = selected_looper
            self.__loopers[self.__selected_looper].updateTracksStats()
            self.__loopers[self.__selected_looper].updateLooperStats()
            self.__view.selectLooper(selected_looper)

    def setLooperVolume(self, looper_volume):
        self.__loopers.get(self.__selected_looper).setLooperVolume(looper_volume)

    def setTrackVolume(self, track_index, track_volume):
        self.__loopers.get(self.__selected_looper).setTrackVolume(track_index, track_volume)

    def setSampleLength(self, sample_length):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.setSampleLength.__name__ + ": selected sample length - " + str(sample_length))
        self.__selectedSampleLength = sample_length
        self.__view.updateSampleLength(sample_length)

        #printAllPluginParameters(17, 9)

    def clear(self):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.clear.__name__)
        for looper_id in self.__loopers:
            self.__loopers[looper_id].clearLooper()
        self.selectLooper(Looper.Looper_1)
        self.setLooperVolume(fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.setDropIntencity(0.0)
        self.setSampleLength(SampleLength.LENGTH_1)
        self.setResampleMode(ResampleMode.NONE)
        self.__view.clear()

    def clearCurrentLooper(self):
        self.__loopers[self.__selected_looper].clearLooper()

    def clearTrack(self, track_id):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.clearTrack.__name__ + ": track - " + str(track_id))
        self.__loopers[self.__selected_looper].clearTrack(track_id)

    def setMasterRoutingLevel(self, routing_level):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "MasterFX1M", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(routing_level, parameter_id, MASTER_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "MasterFX1S", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(routing_level, parameter_id, MASTER_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def changeRecordingState(self, selected_track_id):
            print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.changeRecordingState.__name__ + ": track - " + str(selected_track_id))
            self.__changeRecordingStateTo(selected_track_id, not self.__loopers[self.__selected_looper].isTrackRecordingInProgress(selected_track_id))

    def actionOnDoubleClick(self, pressed_button, action):
        pressed_time = time.time()
        
        if not pressed_button in self.__buttons_last_press_time.keys():
            self.__buttons_last_press_time[pressed_button] = 0
        
        if (pressed_time - self.__buttons_last_press_time[pressed_button]) < 0.5:
            # double click
            self.__buttons_last_press_time[pressed_button] = 0
            action()
        else:
            self.__buttons_last_press_time[pressed_button] = pressed_time

    def __changeRecordingStateTo(self, selected_track_id, recording_state):
        if recording_state:
            self.__startRecordingTrack(selected_track_id)
            
            for track_id in self.__loopers[self.__selected_looper].getTracks():
                if track_id != selected_track_id:
                    self.__stopRecordingTrack(track_id)
            
            self.setMasterRoutingLevel(0)
            
        else:
            self.__stopRecordingTrack(selected_track_id)
            self.setMasterRoutingLevel(fl_helper.MAX_VOLUME_LEVEL_VALUE)

    def __startRecordingTrack(self, selected_track_id):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.__startRecordingTrack.__name__ + ": track - " + str(selected_track_id) + ", resample mode - " + str(self.getResampleMode()))
        self.__loopers[self.__selected_looper].startRecordingTrack(selected_track_id, self.__selectedSampleLength, self.getResampleMode())

        for looper_id in self.__loopers:
            for track_id in self.__loopers[looper_id].getTracks():
                if looper_id == self.__selected_looper:
                    if track_id == selected_track_id:
                        self.__loopers[looper_id].getTrack(track_id).setRoutingLevel(fl_helper.MAX_VOLUME_LEVEL_VALUE)
                    else:
                        self.__loopers[looper_id].getTrack(track_id).setRoutingLevel(0.0)
                else:
                    self.__loopers[looper_id].getTrack(track_id).setRoutingLevel(0.0)

    def __stopRecordingTrack(self, track_id):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.__stopRecordingTrack.__name__ + ": track - " + str(track_id))

        if self.__loopers[self.__selected_looper].getResampleMode(track_id) == ResampleMode.FROM_ALL_LOOPERS_TO_TRACK:
            # clear all tracks of all loopers, except the one for which recording is over
            for looper_id in self.__loopers:
                for track_id_it in self.__loopers[looper_id].getTracks():
                    if ( looper_id != self.__selected_looper or track_id_it != track_id ):
                        self.__loopers[looper_id].clearTrack(track_id_it)
                    else:
                        self.__loopers[looper_id].setTrackVolume(track_id_it, fl_helper.MAX_VOLUME_LEVEL_VALUE)

        self.__loopers[self.__selected_looper].stopRecordingTrack(track_id)
        self.__loopers[self.__selected_looper].getTrack(track_id).setRoutingLevel(0.0)
        self.setResampleMode(ResampleMode.NONE)

    def setInputSideChainLevel(self, track_id, sidechain_level):
        self.__loopers[Looper.Looper_1].setInputSideChainLevel(track_id, sidechain_level)

    def setLooperSideChainLevel(self, track_id, sidechain_level):
        if self.__selected_looper != Looper.Looper_1:
            self.__loopers[self.__selected_looper].setLooperSideChainLevel(track_id, sidechain_level)

    def setDropIntencity(self, drop_intencity):
        plugins.setParamValue(drop_intencity, ENDLESS_SMILE_PLUGIN_INTENSITY_PARAM_INDEX, LOOPER_ALL_CHANNEL, LOOPER_ALL_ENDLESS_SMILE_SLOT_INDEX)
        self.__view.setDropIntencity(drop_intencity)

    def setResampleMode(self, resample_mode):
        
        if resample_mode == self.getResampleMode():
            resample_mode = ResampleMode.NONE
        
        print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.setResampleMode.__name__ + ": to - " + str(resample_mode))
        self.__resample_mode = resample_mode
        
        self.__view.setResampleMode(resample_mode)
    
    def getResampleMode(self):
        return self.__resample_mode
    
    def setTurnadoDictatorLevel(self, turnado_dictator_level):
        self.__loopers[self.__selected_looper].setTurnadoDictatorLevel(turnado_dictator_level)

    def drop(self):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperMux.drop.__name__)
        self.setDropIntencity(0)
        self.__loopers[Looper.Looper_1].setTrackVolume(Track.Track_1, fl_helper.MAX_VOLUME_LEVEL_VALUE)
    
    def turnTrackOnOff(self, track_id):
        if 0 != self.__loopers[self.__selected_looper].getTrackVolume(track_id):
            self.__loopers[self.__selected_looper].setTrackVolume(track_id, 0.0)
        else:
            self.__loopers[self.__selected_looper].setTrackVolume(track_id, fl_helper.MAX_VOLUME_LEVEL_VALUE)
    
class View:
    def setShiftPressedState(self, shift_pressed):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "Shift", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(shift_pressed, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
        
    def setLooperVolume(self, looper_volume):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "Volume", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(looper_volume, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
        
    def setDropIntencity(self, drop_intencity):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "Drop FX", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(drop_intencity, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
        
    def selectLooper(self, selected_looper):
        
        for i in range(4):
            value = 0.0
            if i == selected_looper:
                value = 1.0
            
            parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "Looper " + str(i + 1), LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(value, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()
        
    def clear(self):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "Clear all", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
    def __clearOff(self):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "Clear all", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
    def __clearTracksOff(self):
        for i in range(Track.Track_4 + 1):
            parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "T" + str(i + 1) + "_Clear", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(0.0, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
    
    def setTrackVolume(self, track_index, track_volume):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "T" + str(track_index + 1) + "_Volume", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(track_volume, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
    
    def setPlay(self, value):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "Play", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(value, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
    
    def setInputSideChainLevel(self, track_id, sidechain_level):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "T" + str(track_id + 1) + "_Sidechain", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
    
    def setLooperSideChainLevel(self, track_id, sidechain_level):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "T" + str(track_id + 1) + "_L_S_CH", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
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
        
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "Resample selected looper", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(resample_looper, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "Resample all loopers", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(resample_all_loopers, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()
        
    def setTrackRecordingState(self, track_id, recording_state):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "T" + str(track_id + 1) + "_Recording", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(recording_state, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()
        
    def setTrackResamplingState(self, track_id, recording_state):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "T" + str(track_id + 1) + "_Resampling", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(recording_state, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()
    
    def setTrackClearState(self, track_id, recording_state):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "T" + str(track_id + 1) + "_Clear", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(recording_state, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
    
    def setTrackPlaybackState(self, track_id, recording_state):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "T" + str(track_id + 1) + "_Playback", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(recording_state, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()
    
    def resetToggleFlags(self):
        self.__clearOff()
        self.__clearTracksOff()
        
    def updateSampleLength(self, sample_length):
        
        for i in range(8):
            i_sample_length = int(math.pow(2, i))
            parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "Length_" + str(i_sample_length), LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            
            value = 0
            
            if(sample_length == i_sample_length):
                value = 1
                
            plugins.setParamValue(value, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
     
    def setTempo(self, tempo):
        tempo_hundred = int(tempo) // 100
        tempo_dozens = (tempo % 100) // 10
        tempo_units = (tempo % 10)
        
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "TH", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(tempo_hundred / 10, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "TD", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(tempo_dozens / 10, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "TU", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(tempo_units / 10, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
    def setTrackSampleLength(self, track_id, sample_length):
        sample_length_hundred = int(sample_length) // 100
        sample_length_dozens = (sample_length % 100) // 10
        sample_length_units = (sample_length % 10)
        
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "T" + str(track_id + 1) + "H", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sample_length_hundred / 10, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "T" + str(track_id + 1) + "D", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sample_length_dozens / 10, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "T" + str(track_id + 1) + "U", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sample_length_units / 10, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
    
    def setResampleFXLevel(self, fx_level):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(MASTER_CHANNEL, "Resample FX", LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(fx_level, parameter_id, MASTER_CHANNEL, LOOPER_MUX_CONTROL_SURFACE_MIXER_SLOT_INDEX)
    
view = View()
looper = KorgKaossPad3Plus_LooperMux(view)

def OnInit():
    looper.onInitScript()

def OnMidiMsg(event):

    looper.onInitScript()

    #fl_helper.printAllPluginParameters(LOOPER_1_CHANNEL, LOOPER_TURNADO_SLOT_INDEX)

    event.handled = False

    if event.data1 == MIDI_CC_TRACK_1_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.addPressedSamplerButton(PressedSamplerButton.A_PRESSED)
    elif event.data1 == MIDI_CC_TRACK_1_SAMPLING and event.data2 == KP3_PLUS_ABCD_RELEASED:
        looper.removePressedSamplerButton(PressedSamplerButton.A_PRESSED)
    elif event.data1 == MIDI_CC_TRACK_2_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.addPressedSamplerButton(PressedSamplerButton.B_PRESSED)
    elif event.data1 == MIDI_CC_TRACK_2_SAMPLING and event.data2 == KP3_PLUS_ABCD_RELEASED:
        looper.removePressedSamplerButton(PressedSamplerButton.B_PRESSED)
    elif event.data1 == MIDI_CC_TRACK_3_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.addPressedSamplerButton(PressedSamplerButton.C_PRESSED)
    elif event.data1 == MIDI_CC_TRACK_3_SAMPLING and event.data2 == KP3_PLUS_ABCD_RELEASED:
        looper.removePressedSamplerButton(PressedSamplerButton.C_PRESSED)
    elif event.data1 == MIDI_CC_TRACK_4_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.addPressedSamplerButton(PressedSamplerButton.D_PRESSED)
    elif event.data1 == MIDI_CC_TRACK_4_SAMPLING and event.data2 == KP3_PLUS_ABCD_RELEASED:
        looper.removePressedSamplerButton(PressedSamplerButton.D_PRESSED)


    if event.data1 == MIDI_CC_LOOPER_VOLUME and looper.getShiftPressedState():
        looper.setDropIntencity( (fl_helper.MIDI_MAX_VALUE - event.data2) / fl_helper.MIDI_MAX_VALUE )
    elif event.data1 == MIDI_CC_RESAMPLE_MODE_FROM_LOOPER_TO_TRACK and looper.getShiftPressedState():
        looper.setResampleMode(ResampleMode.FROM_LOOPER_TO_TRACK)
    elif event.data1 == MIDI_CC_RESAMPLE_MODE_FROM_ALL_LOOPERS_TO_TRACK and looper.getShiftPressedState():
        looper.setResampleMode(ResampleMode.FROM_ALL_LOOPERS_TO_TRACK)
    elif event.data1 == MIDI_CC_LOOPER_1 and looper.getShiftPressedState():
        looper.selectLooper(Looper.Looper_1)
    elif event.data1 == MIDI_CC_LOOPER_2 and looper.getShiftPressedState():
        looper.selectLooper(Looper.Looper_2)
    elif event.data1 == MIDI_CC_LOOPER_3 and looper.getShiftPressedState():
        looper.selectLooper(Looper.Looper_3)
    elif event.data1 == MIDI_CC_LOOPER_4 and looper.getShiftPressedState():
        looper.selectLooper(Looper.Looper_4)
    elif event.data1 == MIDI_CC_CLEAR_LOOPER and looper.getShiftPressedState():
        looper.clearCurrentLooper()
    elif event.data1 == MIDI_CC_PLAY_STOP and looper.getShiftPressedState():
        looper.playStop()
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_1:
        looper.setSampleLength(SampleLength.LENGTH_1)
        looper.actionOnDoubleClick(MIDI_CC_SAMPLE_LENGTH_1, looper.drop)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_2:
        looper.setSampleLength(SampleLength.LENGTH_2)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_4:
        looper.setSampleLength(SampleLength.LENGTH_4)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_8:
        looper.setSampleLength(SampleLength.LENGTH_8)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_16:
        looper.setSampleLength(SampleLength.LENGTH_16)
        action = lambda looper = looper: looper.turnTrackOnOff(Track.Track_1)
        looper.actionOnDoubleClick(MIDI_CC_SAMPLE_LENGTH_16, action)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_32:
        looper.setSampleLength(SampleLength.LENGTH_32)
        action = lambda looper = looper: looper.turnTrackOnOff(Track.Track_2)
        looper.actionOnDoubleClick(MIDI_CC_SAMPLE_LENGTH_32, action)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_64:
        looper.setSampleLength(SampleLength.LENGTH_64)
        action = lambda looper = looper: looper.turnTrackOnOff(Track.Track_3)
        looper.actionOnDoubleClick(MIDI_CC_SAMPLE_LENGTH_64, action)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_128:
        looper.setSampleLength(SampleLength.LENGTH_128)
        action = lambda looper = looper: looper.turnTrackOnOff(Track.Track_4)
        looper.actionOnDoubleClick(MIDI_CC_SAMPLE_LENGTH_128, action)
    elif event.data1 == MIDI_CC_TRACK_1_CLEAR and event.data2 == KP3_PLUS_ABCD_PRESSED and looper.getShiftPressedState():
        looper.clearTrack(Track.Track_1)
    elif event.data1 == MIDI_CC_TRACK_2_CLEAR and event.data2 == KP3_PLUS_ABCD_PRESSED and looper.getShiftPressedState():
        looper.clearTrack(Track.Track_2)
    elif event.data1 == MIDI_CC_TRACK_3_CLEAR and event.data2 == KP3_PLUS_ABCD_PRESSED and looper.getShiftPressedState():
        looper.clearTrack(Track.Track_3)
    elif event.data1 == MIDI_CC_TRACK_4_CLEAR and event.data2 == KP3_PLUS_ABCD_PRESSED and looper.getShiftPressedState():
        looper.clearTrack(Track.Track_4)
    elif event.data1 == MIDI_CC_SHIFT:
        looper.setShiftPressedState(event.data2 == fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TEMPO and looper.getShiftPressedState() and not looper.isPlaying():
        looper.setTempo(800 + int((event.data2 / fl_helper.MIDI_MAX_VALUE) * 1000.0)) # from 80 to 180
    elif event.data1 == MIDI_CC_LOOPER_VOLUME:
        looper.setLooperVolume((event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
    elif event.data1 == MIDI_CC_TRACK_VOLUME_1:
        looper.setTrackVolume(0, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
    elif event.data1 == MIDI_CC_TRACK_VOLUME_2:
        looper.setTrackVolume(1, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
    elif event.data1 == MIDI_CC_TRACK_VOLUME_3:
        looper.setTrackVolume(2, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
    elif event.data1 == MIDI_CC_TRACK_VOLUME_4:
        looper.setTrackVolume(3, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
    elif event.data1 == MIDI_CC_TRACK_1_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.changeRecordingState(Track.Track_1)
    elif event.data1 == MIDI_CC_TRACK_2_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.changeRecordingState(Track.Track_2)
    elif event.data1 == MIDI_CC_TRACK_3_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.changeRecordingState(Track.Track_3)
    elif event.data1 == MIDI_CC_TRACK_4_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.changeRecordingState(Track.Track_4)
    elif event.data1 == MIDI_CC_TRACK_SIDECHAIN_1 and looper.getShiftPressedState():
        looper.setLooperSideChainLevel(Track.Track_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TRACK_SIDECHAIN_2 and looper.getShiftPressedState():
        looper.setLooperSideChainLevel(Track.Track_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TRACK_SIDECHAIN_3 and looper.getShiftPressedState():
        looper.setLooperSideChainLevel(Track.Track_3, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TRACK_SIDECHAIN_4 and looper.getShiftPressedState():
        looper.setLooperSideChainLevel(Track.Track_4, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TRACK_SIDECHAIN_1:
        looper.setInputSideChainLevel(Track.Track_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TRACK_SIDECHAIN_2:
        looper.setInputSideChainLevel(Track.Track_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TRACK_SIDECHAIN_3:
        looper.setInputSideChainLevel(Track.Track_3, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TRACK_SIDECHAIN_4:
        looper.setInputSideChainLevel(Track.Track_4, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TURNADO_DICTATOR:
        looper.setTurnadoDictatorLevel(event.data2 / fl_helper.MIDI_MAX_VALUE)

    event.handled = True
