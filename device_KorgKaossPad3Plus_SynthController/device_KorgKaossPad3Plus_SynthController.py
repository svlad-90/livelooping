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
MIDI_CC_ENTER_SAVE_MODE       = 53
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

MIDI_CC_SYNTH_VOLUME          = 93
MIDI_CC_FX_LEVEL              = 94

MIDI_CC_EFFECT_PARAM_1        = 70
MIDI_CC_EFFECT_PARAM_2        = 71
MIDI_CC_EFFECT_PARAM_3        = 72
MIDI_CC_EFFECT_PARAM_4        = 73
MIDI_CC_EFFECT_PARAM_5        = 74
MIDI_CC_EFFECT_PARAM_6        = 75
MIDI_CC_EFFECT_PARAM_7        = 76
MIDI_CC_EFFECT_PARAM_8        = 77

MIDI_CC_ANIMATION_1           = 36
MIDI_CC_ANIMATION_2           = 37
MIDI_CC_ANIMATION_3           = 38
MIDI_CC_ANIMATION_4           = 39
MIDI_CC_ANIMATION_5           = 36
MIDI_CC_ANIMATION_6           = 37
MIDI_CC_ANIMATION_7           = 38
MIDI_CC_ANIMATION_8           = 39

# ROUTING

SYNTH_MAIN_CHANNEL            = 10
SYNTH_FX_CHANNEL              = 9
SYNTH_FX2_CHANNEL             = 8

# CONSTANTS

KP3_PLUS_ABCD_PRESSED        = 100
KP3_PLUS_ABCD_RELEASED       = 64

PARAMS_FIRST_STORAGE_TRACK_ID = 100
NUMBER_OF_FX_IN_PAGE          = 8

# MASTER MIXER SLOT INDICES
MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX = 0
SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX = 1

# MIXER SLOT INDICES
FABFILTER_PRO_Q3_SLOT_INDEX    = 0
FINISHER_VOODOO_SLOT_INDEX     = 1
MANIPULATOR_SLOT_INDEX         = 2
FAST_DIST_SLOT_INDEX           = 3
STEREO_ENHANCER_SLOT_INDEX     = 4
REVERB_SLOT_INDEX              = 5
DELAY_SLOT_INDEX               = 6
FRUITY_FILTER_SLOT_INDEX       = 7
COMPRESSOT_SLOT_INDEX          = 8
LIMITER_SLOT_INDEX             = 9
FX_ACTIVATION_STATE_SLOT_INDEX = 10

NO_ADJUSTABLE_EFFECT_AVAILABLE = -1

PRESET_CHANGE_PROTECTOR_PANOMATIC_SLOT_INDEX = 9

# PARAMS LIMITS
FABFILTER_PRO_Q3_PARAMS_LIMIT = 360
FINISHER_VOODOO_PARAMS_LIMIT  = 10
MANIPULATOR_PARAMS_LIMIT      = 200

# PLUGIN PARAMETERS
PANOMATIC_VOLUME_PARAM_INDEX = 1

FINISHER_VOODOO_EFFECT_PARAM_INDEX = 3
FINISHER_VOODOO_VARIATION_1_PARAM_INDEX = 4
FINISHER_VOODOO_VARIATION_2_PARAM_INDEX = 5
FINISHER_VOODOO_VARIATION_3_PARAM_INDEX = 6
FINISHER_VOODOO_VARIATION_4_PARAM_INDEX = 7

MANIPULATOR_FORMANT_PARAM_INDEX    = 0
MANIPULATOR_PITCH_PARAM_INDEX      = 1
MANIPULATOR_RATIO_PARAM_INDEX      = 2
MANIPULATOR_HARMONICS_PARAM_INDEX  = 3
MANIPULATOR_FM_PARAM_INDEX         = 4
MANIPULATOR_ALTERNATOR_PARAM_INDEX = 5
MANIPULATOR_OCTAVE_PARAM_INDEX     = 6
MANIPULATOR_WETDRY_PARAM_INDEX     = 7

INVALID_PARAM = -1

