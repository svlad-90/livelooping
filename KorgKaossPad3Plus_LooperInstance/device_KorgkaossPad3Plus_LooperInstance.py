# name=KorgKaossPad3Plus_LooperInstance
device_name="KorgKaossPad3Plus_LooperInstance"
print(device_name + ': started')

# python imports
import math

# FL imports
import transport
import mixer
import plugins

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

MIDI_CC_TRACK_1_CLEAR       = 36
MIDI_CC_TRACK_2_CLEAR       = 37
MIDI_CC_TRACK_3_CLEAR       = 38
MIDI_CC_TRACK_4_CLEAR       = 39

MIDI_CC_TRACK_1_SAMPLING    = 36
MIDI_CC_TRACK_2_SAMPLING    = 37
MIDI_CC_TRACK_3_SAMPLING    = 38
MIDI_CC_TRACK_4_SAMPLING    = 39

# ROUTING
MASTER_CHANNEL               = 0
MASTER_FX_1_CHANNEL          = 2
MIC_ROUTE_CHANNEL            = 4
SYNTH_ROUTE_CHANNEL          = 8
LOOPER_ALL_CHANNEL           = 12

# CONSTANTS
LOOPER_1_INITIAL_MIXER_TRACK = 17
LOOPER_2_INITIAL_MIXER_TRACK = 25
LOOPER_3_INITIAL_MIXER_TRACK = 33
LOOPER_4_INITIAL_MIXER_TRACK = 41

KP3_PLUS_ABCD_PRESSED        = 100
KP3_PLUS_ABCD_RELEASED       = 64

# MASTER MIXER SLOT INDICES
CONTROL_SURFACE_MIXER_SLOT_INDEX = 0

# MIXER SLOT INDICES
TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX = 0
TRACK_PANOMATIC_VOLUME_PLUGIN_MIXER_SLOT_INDEX = 8
LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX = 9
LOOPER_ALL_ENDLESS_SMILE_SLOT_INDEX = 8

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

TEMPO_JOG_ROTATION_THRESHOLD = 5

MIDI_MAX_VALUE = 127

def printAllPluginParameters(mixer_track, slot):
    
    number_of_params = plugins.getParamCount(mixer_track, slot)
    plugin_name = plugins.getPluginName(mixer_track, slot)
    
    print("Parameters of the plugin \"" + plugin_name + "\":")
    
    for param_index in range(number_of_params):
        print( "#" + str(param_index) + ": param name - " + plugins.getParamName(param_index, mixer_track, slot) + \
               " param value - " + str( plugins.getParamValue(param_index, mixer_track, slot) ) )

def findSurfaceControlElementIdByName(control_element_name):
    number_of_parameters = plugins.getParamCount(MASTER_CHANNEL, CONTROL_SURFACE_MIXER_SLOT_INDEX)
    
    for parameter_id in range(number_of_parameters):
        parameter_name = plugins.getParamName(parameter_id, MASTER_CHANNEL, CONTROL_SURFACE_MIXER_SLOT_INDEX)
        if(parameter_name == control_element_name):
            return parameter_id  
    raise Exception("Control element " + control_element_name + " not found")

class SampleLength:
    LENGTH_1 = 1
    LENGTH_2 = 2
    LENGTH_4 = 4
    LENGTH_8 = 8
    LENGTH_16 = 16
    LENGTH_32 = 32
    LENGTH_64 = 64
    LENGTH_128 = 128

