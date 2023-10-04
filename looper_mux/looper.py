'''
Created on Feb 7, 2022

@author: Dream Machines
'''

import midi
import plugins

from looper_mux.track import Track
from looper_mux import constants
from looper_mux.resample_mode import ResampleMode
from common import fl_helper


class Looper():

    def __init__(self, looper_number, initial_mixer_track, view, context_provider):
        self.__view = view
        self.__context_provider = context_provider
        self.__looper_number = looper_number
        self.__INITIAL_TRACK_CHANNEL__ = initial_mixer_track
        self.__tracks = { constants.Track_1: Track(looper_number, constants.Track_1,
                                               initial_mixer_track + constants.Track_1,
                                                   self.__view, context_provider),
                          constants.Track_2: Track(looper_number, constants.Track_2,
                                               initial_mixer_track + constants.Track_2,
                                                   self.__view, context_provider),
                          constants.Track_3: Track(looper_number, constants.Track_3,
                                               initial_mixer_track + constants.Track_3,
                                                   self.__view, context_provider),
                          constants.Track_4: Track(looper_number, constants.Track_4,
                                               initial_mixer_track + constants.Track_4,
                                                   self.__view, context_provider) }
        self.__looper_volume = fl_helper.MAX_VOLUME_LEVEL_VALUE
        self.__isTurnadoTurnedOn = False

        self.__looper_channel = 0
        self.__turnado_dictator_level = 0
        self.__turnado_dry_wet_level = 0

        if self.__looper_number == constants.Looper_1:
            self.__looper_channel = constants.LOOPER_1_CHANNEL
        elif self.__looper_number == constants.Looper_2:
            self.__looper_channel = constants.LOOPER_2_CHANNEL
        elif self.__looper_number == constants.Looper_3:
            self.__looper_channel = constants.LOOPER_3_CHANNEL
        elif self.__looper_number == constants.Looper_4:
            self.__looper_channel = constants.LOOPER_4_CHANNEL

        self.__sidechainLevels = { constants.Track_1: 0.0,
                                         constants.Track_2: 0.0,
                                         constants.Track_3: 0.0,
                                         constants.Track_4: 0.0 }

    def onInitScript(self):
        for track_id in self.__tracks:
            self.__tracks[track_id].onInitScript()

        if self.__looper_number != constants.Looper_1:
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

    def setLooperVolume(self, looper_volume, ignore_view=False):
        self.__looper_volume = looper_volume

        if ignore_view == False:
            self.__view.setLooperVolume(looper_volume)

        self.__view.setLooperActivationStatus(self.__looper_number, looper_volume)

        for track_id in self.__tracks:
            self.__tracks[track_id].setLooperVolume(self.__looper_volume)

    def getLooperVolume(self):
        return self.__looper_volume

    def setTrackVolume(self, track_id, track_volume):
        self.__tracks.get(track_id).setTrackVolume(track_volume)

    def getTrackVolume(self, track_id):
        return self.__tracks.get(track_id).getTrackVolume()

    def clearLooper(self):
        self.setLooperVolume(fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.setTurnadoDictatorLevel(0.0)
        self.setTurnadoDryWetLevel(constants.DEFAULT_TURNADO_DRY_WET_LEVEL)
        for track_id in self.__tracks:
            self.__tracks[track_id].clear(True)
            self.__tracks[track_id].resetTrackParams()
            self.__tracks[track_id].setInputSideChainLevel(0.0)

        if self.__looper_number != constants.Looper_1:
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
            self.setTurnadoDryWetLevel(constants.DEFAULT_TURNADO_DRY_WET_LEVEL)

        self.__tracks[track_id].stopRecording()

    def setInputSideChainLevel(self, track_id, sidechain_level):
        self.__tracks[track_id].setInputSideChainLevel(sidechain_level)

    def setLooperSideChainLevel(self, track_id, sidechain_level):
        self.__sidechainLevels[track_id] = sidechain_level

        parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "L1SCT" + str(track_id + 1), constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

        self.__view.setLooperSideChainLevel(track_id, sidechain_level)

    def updateTracksStats(self):
        for track_id in self.__tracks:
            self.__tracks[track_id].updateStats()

    def updateLooperStats(self):
        self.__view.setLooperVolume(self.__looper_volume)
        self.__view.setTurnadoDictatorLevel(self.__turnado_dictator_level)
        self.__view.setTurnadoDryWetLevel(self.__turnado_dry_wet_level)

        if self.__looper_number != constants.Looper_1:
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
        plugins.setParamValue(turnado_dictator_level, constants.TURNADO_DICTATOR_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)

        if self.__isTurnadoTurnedOn == False and turnado_dictator_level != 0.0:
            parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "L_" + str(self.__looper_number + 1) + "_TUR_A", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(1.0, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
            self.__isTurnadoTurnedOn = True
        elif self.__isTurnadoTurnedOn == True and turnado_dictator_level == 0.0:
            parameter_id = fl_helper.findParameterByName(constants.MASTER_CHANNEL, "L_" + str(self.__looper_number + 1) + "_TUR_A", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(0.0, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
            self.__isTurnadoTurnedOn = False

        self.__turnado_dictator_level = turnado_dictator_level
        self.__view.setTurnadoDictatorLevel(turnado_dictator_level)

    def setTurnadoDryWetLevel(self, turnado_dry_wet_level):
        plugins.setParamValue(turnado_dry_wet_level, constants.TURNADO_DRY_WET_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)
        self.__turnado_dry_wet_level = turnado_dry_wet_level
        self.__view.setTurnadoDryWetLevel(turnado_dry_wet_level)

    def randomizeTurnado(self):
        print(self.__context_provider.getDeviceName() + ': ' + Looper.randomizeTurnado.__name__)
        plugins.setParamValue(0.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)

    def switchToNextTurnadoPreset(self):
        plugins.nextPreset(self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, True)
        self.__restoreParams()
        self.__view.switchToNextTurnadoPreset()

    def switchToPrevTurnadoPreset(self):
        plugins.prevPreset(self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, True)
        self.__restoreParams()
        self.__view.switchToPrevTurnadoPreset()

    def __restoreParams(self):
        plugins.setParamValue(self.__turnado_dictator_level, constants.TURNADO_DICTATOR_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(self.__turnado_dry_wet_level, constants.TURNADO_DRY_WET_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)