class FXParameter:
    FXParameter_1 = 0
    FXParameter_2 = 1
    FXParameter_3 = 2
    FXParameter_4 = 3
    FXParameter_5 = 4
    FXParameter_6 = 5
    FXParameter_7 = 6
    FXParameter_8 = 7
    
    def __init__(self, fx_param_id, view):
        self.__fx_param_level = 0.0
        self.__fx_param_id = fx_param_id
        self.__view = view
    
    def getAdjustablePlugin(self):
        
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "S_E2_TO", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        finisher_voodoo_state = fl_helper.externalParamMapping(plugins.getParamValue(parameter_id, SYNTH_MAIN_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX))
        
        if 1.0 == finisher_voodoo_state:
            return FINISHER_VOODOO_SLOT_INDEX
        
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "S_E3_TO", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        manipulator_state = fl_helper.externalParamMapping(plugins.getParamValue(parameter_id, SYNTH_MAIN_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX))
        
        if 1.0 == manipulator_state:
            return MANIPULATOR_SLOT_INDEX
        
        return NO_ADJUSTABLE_EFFECT_AVAILABLE
    
    def getFLParamIndex(self, adjustable_plugin_slot_index, fx_param_id):
        
        if adjustable_plugin_slot_index == FINISHER_VOODOO_SLOT_INDEX:
            if fx_param_id == FXParameter.FXParameter_1:
                return FINISHER_VOODOO_VARIATION_1_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_2:
                return FINISHER_VOODOO_VARIATION_2_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_3:
                return FINISHER_VOODOO_VARIATION_3_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_4:
                return FINISHER_VOODOO_VARIATION_4_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_5:
                return INVALID_PARAM
            elif fx_param_id == FXParameter.FXParameter_6:
                return INVALID_PARAM
            elif fx_param_id == FXParameter.FXParameter_7:
                return INVALID_PARAM
            elif fx_param_id == FXParameter.FXParameter_8:
                return FINISHER_VOODOO_EFFECT_PARAM_INDEX
        elif adjustable_plugin_slot_index == MANIPULATOR_SLOT_INDEX:
            if fx_param_id == FXParameter.FXParameter_1:
                return MANIPULATOR_FORMANT_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_2:
                return MANIPULATOR_PITCH_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_3:
                return MANIPULATOR_RATIO_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_4:
                return MANIPULATOR_HARMONICS_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_5:
                return MANIPULATOR_FM_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_6:
                return MANIPULATOR_ALTERNATOR_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_7:
                return MANIPULATOR_OCTAVE_PARAM_INDEX
            elif fx_param_id == FXParameter.FXParameter_8:
                return MANIPULATOR_WETDRY_PARAM_INDEX
        else:
            return INVALID_PARAM
    
    def setLevel(self, fx_param_level):
        
        adjustable_plugin_slot_index = self.getAdjustablePlugin()
        
        if adjustable_plugin_slot_index != NO_ADJUSTABLE_EFFECT_AVAILABLE:
            fl_param_id = self.getFLParamIndex(adjustable_plugin_slot_index, self.__fx_param_id)
            
            if fl_param_id != INVALID_PARAM:
                plugins.setParamValue(fx_param_level, fl_param_id, SYNTH_FX_CHANNEL, adjustable_plugin_slot_index)
                self.__fx_param_level = fx_param_level
                self.__view.setFXParameterLevel(self.__fx_param_id, fx_param_level)

    def onInitScript(self):
        self.setLevel(self.__fx_param_level)
    
    def updateParamsFromPlugin(self):
        
        adjustable_plugin_slot_index = self.getAdjustablePlugin()
        
        if adjustable_plugin_slot_index != NO_ADJUSTABLE_EFFECT_AVAILABLE:
        
            fl_param_id = self.getFLParamIndex(adjustable_plugin_slot_index, self.__fx_param_id)
            
            if fl_param_id != INVALID_PARAM:
                self.__fx_param_level = fl_helper.externalParamMapping(plugins.getParamValue(fl_param_id, SYNTH_FX_CHANNEL, FINISHER_VOODOO_SLOT_INDEX))
                self.__view.setFXParameterActivationStatus(self.__fx_param_id, 1)
            else:
                self.__fx_param_level = 0.0
                self.__view.setFXParameterActivationStatus(self.__fx_param_id, 0)
            
            self.__view.setFXParameterLevel(self.__fx_param_id, self.__fx_param_level)
        
