# name=device_KorgKaossPad3Plus_SynthController
from _ast import Or
device_name="device_KorgKaossPad3Plus_SynthController"
print(device_name + ': started')

# python imports
import math

# FL imports
import transport
import mixer
import plugins
import playlist

from common import fl_helper
 
# MIDI CC
MIDI_CC_SHIFT                 = 95
MIDI_CC_UPDATE_PRESET         = 53
MIDI_CC_RESET_PRESET          = 54
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

PARAMS_FIRST_STORAGE_TRACK_ID = 100
NUMBER_OF_FX_IN_PAGE          = 8
MAX_PARAM_VALUE               = 1016.0

# MASTER MIXER SLOT INDICES
MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX = 0
SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX = 1

# MIXER SLOT INDICES
PARAMETRIC_EQ_2_SLOT_INDEX     = 0
MANIPULATOR_SLOT_INDEX         = 1
FAST_DIST_SLOT_INDEX           = 2
STEREO_ENHANCER_SLOT_INDEX     = 3
REVERV_SLOT_INDEX              = 4
DELAY_SLOT_INDEX               = 5
FRUITY_FILTER_SLOT_INDEX       = 6
ENDLESS_SMILE_SLOT_INDEX       = 7
COMPRESSOT_SLOT_INDEX          = 8
LIMITER_SLOT_INDEX             = 9
FX_ACTIVATION_STATE_SLOT_INDEX = 10

# PARAMS LIMITE
MANIPULATOR_PARAMS_LIMIT = 200

# PLUGIN PARAMETERS

# mapping formula from 0<->1016 to 0<->1 values
def externalParamMapping(param_value):
    
    base = param_value / 8.0
    base_int = int(base)
    base_diff = base - base_int
    
    if base_int == 127.0:
        return 1.0
    elif base_int == 0.0:
        return 0.0
    else:
        first_part = 1 / ( 2 * ( 127.0 - base_int ) )
        second_part = first_part * base_diff
        return first_part + second_part

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
        self.__parameters = {}
    
    def areParametersLoaded(self):
        return len(self.__parameters) != 0
    
    def __getParamsFromPlugins(self):
        self.__parameters.clear()
        
        self.__parameters[FX_ACTIVATION_STATE_SLOT_INDEX] = []
        
        for mixer_slot in range(10):
            
            self.__parameters[mixer_slot] = []
            
            param_count = plugins.getParamCount(SYNTH_FX_CHANNEL, mixer_slot)
            
            for param_id in range(param_count):
                
                if mixer_slot == MANIPULATOR_SLOT_INDEX and param_id > MANIPULATOR_PARAMS_LIMIT:
                    break;
                
                param_value = plugins.getParamValue(param_id, SYNTH_FX_CHANNEL, mixer_slot)
                
                if mixer_slot == MANIPULATOR_SLOT_INDEX or \
                mixer_slot == ENDLESS_SMILE_SLOT_INDEX:
                    param_value = externalParamMapping(param_value)

                param_value_str = str(param_value)
                
                # param_name = plugins.getParamName(param_id, SYNTH_FX_CHANNEL, mixer_slot)
                # plugin_name = plugins.getPluginName(SYNTH_FX_CHANNEL, mixer_slot)
                # print("Get parameter: plugin name - " + plugin_name + ", param - " + param_name + \
                #       ", param_value - " + param_value_str + ", param_id - " + str(param_id) + \
                #       ", channel - " + str(SYNTH_FX_CHANNEL) + ", mixer_slot - " + str(mixer_slot))

                self.__parameters[mixer_slot].append( param_value_str )


            parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "S_E" + str(mixer_slot+1) + "_TO", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            fx_activation_state = plugins.getParamValue(parameter_id, SYNTH_MAIN_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            self.__parameters[FX_ACTIVATION_STATE_SLOT_INDEX].append(str(fx_activation_state / MAX_PARAM_VALUE))

    def __applyParametersToPlugins(self):
        for mixer_slot in self.__parameters:
            
            for param_id, param_value_str in enumerate(self.__parameters[mixer_slot]):
                
                param_value = float(param_value_str)
                
                if mixer_slot == FX_ACTIVATION_STATE_SLOT_INDEX:
                    plugins.setParamValue(param_value, param_id, SYNTH_MAIN_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
                else:
                    
                    #plugin_name = plugins.getPluginName(SYNTH_FX_CHANNEL, mixer_slot)
                    #param_name = plugins.getParamName(param_id, SYNTH_FX_CHANNEL, mixer_slot)
                    
                    #print("Apply parameter: plugin name - " + plugin_name + ", param - " + param_name + \
                    #      ", param_value - " + str(param_value) + ", param_id - " + str(param_id) + \
                    #      ", channel - " + str(SYNTH_FX_CHANNEL) + ", mixer_slot - " + str(mixer_slot))
                    
                    plugins.setParamValue(param_value, param_id, SYNTH_FX_CHANNEL, mixer_slot)

    def __loadParameters(self):
        paramsStr = playlist.getTrackName( PARAMS_FIRST_STORAGE_TRACK_ID + ( self.__fx_page_number * NUMBER_OF_FX_IN_PAGE ) + self.__fx_number)
        
        if paramsStr:            
            try:
                self.__parameters = eval(paramsStr)
            except Exception as e:
                self.__parameters.clear()
            
        
    def __saveParameters(self):
        playlist.setTrackName( PARAMS_FIRST_STORAGE_TRACK_ID + ( self.__fx_page_number * NUMBER_OF_FX_IN_PAGE ) + self.__fx_number,  str(self.__parameters))
    
    def __resetParameters(self):
        playlist.setTrackName( PARAMS_FIRST_STORAGE_TRACK_ID + ( self.__fx_page_number * NUMBER_OF_FX_IN_PAGE ) + self.__fx_number,  "")
    
    def onInitScript(self):
        print(device_name + ': ' + FXPreset.onInitScript.__name__)
        
    def select(self):
        if not self.areParametersLoaded():
            self.__loadParameters()
        self.__applyParametersToPlugins()
    
    def update(self):
        self.__getParamsFromPlugins()
        self.__saveParameters()
        self.__applyParametersToPlugins()

    def reset(self):
        self.__resetParameters()
        
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
    
    def updateFX(self):
        self.__fxs[self.__selected_fx_preset].update()
    
    def resetFX(self):
        self.__fxs[self.__selected_fx_preset].reset()

    def selectFX(self, preset_fx_id):
        self.__selected_fx_preset = preset_fx_id
        self.__fxs[preset_fx_id].select()
        self.__view.selectFXPreset(preset_fx_id)

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
    
    def selectFXPreset(self, preset_fx_id):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.selectFXPreset.__name__ + ": selected FX - " + str(preset_fx_id))
        self.__fx_preset_pages[self.__selected_fx_preset_page].selectFX(preset_fx_id)

    def resetSelections(self):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.resetSelections.__name__)
        
        self.selectFXPage(FXPresetPage.FXPresetPage_1)
        
        for preset_fx_id in self.__fx_preset_pages:
            self.__fx_preset_pages[preset_fx_id].selectFX(FXPreset.FXPreset_1)
            
    def updateFXPreset(self):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.updateFXPreset.__name__)
        self.__fx_preset_pages[self.__selected_fx_preset_page].updateFX()
        self.__view.updateFXPreset()
        
    def resetFXPreset(self):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.resetFXPreset.__name__)
        self.__fx_preset_pages[self.__selected_fx_preset_page].resetFX()
        self.__view.resetFXPreset()

