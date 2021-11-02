# name=KorgKaossPad3Plus_LooperInstance
from random import sample
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
MIDI_CC_CLEAR_LOOPER        = 55
MIDI_CC_SAMPLE_LENGTH_1     = 49
MIDI_CC_SAMPLE_LENGTH_2     = 50
MIDI_CC_SAMPLE_LENGTH_4     = 51
MIDI_CC_SAMPLE_LENGTH_8     = 52
MIDI_CC_SAMPLE_LENGTH_16    = 53
MIDI_CC_SAMPLE_LENGTH_32    = 54
MIDI_CC_SAMPLE_LENGTH_64    = 55
MIDI_CC_SAMPLE_LENGTH_128   = 56

MIDI_CC_LENGTH              = 56
MIDI_CC_SAMPLE              = 123

MIDI_CC_TRACK_1_CLEAR       = 36
MIDI_CC_TRACK_2_CLEAR       = 37
MIDI_CC_TRACK_3_CLEAR       = 38
MIDI_CC_TRACK_4_CLEAR       = 39

MIDI_CC_TRACK_1_SAMPLING    = 36
MIDI_CC_TRACK_2_SAMPLING    = 37
MIDI_CC_TRACK_3_SAMPLING    = 38
MIDI_CC_TRACK_4_SAMPLING    = 39

# CONSTANTS
LOOPER_1_INITIAL_MIXER_TRACK = 17
LOOPER_2_INITIAL_MIXER_TRACK = 25
LOOPER_3_INITIAL_MIXER_TRACK = 33
LOOPER_4_INITIAL_MIXER_TRACK = 41

KP3_PLUS_ABCD_PRESSED        = 100
KP3_PLUS_ABCD_RELEASED       = 64

# MIXER SLOT INDEXES
TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX = 0
TRACK_PANOMATIC_VOLUME_PLUGIN_MIXER_SLOT_INDEX = 9

# PLUGIN PARAMETERS

AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX = 0
AUGUSTUS_LOOP_PLUGIN_DELAY_TIME_PARAM_INDEX = 1
AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MIN_PARAM_INDEX = 2
AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX = 3
AUGUSTUS_LOOP_PLUGIN_EFFECT_LEVEL_PARAM_INDEX = 22
AUGUSTUS_LOOP_INPUT_LEVEL_PARAM_INDEX = 31
AUGUSTUS_LOOP_HOST_TEMPO_PARAM_INDEX = 33
AUGUSTUS_LOOP_BEATS_PARAM_INDEX = 34
AUGUSTUS_LOOP_BEATS_DIVISOR_PARAM_INDEX = 35
AUGUSTUS_LOOP_CLEAR_LOOP_PARAM_INDEX = 49

PANOMATIC_VOLUME_PARAM_INDEX = 1

TEMPO_JOG_ROTATION_THRESHOLD = 5

MIDI_MAX_VALUE = 127