class FXPreset:
    
    FXPreset_1    = 0
    FXPreset_2    = 1
    FXPreset_3    = 2
    FXPreset_4    = 3
    FXPreset_5    = 4
    FXPreset_6    = 5
    FXPreset_7    = 6
    FXPreset_8    = 7
        
    def __init__(self, fx_page_number, fx_number, view):
        self.__view = view
        self.__fx_page_number = fx_page_number
        self.__fx_number = fx_number
        self.__parameters = {}
        self.__fx_parameters = { FXParameter.FXParameter_1: FXParameter(FXParameter.FXParameter_1, view),
                                 FXParameter.FXParameter_2: FXParameter(FXParameter.FXParameter_2, view),
                                 FXParameter.FXParameter_3: FXParameter(FXParameter.FXParameter_3, view),
                                 FXParameter.FXParameter_4: FXParameter(FXParameter.FXParameter_4, view),
                                 FXParameter.FXParameter_5: FXParameter(FXParameter.FXParameter_5, view),
                                 FXParameter.FXParameter_6: FXParameter(FXParameter.FXParameter_6, view),
                                 FXParameter.FXParameter_7: FXParameter(FXParameter.FXParameter_7, view),
                                 FXParameter.FXParameter_8: FXParameter(FXParameter.FXParameter_8, view) }
    
    def onInitScript(self):
        self.__loadParameters()
        
        for fx_parameter_id in self.__fx_parameters:
            self.__fx_parameters[fx_parameter_id].onInitScript()
    
    def update(self):
        self.__getParamsFromPlugins()
        self.__saveParameters()
        self.__applyParametersToPlugins()

    def reset(self):
        self.__resetParameters()
        self.__parameters.clear()

    def select(self):
        plugins.setParamValue(0.0, PANOMATIC_VOLUME_PARAM_INDEX, SYNTH_MAIN_CHANNEL, PRESET_CHANGE_PROTECTOR_PANOMATIC_SLOT_INDEX)

        if not self.__areParametersLoaded():
            self.__loadParameters()

        self.__applyParametersToPlugins()
        self.__view.selectFXPreset(self.__fx_number)
        
        plugins.setParamValue(fl_helper.MAX_VOLUME_LEVEL_VALUE, PANOMATIC_VOLUME_PARAM_INDEX, SYNTH_MAIN_CHANNEL, PRESET_CHANGE_PROTECTOR_PANOMATIC_SLOT_INDEX)
    
    def view_updateFXPresetAvailability(self):
        self.__view.setFXPresetAvailability(self.__fx_number, len(self.__parameters) > 0)
    
    def view_updateFXParamsFromPlugins(self):
        for fx_param_id in self.__fx_parameters:
            self.__fx_parameters[fx_param_id].updateParamsFromPlugin()
    
    def setFXParameterLevel(self, fx_param_id, fx_param_level):
        self.__fx_parameters[fx_param_id].setLevel(fx_param_level)
    
    def __areParametersLoaded(self):
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
                
                if mixer_slot == FINISHER_VOODOO_SLOT_INDEX and param_id > FINISHER_VOODOO_PARAMS_LIMIT:
                    break;
                
                if mixer_slot == FABFILTER_PRO_Q3_SLOT_INDEX and param_id > FABFILTER_PRO_Q3_PARAMS_LIMIT:
                    break;
                
                param_value = plugins.getParamValue(param_id, SYNTH_FX_CHANNEL, mixer_slot)
                
                if mixer_slot == MANIPULATOR_SLOT_INDEX or \
                   mixer_slot == FABFILTER_PRO_Q3_SLOT_INDEX or \
                   mixer_slot == FINISHER_VOODOO_SLOT_INDEX:
                    param_value = fl_helper.externalParamMapping(param_value)

                param_value_str = str(param_value)
                
                # param_name = plugins.getParamName(param_id, SYNTH_FX_CHANNEL, mixer_slot)
                # plugin_name = plugins.getPluginName(SYNTH_FX_CHANNEL, mixer_slot)
                # print("Get parameter: plugin name - " + plugin_name + ", param - " + param_name + \
                #       ", param_value - " + param_value_str + ", param_id - " + str(param_id) + \
                #       ", channel - " + str(SYNTH_FX_CHANNEL) + ", mixer_slot - " + str(mixer_slot))

                self.__parameters[mixer_slot].append( param_value_str )


            parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "S_E" + str(mixer_slot+1) + "_TO", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            fx_activation_state = plugins.getParamValue(parameter_id, SYNTH_MAIN_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            self.__parameters[FX_ACTIVATION_STATE_SLOT_INDEX].append(str( fl_helper.externalParamMapping(fx_activation_state) ))

    def __applyParametersToPlugins(self):
        for mixer_slot in self.__parameters:
            
            for param_id, param_value_str in reversed(list(enumerate(self.__parameters[mixer_slot]))):
                
                param_value = float(param_value_str)
                
                if mixer_slot == FX_ACTIVATION_STATE_SLOT_INDEX:
                    plugins.setParamValue(param_value, param_id, SYNTH_MAIN_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
                else:
                    
                    # plugin_name = plugins.getPluginName(SYNTH_FX_CHANNEL, mixer_slot)
                    # param_name = plugins.getParamName(param_id, SYNTH_FX_CHANNEL, mixer_slot)
                    #
                    # print("Apply parameter: plugin name - " + plugin_name + ", param - " + param_name + \
                    #       ", param_value - " + str(param_value) + ", param_id - " + str(param_id) + \
                    #       ", channel - " + str(SYNTH_FX_CHANNEL) + ", mixer_slot - " + str(mixer_slot))
                    
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
        
class FXPresetPage:
    
    FXPresetPage_1 = 0
    FXPresetPage_2 = 1
    FXPresetPage_3 = 2
    FXPresetPage_4 = 3
    
    def __init__(self, fx_page_number, view):
        self.__view = view
        self.__fx_page_number = fx_page_number
        self.__selected_fx_preset_id = FXPreset.FXPreset_1
        self.__fx_presets = { FXPreset.FXPreset_1: FXPreset(fx_page_number, FXPreset.FXPreset_1, self.__view),
                       FXPreset.FXPreset_2: FXPreset(fx_page_number, FXPreset.FXPreset_2, self.__view),
                       FXPreset.FXPreset_3: FXPreset(fx_page_number, FXPreset.FXPreset_3, self.__view),
                       FXPreset.FXPreset_4: FXPreset(fx_page_number, FXPreset.FXPreset_4, self.__view),
                       FXPreset.FXPreset_5: FXPreset(fx_page_number, FXPreset.FXPreset_5, self.__view),
                       FXPreset.FXPreset_6: FXPreset(fx_page_number, FXPreset.FXPreset_6, self.__view),
                       FXPreset.FXPreset_7: FXPreset(fx_page_number, FXPreset.FXPreset_7, self.__view),
                       FXPreset.FXPreset_8: FXPreset(fx_page_number, FXPreset.FXPreset_8, self.__view), }
    
    def select(self):
        self.__view_updateStats()
        self.selectFXPreset(self.__selected_fx_preset_id)
    
    def getSelectedFXPresetID(self):
        return self.__selected_fx_preset_id
    
    def onInitScript(self):
        for fx_preset_id in self.__fx_presets:
            self.__fx_presets[fx_preset_id].onInitScript()
    
    def updateFXPreset(self, fx_preset_id):
        self.__fx_presets[fx_preset_id].update()
        self.__fx_presets[fx_preset_id].view_updateFXPresetAvailability()
        self.__fx_presets[fx_preset_id].view_updateFXParamsFromPlugins()
    
    def resetFXPreset(self, fx_preset_id):
        self.__fx_presets[fx_preset_id].reset()
        self.__fx_presets[fx_preset_id].view_updateFXPresetAvailability()
        self.__fx_presets[fx_preset_id].view_updateFXParamsFromPlugins()

    def selectFXPreset(self, fx_preset_id):
        self.__selected_fx_preset_id = fx_preset_id
        self.__fx_presets[fx_preset_id].select()
        self.__fx_presets[fx_preset_id].view_updateFXPresetAvailability()
        self.__fx_presets[fx_preset_id].view_updateFXParamsFromPlugins()
    
    def setFXParameterLevel(self, fx_param_id, fx_param_level):
            self.__fx_presets[self.__selected_fx_preset_id].setFXParameterLevel(fx_param_id, fx_param_level)

    def __view_updateStats(self):
        self.__view.selectFXPage(self.__fx_page_number)
        
        for fx_preset_id in self.__fx_presets:
            self.__fx_presets[fx_preset_id].view_updateFXPresetAvailability()
        
        self.__fx_presets[fx_preset_id].view_updateFXParamsFromPlugins()

class FX:
    
    FX_1  = 0
    FX_2  = 1
    FX_3  = 2
    FX_4  = 3
    FX_5  = 4
    FX_6  = 5
    FX_7  = 6
    FX_8  = 7
    FX_9  = 8
    FX_10 = 9
    
    def __init__(self, fx_number, view):
        self.__fx_number = fx_number
        self.__view = view
        self.__activation_param_id = -1
        self.__level_param_id = -1
        self.__fx_level = 0
    
    def setFXLevel(self, fx_level, force = False):
        
        if self.__activation_param_id == -1:
            self.__activation_param_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "S_E" + str(self.__fx_number + 1) + "_TO", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
        if math.fabs(self.__fx_level - fx_level) >= 0.01 or fx_level == 1.0 or True == force:
            
            fx_activation_status = fl_helper.externalParamMapping( plugins.getParamValue(self.__activation_param_id, SYNTH_MAIN_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX) )
            
            if self.__level_param_id == -1:
                self.__level_param_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "S_FX_L" + str(self.__fx_number + 1), MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            
            if fx_activation_status == 0.0:
                plugins.setParamValue(0.0, self.__level_param_id, SYNTH_MAIN_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            else:
                plugins.setParamValue(fx_level, self.__level_param_id, SYNTH_MAIN_CHANNEL, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            
            self.__fx_level = fx_level

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
        self.__isSaveMode = False
        self.__fxs = { FX.FX_1 : FX(FX.FX_1, self.__view),
                      FX.FX_2 : FX(FX.FX_2, self.__view),
                      FX.FX_3 : FX(FX.FX_3, self.__view),
                      FX.FX_4 : FX(FX.FX_4, self.__view),
                      FX.FX_5 : FX(FX.FX_5, self.__view),
                      FX.FX_6 : FX(FX.FX_6, self.__view),
                      FX.FX_7 : FX(FX.FX_7, self.__view),
                      FX.FX_8 : FX(FX.FX_8, self.__view),
                      FX.FX_9 : FX(FX.FX_9, self.__view),
                      FX.FX_10 : FX(FX.FX_10, self.__view), }
        
        self.__fx_level = 1.0

    def onInitScript(self):

        if False == self.__initialized:
            print(device_name + ': ' + KorgKaossPad3Plus_SynthController.onInitScript.__name__)

            try:
                for preset_page_id in self.__fx_preset_pages:
                    self.__fx_preset_pages[preset_page_id].onInitScript()
                
                self.selectFXPage(self.__selected_fx_preset_page)
                self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_1)
                self.__view.setSaveMode(self.__isSaveMode)
    
                self.__initialized = True
            except Exception as e:
                print(device_name + ': ' + KorgKaossPad3Plus_SynthController.onInitScript.__name__ + ": failed to initialize the script.")
                print(e)

    def isSaveMode(self):
        return self.__isSaveMode
        
    def setSaveMode(self, save_mode):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.setSaveMode.__name__ + ": save mode - " + str(save_mode))
        self.__isSaveMode = save_mode
        self.__view.setSaveMode(save_mode)
        
    def selectFXPage(self, preset_fx_page_id):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.onInitScript.__name__ + ": fx page id - " + str(preset_fx_page_id))
        self.__selected_fx_preset_page = preset_fx_page_id;
        self.__fx_preset_pages[self.__selected_fx_preset_page].select()

    def setShiftPressedState(self, shift_pressed):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.setShiftPressedState.__name__ + ": shift pressed - " + str(shift_pressed))
        view.setShiftPressedState(shift_pressed)
        self.__shift_pressed = shift_pressed

    def getShiftPressedState(self):
        return self.__shift_pressed
        
    def selectFXPresetOnTheVisiblePage(self, preset_fx_id):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.selectFXPresetOnTheVisiblePage.__name__ + ": selected page - " + \
              str(self.__selected_fx_preset_page) + ", selected FX - " + str(preset_fx_id))
        self.__fx_preset_pages[self.__selected_fx_preset_page].selectFXPreset(preset_fx_id)
        
        self.setFXLevel(self.__fx_level, True)

    def resetSelections(self):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.resetSelections.__name__)
        
        self.selectFXPage(FXPresetPage.FXPresetPage_1)
        self.selectFXPreset(FXPreset.FXPreset_1)
        
        self.setFXLevel(self.__fx_level, True)
            
    def updateFXPreset(self, fx_preset_id):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.updateFXPreset.__name__)
        self.__fx_preset_pages[self.__selected_fx_preset_page].updateFXPreset(fx_preset_id)
        
    def resetFXPreset(self):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.resetFXPreset.__name__)
        self.__fx_preset_pages[self.__selected_fx_preset_page].resetFXPreset(self.getSelectedFXPresetID())
        self.__view.resetFXPreset()

    def setSynthVolume(self, synth_volume):
        mixer.setTrackVolume(SYNTH_FX2_CHANNEL, synth_volume)
        self.__view.setSynthVolume(synth_volume)

    def setFXLevel(self, fx_level, force = False):
        for fx_id in self.__fxs:
            self.__fxs[fx_id].setFXLevel(fx_level, force)
        self.__view.setFXLevel(fx_level)
        self.__fx_level = fx_level
    
    def setFXParameterLevel(self, fx_parameter_id, effect_level):
        self.__fx_preset_pages[self.__selected_fx_preset_page].setFXParameterLevel(fx_parameter_id, effect_level)

    def getSelectedFXPresetID(self):
        return self.__fx_preset_pages[self.__selected_fx_preset_page].getSelectedFXPresetID()
    
    def __selectFXPreset(self, preset_fx_page_id, preset_fx_id):
        print(device_name + ': ' + KorgKaossPad3Plus_SynthController.__selectFXPreset.__name__ + ": selected page - " + \
              str(preset_fx_page_id) + ", selected FX - " + str(preset_fx_id))
        self.__fx_preset_pages[preset_fx_page_id].selectFXPreset(preset_fx_id)
        
        self.setFXLevel(self.__fx_level, True)

