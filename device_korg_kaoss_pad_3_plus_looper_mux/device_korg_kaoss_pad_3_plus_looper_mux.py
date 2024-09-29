# name=device_korg_kaoss_pad_3_plus_looper_mux
import device

device_name="device_korg_kaoss_pad_3_plus_looper_mux"
print(device_name + ': started')

print("found MIDI receivers - ", device.dispatchReceiverCount())

# internal imports
from looper_mux.korg_kaoss_pad_3_plus_looper_mux import KorgKaossPad3PlusLooperMux
from looper_mux.context import Context

context = Context(device_name)

looper_mux = KorgKaossPad3PlusLooperMux(context)

def OnMidiMsg(event):
    looper_mux.on_midi_msg(event)

def OnIdle():
    looper_mux.on_update()