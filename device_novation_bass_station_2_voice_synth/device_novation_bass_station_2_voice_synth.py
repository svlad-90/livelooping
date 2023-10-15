# name=device_novation_bass_station_2_voice_synth
device_name="device_novation_bass_station_2_voice_synth"
print(device_name + ': started')

# internal imports
from voice_synth.novation_bass_station_2_voice_synth import NovationBassStation2VoiceSynth

voice_synth = NovationBassStation2VoiceSynth()

def OnMidiMsg(event):
    voice_synth.on_midi_msg(event)