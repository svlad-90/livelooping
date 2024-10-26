'''
Created on Oct 20, 2024

@author: Dream Machines
'''

import midi
import plugins
import channels

from enum import Enum
from common import fl_helper
from looper_mux import constants
from looper_mux import view
from common import updateable

class OneShotSlotStatus(Enum):
    NOT_RECORDED = 0
    RECORDING = 1
    RECORDED = 2

class OneShotSlot:
    def __init__(self,
                 view,
                 slot_number,
                 mixer_channel,
                 mixer_slot,
                 record_on_off_parameter_index,
                 volume_parameter_index,
                 dry_level_parameter_index):
        self.__view = view
        self.__slot_number = slot_number
        self.__mixer_channel = mixer_channel
        self.__mixer_slot = mixer_slot
        self.__record_on_off_parameter_index = record_on_off_parameter_index
        self.__volume_parameter_index = volume_parameter_index
        self.__dry_level_parameter_index = dry_level_parameter_index
        self.__status = OneShotSlotStatus.NOT_RECORDED

    def __set_status(self, status):
        self.__status = status

        if status == OneShotSlotStatus.NOT_RECORDED:
            view_status = view.View.ONESHOT_SAMPLER_STATUS_OFF
        elif status == OneShotSlotStatus.RECORDING:
            view_status = view.View.ONESHOT_SAMPLER_STATUS_RECORDING
        elif status == OneShotSlotStatus.RECORDED:
            view_status = view.View.ONESHOT_SAMPLER_STATUS_RECORDED

        self.__view.set_remixer_slot_state(self.__slot_number, view_status)

    def reset_recording_status(self):
        self.__set_status(OneShotSlotStatus.NOT_RECORDED)

    def on_init_script(self):
        self.__set_dry_level(fl_helper.MIN_LEVEL_VALUE)
        self.__set_volume_level(fl_helper.MAX_LEVEL_VALUE / 2)
        self.__set_status(OneShotSlotStatus.NOT_RECORDED)

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
        self.__set_status(OneShotSlotStatus.RECORDING)

    def stop_recording(self):
        self.__set_dry_level(fl_helper.MIN_LEVEL_VALUE)
        plugins.setParamValue(fl_helper.MIN_LEVEL_VALUE,
                              self.__record_on_off_parameter_index,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)
        self.__set_status(OneShotSlotStatus.RECORDED)

    def status(self):
        return self.__status

    def playback_start(self):
        channels.midiNoteOn( 4 + self.__slot_number, 60, fl_helper.MIDI_MAX_VALUE )

    def playback_stop(self):
        channels.midiNoteOn( 4 + self.__slot_number, 60, fl_helper.MIDI_MIN_VALUE )

