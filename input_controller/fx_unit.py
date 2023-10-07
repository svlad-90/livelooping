'''
Created on Jan 24, 2022

@author: Dream Machines
'''

from input_controller import constants

class FxUnit:
    FX_UNIT_CUSTOM          = 0
    FX_UNIT_MANIPULATOR     = 1
    FX_UNIT_FINISHER_VOODOO = 2

    @staticmethod
    def active_fx_unit_to_adjustable_plugin_slot_index(active_fx_unit):
        if active_fx_unit == FxUnit.FX_UNIT_FINISHER_VOODOO:
            return constants.FINISHER_VOODOO_SLOT_INDEX
        elif active_fx_unit == FxUnit.FX_UNIT_MANIPULATOR:
            return constants.MANIPULATOR_SLOT_INDEX
        else:
            return constants.INVALID_PARAM