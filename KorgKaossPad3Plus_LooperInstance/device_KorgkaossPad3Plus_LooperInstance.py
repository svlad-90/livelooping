# name=KorgKaossPad3Plus_LooperInstance
import math
device_name="KorgKaossPad3Plus_LooperInstance"
print(device_name + ': started')

# FL imports
import transport
import mixer

# define variables
MIDI_CC_SHIFT               = 95
MIDI_CC_PLAY_STOP           = 56
MIDI_CC_TEMPO               = 94
MIDI_CC_LENGTH              = 56
MIDI_CC_LOOPER_1            = 49
MIDI_CC_LOOPER_2            = 50
MIDI_CC_LOOPER_3            = 51
MIDI_CC_LOOPER_4            = 52
MIDI_CC_LOOPER_VOLUME       = 93
MIDI_CC_SAMPLE              = 123
MIDI_CC_TRACK_1_TURN_OFF_ON = 123
MIDI_CC_TRACK_2_TURN_OFF_ON = 123
MIDI_CC_TRACK_3_TURN_OFF_ON = 123
MIDI_CC_TRACK_4_TURN_OFF_ON = 123

LOOPER_1_TRACK_1_MIXER_TRACK = 17
LOOPER_1_TRACK_2_MIXER_TRACK = 18
LOOPER_1_TRACK_3_MIXER_TRACK = 19
LOOPER_1_TRACK_4_MIXER_TRACK = 20

LOOPER_2_TRACK_1_MIXER_TRACK = 25
LOOPER_2_TRACK_2_MIXER_TRACK = 26
LOOPER_2_TRACK_3_MIXER_TRACK = 27
LOOPER_2_TRACK_4_MIXER_TRACK = 28

LOOPER_3_TRACK_1_MIXER_TRACK = 33
LOOPER_3_TRACK_2_MIXER_TRACK = 34
LOOPER_3_TRACK_3_MIXER_TRACK = 35
LOOPER_3_TRACK_4_MIXER_TRACK = 36

LOOPER_4_TRACK_1_MIXER_TRACK = 41
LOOPER_4_TRACK_2_MIXER_TRACK = 42
LOOPER_4_TRACK_3_MIXER_TRACK = 43
LOOPER_4_TRACK_4_MIXER_TRACK = 44

LOOPER_VOLUME_PLUGIN_MIXER_SLOT_INDEX = 10
LOOPER_VOLUME_PLUGIN_PARAM_NAME = ""

TEMPO_JOG_ROTATION_THRESHOLD = 5

MIDI_MAX_VALUE = 127

class Looper():
    Looper_1    = 0
    Looper_2    = 1
    Looper_3    = 2
    Looper_4    = 3

class KorgKaossPad3Plus_LooperInstance:
 
    def __init__(self):
        self.__shiftPressed = False
        self.__selectedLooper = Looper.Looper_1
    
    def playStop(self):
        print(device_name + ': ' + KorgKaossPad3Plus_LooperInstance.playStop.__name__);
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
        
        if self.__selectedLooper == Looper.Looper_1:
            mixer.setTrackVolume(LOOPER_1_TRACK_1_MIXER_TRACK, looperVolume)
            mixer.setTrackVolume(LOOPER_1_TRACK_2_MIXER_TRACK, looperVolume)
            mixer.setTrackVolume(LOOPER_1_TRACK_3_MIXER_TRACK, looperVolume)
            mixer.setTrackVolume(LOOPER_1_TRACK_4_MIXER_TRACK, looperVolume)
        elif self.__selectedLooper == Looper.Looper_2:
            mixer.setTrackVolume(LOOPER_2_TRACK_1_MIXER_TRACK, looperVolume)
            mixer.setTrackVolume(LOOPER_2_TRACK_2_MIXER_TRACK, looperVolume)
            mixer.setTrackVolume(LOOPER_2_TRACK_3_MIXER_TRACK, looperVolume)
            mixer.setTrackVolume(LOOPER_2_TRACK_4_MIXER_TRACK, looperVolume)
        elif self.__selectedLooper == Looper.Looper_3:
            mixer.setTrackVolume(LOOPER_3_TRACK_1_MIXER_TRACK, looperVolume)
            mixer.setTrackVolume(LOOPER_3_TRACK_2_MIXER_TRACK, looperVolume)
            mixer.setTrackVolume(LOOPER_3_TRACK_3_MIXER_TRACK, looperVolume)
            mixer.setTrackVolume(LOOPER_3_TRACK_4_MIXER_TRACK, looperVolume)
        elif self.__selectedLooper == Looper.Looper_4:
            mixer.setTrackVolume(LOOPER_4_TRACK_1_MIXER_TRACK, looperVolume)
            mixer.setTrackVolume(LOOPER_4_TRACK_2_MIXER_TRACK, looperVolume)
            mixer.setTrackVolume(LOOPER_4_TRACK_3_MIXER_TRACK, looperVolume)
            mixer.setTrackVolume(LOOPER_4_TRACK_4_MIXER_TRACK, looperVolume)
    
looper = KorgKaossPad3Plus_LooperInstance()
    
def OnMidiMsg(event):
    
    event.handled = False
    if event.data1 == MIDI_CC_PLAY_STOP:
        looper.playStop()
        event.handled = True
    elif event.data1 == MIDI_CC_SHIFT:
        looper.setShiftPressedState(event.data2 == MIDI_MAX_VALUE)
        event.handled = True
    elif event.data1 == MIDI_CC_TEMPO and looper.getShiftPressedState():
        looper.setTempo(800 + int((event.data2 / MIDI_MAX_VALUE) * 1000.0)) # from 80 to 180
        event.handled = True
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