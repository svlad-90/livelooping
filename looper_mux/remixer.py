'''
Created on Oct 20, 2024

@author: Dream Machines
'''

import midi
import plugins
import channels
import mixer

import time

from enum import Enum
from common import fl_helper, global_constants
from looper_mux import constants
from looper_mux import view
from common import updateable

class RemixerFXUnit:
    def __init__(self, view):
        self._view = view
        self.__pitch_shift_dry_wet_level = fl_helper.MAX_LEVEL_VALUE
        self.__distortion_level = fl_helper.MIN_LEVEL_VALUE
        self.__distortion_dry_wet_level = fl_helper.MAX_LEVEL_VALUE
        self.__volume_level = global_constants.DEFAULT_PANOMATIC_VOLUME_LEVEL
        self.__pan = global_constants.DEFAULT_PANOMATIC_PAN_LEVEL
        self.__pitch_shift_level = fl_helper.MAX_LEVEL_VALUE / 2

    def on_init_script(self):
        self._update_all_fx_parameters()

    def set_pitch_shift_level(self, level, forward_to_device):
        self.stop_play_all_slots()
        self.__pitch_shift_level = level
        self._view.set_remixer_fx_unit_pitch_shift_level(level, forward_to_device)

    def reset_pitch_shift_level(self):
        self.set_pitch_shift_level(global_constants.DEFAULT_PANOMATIC_PAN_LEVEL, True)

    def set_pitch_shift_dry_wet_level(self, level, forward_to_device):
        pass

    def reset_pitch_shift_dry_wet_level(self):
        pass

    def set_distortion_level(self, level, forward_to_device):
        pass

    def reset_distortion_level(self):
        pass

    def set_distortion_dry_wet_level(self, level, forward_to_device):
        pass

    def reset_distortion_dry_wet_level(self):
        pass

    def set_volume_level(self, level, forward_to_device):
        pass

    def reset_volume_level(self):
        pass

    def set_pan_level(self, level, forward_to_device):
        pass

    def reset_pan_level(self):
        pass

    def reverse_clicked(self):
        pass

    def reverse_released(self):
        pass

    def reverb_clicked(self):
        pass

    def reverb_released(self):
        pass

    def delay_clicked(self):
        pass

    def delay_released(self):
        pass

    def phaser_clicked(self):
        pass

    def phaser_released(self):
        pass

    def stereo_enhancer_clicked(self):
        pass

    def stereo_enhancer_released(self):
        pass


    def reset_fx_parameters(self):
        self.reset_pitch_shift_level()

    def _update_all_fx_parameters(self):
        self._view.set_remixer_fx_unit_pitch_shift_level(self.__pitch_shift_level, True)

    def _get_note(self):
        return int(constants.DEFAULT_REMIXER_NOTE + ( ( -0.5 + self.__pitch_shift_level ) * 2 * 12 ))

class RemixerSlotStatus(Enum):
    NOT_RECORDED = 0
    RECORDING = 1
    RECORDED = 2
    PLAYBACK = 3

