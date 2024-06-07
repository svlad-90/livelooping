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
                        # new era
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
                        self.__data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY] = data
                        # we need to save data in new format
                        self.write_to_storage()
                else:
                    self.reset_data()
                    self.__data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY] = data
                    self.write_to_storage()
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Failed to apply data migration! Fallback to the data reset!")
                self.reset_data()

    def reset_data(self):
        self.reset_plugin_parameters()
        self.reset_midi_mapping()
        self.reset_turnado_patch()
        self.reset_active_fx_unit()
        self.__data[constants.PERSISTENCY_VERSION_KEY] = constants.PERSISTENCY_CURRENT_VERSION

    def __data_update_from_1_0_to_2_0(self, data):
        print("Version update from 1.0 to 2.0 has started ...")

        # CONSTANTS

        FX_ACTIVATION_STATE_SLOT_INDEX_DEPRECATED = 10
        PERSISTENCY_PLUGIN_PARAMETERS_KEY = "PLUGIN_PARAMS"
        FX_ACTIVATION_STATE_CHANNEL_INDEX = 99

        # LOGIC

        plugin_params = data[PERSISTENCY_PLUGIN_PARAMETERS_KEY]
        per_channel_plugin_params = {}
        # We need to transfer slot index activation data to new key
        if FX_ACTIVATION_STATE_SLOT_INDEX_DEPRECATED in plugin_params:
            slot_index_activation_data = plugin_params[FX_ACTIVATION_STATE_SLOT_INDEX_DEPRECATED]
            per_channel_plugin_params[FX_ACTIVATION_STATE_CHANNEL_INDEX] = slot_index_activation_data
            del plugin_params[FX_ACTIVATION_STATE_SLOT_INDEX_DEPRECATED]
        # We need to refactor the structure of the plugins parameters
        per_channel_plugin_params[-1] = plugin_params
        data[PERSISTENCY_PLUGIN_PARAMETERS_KEY] = per_channel_plugin_params
        print("Version update from 1.0 to 2.0 has finished ...")

    def __data_update_from_2_0_to_2_1(self, data):
        print("Version update from 2.0 to 2.1 has started ...")

        # CONSTANTS

        PERSISTENCY_PLUGIN_PARAMETERS_KEY = "PLUGIN_PARAMS"
        FX_ACTIVATION_STATE_CHANNEL_INDEX = 99
        NUMBER_OF_ACTIVATION_SLOTS = 20

        # LOGIC

        plugin_params = data[PERSISTENCY_PLUGIN_PARAMETERS_KEY]
        slot_activation_statuses = plugin_params[FX_ACTIVATION_STATE_CHANNEL_INDEX]
        slot_activation_statuses_length = len(slot_activation_statuses)
        if slot_activation_statuses_length < NUMBER_OF_ACTIVATION_SLOTS:
            for _ in range(NUMBER_OF_ACTIVATION_SLOTS - slot_activation_statuses_length):
                slot_activation_statuses.append('0.0')
        print("Version update from 2.0 to 2.1 has finished ...")

    def __data_update_from_2_1_to_2_2(self, data):
        print("Version update from 2.1 to 2.2 has started ...")

        # CONSTANTS

        PERSISTENCY_PLUGIN_PARAMETERS_KEY = "PLUGIN_PARAMS"
        FX_ACTIVATION_STATE_CHANNEL_INDEX = 99
        MAX_SLOT_INDEX_PER_CHANNEL = 10

        # LOGIC

        plugin_params = data[PERSISTENCY_PLUGIN_PARAMETERS_KEY]
        slot_activation_statuses = plugin_params[FX_ACTIVATION_STATE_CHANNEL_INDEX]

        new_slot_activation_statuses = {0: [], 1: []}

        for activation_slot_idx, activation_slot_status in enumerate(slot_activation_statuses):
            if math.floor(activation_slot_idx / MAX_SLOT_INDEX_PER_CHANNEL) == 0:
                channel_idx = 1
            if math.floor(activation_slot_idx / MAX_SLOT_INDEX_PER_CHANNEL) == 1:
                channel_idx = 0

            new_slot_activation_statuses[channel_idx].append(activation_slot_status)

        plugin_params[FX_ACTIVATION_STATE_CHANNEL_INDEX] = new_slot_activation_statuses

        print("Version update from 2.1 to 2.2 has finished ...")

    def __data_update_from_2_2_to_2_3(self, data):
        print("Version update from 2.2 to 2.3 has started ...")

        # CONSTANTS

        PERSISTENCY_TURNADO_PATCH_KEY = "TURNADO_PATCH"

        # LOGIC

        data[PERSISTENCY_TURNADO_PATCH_KEY] = 0

        print("Version update from 2.2 to 2.3 has finished ...")

    def __data_update_from_2_3_to_2_4(self, data):
        print("Version update from 2.3 to 2.4 has started ...")

        # CONSTANTS

        PERSISTENCY_TURNADO_PATCH_KEY = "TURNADO_PATCH"

        # LOGIC

        data[PERSISTENCY_TURNADO_PATCH_KEY] = 0.0079

        print("Version update from 2.3 to 2.4 has finished ...")

    def __data_update_from_2_4_to_2_5(self, data):
        print("Version update from 2.4 to 2.5 has started ...")

        fx_1_channel_mic = 6
        fx_1_channel_synth = 11

        # LOGIC
        if fx_1_channel_mic in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]:
            if constants.FX1_MULTIBAND_COMPRESSOR_SLOT_INDEX in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][fx_1_channel_mic]:
                bypass_parameter_index = 0
                data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][fx_1_channel_mic][constants.FX1_MULTIBAND_COMPRESSOR_SLOT_INDEX][bypass_parameter_index] = 0.00


        if fx_1_channel_synth in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]:
            if constants.FX1_MULTIBAND_COMPRESSOR_SLOT_INDEX in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][fx_1_channel_synth]:
                bypass_parameter_index = 0
                data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][fx_1_channel_synth][constants.FX1_MULTIBAND_COMPRESSOR_SLOT_INDEX][bypass_parameter_index] = 0.00

        print("Version update from 2.4 to 2.5 has finished ...")

    def __data_update_from_2_5_to_2_6(self, data):
        print("Version update from 2.5 to 2.6 has started ...")

        # LOGIC
        fx_2_channel_mic = 5
        fx_2_channel_synth = 10

        if fx_2_channel_mic in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]:
            if constants.FX2_MANIPULATOR_SLOT_INDEX in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][fx_2_channel_mic]:
                for i in reversed(range(191, 201)):
                    data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][fx_2_channel_mic][constants.FX2_MANIPULATOR_SLOT_INDEX].pop(i)

        if fx_2_channel_synth in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]:
            if constants.FX2_MANIPULATOR_SLOT_INDEX in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][fx_2_channel_synth]:
                for i in reversed(range(191, 201)):
                    data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][fx_2_channel_synth][constants.FX2_MANIPULATOR_SLOT_INDEX].pop(i)

        print("Version update from 2.5 to 2.6 has finished ...")

    def __data_update_from_2_6_to_2_7(self, data):
        print("Version update from 2.6 to 2.7 has started ...")

        # LOGIC
        fx_1_channel_mic = 6
        fx_1_channel_synth = 11
        MULTIBAND_COMPRESSOR_PARAMS_LIMIT = 56
        MULTIBAND_COMPRESSOR_PARAMS_OLD_LIMIT = 4239

        if fx_1_channel_mic in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]:
            if constants.FX1_MULTIBAND_COMPRESSOR_SLOT_INDEX in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][fx_1_channel_mic]:
                for i in reversed(range(MULTIBAND_COMPRESSOR_PARAMS_LIMIT, MULTIBAND_COMPRESSOR_PARAMS_OLD_LIMIT)):
                    data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][fx_1_channel_mic][constants.FX1_MULTIBAND_COMPRESSOR_SLOT_INDEX].pop(i)

        if fx_1_channel_synth in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]:
            if constants.FX1_MULTIBAND_COMPRESSOR_SLOT_INDEX in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][fx_1_channel_synth]:
                for i in reversed(range(MULTIBAND_COMPRESSOR_PARAMS_LIMIT, MULTIBAND_COMPRESSOR_PARAMS_OLD_LIMIT)):
                    data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][fx_1_channel_synth][constants.FX1_MULTIBAND_COMPRESSOR_SLOT_INDEX].pop(i)

        print("Version update from 2.6 to 2.7 has finished ...")

    def __data_update_from_2_7_to_2_8(self, data):
        print("Version update from 2.7 to 2.8 has started ...")

        # LOGIC

        old_mic_fx_1_channel = 6
        new_mic_fx_1_channel = 10
        old_mic_fx_2_channel = 5
        new_mic_fx_2_channel = 9
        old_synth_fx_1_channel = 11
        new_synth_fx_1_channel = 15
        old_synth_fx_2_channel = 10
        new_synth_fx_2_channel = 14

        is_mic = old_mic_fx_1_channel in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]

        if is_mic:
            if old_mic_fx_1_channel in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]:
                data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][new_mic_fx_1_channel] = data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][old_mic_fx_1_channel]
                del data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][old_mic_fx_1_channel]
            if old_mic_fx_2_channel in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]:
                data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][new_mic_fx_2_channel] = data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][old_mic_fx_2_channel]
                del data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][old_mic_fx_2_channel]

            for _, value in data[constants.PERSISTENCY_MIDI_MAPPING_KEY].items():
                if value[0] != constants.INVALID_PARAM:
                    if value[2] == constants.INVALID_PARAM:
                        value[2] = new_mic_fx_2_channel
                    else:
                        if value[2] == old_mic_fx_1_channel:
                            value[2] = new_mic_fx_1_channel
                        elif value[2] == old_mic_fx_2_channel:
                            value[2] = new_mic_fx_2_channel

        else:
            if old_synth_fx_1_channel in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]:
                data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][new_synth_fx_1_channel] = data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][old_synth_fx_1_channel]
                del data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][old_synth_fx_1_channel]

            if old_synth_fx_2_channel in data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]:
                data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][new_synth_fx_2_channel] = data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][old_synth_fx_2_channel]
                del data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY][old_synth_fx_2_channel]

            for _, value in data[constants.PERSISTENCY_MIDI_MAPPING_KEY].items():
                if value[0] != constants.INVALID_PARAM:
                    if value[2] == constants.INVALID_PARAM:
                        value[2] = new_synth_fx_2_channel
                    else:
                        if value[2] == old_synth_fx_1_channel:
                            value[2] = new_synth_fx_1_channel
                        elif value[2] == old_synth_fx_2_channel:
                            value[2] = new_synth_fx_2_channel

        print("Version update from 2.7 to 2.8 has finished ...")

    def handle_version_mismatch(self, data, old_version, _):

        supported_version_updates = {
            1.0: self.__data_update_from_1_0_to_2_0,
            2.0: self.__data_update_from_2_0_to_2_1,
            2.1: self.__data_update_from_2_1_to_2_2,
            2.2: self.__data_update_from_2_2_to_2_3,
            2.3: self.__data_update_from_2_3_to_2_4,
            2.4: self.__data_update_from_2_4_to_2_5,
            2.5: self.__data_update_from_2_5_to_2_6,
            2.6: self.__data_update_from_2_6_to_2_7,
            2.7: self.__data_update_from_2_7_to_2_8,
        }

        start = False

        for key, value in supported_version_updates.items():
            if key == old_version:
                start = True
            if start:
                value(data)
