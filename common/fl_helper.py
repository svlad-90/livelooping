import plugins

MIDI_MAX_VALUE = 127

def printAllPluginParameters(mixer_track, slot):

    number_of_params = plugins.getParamCount(mixer_track, slot)
    plugin_name = plugins.getPluginName(mixer_track, slot)

    print("Parameters of the plugin \"" + plugin_name + "\":")

    for param_index in range(number_of_params):
        print( "#" + str(param_index) + ": param name - " + plugins.getParamName(param_index, mixer_track, slot) + \
               " param value - " + str( plugins.getParamValue(param_index, mixer_track, slot) ) )

def findSurfaceControlElementIdByName(mixer_channel, control_element_name, slot_index):
    number_of_parameters = plugins.getParamCount(mixer_channel, slot_index)

    for parameter_id in range(number_of_parameters):
        parameter_name = plugins.getParamName(parameter_id, mixer_channel, slot_index)
        if(parameter_name == control_element_name):
            return parameter_id
    raise Exception("Control element " + control_element_name + " not found")