class RemixerOneShotSlot:
    def __init__(self,
                 view,
                 slot_number,
                 mixer_channel,
                 mixer_slot,
                 record_on_off_parameter_index,
                 volume_parameter_index,
                 dry_level_parameter_index,
                 first_slot_channel,
                 note_provider):
        self.__view = view
        self.__slot_number = slot_number
        self.__mixer_channel = mixer_channel
        self.__mixer_slot = mixer_slot
        self.__record_on_off_parameter_index = record_on_off_parameter_index
        self.__volume_parameter_index = volume_parameter_index
        self.__dry_level_parameter_index = dry_level_parameter_index
        self.__status = RemixerSlotStatus.NOT_RECORDED
        self.__first_slot_channel = first_slot_channel
        self.__note_provider = note_provider

    def __set_status(self, status):
        self.__status = status
        self.update_recording_status()

    def update_recording_status(self):
        if self.__status == RemixerSlotStatus.NOT_RECORDED:
            view_status = view.View.ONESHOT_SAMPLER_STATUS_OFF
        elif self.__status == RemixerSlotStatus.RECORDING:
            view_status = view.View.ONESHOT_SAMPLER_STATUS_RECORDING
        elif self.__status == RemixerSlotStatus.RECORDED:
            view_status = view.View.ONESHOT_SAMPLER_STATUS_RECORDED
        elif self.__status == RemixerSlotStatus.PLAYBACK:
            view_status = view.View.ONESHOT_SAMPLER_STATUS_PLAYBACK

        self.__view.set_remixer_slot_state(self.__slot_number, view_status)

    def reset_recording_status(self):
        self.__set_status(RemixerSlotStatus.NOT_RECORDED)

    def on_init_script(self):
        self.__set_dry_level(fl_helper.MIN_LEVEL_VALUE)
        self.__set_volume_level(fl_helper.MAX_LEVEL_VALUE / 2)
        self.__set_status(RemixerSlotStatus.NOT_RECORDED)

    def __set_volume_level(self, volume_level):
        plugins.setParamValue(volume_level,
                              self.__volume_parameter_index,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)

    def __set_dry_level(self, dry_level):
        plugins.setParamValue(dry_level,
                              self.__dry_level_parameter_index,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)

    def start_recording(self):
        plugins.setParamValue(fl_helper.MAX_LEVEL_VALUE,
                              self.__record_on_off_parameter_index,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)
        self.__set_status(RemixerSlotStatus.RECORDING)

    def stop_recording(self):
        self.__set_dry_level(fl_helper.MIN_LEVEL_VALUE)
        plugins.setParamValue(fl_helper.MIN_LEVEL_VALUE,
                              self.__record_on_off_parameter_index,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)
        self.__set_status(RemixerSlotStatus.RECORDED)

    def status(self):
        return self.__status

    def playback_start(self):
        channels.midiNoteOn( self.__first_slot_channel + self.__slot_number, self.__note_provider(), fl_helper.MIDI_MAX_VALUE )
        self.__set_status(RemixerSlotStatus.PLAYBACK)

    def playback_stop(self):
        channels.midiNoteOn( self.__first_slot_channel + self.__slot_number, self.__note_provider(), fl_helper.MIDI_MIN_VALUE )
        self.__set_status(RemixerSlotStatus.RECORDED)

