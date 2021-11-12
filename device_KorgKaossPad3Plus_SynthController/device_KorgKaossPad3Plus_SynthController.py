# name=device_KorgKaossPad3Plus_SynthController
device_name="device_KorgKaossPad3Plus_SynthController"
print(device_name + ': started')

# python imports
import math

# FL imports
import transport
import mixer
import plugins

from common import fl_helper
 
# MIDI CC
MIDI_CC_SHIFT                 = 95
MIDI_CC_SAVE_PRESET           = 53
MIDI_CC_DELETE_PRESET         = 54
MIDI_CC_RESET_SELECTIONS      = 55
MIDI_CC_EFFECTS_PAGE_1        = 49
MIDI_CC_EFFECTS_PAGE_2        = 50
MIDI_CC_EFFECTS_PAGE_3        = 51
MIDI_CC_EFFECTS_PAGE_4        = 52

MIDI_CC_EFFECT_1              = 49
MIDI_CC_EFFECT_2              = 50
MIDI_CC_EFFECT_3              = 51
MIDI_CC_EFFECT_4              = 52
MIDI_CC_EFFECT_5              = 53
MIDI_CC_EFFECT_6              = 54
MIDI_CC_EFFECT_7              = 55
MIDI_CC_EFFECT_8              = 56

MIDI_CC_EFFECT_PARAM_1        = 70
MIDI_CC_EFFECT_PARAM_2        = 71
MIDI_CC_EFFECT_PARAM_3        = 72
MIDI_CC_EFFECT_PARAM_4        = 73
MIDI_CC_EFFECT_PARAM_5        = 74
MIDI_CC_EFFECT_PARAM_6        = 75
MIDI_CC_EFFECT_PARAM_7        = 76
MIDI_CC_EFFECT_PARAM_8        = 77

MIDI_CC_SYNTH_VOLUME          = 93

MIDI_CC_ANIMATION_1           = 36
MIDI_CC_ANIMATION_2           = 37
MIDI_CC_ANIMATION_3           = 38
MIDI_CC_ANIMATION_4           = 39
MIDI_CC_ANIMATION_5           = 36
MIDI_CC_ANIMATION_6           = 37
MIDI_CC_ANIMATION_7           = 38
MIDI_CC_ANIMATION_8           = 39

MIDI_CC_FX_AMOUNT             = 94

# ROUTING

SYNTH_MAIN_CHANNEL            = 10
SYNTH_FX_CHANNEL              = 9

# CONSTANTS

KP3_PLUS_ABCD_PRESSED        = 100
KP3_PLUS_ABCD_RELEASED       = 64

# MASTER MIXER SLOT INDICES
MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX = 0
SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX = 1

# MIXER SLOT INDICES

# PLUGIN PARAMETERS

class FXPreset:
    
    FXPreset_1 = 0
    FXPreset_2 = 1
    FXPreset_3 = 2
    FXPreset_4 = 3
    FXPreset_5 = 4
    FXPreset_6 = 5
    FXPreset_7 = 6
    FXPreset_8 = 7
        
    def __init__(self, fx_page_number, fx_number, view):
        self.__view = view
        self.__fx_page_number = fx_page_number
        self.__fx_number = fx_number
        self.__parameters = ""
        
    def onInitScript(self):
        print(device_name + ': ' + FXPreset.onInitScript.__name__)
        
    def select(self):
        self.__view.selectFX(self.__fx_number)
    
    def save(self):
        print(device_name + ': ' + FXPresetPage.save.__name__)
    
    def delete(self):
        print(device_name + ': ' + FXPresetPage.delete.__name__)
        
class FXPresetPage:
    
    FXPresetPage_1 = 0
    FXPresetPage_2 = 1
    FXPresetPage_3 = 2
    FXPresetPage_4 = 3
    
    def __init__(self, fx_page_number, view):        
        self.__view = view
        self.__selected_fx_preset = FXPreset.FXPreset_1
        self.__fxs = { FXPreset.FXPreset_1: FXPreset(fx_page_number, FXPreset.FXPreset_1, self.__view),
                       FXPreset.FXPreset_2: FXPreset(fx_page_number, FXPreset.FXPreset_2, self.__view),
                       FXPreset.FXPreset_3: FXPreset(fx_page_number, FXPreset.FXPreset_3, self.__view),
                       FXPreset.FXPreset_4: FXPreset(fx_page_number, FXPreset.FXPreset_4, self.__view),
                       FXPreset.FXPreset_5: FXPreset(fx_page_number, FXPreset.FXPreset_5, self.__view),
                       FXPreset.FXPreset_6: FXPreset(fx_page_number, FXPreset.FXPreset_6, self.__view),
                       FXPreset.FXPreset_7: FXPreset(fx_page_number, FXPreset.FXPreset_7, self.__view),
                       FXPreset.FXPreset_8: FXPreset(fx_page_number, FXPreset.FXPreset_8, self.__view), }
    
    def onInitScript(self):
        self.selectFX(self.__selected_fx_preset)
    
    def activateFX(self, preset_fx_id):
        self.__fxs[preset_fx_id].activate()
    
    def saveFX(self, preset_fx_id):
        self.__fxs[preset_fx_id].save()
    
    def deleteFX(self, preset_fx_id):
        self.__fxs[preset_fx_id].delete()

    def selectFX(self, preset_fx_id):
        self.__selected_fx_preset = preset_fx_id
        self.__fxs[preset_fx_id].select()

    def updateSelectedFX(self):
        self.__fxs[self.__selected_fx_preset].select()

