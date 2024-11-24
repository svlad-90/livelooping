'''
Created on Jan 24, 2022

@author: Dream Machines
'''

import math

import playlist

from input_controller import constants
from input_controller.fx_unit import FxUnit


class PersistencyItem:

    def __init__(self, track_id):
        self.__track_id = track_id
        self.__data = {}  # key - data_key, data - any storable data type

    def init(self):
        self.read_from_storage()

    # plugin parameters
    def set_mixer_parameters(self, plugin_parameters):
        self.__data[constants.PERSISTENCY_MIXER_PARAMETERS_KEY] = plugin_parameters

    def get_mixer_parameters(self):
        return self.__data[constants.PERSISTENCY_MIXER_PARAMETERS_KEY]

    def reset_mixer_parameters(self):
        self.__data[constants.PERSISTENCY_MIXER_PARAMETERS_KEY] = {}

    def delete_mixer_parameters(self):
        if self.__data.get(constants.PERSISTENCY_MIXER_PARAMETERS_KEY) != None:
            del self.__data[constants.PERSISTENCY_MIXER_PARAMETERS_KEY]

    def is_mixer_parameters_available(self):
        return self.__data.get(constants.PERSISTENCY_MIXER_PARAMETERS_KEY) != None

    # turnado patch
    def set_turnado_patch(self, patch_id):
        self.__data[constants.PERSISTENCY_TURNADO_PATCH_KEY] = patch_id

    def get_turnado_patch(self):
        return self.__data[constants.PERSISTENCY_TURNADO_PATCH_KEY]

    def reset_turnado_patch(self):
        self.__data[constants.PERSISTENCY_TURNADO_PATCH_KEY] = 0

    def is_turnado_patch_available(self):
        return self.__data.get(constants.PERSISTENCY_TURNADO_PATCH_KEY) != None

    # midi mapping
    def set_midi_mapping(self, midi_mapping):
        self.__data[constants.PERSISTENCY_MIDI_MAPPING_KEY] = midi_mapping

    def get_midi_mapping(self):
        return self.__data[constants.PERSISTENCY_MIDI_MAPPING_KEY]

    def reset_midi_mapping(self):
        self.__data[constants.PERSISTENCY_MIDI_MAPPING_KEY] = {}

    def delete_midi_mapping(self):
        if self.__data.get(constants.PERSISTENCY_MIDI_MAPPING_KEY) != None:
            del self.__data[constants.PERSISTENCY_MIDI_MAPPING_KEY]

    def is_midi_mapping_available(self):
        return self.__data.get(constants.PERSISTENCY_MIDI_MAPPING_KEY) != None

    # active fx unit
    def set_active_fx_unit(self, active_fx_unit):
        self.__data[constants.PERSISTENCY_ACTIVE_FX_UNIT_KEY] = active_fx_unit

    def get_active_fx_unit(self):
        return self.__data[constants.PERSISTENCY_ACTIVE_FX_UNIT_KEY]

    def reset_active_fx_unit(self):
        self.__data[constants.PERSISTENCY_ACTIVE_FX_UNIT_KEY] = FxUnit.FX_UNIT_CUSTOM

    def delete_active_fx_unit(self):
        if self.__data.get(constants.PERSISTENCY_ACTIVE_FX_UNIT_KEY) != None:
            del self.__data[constants.PERSISTENCY_ACTIVE_FX_UNIT_KEY]

    def is_active_fx_unit_available(self):
        return self.__data.get(constants.PERSISTENCY_MIDI_MAPPING_KEY) != None

    # general operations
    def reset_storage(self):
        self.reset_data()
        playlist.setTrackName(self.__track_id, "")

    def write_to_storage(self):
        self.__data[constants.PERSISTENCY_VERSION_KEY] = constants.PERSISTENCY_CURRENT_VERSION
        playlist.setTrackName(self.__track_id, str(self.__data))

    def read_from_storage(self):
        data_str = playlist.getTrackName(self.__track_id)

        if data_str:
            try:
                data = {}
                if data_str.startswith("{"):
                    data = eval(data_str)

                    found_version = data.get(constants.PERSISTENCY_VERSION_KEY)

                    if found_version != None:
                        if found_version != constants.PERSISTENCY_CURRENT_VERSION:
                            print("Version mismatch identified. Old version - " + str(found_version) + \
                                  ", new version - " + str(constants.PERSISTENCY_CURRENT_VERSION) + ".")
                            print("Data migration procedure activated ...")
                            self.handle_version_mismatch(data, found_version, constants.PERSISTENCY_CURRENT_VERSION)
                            self.__data = data
                            self.write_to_storage()
                            print("Data migration procedure finished ...")
                        else:
                            self.__data = data
                    else:
                        # reset all fields, so that they exist as empty ones
                        self.reset_data()
                        # old era. Read data as related to plugins
                        self.__data[constants.PERSISTENCY_MIXER_PARAMETERS_KEY] = data
                        # we need to save data in new format
                        self.write_to_storage()
                else:
                    self.reset_data()
                    self.__data[constants.PERSISTENCY_MIXER_PARAMETERS_KEY] = data
                    self.write_to_storage()
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Failed to apply data migration! Fallback to the data reset!")
                self.reset_data()

    def reset_data(self):
        self.reset_mixer_parameters()
        self.reset_midi_mapping()
        self.reset_turnado_patch()
        self.reset_active_fx_unit()
        self.__data[constants.PERSISTENCY_VERSION_KEY] = constants.PERSISTENCY_CURRENT_VERSION

    def __data_update_from_2_11_to_3_0(self, data):
        print("Start migration to version 3.0 ...")
        data.clear()
        data[constants.PERSISTENCY_MIDI_MAPPING_KEY] = {0:[-1,-1,-1],
                              1:[-1,-1,-1],
                              2:[-1,-1,-1],
                              3:[-1,-1,-1],
                              4:[-1,-1,-1],
                              5:[-1,-1,-1],
                              6:[-1,-1,-1],
                              7:[-1,-1,-1]}
        data[constants.PERSISTENCY_MIXER_PARAMETERS_KEY] = {}
        data[constants.PERSISTENCY_ACTIVE_FX_UNIT_KEY] = 0
        data[constants.PERSISTENCY_TURNADO_PATCH_KEY] = 0.0
        print("Finished migration to version 3.0 ...")

    def handle_version_mismatch(self, data, old_version, _):

        supported_version_updates = {
            "1.0": self.__data_update_from_2_11_to_3_0,
            "2.0": self.__data_update_from_2_11_to_3_0,
            "2.1": self.__data_update_from_2_11_to_3_0,
            "2.2": self.__data_update_from_2_11_to_3_0,
            "2.3": self.__data_update_from_2_11_to_3_0,
            "2.4": self.__data_update_from_2_11_to_3_0,
            "2.5": self.__data_update_from_2_11_to_3_0,
            "2.6": self.__data_update_from_2_11_to_3_0,
            "2.7": self.__data_update_from_2_11_to_3_0,
            "2.8": self.__data_update_from_2_11_to_3_0,
            "2.9": self.__data_update_from_2_11_to_3_0,
            "2.10": self.__data_update_from_2_11_to_3_0,
            "2.11": self.__data_update_from_2_11_to_3_0,
        }

        start = False

        for key, value in supported_version_updates.items():
            if isinstance(old_version, float):
                if key == str(old_version):
                    start = True
            else:
                if key == old_version:
                    start = True
            if start:
                value(data)
