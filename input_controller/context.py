'''
Created on Jan 24, 2022

@author: Dream Machines
'''

class Context:

    def __init__(self, device_name,
                 device_type, main_channel,
                 fx_input_channel,
                 fx_1_channel,
                 fx_2_channel,
                 fx_3_channel,
                 fx_4_channel,
                 fx_finalize_channel,
                 fx_output_channel,
                 params_first_storage_track_id,
                 first_scene_pattern,
                 loopers_sc_ctrl_name):
        self.device_name = device_name
        self.device_type = device_type
        self.main_channel = main_channel
        self.fx_input_channel = fx_input_channel
        self.fx_1_channel = fx_1_channel
        self.fx_2_channel = fx_2_channel
        self.fx_3_channel = fx_3_channel
        self.fx_4_channel = fx_4_channel
        self.fx_finalize_channel = fx_finalize_channel
        self.fx_output_channel = fx_output_channel
        self.params_first_storage_track_id = params_first_storage_track_id
        self.first_scene_pattern = first_scene_pattern
        self.loopers_sc_ctrl_name = loopers_sc_ctrl_name