class OneshotSampler:

    CLEAR_MODE_OFF = 0
    CLEAR_MODE_ON = 1
    CLEAR_ALL = 2

    def __init__(self, view, updateable_mux, mixer_channel, mixer_slot):
        self.__view = view
        self.__updateable_mux = updateable_mux
        self.__mixer_channel = mixer_channel
        self.__mixer_slot = mixer_slot
        self.__one_shot_slots = []
        self.__clear_mode = OneshotSampler.CLEAR_MODE_OFF
        self.__clear_handler = updateable.DoubleClickTimeoutHandler(self.__handle_clear_first_click,
                                                                         self.__handle_clear_first_release,
                                                                         self.__handle_clear_second_click,
                                                                         self.__handle_clear_second_release,
                                                                         self.__handle_clear_timeout,
                                                                         0.3)

        self.__updateable_mux.add_updateable(self.__clear_handler)

    def on_init_script(self):
        self.__one_shot_slots.append(OneShotSlot(self.__view,
                                                 constants.RemixerSlot_1,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_1_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_1_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_1_DRY_LEVEL_PARAMETER_INDEX))

        self.__one_shot_slots.append(OneShotSlot(self.__view,
                                                 constants.RemixerSlot_2,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_2_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_2_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_2_DRY_LEVEL_PARAMETER_INDEX))

        self.__one_shot_slots.append(OneShotSlot(self.__view,
                                                 constants.RemixerSlot_3,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_3_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_3_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_3_DRY_LEVEL_PARAMETER_INDEX))

        self.__one_shot_slots.append(OneShotSlot(self.__view,
                                                 constants.RemixerSlot_4,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_4_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_4_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_4_DRY_LEVEL_PARAMETER_INDEX))

        self.__one_shot_slots.append(OneShotSlot(self.__view,
                                                 constants.RemixerSlot_5,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_5_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_5_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_5_DRY_LEVEL_PARAMETER_INDEX))

        self.__one_shot_slots.append(OneShotSlot(self.__view,
                                                 constants.RemixerSlot_6,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_6_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_6_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_6_DRY_LEVEL_PARAMETER_INDEX))

        self.__one_shot_slots.append(OneShotSlot(self.__view,
                                                 constants.RemixerSlot_7,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_7_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_7_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_7_DRY_LEVEL_PARAMETER_INDEX))

        self.__one_shot_slots.append(OneShotSlot(self.__view,
                                                 constants.RemixerSlot_8,
                                                 self.__mixer_channel,
                                                 self.__mixer_slot,
                                                 constants.ONESHOT_SAMPLER_8_REC_ON_OFF_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_8_VOLUME_PARAMETER_INDEX,
                                                 constants.ONESHOT_SAMPLER_8_DRY_LEVEL_PARAMETER_INDEX))

        for one_shot_slot in self.__one_shot_slots:
            one_shot_slot.on_init_script()

    def activate(self):
        pass

    def deactivate(self):
        pass

    def clear_click(self):
        self.__clear_handler.click()

    def clear_release(self):
        self.__clear_handler.release()

    def slot_click(self, remixer_slot_index):
        if not self.__get_clear_mode():
            if self.__status(remixer_slot_index) == OneShotSlotStatus.NOT_RECORDED:
                self.__start_recording(remixer_slot_index)
            elif self.__status(remixer_slot_index) == OneShotSlotStatus.RECORDED:
                self.__playback_start(remixer_slot_index)
        else:
            self.__reset_recording_status(remixer_slot_index)

    def slot_release(self, remixer_slot_index):
        if not self.__get_clear_mode():
            if self.__status(remixer_slot_index) == OneShotSlotStatus.RECORDING:
                self.__stop_recording(remixer_slot_index)
            elif self.__status(remixer_slot_index) == OneShotSlotStatus.RECORDED:
                self.__playback_stop(remixer_slot_index)

    def __handle_clear_first_click(self):
        self.__clear_mode = OneshotSampler.CLEAR_MODE_ON
        self.__view.set_remixer_clear_button_state(updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_DONE)

    def __handle_clear_first_release(self):
        self.__clear_mode = OneshotSampler.CLEAR_MODE_OFF
        self.__view.set_remixer_clear_button_state(updateable.DoubleClickTimeoutHandler.STATE_FIRST_CLICK_RELEASED)

    def __handle_clear_second_click(self):
        self.__reset_all_recording_statuses()
        self.__view.set_remixer_clear_button_state(updateable.DoubleClickTimeoutHandler.STATE_SECOND_CLICK_DONE)

    def __handle_clear_second_release(self):
        self.__view.set_remixer_clear_button_state(updateable.DoubleClickTimeoutHandler.STATE_INITITAL)

    def __handle_clear_timeout(self):
        self.__view.set_remixer_clear_button_state(updateable.DoubleClickTimeoutHandler.STATE_INITITAL)

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

class RemixTape:

    def __init__(self):
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass

    def clear_click(self):
        pass

    def clear_release(self):
        pass

    def slot_click(self, remixer_slot_index):
        pass

    def slot_release(self, remixer_slot_index):
        pass

class RemixUnitType(Enum):
    MIC = 0
    SYNTH = 1
    LOOPER_1 = 2
    LOOPER_2 = 3
    LOOPER_3 = 4
    LOOPER_4 = 5
    LOOPERS_ALL = 6

class RemixUnitSubType(Enum):
    ONE_SHOT_SAMPLE = 0
    REMIX_TAPE = 1    

class RemixManager:

    def __init__(self):
        pass

    def activate_unit(self, unit_id):
        pass

    def clear_click(self):
        pass

    def clear_release(self):
        pass

    def slot_click(self, remixer_slot_index):
        pass

    def slot_release(self, remixer_slot_index):
        pass
