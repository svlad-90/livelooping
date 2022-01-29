'''
Created on Jan 24, 2022

@author: Dream Machines
'''

class Context:

    def __init__(self, device_name, main_channel, fx1_channel, fx2_channel, params_first_storage_track_id):
        self.device_name = device_name
        self.main_channel = main_channel
        self.fx1_channel = fx1_channel
        self.fx2_channel = fx2_channel
        self.params_first_storage_track_id = params_first_storage_track_id
        