class Track():
    
    Track_1    = 0
    Track_2    = 1
    Track_3    = 2
    Track_4    = 3
    
    def __init__(self, looper_number, track_number, mixer_track):
        self.__looper_number = looper_number
        self.__track_number = track_number
        self.__mixer_track = mixer_track
        self.__sample_length = SampleLength.LENGTH_1
    
    def onInitScript(self):
        self.resetTrackParams()
        self.setTrackVolume(0.8)
        
    def setLooperVolume(self, looperVolume):
        mixer.setTrackVolume(self.__mixer_track, looperVolume)
        
    def setTrackVolume(self, trackVolume):
        plugins.setParamValue(trackVolume, PANOMATIC_VOLUME_PARAM_INDEX, self.__mixer_track, TRACK_PANOMATIC_VOLUME_PLUGIN_MIXER_SLOT_INDEX)
    
    def clear(self):
        plugins.setParamValue(1, AUGUSTUS_LOOP_PLUGIN_CLEAR_LOOP_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
    
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
            plugins.setParamValue(0.8, PEAK_CONTROLLER_BASE_PARAM_INDEX, self.__mixer_track, LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX)
            plugins.setParamValue(0.12, PEAK_CONTROLLER_VOLUME_PARAM_INDEX, self.__mixer_track, LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX)
            plugins.setParamValue(0.85, PEAK_CONTROLLER_TENSION_PARAM_INDEX, self.__mixer_track, LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX)
            plugins.setParamValue(0.5, PEAK_CONTROLLER_DECAY_PARAM_INDEX, self.__mixer_track, LOOPER_1_PEAK_CONTROLLER_SIDECHAIN_SLOT_INDEX)
        
        self.__setRouting();
        
        self.setSampleLength(self.__sample_length, True) 
    
    def setSampleLength(self, sample_length, unconditionally = False):
        
        if(sample_length != self.__sample_length or True == unconditionally):            
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
        
    def startRecording(self, sample_length):
        self.setSampleLength(sample_length)
        plugins.setParamValue(1.0, AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
    
    def stopRecording(self):
        plugins.setParamValue(0.0, AUGUSTUS_LOOP_PLUGIN_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        
    def __setRouting(self):
        mixer.setRouteTo(MIC_ROUTE_CHANNEL, self.__mixer_track, 1)
        mixer.setRouteTo(SYNTH_ROUTE_CHANNEL, self.__mixer_track, 1)
        
    def __removeRouting(self):
        mixer.setRouteTo(MIC_ROUTE_CHANNEL, self.__mixer_track, 0)
        mixer.setRouteTo(SYNTH_ROUTE_CHANNEL, self.__mixer_track, 0)
        
    def setRoutingLevel(self, routing_level):
        parameter_id = findSurfaceControlElementIdByName("L" + str(self.__looper_number + 1) + "T" + str(self.__track_number + 1) + "M")
        plugins.setParamValue(routing_level, parameter_id, MASTER_CHANNEL, CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = findSurfaceControlElementIdByName("L" + str(self.__looper_number + 1) + "T" + str(self.__track_number + 1) + "S")
        plugins.setParamValue(routing_level, parameter_id, MASTER_CHANNEL, CONTROL_SURFACE_MIXER_SLOT_INDEX)
    
    def setSideChainLevel(self, sidechain_level):
        parameter_id = findSurfaceControlElementIdByName("M2L1T" + str(self.__track_number + 1) + "S")
        plugins.setParamValue(sidechain_level, parameter_id, MASTER_CHANNEL, CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = findSurfaceControlElementIdByName("S2L1T" + str(self.__track_number + 1) + "S")
        plugins.setParamValue(sidechain_level, parameter_id, MASTER_CHANNEL, CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
class Looper():
    Looper_1    = 0
    Looper_2    = 1
    Looper_3    = 2
    Looper_4    = 3
    
    def __init__(self, looper_number, initial_mixer_track):
        self.__looper_number = looper_number
        self.__initial_mixer_track__ = initial_mixer_track
        self.__tracks = { Track.Track_1: Track(looper_number, Track.Track_1, 
                                               initial_mixer_track + Track.Track_1),
                          Track.Track_2: Track(looper_number, Track.Track_2, 
                                               initial_mixer_track + Track.Track_2),
                          Track.Track_3: Track(looper_number, Track.Track_3, 
                                               initial_mixer_track + Track.Track_3),
                          Track.Track_4: Track(looper_number, Track.Track_4, 
                                               initial_mixer_track + Track.Track_4) }
    
    def onInitScript(self):
        for track_id in self.__tracks:
            self.__tracks[track_id].onInitScript() 
    
    def getLooperNumber(self):
        return self.__looper_number
    
    def getTracks(self):
        return self.__tracks
    
    def getTrack(self, track_number):
        return self.__tracks.get(track_number)
    
    def setLooperVolume(self, looperVolume):
        for track_id in self.__tracks:
            self.__tracks[track_id].setLooperVolume(looperVolume)
            
    def setTrackVolume(self, track_id, trackVolume):
        self.__tracks.get(track_id).setTrackVolume(trackVolume)
        
    def clearLooper(self):
        for track_id in self.__tracks:
            self.__tracks[track_id].clear()
            self.__tracks[track_id].resetTrackParams()
            
    def clearTrack(self, track_id):
            self.__tracks[track_id].clear()
            
    def startRecordingTrack(self, track_id, sample_length):
        self.__tracks[track_id].startRecording(sample_length)
        
    def stopRecordingTrack(self, track_id):
        self.__tracks[track_id].stopRecording()
        
    def setSideChainLevel(self, track_id, sidechain_level):
        self.__tracks[track_id].setSideChainLevel(sidechain_level)

class PressedSamplerButton:
    A_PRESSED = 0;
    B_PRESSED = 1;
    C_PRESSED = 2;
    D_PRESSED = 3;
   
class KorgKaossPad3Plus_LooperInstance:
 
    def __init__(self):
        self.__shiftPressed = False
        self.__pressedSamplerButtons = set()
        self.__selectedLooper = Looper.Looper_1
        self.__loopers = { Looper.Looper_1: Looper(Looper.Looper_1, 
                                                   LOOPER_1_INITIAL_MIXER_TRACK),
                           Looper.Looper_2: Looper(Looper.Looper_2, 
                                                   LOOPER_2_INITIAL_MIXER_TRACK),
                           Looper.Looper_3: Looper(Looper.Looper_3, 
                                                   LOOPER_3_INITIAL_MIXER_TRACK),
                           Looper.Looper_4: Looper(Looper.Looper_4, 
                                                   LOOPER_4_INITIAL_MIXER_TRACK) }
        self.__selectedSampleLength = SampleLength.LENGTH_1
        self.__initialized = False
        
    def onInitScript(self):
        
        if False == self.__initialized:
            print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.onInitScript.__name__)
            
            try:
                for looper_id in self.__loopers:
                    self.__loopers[looper_id].onInitScript()
                mixer.setRouteTo(MIC_ROUTE_CHANNEL, MASTER_FX_1_CHANNEL, 1)
                mixer.setRouteTo(SYNTH_ROUTE_CHANNEL, MASTER_FX_1_CHANNEL, 1)
                self.__initialized = True
            except Exception as e:
                print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.onInitScript.__name__ + ": failed to initialize the script.")
                print(e)
    
    def playStop(self):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.playStop.__name__)
        
        looper.clear()
        
        if transport.isPlaying():
            transport.stop()
        else:
            transport.start()
        
    def setTempo(self, tempo):
        targetTempo = tempo - tempo % 50
        currentTempo = mixer.getCurrentTempo() / 100.0
        if math.fabs( int(currentTempo/10) - int(targetTempo/10) ) >= TEMPO_JOG_ROTATION_THRESHOLD:
            jogRotation = int( targetTempo - currentTempo )
            print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.setTempo.__name__ + ": target tempo: " + str(targetTempo) + ", current tempo: " + str(currentTempo) + ", jog rotation: " + str(jogRotation))
            transport.globalTransport( 105, jogRotation )
        
    def setShiftPressedState(self, shiftPressed):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.setShiftPressedState.__name__ + ": shift pressed - " + str(shiftPressed))
        self.__shiftPressed = shiftPressed
        
        if(False == shiftPressed):
            for element in self.__pressedSamplerButtons:
                if(element == PressedSamplerButton.A_PRESSED):
                    self.startRecordingTrack(Track.Track_1)
                elif(element == PressedSamplerButton.B_PRESSED):
                    self.startRecordingTrack(Track.Track_2)
                elif(element == PressedSamplerButton.C_PRESSED):
                    self.startRecordingTrack(Track.Track_3)
                elif(element == PressedSamplerButton.D_PRESSED):
                    self.startRecordingTrack(Track.Track_4)
        
    def getShiftPressedState(self):
        return self.__shiftPressed
    
    def addPressedSamplerButton(self, pressedSamplerButton):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.addPressedSamplerButton.__name__ + ": added sampelr button - " + str(pressedSamplerButton))
        self.__pressedSamplerButtons.add(pressedSamplerButton)
        
    def removePressedSamplerButton(self, releasedSamplerButton):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.addPressedSamplerButton.__name__ + ": removed sampelr button - " + str(releasedSamplerButton))
        self.__pressedSamplerButtons.remove(releasedSamplerButton)
    
    def selectLooper(self, selectedLooper):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.selectLooper.__name__ + ": selected looper - " + str(selectedLooper))
        self.__selectedLooper = selectedLooper
        
    def setLooperVolume(self, looperVolume):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.setLooperVolume.__name__ + ": selected looper - " + str(self.__selectedLooper) + ", looper volume - " + str(looperVolume))
        self.__loopers.get(self.__selectedLooper).setLooperVolume(looperVolume)
            
    def setTrackVolume(self, trackIndex, trackVolume):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.setTrackVolume.__name__ + ": track index - " + str(trackIndex) + ", track volume - " + str(trackVolume))

        self.__loopers.get(self.__selectedLooper).setTrackVolume(trackIndex, trackVolume)
        
    def setSampleLength(self, sampleLength):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.setSampleLength.__name__ + ": selected sample length - " + str(sampleLength))
        self.__selectedSampleLength = sampleLength
        
        #printAllPluginParameters(17, 9)
        
    def clear(self):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.clear.__name__)
        for looper_id in self.__loopers:
            self.__loopers[looper_id].clearLooper()
            
    def clearTrack(self, track_id):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.clearTrack.__name__ + ": track - " + str(track_id))
        self.__loopers[self.__selectedLooper].clearTrack(track_id)
    
    def setMasterRoutingLevel(self, routing_level):
        parameter_id = findSurfaceControlElementIdByName("MasterFX1M")
        plugins.setParamValue(routing_level, parameter_id, MASTER_CHANNEL, CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = findSurfaceControlElementIdByName("MasterFX1S")
        plugins.setParamValue(routing_level, parameter_id, MASTER_CHANNEL, CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def startRecordingTrack(self, selected_track_id):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.startRecordingTrack.__name__ + ": track - " + str(selected_track_id))
        self.__loopers[self.__selectedLooper].startRecordingTrack(selected_track_id, self.__selectedSampleLength)
        
        for looper_id in self.__loopers:
            for track_id in self.__loopers[looper_id].getTracks():
                if looper_id == self.__selectedLooper:
                    if track_id == selected_track_id:
                        self.__loopers[looper_id].getTrack(track_id).setRoutingLevel(0.8)
                    else:
                        self.__loopers[looper_id].getTrack(track_id).setRoutingLevel(0.0)
                else:
                    self.__loopers[looper_id].getTrack(track_id).setRoutingLevel(0.0)
        
        self.setMasterRoutingLevel(0.0)
        
    def stopRecordingTrack(self, track_id):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.stopRecordingTrack.__name__ + ": track - " + str(track_id))
        self.__loopers[self.__selectedLooper].stopRecordingTrack(track_id)
        
        self.__loopers[self.__selectedLooper].getTrack(track_id).setRoutingLevel(0.0)
        
        self.setMasterRoutingLevel(0.8)
        
    def setSideChainLevel(self, track_id, sidechain_level):
        self.__loopers[Looper.Looper_1].setSideChainLevel(track_id, sidechain_level)
    
    def setDropIntencity(self, drop_intencity):
        plugins.setParamValue(drop_intencity, ENDLESS_SMILE_PLUGIN_INTENSITY_PARAM_INDEX, LOOPER_ALL_CHANNEL, LOOPER_ALL_ENDLESS_SMILE_SLOT_INDEX)
    