class RemixerOneshotSampler(RemixerFXUnit):

    CLEAR_MODE_OFF = 0
    CLEAR_MODE_ON = 1

    def __init__(self, view, updateable_mux, mixer_channel, mixer_slot, first_slot_channel):
        super().__init__(view)
        self.__updateable_mux = updateable_mux
        self.__mixer_channel = mixer_channel
        self.__mixer_slot = mixer_slot
        self.__one_shot_slots = []
        self.__clear_mode = RemixerOneshotSampler.CLEAR_MODE_OFF
        self.__clear_handler = updateable.DoubleClickTimeoutHandler(self.__handle_clear_first_click,
                                                                         self.__handle_clear_first_release,
                                                                         self.__handle_clear_second_click,
                                                                         self.__handle_clear_second_release,
                                                                         self.__handle_clear_timeout,
                                                                         0.3)

        self.__updateable_mux.add_updateable(self.__clear_handler)
        self.__first_slot_channel = first_slot_channel

    def on_init_script(self):
        super().on_init_script()
        self.__one_shot_slots.append(RemixerOneShotSlot(self._view,
                                                 constants.RemixerSlot_1,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_1_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_1_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_1_DRY_LEVEL_PARAMETER_INDEX,
                                                 self.__first_slot_channel,
                                                 self._get_note))

        self.__one_shot_slots.append(RemixerOneShotSlot(self._view,
                                                 constants.RemixerSlot_2,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_2_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_2_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_2_DRY_LEVEL_PARAMETER_INDEX,
                                                 self.__first_slot_channel,
                                                 self._get_note))

        self.__one_shot_slots.append(RemixerOneShotSlot(self._view,
                                                 constants.RemixerSlot_3,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_3_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_3_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_3_DRY_LEVEL_PARAMETER_INDEX,
                                                 self.__first_slot_channel,
                                                 self._get_note))

        self.__one_shot_slots.append(RemixerOneShotSlot(self._view,
                                                 constants.RemixerSlot_4,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_4_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_4_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_4_DRY_LEVEL_PARAMETER_INDEX,
                                                 self.__first_slot_channel,
                                                 self._get_note))

        self.__one_shot_slots.append(RemixerOneShotSlot(self._view,
                                                 constants.RemixerSlot_5,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_5_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_5_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_5_DRY_LEVEL_PARAMETER_INDEX,
                                                 self.__first_slot_channel,
                                                 self._get_note))

        self.__one_shot_slots.append(RemixerOneShotSlot(self._view,
                                                 constants.RemixerSlot_6,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_6_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_6_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_6_DRY_LEVEL_PARAMETER_INDEX,
                                                 self.__first_slot_channel,
                                                 self._get_note))

        self.__one_shot_slots.append(RemixerOneShotSlot(self._view,
                                                 constants.RemixerSlot_7,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_7_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_7_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_7_DRY_LEVEL_PARAMETER_INDEX,
                                                 self.__first_slot_channel,
                                                 self._get_note))

        self.__one_shot_slots.append(RemixerOneShotSlot(self._view,
                                                 constants.RemixerSlot_8,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_8_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_8_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_8_DRY_LEVEL_PARAMETER_INDEX,
                                                 self.__first_slot_channel,
                                                 self._get_note))

        for one_shot_slot in self.__one_shot_slots:
            one_shot_slot.on_init_script()

        self._update_all_fx_parameters()

    def activate(self):
        mixer.setRouteToLevel(self.__mixer_channel, constants.REMIXER_FX_1_MIXER_CHANNEL, fl_helper.MAX_VOLUME_LEVEL_VALUE)
        for slot in self.__one_shot_slots:
            slot.update_recording_status()
        self._update_all_fx_parameters()

    def deactivate(self):
        mixer.setRouteToLevel(self.__mixer_channel, constants.REMIXER_FX_1_MIXER_CHANNEL, fl_helper.MIN_LEVEL_VALUE)

    def clear_click(self):
        self.__clear_handler.click()

    def clear_release(self):
        self.__clear_handler.release()

    def slot_click(self, remixer_slot_index):
        if not self.__get_clear_mode():
            if self.__status(remixer_slot_index) == RemixerSlotStatus.NOT_RECORDED:
                self.__start_recording(remixer_slot_index)
            elif self.__status(remixer_slot_index) == RemixerSlotStatus.RECORDED:
                self.__playback_start(remixer_slot_index)
        else:
            self.__reset_recording_status(remixer_slot_index)

    def slot_release(self, remixer_slot_index):
        if not self.__get_clear_mode():
            if self.__status(remixer_slot_index) == RemixerSlotStatus.RECORDING:
                self.__stop_recording(remixer_slot_index)
            elif self.__status(remixer_slot_index) == RemixerSlotStatus.PLAYBACK:
                self.__playback_stop(remixer_slot_index)

    def stop_play_all_slots(self):
        for slot_id in range(constants.RemixerSlot_1, constants.RemixerSlot_8 + 1):
            self.slot_release(slot_id)

    def __handle_clear_first_click(self):
        self.__clear_mode = RemixerOneshotSampler.CLEAR_MODE_ON
        self._view.set_remixer_clear_button_state(updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_DONE)

    def __handle_clear_first_release(self):
        self.__clear_mode = RemixerOneshotSampler.CLEAR_MODE_OFF
        self._view.set_remixer_clear_button_state(updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_RELEASED)

    def __handle_clear_second_click(self):
        self.__reset_all_recording_statuses()
        self._view.set_remixer_clear_button_state(updateable.DoubleClickTimeoutHandler.STATE_SECOND_CLICK_DONE)

    def __handle_clear_second_release(self):
        self._view.set_remixer_clear_button_state(updateable.DoubleClickTimeoutHandler.STATE_INITITAL)

    def __handle_clear_timeout(self):
        self._view.set_remixer_clear_button_state(updateable.DoubleClickTimeoutHandler.STATE_INITITAL)

    def __start_recording(self, remixer_slot_index):
        self.__one_shot_slots[remixer_slot_index].start_recording()

    def __stop_recording(self, remixer_slot_index):
        self.__one_shot_slots[remixer_slot_index].stop_recording()

    def __playback_start(self, remixer_slot_index):
        self.__one_shot_slots[remixer_slot_index].playback_start()

    def __playback_stop(self, remixer_slot_index):
        self.__one_shot_slots[remixer_slot_index].playback_stop()

    def __status(self, remixer_slot_index):
        return self.__one_shot_slots[remixer_slot_index].status()

    def __reset_all_recording_statuses(self):
        for slot in self.__one_shot_slots:
            slot.reset_recording_status()

    def __reset_recording_status(self, remixer_slot_index):
        self.__one_shot_slots[remixer_slot_index].reset_recording_status()

    def __get_clear_mode(self):
        return self.__clear_mode

    def sync_daw_transport_click(self):
        pass

    def sync_daw_transport_release(self):
        pass

