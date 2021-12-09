# name=device_KorgKaossPad3Plus_MicController
device_name="device_KorgKaossPad3Plus_MicController"
print(device_name + ': started')

from common import input_controller

SYNTH_MAIN_CHANNEL            = 6
SYNTH_FX_CHANNEL              = 5
SYNTH_FX2_CHANNEL             = 4
PARAMS_FIRST_STORAGE_TRACK_ID = 200

context = input_controller.Context(device_name,
                                   SYNTH_MAIN_CHANNEL,
                                   SYNTH_FX_CHANNEL,
                                   SYNTH_FX2_CHANNEL,
                                   PARAMS_FIRST_STORAGE_TRACK_ID)

mic_controller = input_controller.KorgKaossPad3Plus_InputController(context)

def OnInit():
    mic_controller.onInitScript()
    
def OnMidiMsg(event):
    mic_controller.OnMidiMsg(event)