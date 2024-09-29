'''
Created on Feb 7, 2022

@author: Dream Machines
'''

from common import updateable

class IContextInterface:
    def get_sample_length(self) -> int:
        pass

    def get_device_name(self) -> str:
        pass

    def get_updateable_mux(self) -> updateable.UpdateableMux:
        pass