class View:
    
    def __init__(self):
        print(device_name + ': ' + View.__init__.__name__)

    def setShiftPressedState(self, shift_pressed):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "Shift", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(shift_pressed, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
    
    def resetToggleFlags(self):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "Save", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "Delete", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
    def selectFXPage(self, preset_fx_page_id):
        for i in range(4):
            value = 0.0
            if i == preset_fx_page_id:
                value = 1.0
            
            parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "Page " + str(i + 1), SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(value, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()
        
    def selectFXPreset(self, preset_fx_id):
        for i in range(8):
            value = 0.0
            if i == preset_fx_id:
                value = 1.0
            
            parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "FX" + str(i + 1), SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(value, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        self.resetToggleFlags()
        
    def updateFXPreset(self):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "Save", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
    def resetFXPreset(self):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "Delete", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)


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
    elif event.data1 == MIDI_CC_UPDATE_PRESET and synth_controller.getShiftPressedState():
        synth_controller.updateFXPreset()
    elif event.data1 == MIDI_CC_RESET_PRESET and synth_controller.getShiftPressedState():
        synth_controller.resetFXPreset()
    elif event.data1 == MIDI_CC_EFFECT_1 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPreset(FXPreset.FXPreset_1)
    elif event.data1 == MIDI_CC_EFFECT_2 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPreset(FXPreset.FXPreset_2)
    elif event.data1 == MIDI_CC_EFFECT_3 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPreset(FXPreset.FXPreset_3)
    elif event.data1 == MIDI_CC_EFFECT_4 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPreset(FXPreset.FXPreset_4)
    elif event.data1 == MIDI_CC_EFFECT_5 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPreset(FXPreset.FXPreset_5)
    elif event.data1 == MIDI_CC_EFFECT_6 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPreset(FXPreset.FXPreset_6)
    elif event.data1 == MIDI_CC_EFFECT_7 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPreset(FXPreset.FXPreset_7)
    elif event.data1 == MIDI_CC_EFFECT_8 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPreset(FXPreset.FXPreset_8)
        
    event.handled = True