class KorgKaossPad3Plus_SynthController:

    def __init__(self, view):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.__init__.__name__)
        
        self.__view = view
        self.__initialized = False
        self.__shift_pressed = False
        self.__selected_fx_preset_page = FXPresetPage.FXPresetPage_1
        self.__fx_preset_pages = { FXPresetPage.FXPresetPage_1: FXPresetPage(FXPresetPage.FXPresetPage_1, self.__view),
                                FXPresetPage.FXPresetPage_2: FXPresetPage(FXPresetPage.FXPresetPage_2, self.__view),
                                FXPresetPage.FXPresetPage_3: FXPresetPage(FXPresetPage.FXPresetPage_3, self.__view),
                                FXPresetPage.FXPresetPage_4: FXPresetPage(FXPresetPage.FXPresetPage_4, self.__view) }

    def onInitScript(self):

        if False == self.__initialized:
            print(device_name + ': ' + KorgKaossPad3Plus_SynthController.onInitScript.__name__)

            try:
                for preset_page_id in self.__fx_preset_pages:
                    self.__fx_preset_pages[preset_page_id].onInitScript()
                
                self.selectFXPage(FXPresetPage.FXPresetPage_1)
                
                self.__initialized = True
            except Exception as e:
                print(device_name + ': ' + KorgKaossPad3Plus_SynthController.onInitScript.__name__ + ": failed to initialize the script.")
                print(e)


    def selectFXPage(self, preset_fx_page_id):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.onInitScript.__name__ + ": fx page id - " + str(preset_fx_page_id))
        self.__selected_fx_preset_page = preset_fx_page_id;
        self.__view.selectFXPage(preset_fx_page_id)
        self.__fx_preset_pages[preset_fx_page_id].updateSelectedFX()

    def setShiftPressedState(self, shift_pressed):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.setShiftPressedState.__name__ + ": shift pressed - " + str(shift_pressed))
        view.setShiftPressedState(shift_pressed)
        self.__shift_pressed = shift_pressed

    def getShiftPressedState(self):
        return self.__shift_pressed
    
    def selectFX(self, preset_fx_id):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.selectFX.__name__ + ": selected FX - " + str(preset_fx_id))
        self.__fx_preset_pages[self.__selected_fx_preset_page].selectFX(preset_fx_id)

    def resetSelections(self):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.resetSelections.__name__)
        
        self.selectFXPage(FXPresetPage.FXPresetPage_1)
        
        for preset_fx_id in self.__fx_preset_pages:
            self.__fx_preset_pages[preset_fx_id].selectFX(FXPreset.FXPreset_1)

class View:
    
    def __init__(self):
        print(device_name + ': ' + View.__init__.__name__)

    def setShiftPressedState(self, shift_pressed):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "Shift", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(shift_pressed, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
    
    def resetToggleFlags(self):
        print(device_name + ': ' + View.resetToggleFlags.__name__)
        
    def selectFXPage(self, preset_fx_page_id):
        for i in range(4):
            value = 0.0
            if i == preset_fx_page_id:
                value = 1.0
            
            parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "Page " + str(i + 1), SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(value, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()
        
    def selectFX(self, preset_fx_id):
        for i in range(8):
            value = 0.0
            if i == preset_fx_id:
                value = 1.0
            
            parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "FX" + str(i + 1), SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(value, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()


view = View()
synth_controller = KorgKaossPad3Plus_SynthController(view)

def OnInit():
    synth_controller.onInitScript()
    
def OnMidiMsg(event):

    synth_controller.onInitScript()

    event.handled = False

    if event.data1 == MIDI_CC_EFFECTS_PAGE_1 and synth_controller.getShiftPressedState():
        synth_controller.selectFXPage(FXPresetPage.FXPresetPage_1)
    elif event.data1 == MIDI_CC_EFFECTS_PAGE_2 and synth_controller.getShiftPressedState():
        synth_controller.selectFXPage(FXPresetPage.FXPresetPage_2)
    elif event.data1 == MIDI_CC_EFFECTS_PAGE_3 and synth_controller.getShiftPressedState():
        synth_controller.selectFXPage(FXPresetPage.FXPresetPage_3)
    elif event.data1 == MIDI_CC_EFFECTS_PAGE_4 and synth_controller.getShiftPressedState():
        synth_controller.selectFXPage(FXPresetPage.FXPresetPage_4)
    elif event.data1 == MIDI_CC_RESET_SELECTIONS and synth_controller.getShiftPressedState():
        synth_controller.resetSelections()
    elif event.data1 == MIDI_CC_SHIFT:
        synth_controller.setShiftPressedState(event.data2 == fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_EFFECT_1 and not synth_controller.getShiftPressedState():
        synth_controller.selectFX(FXPreset.FXPreset_1)
    elif event.data1 == MIDI_CC_EFFECT_2 and not synth_controller.getShiftPressedState():
        synth_controller.selectFX(FXPreset.FXPreset_2)
    elif event.data1 == MIDI_CC_EFFECT_3 and not synth_controller.getShiftPressedState():
        synth_controller.selectFX(FXPreset.FXPreset_3)
    elif event.data1 == MIDI_CC_EFFECT_4 and not synth_controller.getShiftPressedState():
        synth_controller.selectFX(FXPreset.FXPreset_4)
    elif event.data1 == MIDI_CC_EFFECT_5 and not synth_controller.getShiftPressedState():
        synth_controller.selectFX(FXPreset.FXPreset_5)
    elif event.data1 == MIDI_CC_EFFECT_6 and not synth_controller.getShiftPressedState():
        synth_controller.selectFX(FXPreset.FXPreset_6)
    elif event.data1 == MIDI_CC_EFFECT_7 and not synth_controller.getShiftPressedState():
        synth_controller.selectFX(FXPreset.FXPreset_7)
    elif event.data1 == MIDI_CC_EFFECT_8 and not synth_controller.getShiftPressedState():
        synth_controller.selectFX(FXPreset.FXPreset_8)
        
    event.handled = True
