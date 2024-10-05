'''
Created on Oct 5, 2024

@author: Dream Machines
'''

import math

import midi
import plugins

from common import fl_helper
from looper_mux import view
from looper_mux import constants


class FXAnimation:

    ANIMATION_1 = 0
    ANIMATION_2 = 1
    ANIMATION_3 = 2
    ANIMATION_4 = 3
    ANIMATION_5 = 4
    ANIMATION_6 = 5
    ANIMATION_7 = 6
    ANIMATION_8 = 7

    def __init__(self, view, x1, y1, x2, y2):
        self.__view = view
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

    def get_x1(self):
        return self.__x1

    def get_y1(self):
        return self.__y1

    def get_x2(self):
        return self.__x2

    def get_y2(self):
        return self.__y2


class FXSlot:

    PARAMETER_DEFAULT_VALUE = 0.5

    SLOT_1 = 0
    SLOT_2 = 1
    SLOT_3 = 2
    SLOT_4 = 3
    SLOT_5 = 4
    SLOT_6 = 5
    SLOT_7 = 6
    SLOT_8 = 7
    SLOT_9 = 8
    SLOT_10 = 9
    SLOTS_IN_BANK = 10

    def __init__(self, view, animations, bank_number, slot_number,
                 mixer_channel, mixer_slot, parameter_1, parameter_2,
                 parameter_3, parameter_4, parameter_5, parameter_6,
                 parameter_7, parameter_8, parameter_9):
        # print("bank_number - " + str(bank_number) + ", slot_number - - " + str(slot_number))
        self.__view = view
        self.__animations = animations
        self.__bank_number = bank_number
        self.__slot_number = slot_number
        self.__mixer_channel = mixer_channel
        self.__mixer_slot = mixer_slot
        self.__parameter_1 = parameter_1
        self.__parameter_2 = parameter_2
        self.__parameter_3 = parameter_3
        self.__parameter_4 = parameter_4
        self.__parameter_5 = parameter_5
        self.__parameter_6 = parameter_6
        self.__parameter_7 = parameter_7
        self.__parameter_8 = parameter_8
        self.__parameter_9 = parameter_9
        self.__animation_active = False
        self.__number_of_selected_animations = 0
        self.__fx_turn_on_parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL,
                                                                          "TUR" + str(self.__bank_number * FXSlot.SLOTS_IN_BANK + self.__slot_number + 1),
                                                                          constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.__fx_dry_wet_parameter_id = fl_helper.find_parameter_by_name(constants.MASTER_CHANNEL,
                                                                          "TUR" + str(self.__bank_number * FXSlot.SLOTS_IN_BANK + self.__slot_number + 1) + "W",
                                                                          constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def select(self, dry_wet_level, x1, y1, x2, y2):
        plugins.setParamValue(1,
                              self.__fx_turn_on_parameter_id,
                              constants.MASTER_CHANNEL,
                              constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX,
                              midi.PIM_None,
                              True)
        self.set_dry_wet_level(dry_wet_level, True)
        self.__apply_parameters(x1, y1, x2, y2)
        self.__view.set_fx_slot_status(self.__slot_number, True)
        
    def unselect(self):
        plugins.setParamValue(0,
                              self.__fx_turn_on_parameter_id,
                              constants.MASTER_CHANNEL,
                              constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX,
                              midi.PIM_None,
                              True)
        self.set_dry_wet_level(0, False)
        self.__view.set_fx_slot_status(self.__slot_number, False)

    def set_param_x1(self, x1):
        if not self.__animation_active:
            self.__apply_parameter(self.__parameter_4, self.__parameter_2, x1)    

    def set_param_y1(self, y1):
        if not self.__animation_active:
            self.__apply_parameter(self.__parameter_3, self.__parameter_1, y1)

    def set_param_x2(self, x2):
        if not self.__animation_active:
            self.__apply_parameter(self.__parameter_8, self.__parameter_6, x2)

    def set_param_y2(self, y2):
        if not self.__animation_active:
            self.__apply_parameter(self.__parameter_7, self.__parameter_5, y2)

    def select_animation(self, selected_animation):

        self.__animation_active = True
        self.__number_of_selected_animations += 1

        for animation_id in self.__animations:
            if animation_id == selected_animation:
                target_animation = self.__animations[animation_id]
                self.__apply_parameters(target_animation.get_x1(), target_animation.get_y1(), target_animation.get_x2(), target_animation.get_y2())
            else:
                self.unselect_animation(animation_id)

    def unselect_animation(self, animation):

        self.__number_of_selected_animations -= 1

        if self.__number_of_selected_animations == 0:
            self.__animation_active = False
            self.__apply_default_parameters()

    def __apply_default_parameters(self):
        self.__apply_parameters(FXSlot.PARAMETER_DEFAULT_VALUE, FXSlot.PARAMETER_DEFAULT_VALUE,
                                FXSlot.PARAMETER_DEFAULT_VALUE, FXSlot.PARAMETER_DEFAULT_VALUE)

    def __apply_parameters(self, x1, y1, x2, y2):
        # print("__apply_parameters - x1 - " + str(x1) + ", y1 - " + str(y1) + ", x2 - " + str(x2) + ", y2 - " + str(y2))
        self.__apply_parameter(self.__parameter_4, self.__parameter_2, x1)
        self.__apply_parameter(self.__parameter_3, self.__parameter_1, y1)
        self.__apply_parameter(self.__parameter_8, self.__parameter_6, x2)
        self.__apply_parameter(self.__parameter_7, self.__parameter_5, y2)

    def __apply_parameter(self, param_slot_min, param_slot_max, param_value):
        target_parameter_id = param_slot_min if param_value < FXSlot.PARAMETER_DEFAULT_VALUE else param_slot_max
        target_parameter_value = 1

        dead_zone = 0.15

        dead_zone_lower_limit = FXSlot.PARAMETER_DEFAULT_VALUE - dead_zone
        dead_zone_upper_limit = FXSlot.PARAMETER_DEFAULT_VALUE + dead_zone

        if param_value >= dead_zone_lower_limit and param_value <= dead_zone_upper_limit:
            target_parameter_value = 0
        else:
            target_parameter_value = ( math.fabs(param_value - FXSlot.PARAMETER_DEFAULT_VALUE ) - dead_zone ) / (FXSlot.PARAMETER_DEFAULT_VALUE - dead_zone)

        plugins.setParamValue(target_parameter_value,
                              target_parameter_id,
                              self.__mixer_channel,
                              self.__mixer_slot,
                              midi.PIM_None,
                              True)

    def set_dry_wet_level(self, dry_wet_level, forward_to_device):
        plugins.setParamValue(dry_wet_level,
                              self.__fx_dry_wet_parameter_id,
                              constants.MASTER_CHANNEL,
                              constants.MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX,
                              midi.PIM_None,
                              True)
        self.__view.set_fx_dry_wet_level(dry_wet_level, forward_to_device)

    def on_init_script(self):
        self.__apply_default_parameters()

    def set_extra_param_1_level(self, parameter_level, forward_to_device):
        plugins.setParamValue(parameter_level,
                      self.__parameter_9,
                      constants.FX_UNIT_BLOCK_1_CHANNEL + self.__bank_number,
                      self.__slot_number,
                      midi.PIM_None,
                      True)
        self.__view.set_fx_extra_parameter_1_level(parameter_level, forward_to_device)

class FXBank:

    BANK_1 = 0
    BANK_2 = 1
    BANK_3 = 2
    BANK_4 = 3
    BANK_5 = 4

    def __init__(self, view, bank_number, slots):
        self.__view = view
        self.__slots = slots
        self.__selected_slot = FXSlot.SLOT_1
        self.__bank_number = bank_number

    def select(self, dry_wet_level, x1, y1, x2 , y2):
        self.select_slot(self.__selected_slot, dry_wet_level, x1, y1, x2 , y2)
        self.__view.set_fx_bank_status(self.__bank_number, True)

    def unselect(self):
        self.__view.set_fx_bank_status(self.__bank_number, False)
        for slot_id in self.__slots:
            self.__slots[slot_id].unselect()

    def select_slot(self, slot_id, dry_wet_level, x1, y1, x2 , y2):
        self.__selected_slot = slot_id
        for slot_id in self.__slots:
            self.__slots[slot_id].unselect()

        self.set_extra_param_1_level(0.0, True)
        self.__slots[self.__selected_slot].select(dry_wet_level, x1, y1, x2 , y2)

    def set_param_x1(self, x1):
        self.__slots[self.__selected_slot].set_param_x1(x1)

    def set_param_y1(self, y1):
        self.__slots[self.__selected_slot].set_param_y1(y1)

    def set_param_x2(self, x2):
        self.__slots[self.__selected_slot].set_param_x2(x2)

    def set_param_y2(self, y2):
        self.__slots[self.__selected_slot].set_param_y2(y2)

    def select_animation(self, animation):
        self.__slots[self.__selected_slot].select_animation(animation)

    def unselect_animation(self, animation):
        self.__slots[self.__selected_slot].unselect_animation(animation)

    def set_dry_wet_level(self, dry_wet_level, forward_to_device):
        self.__slots[self.__selected_slot].set_dry_wet_level(dry_wet_level, forward_to_device)

    def on_init_script(self):
        for slot_id in self.__slots:
            self.__slots[slot_id].on_init_script()

    def set_extra_param_1_level(self, dictator_level, forward_to_device):
        self.__slots[self.__selected_slot].set_extra_param_1_level(dictator_level, forward_to_device)

class FXManager:

    PARAMETER_DEFAULT_VALUE = 0.5

    def __init__(self, view):
        self.__view = view
        self.__selected_bank = FXBank.BANK_1
        self.__dry_wet_level = 1
        self.__x1 = FXManager.PARAMETER_DEFAULT_VALUE
        self.__y1 = FXManager.PARAMETER_DEFAULT_VALUE
        self.__x2 = FXManager.PARAMETER_DEFAULT_VALUE
        self.__y2 = FXManager.PARAMETER_DEFAULT_VALUE

    def select_bank(self, bank_id):
        self.__selected_bank = bank_id
        for bank_id in self.__banks:
            self.__banks[bank_id].unselect()

        self.__banks[self.__selected_bank].select(self.__dry_wet_level,
                             self.__x1,
                             self.__y1,
                             self.__x2,
                             self.__y2)

    def select_slot(self, slot_id):
        self.__banks[self.__selected_bank].select_slot(slot_id,
                                                       self.__dry_wet_level,
                                                       self.__x1,
                                                       self.__y1,
                                                       self.__x2,
                                                       self.__y2)

    def set_param_x1(self, x1):
        self.__x1 = x1
        self.__banks[self.__selected_bank].set_param_x1(x1)

    def set_param_y1(self, y1):
        self.__y1 = y1
        self.__banks[self.__selected_bank].set_param_y1(y1)

    def set_param_x2(self, x2):
        self.__x2 = x2
        self.__banks[self.__selected_bank].set_param_x2(x2)

    def set_param_y2(self, y2):
        self.__y2 = y2
        self.__banks[self.__selected_bank].set_param_y2(y2)

    def select_animation(self, animation):
        self.__banks[self.__selected_bank].select_animation(animation)

    def unselect_animation(self, animation):
        self.__banks[self.__selected_bank].unselect_animation(animation)

    def set_dry_wet_level(self, dry_wet_level, forward_to_device):
        self.__dry_wet_level = dry_wet_level
        self.__banks[self.__selected_bank].set_dry_wet_level(dry_wet_level, forward_to_device)

    def on_init_script(self):

        # BANK 1

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_1 = FXSlot(self.__view, animations, FXBank.BANK_1, FXSlot.SLOT_1,
                 constants.FX_UNIT_BLOCK_1_CHANNEL, FXSlot.SLOT_1,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_2 = FXSlot(self.__view, animations, FXBank.BANK_1, FXSlot.SLOT_2,
                 constants.FX_UNIT_BLOCK_1_CHANNEL, FXSlot.SLOT_2,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_3 = FXSlot(self.__view, animations, FXBank.BANK_1, FXSlot.SLOT_3,
                 constants.FX_UNIT_BLOCK_1_CHANNEL, FXSlot.SLOT_3,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_4 = FXSlot(self.__view, animations, FXBank.BANK_1, FXSlot.SLOT_4,
                 constants.FX_UNIT_BLOCK_1_CHANNEL, FXSlot.SLOT_4,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_5 = FXSlot(self.__view, animations, FXBank.BANK_1, FXSlot.SLOT_5,
                 constants.FX_UNIT_BLOCK_1_CHANNEL, FXSlot.SLOT_5,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_6 = FXSlot(self.__view, animations, FXBank.BANK_1, FXSlot.SLOT_6,
                 constants.FX_UNIT_BLOCK_1_CHANNEL, FXSlot.SLOT_6,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_7 = FXSlot(self.__view, animations, FXBank.BANK_1, FXSlot.SLOT_7,
                 constants.FX_UNIT_BLOCK_1_CHANNEL, FXSlot.SLOT_7,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_8 = FXSlot(self.__view, animations, FXBank.BANK_1, FXSlot.SLOT_8,
                 constants.FX_UNIT_BLOCK_1_CHANNEL, FXSlot.SLOT_8,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_9 = FXSlot(self.__view, animations, FXBank.BANK_1, FXSlot.SLOT_9,
                 constants.FX_UNIT_BLOCK_1_CHANNEL, FXSlot.SLOT_9,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_10 = FXSlot(self.__view, animations, FXBank.BANK_1, FXSlot.SLOT_10,
                 constants.FX_UNIT_BLOCK_1_CHANNEL, FXSlot.SLOT_10,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        bank_1 = FXBank(self.__view, FXBank.BANK_1,
                        {FXSlot.SLOT_1: fx_slot_1,
                         FXSlot.SLOT_2: fx_slot_2,
                         FXSlot.SLOT_3: fx_slot_3,
                         FXSlot.SLOT_4: fx_slot_4,
                         FXSlot.SLOT_5: fx_slot_5,
                         FXSlot.SLOT_6: fx_slot_6,
                         FXSlot.SLOT_7: fx_slot_7,
                         FXSlot.SLOT_8: fx_slot_8,
                         FXSlot.SLOT_9: fx_slot_9,
                         FXSlot.SLOT_10: fx_slot_10, })

        # BANK 2

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_1 = FXSlot(self.__view, animations, FXBank.BANK_2, FXSlot.SLOT_1,
                 constants.FX_UNIT_BLOCK_2_CHANNEL, FXSlot.SLOT_1,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_2 = FXSlot(self.__view, animations, FXBank.BANK_2, FXSlot.SLOT_2,
                 constants.FX_UNIT_BLOCK_2_CHANNEL, FXSlot.SLOT_2,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_3 = FXSlot(self.__view, animations, FXBank.BANK_2, FXSlot.SLOT_3,
                 constants.FX_UNIT_BLOCK_2_CHANNEL, FXSlot.SLOT_3,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_4 = FXSlot(self.__view, animations, FXBank.BANK_2, FXSlot.SLOT_4,
                 constants.FX_UNIT_BLOCK_2_CHANNEL, FXSlot.SLOT_4,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_5 = FXSlot(self.__view, animations, FXBank.BANK_2, FXSlot.SLOT_5,
                 constants.FX_UNIT_BLOCK_2_CHANNEL, FXSlot.SLOT_5,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_6 = FXSlot(self.__view, animations, FXBank.BANK_2, FXSlot.SLOT_6,
                 constants.FX_UNIT_BLOCK_2_CHANNEL, FXSlot.SLOT_6,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_7 = FXSlot(self.__view, animations, FXBank.BANK_2, FXSlot.SLOT_7,
                 constants.FX_UNIT_BLOCK_2_CHANNEL, FXSlot.SLOT_7,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_8 = FXSlot(self.__view, animations, FXBank.BANK_2, FXSlot.SLOT_8,
                 constants.FX_UNIT_BLOCK_2_CHANNEL, FXSlot.SLOT_8,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_9 = FXSlot(self.__view, animations, FXBank.BANK_2, FXSlot.SLOT_9,
                 constants.FX_UNIT_BLOCK_2_CHANNEL, FXSlot.SLOT_9,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_10 = FXSlot(self.__view, animations, FXBank.BANK_2, FXSlot.SLOT_10,
                 constants.FX_UNIT_BLOCK_2_CHANNEL, FXSlot.SLOT_10,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        bank_2 = FXBank(self.__view, FXBank.BANK_2,
                        {FXSlot.SLOT_1: fx_slot_1,
                         FXSlot.SLOT_2: fx_slot_2,
                         FXSlot.SLOT_3: fx_slot_3,
                         FXSlot.SLOT_4: fx_slot_4,
                         FXSlot.SLOT_5: fx_slot_5,
                         FXSlot.SLOT_6: fx_slot_6,
                         FXSlot.SLOT_7: fx_slot_7,
                         FXSlot.SLOT_8: fx_slot_8,
                         FXSlot.SLOT_9: fx_slot_9,
                         FXSlot.SLOT_10: fx_slot_10, })

        # BANK 3

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_1 = FXSlot(self.__view, animations, FXBank.BANK_3, FXSlot.SLOT_1,
                 constants.FX_UNIT_BLOCK_3_CHANNEL, FXSlot.SLOT_1,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_2 = FXSlot(self.__view, animations, FXBank.BANK_3, FXSlot.SLOT_2,
                 constants.FX_UNIT_BLOCK_3_CHANNEL, FXSlot.SLOT_2,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_3 = FXSlot(self.__view, animations, FXBank.BANK_3, FXSlot.SLOT_3,
                 constants.FX_UNIT_BLOCK_3_CHANNEL, FXSlot.SLOT_3,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_4 = FXSlot(self.__view, animations, FXBank.BANK_3, FXSlot.SLOT_4,
                 constants.FX_UNIT_BLOCK_3_CHANNEL, FXSlot.SLOT_4,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_5 = FXSlot(self.__view, animations, FXBank.BANK_3, FXSlot.SLOT_5,
                 constants.FX_UNIT_BLOCK_3_CHANNEL, FXSlot.SLOT_5,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_6 = FXSlot(self.__view, animations, FXBank.BANK_3, FXSlot.SLOT_6,
                 constants.FX_UNIT_BLOCK_3_CHANNEL, FXSlot.SLOT_6,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_7 = FXSlot(self.__view, animations, FXBank.BANK_3, FXSlot.SLOT_7,
                 constants.FX_UNIT_BLOCK_3_CHANNEL, FXSlot.SLOT_7,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_8 = FXSlot(self.__view, animations, FXBank.BANK_3, FXSlot.SLOT_8,
                 constants.FX_UNIT_BLOCK_3_CHANNEL, FXSlot.SLOT_8,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_9 = FXSlot(self.__view, animations, FXBank.BANK_3, FXSlot.SLOT_9,
                 constants.FX_UNIT_BLOCK_3_CHANNEL, FXSlot.SLOT_9,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_10 = FXSlot(self.__view, animations, FXBank.BANK_3, FXSlot.SLOT_10,
                 constants.FX_UNIT_BLOCK_3_CHANNEL, FXSlot.SLOT_10,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        bank_3 = FXBank(self.__view, FXBank.BANK_3,
                        {FXSlot.SLOT_1: fx_slot_1,
                         FXSlot.SLOT_2: fx_slot_2,
                         FXSlot.SLOT_3: fx_slot_3,
                         FXSlot.SLOT_4: fx_slot_4,
                         FXSlot.SLOT_5: fx_slot_5,
                         FXSlot.SLOT_6: fx_slot_6,
                         FXSlot.SLOT_7: fx_slot_7,
                         FXSlot.SLOT_8: fx_slot_8,
                         FXSlot.SLOT_9: fx_slot_9,
                         FXSlot.SLOT_10: fx_slot_10, })

        # BANK 4

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_1 = FXSlot(self.__view, animations, FXBank.BANK_4, FXSlot.SLOT_1,
                 constants.FX_UNIT_BLOCK_4_CHANNEL, FXSlot.SLOT_1,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_2 = FXSlot(self.__view, animations, FXBank.BANK_4, FXSlot.SLOT_2,
                 constants.FX_UNIT_BLOCK_4_CHANNEL, FXSlot.SLOT_2,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_3 = FXSlot(self.__view, animations, FXBank.BANK_4, FXSlot.SLOT_3,
                 constants.FX_UNIT_BLOCK_4_CHANNEL, FXSlot.SLOT_3,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_4 = FXSlot(self.__view, animations, FXBank.BANK_4, FXSlot.SLOT_4,
                 constants.FX_UNIT_BLOCK_4_CHANNEL, FXSlot.SLOT_4,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_5 = FXSlot(self.__view, animations, FXBank.BANK_4, FXSlot.SLOT_5,
                 constants.FX_UNIT_BLOCK_4_CHANNEL, FXSlot.SLOT_5,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_6 = FXSlot(self.__view, animations, FXBank.BANK_4, FXSlot.SLOT_6,
                 constants.FX_UNIT_BLOCK_4_CHANNEL, FXSlot.SLOT_6,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_7 = FXSlot(self.__view, animations, FXBank.BANK_4, FXSlot.SLOT_7,
                 constants.FX_UNIT_BLOCK_4_CHANNEL, FXSlot.SLOT_7,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_8 = FXSlot(self.__view, animations, FXBank.BANK_4, FXSlot.SLOT_8,
                 constants.FX_UNIT_BLOCK_4_CHANNEL, FXSlot.SLOT_8,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_9 = FXSlot(self.__view, animations, FXBank.BANK_4, FXSlot.SLOT_9,
                 constants.FX_UNIT_BLOCK_4_CHANNEL, FXSlot.SLOT_9,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_10 = FXSlot(self.__view, animations, FXBank.BANK_4, FXSlot.SLOT_10,
                 constants.FX_UNIT_BLOCK_4_CHANNEL, FXSlot.SLOT_10,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        bank_4 = FXBank(self.__view, FXBank.BANK_4,
                        {FXSlot.SLOT_1: fx_slot_1,
                         FXSlot.SLOT_2: fx_slot_2,
                         FXSlot.SLOT_3: fx_slot_3,
                         FXSlot.SLOT_4: fx_slot_4,
                         FXSlot.SLOT_5: fx_slot_5,
                         FXSlot.SLOT_6: fx_slot_6,
                         FXSlot.SLOT_7: fx_slot_7,
                         FXSlot.SLOT_8: fx_slot_8,
                         FXSlot.SLOT_9: fx_slot_9,
                         FXSlot.SLOT_10: fx_slot_10, })

        # BANK 5

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_1 = FXSlot(self.__view, animations, FXBank.BANK_5, FXSlot.SLOT_1,
                 constants.FX_UNIT_BLOCK_5_CHANNEL, FXSlot.SLOT_1,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_2 = FXSlot(self.__view, animations, FXBank.BANK_5, FXSlot.SLOT_2,
                 constants.FX_UNIT_BLOCK_5_CHANNEL, FXSlot.SLOT_2,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_3 = FXSlot(self.__view, animations, FXBank.BANK_5, FXSlot.SLOT_3,
                 constants.FX_UNIT_BLOCK_5_CHANNEL, FXSlot.SLOT_3,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_4 = FXSlot(self.__view, animations, FXBank.BANK_5, FXSlot.SLOT_4,
                 constants.FX_UNIT_BLOCK_5_CHANNEL, FXSlot.SLOT_4,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_5 = FXSlot(self.__view, animations, FXBank.BANK_5, FXSlot.SLOT_5,
                 constants.FX_UNIT_BLOCK_5_CHANNEL, FXSlot.SLOT_5,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_6 = FXSlot(self.__view, animations, FXBank.BANK_5, FXSlot.SLOT_6,
                 constants.FX_UNIT_BLOCK_5_CHANNEL, FXSlot.SLOT_6,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_7 = FXSlot(self.__view, animations, FXBank.BANK_5, FXSlot.SLOT_7,
                 constants.FX_UNIT_BLOCK_5_CHANNEL, FXSlot.SLOT_7,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_8 = FXSlot(self.__view, animations, FXBank.BANK_5, FXSlot.SLOT_8,
                 constants.FX_UNIT_BLOCK_5_CHANNEL, FXSlot.SLOT_8,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_9 = FXSlot(self.__view, animations, FXBank.BANK_5, FXSlot.SLOT_9,
                 constants.FX_UNIT_BLOCK_5_CHANNEL, FXSlot.SLOT_9,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        animation1 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation2 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation3 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation4 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation5 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation6 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation7 = FXAnimation(self.__view, 0, 0, 0, 0)
        animation8 = FXAnimation(self.__view, 0, 0, 0, 0)

        animations = {FXAnimation.ANIMATION_1: animation1,
                      FXAnimation.ANIMATION_2: animation2,
                      FXAnimation.ANIMATION_3: animation3,
                      FXAnimation.ANIMATION_4: animation4,
                      FXAnimation.ANIMATION_5: animation5,
                      FXAnimation.ANIMATION_6: animation6,
                      FXAnimation.ANIMATION_7: animation7,
                      FXAnimation.ANIMATION_8: animation8
                      }

        fx_slot_10 = FXSlot(self.__view, animations, FXBank.BANK_5, FXSlot.SLOT_10,
                 constants.FX_UNIT_BLOCK_5_CHANNEL, FXSlot.SLOT_10,
                 constants.TURNADO_CONTROL_PARAMETER_1,
                 constants.TURNADO_CONTROL_PARAMETER_2,
                 constants.TURNADO_CONTROL_PARAMETER_3,
                 constants.TURNADO_CONTROL_PARAMETER_4,
                 constants.TURNADO_CONTROL_PARAMETER_5,
                 constants.TURNADO_CONTROL_PARAMETER_6,
                 constants.TURNADO_CONTROL_PARAMETER_7,
                 constants.TURNADO_CONTROL_PARAMETER_8,
                 constants.TURNADO_DICTATOR_PARAM_INDEX)

        bank_5 = FXBank(self.__view, FXBank.BANK_5,
                        {FXSlot.SLOT_1: fx_slot_1,
                         FXSlot.SLOT_2: fx_slot_2,
                         FXSlot.SLOT_3: fx_slot_3,
                         FXSlot.SLOT_4: fx_slot_4,
                         FXSlot.SLOT_5: fx_slot_5,
                         FXSlot.SLOT_6: fx_slot_6,
                         FXSlot.SLOT_7: fx_slot_7,
                         FXSlot.SLOT_8: fx_slot_8,
                         FXSlot.SLOT_9: fx_slot_9,
                         FXSlot.SLOT_10: fx_slot_10, })

        self.__banks = { FXBank.BANK_1: bank_1,
                         FXBank.BANK_2: bank_2,
                         FXBank.BANK_3: bank_3,
                         FXBank.BANK_4: bank_4,
                         FXBank.BANK_5: bank_5 }

        for bank_id in self.__banks:
            self.__banks[bank_id].on_init_script()

        self.select_bank(self.__selected_bank)

    def set_extra_param_1_level(self, dictator_level, forward_to_device):
        self.__banks[self.__selected_bank].set_extra_param_1_level(dictator_level, forward_to_device)