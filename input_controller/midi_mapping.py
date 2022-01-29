'''
Created on Jan 24, 2022

@author: Dream Machines
'''

from input_controller import constants

class MidiMapping:
    def __init__(self,
                 plugin_number = constants.INVALID_PARAM,
                 parameter_id = constants.INVALID_PARAM):
        self.__plugin_number = plugin_number
        self.__parameter_id = parameter_id

    def isValid(self):
        return (self.__plugin_number >= constants.MIN_PLUGIN_NUMBER and self.__plugin_number <= constants.MAX_PLUGIN_NUMBER) and\
               (self.__parameter_id >= 0)

    def getPluginNumber(self):
        return self.__plugin_number

    def getParameterId(self):
        return self.__parameter_id

    def convertToList(self):
        result = []
        result.append(self.__plugin_number)
        result.append(self.__parameter_id)
        return result

    @staticmethod
    def createFromList(input_list):
        result = None
        if len(input_list) == 2:
            plugin_number = input_list[0]
            parameter_id = input_list[1]
            result = MidiMapping(plugin_number, parameter_id)
        return result