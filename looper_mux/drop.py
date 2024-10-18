'''
Created on Sep 28, 2024

@author: Dream Machines
'''

import midi
import plugins
from common import input_handlers
from looper_mux import constants
from common import updateable

from looper_mux import view

class DropFX:
    def __init__(self, midi_channel,
                 midi_cc,
                 mixer_channel,
                 mixer_slot,
                 plugin_parameter,
                 view):
        self.__midi_channel = midi_channel
        self.__midi_cc = midi_cc
        self.__mixer_channel = mixer_channel
        self.__mixer_slot = mixer_slot
        self.__plugin_parameter = plugin_parameter
        self.__view = view
        self.__fx_level = 0.0

    def drop(self):
        self.__fx_level = 0.0
        self.__update_plugin_parameter()
        self.__view.set_drop_fx_level(self.__fx_level,
                                      self.__midi_cc,
                                      self.__midi_channel,
                                      True)

    def set_fx_level(self, fx_level, forward_to_device):
        self.__fx_level = fx_level
        self.__update_plugin_parameter()
        self.__view.set_drop_fx_level(self.__fx_level,
                                      self.__midi_cc,
                                      self.__midi_channel,
                                      forward_to_device)

    def __update_plugin_parameter(self):
        plugins.setParamValue(self.__fx_level,
                              self.__plugin_parameter,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)

class DropManager(updateable.Updateable):
    def __init__(self, view):
        self.__drop_fx_items = {}
        self.__view = view
        self.__delayed_reverb_activation = False

        drop_btn_release = lambda: \
            self.__view.set_drop_btn_state(False)

        self.__drop_button_handler = input_handlers.ClickReleaseHandler(self.__drop_btn_click,
                                                                     drop_btn_release)

    def __drop_btn_click(self):
        self.__view.set_drop_btn_state(True)

    def add_drop_fx(self, midi_channel,
                    midi_cc,
                    mixer_channel,
                    mixer_slot,
                    plugin_parameter):
        self.__drop_fx_items[(midi_channel, midi_cc)] = DropFX(midi_channel,
                                                            midi_cc,
                                                            mixer_channel,
                                                            mixer_slot,
                                                            plugin_parameter,
                                                            self.__view)

    def set_fx_level(self, midi_channel, midi_cc, fx_level, forward_to_device):
        self.__drop_fx_items[(midi_channel, midi_cc)].set_fx_level(fx_level, forward_to_device)

    def click_drop(self):
        self.__drop_button_handler.click()
        for drop_fx_item in self.__drop_fx_items:
            self.__drop_fx_items[drop_fx_item].drop()
        plugins.setParamValue(0.0,
                              constants.TURNADO_CONTROL_PARAMETER_1,
                              constants.DROP_REVERB_MIXER_CHANNEL,
                              constants.DROP_REVERB_MIXER_SLOT,
                              midi.PIM_None, True)
        plugins.setParamValue(0.0,
                              constants.TURNADO_CONTROL_PARAMETER_2,
                              constants.DROP_REVERB_MIXER_CHANNEL,
                              constants.DROP_REVERB_MIXER_SLOT,
                              midi.PIM_None, True)
        plugins.setParamValue(0.0,
                              constants.TURNADO_CONTROL_PARAMETER_3,
                              constants.DROP_REVERB_MIXER_CHANNEL,
                              constants.DROP_REVERB_MIXER_SLOT,
                              midi.PIM_None, True)
        self.__delayed_reverb_activation = True

    def release_drop(self):
        self.__drop_button_handler.release()

    def update(self, update_time):
        if self.__delayed_reverb_activation:
            plugins.setParamValue(1.0,
                              constants.TURNADO_CONTROL_PARAMETER_1,
                              constants.DROP_REVERB_MIXER_CHANNEL,
                              constants.DROP_REVERB_MIXER_SLOT,
                              midi.PIM_None, True)
            plugins.setParamValue(1.0,
                              constants.TURNADO_CONTROL_PARAMETER_2,
                              constants.DROP_REVERB_MIXER_CHANNEL,
                              constants.DROP_REVERB_MIXER_SLOT,
                              midi.PIM_None, True)
            plugins.setParamValue(1.0,
                              constants.TURNADO_CONTROL_PARAMETER_3,
                              constants.DROP_REVERB_MIXER_CHANNEL,
                              constants.DROP_REVERB_MIXER_SLOT,
                              midi.PIM_None, True)