def printAllPluginParameters(mixer_track, slot):
    
    number_of_params = plugins.getParamCount(mixer_track, slot)
    plugin_name = plugins.getPluginName(mixer_track, slot)
    
    print("Parameters of the plugin \"" + plugin_name + "\":")
    
    for param_index in range(number_of_params):
        print( "#" + str(param_index) + ": param name - " + plugins.getParamName(param_index, mixer_track, slot) + \
               "; param value - " + str( plugins.getParamValue(param_index, mixer_track, slot) ) )

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
    
    def __init__(self, track_number, mixer_track):
        self.__track_number = track_number
        self.__mixer_track = mixer_track
        self.__sample_length = SampleLength.LENGTH_1
    
    def onInitScript(self):
        self.resetTrackParams()
        
    def setLooperVolume(self, looperVolume):
        mixer.setTrackVolume(self.__mixer_track, looperVolume)
        
    def setTrackVolume(self, trackVolume):
        plugins.setParamValue(trackVolume, PANOMATIC_VOLUME_PARAM_INDEX, self.__mixer_track, TRACK_PANOMATIC_VOLUME_PLUGIN_MIXER_SLOT_INDEX)
    
    def clear(self):
        plugins.setParamValue(1, AUGUSTUS_LOOP_CLEAR_LOOP_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)    
    
    def resetTrackParams(self):
        plugins.setParamValue(0.0, AUGUSTUS_LOOP_PLUGIN_DELAY_TIME_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.938302, AUGUSTUS_LOOP_PLUGIN_MAX_DELAY_TIME_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(0, AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MIN_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.938576, AUGUSTUS_LOOP_PLUGIN_DELAY_SLIDER_MAX_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, AUGUSTUS_LOOP_HOST_TEMPO_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.99219, AUGUSTUS_LOOP_BEATS_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.995, AUGUSTUS_LOOP_BEATS_DIVISOR_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.99218, AUGUSTUS_LOOP_PLUGIN_EFFECT_LEVEL_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, AUGUSTUS_LOOP_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
    
    def startRecording(self, sample_length):
        if(sample_length == self.__sample_length):
            plugins.setParamValue(0.99218, AUGUSTUS_LOOP_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        else:
            self.__sample_length == sample_length
            
            plugins.setParamValue(0.99218, AUGUSTUS_LOOP_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
        
    def stopRecording(self):
        plugins.setParamValue(0.0, AUGUSTUS_LOOP_INPUT_LEVEL_PARAM_INDEX, self.__mixer_track, TRACK_AUGUSTUS_LOOP_PLUGIN_MIXER_SLOT_INDEX)
    
class Looper():
    Looper_1    = 0
    Looper_2    = 1
    Looper_3    = 2
    Looper_4    = 3
    
    def __init__(self, looper_number, initial_mixer_track):
        self.__looper_number = looper_number
        self.__initial_mixer_track__ = initial_mixer_track
        self.__tracks = { Track.Track_1: Track(Track.Track_1, initial_mixer_track + Track.Track_1),
                          Track.Track_2: Track(Track.Track_2, initial_mixer_track + Track.Track_2),
                          Track.Track_3: Track(Track.Track_3, initial_mixer_track + Track.Track_3),
                          Track.Track_4: Track(Track.Track_4, initial_mixer_track + Track.Track_4) }
    
    def onInitScript(self):
        for track_id in self.__tracks:
            self.__tracks[track_id].onInitScript() 
    
    def getLooperNumber(self):
        return self.__looper_number
    
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
        self.__tracks[track_id].startRecording(sample_length);
        
    def stopRecordingTrack(self, track_id):
        self.__tracks[track_id].stopRecording();
        
class KorgKaossPad3Plus_LooperInstance:
 
    def __init__(self):
        self.__shiftPressed = False
        self.__selectedLooper = Looper.Looper_1
        self.__loopers = { Looper.Looper_1: Looper(Looper.Looper_1, LOOPER_1_INITIAL_MIXER_TRACK),
                           Looper.Looper_2: Looper(Looper.Looper_2, LOOPER_2_INITIAL_MIXER_TRACK),
                           Looper.Looper_3: Looper(Looper.Looper_3, LOOPER_3_INITIAL_MIXER_TRACK),
                           Looper.Looper_4: Looper(Looper.Looper_4, LOOPER_4_INITIAL_MIXER_TRACK) }
        self.__selectedSampleLength = SampleLength.LENGTH_1
        
    def onInitScript(self):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.onInitScript.__name__);
        for looper_id in self.__loopers:
            self.__loopers[looper_id].onInitScript();
    
    def playStop(self):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.playStop.__name__);
        
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
            print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.setTempo.__name__ + ": target tempo: " + str(targetTempo) + ", current tempo: " + str(currentTempo) + ", jog rotation: " + str(jogRotation));
            transport.globalTransport( 105, jogRotation )
        
    def setShiftPressedState(self, shiftPressed):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.setShiftPressedState.__name__ + ": shift pressed - " + str(shiftPressed));
        self.__shiftPressed = shiftPressed
        
    def getShiftPressedState(self):
        return self.__shiftPressed
    
    def selectLooper(self, selectedLooper):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.selectLooper.__name__ + ": selected looper - " + str(selectedLooper));
        self.__selectedLooper = selectedLooper
        
    def setLooperVolume(self, looperVolume):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.setLooperVolume.__name__ + ": selected looper - " + str(self.__selectedLooper) + ", looper volume - " + str(looperVolume));
        self.__loopers.get(self.__selectedLooper).setLooperVolume(looperVolume)
            
    def setTrackVolume(self, trackIndex, trackVolume):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.setTrackVolume.__name__ + ": track index - " + str(trackIndex) + ", track volume - " + str(trackVolume));
        
        # From 0.000000001 to 0.000000298
        trackVolumeNormalized = 0.000000001 + ( 0.000000297 * trackVolume )
        self.__loopers.get(self.__selectedLooper).setTrackVolume(trackIndex, trackVolumeNormalized)
        
    def setSampleLength(self, sampleLength):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.setSampleLength.__name__ + ": selected sample length - " + str(sampleLength))
        self.__selectedSampleLength = sampleLength
        
    def clear(self):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.clear.__name__);
        for looper_id in self.__loopers:
            self.__loopers[looper_id].clearLooper();
            
    def clearTrack(self, track_id):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.clearTrack.__name__ + ": track - " + str(track_id));
        self.__loopers[self.__selectedLooper].clearTrack(track_id);
        
    def startRecordingTrack(self, track_id):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.startRecordingTrack.__name__ + ": track - " + str(track_id));
        self.__loopers[self.__selectedLooper].startRecordingTrack(track_id, self.__selectedSampleLength);
        
    def stopRecordingTrack(self, track_id):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.stopRecordingTrack.__name__ + ": track - " + str(track_id));
        self.__loopers[self.__selectedLooper].stopRecordingTrack(track_id);
    
