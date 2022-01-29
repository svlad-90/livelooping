'''
Created on Jan 24, 2022

@author: Dream Machines
'''

from input_controller import constants

class FXUnit:
    FX_UNIT_CUSTOM          = 0
    FX_UNIT_MANIPULATOR     = 1
    FX_UNIT_FINISHER_VOODOO = 2
    
    @staticmethod
    def activeFXUnitToAdjustablePluginSlotIndex(active_fx_unit):
        if active_fx_unit == FXUnit.FX_UNIT_FINISHER_VOODOO:
            return constants.FINISHER_VOODOO_SLOT_INDEX
        elif active_fx_unit == FXUnit.FX_UNIT_MANIPULATOR:
            return constants.MANIPULATOR_SLOT_INDEX
        else:
            return constants.INVALID_PARAM