looper = KorgKaossPad3Plus_LooperInstance()

def OnInit():
    looper.onInitScript()
 
def OnMidiMsg(event):
    
    looper.onInitScript()
        
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
        looper.setDropIntencity( (MIDI_MAX_VALUE - event.data2) / MIDI_MAX_VALUE )
    elif event.data1 == MIDI_CC_LOOPER_1 and looper.getShiftPressedState():
        looper.selectLooper(Looper.Looper_1)
    elif event.data1 == MIDI_CC_LOOPER_2 and looper.getShiftPressedState():
        looper.selectLooper(Looper.Looper_2)
    elif event.data1 == MIDI_CC_LOOPER_3 and looper.getShiftPressedState():
        looper.selectLooper(Looper.Looper_3)
    elif event.data1 == MIDI_CC_LOOPER_4 and looper.getShiftPressedState():
        looper.selectLooper(Looper.Looper_4)
    elif event.data1 == MIDI_CC_CLEAR_LOOPER and looper.getShiftPressedState():
        looper.clear()
    elif event.data1 == MIDI_CC_PLAY_STOP and looper.getShiftPressedState():
        looper.playStop()
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_1:
        looper.setSampleLength(SampleLength.LENGTH_1)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_2:
        looper.setSampleLength(SampleLength.LENGTH_2)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_4:
        looper.setSampleLength(SampleLength.LENGTH_4)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_8:
        looper.setSampleLength(SampleLength.LENGTH_8)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_16:
        looper.setSampleLength(SampleLength.LENGTH_16)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_32:
        looper.setSampleLength(SampleLength.LENGTH_32)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_64:
        looper.setSampleLength(SampleLength.LENGTH_64)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_128:
        looper.setSampleLength(SampleLength.LENGTH_128)
    elif event.data1 == MIDI_CC_TRACK_1_CLEAR and event.data2 == KP3_PLUS_ABCD_PRESSED and looper.getShiftPressedState():
        looper.clearTrack(Track.Track_1)
        looper.stopRecordingTrack(Track.Track_1)
    elif event.data1 == MIDI_CC_TRACK_2_CLEAR and event.data2 == KP3_PLUS_ABCD_PRESSED and looper.getShiftPressedState():
        looper.clearTrack(Track.Track_2)
        looper.stopRecordingTrack(Track.Track_2)
    elif event.data1 == MIDI_CC_TRACK_3_CLEAR and event.data2 == KP3_PLUS_ABCD_PRESSED and looper.getShiftPressedState():
        looper.clearTrack(Track.Track_3)
        looper.stopRecordingTrack(Track.Track_3)
    elif event.data1 == MIDI_CC_TRACK_4_CLEAR and event.data2 == KP3_PLUS_ABCD_PRESSED and looper.getShiftPressedState():
        looper.clearTrack(Track.Track_4)
        looper.stopRecordingTrack(Track.Track_4)
    elif event.data1 == MIDI_CC_SHIFT:
        looper.setShiftPressedState(event.data2 == MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TEMPO and looper.getShiftPressedState():
        looper.setTempo(800 + int((event.data2 / MIDI_MAX_VALUE) * 1000.0)) # from 80 to 180
    elif event.data1 == MIDI_CC_LOOPER_VOLUME:
        looper.setLooperVolume((event.data2 / MIDI_MAX_VALUE) * 0.8)
    elif event.data1 == MIDI_CC_TRACK_VOLUME_1:
        looper.setTrackVolume(0, (event.data2 / MIDI_MAX_VALUE) * 0.8)
    elif event.data1 == MIDI_CC_TRACK_VOLUME_2:
        looper.setTrackVolume(1, (event.data2 / MIDI_MAX_VALUE) * 0.8)
    elif event.data1 == MIDI_CC_TRACK_VOLUME_3:
        looper.setTrackVolume(2, (event.data2 / MIDI_MAX_VALUE) * 0.8)
    elif event.data1 == MIDI_CC_TRACK_VOLUME_4:
        looper.setTrackVolume(3, (event.data2 / MIDI_MAX_VALUE) * 0.8)
    elif event.data1 == MIDI_CC_TRACK_1_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.startRecordingTrack(Track.Track_1)
    elif event.data1 == MIDI_CC_TRACK_1_SAMPLING and event.data2 == KP3_PLUS_ABCD_RELEASED:
        looper.stopRecordingTrack(Track.Track_1)
    elif event.data1 == MIDI_CC_TRACK_2_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.startRecordingTrack(Track.Track_2)
    elif event.data1 == MIDI_CC_TRACK_2_SAMPLING and event.data2 == KP3_PLUS_ABCD_RELEASED:
        looper.stopRecordingTrack(Track.Track_2)
    elif event.data1 == MIDI_CC_TRACK_3_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.startRecordingTrack(Track.Track_3)
    elif event.data1 == MIDI_CC_TRACK_3_SAMPLING and event.data2 == KP3_PLUS_ABCD_RELEASED:
        looper.stopRecordingTrack(Track.Track_3)
    elif event.data1 == MIDI_CC_TRACK_4_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.startRecordingTrack(Track.Track_4)
    elif event.data1 == MIDI_CC_TRACK_4_SAMPLING and event.data2 == KP3_PLUS_ABCD_RELEASED:
        looper.stopRecordingTrack(Track.Track_4)
    elif event.data1 == MIDI_CC_TRACK_SIDECHAIN_1:
        looper.setSideChainLevel(Track.Track_1, event.data2 / MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TRACK_SIDECHAIN_2:
        looper.setSideChainLevel(Track.Track_2, event.data2 / MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TRACK_SIDECHAIN_3:
        looper.setSideChainLevel(Track.Track_3, event.data2 / MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TRACK_SIDECHAIN_4:
        looper.setSideChainLevel(Track.Track_4, event.data2 / MIDI_MAX_VALUE)
        
    event.handled = True
