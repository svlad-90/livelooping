'''
Created on Feb 7, 2022

@author: Dream Machines
'''

import midi
import plugins
import mixer

from looper_mux.track import Track
from looper_mux import constants
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
        self.__looper_fx1_channel = 0
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
            self.__looper_fx1_channel = constants.LOOPER_1_FX_1_CHANNEL
        elif self.__looper_number == constants.Looper_2:
            self.__looper_channel = constants.LOOPER_2_CHANNEL
            self.__looper_fx1_channel = constants.LOOPER_2_FX_1_CHANNEL
        elif self.__looper_number == constants.Looper_3:
            self.__looper_channel = constants.LOOPER_3_CHANNEL
            self.__looper_fx1_channel = constants.LOOPER_3_FX_1_CHANNEL
        elif self.__looper_number == constants.Looper_4:
            self.__looper_channel = constants.LOOPER_4_CHANNEL
            self.__looper_fx1_channel = constants.LOOPER_4_FX_1_CHANNEL

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

        for track_id in self.__tracks:
            self.set_looper_side_chain_level(track_id, constants.DEFAULT_SIDECHAIN_LEVEL, True)

    def get_looper_number(self):
        return self.__looper_number

    def get_tracks(self):
        return self.__tracks

    def get_track(self, track_number):
        return self.__tracks.get(track_number)

    def set_looper_volume(self, looper_volume, forward_to_device):
        self.__looper_volume = looper_volume

        self.__view.set_looper_muted(self.__looper_number, looper_volume == 0)

        for track_id in self.__tracks:
            self.__tracks[track_id].set_looper_volume(self.__looper_volume)

    def get_looper_volume(self):
        return self.__looper_volume

    def set_track_volume(self, track_id, track_volume, forward_to_device):
        self.__tracks.get(track_id).set_track_volume(track_volume, forward_to_device)

    def set_track_hp_filter_level(self, track_id, hp_filter_level, forward_to_device):
        self.__tracks.get(track_id).set_track_hp_filter_level(hp_filter_level, forward_to_device)

    def set_track_lp_filter_level(self, track_id, lp_filter_level, forward_to_device):
        self.__tracks.get(track_id).set_track_lp_filter_level(lp_filter_level, forward_to_device)

    def get_track_volume(self, track_id):
        return self.__tracks.get(track_id).get_track_volume()

    def clear_looper(self):
        self.set_looper_volume(fl_helper.MAX_VOLUME_LEVEL_VALUE, True)
        for track_id in self.__tracks:
            self.__tracks[track_id].clear(True)
            self.__tracks[track_id].reset_track_params()

        for track_id in self.__tracks:
            self.set_looper_side_chain_level(track_id, constants.DEFAULT_SIDECHAIN_LEVEL, True)

    def clear_track(self, track_id):
            self.__tracks[track_id].clear()

    def start_recording_track(self, track_id, sample_length):
        if self.__tracks[track_id].get_track_selection_status():
            self.__tracks[track_id].set_track_selection_status(False)

        if self.__is_any_track_selected():
            self.__set_track_routing(constants.FX_UNIT_OUT_CHANNEL, self.__looper_fx1_channel, 0.0)
            self.__set_track_routing(constants.FX_UNIT_OUT_CHANNEL, constants.RECORDING_BUS_FEEDBACK_LOOP_CHANNEL, fl_helper.MAX_VOLUME_LEVEL_VALUE)

        self.__tracks[track_id].start_recording(sample_length)

    def stop_recording_track(self, track_id):            
        self.__tracks[track_id].stop_recording()

        if self.__is_any_track_selected() and not self.__is_any_track_recording():
            for track_id in self.__tracks:
                if self.__tracks[track_id].get_track_selection_status():
                    self.__tracks[track_id].set_track_volume(0.0, True)
            self.__set_track_routing(constants.FX_UNIT_OUT_CHANNEL, self.__looper_fx1_channel, fl_helper.MAX_VOLUME_LEVEL_VALUE)
            self.__set_track_routing(constants.FX_UNIT_OUT_CHANNEL, constants.RECORDING_BUS_FEEDBACK_LOOP_CHANNEL, 0.0)
            self.__reset_all_tracks_selection()

    def set_looper_side_chain_level(self, track_id, sidechain_level, forward_to_device):
        if self.__looper_number != constants.Looper_1:
            self.__sidechain_levels[track_id] = sidechain_level

            parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "L" + str(self.__looper_number + 1) + "L1SCT" + str(track_id + 1), constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

            if self.__is_gui_active == True:
                self.__view.set_looper_side_chain_level(track_id, sidechain_level, forward_to_device)
        else:
            if self.__is_gui_active == True:
                self.__view.set_looper_side_chain_level(track_id, 0.0, True)

    def __update_tracks_stats(self):
        for track_id in self.__tracks:
            self.__tracks[track_id].update_stats()

    def __update_looper_stats(self):
        if True == self.__is_gui_active:
            for track_id, sidechain_value in self.__sidechain_levels.items():
                self.__view.set_looper_side_chain_level(track_id, sidechain_value, True)

        self.__view.set_looper_muted(self.__looper_number, self.__looper_volume == 0)

    def is_track_recording_in_progress(self, track_id):
        return self.__tracks[track_id].is_recording_in_progress()

    def stop_all_recordings(self):
        for track_id in self.__tracks:
            if self.__tracks[track_id].is_recording_in_progress():
                self.__tracks[track_id].stop_recording()

    def randomize_turnado(self):
        print(self.__context_provider.get_device_name() + ': ' + Looper.randomize_turnado.__name__)
        plugins.setParamValue(0.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(1.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__looper_channel, constants.LOOPER_TURNADO_SLOT_INDEX, midi.PIM_None, True)

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

        self.__reset_all_tracks_selection()

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

    def set_track_selection_status(self, track_id, selection_status):

        if selection_status and self.__tracks[track_id].is_recording_in_progress():
            return

        self.__tracks.get(track_id).set_track_selection_status(selection_status)
        if selection_status:
            self.__set_track_routing(constants.FX_UNIT_OUT_CHANNEL, self.__looper_fx1_channel, fl_helper.MAX_VOLUME_LEVEL_VALUE)
        else:
            if not self.__is_any_track_selected():
                self.__set_track_routing(constants.FX_UNIT_OUT_CHANNEL, self.__looper_fx1_channel, 0.0)

    def get_track_selection_status(self, track_id):
        return self.__tracks.get(track_id).get_track_selection_status()

    def __reset_all_tracks_selection(self):
        for track_id in self.__tracks:
            self.set_track_selection_status(track_id, False)

    def __is_any_track_selected(self):
        any_track_selected = False
        for track_id in self.__tracks:
            if self.__tracks[track_id].get_track_selection_status():
                any_track_selected = True
                break
        return any_track_selected

    def __is_any_track_recording(self):
        any_track_recording = False
        for track_id in self.__tracks:
            if self.__tracks[track_id].is_recording_in_progress():
                any_track_recording = True
                break
        return any_track_recording

    def __set_track_routing(self, source_channel, target_channel, routing_level):
        mixer.setRouteToLevel(source_channel, target_channel, routing_level)