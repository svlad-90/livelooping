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

    def on_init_script(self):

        if False == self.__initialized:
            print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.on_init_script.__name__)

            try:
                for looper_id in self.__loopers:
                    self.__loopers[looper_id].on_init_script()
                self.__initialized = True
                self.clear()
                self.__view.set_tempo(mixer.getCurrentTempo() / 1000.0)
                self.set_sample_length(SampleLength.LENGTH_1)
                self.set_resample_mode(ResampleMode.NONE)
            except Exception as e:
                print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.on_init_script.__name__ + ": failed to initialize the script.")
                print(e)

    # context_interface Implementation
    def get_sample_length(self) -> int:
        return self.__selected_sample_length

    def get_device_name(self) -> str:
        return self.__context.device_name
    # context_interface implementation end

    def is_playing(self):
        return transport.isPlaying()

    def play_stop(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.play_stop.__name__)

        self.clear()

        if transport.isPlaying():
            transport.stop()
            self.__view._p(False)
        else:
            transport.start()
            self.__view._p(True)

    def set_tempo(self, tempo):
        target_tempo = tempo - tempo % 50
        current_tempo = mixer.getCurrentTempo() / 100.0
        if math.fabs( int(current_tempo/10) - int(target_tempo/10) ) >= constants.TEMPO_JOG_ROTATION_THRESHOLD:
            jog_rotation = int( target_tempo - current_tempo )
            print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.set_tempo.__name__ + ": target tempo: " + str(target_tempo) + ", current tempo: " + str(current_tempo) + ", jog rotation: " + str(jog_rotation))
            transport.globalTransport( 105, jog_rotation )
            self.__view.set_tempo(target_tempo / 10.0)

    def set_shift_pressed_state(self, shift_pressed):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.set_shift_pressed_state.__name__ + ": shift pressed - " + str(shift_pressed))

        self.__view.set_shift_pressed_state(shift_pressed)

        self.__shift_pressed = shift_pressed

        if(True == shift_pressed):
            self.action_on_double_click(constants.MIDI_CC_SHIFT, self.__loopers[self.__selected_looper].randomize_turnado)

    def switch_to_next_turnado_preset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.switch_to_next_turnado_preset.__name__)
        self.__loopers[self.__selected_looper].switch_to_next_turnado_preset()

        self.__view.switch_to_next_turnado_preset()

    def switch_to_prev_turnado_preset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.switch_to_prev_turnado_preset.__name__)
        self.__loopers[self.__selected_looper].switch_to_prev_turnado_preset()

    def get_shift_pressed_state(self):
        return self.__shift_pressed

    def get_sidechain_change_mode(self):
        self.__sidechain_change_mode

    def add_pressed_sampler_button(self, pressed_sampler_button):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.add_pressed_sampler_button.__name__ + ": added sampler button - " + str(pressed_sampler_button))
        self.__pressed_sampler_buttons.add(pressed_sampler_button)
        self.__last_pressed_sampler_button = pressed_sampler_button

    def removepressed_sampler_button(self, released_sampler_button):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.add_pressed_sampler_button.__name__ + ": removed sampler button - " + str(released_sampler_button))
        self.__pressed_sampler_buttons.remove(released_sampler_button)

        if self.__last_pressed_sampler_button == released_sampler_button:
            self.__last_pressed_sampler_button = PressedSamplerButton.NONE

    def select_looper(self, selected_looper):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.select_looper.__name__ + ": selected looper - " + str(selected_looper))

        if selected_looper != self.__selected_looper:

            self.__loopers[self.__selected_looper].stop_all_recordings()

            self.__selected_looper = selected_looper
            self.__loopers[self.__selected_looper].update_tracks_stats()
            self.__loopers[self.__selected_looper].update_looper_stats()
            self.__view.select_looper(selected_looper)

    def set_looper_volume(self, looper_volume):
        self.__loopers.get(self.__selected_looper).set_looper_volume(looper_volume)

    def set_track_volume(self, track_index, track_volume):
        self.__loopers.get(self.__selected_looper).set_track_volume(track_index, track_volume)

    def set_sample_length(self, sample_length):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.set_sample_length.__name__ + ": selected sample length - " + str(sample_length))
        self.__selected_sample_length = sample_length
        self.__view.update_sample_length(sample_length)

        #print_all_plugin_parameters(17, 9)

    def clear(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.clear.__name__)
        for looper_id in self.__loopers:
            self.__loopers[looper_id].clear_looper()
        self.select_looper(constants.Looper_1)
        self.set_looper_volume(fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.set_drop_intencity(0.0)
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
        self.__view.clear()

    def clear_current_looper(self):
        self.__loopers[self.__selected_looper].clear_looper()

    def clear_track(self, track_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.clear_track.__name__ + ": track - " + str(track_id))
        self.__loopers[self.__selected_looper].clear_track(track_id)

    def set_master_routing_level(self, routing_level):
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "MasterFX1M", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(routing_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
        parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL, "MasterFX1S", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(routing_level, parameter_id, constants.MASTER_CHANNEL, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

    def change_recording_state(self, selected_track_id):
            print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.change_recording_state.__name__ + ": track - " + str(selected_track_id))
            self.__change_recording_state_to(selected_track_id, not self.__loopers[self.__selected_looper].is_track_recording_in_progress(selected_track_id))

    def action_on_double_click(self, pressed_button, action):
        pressed_time = time.time()

        if not pressed_button in self.__buttons_last_press_time.keys():
            self.__buttons_last_press_time[pressed_button] = 0

        if (pressed_time - self.__buttons_last_press_time[pressed_button]) < 0.5:
            # double click
            self.__buttons_last_press_time[pressed_button] = 0
            action()
        else:
            self.__buttons_last_press_time[pressed_button] = pressed_time

    def set_looper_side_chain_level(self, track_id, sidechain_level):
        if self.__selected_looper != constants.Looper_1:
            self.__loopers[self.__selected_looper].set_looper_side_chain_level(track_id, sidechain_level)

    def set_drop_intencity(self, drop_intencity):
        plugins.setParamValue(drop_intencity, constants.ENDLESS_SMILE_PLUGIN_INTENSITY_PARAM_INDEX, constants.LOOPER_ALL_CHANNEL, constants.LOOPER_ALL_ENDLESS_SMILE_SLOT_INDEX, midi.PIM_None, True)
        self.__view.set_drop_intencity(drop_intencity)

    def set_resample_mode(self, resample_mode):

        if resample_mode == self.get_resample_mode():
            resample_mode = ResampleMode.NONE

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
        self.set_drop_intencity(0)
        self.__loopers[constants.Looper_1].set_track_volume(constants.Track_1, fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.__loopers[constants.Looper_1].set_track_volume(constants.Track_2, fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.__loopers[constants.Looper_1].set_track_volume(constants.Track_3, fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.__loopers[constants.Looper_1].set_track_volume(constants.Track_4, fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.__loopers[constants.Looper_1].set_looper_volume(fl_helper.MAX_VOLUME_LEVEL_VALUE)
        self.__loopers[constants.Looper_1].set_turnado_dictator_level(0.0)
        self.__loopers[constants.Looper_1].set_turnado_dry_wet_level(constants.DEFAULT_TURNADO_DRY_WET_LEVEL)

    def turn_track_on_off(self, track_id):
        if 0 != self.__loopers[self.__selected_looper].get_track_volume(track_id):
            self.__loopers[self.__selected_looper].set_track_volume(track_id, 0.0)
        else:
            self.__loopers[self.__selected_looper].set_track_volume(track_id, fl_helper.MAX_VOLUME_LEVEL_VALUE)

    def turn_looper_on_off(self, looper_id):

        update_view = looper_id == self.__selected_looper

        if 0 != self.__loopers[looper_id].get_looper_volume():
            self.__loopers[looper_id].set_looper_volume(0.0, not update_view)
        else:
            self.__loopers[looper_id].set_looper_volume(fl_helper.MAX_VOLUME_LEVEL_VALUE, not update_view)

    def __change_recording_state_to(self, selected_track_id, recording_state):
        if recording_state:
            self.__start_recording_track(selected_track_id)

            for track_id in self.__loopers[self.__selected_looper].get_tracks():
                if track_id != selected_track_id:
                    self.__stop_recording_track(track_id)

            self.set_master_routing_level(0)

        else:
            self.__stop_recording_track(selected_track_id)
            self.set_master_routing_level(fl_helper.MAX_VOLUME_LEVEL_VALUE)

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

    def __stop_recording_track(self, track_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.__stop_recording_track.__name__ + ": track - " + str(track_id))

        if self.__loopers[self.__selected_looper].get_resample_mode(track_id) == ResampleMode.FROM_ALL_LOOPERS_TO_TRACK:
            # clear all tracks of all loopers, except the one for which recording is over
            for looper_id in self.__loopers:
                for track_id_it in self.__loopers[looper_id].get_tracks():
                    if ( looper_id != self.__selected_looper or track_id_it != track_id ):
                        self.__loopers[looper_id].clear_track(track_id_it)
                        self.__loopers[looper_id].set_turnado_dictator_level(0.0)
                        self.__loopers[looper_id].set_turnado_dry_wet_level(constants.DEFAULT_TURNADO_DRY_WET_LEVEL)
                    else:
                        self.__loopers[looper_id].set_track_volume(track_id_it, fl_helper.MAX_VOLUME_LEVEL_VALUE)

        self.__loopers[self.__selected_looper].stop_recording_track(track_id)
        self.__loopers[self.__selected_looper].get_track(track_id).set_routing_level(0.0)
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
        print(self.__context.device_name + ': ' + KorgKaossPad3PlusLooperMux.__sync_daw_transport.__name__)
        transport.setSongPos(0.0)

    def __on_midi_msg_processing(self, event):

        # fl_helper.print_midi_event(event)

        if event.data1 == constants.MIDI_CC_TRACK_1_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.add_pressed_sampler_button(PressedSamplerButton.A_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_1_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_RELEASED:
            self.removepressed_sampler_button(PressedSamplerButton.A_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_2_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.add_pressed_sampler_button(PressedSamplerButton.B_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_2_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_RELEASED:
            self.removepressed_sampler_button(PressedSamplerButton.B_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_3_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.add_pressed_sampler_button(PressedSamplerButton.C_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_3_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_RELEASED:
            self.removepressed_sampler_button(PressedSamplerButton.C_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_4_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.add_pressed_sampler_button(PressedSamplerButton.D_PRESSED)
        elif event.data1 == constants.MIDI_CC_TRACK_4_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_RELEASED:
            self.removepressed_sampler_button(PressedSamplerButton.D_PRESSED)

        if True == fl_helper.is_kp3_program_change_event(event):
            self.__sync_daw_transport()
        elif event.data1 == constants.MIDI_CC_LOOPER_VOLUME and self.get_shift_pressed_state():
            self.set_drop_intencity( (fl_helper.MIDI_MAX_VALUE - event.data2) / fl_helper.MIDI_MAX_VALUE )
        elif event.data1 == constants.MIDI_CC_RESAMPLE_MODE_FROM_LOOPER_TO_TRACK and self.get_shift_pressed_state():
            self.set_resample_mode(ResampleMode.FROM_LOOPER_TO_TRACK)

            action = lambda self = self: ( self.set_resample_mode(ResampleMode.NONE), \
                                           self.switch_to_prev_turnado_preset())
            self.action_on_double_click(constants.MIDI_CC_RESAMPLE_MODE_FROM_LOOPER_TO_TRACK + constants.SHIFT_BUTTON_ON_DOUBLE_CLICK_SHIFT, action)

        elif event.data1 == constants.MIDI_CC_RESAMPLE_MODE_FROM_ALL_LOOPERS_TO_TRACK and self.get_shift_pressed_state():
            self.set_resample_mode(ResampleMode.FROM_ALL_LOOPERS_TO_TRACK)

            action = lambda self = self: ( self.set_resample_mode(ResampleMode.NONE), \
                                           self.switch_to_next_turnado_preset())
            self.action_on_double_click(constants.MIDI_CC_RESAMPLE_MODE_FROM_ALL_LOOPERS_TO_TRACK + constants.SHIFT_BUTTON_ON_DOUBLE_CLICK_SHIFT, action)
        elif event.data1 == constants.MIDI_CC_LOOPER_1 and self.get_shift_pressed_state():
            self.select_looper(constants.Looper_1)
            self.action_on_double_click(constants.SHIFT_BUTTON_ON_DOUBLE_CLICK_SHIFT + constants.MIDI_CC_SAMPLE_LENGTH_1, self.drop)
        elif event.data1 == constants.MIDI_CC_LOOPER_2 and self.get_shift_pressed_state():
            self.select_looper(constants.Looper_2)
        elif event.data1 == constants.MIDI_CC_LOOPER_3 and self.get_shift_pressed_state():
            self.select_looper(constants.Looper_3)
        elif event.data1 == constants.MIDI_CC_LOOPER_4 and self.get_shift_pressed_state():
            self.select_looper(constants.Looper_4)
        elif event.data1 == constants.MIDI_CC_CLEAR_LOOPER and self.get_shift_pressed_state():
            action = lambda self = self: ( self.clear_current_looper() )
            self.action_on_double_click(constants.MIDI_CC_CLEAR_LOOPER, action)
        elif event.data1 == constants.MIDI_CC_PLAY_STOP and self.get_shift_pressed_state():
            action = lambda self = self: ( self.play_stop() )
            self.action_on_double_click(constants.MIDI_CC_PLAY_STOP, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_1:
            self.set_sample_length(SampleLength.LENGTH_1)
            action = lambda self = self: self.turn_looper_on_off(constants.Looper_1)
            self.action_on_double_click(constants.MIDI_CC_SAMPLE_LENGTH_1, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_2:
            self.set_sample_length(SampleLength.LENGTH_2)
            action = lambda self = self: self.turn_looper_on_off(constants.Looper_2)
            self.action_on_double_click(constants.MIDI_CC_SAMPLE_LENGTH_2, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_4:
            self.set_sample_length(SampleLength.LENGTH_4)
            action = lambda self = self: self.turn_looper_on_off(constants.Looper_3)
            self.action_on_double_click(constants.MIDI_CC_SAMPLE_LENGTH_4, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_8:
            self.set_sample_length(SampleLength.LENGTH_8)
            action = lambda self = self: self.turn_looper_on_off(constants.Looper_4)
            self.action_on_double_click(constants.MIDI_CC_SAMPLE_LENGTH_8, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_16:
            self.set_sample_length(SampleLength.LENGTH_16)
            action = lambda self = self: self.turn_track_on_off(constants.Track_1)
            self.action_on_double_click(constants.MIDI_CC_SAMPLE_LENGTH_16, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_32:
            self.set_sample_length(SampleLength.LENGTH_32)
            action = lambda self = self: self.turn_track_on_off(constants.Track_2)
            self.action_on_double_click(constants.MIDI_CC_SAMPLE_LENGTH_32, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_64:
            self.set_sample_length(SampleLength.LENGTH_64)
            action = lambda self = self: self.turn_track_on_off(constants.Track_3)
            self.action_on_double_click(constants.MIDI_CC_SAMPLE_LENGTH_64, action)
        elif event.data1 == constants.MIDI_CC_SAMPLE_LENGTH_128:
            self.set_sample_length(SampleLength.LENGTH_128)
            action = lambda self = self: self.turn_track_on_off(constants.Track_4)
            self.action_on_double_click(constants.MIDI_CC_SAMPLE_LENGTH_128, action)
        elif event.data1 == constants.MIDI_CC_TRACK_1_CLEAR and event.data2 == constants.KP3_PLUS_ABCD_PRESSED and self.get_shift_pressed_state():
            self.clear_track(constants.Track_1)
        elif event.data1 == constants.MIDI_CC_TRACK_2_CLEAR and event.data2 == constants.KP3_PLUS_ABCD_PRESSED and self.get_shift_pressed_state():
            self.clear_track(constants.Track_2)
        elif event.data1 == constants.MIDI_CC_TRACK_3_CLEAR and event.data2 == constants.KP3_PLUS_ABCD_PRESSED and self.get_shift_pressed_state():
            self.clear_track(constants.Track_3)
        elif event.data1 == constants.MIDI_CC_TRACK_4_CLEAR and event.data2 == constants.KP3_PLUS_ABCD_PRESSED and self.get_shift_pressed_state():
            self.clear_track(constants.Track_4)
        elif event.data1 == constants.MIDI_CC_SHIFT:
            self.set_shift_pressed_state(event.data2 == fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TURNADO_DRY_WET and self.get_shift_pressed_state():
            self.set_turnado_dry_wet_level(event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_LOOPER_VOLUME:
            self.set_looper_volume((event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_1 and True == self.get_shift_pressed_state():
            self.set_tension_side_chain_level(constants.Track_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_2 and True == self.get_shift_pressed_state():
            self.set_decay_side_chain_level(constants.Track_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_3 and True == self.get_shift_pressed_state():
            self.set_tension_side_chain_level(constants.Track_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_4 and True == self.get_shift_pressed_state():
            self.set_decay_side_chain_level(constants.Track_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_1:
            self.set_track_volume(0, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_2:
            self.set_track_volume(1, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_3:
            self.set_track_volume(2, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_VOLUME_4:
            self.set_track_volume(3, (event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
        elif event.data1 == constants.MIDI_CC_TRACK_1_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.change_recording_state(constants.Track_1)
        elif event.data1 == constants.MIDI_CC_TRACK_2_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.change_recording_state(constants.Track_2)
        elif event.data1 == constants.MIDI_CC_TRACK_3_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
            self.change_recording_state(constants.Track_3)
        elif event.data1 == constants.MIDI_CC_TRACK_4_SAMPLING and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
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

        #fl_helper.print_all_plugin_parameters(LOOPER_1_CHANNEL, LOOPER_TURNADO_SLOT_INDEX)

        event.handled = False

        if not self.is_playing():
            if event.data1 == constants.MIDI_CC_TEMPO and not self.is_playing():
                self.set_tempo(800 + int((event.data2 / fl_helper.MIDI_MAX_VALUE) * 1000.0)) # from 80 to 180
            else:
                if ( not ( event.data1 == constants.MIDI_CC_SHIFT and event.data2 == 0 ) \
                and ( not ( event.data1 == constants.MIDI_CC_PLAY_STOP and self.get_shift_pressed_state() ) ) ):
                    self.play_stop()

                self.__on_midi_msg_processing(event)
        else:
            self.__on_midi_msg_processing(event)

        event.handled = True
