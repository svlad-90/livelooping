'''
Created on Jan 24, 2022

@author: Dream Machines
'''

import math

import midi
import plugins

from input_controller import constants
from common import fl_helper

class Fx:

    FX_1  = 0
    FX_2  = 1
    FX_3  = 2
    FX_4  = 3
    FX_5  = 4
    FX_6  = 5
    FX_7  = 6
    FX_8  = 7
    FX_9  = 8
    FX_10 = 9

    def __init__(self, context, fx_number, view):
        self.__context = context
        self.__fx_number = fx_number
        self.__view = view
        self.__activation_param_id = -1
        self.__level_param_id = -1
        self.__fx_level = 0

    def set_fx_level(self, fx_level, force = False):

        if self.__activation_param_id == -1:
            self.__activation_param_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "E" + str(self.__fx_number + 1) + "_TO", constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)

        if math.fabs(self.__fx_level - fx_level) >= 0.01 or fx_level == 1.0 or True == force:

            fx_activation_status = plugins.getParamValue(self.__activation_param_id, self.__context.main_channel, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, True)

            if self.__level_param_id == -1:
                self.__level_param_id = fl_helper.find_parameter_by_name(self.__context.main_channel, "FX_L" + str(self.__fx_number + 1), constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)

            if fx_activation_status == 0.0:
                plugins.setParamValue(0.0, self.__level_param_id, self.__context.main_channel, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)
            else:
                plugins.setParamValue(fx_level, self.__level_param_id, self.__context.main_channel, constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX, midi.PIM_None, True)

            self.__fx_level = fx_level
