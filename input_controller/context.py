'''
Created on Jan 24, 2022

@author: Dream Machines
'''

class Context:

    def __init__(self, device_name,
                 device_type, main_channel,
                 fx1_channel,
                 fx2_channel,
                 fx3_channel,
                 params_first_storage_track_id,
                 first_scene_pattern,
                 loopers_sc_ctrl_name):
        self.device_name = device_name
        self.device_type = device_type
        self.main_channel = main_channel
        self.fx1_channel = fx1_channel
        self.fx2_channel = fx2_channel
        self.fx3_channel = fx3_channel
        self.params_first_storage_track_id = params_first_storage_track_id
        self.first_scene_pattern = first_scene_pattern
        self.loopers_sc_ctrl_name = loopers_sc_ctrl_name
