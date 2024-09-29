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
from common import updateable
from looper_mux.view import View

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
        self.__is_turnado_turned_on = False

        self.__looper_channel = 0
        self.__turnado_dictator_level = 0
        self.__turnado_dry_wet_level = 0
        
        action_first_click = lambda: \
            self.__view.set_clear_looper_btn_state(updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_DONE)
        
        action_first_release = lambda: \
            self.__view.set_clear_looper_btn_state(updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_RELEASED)
        
        action_second_release = lambda: \
            self.__view.set_clear_looper_btn_state(updateable.DoubleClickTimeoutHandler.STATE_INITITAL)
        
        action_timeout = lambda: \
            self.__view.set_clear_looper_btn_state(updateable.DoubleClickTimeoutHandler.STATE_INITITAL)

        self.__clear_looper_handler = updateable.DoubleClickTimeoutHandler(action_first_click,
                                                                           action_first_release,
                                                                           self.clear_second_click_handler,
                                                                           action_second_release,
                                                                           action_timeout, 0.5)

        self.__context_provider.get_updateable_mux().add_updateable(self.__clear_looper_handler)

        if self.__looper_number == constants.Looper_1:
            self.__looper_channel = constants.LOOPER_1_CHANNEL
        elif self.__looper_number == constants.Looper_2:
            self.__looper_channel = constants.LOOPER_2_CHANNEL
        elif self.__looper_number == constants.Looper_3:
            self.__looper_channel = constants.LOOPER_3_CHANNEL
        elif self.__looper_number == constants.Looper_4:
            self.__looper_channel = constants.LOOPER_4_CHANNEL

        self.__sidechain_levels = { constants.Track_1: 0.0,
                                         constants.Track_2: 0.0,
                                         constants.Track_3: 0.0,
                                         constants.Track_4: 0.0 }
        self.__is_gui_active = False

    def clear_second_click_handler(self):
        self.__view.set_clear_looper_btn_state(updateable.DoubleClickTimeoutHandler.STATE_SECOND_CLICK_DONE)
        self.clear_looper()

    def on_init_script(self):
        for track_id in self.__tracks:
            self.__tracks[track_id].on_init_script()

        if self.__looper_number != constants.Looper_1:
            for track_id in self.__tracks:
                self.set_looper_side_chain_level(track_id, constants.DEFAULT_SIDECHAIN_LEVEL)

    def get_resample_mode(self, track_id):
        return self.__tracks[track_id].get_resample_mode()

    def get_looper_number(self):
        return self.__looper_number

    def get_tracks(self):
        return self.__tracks

    def get_track(self, track_number):
        return self.__tracks.get(track_number)

    def set_looper_volume(self, looper_volume, forward_to_device):
        self.__looper_volume = looper_volume

        self.__view.set_looper_volume(self.get_looper_number(), looper_volume, forward_to_device)
        self.__view.set_looper_muted(self.__looper_number, looper_volume == 0)

        for track_id in self.__tracks:
            self.__tracks[track_id].set_looper_volume(self.__looper_volume)

    def get_looper_volume(self):
        return self.__looper_volume

    def set_track_volume(self, track_id, track_volume, forward_to_device):
        self.__tracks.get(track_id).set_track_volume(track_volume, forward_to_device)

    def get_track_volume(self, track_id):
        return self.__tracks.get(track_id).get_track_volume()

    def clear_looper(self):
        self.set_looper_volume(fl_helper.MAX_VOLUME_LEVEL_VALUE, True)
        self.set_turnado_dictator_level(0.0)
        self.set_turnado_dry_wet_level(constants.DEFAULT_TURNADO_DRY_WET_LEVEL)
        for track_id in self.__tracks:
            self.__tracks[track_id].clear(True)
            self.__tracks[track_id].reset_track_params()

        if self.__looper_number != constants.Looper_1:
            for track_id in self.__tracks:
                self.set_looper_side_chain_level(track_id, constants.DEFAULT_SIDECHAIN_LEVEL)

    def clear_track(self, track_id):
            self.__tracks[track_id].clear()

    def start_recording_track(self, track_id, sample_length, resample_mode):
        self.__tracks[track_id].start_recording(sample_length, resample_mode)

    def stop_recording_track(self, track_id):

        if self.__tracks[track_id].get_resample_mode() == ResampleMode.FROM_LOOPER_TO_TRACK:
            # clear all the tracks of the looper, except the one for which recording is over
            for track_id_it in self.__tracks:
                if track_id_it != track_id:
                    self.__tracks[track_id_it].set_track_volume(0.0, True)
                else:
                    self.__tracks[track_id_it].set_track_volume(fl_helper.MAX_VOLUME_LEVEL_VALUE, True)
            self.set_turnado_dictator_level(0.0)
            self.set_turnado_dry_wet_level(constants.DEFAULT_TURNADO_DRY_WET_LEVEL)

        self.__tracks[track_id].stop_recording()

    def set_looper_side_chain_level(self, track_id, sidechain_level):
        self.__sidechain_levels[track_id] = sidechain_level

        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "L1SCT" + str(track_id + 1), constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

        if self.__is_gui_active == True:
            self.__view.set_looper_side_chain_level(track_id, sidechain_level)

    def __update_tracks_stats(self):
        for track_id in self.__tracks:
            self.__tracks[track_id].update_stats()

    def __update_looper_stats(self):
        if True == self.__is_gui_active:
            self.__view.set_turnado_dictator_level(self.__turnado_dictator_level)
            self.__view.set_turnado_dry_wet_level(self.__turnado_dry_wet_level)

            if self.__looper_number != constants.Looper_1:
                for track_id, sidechain_value in self.__sidechain_levels.items():
                    self.__view.set_looper_side_chain_level(track_id, sidechain_value)
            else:
                for track_id, sidechain_value in self.__sidechain_levels.items():
                    self.__view.set_looper_side_chain_level(track_id, constants.DEFAULT_SIDECHAIN_LEVEL)

        self.__view.set_looper_volume(self.get_looper_number(), self.__looper_volume, True)
        self.__view.set_looper_muted(self.__looper_number, self.__looper_volume == 0)

    def is_track_recording_in_progress(self, track_id):
        return self.__tracks[track_id].is_recording_in_progress()

    def stop_all_recordings(self):
        for track_id in self.__tracks:
            if self.__tracks[track_id].is_recording_in_progress():
                self.__tracks[track_id].stop_recording()

    def set_turnado_dictator_level(self, turnado_dictator_level):
        plugins.setParamValue(turnado_dictator_level, constants.TURNADO_DICTATOR_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)

        if self.__is_turnado_turned_on == False and turnado_dictator_level != 0.0:
            parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "L_" + str(self.__looper_number + 1) + "_TUR_A", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(1.0, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
            self.__is_turnado_turned_on = True
        elif self.__is_turnado_turned_on == True and turnado_dictator_level == 0.0:
            parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "L_" + str(self.__looper_number + 1) + "_TUR_A", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(0.0, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
            self.__is_turnado_turned_on = False

        self.__turnado_dictator_level = turnado_dictator_level

        if self.__is_gui_active == True:
            self.__view.set_turnado_dictator_level(turnado_dictator_level)

    def set_turnado_dry_wet_level(self, turnado_dry_wet_level):
        plugins.setParamValue(turnado_dry_wet_level, constants.TURNADO_DRY_WET_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)
        self.__turnado_dry_wet_level = turnado_dry_wet_level

        if self.__is_gui_active == True:
            self.__view.set_turnado_dry_wet_level(turnado_dry_wet_level)

    def randomize_turnado(self):
        print(self.__context_provider.get_device_name() + ': ' + Looper.randomize_turnado.__name__)
        plugins.setParamValue(0.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)

    def switch_to_next_turnado_preset(self):
        plugins.nextPreset(self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, True)
        self.__restore_params()
        if self.__is_gui_active == True:
            self.__view.switch_to_next_turnado_preset()

    def switch_to_prev_turnado_preset(self):
        plugins.prevPreset(self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, True)
        self.__restore_params()
        if self.__is_gui_active == True:
            self.__view.switch_to_prev_turnado_preset()

    def __restore_params(self):
        plugins.setParamValue(self.__turnado_dictator_level, constants.TURNADO_DICTATOR_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(self.__turnado_dry_wet_level, constants.TURNADO_DRY_WET_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)

    def select(self):
        self.__set_gui_active(True)
        self.__update_looper_stats()
        self.__update_tracks_stats()
        self.__view.set_looper_state(self.__looper_number, View.LOOPER_STATE_SELECTED)

    def is_any_track_playing(self):
        result = False
        for track_id in self.__tracks:
            if self.__tracks[track_id].is_playback_in_progress():
                result = True
                break
        return result

    def unselect(self):
        self.__set_gui_active(False)

        value = View.LOOPER_STATE_OFF

        if self.is_any_track_playing():
            value = View.LOOPER_STATE_PLAYING
        else:
            value = View.LOOPER_STATE_OFF

        self.__view.set_looper_state(self.__looper_number, value)

    def set_track_pan(self, track_id, pan, forward_to_device):
        self.__tracks.get(track_id).set_track_pan(pan, forward_to_device)

    def __set_gui_active(self, value):
        self.__is_gui_active = value
        for track_id in self.__tracks:
            self.__tracks[track_id].set_gui_active(value)

    def handle_clear_looper_click(self):
        self.__clear_looper_handler.click()

    def handle_clear_looper_release(self):
        self.__clear_looper_handler.release()