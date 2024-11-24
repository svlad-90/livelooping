'''
Created on Nov 23, 2024

@author: Dream Machines
'''

import midi
import mixer
import plugins
import general

from input_controller import constants
from common import fl_helper

PLUGIN_ACTIVATION_STORAGE_KEY = "PL_ACTIVATION"
PLUGIN_MIX_LEVEL_STORAGE_KEY = "PL_MIX_LEVEL"
PLUGIN_PARAMETERS_STORAGE_KEY = "PL_PARAMETERS"
MIXER_CHANNEL_VOLUME_KEY = "M_CH_VOLUME"
MIXER_CHANNEL_PAN_KEY = "M_CH_PAN"
MIXER_CHANNEL_STEREO_SEPARATION_KEY = "M_CH_ST_SEP"
INPUT_MIXER_CHANNEL_ROUTING_LEVELS = "M_IN_CH_ROUTING"

class DAWFxPlugin:
    def __init__(self, mixer_channel_id, plugin_slot_id):
        self.__mixer_channel_id = mixer_channel_id
        self.__plugin_slot_id = plugin_slot_id      

    def on_init_script(self):
        pass


    def __calc_params_limit(self):
        result = 4096
        if self.__is_valid():
            name = plugins.getPluginName(self.__mixer_channel_id, self.__plugin_slot_id)
            if name == "C6 Stereo":
                result = constants.MULTIBAND_COMPRESSOR_PARAMS_LIMIT
            elif name == "Pro-Q 3":
                result = constants.FABFILTER_PRO_Q3_PARAMS_LIMIT
            elif name == "ValhallaVintageVerb":
                result = constants.VALHALLA_VINTAGE_VERB_PARAMS_LIMIT
            elif name == "H-Delay Stereo":
                result = constants.WAVES_H_DELAY_PARAMS_LIMIT
            elif name == "Manipulator":
                result = constants.MANIPULATOR_PARAMS_LIMIT
            elif name == "NS1 Stereo":
                result = constants.NS1_PARAMS_LIMIT
            elif name == "Blue Cat's Protector 2":
                result = constants.BLUECATSPROTECTOR_PARAMS_LIMIT
            elif name == "C1 comp Stereo":
                result = constants.C1_COMP_PARAMS_LIMIT
            elif name == "Magma BB Tubes Stereo":
                result = constants.MAGMA_BB_TUBES_PARAMS_LIMIT
            else:
                result = 4240
        else:
            result = 4240

        return result

    def get_parameters(self):
        result = {}
        if self.__is_valid():
            params = []
            param_count = plugins.getParamCount(self.__mixer_channel_id, self.__plugin_slot_id, True)

            params_limit = self.__calc_params_limit()

            for param_id in range(param_count):

                if param_id > params_limit:
                    break
                param_value = plugins.getParamValue(param_id, self.__mixer_channel_id, self.__plugin_slot_id, True)
                param_value_str = str(param_value)
                params.append(param_value_str)
            result[PLUGIN_PARAMETERS_STORAGE_KEY] = params

            track_plugin_id = mixer.getTrackPluginId(self.__mixer_channel_id, self.__plugin_slot_id)
            
            event_id_plugin_mix_level = midi.REC_Plug_MixLevel + track_plugin_id
            plugin_mix_level = general.processRECEvent(event_id_plugin_mix_level, 0, midi.REC_GetValue)
            result[PLUGIN_MIX_LEVEL_STORAGE_KEY] = str(plugin_mix_level)
            
            event_id_plugin_activation = midi.REC_Plug_Mute + track_plugin_id
            plugin_activation = general.processRECEvent(event_id_plugin_activation, 0, midi.REC_GetValue)
            result[PLUGIN_ACTIVATION_STORAGE_KEY] = str(plugin_activation)

        return result

    def set_parameters(self, data):
        if self.__is_valid():
            if PLUGIN_PARAMETERS_STORAGE_KEY in data:
                params = data[PLUGIN_PARAMETERS_STORAGE_KEY]
                for param_id, param_value_str in reversed(list(enumerate(params))):
                    param_value = float(param_value_str)
                    existing_param_value = plugins.getParamValue(param_id, self.__mixer_channel_id, self.__plugin_slot_id, True)
                    if existing_param_value != param_value:
                        plugins.setParamValue(param_value, param_id, self.__mixer_channel_id, self.__plugin_slot_id, midi.PIM_None, True)
    
                track_plugin_id = mixer.getTrackPluginId(self.__mixer_channel_id, self.__plugin_slot_id)
                
                event_id_plugin_mix_level = midi.REC_Plug_MixLevel + track_plugin_id
                general.processRECEvent(event_id_plugin_mix_level, int(data[PLUGIN_MIX_LEVEL_STORAGE_KEY]), midi.REC_UpdateValue)
    
                event_id_plugin_activation = midi.REC_Plug_Mute + track_plugin_id
                general.processRECEvent(event_id_plugin_activation, int(data[PLUGIN_ACTIVATION_STORAGE_KEY]), midi.REC_UpdateValue)

    def set_fx_level(self, fx_level):
        if self.__is_valid():
            # print("set_fx_level: mixer_channel_id - " + str(self.__mixer_channel_id) + ", plugin_slot_id - " + str(self.__plugin_slot_id) + ", fx_level - " + str(fx_level))
            track_plugin_id = mixer.getTrackPluginId(self.__mixer_channel_id, self.__plugin_slot_id)
            
            event_id_plugin_mix_level = midi.REC_Plug_MixLevel + track_plugin_id
            general.processRECEvent(event_id_plugin_mix_level, int(fx_level * fl_helper.MIDI_MAX_VALUE) * 100, midi.REC_UpdateValue)

    def __is_valid(self):
        return plugins.isValid(self.__mixer_channel_id, self.__plugin_slot_id)

