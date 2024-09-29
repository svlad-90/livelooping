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
from looper_mux.view import View
from common import fl_helper
from common import updateable
from looper_mux import drop

class KorgKaossPad3PlusLooperMux(IContextInterface):

    def __init__(self, context):
        self.__context = context
        self.__view = View()
        self.__shift_pressed = False
        self.__extra_1_state = False
        self.__selected_looper = constants.Looper_1
        self.__updateable_mux = updateable.UpdateableMux()
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
        self.__prolonged_record_length_mode = False
        self.__selected_sample_length = SampleLength.LENGTH_1

        clear_handler_action_first_click = lambda: \
            self.__view.set_clear_btn_state(updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_DONE)
        
        clear_handler_action_first_release = lambda: \
            self.__view.set_clear_btn_state(updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_RELEASED)
        
        clear_handler_action_second_release = lambda: \
            self.__view.set_clear_btn_state(updateable.DoubleClickTimeoutHandler.STATE_INITITAL)
        
        clear_handler_action_timeout = lambda: \
            self.__view.set_clear_btn_state(updateable.DoubleClickTimeoutHandler.STATE_INITITAL)

        self.__clear_handler = updateable.DoubleClickTimeoutHandler(clear_handler_action_first_click,
                                                                    clear_handler_action_first_release,
                                                                    self.clear_handler_action_second_click,
                                                                    clear_handler_action_second_release,
                                                                    clear_handler_action_timeout, 0.5)

        self.__updateable_mux.add_updateable(self.__clear_handler)

        sync_daw_transport_action_release = lambda: \
            self.__view.set_sync_daw_transport_button_state(False)

        sync_daw_transport_action_delay = lambda: \
            None

        self.__sync_saw_transport_handler = updateable.DelayedActionHandler(self.sync_daw_transport_action_click,
                                                                           sync_daw_transport_action_release,
                                                                           sync_daw_transport_action_delay,
                                                                           0.1)

        self.__updateable_mux.add_updateable(self.__sync_saw_transport_handler)

        self.__drop_manager = drop.DropManager(self.__view, self.__updateable_mux)

        self.__drop_manager.add_drop_fx(constants.MIDI_CH_DROP_FX_1,
                                        constants.MIDI_CC_DROP_FX_1,
                                        constants.LOOPERS_ALL_CHANNEL,
                                        constants.DROP_FX_1_MIXER_SLOT,
                                        constants.ENDLESS_SMILE_PLUGIN_INTENSITY_PARAM_INDEX)

        self.__drop_manager.add_drop_fx(constants.MIDI_CH_DROP_FX_2,
                                        constants.MIDI_CC_DROP_FX_2,
                                        constants.LOOPERS_ALL_CHANNEL,
                                        constants.DROP_FX_2_MIXER_SLOT,
                                        constants.TURNADO_DICTATOR_PARAM_INDEX)

        self.__drop_manager.add_drop_fx(constants.MIDI_CH_DROP_FX_3,
                                        constants.MIDI_CC_DROP_FX_3,
                                        constants.LOOPERS_ALL_CHANNEL,
                                        constants.DROP_FX_3_MIXER_SLOT,
                                        constants.TURNADO_DICTATOR_PARAM_INDEX)

        self.__drop_manager.add_drop_fx(constants.MIDI_CH_DROP_FX_4,
                                        constants.MIDI_CC_DROP_FX_4,
                                        constants.LOOPERS_ALL_CHANNEL,
                                        constants.DROP_FX_4_MIXER_SLOT,
                                        constants.TURNADO_DICTATOR_PARAM_INDEX)

        self.__drop_manager.add_drop_fx(constants.MIDI_CH_DROP_FX_5,
                                        constants.MIDI_CC_DROP_FX_5,
                                        constants.LOOPERS_ALL_CHANNEL,
                                        constants.DROP_FX_5_MIXER_SLOT,
                                        constants.TURNADO_DICTATOR_PARAM_INDEX)

        self.__drop_manager.add_drop_fx(constants.MIDI_CH_DROP_FX_6,
                                        constants.MIDI_CC_DROP_FX_6,
                                        constants.LOOPERS_ALL_CHANNEL,
                                        constants.DROP_FX_6_MIXER_SLOT,
                                        constants.TURNADO_DICTATOR_PARAM_INDEX)

        self.__drop_manager.add_drop_fx(constants.MIDI_CH_DROP_FX_7,
                                        constants.MIDI_CC_DROP_FX_7,
                                        constants.LOOPERS_ALL_CHANNEL,
                                        constants.DROP_FX_7_MIXER_SLOT,
                                        constants.TURNADO_DICTATOR_PARAM_INDEX)

    def on_init_script(self):

        if False == self.__initialized:
            print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.on_init_script.__name__)

            try:
                for looper_id in self.__loopers:
                    self.__loopers[looper_id].on_init_script()
                self.__initialized = True
                self.clear()
                self.__view.set_tempo(mixer.getCurrentTempo() / 1000.0, True)
                self.set_sample_length(SampleLength.LENGTH_1)
                self.set_resample_mode(ResampleMode.NONE)
                self.__loopers[self.__selected_looper].select()
            except Exception as e:
                print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.on_init_script.__name__ + ": failed to initialize the script.")
                print(e)

    # context_interface Implementation
    def get_sample_length(self) -> int:
        return self.__selected_sample_length

    def get_device_name(self) -> str:
        return self.__context.device_name

    def get_updateable_mux(self) -> updateable.UpdateableMux:
        return self.__updateable_mux
    # context_interface implementation end

    def sync_daw_transport_action_click(self):
        self.__view.set_sync_daw_transport_button_state(True)
        self.__sync_daw_transport()

    def clear_handler_action_second_click(self):
        self.__view.set_clear_btn_state(updateable.DoubleClickTimeoutHandler.STATE_SECOND_CLICK_DONE)
        self.stop()

    def is_playing(self):
        return transport.isPlaying()

    def stop(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.stop.__name__)

        self.clear()

        if transport.isPlaying():
            transport.stop()
            transport.setSongPos(0.0)
            self.__view.set_start_btn_state(False)

    def start(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.start.__name__)

        if not transport.isPlaying():
            transport.start()
            self.__view.set_start_btn_state(True)

    def set_tempo(self, tempo, forward_to_device):
        target_tempo = tempo - tempo % 50
        current_tempo = mixer.getCurrentTempo() / 100.0
        if math.fabs(int(current_tempo / 10) - int(target_tempo / 10)) >= constants.TEMPO_JOG_ROTATION_THRESHOLD:
            jog_rotation = int(target_tempo - current_tempo)
            print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.set_tempo.__name__ + \
                  ": target tempo: " + str(target_tempo) + ", current tempo: " + str(current_tempo) + \
                  ", jog rotation: " + str(jog_rotation))
            transport.globalTransport(105, jog_rotation)
            self.__view.set_tempo(target_tempo / 10.0, forward_to_device)

    def set_shift_pressed_state(self, shift_pressed):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.set_shift_pressed_state.__name__ + ": shift pressed - " + str(shift_pressed))

        self.__view.set_shift_pressed_state(shift_pressed)

        self.__shift_pressed = shift_pressed

        # if(True == shift_pressed):
        #    self.action_on_double_click(constants.MIDI_CC_SHIFT, self.__loopers[self.__selected_looper].randomize_turnado)

    def set_extra_1_state(self, value, forward_to_device):
        self.__extra_1_state = value
        self.__view.set_extra_1_state(value, forward_to_device)

    def switch_to_next_turnado_preset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.switch_to_next_turnado_preset.__name__)
        self.__loopers[self.__selected_looper].switch_to_next_turnado_preset()

        self.__view.switch_to_next_turnado_preset()

    def switch_to_prev_turnado_preset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.switch_to_prev_turnado_preset.__name__)
        self.__loopers[self.__selected_looper].switch_to_prev_turnado_preset()

    def get_shift_pressed_state(self):
        return self.__shift_pressed

    def get_extra_1_state(self):
        return self.__extra_1_state

    def get_sidechain_change_mode(self):
        self.__sidechain_change_mode

    def __select_looper(self, selected_looper, force = False):
        # print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.__select_looper.__name__ + ": selected looper - " + str(selected_looper))

        if selected_looper != self.__selected_looper or force:
            self.__loopers[self.__selected_looper].stop_all_recordings()
            self.__selected_looper = selected_looper
            for looper_id in self.__loopers:
                if looper_id == selected_looper:
                    self.__loopers[looper_id].select()
                else:
                    self.__loopers[looper_id].unselect()

    def __set_looper_volume(self, looper_index, looper_volume, forward_to_device):
        self.__loopers.get(looper_index).set_looper_volume(looper_volume, forward_to_device)

    def __get_looper_volume(self, looper_index):
        return self.__loopers.get(looper_index).get_looper_volume()

    def __set_track_volume(self, track_index, track_volume, forward_to_device):
        self.__loopers.get(self.__selected_looper).set_track_volume(track_index, track_volume, forward_to_device)

    def set_sample_length(self, sample_length):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.set_sample_length.__name__ + ": selected sample length - " + str(sample_length))
        self.__selected_sample_length = sample_length
        self.__view.update_sample_length(sample_length)

        # print_all_plugin_parameters(17, 9)

    def clear(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.clear.__name__)
        self.__set_prolonged_record_length_mode(False)
        for looper_id in self.__loopers:
            self.__loopers[looper_id].clear_looper()
        self.__select_looper(constants.Looper_1, True)
        self.__drop_manager.click_drop()
        self.__drop_manager.release_drop()
        self.set_sample_length(SampleLength.LENGTH_1)
        self.set_resample_mode(ResampleMode.NONE)
        self.set_decay_side_chain_level(constants.Track_1, constants.DEFAULT_DECAY_SIDECHAIN_LEVEL)
        self.set_decay_side_chain_level(constants.Track_2, constants.DEFAULT_DECAY_SIDECHAIN_LEVEL)
        self.set_decay_side_chain_level(constants.Track_3, constants.DEFAULT_DECAY_SIDECHAIN_LEVEL)
        self.set_decay_side_chain_level(constants.Track_4, constants.DEFAULT_DECAY_SIDECHAIN_LEVEL)
        self.set_tension_side_chain_level(constants.Track_1, constants.DEFAULT_TENSION_SIDECHAIN_LEVEL)
        self.set_tension_side_chain_level(constants.Track_2, constants.DEFAULT_TENSION_SIDECHAIN_LEVEL)
        self.set_tension_side_chain_level(constants.Track_3, constants.DEFAULT_TENSION_SIDECHAIN_LEVEL)
        self.set_tension_side_chain_level(constants.Track_4, constants.DEFAULT_TENSION_SIDECHAIN_LEVEL)
        self.set_extra_1_state(0, True)
        self.__reset_recording_routing_status()

    def clear_current_looper(self):
        self.__loopers[self.__selected_looper].clear_looper()

    def clear_track(self, track_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.clear_track.__name__ + ": track - " + str(track_id))
        self.__loopers[self.__selected_looper].clear_track(track_id)

    def __set_restream_activation_status(self, status):
        parameter_id_restream_activation_status = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "RESTREAM_ACTIVATION_STATUS", constants.RESAMPLING_AUDIO_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(status, parameter_id_restream_activation_status, constants.MASTER_CHANNEL, constants.RESAMPLING_AUDIO_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def __reset_recording_routing_status(self):
        parameter_id_route_to_master = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "RouteInput2Master", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id_route_to_recodring_bus = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "RouteInput2RB", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(fl_helper.MAX_VOLUME_LEVEL_VALUE, parameter_id_route_to_master, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        plugins.setParamValue(0.0, parameter_id_route_to_recodring_bus, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        self.__set_restream_activation_status(False)

    def set_recording_routing_status(self, recording_status):

        parameter_id_route_to_master = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "RouteInput2Master", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id_route_to_recodring_bus = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "RouteInput2RB", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)

        if recording_status == True:
            plugins.setParamValue(0.0, parameter_id_route_to_master, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(fl_helper.MAX_VOLUME_LEVEL_VALUE, parameter_id_route_to_recodring_bus, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        else:
            plugins.setParamValue(fl_helper.MAX_VOLUME_LEVEL_VALUE, parameter_id_route_to_master, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
            plugins.setParamValue(0.0, parameter_id_route_to_recodring_bus, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def change_recording_state(self, selected_track_id):
            print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.change_recording_state.__name__ + ": track - " + str(selected_track_id))
            self.__change_recording_state_to(selected_track_id, not self.__loopers[self.__selected_looper].is_track_recording_in_progress(selected_track_id))

    def action_on_double_click(self, pressed_button, action_first_click, action_second_click):
        pressed_time = time.time()

        if not pressed_button in self.__buttons_last_press_time.keys():
            self.__buttons_last_press_time[pressed_button] = 0

        if (pressed_time - self.__buttons_last_press_time[pressed_button]) < 0.5:
            # double click
            self.__buttons_last_press_time[pressed_button] = 0
            action_second_click()
        else:
            self.__buttons_last_press_time[pressed_button] = pressed_time
            action_first_click()

    def set_looper_side_chain_level(self, track_id, sidechain_level):
        if self.__selected_looper != constants.Looper_1:
            self.__loopers[self.__selected_looper].set_looper_side_chain_level(track_id, sidechain_level)

    def set_resample_mode(self, resample_mode):

        if resample_mode == self.get_resample_mode():
            resample_mode = ResampleMode.NONE

        self.__set_restream_activation_status(resample_mode != ResampleMode.NONE)

        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.set_resample_mode.__name__ + ": to - " + str(resample_mode))
        self.__resample_mode = resample_mode

        self.__view.set_resample_mode(resample_mode)

    def get_resample_mode(self):
        return self.__resample_mode

    def set_turnado_dictator_level(self, turnado_dictator_level):
        self.__loopers[self.__selected_looper].set_turnado_dictator_level(turnado_dictator_level)

    def set_turnado_dry_wet_level(self, turnado_dry_wet_level):
        self.__loopers[self.__selected_looper].set_turnado_dry_wet_level(turnado_dry_wet_level)

    def drop(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.drop.__name__)
        self.__drop_manager.click_drop()
        self.__loopers[constants.Looper_1].set_track_volume(constants.Track_1, fl_helper.MAX_VOLUME_LEVEL_VALUE, True)
        self.__loopers[constants.Looper_1].set_track_volume(constants.Track_2, fl_helper.MAX_VOLUME_LEVEL_VALUE, True)
        self.__loopers[constants.Looper_1].set_track_volume(constants.Track_3, fl_helper.MAX_VOLUME_LEVEL_VALUE, True)
        self.__loopers[constants.Looper_1].set_track_volume(constants.Track_4, fl_helper.MAX_VOLUME_LEVEL_VALUE, True)
        self.__set_looper_volume(constants.Looper_1, fl_helper.MAX_VOLUME_LEVEL_VALUE, True)
        self.__loopers[constants.Looper_1].set_turnado_dictator_level(0.0)
        self.__loopers[constants.Looper_1].set_turnado_dry_wet_level(constants.DEFAULT_TURNADO_DRY_WET_LEVEL)

    def turn_track_on_off(self, track_id):
        if 0 != self.__loopers[self.__selected_looper].get_track_volume(track_id):
            self.__loopers[self.__selected_looper].set_track_volume(track_id, 0.0, True)
        else:
            self.__loopers[self.__selected_looper].set_track_volume(track_id, fl_helper.MAX_VOLUME_LEVEL_VALUE, True)

    def turn_looper_on_off(self, looper_id):
        if 0 != self.__get_looper_volume(looper_id):
            self.__set_looper_volume(looper_id, 0.0, True)
        else:
            self.__set_looper_volume(looper_id, fl_helper.MAX_VOLUME_LEVEL_VALUE, True)

    def __get_visible_track_volume(self, track_id):
        return self.__loopers[self.__selected_looper].get_track_volume(track_id)

    def __change_recording_state_to(self, selected_track_id, recording_state):
        if recording_state:
            self.__start_recording_track(selected_track_id)

            for track_id in self.__loopers[self.__selected_looper].get_tracks():
                if track_id != selected_track_id:
                    self.__stop_recording_track(track_id, selected_track_id)

            self.set_recording_routing_status(True)
        else:
            self.__stop_recording_track(selected_track_id, selected_track_id)
            self.set_recording_routing_status(False)

    def __start_recording_track(self, selected_track_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.__start_recording_track.__name__ + ": track - " + str(selected_track_id) + ", resample mode - " + str(self.get_resample_mode()))
        self.__loopers[self.__selected_looper].start_recording_track(selected_track_id, self.__selected_sample_length, self.get_resample_mode())

        for looper_id in self.__loopers:
            for track_id in self.__loopers[looper_id].get_tracks():
                if looper_id == self.__selected_looper:
                    if track_id == selected_track_id:
                        self.__loopers[looper_id].get_track(track_id).set_routing_level(fl_helper.MAX_VOLUME_LEVEL_VALUE)
                    else:
                        self.__loopers[looper_id].get_track(track_id).set_routing_level(0.0)
                else:
                    self.__loopers[looper_id].get_track(track_id).set_routing_level(0.0)

    def __stop_recording_track(self, track_id, selected_track_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.__stop_recording_track.__name__ + ": track - " + str(track_id))

        if self.__loopers[self.__selected_looper].get_resample_mode(track_id) == ResampleMode.FROM_ALL_LOOPERS_TO_TRACK:
            # clear all tracks of all loopers, except the one for which recording is over
            for looper_id in self.__loopers:
                for track_id_it in self.__loopers[looper_id].get_tracks():
                    if (looper_id != self.__selected_looper or track_id_it != track_id):
                        self.__loopers[looper_id].clear_track(track_id_it)
                    else:
                        self.__loopers[looper_id].set_track_volume(track_id_it, fl_helper.MAX_VOLUME_LEVEL_VALUE, True)
                self.__loopers[looper_id].set_turnado_dictator_level(0.0)
                self.__loopers[looper_id].set_turnado_dry_wet_level(constants.DEFAULT_TURNADO_DRY_WET_LEVEL)

        self.__loopers[self.__selected_looper].stop_recording_track(track_id)
        self.__loopers[self.__selected_looper].get_track(track_id).set_routing_level(0.0)

        if track_id == selected_track_id:
            self.set_resample_mode(ResampleMode.NONE)

    def set_tension_side_chain_level(self, track_id, sidechain_level):
        self.__view.set_tension_side_chain_level(track_id, sidechain_level)

        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "ST", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def set_decay_side_chain_level(self, track_id, sidechain_level):
        self.__view.set_decay_side_chain_level(track_id, sidechain_level)

        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "T" + str(track_id + 1) + "SD", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(sidechain_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def __sync_daw_transport(self):
        # print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.__sync_daw_transport.__name__)
        transport.setSongPos(0.0)

    def __set_prolonged_record_length_mode(self, val):
        self.__prolonged_record_length_mode = val
        self.__view.set_prolonged_record_length_mode(val)

    def __get_prolonged_record_length_mode(self):
        return self.__prolonged_record_length_mode

    def __change_prolonged_record_length_mode(self):
        self.__set_prolonged_record_length_mode(not self.__get_prolonged_record_length_mode())

    def __process_mute_track(self, event, track_id):
        visible_track_volume = self.__get_visible_track_volume(track_id)
        if self.get_extra_1_state():
            if event.data2 != 0:
                if visible_track_volume != 0:
                    self.turn_track_on_off(track_id)
            else:
                if visible_track_volume == 0:
                    self.turn_track_on_off(track_id)
        else:
            if event.data2 != 0:
                self.turn_track_on_off(track_id)

    def __process_mute_looper(self, event, looper_id):
        visible_looper_volume = self.__get_looper_volume(looper_id)
        if self.get_extra_1_state():
            if event.data2 != 0:
                if visible_looper_volume != 0:
                    self.turn_looper_on_off(looper_id)
            else:
                if visible_looper_volume == 0:
                    self.turn_looper_on_off(looper_id)
        else:
            if event.data2 != 0:
                self.turn_looper_on_off(looper_id)

    def __process_clear_track(self, event, track_id):
        if event.data2 != 0:
            self.clear_track(track_id)

    def __set_track_pan(self, track_id, pan, forward_to_device):
        self.__loopers[self.__selected_looper].set_track_pan(track_id, pan, forward_to_device)

    

    def __on_midi_msg_processing(self, event):

        # fl_helper.print_midi_event(event)

        if event.data1 == constants.MIDI_CC_SYNC_DAW_TRANSPORT and event.midiChan == constants.MIDI_CH_SYNC_DAW_TRANSPORT:
            if event.data2 != 0:
                self.__sync_saw_transport_handler.click()
            else:
                self.__sync_saw_transport_handler.release()
        elif event.data1 == constants.MIDI_CC_DROP_FX_1 and event.midiChan == constants.MIDI_CH_DROP_FX_1:
            self.__drop_manager.set_fx_level(event.midiChan, event.data1, event.data2 / fl_helper.MIDI_MAX_VALUE, False)
        elif event.data1 == constants.MIDI_CC_DROP_FX_2 and event.midiChan == constants.MIDI_CH_DROP_FX_2:
            self.__drop_manager.set_fx_level(event.midiChan, event.data1, event.data2 / fl_helper.MIDI_MAX_VALUE, False)
        elif event.data1 == constants.MIDI_CC_DROP_FX_3 and event.midiChan == constants.MIDI_CH_DROP_FX_3:
            self.__drop_manager.set_fx_level(event.midiChan, event.data1, event.data2 / fl_helper.MIDI_MAX_VALUE, False)
        elif event.data1 == constants.MIDI_CC_DROP_FX_4 and event.midiChan == constants.MIDI_CH_DROP_FX_4:
            self.__drop_manager.set_fx_level(event.midiChan, event.data1, event.data2 / fl_helper.MIDI_MAX_VALUE, False)
        elif event.data1 == constants.MIDI_CC_DROP_FX_5 and event.midiChan == constants.MIDI_CH_DROP_FX_5:
            self.__drop_manager.set_fx_level(event.midiChan, event.data1, event.data2 / fl_helper.MIDI_MAX_VALUE, False)
        elif event.data1 == constants.MIDI_CC_DROP_FX_6 and event.midiChan == constants.MIDI_CH_DROP_FX_6:
            self.__drop_manager.set_fx_level(event.midiChan, event.data1, event.data2 / fl_helper.MIDI_MAX_VALUE, False)
        elif event.data1 == constants.MIDI_CC_DROP_FX_7 and event.midiChan == constants.MIDI_CH_DROP_FX_7:
            self.__drop_manager.set_fx_level(event.midiChan, event.data1, event.data2 / fl_helper.MIDI_MAX_VALUE, False)
        elif event.data1 == constants.MIDI_CC_DROP and event.midiChan == constants.MIDI_CH_DROP:
            if event.data2 != 0:
                self.drop()
            else:
                self.__drop_manager.release_drop()
        # elif event.data1 == constants.MIDI_CC_RESAMPLE_MODE_FROM_LOOPER_TO_TRACK and self.get_shift_pressed_state():
        #    self.set_resample_mode(ResampleMode.FROM_LOOPER_TO_TRACK)

            # action = lambda self = self: (self.set_resample_mode(ResampleMode.NONE), \
            #                             self.switch_to_prev_turnado_preset())
            # self.action_on_double_click(constants.MIDI_CC_RESAMPLE_MODE_FROM_LOOPER_TO_TRACK + constants.SHIFT_BUTTON_ON_DOUBLE_CLICK_SHIFT, action)

        # elif event.data1 == constants.MIDI_CC_RESAMPLE_MODE_FROM_ALL_LOOPERS_TO_TRACK and self.get_shift_pressed_state():
            # self.set_resample_mode(ResampleMode.FROM_ALL_LOOPERS_TO_TRACK)
            #
            # action = lambda self = self: (self.set_resample_mode(ResampleMode.NONE), \
            #                               self.switch_to_next_turnado_preset())
            # self.action_on_double_click(constants.MIDI_CC_RESAMPLE_MODE_FROM_ALL_LOOPERS_TO_TRACK + constants.SHIFT_BUTTON_ON_DOUBLE_CLICK_SHIFT, action)
        elif event.data1 == constants.MIDI_CC_LOOPER_1 and event.midiChan == constants.MIDI_CH_LOOPER_1:
            self.__select_looper(constants.Looper_1)
        elif event.data1 == constants.MIDI_CC_LOOPER_2 and event.midiChan == constants.MIDI_CH_LOOPER_2:
            self.__select_looper(constants.Looper_2)
            # self.action_on_double_click(constants.SHIFT_BUTTON_ON_DOUBLE_CLICK_SHIFT + constants.MIDI_CC_SAMPLE_LENGTH_2, self.__change_prolonged_record_length_mode)
        elif event.data1 == constants.MIDI_CC_LOOPER_3 and event.midiChan == constants.MIDI_CH_LOOPER_3:
            self.__select_looper(constants.Looper_3)
        elif event.data1 == constants.MIDI_CC_LOOPER_4 and event.midiChan == constants.MIDI_CH_LOOPER_4:
            self.__select_looper(constants.Looper_4)
        elif event.data1 == constants.MIDI_CC_CLEAR_LOOPER and constants.MIDI_CH_CLEAR_LOOPER:
            if event.data2 != 0:
                self.__loopers[self.__selected_looper].handle_clear_looper_click()
            else:
                self.__loopers[self.__selected_looper].handle_clear_looper_release()
        elif event.data1 == constants.MIDI_CC_CLEAR and event.midiChan == constants.MIDI_CH_CLEAR:
            if event.data2 != 0:
                self.__clear_handler.click()
            else:
                self.__clear_handler.release()
        elif event.data1 == constants.MIDI_CC_START and event.midiChan == constants.MIDI_CH_START:
            if event.data2 != 0:
                self.start()
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_1_64 and event.midiChan == constants.MIDI_CH_SAMPLE_LENGTH_1_64:
            self.set_sample_length(SampleLength.LENGTH_1_64)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_1_32 and event.midiChan == constants.MIDI_CH_SAMPLE_LENGTH_1_32:
            self.set_sample_length(SampleLength.LENGTH_1_32)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_1_16 and event.midiChan == constants.MIDI_CH_SAMPLE_LENGTH_1_16:
            self.set_sample_length(SampleLength.LENGTH_1_16)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_1_8 and event.midiChan == constants.MIDI_CH_SAMPLE_LENGTH_1_8:
            self.set_sample_length(SampleLength.LENGTH_1_8)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_1_4 and event.midiChan == constants.MIDI_CH_SAMPLE_LENGTH_1_4:
            self.set_sample_length(SampleLength.LENGTH_1_4)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_1_2 and event.midiChan == constants.MIDI_CH_SAMPLE_LENGTH_1_2:
            self.set_sample_length(SampleLength.LENGTH_1_2)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_1 and event.midiChan == constants.MIDI_CH_SAMPLE_LENGTH_1:
            self.set_sample_length(SampleLength.LENGTH_1)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_2:
            if True == self.__get_prolonged_record_length_mode():
                self.set_sample_length(SampleLength.LENGTH_3)
            else:
                self.set_sample_length(SampleLength.LENGTH_2)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_4:
            if True == self.__get_prolonged_record_length_mode():
                self.set_sample_length(SampleLength.LENGTH_6)
            else:
                self.set_sample_length(SampleLength.LENGTH_4)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_8:
            if True == self.__get_prolonged_record_length_mode():
                self.set_sample_length(SampleLength.LENGTH_12)
            else:
                self.set_sample_length(SampleLength.LENGTH_8)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_16:
            if True == self.__get_prolonged_record_length_mode():
                self.set_sample_length(SampleLength.LENGTH_24)
            else:
                self.set_sample_length(SampleLength.LENGTH_16)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_32:
            if True == self.__get_prolonged_record_length_mode():
                self.set_sample_length(SampleLength.LENGTH_48)
            else:
                self.set_sample_length(SampleLength.LENGTH_32)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_64:
            if True == self.__get_prolonged_record_length_mode():
                self.set_sample_length(SampleLength.LENGTH_96)
            else:
                self.set_sample_length(SampleLength.LENGTH_64)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_128:
            self.set_sample_length(SampleLength.LENGTH_128)
        elif event.data1 == constants.MIDI_CC_TRACK_CLEAR_1 and event.midiChan == constants.MIDI_CH_TRACK_CLEAR_1:
            self.__process_clear_track(event, constants.Track_1)
        elif event.data1 == constants.MIDI_CC_TRACK_CLEAR_2 and event.midiChan == constants.MIDI_CH_TRACK_CLEAR_2:
            self.__process_clear_track(event, constants.Track_2)
        elif event.data1 == constants.MIDI_CC_TRACK_CLEAR_3 and event.midiChan == constants.MIDI_CH_TRACK_CLEAR_3:
            self.__process_clear_track(event, constants.Track_3)
        elif event.data1 == constants.MIDI_CC_TRACK_CLEAR_4 and event.midiChan == constants.MIDI_CH_TRACK_CLEAR_4:
            self.__process_clear_track(event, constants.Track_4)
        elif event.data1 == constants.MIDI_CC_SHIFT:
            self.set_shift_pressed_state(event.data2 == fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TURNADO_DRY_WET and self.get_shift_pressed_state():
            self.set_turnado_dry_wet_level(event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_LOOPER_VOLUME_1 and event.midiChan == constants.MIDI_CH_LOOPER_VOLUME_1:
            self.__set_looper_volume(constants.Looper_1, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE, False)
        elif event.data1 == constants.MIDI_CC_LOOPER_VOLUME_2 and event.midiChan == constants.MIDI_CH_LOOPER_VOLUME_2:
            self.__set_looper_volume(constants.Looper_2, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE, False)
        elif event.data1 == constants.MIDI_CC_LOOPER_VOLUME_3 and event.midiChan == constants.MIDI_CH_LOOPER_VOLUME_3:
            self.__set_looper_volume(constants.Looper_3, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE, False)
        elif event.data1 == constants.MIDI_CC_LOOPER_VOLUME_4 and event.midiChan == constants.MIDI_CH_LOOPER_VOLUME_4:
            self.__set_looper_volume(constants.Looper_4, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE, False)
        elif event.data1 == constants.MIDI_CC_LOOPER_MUTE_1 and event.midiChan == constants.MIDI_CH_LOOPER_MUTE_1:
            self.__process_mute_looper(event, constants.Looper_1)
        elif event.data1 == constants.MIDI_CC_LOOPER_MUTE_2 and event.midiChan == constants.MIDI_CH_LOOPER_MUTE_2:
            self.__process_mute_looper(event, constants.Looper_2)
        elif event.data1 == constants.MIDI_CC_LOOPER_MUTE_3 and event.midiChan == constants.MIDI_CH_LOOPER_MUTE_3:
            self.__process_mute_looper(event, constants.Looper_3)
        elif event.data1 == constants.MIDI_CC_LOOPER_MUTE_4 and event.midiChan == constants.MIDI_CH_LOOPER_MUTE_4:
            self.__process_mute_looper(event, constants.Looper_4)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_1 and True == self.get_shift_pressed_state():
            self.set_tension_side_chain_level(constants.Track_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_2 and True == self.get_shift_pressed_state():
            self.set_decay_side_chain_level(constants.Track_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_3 and True == self.get_shift_pressed_state():
            self.set_tension_side_chain_level(constants.Track_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_4 and True == self.get_shift_pressed_state():
            self.set_decay_side_chain_level(constants.Track_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_1 and event.midiChan == constants.MIDI_CH_TRACK_VOLUME_1:
            self.__set_track_volume(constants.Track_1, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE, False)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_2 and event.midiChan == constants.MIDI_CH_TRACK_VOLUME_2:
            self.__set_track_volume(constants.Track_2, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE, False)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_3 and event.midiChan == constants.MIDI_CH_TRACK_VOLUME_3:
            self.__set_track_volume(constants.Track_3, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE, False)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_4 and event.midiChan == constants.MIDI_CH_TRACK_VOLUME_4:
            self.__set_track_volume(constants.Track_4, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE, False)
        elif event.data1 == constants.MIDI_CC_EXTRA_1 and event.midiChan == constants.MIDI_CH_EXTRA_1 and event.data2 != 0:
            self.set_extra_1_state(not self.get_extra_1_state(), True)
        elif event.data1 == constants.MIDI_CC_TRACK_MUTE_1 and event.midiChan == constants.MIDI_CH_TRACK_MUTE_1:
            self.__process_mute_track(event, constants.Track_1)
        elif event.data1 == constants.MIDI_CC_TRACK_MUTE_2 and event.midiChan == constants.MIDI_CH_TRACK_MUTE_2:
            self.__process_mute_track(event, constants.Track_2)
        elif event.data1 == constants.MIDI_CC_TRACK_MUTE_3 and event.midiChan == constants.MIDI_CH_TRACK_MUTE_3:
            self.__process_mute_track(event, constants.Track_3)
        elif event.data1 == constants.MIDI_CC_TRACK_MUTE_4 and event.midiChan == constants.MIDI_CH_TRACK_MUTE_4:
            self.__process_mute_track(event, constants.Track_4)
        elif event.data1 == constants.MIDI_CC_TRACK_PAN_1 and event.midiChan == constants.MIDI_CH_TRACK_PAN_1:
            self.__set_track_pan(constants.Track_1, (event.data2 / fl_helper.MIDI_MAX_VALUE), False)
        elif event.data1 == constants.MIDI_CC_TRACK_PAN_2 and event.midiChan == constants.MIDI_CH_TRACK_PAN_2:
            self.__set_track_pan(constants.Track_2, (event.data2 / fl_helper.MIDI_MAX_VALUE), False)
        elif event.data1 == constants.MIDI_CC_TRACK_PAN_3 and event.midiChan == constants.MIDI_CH_TRACK_PAN_3:
            self.__set_track_pan(constants.Track_3, (event.data2 / fl_helper.MIDI_MAX_VALUE), False)
        elif event.data1 == constants.MIDI_CC_TRACK_PAN_4 and event.midiChan == constants.MIDI_CH_TRACK_PAN_4:
            self.__set_track_pan(constants.Track_4, (event.data2 / fl_helper.MIDI_MAX_VALUE), False)
        elif event.data1 == constants.MIDI_CC_TRACK_RECORD_1 and event.midiChan == constants.MIDI_CH_TRACK_RECORD_1:
            self.change_recording_state(constants.Track_1)
        elif event.data1 == constants.MIDI_CC_TRACK_RECORD_2 and event.midiChan == constants.MIDI_CH_TRACK_RECORD_2:
            self.change_recording_state(constants.Track_2)
        elif event.data1 == constants.MIDI_CC_TRACK_RECORD_3 and event.midiChan == constants.MIDI_CH_TRACK_RECORD_3:
            self.change_recording_state(constants.Track_3)
        elif event.data1 == constants.MIDI_CC_TRACK_RECORD_4 and event.midiChan == constants.MIDI_CH_TRACK_RECORD_4:
            self.change_recording_state(constants.Track_4)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_1 and True == self.get_shift_pressed_state():
            self.set_tension_side_chain_level(constants.Track_3, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_2 and True == self.get_shift_pressed_state():
            self.set_decay_side_chain_level(constants.Track_3, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_3 and True == self.get_shift_pressed_state():
            self.set_tension_side_chain_level(constants.Track_4, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_4 and True == self.get_shift_pressed_state():
            self.set_decay_side_chain_level(constants.Track_4, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_1:
            self.set_looper_side_chain_level(constants.Track_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_2:
            self.set_looper_side_chain_level(constants.Track_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_3:
            self.set_looper_side_chain_level(constants.Track_3, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_SIDECHAIN_4:
            self.set_looper_side_chain_level(constants.Track_4, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TURNADO_DICTATOR and self.is_playing():
            self.set_turnado_dictator_level(event.data2 / fl_helper.MIDI_MAX_VALUE)

    def on_midi_msg(self, event):

        self.on_init_script()

        # fl_helper.print_all_plugin_parameters(LOOPER_1_CHANNEL, LOOPER_TURNADO_SLOT_INDEX)

        event.handled = False

        if event.data1 == constants.MIDI_CC_TEMPO and \
           event.midiChan == constants.MIDI_CH_TEMPO:
            if not self.is_playing():
                self.set_tempo(800 + int((event.data2 / fl_helper.MIDI_MAX_VALUE) * 1000.0), False)  # from 80 to 180
            else:
                self.__view.set_tempo(mixer.getCurrentTempo() / 1000.0, True)
        else:
            if (not (event.data1 == constants.MIDI_CC_CLEAR and event.midiChan == constants.MIDI_CH_CLEAR and not self.is_playing())):
                if not transport.isPlaying():
                    self.start()
            self.__on_midi_msg_processing(event)

        event.handled = True

    def on_update(self):
        self.__updateable_mux.update()