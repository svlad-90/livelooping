import plugins

MIDI_MAX_VALUE = 127
MAX_VOLUME_LEVEL_VALUE   = 0.8

def print_all_plugin_parameters(mixer_track, slot):

    number_of_params = plugins.getParamCount(mixer_track, slot, True)
    plugin_name = plugins.getPluginName(mixer_track, slot, True)

    print("Parameters of the plugin \"" + plugin_name + "\":")

    for param_index in range(number_of_params):
        print( "#" + str(param_index) + ": param name - " + plugins.getParamName(param_index, mixer_track, slot, True) + \
               " param value - " + str( plugins.getParamValue(param_index, mixer_track, slot) ) , True)

def print_midi_event(event):
        print("handled - " + str(event.handled) + "; "
              "timestamp - " + str(event.timestamp) + "; "
              "data1 - " + str(event.data1) + "; "
              "data2 - " + str(event.data2) + "; "
              "port - " + str(event.port) + "; "
              "note - " + str(event.note) + "; "
              "velocity - " + str(event.velocity) + "; "
              "pressure - " + str(event.pressure) + "; "
              "progNum - " + str(event.progNum) + "; "
              "controlNum - " + str(event.controlNum) + "; "
              "controlVal - " + str(event.controlVal) + "; "
              "pitchBend - " + str(event.pitchBend) + "; "
              "sysex - " + str(event.sysex) + "; "
              "isIncrement - " + str(event.isIncrement) + "; "
              "res - " + str(event.res) + "; "
              "inEv - " + str(event.inEv) + "; "
              "outEv - " + str(event.outEv) + "; "
              "midiId - " + str(event.midiId) + "; "
              "midiChan - " + str(event.midiChan) + "; "
              "midiChanEx - " + str(event.midiChanEx) + "; ")

def is_kp3_program_change_event(event):
    return event.midiId == 192

class PluginParametersCache:

    __cache = {}

    @staticmethod
    def find_parameter_by_name(mixer_channel, parameter_name, slot_index):
        plugin_key = PluginParametersCache.CachePluginKey(mixer_channel, slot_index)

        found_item = PluginParametersCache.__cache.get(plugin_key)

        if found_item != None:
            return found_item.get_plugin_parameter_id(parameter_name)
        else:
            CachedPluginDataItem = PluginParametersCache.CachedPluginDataItem(mixer_channel, slot_index)
            PluginParametersCache.__cache[plugin_key] = CachedPluginDataItem
            return CachedPluginDataItem.get_plugin_parameter_id(parameter_name)

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

        def __cache_and_get_plugin_parmaters(self, parameter_name):
            number_of_parameters = plugins.getParamCount(self.__mixer_channel, self.__slot_index, True)

            for parameter_id in range(self.__fetched_up_to, number_of_parameters):
                fetched_parameter_name = plugins.getParamName(parameter_id, self.__mixer_channel, self.__slot_index, True)
                self.__fetched_up_to = parameter_id
                self.__fetched_parameter_ids[fetched_parameter_name] = parameter_id
                if(fetched_parameter_name == parameter_name):
                    return parameter_id
            raise Exception("Parameter id for '" + parameter_name + "' was not found")

        def get_plugin_parameter_id(self, parameter_name):
            found_plugin_id = self.__fetched_parameter_ids.get(parameter_name)

            result = None

            if found_plugin_id != None:
                result = found_plugin_id
            else:
                result = self.__cache_and_get_plugin_parmaters(parameter_name)

            return result

def find_parameter_by_name(mixer_channel, parameter_name, slot_index):
    return PluginParametersCache.find_parameter_by_name(mixer_channel, parameter_name, slot_index)