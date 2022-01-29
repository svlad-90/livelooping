import plugins

MIDI_MAX_VALUE = 127
MAX_VOLUME_LEVEL_VALUE   = 0.8

def printAllPluginParameters(mixer_track, slot):

    number_of_params = plugins.getParamCount(mixer_track, slot)
    plugin_name = plugins.getPluginName(mixer_track, slot)

    print("Parameters of the plugin \"" + plugin_name + "\":")

    for param_index in range(number_of_params):
        print( "#" + str(param_index) + ": param name - " + plugins.getParamName(param_index, mixer_track, slot) + \
               " param value - " + str( plugins.getParamValue(param_index, mixer_track, slot) ) )

class PluginParametersCache:

    __cache = {}

    @staticmethod
    def findParameterByName(mixer_channel, parameter_name, slot_index):
        plugin_key = PluginParametersCache.CachePluginKey(mixer_channel, slot_index)
    
        found_item = PluginParametersCache.__cache.get(plugin_key)
        
        if found_item != None:
            return found_item.getPluginParameterId(parameter_name)
        else:
            cached_plugin_data_item = PluginParametersCache.CachedPluginDataItem(mixer_channel, slot_index)
            PluginParametersCache.__cache[plugin_key] = cached_plugin_data_item
            return cached_plugin_data_item.getPluginParameterId(parameter_name)

    class CachePluginKey:
        def __init__(self, mixer_track, slot):
            self.__mixer_track = mixer_track
            self.__slot = slot
    
        def __hash__(self):
            return hash((self.__mixer_track, self.__slot))
    
        def __eq__(self, other):
            return (self.__mixer_track, self.__slot) == (other.__mixer_track, other.__slot)

    class CachedPluginDataItem:
        def __init__(self, mixer_channel, slot_index):
            self.__mixer_channel = mixer_channel
            self.__slot_index = slot_index
            self.__fetched_up_to = 0
            self.__fetched_parameter_ids = {}
            
        def __cacheAndGetPluginParmaters(self, parameter_name):            
            number_of_parameters = plugins.getParamCount(self.__mixer_channel, self.__slot_index)
    
            for parameter_id in range(self.__fetched_up_to, number_of_parameters):
                fetched_parameter_name = plugins.getParamName(parameter_id, self.__mixer_channel, self.__slot_index)
                self.__fetched_up_to = parameter_id
                self.__fetched_parameter_ids[fetched_parameter_name] = parameter_id
                if(fetched_parameter_name == parameter_name):
                    return parameter_id
            raise Exception("Parameter id for '" + parameter_name + "' was not found")
    
        def getPluginParameterId(self, parameter_name):
            found_plugin_id = self.__fetched_parameter_ids.get(parameter_name)

            result = None

            if found_plugin_id != None:
                result = found_plugin_id
            else:
                result = self.__cacheAndGetPluginParmaters(parameter_name)

            return result

def findParameterByName(mixer_channel, parameter_name, slot_index):
    return PluginParametersCache.findParameterByName(mixer_channel, parameter_name, slot_index)

# mapping formula from 0<->1016 to 0<->1 values
def externalParamMapping(param_value):
    
    base = param_value / 8.0
    base_int = int(base)
    base_diff = base - base_int
    
    if base_int == 127.0:
        return 1.0
    elif base_int == 0.0:
        return 0.0
    else:
        first_part = 1 / pow( 2, ( 127.0 - base_int ) )
        second_part = first_part * base_diff
        return first_part + second_part