class RemixerTape(RemixerFXUnit):

    def __init__(self, view,
                 mixer_channel,
                 mixer_slot,
                 record_on_off_parameter_index,
                 volume_parameter_index,
                 dry_level_parameter_index,
                 channel_slot_number,
                 mute_looper_provider,
                 looper):
        super().__init__(view)
        self.__mixer_channel = mixer_channel
        self.__mixer_slot = mixer_slot
        self.__record_on_off_parameter_index = record_on_off_parameter_index
        self.__volume_parameter_index = volume_parameter_index
        self.__dry_level_parameter_index = dry_level_parameter_index
        self.__channel_slot_number = channel_slot_number
        self.__mute_looper_provider = mute_looper_provider
        self.__looper = looper
        self.__tape_recording_status = False
        self.__number_of_pressed_buttons = 0
        self.__first_playback = False

    def __set_playback_status(self, slot_index, status):
        if status == RemixerSlotStatus.NOT_RECORDED:
            view_status = view.View.ONESHOT_SAMPLER_STATUS_OFF
        elif status == RemixerSlotStatus.RECORDING:
            view_status = view.View.ONESHOT_SAMPLER_STATUS_RECORDING
        elif status == RemixerSlotStatus.RECORDED:
            view_status = view.View.ONESHOT_SAMPLER_STATUS_RECORDED
        elif status == RemixerSlotStatus.PLAYBACK:
            view_status = view.View.ONESHOT_SAMPLER_STATUS_PLAYBACK

        self._view.set_remixer_slot_state(slot_index, view_status)

    def on_init_script(self):
        super().on_init_script()
        self.__set_dry_level(fl_helper.MIN_LEVEL_VALUE)
        self.__set_volume_level(fl_helper.MAX_LEVEL_VALUE / 2)
        self.__reset_parameters()
        self.__set_tape_recording_status(True)
        self._update_all_fx_parameters()

    def activate(self):
        self.__set_tape_recording_status(False)
        mixer.setRouteToLevel(self.__mixer_channel, constants.REMIXER_FX_1_MIXER_CHANNEL, fl_helper.MAX_VOLUME_LEVEL_VALUE)

        for slot_id in range(constants.RemixerSlot_1, constants.RemixerSlot_8+1):
            self.__set_playback_status(slot_id, RemixerSlotStatus.RECORDED)
        self.__first_playback = True
        self._update_all_fx_parameters()

    def deactivate(self):
        self.__reset_parameters()
        self.__set_tape_recording_status(True)
        self.__playback_stop()
        self.__first_playback = True

    def clear_click(self):
        pass

    def clear_release(self):
        pass

    def slot_click(self, remixer_slot_index):
        self.__move_to_part(remixer_slot_index)
        time.sleep(0.015)
        self.__playback_start()
        self.__number_of_pressed_buttons += 1
        self.__set_playback_status(remixer_slot_index, RemixerSlotStatus.PLAYBACK)

        if self.__first_playback == True:
            if self.__mute_looper_provider:
                self.__mute_looper_provider(self.__looper)
            self.__first_playback = False

    def slot_release(self, remixer_slot_index):
        self.__number_of_pressed_buttons -= 1
        if self.__number_of_pressed_buttons == 0:
            self.__playback_stop()
        self.__set_playback_status(remixer_slot_index, RemixerSlotStatus.RECORDED)

    def __move_to_part(self, remixer_slot_index):
        plugins.setParamValue(1 / constants.REMIXER_NUMBER_OF_SLOTS * remixer_slot_index,
                              constants.CROSSFADE_LOOP_SYNTH_PLAY_POSITION_PARAM_INDEX,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)

    def __playback_start(self):
        channels.midiNoteOn( self.__channel_slot_number, self._get_note(), fl_helper.MIDI_MAX_VALUE )

    def __playback_stop(self):
        channels.midiNoteOn( self.__channel_slot_number, self._get_note(), fl_helper.MIDI_MIN_VALUE )
        self.__number_of_pressed_buttons = 0


    def __reset_parameters(self):
        plugins.setParamValue(0.33333,
                      constants.CROSSFADE_LOOP_SYNTH_RECORD_MODE_PARAM_INDEX,
                      self.__mixer_channel,
                      self.__mixer_slot,
                      midi.PIM_None, True)
        plugins.setParamValue(0.4,
                              constants.CROSSFADE_LOOP_SYNTH_BEAT_DIVISOR_PARAM_INDEX,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)
        plugins.setParamValue(0.1111,
                              constants.CROSSFADE_LOOP_SYNTH_BEATS_PARAM_INDEX,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)
        plugins.setParamValue(0.0,
                              constants.CROSSFADE_LOOP_SYNTH_ATTACK_PARAM_INDEX,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)
        plugins.setParamValue(1.0,
                              constants.CROSSFADE_LOOP_SYNTH_DECAY_PARAM_INDEX,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)
        plugins.setParamValue(1.0,
                              constants.CROSSFADE_LOOP_SYNTH_SUSTAIN_PARAM_INDEX,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)
        plugins.setParamValue(0.01,
                              constants.CROSSFADE_LOOP_SYNTH_RELEASE_PARAM_INDEX,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)
        plugins.setParamValue(0.6666,
                              constants.CROSSFADE_LOOP_SYNTH_USE_BEATS_PARAM_INDEX,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)
        plugins.setParamValue(0.0,
                              constants.CROSSFADE_LOOP_SYNTH_CROSSFADE_PARAM_INDEX,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)

    def __set_tape_recording_status(self, status):
        self.__tape_recording_status = status
        plugins.setParamValue(fl_helper.MAX_LEVEL_VALUE if status else 0.0,
                              self.__record_on_off_parameter_index,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)

    def __set_volume_level(self, volume_level):
        plugins.setParamValue(volume_level,
                              self.__volume_parameter_index,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)

    def __set_dry_level(self, dry_level):
        plugins.setParamValue(dry_level,
                              self.__dry_level_parameter_index,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)

    def sync_daw_transport_click(self):
        self.__set_tape_recording_status(False)

    def sync_daw_transport_release(self):
        self.__set_tape_recording_status(True)        

    def stop_play_all_slots(self):
        for slot_id in range(constants.RemixerSlot_1, constants.RemixerSlot_8 + 1):
            self.slot_release(slot_id)

