'''
Created on Jan 24, 2022

@author: Dream Machines
'''

from input_controller.fx_unit import FXUnit
from input_controller.fx_preset import FXPreset

class FXPresetPage:

    FXPresetPage_1 = 0
    FXPresetPage_2 = 1
    FXPresetPage_3 = 2
    FXPresetPage_4 = 3

    def __init__(self, context, fx_page_number, view):
        self.__context = context
        self.__view = view
        self.__fx_page_number = fx_page_number
        self.__selected_fx_preset_id = FXPreset.FXPreset_1
        self.__fx_presets = { FXPreset.FXPreset_1: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_1, self.__view),
                       FXPreset.FXPreset_2: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_2, self.__view),
                       FXPreset.FXPreset_3: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_3, self.__view),
                       FXPreset.FXPreset_4: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_4, self.__view),
                       FXPreset.FXPreset_5: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_5, self.__view),
                       FXPreset.FXPreset_6: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_6, self.__view),
                       FXPreset.FXPreset_7: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_7, self.__view),
                       FXPreset.FXPreset_8: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_8, self.__view) }
        self.__initialized = False

    def select(self, select_preset = True):
        self.selectFXPreset(self.__selected_fx_preset_id, select_preset)
        self.__view_updateStats()

    def getSelectedFXPresetID(self):
        return self.__selected_fx_preset_id

    def onInitScript(self):

        if False == self.__initialized:

            for fx_preset_id in self.__fx_presets:
                self.__fx_presets[fx_preset_id].onInitScript()

            self.__initialized = True

    def setMidiMappings(self, fx_preset_id, midi_mappings):
        print(f"setMidiMappings: page - {str(self.__fx_page_number)}; fx_preset_id - {str(fx_preset_id)}; midi_mappings - {str(midi_mappings)}")
        self.__fx_presets[fx_preset_id].setMidiMappings(midi_mappings)

    def getMidiMappings(self, fx_preset_id):
        midi_mappings = self.__fx_presets[fx_preset_id].getMidiMappings()
        print(f"getMidiMappings: page - {str(self.__fx_page_number)}; fx_preset_id - {str(fx_preset_id)}; midi_mappings - {str(midi_mappings)}")
        return midi_mappings

    def updateFXPreset(self, fx_preset_id):
        self.__fx_presets[fx_preset_id].update()
        self.__fx_presets[fx_preset_id].view_updateFXPresetAvailability()
        self.__fx_presets[fx_preset_id].view_updateActiveFXUnit()
        self.__fx_presets[fx_preset_id].view_updateFXParamsFromPlugins()

    def resetFXPreset(self, fx_preset_id):
        self.__fx_presets[fx_preset_id].reset()
        self.__fx_presets[fx_preset_id].view_updateFXPresetAvailability()
        self.__fx_presets[fx_preset_id].view_updateFXParamsFromPlugins()
        self.__fx_presets[fx_preset_id].view_updateActiveFXUnit()

    def selectFXPreset(self, fx_preset_id, select_preset = True):
        print(self.__context.device_name + '_FXPresetPage' + ': ' + FXPresetPage.selectFXPreset.__name__ + " page - " + str(self.__fx_page_number) + ", preset - " + str(fx_preset_id))
        self.__selected_fx_preset_id = fx_preset_id

        if True == select_preset:
            self.__fx_presets[fx_preset_id].select()
            self.__fx_presets[fx_preset_id].view_updateFXPresetAvailability()
            self.__fx_presets[fx_preset_id].view_updateFXParamsFromPlugins()
            self.__fx_presets[fx_preset_id].view_updateActiveFXUnit()
        else:
            self.__view.selectFXPreset(self.__selected_fx_preset_id)

    def setMidiMapping(self, fx_parameter_number, midi_mapping):
        self.__fx_presets[self.__selected_fx_preset_id].setMidiMapping(fx_parameter_number, midi_mapping)

    def view_updateFXParamsFromPlugins(self):
        self.__fx_presets[self.__selected_fx_preset_id].view_updateFXParamsFromPlugins()

    def setFXParameterLevel(self, fx_param_id, fx_param_level):
            self.__fx_presets[self.__selected_fx_preset_id].setFXParameterLevel(fx_param_id, fx_param_level)

    def __view_updateStats(self):
        self.__view.selectFXPage(self.__fx_page_number)

        for fx_preset_id in self.__fx_presets:
            self.__fx_presets[fx_preset_id].view_updateFXPresetAvailability()

        self.__fx_presets[self.__selected_fx_preset_id].view_updateFXParamsFromPlugins()
        self.__fx_presets[self.__selected_fx_preset_id].view_updateActiveFXUnit()

    def changeActiveFXUnit(self):
        active_fx_unit = self.__fx_presets[self.__selected_fx_preset_id].getActiveFXUnit()

        if active_fx_unit == FXUnit.FX_UNIT_CUSTOM:
            print(self.__context.device_name + ': ' + FXPresetPage.changeActiveFXUnit.__name__ + ": to manipulator")
            self.__fx_presets[self.__selected_fx_preset_id].setActiveFXUnit(FXUnit.FX_UNIT_MANIPULATOR)
        elif active_fx_unit == FXUnit.FX_UNIT_MANIPULATOR:
            print(self.__context.device_name + ': ' + FXPresetPage.changeActiveFXUnit.__name__ + ": to finisher voodoo")
            self.__fx_presets[self.__selected_fx_preset_id].setActiveFXUnit(FXUnit.FX_UNIT_FINISHER_VOODOO)
        elif active_fx_unit == FXUnit.FX_UNIT_FINISHER_VOODOO:
            print(self.__context.device_name + ': ' + FXPresetPage.changeActiveFXUnit.__name__ + ": to custom")
            self.__fx_presets[self.__selected_fx_preset_id].setActiveFXUnit(FXUnit.FX_UNIT_CUSTOM)

        self.__fx_presets[self.__selected_fx_preset_id].view_updateActiveFXUnit()

    def setActiveFXUnit(self, active_fx_unit):
        self.__fx_presets[self.__selected_fx_preset_id].setActiveFXUnit(active_fx_unit)
        self.__fx_presets[self.__selected_fx_preset_id].view_updateActiveFXUnit()

    def getActiveFXUnit(self):
        return self.__fx_presets[self.__selected_fx_preset_id].getActiveFXUnit()