class View:
    
    def __init__(self):
        print(device_name + ': ' + View.__init__.__name__)

    def setShiftPressedState(self, shift_pressed):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "Shift", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(shift_pressed, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()
    
    def resetToggleFlags(self):
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
        
    def setSaveMode(self, save_mode):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "Save mode", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(save_mode, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        
    def resetFXPreset(self):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "Delete", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setSynthVolume(self, synth_volume):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "Volume", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(synth_volume, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setFXLevel(self, fx_level):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "FX level", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(fx_level, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setFXPresetAvailability(self, fx_preset_id, preset_availability):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "FX_" + str(fx_preset_id + 1) + "_A", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(preset_availability, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setFXParameterLevel(self, fx_param_id, fx_level):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "SFXP" + str(fx_param_id + 1), SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(fx_level, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setFXParameterActivationStatus(self, fx_param_id, activation_status):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(SYNTH_MAIN_CHANNEL, "FX_P_" + str(fx_param_id + 1) + "_A", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(activation_status, parameter_id, SYNTH_MAIN_CHANNEL, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

view = View()
synth_controller = KorgKaossPad3Plus_SynthController(view)

def OnInit():
    synth_controller.onInitScript()
    
def OnMidiMsg(event):

    #fl_helper.printAllPluginParameters(SYNTH_FX_CHANNEL, MANIPULATOR_SLOT_INDEX)

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
    elif event.data1 == MIDI_CC_ENTER_SAVE_MODE and synth_controller.getShiftPressedState():
        synth_controller.setSaveMode(not synth_controller.isSaveMode())
    elif event.data1 == MIDI_CC_RESET_PRESET and synth_controller.getShiftPressedState():
        synth_controller.resetFXPreset()
    elif event.data1 == MIDI_CC_EFFECT_1 and synth_controller.isSaveMode():
        synth_controller.updateFXPreset(FXPreset.FXPreset_1)
        synth_controller.setSaveMode(False)
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_1)
    elif event.data1 == MIDI_CC_EFFECT_2 and synth_controller.isSaveMode():
        synth_controller.updateFXPreset(FXPreset.FXPreset_2)
        synth_controller.setSaveMode(False)
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_2)
    elif event.data1 == MIDI_CC_EFFECT_3 and synth_controller.isSaveMode():
        synth_controller.updateFXPreset(FXPreset.FXPreset_3)
        synth_controller.setSaveMode(False)
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_3)
    elif event.data1 == MIDI_CC_EFFECT_4 and synth_controller.isSaveMode():
        synth_controller.updateFXPreset(FXPreset.FXPreset_4)
        synth_controller.setSaveMode(False)
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_4)
    elif event.data1 == MIDI_CC_EFFECT_5 and synth_controller.isSaveMode():
        synth_controller.updateFXPreset(FXPreset.FXPreset_5)
        synth_controller.setSaveMode(False)
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_5)
    elif event.data1 == MIDI_CC_EFFECT_6 and synth_controller.isSaveMode():
        synth_controller.updateFXPreset(FXPreset.FXPreset_6)
        synth_controller.setSaveMode(False)
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_6)
    elif event.data1 == MIDI_CC_EFFECT_7 and synth_controller.isSaveMode():
        synth_controller.updateFXPreset(FXPreset.FXPreset_7)
        synth_controller.setSaveMode(False)
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_7)
    elif event.data1 == MIDI_CC_EFFECT_8 and synth_controller.isSaveMode():
        synth_controller.updateFXPreset(FXPreset.FXPreset_8)
        synth_controller.setSaveMode(False)
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_8)
    elif event.data1 == MIDI_CC_EFFECT_1 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_1)
    elif event.data1 == MIDI_CC_EFFECT_2 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_2)
    elif event.data1 == MIDI_CC_EFFECT_3 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_3)
    elif event.data1 == MIDI_CC_EFFECT_4 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_4)
    elif event.data1 == MIDI_CC_EFFECT_5 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_5)
    elif event.data1 == MIDI_CC_EFFECT_6 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_6)
    elif event.data1 == MIDI_CC_EFFECT_7 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_7)
    elif event.data1 == MIDI_CC_EFFECT_8 and not synth_controller.getShiftPressedState():
        synth_controller.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_8)
    elif event.data1 == MIDI_CC_SYNTH_VOLUME:
        synth_controller.setSynthVolume((event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
    elif event.data1 == MIDI_CC_FX_LEVEL:
        synth_controller.setFXLevel(event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_EFFECT_PARAM_1:
        synth_controller.setFXParameterLevel(FXParameter.FXParameter_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_EFFECT_PARAM_2:
        synth_controller.setFXParameterLevel(FXParameter.FXParameter_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_EFFECT_PARAM_3:
        synth_controller.setFXParameterLevel(FXParameter.FXParameter_3, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_EFFECT_PARAM_4:
        synth_controller.setFXParameterLevel(FXParameter.FXParameter_4, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_EFFECT_PARAM_5:
        synth_controller.setFXParameterLevel(FXParameter.FXParameter_5, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_EFFECT_PARAM_6:
        synth_controller.setFXParameterLevel(FXParameter.FXParameter_6, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_EFFECT_PARAM_7:
        synth_controller.setFXParameterLevel(FXParameter.FXParameter_7, event.data2 / fl_helper.MIDI_MAX_VALUE)
    elif event.data1 == MIDI_CC_EFFECT_PARAM_8:
        synth_controller.setFXParameterLevel(FXParameter.FXParameter_8, event.data2 / fl_helper.MIDI_MAX_VALUE)
        
    event.handled = True
