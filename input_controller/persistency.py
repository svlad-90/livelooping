'''
Created on Jan 24, 2022

@author: Dream Machines
'''

import playlist

from input_controller import constants
from input_controller.fx_unit import FXUnit

class PersistencyItem:
    def __init__(self, track_id):
        self.__track_id = track_id
        self.__data = {} # key - data_key, data - any storable data type
        
        

    def init(self):
        self.readFromStorage() 

    # plugin parameters
    def setPluginParameters(self, plugin_parameters):
        self.__data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY] = plugin_parameters
    def getPluginParameters(self):
        return self.__data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]
    def resetPluginParameters(self):
        self.__data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY] = {}
    def deletePluginParameters(self):
        if self.__data.get(constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY) != None:
            del self.__data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY]
    def isPluginParametersAvailable(self):
        return self.__data.get(constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY) != None

    # midi mapping
    def setMidiMapping(self, midi_mapping):
        self.__data[constants.PERSISTENCY_MIDI_MAPPING_KEY] = midi_mapping
    def getMidiMapping(self):
        return self.__data[constants.PERSISTENCY_MIDI_MAPPING_KEY]
    def resetMidiMapping(self):
        self.__data[constants.PERSISTENCY_MIDI_MAPPING_KEY] = {}
    def deleteMidiMapping(self):
        if self.__data.get(constants.PERSISTENCY_MIDI_MAPPING_KEY) != None:
            del self.__data[constants.PERSISTENCY_MIDI_MAPPING_KEY]
    def isMidiMappingAvailable(self):
        return self.__data.get(constants.PERSISTENCY_MIDI_MAPPING_KEY) != None

    # active fx unit
    def setActiveFxUnit(self, active_fx_unit):
        self.__data[constants.PERSISTENCY_ACTIVE_FX_UNIT_KEY] = active_fx_unit
    def getActiveFxUnit(self):
        return self.__data[constants.PERSISTENCY_ACTIVE_FX_UNIT_KEY]
    def resetActiveFxUnit(self):
        self.__data[constants.PERSISTENCY_ACTIVE_FX_UNIT_KEY] = FXUnit.FX_UNIT_CUSTOM
    def deleteActiveFxUnit(self):
        if self.__data.get(constants.PERSISTENCY_ACTIVE_FX_UNIT_KEY) != None:
            del self.__data[constants.PERSISTENCY_ACTIVE_FX_UNIT_KEY]
    def isActiveFxUnitAvailable(self):
        return self.__data.get(constants.PERSISTENCY_MIDI_MAPPING_KEY) != None

    # general operations
    def resetStorage(self):
        self.__data[constants.PERSISTENCY_VERSION_KEY] = constants.PERSISTENCY_CURRENT_VERSION
        playlist.setTrackName(self.__track_id,  "")

    def writeToStorage(self):
        self.__data[constants.PERSISTENCY_VERSION_KEY] = constants.PERSISTENCY_CURRENT_VERSION
        playlist.setTrackName(self.__track_id,  str(self.__data))

    def readFromStorage(self):
        data_str = playlist.getTrackName(self.__track_id)

        if data_str:
            try:
                data = eval(data_str)

                found_version = data.get(constants.PERSISTENCY_VERSION_KEY)

                if found_version != None:
                    # new era
                    if found_version != constants.PERSISTENCY_CURRENT_VERSION:
                        self.handleVersionMismatch(found_version, constants.PERSISTENCY_CURRENT_VERSION, self.__data)
                    self.__data = data
                    pass
                else:
                    # reset all fields, so that they exist as empty ones
                    self.resetData()
                    # old era. Read data as related to plugins
                    self.__data[constants.PERSISTENCY_PLUGIN_PARAMETERS_KEY] = data
                    # we need to save data in new format
                    self.writeToStorage()
            except Exception as e:
                self.resetData()

    def resetData(self):
        self.resetPluginParameters()
        self.resetMidiMapping()
        self.resetActiveFxUnit()
        self.__data[constants.PERSISTENCY_VERSION_KEY] = constants.PERSISTENCY_CURRENT_VERSION

    def handleVersionMismatch(self, old_version, new_version, data):
        pass