# name=device_korg_kaoss_pad_3_plus_looper_mux
device_name="device_korg_kaoss_pad_3_plus_looper_mux"
print(device_name + ': started')

# internal imports
from looper_mux.korg_kaoss_pad_3_plus_looper_mux import KorgKaossPad3PlusLooperMux
from looper_mux.context import Context

context = Context(device_name)

looper_mux = KorgKaossPad3PlusLooperMux(context)

def OnMidiMsg(event):
    looper_mux.on_midi_msg(event)