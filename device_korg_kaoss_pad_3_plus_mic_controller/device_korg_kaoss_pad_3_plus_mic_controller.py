# name=device_korg_kaoss_pad_3_plus_mic_controller
# receiveFrom=device_korg_kaoss_pad_3_plus_looper_mux
device_name="device_korg_kaoss_pad_3_plus_mic_controller"
print(device_name + ': started')

from input_controller.context import Context
from input_controller.device_type import DeviceType
from input_controller.korg_kaoss_pad_3_plus_input_controller import KorgKaossPad3PlusInputController

MIC_MAIN_CHANNEL              = 11
MIC_FX1_CHANNEL               = 10
MIC_FX2_CHANNEL               = 9
MIC_FX3_CHANNEL               = 8
PARAMS_FIRST_STORAGE_TRACK_ID = 200
FIRST_SCENE_PATTERN           = 0
LOOPERS_SC_CTRL_NAME          = "Mic_Loopers_SC"

context = Context(device_name,
                  DeviceType.MIC,
                  MIC_MAIN_CHANNEL,
                  MIC_FX1_CHANNEL,
                  MIC_FX2_CHANNEL,
                  MIC_FX3_CHANNEL,
                  PARAMS_FIRST_STORAGE_TRACK_ID,
                  FIRST_SCENE_PATTERN,
                  LOOPERS_SC_CTRL_NAME)

mic_controller = KorgKaossPad3PlusInputController(context)

def OnMidiMsg(event):
    mic_controller.on_midi_msg(event)

def OnRefresh(flags):
    mic_controller.on_refresh(flags)
