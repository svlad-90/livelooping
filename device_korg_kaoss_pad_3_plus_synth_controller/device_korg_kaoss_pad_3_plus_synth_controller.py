# name=device_korg_kaoss_pad_3_plus_synth_controller
# receiveFrom=device_korg_kaoss_pad_3_plus_looper_mux
device_name="device_korg_kaoss_pad_3_plus_synth_controller"
print(device_name + ': started')

from input_controller.context import Context
from input_controller.device_type import DeviceType
from input_controller.korg_kaoss_pad_3_plus_input_controller import KorgKaossPad3PlusInputController

SYNTH_MAIN_CHANNEL              = 24
SYNTH_INPUT_CHANNEL             = 23
SYNTH_FX1_CHANNEL               = 22
SYNTH_FX2_CHANNEL               = 21
SYNTH_FX3_CHANNEL               = 20
SYNTH_FX4_CHANNEL               = 19
SYNTH_FINALIZE_CHANNEL          = 18
SYNTH_OUT_CHANNEL               = 17
PARAMS_FIRST_STORAGE_TRACK_ID = 200
FIRST_SCENE_PATTERN           = 320
LOOPERS_SC_CTRL_NAME          = "Synth_Loopers_SC"

context = Context(device_name,
          DeviceType.SYNTH,
          SYNTH_MAIN_CHANNEL,
          SYNTH_INPUT_CHANNEL,
          SYNTH_FX1_CHANNEL,
          SYNTH_FX2_CHANNEL,
          SYNTH_FX3_CHANNEL,
          SYNTH_FX4_CHANNEL,
          SYNTH_FINALIZE_CHANNEL,
          SYNTH_OUT_CHANNEL,
          PARAMS_FIRST_STORAGE_TRACK_ID,
          FIRST_SCENE_PATTERN,
          LOOPERS_SC_CTRL_NAME)

synth_controller = KorgKaossPad3PlusInputController(context)

def OnMidiMsg(event):
    synth_controller.on_midi_msg(event)

def OnRefresh(flags):
    synth_controller.on_refresh(flags)