looper = KorgKaossPad3Plus_LooperInstance()

def OnInit():
    looper.onInitScript();
 
def OnMidiMsg(event):
        
    event.handled = False
    if event.data1 == MIDI_CC_SAMPLE_LENGTH_1 and looper.getShiftPressedState():
        looper.setSampleLength(SampleLength.LENGTH_1)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_2 and looper.getShiftPressedState():
        looper.setSampleLength(SampleLength.LENGTH_2)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_4 and looper.getShiftPressedState():
        looper.setSampleLength(SampleLength.LENGTH_4)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_8 and looper.getShiftPressedState():
        looper.setSampleLength(SampleLength.LENGTH_8)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_16 and looper.getShiftPressedState():
        looper.setSampleLength(SampleLength.LENGTH_16)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_32 and looper.getShiftPressedState():
        looper.setSampleLength(SampleLength.LENGTH_32)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_64 and looper.getShiftPressedState():
        looper.setSampleLength(SampleLength.LENGTH_64)
    elif event.data1 == MIDI_CC_SAMPLE_LENGTH_128 and looper.getShiftPressedState():
        looper.setSampleLength(SampleLength.LENGTH_128)
    elif event.data1 == MIDI_CC_TRACK_1_CLEAR and event.data2 == KP3_PLUS_ABCD_PRESSED and looper.getShiftPressedState():
        looper.clearTrack(Track.Track_1)
    elif event.data1 == MIDI_CC_TRACK_2_CLEAR and event.data2 == KP3_PLUS_ABCD_PRESSED and looper.getShiftPressedState():
        looper.clearTrack(Track.Track_2)
    elif event.data1 == MIDI_CC_TRACK_3_CLEAR and event.data2 == KP3_PLUS_ABCD_PRESSED and looper.getShiftPressedState():
        looper.clearTrack(Track.Track_3)
    elif event.data1 == MIDI_CC_TRACK_4_CLEAR and event.data2 == KP3_PLUS_ABCD_PRESSED and looper.getShiftPressedState():
        looper.clearTrack(Track.Track_4)
    elif event.data1 == MIDI_CC_PLAY_STOP:
        looper.playStop()
    elif event.data1 == MIDI_CC_SHIFT:
        looper.setShiftPressedState(event.data2 == MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_TEMPO and looper.getShiftPressedState():
        looper.setTempo(800 + int((event.data2 / MIDI_MAX_VALUE) * 1000.0)) # from 80 to 180
    elif event.data1 == MIDI_CC_LOOPER_1:
        looper.selectLooper(Looper.Looper_1)
    elif event.data1 == MIDI_CC_LOOPER_2:
        looper.selectLooper(Looper.Looper_2)
    elif event.data1 == MIDI_CC_LOOPER_3:
        looper.selectLooper(Looper.Looper_3)
    elif event.data1 == MIDI_CC_LOOPER_4:
        looper.selectLooper(Looper.Looper_4)
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
    elif event.data1 == MIDI_CC_CLEAR_LOOPER:
        looper.clear()
    elif event.data1 == MIDI_CC_TRACK_1_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.startRecordingTrack(Track.Track_1)
    elif event.data1 == MIDI_CC_TRACK_1_SAMPLING and event.data2 == KP3_PLUS_ABCD_RELEASED:
        looper.stopRecordingTrack(Track.Track_1)
    elif event.data1 == MIDI_CC_TRACK_2_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.startRecordingTrack(Track.Track_2)
    elif event.data1 == MIDI_CC_TRACK_1_SAMPLING and event.data2 == KP3_PLUS_ABCD_RELEASED:
        looper.stopRecordingTrack(Track.Track_2)
    elif event.data1 == MIDI_CC_TRACK_3_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.startRecordingTrack(Track.Track_3)
    elif event.data1 == MIDI_CC_TRACK_1_SAMPLING and event.data2 == KP3_PLUS_ABCD_RELEASED:
        looper.stopRecordingTrack(Track.Track_3)
    elif event.data1 == MIDI_CC_TRACK_4_SAMPLING and event.data2 == KP3_PLUS_ABCD_PRESSED:
        looper.startRecordingTrack(Track.Track_4)
    elif event.data1 == MIDI_CC_TRACK_1_SAMPLING and event.data2 == KP3_PLUS_ABCD_RELEASED:
        looper.stopRecordingTrack(Track.Track_4)
        
    event.handled = True