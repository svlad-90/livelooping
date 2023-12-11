'''
Created on Jan 24, 2022

@author: Dream Machines
'''

from input_controller import constants

class MidiMapping:
    def __init__(self,
                 plugin_number = constants.INVALID_PARAM,
                 parameter_id = constants.INVALID_PARAM,
                 channel_id = constants.INVALID_PARAM):
        self.__plugin_number = plugin_number
        self.__parameter_id = parameter_id
        self.__channel_id = channel_id

    def is_valid(self):
        return (self.__plugin_number >= constants.MIN_PLUGIN_NUMBER and self.__plugin_number <= constants.MAX_PLUGIN_NUMBER) and\
               (self.__parameter_id >= 0)

    def get_plugin_number(self):
        return self.__plugin_number

    def get_parameter_id(self):
        return self.__parameter_id

    def get_channel_id(self):
        return self.__channel_id

    def convert_to_list(self):
        result = []
        result.append(self.__plugin_number)
        result.append(self.__parameter_id)
        result.append(self.__channel_id)
        return result

    @staticmethod
    def create_from_list(input_list):
        result = None
        if len(input_list) == 2:
            plugin_number = input_list[0]
            parameter_id = input_list[1]
            channel_id = constants.INVALID_PARAM
            result = MidiMapping(plugin_number, parameter_id, channel_id)
        elif len(input_list) == 3:
            plugin_number = input_list[0]
            parameter_id = input_list[1]
            channel_id = input_list[2]
            result = MidiMapping(plugin_number, parameter_id, channel_id)
        return result
