# name=device_KorgKaossPad3Plus_MicController
device_name="device_KorgKaossPad3Plus_MicController"
print(device_name + ': started')

from input_controller.context import Context
from input_controller.korg_kaoss_pad_3_plus_input_controller import KorgKaossPad3Plus_InputController

SYNTH_MAIN_CHANNEL            = 6
SYNTH_FX_CHANNEL              = 5
SYNTH_FX2_CHANNEL             = 4
PARAMS_FIRST_STORAGE_TRACK_ID = 200

context = Context(device_name,
                  SYNTH_MAIN_CHANNEL,
                  SYNTH_FX_CHANNEL,
                  SYNTH_FX2_CHANNEL,
                  PARAMS_FIRST_STORAGE_TRACK_ID)

mic_controller = KorgKaossPad3Plus_InputController(context)
    
def OnMidiMsg(event):
    mic_controller.OnMidiMsg(event)