class DAWFxMixerChannel:
    def __init__(self, mixer_channel_id):
        self.__mixer_channel_id = mixer_channel_id
        self.__plugins = {int(constants.Plugins.Plugin_1) : DAWFxPlugin(self.__mixer_channel_id, int(constants.Plugins.Plugin_1)),
                          int(constants.Plugins.Plugin_2) : DAWFxPlugin(self.__mixer_channel_id, int(constants.Plugins.Plugin_2)),
                          int(constants.Plugins.Plugin_3) : DAWFxPlugin(self.__mixer_channel_id, int(constants.Plugins.Plugin_3)),
                          int(constants.Plugins.Plugin_4) : DAWFxPlugin(self.__mixer_channel_id, int(constants.Plugins.Plugin_4)),
                          int(constants.Plugins.Plugin_5) : DAWFxPlugin(self.__mixer_channel_id, int(constants.Plugins.Plugin_5)),
                          int(constants.Plugins.Plugin_6) : DAWFxPlugin(self.__mixer_channel_id, int(constants.Plugins.Plugin_6)),
                          int(constants.Plugins.Plugin_7) : DAWFxPlugin(self.__mixer_channel_id, int(constants.Plugins.Plugin_7)),
                          int(constants.Plugins.Plugin_8) : DAWFxPlugin(self.__mixer_channel_id, int(constants.Plugins.Plugin_8)),
                          int(constants.Plugins.Plugin_9) : DAWFxPlugin(self.__mixer_channel_id, int(constants.Plugins.Plugin_9)),
                          int(constants.Plugins.Plugin_10) : DAWFxPlugin(self.__mixer_channel_id, int(constants.Plugins.Plugin_10))}

    def on_init_script(self):
        for plugin in self.__plugins.values():
            plugin.on_init_script()

    def get_parameters(self):
        result = {}
        for plugin_key, plugin in self.__plugins.items():
            result[plugin_key] = plugin.get_parameters()
        result[MIXER_CHANNEL_VOLUME_KEY] = mixer.getTrackVolume(self.__mixer_channel_id)
        result[MIXER_CHANNEL_PAN_KEY] = mixer.getTrackPan(self.__mixer_channel_id)
        result[MIXER_CHANNEL_STEREO_SEPARATION_KEY] = mixer.getTrackStereoSep(self.__mixer_channel_id)
        return result

    def set_parameters(self, data):
        for plugin_key, plugin in self.__plugins.items():
            if plugin_key in data:
                plugin.set_parameters(data[plugin_key])
        mixer.setTrackVolume(self.__mixer_channel_id, float(data[MIXER_CHANNEL_VOLUME_KEY]))
        mixer.setTrackPan(self.__mixer_channel_id, float(data[MIXER_CHANNEL_PAN_KEY]))
        mixer.setTrackStereoSep(self.__mixer_channel_id, float(data[MIXER_CHANNEL_STEREO_SEPARATION_KEY]))

    def set_fx_level(self, fx_level):
        for plugin in self.__plugins.values():
            plugin.set_fx_level(fx_level)

class DAWFxManager():
    def __init__(self, input_channel, fx_mixer_channels):
        self.__input_channel = input_channel
        self.__fx_mixer_channels = fx_mixer_channels
        self.__controlled_mixer_channels = {}

        self.__controlled_mixer_channels[input_channel] = DAWFxMixerChannel(input_channel)
        for controlled_mixer_channel in fx_mixer_channels:
            self.__controlled_mixer_channels[controlled_mixer_channel] = DAWFxMixerChannel(controlled_mixer_channel)

    def on_init_script(self):
        for controlled_mixer_channel in self.__controlled_mixer_channels.values():
            controlled_mixer_channel.on_init_script()

    def get_parameters(self):
        result = {}
        for mixer_channel_id, controlled_mixer_channel in self.__controlled_mixer_channels.items():
            result[mixer_channel_id] = controlled_mixer_channel.get_parameters()

        routing_levels = {}

        for fx_mixer_channel_id in self.__fx_mixer_channels:
            routing_levels[fx_mixer_channel_id] = mixer.getRouteToLevel(self.__input_channel, fx_mixer_channel_id)

        result[INPUT_MIXER_CHANNEL_ROUTING_LEVELS] = routing_levels

        return result

    def set_parameters(self, data):
        for mixer_channel_id, controlled_mixer_channel in self.__controlled_mixer_channels.items():
            if mixer_channel_id in data:
                controlled_mixer_channel.set_parameters(data[mixer_channel_id])

        if INPUT_MIXER_CHANNEL_ROUTING_LEVELS in data:
            routing_levels = data[INPUT_MIXER_CHANNEL_ROUTING_LEVELS]

            for fx_mixer_channel_id in self.__fx_mixer_channels:
                mixer.setRouteToLevel(self.__input_channel, fx_mixer_channel_id, routing_levels[fx_mixer_channel_id])

    def set_fx_level(self, fx_level):
        for  controlled_mixer_channel in self.__controlled_mixer_channels.values():
            controlled_mixer_channel.set_fx_level(fx_level)