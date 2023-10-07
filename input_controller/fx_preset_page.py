'''
Created on Jan 24, 2022

@author: Dream Machines
'''

from input_controller.fx_unit import FxUnit
from input_controller.fx_preset import FxPreset

class FxPresetPage:

    fx_preset_page_1 = 0
    fx_preset_page_2 = 1
    fx_preset_page_3 = 2
    fx_preset_page_4 = 3

    def __init__(self, context, fx_page_number, view):
        self.__context = context
        self.__view = view
        self.__fx_page_number = fx_page_number
        self.__selected_fx_preset_id = FxPreset.fx_preset_1
        self.__fx_presets = { FxPreset.fx_preset_1: FxPreset(self.__context, fx_page_number, FxPreset.fx_preset_1, self.__view),
                       FxPreset.fx_preset_2: FxPreset(self.__context, fx_page_number, FxPreset.fx_preset_2, self.__view),
                       FxPreset.fx_preset_3: FxPreset(self.__context, fx_page_number, FxPreset.fx_preset_3, self.__view),
                       FxPreset.fx_preset_4: FxPreset(self.__context, fx_page_number, FxPreset.fx_preset_4, self.__view),
                       FxPreset.fx_preset_5: FxPreset(self.__context, fx_page_number, FxPreset.fx_preset_5, self.__view),
                       FxPreset.fx_preset_6: FxPreset(self.__context, fx_page_number, FxPreset.fx_preset_6, self.__view),
                       FxPreset.fx_preset_7: FxPreset(self.__context, fx_page_number, FxPreset.fx_preset_7, self.__view),
                       FxPreset.fx_preset_8: FxPreset(self.__context, fx_page_number, FxPreset.fx_preset_8, self.__view) }
        self.__initialized = False

    def select(self, select_preset = True):
        self.select_fx_preset(self.__selected_fx_preset_id, select_preset)
        self.__view_update_stats()

    def get_selected_fx_preset_id(self):
        return self.__selected_fx_preset_id

    def on_init_script(self):

        if False == self.__initialized:

            for fx_preset_id in self.__fx_presets:
                self.__fx_presets[fx_preset_id].on_init_script()

            self.__initialized = True

    def set_midi_mappings(self, fx_preset_id, midi_mappings):
        print(f"set_midi_mappings: page - {str(self.__fx_page_number)}; fx_preset_id - {str(fx_preset_id)}; midi_mappings - {str(midi_mappings)}")
        self.__fx_presets[fx_preset_id].set_midi_mappings(midi_mappings)

    def get_midi_mappings(self, fx_preset_id):
        midi_mappings = self.__fx_presets[fx_preset_id].get_midi_mappings()
        print(f"get_midi_mappings: page - {str(self.__fx_page_number)}; fx_preset_id - {str(fx_preset_id)}; midi_mappings - {str(midi_mappings)}")
        return midi_mappings

    def update_fx_preset(self, fx_preset_id):
        self.__fx_presets[fx_preset_id].update()
        self.__fx_presets[fx_preset_id].view_update_fx_preset_availability()
        self.__fx_presets[fx_preset_id].view_update_active_fx_unit()
        self.__fx_presets[fx_preset_id].view_update_fx_params_from_plugins()

    def reset_fx_preset(self, fx_preset_id):
        self.__fx_presets[fx_preset_id].reset()
        self.__fx_presets[fx_preset_id].view_update_fx_preset_availability()
        self.__fx_presets[fx_preset_id].view_update_fx_params_from_plugins()
        self.__fx_presets[fx_preset_id].view_update_active_fx_unit()

    def select_fx_preset(self, fx_preset_id, select_preset = True):
        print(self.__context.device_name + '_fx_preset_page' + ': ' + FxPresetPage.select_fx_preset.__name__ + " page - " + str(self.__fx_page_number) + ", preset - " + str(fx_preset_id))
        self.__selected_fx_preset_id = fx_preset_id

        if True == select_preset:
            self.__fx_presets[fx_preset_id].select()
            self.__fx_presets[fx_preset_id].view_update_fx_preset_availability()
            self.__fx_presets[fx_preset_id].view_update_fx_params_from_plugins()
            self.__fx_presets[fx_preset_id].view_update_active_fx_unit()
        else:
            self.__view.select_fx_preset(self.__selected_fx_preset_id)

    def set_midi_mapping(self, fx_parameter_number, midi_mapping):
        self.__fx_presets[self.__selected_fx_preset_id].set_midi_mapping(fx_parameter_number, midi_mapping)

    def view_update_fx_params_from_plugins(self):
        self.__fx_presets[self.__selected_fx_preset_id].view_update_fx_params_from_plugins()

    def set_fx_parameter_level(self, fx_param_id, fx_param_level):
            self.__fx_presets[self.__selected_fx_preset_id].set_fx_parameter_level(fx_param_id, fx_param_level)

    def __view_update_stats(self):
        self.__view.select_fx_page(self.__fx_page_number)

        for fx_preset_id in self.__fx_presets:
            self.__fx_presets[fx_preset_id].view_update_fx_preset_availability()

        self.__fx_presets[self.__selected_fx_preset_id].view_update_fx_params_from_plugins()
        self.__fx_presets[self.__selected_fx_preset_id].view_update_active_fx_unit()

    def change_active_fx_unit(self):
        active_fx_unit = self.__fx_presets[self.__selected_fx_preset_id].get_active_fx_unit()

        if active_fx_unit == FxUnit.FX_UNIT_CUSTOM:
            print(self.__context.device_name + ': ' + FxPresetPage.change_active_fx_unit.__name__ + ": to manipulator")
            self.__fx_presets[self.__selected_fx_preset_id].set_active_fx_unit(FxUnit.FX_UNIT_MANIPULATOR)
        elif active_fx_unit == FxUnit.FX_UNIT_MANIPULATOR:
            print(self.__context.device_name + ': ' + FxPresetPage.change_active_fx_unit.__name__ + ": to finisher voodoo")
            self.__fx_presets[self.__selected_fx_preset_id].set_active_fx_unit(FxUnit.FX_UNIT_FINISHER_VOODOO)
        elif active_fx_unit == FxUnit.FX_UNIT_FINISHER_VOODOO:
            print(self.__context.device_name + ': ' + FxPresetPage.change_active_fx_unit.__name__ + ": to custom")
            self.__fx_presets[self.__selected_fx_preset_id].set_active_fx_unit(FxUnit.FX_UNIT_CUSTOM)

        self.__fx_presets[self.__selected_fx_preset_id].view_update_active_fx_unit()

    def set_active_fx_unit(self, active_fx_unit):
        self.__fx_presets[self.__selected_fx_preset_id].set_active_fx_unit(active_fx_unit)
        self.__fx_presets[self.__selected_fx_preset_id].view_update_active_fx_unit()

    def get_active_fx_unit(self):
        return self.__fx_presets[self.__selected_fx_preset_id].get_active_fx_unit()