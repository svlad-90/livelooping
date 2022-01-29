# name=device_KorgKaossPad3Plus_SynthController
device_name="device_KorgKaossPad3Plus_SynthController"
print(device_name + ': started')

from input_controller.context import Context
from input_controller.korg_kaoss_pad_3_plus_input_controller import KorgKaossPad3Plus_InputController

SYNTH_MAIN_CHANNEL            = 10
SYNTH_FX_CHANNEL              = 9
SYNTH_FX2_CHANNEL             = 8
PARAMS_FIRST_STORAGE_TRACK_ID = 100

context = Context(device_name,
          SYNTH_MAIN_CHANNEL,
          SYNTH_FX_CHANNEL,
          SYNTH_FX2_CHANNEL,
          PARAMS_FIRST_STORAGE_TRACK_ID)

synth_controller = KorgKaossPad3Plus_InputController(context)

def OnMidiMsg(event):
    synth_controller.OnMidiMsg(event)