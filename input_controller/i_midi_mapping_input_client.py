'''
Created on Jan 27, 2022

@author: Dream Machines
'''

class IMidiMappingInputClient:
    def MidiMappingInputDone(self, fx_parameter_number, midi_mapping):
        pass

    def MidiMappingInputCancelled(self):
        pass

    def getShiftPressedState(self):
        pass