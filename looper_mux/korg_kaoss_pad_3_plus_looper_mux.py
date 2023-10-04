'''
Created on Feb 7, 2022

@author: Dream Machines
'''

import math
import time

import midi
import transport
import mixer
import plugins

from looper_mux.i_context_interface import IContextInterface
from looper_mux.pressed_sampler_button import PressedSamplerButton
from looper_mux.looper import Looper
from looper_mux import constants
from looper_mux.resample_mode import ResampleMode
from looper_mux.sample_length import SampleLength
from looper_mux.track import Track
from looper_mux.view import View
from common import fl_helper

class KorgKaossPad3PlusLooperMux(IContextInterface):

    def __init__(self, context):
        self.__context = context
        self.__view = View()
        self.__shift_pressed = False
        self.__pressed_sampler_buttons = set()
        self.__last_pressed_sampler_button = PressedSamplerButton.NONE
        self.__selected_looper = constants.Looper_1
        self.__loopers = { constants.Looper_1: Looper(constants.Looper_1,
                                                   constants.LOOPER_1_INITIAL_TRACK_CHANNEL,
                                                   self.__view, self),
                           constants.Looper_2: Looper(constants.Looper_2,
                                                   constants.LOOPER_2_INITIAL_TRACK_CHANNEL,
                                                   self.__view, self),
                           constants.Looper_3: Looper(constants.Looper_3,
                                                   constants.LOOPER_3_INITIAL_TRACK_CHANNEL,
                                                   self.__view, self),
                           constants.Looper_4: Looper(constants.Looper_4,
                                                   constants.LOOPER_4_INITIAL_TRACK_CHANNEL,
                                                   self.__view, self) }
        self.__initialized = False
        self.__resample_mode = ResampleMode.NONE
        self.__buttons_last_press_time = {}

    def onInitScript(self):

        if False == self.__initialized:
            print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.onInitScript.__name__)

            try:
                for looper_id in self.__loopers:
                    self.__loopers[looper_id].onInitScript()
                mixer.setRouteTo(constants.MIC_ROUTE_CHANNEL, constants.MASTER_FX_1_CHANNEL, 1)
                mixer.setRouteTo(constants.SYNTH_ROUTE_CHANNEL, constants.MASTER_FX_1_CHANNEL, 1)
                self.__initialized = True
                self.clear()
                self.__view.setTempo(mixer.getCurrentTempo() / 1000.0)
                self.setSampleLength(SampleLength.LENGTH_1)
                self.setResampleMode(ResampleMode.NONE)
            except Exception as e:
                print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.onInitScript.__name__ + ": failed to initialize the script.")
                print(e)

    # ContextInterface Implementation
    def getSampleLength(self) -> int:
        return self.__selectedSampleLength

    def getDeviceName(self) -> str:
        return self.__context.device_name
    # ContextInterface implementation end

    def isPlaying(self):
        return transport.isPlaying()

    def playStop(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.playStop.__name__)

        self.clear()

        if transport.isPlaying():
            transport.stop()
            self.__view.setPlay(False)
        else:
            transport.start()
            self.__view.setPlay(True)

    def setTempo(self, tempo):
        targetTempo = tempo - tempo % 50
        currentTempo = mixer.getCurrentTempo() / 100.0
        if math.fabs( int(currentTempo/10) - int(targetTempo/10) ) >= constants.TEMPO_JOG_ROTATION_THRESHOLD:
            jogRotation = int( targetTempo - currentTempo )
            print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.setTempo.__name__ + ": target tempo: " + str(targetTempo) + ", current tempo: " + str(currentTempo) + ", jog rotation: " + str(jogRotation))
            transport.globalTransport( 105, jogRotation )
            self.__view.setTempo(targetTempo / 10.0)

    def setShiftPressedState(self, shift_pressed):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.setShiftPressedState.__name__ + ": shift pressed - " + str(shift_pressed))

        self.__view.setShiftPressedState(shift_pressed)

        self.__shift_pressed = shift_pressed

        if(True == shift_pressed):
            self.actionOnDoubleClick(constants.MIDI_CC_SHIFT, self.__loopers[self.__selected_looper].randomizeTurnado)

    def switchToNextTurnadoPreset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.switchToNextTurnadoPreset.__name__)
        self.__loopers[self.__selected_looper].switchToNextTurnadoPreset()

        self.__view.switchToNextTurnadoPreset()

    def switchToPrevTurnadoPreset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.switchToPrevTurnadoPreset.__name__)
        self.__loopers[self.__selected_looper].switchToPrevTurnadoPreset()

    def getShiftPressedState(self):
        return self.__shift_pressed

    def addPressedSamplerButton(self, pressed_sampler_button):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.addPressedSamplerButton.__name__ + ": added sampler button - " + str(pressed_sampler_button))
        self.__pressed_sampler_buttons.add(pressed_sampler_button)
        self.__last_pressed_sampler_button = pressed_sampler_button

    def removePressedSamplerButton(self, released_sampler_button):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.addPressedSamplerButton.__name__ + ": removed sampler button - " + str(released_sampler_button))
        self.__pressed_sampler_buttons.remove(released_sampler_button)

        if self.__last_pressed_sampler_button == released_sampler_button:
            self.__last_pressed_sampler_button = PressedSamplerButton.NONE

    def selectLooper(self, selected_looper):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.selectLooper.__name__ + ": selected looper - " + str(selected_looper))

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
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.setSampleLength.__name__ + ": selected sample length - " + str(sample_length))
        self.__selectedSampleLength = sample_length
        self.__view.updateSampleLength(sample_length)

        #printAllPluginParameters(17, 9)

    def clear(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.clear.__name__)
        for looper_id in self.__loopers:
            self.__loopers[looper_id].clearLooper()
        self.selectLooper(constants.Looper_1)
        self.setLooperVolume(fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.setDropIntencity(0.0)
        self.setSampleLength(SampleLength.LENGTH_1)
        self.setResampleMode(ResampleMode.NONE)
        self.__view.clear()

    def clearCurrentLooper(self):
        self.__loopers[self.__selected_looper].clearLooper()

    def clearTrack(self, track_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.clearTrack.__name__ + ": track - " + str(track_id))
        self.__loopers[self.__selected_looper].clearTrack(track_id)

    def setMasterRoutingLevel(self, routing_level):
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "MasterFX1M", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(routing_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "MasterFX1S", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(routing_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def changeRecordingState(self, selected_track_id):
            print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.changeRecordingState.__name__ + ": track - " + str(selected_track_id))
            self.__changeRecordingStateTo(selected_track_id, not self.__loopers[self.__selected_looper].isTrackRecordingInProgress(selected_track_id))

    def actionOnDoubleClick(self, pressed_button, action):
        pressed_time = time.time()

        if not pressed_button in self.__buttons_last_press_time.keys():
            self.__buttons_last_press_time[pressed_button] = 0

        if (pressed_time - self.__buttons_last_press_time[pressed_button]) < 0.5:
            # double click
            self.__buttons_last_press_time.clear()
            self.__buttons_last_press_time[pressed_button] = 0
            action()
        else:
            self.__buttons_last_press_time.clear()
            self.__buttons_last_press_time[pressed_button] = pressed_time

    def setInputSideChainLevel(self, track_id, sidechain_level):
        self.__loopers[constants.Looper_1].setInputSideChainLevel(track_id, sidechain_level)

    def setLooperSideChainLevel(self, track_id, sidechain_level):
        if self.__selected_looper != constants.Looper_1:
            self.__loopers[self.__selected_looper].setLooperSideChainLevel(track_id, sidechain_level)

    def setDropIntencity(self, drop_intencity):
        plugins.setParamValue(drop_intencity, constants.ENDLESS_SMILE_PLUGIN_INTENSITY_PARAM_INDEX, constants.LOOPER_ALL_CHANNEL, constants.LOOPER_ALL_ENDLESS_SMILE_SLOT_INDEX, midi.PIM_None, True)
        self.__view.setDropIntencity(drop_intencity)

    def setResampleMode(self, resample_mode):

        if resample_mode == self.getResampleMode():
            resample_mode = ResampleMode.NONE

        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.setResampleMode.__name__ + ": to - " + str(resample_mode))
        self.__resample_mode = resample_mode

        self.__view.setResampleMode(resample_mode)

    def getResampleMode(self):
        return self.__resample_mode

    def setTurnadoDictatorLevel(self, turnado_dictator_level):
        self.__loopers[self.__selected_looper].setTurnadoDictatorLevel(turnado_dictator_level)

    def setTurnadoDryWetLevel(self, turnado_dry_wet_level):
        self.__loopers[self.__selected_looper].setTurnadoDryWetLevel(turnado_dry_wet_level)

    def drop(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.drop.__name__)
        self.setDropIntencity(0)
        self.__loopers[constants.Looper_1].setTrackVolume(constants.Track_1, fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.__loopers[constants.Looper_1].setTrackVolume(constants.Track_2, fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.__loopers[constants.Looper_1].setTrackVolume(constants.Track_3, fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.__loopers[constants.Looper_1].setTrackVolume(constants.Track_4, fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.__loopers[constants.Looper_1].setLooperVolume(fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.__loopers[constants.Looper_1].setTurnadoDictatorLevel(0.0)
        self.__loopers[constants.Looper_1].setTurnadoDryWetLevel(constants.DEFAULT_TURNADO_DRY_WET_LEVEL)

    def turnTrackOnOff(self, track_id):
        if 0 != self.__loopers[self.__selected_looper].getTrackVolume(track_id):
            self.__loopers[self.__selected_looper].setTrackVolume(track_id, 0.0)
        else:
            self.__loopers[self.__selected_looper].setTrackVolume(track_id, fl_helper.MAX_VOLUME_LEVEL_VALUE)

    def turnLooperOnOff(self, looper_id):

        update_view = looper_id == self.__selected_looper

        if 0 != self.__loopers[looper_id].getLooperVolume():
            self.__loopers[looper_id].setLooperVolume(0.0, not update_view)
        else:
            self.__loopers[looper_id].setLooperVolume(fl_helper.MAX_VOLUME_LEVEL_VALUE, not update_view)

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
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.__startRecordingTrack.__name__ + ": track - " + str(selected_track_id) + ", resample mode - " + str(self.getResampleMode()))
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
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.__stopRecordingTrack.__name__ + ": track - " + str(track_id))

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

    def onMidiMsgProcessing(self, event):

        if event.data1 == constants.MIDI_CC_TRACK_1_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.addPressedSamplerButton(PressedSamplerButton.A_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_1_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_RELEASED:
            self.removePressedSamplerButton(PressedSamplerButton.A_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_2_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.addPressedSamplerButton(PressedSamplerButton.B_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_2_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_RELEASED:
            self.removePressedSamplerButton(PressedSamplerButton.B_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_3_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.addPressedSamplerButton(PressedSamplerButton.C_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_3_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_RELEASED:
            self.removePressedSamplerButton(PressedSamplerButton.C_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_4_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.addPressedSamplerButton(PressedSamplerButton.D_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_4_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_RELEASED:
            self.removePressedSamplerButton(PressedSamplerButton.D_PRESSED)


        if event.data1 == constants.MIDI_CC_LOOPER_VOLUME and self.getShiftPressedState():
            self.setDropIntencity( (fl_helper.MIDI_MAX_VALUE - event.data2) / fl_helper.MIDI_MAX_VALUE )
        elif event.data1 == constants.MIDI_CC_RESAMPLE_MODE_FROM_LOOPER_TO_TRACK and self.getShiftPressedState():
            self.setResampleMode(ResampleMode.FROM_LOOPER_TO_TRACK)

            action = lambda self = self: ( self.setResampleMode(ResampleMode.NONE), \
                                           self.switchToPrevTurnadoPreset())
            self.actionOnDoubleClick(constants.MIDI_CC_RESAMPLE_MODE_FROM_LOOPER_TO_TRACK + constants.SHIFT_BUTTON_ON_DOUBLE_CLICK_SHIFT, action)

        elif event.data1 == constants.MIDI_CC_RESAMPLE_MODE_FROM_ALL_LOOPERS_TO_TRACK and self.getShiftPressedState():
            self.setResampleMode(ResampleMode.FROM_ALL_LOOPERS_TO_TRACK)

            action = lambda self = self: ( self.setResampleMode(ResampleMode.NONE), \
                                           self.switchToNextTurnadoPreset())
            self.actionOnDoubleClick(constants.MIDI_CC_RESAMPLE_MODE_FROM_ALL_LOOPERS_TO_TRACK + constants.SHIFT_BUTTON_ON_DOUBLE_CLICK_SHIFT, action)
        elif event.data1 == constants.MIDI_CC_LOOPER_1 and self.getShiftPressedState():
            self.selectLooper(constants.Looper_1)
            self.actionOnDoubleClick(constants.SHIFT_BUTTON_ON_DOUBLE_CLICK_SHIFT + constants.MIDI_CC_SAMPLE_LENGTH_1, self.drop)
        elif event.data1 == constants.MIDI_CC_LOOPER_2 and self.getShiftPressedState():
            self.selectLooper(constants.Looper_2)
        elif event.data1 == constants.MIDI_CC_LOOPER_3 and self.getShiftPressedState():
            self.selectLooper(constants.Looper_3)
        elif event.data1 == constants.MIDI_CC_LOOPER_4 and self.getShiftPressedState():
            self.selectLooper(constants.Looper_4)
        elif event.data1 == constants.MIDI_CC_CLEAR_LOOPER and self.getShiftPressedState():
            action = lambda self = self: ( self.clearCurrentLooper() )
            self.actionOnDoubleClick(constants.MIDI_CC_CLEAR_LOOPER, action)
        elif event.data1 == constants.MIDI_CC_PLAY_STOP and self.getShiftPressedState():
            action = lambda self = self: ( self.playStop() )
            self.actionOnDoubleClick(constants.MIDI_CC_PLAY_STOP, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_1:
            self.setSampleLength(SampleLength.LENGTH_1)
            action = lambda self = self: self.turnLooperOnOff(constants.Looper_1)
            self.actionOnDoubleClick(constants.MIDI_CC_SAMPLE_LENGTH_1, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_2:
            self.setSampleLength(SampleLength.LENGTH_2)
            action = lambda self = self: self.turnLooperOnOff(constants.Looper_2)
            self.actionOnDoubleClick(constants.MIDI_CC_SAMPLE_LENGTH_2, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_4:
            self.setSampleLength(SampleLength.LENGTH_4)
            action = lambda self = self: self.turnLooperOnOff(constants.Looper_3)
            self.actionOnDoubleClick(constants.MIDI_CC_SAMPLE_LENGTH_4, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_8:
            self.setSampleLength(SampleLength.LENGTH_8)
            action = lambda self = self: self.turnLooperOnOff(constants.Looper_4)
            self.actionOnDoubleClick(constants.MIDI_CC_SAMPLE_LENGTH_8, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_16:
            self.setSampleLength(SampleLength.LENGTH_16)
            action = lambda self = self: self.turnTrackOnOff(constants.Track_1)
            self.actionOnDoubleClick(constants.MIDI_CC_SAMPLE_LENGTH_16, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_32:
            self.setSampleLength(SampleLength.LENGTH_32)
            action = lambda self = self: self.turnTrackOnOff(constants.Track_2)
            self.actionOnDoubleClick(constants.MIDI_CC_SAMPLE_LENGTH_32, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_64:
            self.setSampleLength(SampleLength.LENGTH_64)
            action = lambda self = self: self.turnTrackOnOff(constants.Track_3)
            self.actionOnDoubleClick(constants.MIDI_CC_SAMPLE_LENGTH_64, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_128:
            self.setSampleLength(SampleLength.LENGTH_128)
            action = lambda self = self: self.turnTrackOnOff(constants.Track_4)
            self.actionOnDoubleClick(constants.MIDI_CC_SAMPLE_LENGTH_128, action)
        elif event.data1 == constants.MIDI_CC_TRACK_1_CLEAR and event.data2 == constants.KP3_PLUS_ABCD_PRESSED and self.getShiftPressedState():
            self.clearTrack(constants.Track_1)
        elif event.data1 == constants.MIDI_CC_TRACK_2_CLEAR and event.data2 == constants.KP3_PLUS_ABCD_PRESSED and self.getShiftPressedState():
            self.clearTrack(constants.Track_2)
        elif event.data1 == constants.MIDI_CC_TRACK_3_CLEAR and event.data2 == constants.KP3_PLUS_ABCD_PRESSED and self.getShiftPressedState():
            self.clearTrack(constants.Track_3)
        elif event.data1 == constants.MIDI_CC_TRACK_4_CLEAR and event.data2 == constants.KP3_PLUS_ABCD_PRESSED and self.getShiftPressedState():
            self.clearTrack(constants.Track_4)
        elif event.data1 == constants.MIDI_CC_SHIFT:
            self.setShiftPressedState(event.data2 == fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TURNADO_DRY_WET and self.getShiftPressedState():
            self.setTurnadoDryWetLevel(event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_LOOPER_VOLUME:
            self.setLooperVolume((event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_1:
            self.setTrackVolume(0, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_2:
            self.setTrackVolume(1, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_3:
            self.setTrackVolume(2, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_4:
            self.setTrackVolume(3, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_1_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.changeRecordingState(constants.Track_1)
        elif event.data1 == constants.MIDI_CC_TRACK_2_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.changeRecordingState(constants.Track_2)
        elif event.data1 == constants.MIDI_CC_TRACK_3_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.changeRecordingState(constants.Track_3)
        elif event.data1 == constants.MIDI_CC_TRACK_4_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.changeRecordingState(constants.Track_4)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_1 and self.getShiftPressedState():
            self.setLooperSideChainLevel(constants.Track_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_2 and self.getShiftPressedState():
            self.setLooperSideChainLevel(constants.Track_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_3 and self.getShiftPressedState():
            self.setLooperSideChainLevel(constants.Track_3, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_4 and self.getShiftPressedState():
            self.setLooperSideChainLevel(constants.Track_4, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_1:
            self.setInputSideChainLevel(constants.Track_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_2:
            self.setInputSideChainLevel(constants.Track_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_3:
            self.setInputSideChainLevel(constants.Track_3, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_4:
            self.setInputSideChainLevel(constants.Track_4, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TURNADO_DICTATOR and self.isPlaying():
            self.setTurnadoDictatorLevel(event.data2 / fl_helper.MIDI_MAX_VALUE)

    def OnMidiMsg(self, event):

        self.onInitScript()

        #fl_helper.printAllPluginParameters(LOOPER_1_CHANNEL, LOOPER_TURNADO_SLOT_INDEX)

        event.handled = False

        if not self.isPlaying():
            if event.data1 == constants.MIDI_CC_TEMPO and not self.isPlaying():
                self.setTempo(800 + int((event.data2 / fl_helper.MIDI_MAX_VALUE) * 1000.0)) # from 80 to 180
            else:
                if ( not ( event.data1 == constants.MIDI_CC_SHIFT and event.data2 == 0 ) \
                and ( not ( event.data1 == constants.MIDI_CC_PLAY_STOP and self.getShiftPressedState() ) ) ):
                    self.playStop()

                self.onMidiMsgProcessing(event)
        else:
            self.onMidiMsgProcessing(event)

        event.handled = True