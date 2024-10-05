'''
Created on Sep 29, 2024

@author: Dream Machines
'''

import midi
import plugins

from looper_mux import view
from common import fl_helper
from looper_mux import constants

class SidechainItem:
    def __init__(self,
                 view,
                 midi_channel_tension,
                 midi_cc_tension,
                 midi_channel_decay,
                 midi_cc_decay,
                 track_id):
        self.__view = view
        self.__midi_channel_tension = midi_channel_tension
        self.__midi_cc_tension = midi_cc_tension
        self.__midi_channel_decay = midi_channel_decay
        self.__midi_cc_decay = midi_cc_decay
        self.__tension = 0.0
        self.__decay = 0.0
        self.__mixer_channel = constants.MASTER_CHANNEL
        self.__mixer_slot = constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX
        self.__tension_parameter_slot = fl_helper.find_parameter_by_name(self.__mixer_channel,
                                                                         "T" + str(track_id + 1) + "ST",
                                                                         self.__mixer_slot)
        self.__decay_parameter_slot = fl_helper.find_parameter_by_name(self.__mixer_channel,
                                                                         "T" + str(track_id + 1) + "SD",
                                                                         self.__mixer_slot)

    def set_sidechain_tension(self, tension, forward_to_device):
        print("set_sidechain_tension: tension - " + str(tension) + ", forward_to_device - " + str(forward_to_device))
        self.__tension = tension
        plugins.setParamValue(self.__tension,
                              self.__tension_parameter_slot,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)
        self.__view.set_tension_side_chain_level(self.__midi_channel_tension,
                                                 self.__midi_cc_tension,
                                                 self.__tension,
                                                 forward_to_device)

    def set_sidechain_decay(self, decay, forward_to_device):
        print("set_sidechain_decay: decay - " + str(decay) + ", forward_to_device - " + str(forward_to_device))
        self.__decay = decay
        plugins.setParamValue(self.__decay,
                              self.__decay_parameter_slot,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None, True)
        self.__view.set_tension_side_chain_level(self.__midi_channel_decay,
                                                 self.__midi_cc_decay,
                                                 self.__decay,
                                                 forward_to_device)

    def update_sidechain_tension(self):
        self.__view.set_tension_side_chain_level(self.__midi_channel_tension,
                                                 self.__midi_cc_tension,
                                                 self.__tension,
                                                 True)

    def update_sidechain_decay(self):
        self.__view.set_decay_side_chain_level(self.__midi_channel_decay,
                                               self.__midi_cc_decay,
                                               self.__decay,
                                               True)

class SidechainManager:
    def __init__(self, view):
        self.__sidechain_items = {}
        self.__view = view

    def add_sidechain_item(self,
                 midi_channel_tension,
                 midi_cc_tension,
                 midi_channel_decay,
                 midi_cc_decay,
                 track_id):
        sidechain_item = SidechainItem(self.__view,
                                       midi_channel_tension,
                                       midi_cc_tension,
                                       midi_channel_decay,
                                       midi_cc_decay,
                                       track_id)
        self.__sidechain_items[track_id] = sidechain_item
        self.__sidechain_items[track_id] = sidechain_item

    def remove_sidechain_item(self, track_id):
        del self.__sidechain_items[track_id]

    def set_sidechain_tension(self, track_id, tension, forward_to_device):
        self.__sidechain_items[track_id].set_sidechain_tension(tension, forward_to_device)

    def set_sidechain_decay(self, track_id, decay, forward_to_device):
        self.__sidechain_items[track_id].set_sidechain_decay(decay, forward_to_device)

    def update_sidechain_parameters(self):
        for sidechain_item_key in self.__sidechain_items:
            self.__sidechain_items[sidechain_item_key].update_sidechain_tension()
            self.__sidechain_items[sidechain_item_key].update_sidechain_decay()