class RemixerManager:

    def __init__(self, view, updateable_mux, mute_looper_provider):
        self.__updateable_mux = updateable_mux
        self.__view = view
        self.__remixer_units = {constants.RemixerUnitType.MIC: RemixerOneshotSampler(self.__view, self.__updateable_mux,
                                                                           constants.REMIXER_MIC_MIXER_CHANNEL,
                                                                           constants.REMIXER_MIC_MIXER_SLOT,
                                                                           constants.REMIXER_UNIT_MIC_FIRST_SLOT_CHANNEL),
                                constants.RemixerUnitType.SYNTH: RemixerOneshotSampler( self.__view, self.__updateable_mux,
                                                                    constants.REMIXER_SYNTH_MIXER_CHANNEL,
                                                                    constants.REMIXER_SYNTH_MIXER_SLOT,
                                                                    constants.REMIXER_UNIT_SYNTH_FIRST_SLOT_CHANNEL),
                                constants.RemixerUnitType.LOOPER_1: RemixerTape(self.__view,
                                                                                constants.REMIXER_LOOPER_1_MIXER_CHANNEL,
                                                                                constants.REMIXER_LOOPER_1_MIXER_SLOT,
                                                                                constants.CROSSFADE_LOOP_SYNTH_RECORD_PARAM_INDEX,
                                                                                constants.CROSSFADE_LOOP_SYNTH_VOLUME_PARAM_INDEX,
                                                                                constants.CROSSFADE_LOOP_SYNTH_DRY_WET_PARAM_INDEX,
                                                                                constants.REMIXER_LOOPER_1_INPUT_CHANNEL,
                                                                                mute_looper_provider,
                                                                                constants.Looper_1),
                                constants.RemixerUnitType.LOOPER_2: RemixerTape(self.__view,
                                                                                constants.REMIXER_LOOPER_2_MIXER_CHANNEL,
                                                                                constants.REMIXER_LOOPER_2_MIXER_SLOT,
                                                                                constants.CROSSFADE_LOOP_SYNTH_RECORD_PARAM_INDEX,
                                                                                constants.CROSSFADE_LOOP_SYNTH_VOLUME_PARAM_INDEX,
                                                                                constants.CROSSFADE_LOOP_SYNTH_DRY_WET_PARAM_INDEX,
                                                                                constants.REMIXER_LOOPER_2_INPUT_CHANNEL,
                                                                                mute_looper_provider,
                                                                                constants.Looper_2),
                                constants.RemixerUnitType.LOOPER_3: RemixerTape(self.__view,
                                                                                constants.REMIXER_LOOPER_3_MIXER_CHANNEL,
                                                                                constants.REMIXER_LOOPER_3_MIXER_SLOT,
                                                                                constants.CROSSFADE_LOOP_SYNTH_RECORD_PARAM_INDEX,
                                                                                constants.CROSSFADE_LOOP_SYNTH_VOLUME_PARAM_INDEX,
                                                                                constants.CROSSFADE_LOOP_SYNTH_DRY_WET_PARAM_INDEX,
                                                                                constants.REMIXER_LOOPER_3_INPUT_CHANNEL,
                                                                                mute_looper_provider,
                                                                                constants.Looper_3),
                                constants.RemixerUnitType.LOOPER_4: RemixerTape(self.__view,
                                                                                constants.REMIXER_LOOPER_4_MIXER_CHANNEL,
                                                                                constants.REMIXER_LOOPER_4_MIXER_SLOT,
                                                                                constants.CROSSFADE_LOOP_SYNTH_RECORD_PARAM_INDEX,
                                                                                constants.CROSSFADE_LOOP_SYNTH_VOLUME_PARAM_INDEX,
                                                                                constants.CROSSFADE_LOOP_SYNTH_DRY_WET_PARAM_INDEX,
                                                                                constants.REMIXER_LOOPER_4_INPUT_CHANNEL,
                                                                                mute_looper_provider,
                                                                                constants.Looper_4),
                                constants.RemixerUnitType.LOOPERS_ALL: RemixerTape(self.__view,
                                                                                   constants.REMIXER_ALL_LOOPERS_MIXER_CHANNEL,
                                                                                   constants.REMIXER_ALL_LOOPERS_MIXER_SLOT,
                                                                                   constants.CROSSFADE_LOOP_SYNTH_RECORD_PARAM_INDEX,
                                                                                   constants.CROSSFADE_LOOP_SYNTH_VOLUME_PARAM_INDEX,
                                                                                   constants.CROSSFADE_LOOP_SYNTH_DRY_WET_PARAM_INDEX,
                                                                                   constants.REMIXER_LOOPERS_ALL_INPUT_CHANNEL,
                                                                                   mute_looper_provider,
                                                                                   constants.LoopersAll)}
        self.__current_active_unit = constants.RemixerUnitType.NONE
        self.__reset_handler = updateable.DoubleClickTimeoutHandler(self.__handle_reset_first_click,
                                                                         self.__handle_reset_first_release,
                                                                         self.__handle_reset_second_click,
                                                                         self.__handle_reset_second_release,
                                                                         self.__handle_reset_timeout,
                                                                         0.3)

    def __handle_reset_first_click(self):
        self.__view.set_remixer_fx_unit_reset_fx_params_btn_state(updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_DONE)

    def __handle_reset_first_release(self):
        self.__view.set_remixer_fx_unit_reset_fx_params_btn_state(updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_RELEASED)

    def __handle_reset_second_click(self):
        self.__remixer_units[self.__current_active_unit].reset_fx_parameters()
        self.__view.set_remixer_fx_unit_reset_fx_params_btn_state(updateable.DoubleClickTimeoutHandler.STATE_SECOND_CLICK_DONE)

    def __handle_reset_second_release(self):
        self.__view.set_remixer_fx_unit_reset_fx_params_btn_state(updateable.DoubleClickTimeoutHandler.STATE_INITITAL)

    def __handle_reset_timeout(self):
        self.__view.set_remixer_fx_unit_reset_fx_params_btn_state(updateable.DoubleClickTimeoutHandler.STATE_INITITAL)

    def on_init_script(self):

        for remixer_unit in self.__remixer_units.values():
            remixer_unit.on_init_script()

        self.activate_unit(constants.RemixerUnitType.MIC)
        self.__view.set_remixer_fx_unit_reset_fx_params_btn_state(updateable.DoubleClickTimeoutHandler.STATE_INITITAL)

    def activate_unit(self, unit_id):
        if unit_id != self.__current_active_unit:
            if self.__current_active_unit != constants.RemixerUnitType.NONE:
                self.__remixer_units[self.__current_active_unit].deactivate()

            self.__current_active_unit = unit_id
            self.__remixer_units[self.__current_active_unit].activate()
            self.__view.activate_remixer_unit(int(self.__current_active_unit))

    def clear_click(self):
        self.__remixer_units[self.__current_active_unit].clear_click()

    def clear_release(self):
        self.__remixer_units[self.__current_active_unit].clear_release()

    def slot_click(self, remixer_slot_index):
        self.__remixer_units[self.__current_active_unit].slot_click(remixer_slot_index)

    def slot_release(self, remixer_slot_index):
        self.__remixer_units[self.__current_active_unit].slot_release(remixer_slot_index)

    def set_pitch_shift_level(self, level, forward_to_device):
        self.__remixer_units[self.__current_active_unit].set_pitch_shift_level(level, forward_to_device)

    def reset_pitch_shift_level(self):
        self.__remixer_units[self.__current_active_unit].reset_pitch_shift_level()

    def set_pitch_shift_dry_wet_level(self, level, forward_to_device):
        self.__remixer_units[self.__current_active_unit].set_pitch_shift_dry_wet_level(level, forward_to_device)

    def reset_pitch_shift_dry_wet_level(self):
        self.__remixer_units[self.__current_active_unit].reset_pitch_shift_dry_wet_level()

    def set_distortion_level(self, level, forward_to_device):
        self.__remixer_units[self.__current_active_unit].set_distortion_level(level, forward_to_device)

    def reset_distortion_level(self):
        self.__remixer_units[self.__current_active_unit].reset_distortion_level()

    def set_distortion_dry_wet_level(self, level, forward_to_device):
        self.__remixer_units[self.__current_active_unit].set_distortion_dry_wet_level(level, forward_to_device)

    def reset_distortion_dry_wet_level(self):
        self.__remixer_units[self.__current_active_unit].reset_distortion_dry_wet_level()

    def set_volume_level(self, level, forward_to_device):
        self.__remixer_units[self.__current_active_unit].set_volume_level(level, forward_to_device)

    def reset_volume_level(self):
        self.__remixer_units[self.__current_active_unit].reset_volume_level()

    def set_pan_level(self, level, forward_to_device):
        self.__remixer_units[self.__current_active_unit].set_pan_level(level, forward_to_device)

    def reset_pan_level(self):
        self.__remixer_units[self.__current_active_unit].reset_pan_level()

    def reverse_clicked(self):
        self.__remixer_units[self.__current_active_unit].reverse_clicked()

    def reverse_released(self):
        self.__remixer_units[self.__current_active_unit].reverse_released()

    def reverb_clicked(self):
        self.__remixer_units[self.__current_active_unit].reverb_clicked()

    def reverb_released(self):
        self.__remixer_units[self.__current_active_unit].reverb_released()

    def delay_clicked(self):
        self.__remixer_units[self.__current_active_unit].delay_clicked()

    def delay_released(self):
        self.__remixer_units[self.__current_active_unit].delay_released()

    def phaser_clicked(self):
        self.__remixer_units[self.__current_active_unit].phaser_clicked()

    def phaser_released(self):
        self.__remixer_units[self.__current_active_unit].phaser_released()

    def stereo_enhancer_clicked(self):
        self.__remixer_units[self.__current_active_unit].stereo_enhancer_clicked()

    def stereo_enhancer_released(self):
        self.__remixer_units[self.__current_active_unit].stereo_enhancer_released()

    def reset_fx_parameters_clicked(self):
        self.__reset_handler.click()

    def reset_fx_parameters_released(self):
        self.__reset_handler.release()

    def reset_all_fx_parameters(self):
        for remixer_unit in self.__remixer_units.values():
            remixer_unit.reset_fx_parameters()

    def sync_daw_transport_click(self):
        for remixer_unit in self.__remixer_units.values():
            remixer_unit.sync_daw_transport_click()

    def sync_daw_transport_release(self):
        for remixer_unit in self.__remixer_units.values():
            remixer_unit.sync_daw_transport_release()