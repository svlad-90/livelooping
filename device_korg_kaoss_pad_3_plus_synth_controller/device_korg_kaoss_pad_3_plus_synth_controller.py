# name=device_korg_kaoss_pad_3_plus_synth_controller
device_name="device_korg_kaoss_pad_3_plus_synth_controller"
print(device_name + ': started')

from input_controller.context import Context
from input_controller.korg_kaoss_pad_3_plus_input_controller import KorgKaossPad3PlusInputController

SYNTH_MAIN_CHANNEL            = 10
SYNTH_FX_CHANNEL              = 9
SYNTH_FX2_CHANNEL             = 8
PARAMS_FIRST_STORAGE_TRACK_ID = 100

context = Context(device_name,
          SYNTH_MAIN_CHANNEL,
          SYNTH_FX_CHANNEL,
          SYNTH_FX2_CHANNEL,
          PARAMS_FIRST_STORAGE_TRACK_ID)

synth_controller = KorgKaossPad3PlusInputController(context)

def OnMidiMsg(event):
    synth_controller.on_midi_msg(event)