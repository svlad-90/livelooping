'''
Created on Feb 7, 2022

@author: Dream Machines
'''

class IContextInterface:
    def get_sample_length(self) -> int:
        pass

    def get_device_name(self) -> str:
        pass