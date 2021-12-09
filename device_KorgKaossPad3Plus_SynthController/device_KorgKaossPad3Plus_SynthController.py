# name=device_KorgKaossPad3Plus_SynthController
device_name="device_KorgKaossPad3Plus_SynthController"
print(device_name + ': started')

from common import input_controller

SYNTH_MAIN_CHANNEL            = 10
SYNTH_FX_CHANNEL              = 9
SYNTH_FX2_CHANNEL             = 8
PARAMS_FIRST_STORAGE_TRACK_ID = 100

context = input_controller.Context(device_name,
                                   SYNTH_MAIN_CHANNEL,
                                   SYNTH_FX_CHANNEL,
                                   SYNTH_FX2_CHANNEL,
                                   PARAMS_FIRST_STORAGE_TRACK_ID)

synth_controller = input_controller.KorgKaossPad3Plus_InputController(context)

def OnInit():
    synth_controller.onInitScript()
    
def OnMidiMsg(event):
    synth_controller.OnMidiMsg(event)