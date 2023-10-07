'''
Created on Jan 24, 2022

@author: Dream Machines
'''

import playlist

from input_controller import constants
from input_controller.fx_unit import FxUnit

class PersistencyItem:
    def __init__(self, track_id):
        self.__track_id = track_id
        self.__data = {} # key - data_key, data - any storable data type



    def init(self):
        self.read_from_storage()

    # plugin parameters
    def set_plugin_parameters(self, plugin_parameters):
        self.__data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY] = plugin_parameters
    def get_plugin_parameters(self):
        return self.__data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]
    def reset_plugin_parameters(self):
        self.__data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY] = {}
    def delete_plugin_parameters(self):
        if self.__data.get(constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY) != None:
            del self.__data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]
    def is_plugin_parameters_available(self):
        return self.__data.get(constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY) != None

    # midi mapping
    def set_midi_mapping(self, midi_mapping):
        self.__data[constants.PERSISTENCY_MIDI_MAPPING_KEY] = midi_mapping
    def get_midi_mapping(self):
        return self.__data[constants.PERSISTENCY_MIDI_MAPPING_KEY]
    def reset_midi_mapping(self):
        self.__data[constants.PERSISTENCY_MIDI_MAPPING_KEY] = {}
    def deletemidi_mapping(self):
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
        playlist.setTrackName(self.__track_id,  "")

    def write_to_storage(self):
        self.__data[constants.PERSISTENCY_VERSION_KEY] = constants.PERSISTENCY_CURRENT_VERSION
        playlist.setTrackName(self.__track_id,  str(self.__data))

    def read_from_storage(self):
        data_str = playlist.getTrackName(self.__track_id)

        if data_str:
            try:
                data = eval(data_str)

                found_version = data.get(constants.PERSISTENCY_VERSION_KEY)

                if found_version != None:
                    # new era
                    if found_version != constants.PERSISTENCY_CURRENT_VERSION:
                        self.handle_version_mismatch(found_version, constants.PERSISTENCY_CURRENT_VERSION, self.__data)
                    self.__data = data
                    pass
                else:
                    # reset all fields, so that they exist as empty ones
                    self.reset_data()
                    # old era. Read data as related to plugins
                    self.__data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY] = data
                    # we need to save data in new format
                    self.write_to_storage()
            except Exception as e:
                self.reset_data()

    def reset_data(self):
        self.reset_plugin_parameters()
        self.reset_midi_mapping()
        self.reset_active_fx_unit()
        self.__data[constants.PERSISTENCY_VERSION_KEY] = constants.PERSISTENCY_CURRENT_VERSION

    def handle_version_mismatch(self, old_version, new_version, data):
        pass