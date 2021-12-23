

# python imports
import math
import time

# FL imports
import transport
import mixer
import plugins
import playlist

from common import fl_helper

# MIDI CC
MIDI_CC_SHIFT                      = 95
MIDI_CC_ENTER_SAVE_MODE            = 53
MIDI_CC_RESET_PRESET               = 54
MIDI_CC_PREV_ACTIVE_FX_UNIT_PRESET = 55
MIDI_CC_NEXT_ACTIVE_FX_UNIT_PRESET = 56
MIDI_CC_EFFECTS_PAGE_1             = 49
MIDI_CC_EFFECTS_PAGE_2             = 50
MIDI_CC_EFFECTS_PAGE_3             = 51
MIDI_CC_EFFECTS_PAGE_4             = 52

MIDI_CC_EFFECT_1              = 49
MIDI_CC_EFFECT_2              = 50
MIDI_CC_EFFECT_3              = 51
MIDI_CC_EFFECT_4              = 52
MIDI_CC_EFFECT_5              = 53
MIDI_CC_EFFECT_6              = 54
MIDI_CC_EFFECT_7              = 55
MIDI_CC_EFFECT_8              = 56

MIDI_CC_SYNTH_VOLUME          = 93
MIDI_CC_FX_LEVEL              = 93

MIDI_CC_TURNADO_DICTATOR      = 94
MIDI_CC_TURNADO_DRY_WET       = 94
MIDI_CC_TURNADO_RANDOMIZE     = 95

MIDI_CC_TURNADO_PREV_PRESET   = 36
MIDI_CC_TURNADO_NEXT_PRESET   = 37
MIDI_CC_TURNADO_ON_OFF        = 38
MIDI_CC_CHANGE_ACTIVE_FX_UNIT = 39

MIDI_CC_EFFECT_PARAM_1        = 70
MIDI_CC_EFFECT_PARAM_2        = 71
MIDI_CC_EFFECT_PARAM_3        = 72
MIDI_CC_EFFECT_PARAM_4        = 73
MIDI_CC_EFFECT_PARAM_5        = 74
MIDI_CC_EFFECT_PARAM_6        = 75
MIDI_CC_EFFECT_PARAM_7        = 76
MIDI_CC_EFFECT_PARAM_8        = 77

# ROUTING
# ...

# CONSTANTS

KP3_PLUS_ABCD_PRESSED         = 100
KP3_PLUS_ABCD_RELEASED        = 64

NUMBER_OF_FX_IN_PAGE          = 8

FINISHER_VOODOO_MODE_NUMBER   = 50

DEFAULT_TURNADO_DRY_WET_LEVEL = 0.5

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

TURNADO_SLOT_INDEX             = 0

NO_ADJUSTABLE_EFFECT_AVAILABLE = -1

PRESET_CHANGE_PROTECTOR_PANOMATIC_SLOT_INDEX = 9

# PARAMS LIMITS
FABFILTER_PRO_Q3_PARAMS_LIMIT = 360
FINISHER_VOODOO_PARAMS_LIMIT  = 10
MANIPULATOR_PARAMS_LIMIT      = 200
TURNADO_PARAMS_LIMIT          = 4000

# PLUGIN PARAMETERS
PANOMATIC_VOLUME_PARAM_INDEX = 1

FINISHER_VOODOO_MODE_PARAM_INDEX   = 2
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

TURNADO_DICTATOR_PARAM_INDEX       = 8
TURNADO_DRY_WET_PARAM_INDEX        = 9
TURNADO_RANDOMIZE_PARAM_INDEX      = 10

TURNADO_NEXT_PRESET_PARAM_INDEX    = 8
TURNADO_PREV_PRESET_PARAM_INDEX    = 8

INVALID_PARAM = -1

def getAdjustablePlugin(context):

    parameter_id = fl_helper.findSurfaceControlElementIdByName(context.main_channel, "E2_TO", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
    finisher_voodoo_state = fl_helper.externalParamMapping(plugins.getParamValue(parameter_id, context.main_channel, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX))

    if 1.0 == finisher_voodoo_state:
        return FINISHER_VOODOO_SLOT_INDEX

    parameter_id = fl_helper.findSurfaceControlElementIdByName(context.main_channel, "E3_TO", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
    manipulator_state = fl_helper.externalParamMapping(plugins.getParamValue(parameter_id, context.main_channel, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX))

    if 1.0 == manipulator_state:
        return MANIPULATOR_SLOT_INDEX

    return NO_ADJUSTABLE_EFFECT_AVAILABLE

class Context:

    def __init__(self, device_name, main_channel, fx1_channel, fx2_channel, params_first_storage_track_id):
        self.device_name = device_name
        self.main_channel = main_channel
        self.fx1_channel = fx1_channel
        self.fx2_channel = fx2_channel
        self.params_first_storage_track_id = params_first_storage_track_id

class FXParameter:
    FXParameter_1 = 0
    FXParameter_2 = 1
    FXParameter_3 = 2
    FXParameter_4 = 3
    FXParameter_5 = 4
    FXParameter_6 = 5
    FXParameter_7 = 6
    FXParameter_8 = 7

    def __init__(self, context, fx_param_id, view):
        self.__context = context
        self.__fx_param_level = 0.0
        self.__fx_param_id = fx_param_id
        self.__view = view

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

        adjustable_plugin_slot_index = getAdjustablePlugin(self.__context)

        if adjustable_plugin_slot_index != NO_ADJUSTABLE_EFFECT_AVAILABLE:
            fl_param_id = self.getFLParamIndex(adjustable_plugin_slot_index, self.__fx_param_id)

            if fl_param_id != INVALID_PARAM:
                plugins.setParamValue(fx_param_level, fl_param_id, self.__context.fx1_channel, adjustable_plugin_slot_index)
                self.__fx_param_level = fx_param_level
                self.__view.setFXParameterLevel(self.__fx_param_id, fx_param_level)

    def onInitScript(self):
        self.setLevel(self.__fx_param_level)

    def updateParamsFromPlugin(self):

        adjustable_plugin_slot_index = getAdjustablePlugin(self.__context)

        if adjustable_plugin_slot_index != NO_ADJUSTABLE_EFFECT_AVAILABLE:

            fl_param_id = self.getFLParamIndex(adjustable_plugin_slot_index, self.__fx_param_id)

            if fl_param_id != INVALID_PARAM:
                self.__fx_param_level = fl_helper.externalParamMapping(plugins.getParamValue(fl_param_id, self.__context.fx1_channel, FINISHER_VOODOO_SLOT_INDEX))
                self.__view.setFXParameterActivationStatus(self.__fx_param_id, 1)
            else:
                self.__fx_param_level = 0.0
                self.__view.setFXParameterActivationStatus(self.__fx_param_id, 0)

            self.__view.setFXParameterLevel(self.__fx_param_id, self.__fx_param_level)

        else:

            self.__fx_param_level = 0.0
            self.__view.setFXParameterActivationStatus(self.__fx_param_id, 0)
            self.__view.setFXParameterLevel(self.__fx_param_id, self.__fx_param_level)

class FXUnit:
    FX_UNIT_NONE            = 0
    FX_UNIT_MANIPULATOR     = 1
    FX_UNIT_FINISHER_VOODOO = 2

class FXPreset:

    FXPreset_1    = 0
    FXPreset_2    = 1
    FXPreset_3    = 2
    FXPreset_4    = 3
    FXPreset_5    = 4
    FXPreset_6    = 5
    FXPreset_7    = 6
    FXPreset_8    = 7

    def __init__(self, context, fx_page_number, fx_number, view):
        self.__context = context
        self.__view = view
        self.__fx_page_number = fx_page_number
        self.__fx_number = fx_number
        self.__parameters = {}
        self.__fx_parameters = { FXParameter.FXParameter_1: FXParameter(self.__context, FXParameter.FXParameter_1, view),
                                 FXParameter.FXParameter_2: FXParameter(self.__context, FXParameter.FXParameter_2, view),
                                 FXParameter.FXParameter_3: FXParameter(self.__context, FXParameter.FXParameter_3, view),
                                 FXParameter.FXParameter_4: FXParameter(self.__context, FXParameter.FXParameter_4, view),
                                 FXParameter.FXParameter_5: FXParameter(self.__context, FXParameter.FXParameter_5, view),
                                 FXParameter.FXParameter_6: FXParameter(self.__context, FXParameter.FXParameter_6, view),
                                 FXParameter.FXParameter_7: FXParameter(self.__context, FXParameter.FXParameter_7, view),
                                 FXParameter.FXParameter_8: FXParameter(self.__context, FXParameter.FXParameter_8, view) }

        self.__active_fx_unit = FXUnit.FX_UNIT_NONE

    def onInitScript(self):
        self.__loadParameters()

        for fx_parameter_id in self.__fx_parameters:
            self.__fx_parameters[fx_parameter_id].onInitScript()

        self.setActiveFXUnit(self.getActiveFXUnit())

    def update(self):
        self.__getParamsFromPlugins()
        self.__saveParameters()
        self.__applyParametersToPlugins()

    def reset(self):
        self.__resetParameters()
        self.__parameters.clear()

    def select(self):
        plugins.setParamValue(0.0, PANOMATIC_VOLUME_PARAM_INDEX, self.__context.main_channel, PRESET_CHANGE_PROTECTOR_PANOMATIC_SLOT_INDEX)

        if not self.__areParametersLoaded():
            self.__loadParameters()

        self.__applyParametersToPlugins()
        self.__view.selectFXPreset(self.__fx_number)

        plugins.setParamValue(fl_helper.MAX_VOLUME_LEVEL_VALUE, PANOMATIC_VOLUME_PARAM_INDEX, self.__context.main_channel, PRESET_CHANGE_PROTECTOR_PANOMATIC_SLOT_INDEX)

    def view_updateFXPresetAvailability(self):
        self.__view.setFXPresetAvailability(self.__fx_number, len(self.__parameters) > 0)

    def view_updateFXParamsFromPlugins(self):
        for fx_param_id in self.__fx_parameters:
            self.__fx_parameters[fx_param_id].updateParamsFromPlugin()

    def view_updateActiveFXUnit(self):
        self.setActiveFXUnit(self.getActiveFXUnit())

    def setFXParameterLevel(self, fx_param_id, fx_param_level):
        self.__fx_parameters[fx_param_id].setLevel(fx_param_level)

    def getActiveFXUnit(self):
        active_fx_unit = FXUnit.FX_UNIT_NONE

        adjustable_plugin = getAdjustablePlugin(self.__context)

        if adjustable_plugin == MANIPULATOR_SLOT_INDEX:
            active_fx_unit = FXUnit.FX_UNIT_MANIPULATOR
        elif adjustable_plugin == FINISHER_VOODOO_SLOT_INDEX:
            active_fx_unit = FXUnit.FX_UNIT_FINISHER_VOODOO

        return active_fx_unit

    def setActiveFXUnit(self, active_fx_unit):

        manipulator_activation_status_value = 0.0
        finisher_voodoo_activation_status_value = 0.0


        if active_fx_unit == FXUnit.FX_UNIT_MANIPULATOR:
            manipulator_activation_status_value = 1.0
        elif active_fx_unit == FXUnit.FX_UNIT_FINISHER_VOODOO:
            finisher_voodoo_activation_status_value = 1.0

        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "E3_TO", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(manipulator_activation_status_value, parameter_id, self.__context.main_channel, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)

        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "E2_TO", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(finisher_voodoo_activation_status_value, parameter_id, self.__context.main_channel, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)

        self.__view.setActiveFXUnit(active_fx_unit)
        self.view_updateFXParamsFromPlugins()

    def __areParametersLoaded(self):
        return len(self.__parameters) != 0

    def __getParamsFromPlugins(self):
        self.__parameters.clear()

        self.__parameters[FX_ACTIVATION_STATE_SLOT_INDEX] = []

        for mixer_slot in range(10):

            self.__parameters[mixer_slot] = []

            param_count = plugins.getParamCount(self.__context.fx1_channel, mixer_slot)

            for param_id in range(param_count):

                if mixer_slot == MANIPULATOR_SLOT_INDEX and param_id > MANIPULATOR_PARAMS_LIMIT:
                    break;

                if mixer_slot == FINISHER_VOODOO_SLOT_INDEX and param_id > FINISHER_VOODOO_PARAMS_LIMIT:
                    break;

                if mixer_slot == FABFILTER_PRO_Q3_SLOT_INDEX and param_id > FABFILTER_PRO_Q3_PARAMS_LIMIT:
                    break;

                param_value = plugins.getParamValue(param_id, self.__context.fx1_channel, mixer_slot)

                if mixer_slot == MANIPULATOR_SLOT_INDEX or \
                   mixer_slot == FABFILTER_PRO_Q3_SLOT_INDEX or \
                   mixer_slot == FINISHER_VOODOO_SLOT_INDEX:
                    param_value = fl_helper.externalParamMapping(param_value)

                param_value_str = str(param_value)

                # param_name = plugins.getParamName(param_id, self.__context.fx1_channel, mixer_slot)
                # plugin_name = plugins.getPluginName(self.__context.fx1_channel, mixer_slot)
                # print("Get parameter: plugin name - " + plugin_name + ", param - " + param_name + \
                #       ", param_value - " + param_value_str + ", param_id - " + str(param_id) + \
                #       ", channel - " + str(self.__context.fx1_channel) + ", mixer_slot - " + str(mixer_slot))

                self.__parameters[mixer_slot].append( param_value_str )


            parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "E" + str(mixer_slot+1) + "_TO", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            fx_activation_state = plugins.getParamValue(parameter_id, self.__context.main_channel, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            self.__parameters[FX_ACTIVATION_STATE_SLOT_INDEX].append(str( fl_helper.externalParamMapping(fx_activation_state) ))

    def __applyParametersToPlugins(self):
        for mixer_slot in self.__parameters:

            for param_id, param_value_str in reversed(list(enumerate(self.__parameters[mixer_slot]))):

                param_value = float(param_value_str)

                if mixer_slot == FX_ACTIVATION_STATE_SLOT_INDEX:
                    #print("__applyParametersToPlugins: FX_ACTIVATION_STATE_SLOT_INDEX mixer channel -" + str(self.__context.main_channel) + \
                    #", param_id - " + str(param_id) + ", param_value - " + str(param_value))
                    plugins.setParamValue(param_value, param_id, self.__context.main_channel, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
                else:

                    # plugin_name = plugins.getPluginName(self.__context.fx1_channel, mixer_slot)
                    # param_name = plugins.getParamName(param_id, self.__context.fx1_channel, mixer_slot)
                    #
                    # print("Apply parameter: plugin name - " + plugin_name + ", param - " + param_name + \
                    #       ", param_value - " + str(param_value) + ", param_id - " + str(param_id) + \
                    #       ", channel - " + str(self.__context.fx1_channel) + ", mixer_slot - " + str(mixer_slot))

                    plugins.setParamValue(param_value, param_id, self.__context.fx1_channel, mixer_slot)

    def __loadParameters(self):
        paramsStr = playlist.getTrackName( self.__context.params_first_storage_track_id + ( self.__fx_page_number * NUMBER_OF_FX_IN_PAGE ) + self.__fx_number)

        if paramsStr:
            try:
                self.__parameters = eval(paramsStr)
            except Exception as e:
                self.__parameters.clear()

    def __saveParameters(self):
        playlist.setTrackName( self.__context.params_first_storage_track_id + ( self.__fx_page_number * NUMBER_OF_FX_IN_PAGE ) + self.__fx_number,  str(self.__parameters))

    def __resetParameters(self):
        playlist.setTrackName( self.__context.params_first_storage_track_id + ( self.__fx_page_number * NUMBER_OF_FX_IN_PAGE ) + self.__fx_number,  "")

class FXPresetPage:

    FXPresetPage_1 = 0
    FXPresetPage_2 = 1
    FXPresetPage_3 = 2
    FXPresetPage_4 = 3

    def __init__(self, context, fx_page_number, view):
        self.__context = context
        self.__view = view
        self.__fx_page_number = fx_page_number
        self.__selected_fx_preset_id = FXPreset.FXPreset_1
        self.__fx_presets = { FXPreset.FXPreset_1: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_1, self.__view),
                       FXPreset.FXPreset_2: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_2, self.__view),
                       FXPreset.FXPreset_3: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_3, self.__view),
                       FXPreset.FXPreset_4: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_4, self.__view),
                       FXPreset.FXPreset_5: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_5, self.__view),
                       FXPreset.FXPreset_6: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_6, self.__view),
                       FXPreset.FXPreset_7: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_7, self.__view),
                       FXPreset.FXPreset_8: FXPreset(self.__context, fx_page_number, FXPreset.FXPreset_8, self.__view), }

    def select(self):
        self.selectFXPreset(self.__selected_fx_preset_id)
        self.__view_updateStats()

    def getSelectedFXPresetID(self):
        return self.__selected_fx_preset_id

    def onInitScript(self):
        for fx_preset_id in self.__fx_presets:
            self.__fx_presets[fx_preset_id].onInitScript()

    def updateFXPreset(self, fx_preset_id):
        self.__fx_presets[fx_preset_id].update()
        self.__fx_presets[fx_preset_id].view_updateFXPresetAvailability()
        self.__fx_presets[fx_preset_id].view_updateFXParamsFromPlugins()
        self.__fx_presets[fx_preset_id].view_updateActiveFXUnit()

    def resetFXPreset(self, fx_preset_id):
        self.__fx_presets[fx_preset_id].reset()
        self.__fx_presets[fx_preset_id].view_updateFXPresetAvailability()
        self.__fx_presets[fx_preset_id].view_updateFXParamsFromPlugins()
        self.__fx_presets[fx_preset_id].view_updateActiveFXUnit()

    def selectFXPreset(self, fx_preset_id):
        print(self.__context.device_name + '_FXPresetPage' + ': ' + FXPresetPage.selectFXPreset.__name__ + " page - " + str(self.__fx_page_number) + ", preset - " + str(fx_preset_id))
        self.__selected_fx_preset_id = fx_preset_id
        self.__fx_presets[fx_preset_id].select()
        self.__fx_presets[fx_preset_id].view_updateFXPresetAvailability()
        self.__fx_presets[fx_preset_id].view_updateFXParamsFromPlugins()
        self.__fx_presets[fx_preset_id].view_updateActiveFXUnit()

    def view_updateFXParamsFromPlugins(self):
        self.__fx_presets[self.__selected_fx_preset_id].view_updateFXParamsFromPlugins()

    def setFXParameterLevel(self, fx_param_id, fx_param_level):
            self.__fx_presets[self.__selected_fx_preset_id].setFXParameterLevel(fx_param_id, fx_param_level)

    def __view_updateStats(self):
        self.__view.selectFXPage(self.__fx_page_number)

        for fx_preset_id in self.__fx_presets:
            self.__fx_presets[fx_preset_id].view_updateFXPresetAvailability()

        self.__fx_presets[fx_preset_id].view_updateFXParamsFromPlugins()
        self.__fx_presets[fx_preset_id].view_updateActiveFXUnit()

    def changeActiveFXUnit(self):
        active_fx_unit = self.__fx_presets[self.__selected_fx_preset_id].getActiveFXUnit()

        if active_fx_unit == FXUnit.FX_UNIT_NONE:
            print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.changeActiveFXUnit.__name__ + ": to manipulator")
            self.__fx_presets[self.__selected_fx_preset_id].setActiveFXUnit(FXUnit.FX_UNIT_MANIPULATOR)
        elif active_fx_unit == FXUnit.FX_UNIT_MANIPULATOR:
            print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.changeActiveFXUnit.__name__ + ": to finisher voodoo")
            self.__fx_presets[self.__selected_fx_preset_id].setActiveFXUnit(FXUnit.FX_UNIT_FINISHER_VOODOO)
        elif active_fx_unit == FXUnit.FX_UNIT_FINISHER_VOODOO:
            print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.changeActiveFXUnit.__name__ + ": to none")
            self.__fx_presets[self.__selected_fx_preset_id].setActiveFXUnit(FXUnit.FX_UNIT_NONE)

    def getActiveFXUnit(self):
        return self.__fx_presets[self.__selected_fx_preset_id].getActiveFXUnit()

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

    def __init__(self, context, fx_number, view):
        self.__context = context
        self.__fx_number = fx_number
        self.__view = view
        self.__activation_param_id = -1
        self.__level_param_id = -1
        self.__fx_level = 0

    def setFXLevel(self, fx_level, force = False):

        if self.__activation_param_id == -1:
            self.__activation_param_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "E" + str(self.__fx_number + 1) + "_TO", MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)

        if math.fabs(self.__fx_level - fx_level) >= 0.01 or fx_level == 1.0 or True == force:

            fx_activation_status = fl_helper.externalParamMapping( plugins.getParamValue(self.__activation_param_id, self.__context.main_channel, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX) )

            if self.__level_param_id == -1:
                self.__level_param_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "FX_L" + str(self.__fx_number + 1), MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)

            if fx_activation_status == 0.0:
                plugins.setParamValue(0.0, self.__level_param_id, self.__context.main_channel, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            else:
                plugins.setParamValue(fx_level, self.__level_param_id, self.__context.main_channel, MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX)

            self.__fx_level = fx_level

class View:

    def __init__(self, context):
        self.__context = context
        print(self.__context.device_name + ': ' + View.__init__.__name__)

    def setShiftPressedState(self, shift_pressed):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "Shift", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(shift_pressed, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        self.resetToggleFlags()

    def resetToggleFlags(self):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "Delete", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def selectFXPage(self, preset_fx_page_id):
        for i in range(4):
            value = 0.0
            if i == preset_fx_page_id:
                value = 1.0

            parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "Page " + str(i + 1), SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(value, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

        self.resetToggleFlags()

    def selectFXPreset(self, preset_fx_id):
        for i in range(8):
            value = 0.0
            if i == preset_fx_id:
                value = 1.0

            parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "FX" + str(i + 1), SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
            plugins.setParamValue(value, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

        self.resetToggleFlags()

    def setSaveMode(self, save_mode):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "Save mode", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(save_mode, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def resetFXPreset(self):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "Delete", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setVolume(self, synth_volume):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "Volume", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(synth_volume, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setFXLevel(self, fx_level):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "FX level", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(fx_level, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setFXPresetAvailability(self, fx_preset_id, preset_availability):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "FX_" + str(fx_preset_id + 1) + "_A", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(preset_availability, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setFXParameterLevel(self, fx_param_id, fx_level):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "FXP" + str(fx_param_id + 1), SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(fx_level, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setFXParameterActivationStatus(self, fx_param_id, activation_status):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "FX_P_" + str(fx_param_id + 1) + "_A", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(activation_status, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setTurnadoDryWetLevel(self, turnado_dry_wet_level):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "T_Dry/Wet", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(turnado_dry_wet_level, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setTurnadoDictatorLevel(self, turnado_dictator_level):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "T_Dictator", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(turnado_dictator_level, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def switchToNextTurnadoPreset(self):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "T_Next_Preset", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def switchToPrevTurnadoPreset(self):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "T_Previous_Preset", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def switchActiveFXUnitToNextPreset(self):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "FX_U_Next_Preset", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def switchActiveFXUnitToPrevPreset(self):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "FX_U_Prev_Preset", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(1.0, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(0.0, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def turnadoOff(self, off_value):
        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "T_Off", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(off_value, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

    def setActiveFXUnit(self, active_fx_unit):

        manipulator_value = 0.0
        voodoo_finisher_value = 0.0
        none_value = 0.0

        if active_fx_unit == FXUnit.FX_UNIT_MANIPULATOR:
            manipulator_value = 1.0
        elif active_fx_unit == FXUnit.FX_UNIT_FINISHER_VOODOO:
            voodoo_finisher_value = 1.0
        elif active_fx_unit == FXUnit.FX_UNIT_NONE:
            none_value = 1.0

        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "AFX_Manipulator", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(manipulator_value, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "AFX_Voodoo_Finisher", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(voodoo_finisher_value, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

        parameter_id = fl_helper.findSurfaceControlElementIdByName(self.__context.main_channel, "AFX_None", SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)
        plugins.setParamValue(none_value, parameter_id, self.__context.main_channel, SYNTH_CONTROL_SURFACE_MIXER_SLOT_INDEX)

class KorgKaossPad3Plus_InputController:

    def __init__(self, context):
        print(context.device_name + ': ' + KorgKaossPad3Plus_InputController.__init__.__name__)

        self.__context = context
        self.__view = View(context)
        self.__initialized = False
        self.__shift_pressed = False
        self.__selected_fx_preset_page = FXPresetPage.FXPresetPage_1
        self.__fx_preset_pages = { FXPresetPage.FXPresetPage_1: FXPresetPage(self.__context, FXPresetPage.FXPresetPage_1, self.__view),
                                   FXPresetPage.FXPresetPage_2: FXPresetPage(self.__context, FXPresetPage.FXPresetPage_2, self.__view),
                                   FXPresetPage.FXPresetPage_3: FXPresetPage(self.__context, FXPresetPage.FXPresetPage_3, self.__view),
                                   FXPresetPage.FXPresetPage_4: FXPresetPage(self.__context, FXPresetPage.FXPresetPage_4, self.__view) }
        self.__isSaveMode = False
        self.__fxs = { FX.FX_1 : FX(self.__context, FX.FX_1, self.__view),
                      FX.FX_2 : FX(self.__context, FX.FX_2, self.__view),
                      FX.FX_3 : FX(self.__context, FX.FX_3, self.__view),
                      FX.FX_4 : FX(self.__context, FX.FX_4, self.__view),
                      FX.FX_5 : FX(self.__context, FX.FX_5, self.__view),
                      FX.FX_6 : FX(self.__context, FX.FX_6, self.__view),
                      FX.FX_7 : FX(self.__context, FX.FX_7, self.__view),
                      FX.FX_8 : FX(self.__context, FX.FX_8, self.__view),
                      FX.FX_9 : FX(self.__context, FX.FX_9, self.__view),
                      FX.FX_10 : FX(self.__context, FX.FX_10, self.__view), }

        self.__buttons_last_press_time = {}

        self.__fx_level = 1.0

        self.__turnado_dry_wet_level = 0.0
        self.__turnado_dictator_level = 0.0
        self.__turnado_is_off = True

    def onInitScript(self):

        if False == self.__initialized:
            print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.onInitScript.__name__)

            try:
                for preset_page_id in self.__fx_preset_pages:
                    self.__fx_preset_pages[preset_page_id].onInitScript()

                self.reset()

                self.__initialized = True

            except Exception as e:
                print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.onInitScript.__name__ + ": failed to initialize the script.")
                print(e)

    def actionOnDoubleClick(self, pressed_button, action):
        pressed_time = time.time()

        if not pressed_button in self.__buttons_last_press_time.keys():
            self.__buttons_last_press_time[pressed_button] = 0

        if (pressed_time - self.__buttons_last_press_time[pressed_button]) < 0.5:
            # double click
            self.__buttons_last_press_time[pressed_button] = 0
            action()
        else:
            self.__buttons_last_press_time[pressed_button] = pressed_time

    def isSaveMode(self):
        return self.__isSaveMode

    def setSaveMode(self, save_mode):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.setSaveMode.__name__ + ": save mode - " + str(save_mode))
        self.__isSaveMode = save_mode
        self.__view.setSaveMode(save_mode)

    def selectFXPage(self, preset_fx_page_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.selectFXPage.__name__ + ": fx page id - " + str(preset_fx_page_id))
        self.__selected_fx_preset_page = preset_fx_page_id;
        self.__fx_preset_pages[self.__selected_fx_preset_page].select()
        
        self.setFXLevel(self.__fx_level, True)

    def setShiftPressedState(self, shift_pressed):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.setShiftPressedState.__name__ + ": shift pressed - " + str(shift_pressed))
        self.__view.setShiftPressedState(shift_pressed)
        self.__shift_pressed = shift_pressed

        if(True == shift_pressed):
            self.actionOnDoubleClick(MIDI_CC_SHIFT, self.randomizeTurnado)

    def randomizeTurnado(self):
        print(self.__context.device_name + ': ' + self.randomizeTurnado.__name__)
        plugins.setParamValue(0.0, TURNADO_RANDOMIZE_PARAM_INDEX, self.__context.fx2_channel, TURNADO_SLOT_INDEX)
        plugins.setParamValue(1.0, TURNADO_RANDOMIZE_PARAM_INDEX, self.__context.fx2_channel, TURNADO_SLOT_INDEX)
        plugins.setParamValue(0.0, TURNADO_RANDOMIZE_PARAM_INDEX, self.__context.fx2_channel, TURNADO_SLOT_INDEX)
        self.__restoreParams()

    def getShiftPressedState(self):
        return self.__shift_pressed

    def selectFXPresetOnTheVisiblePage(self, preset_fx_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.selectFXPresetOnTheVisiblePage.__name__ + ": selected page - " + \
              str(self.__selected_fx_preset_page) + ", selected FX - " + str(preset_fx_id))
        self.__fx_preset_pages[self.__selected_fx_preset_page].selectFXPreset(preset_fx_id)

        self.setFXLevel(self.__fx_level, True)

    def updateFXPreset(self, fx_preset_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.updateFXPreset.__name__)
        self.__fx_preset_pages[self.__selected_fx_preset_page].updateFXPreset(fx_preset_id)

    def resetFXPreset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.resetFXPreset.__name__)
        self.__fx_preset_pages[self.__selected_fx_preset_page].resetFXPreset(self.getSelectedFXPresetID())
        self.__view.resetFXPreset()

    def setVolume(self, synth_volume):
        mixer.setTrackVolume(self.__context.fx2_channel, synth_volume)
        self.__view.setVolume(synth_volume)

    def setFXLevel(self, fx_level, force = False):
        for fx_id in self.__fxs:
            self.__fxs[fx_id].setFXLevel(fx_level, force)
        self.__view.setFXLevel(fx_level)
        self.__fx_level = fx_level

    def setFXParameterLevel(self, fx_parameter_id, effect_level):
        self.__fx_preset_pages[self.__selected_fx_preset_page].setFXParameterLevel(fx_parameter_id, effect_level)

    def getSelectedFXPresetID(self):
        return self.__fx_preset_pages[self.__selected_fx_preset_page].getSelectedFXPresetID()

    def setTurnadoDryWetLevel(self, turnado_dry_wet_level):
        self.__turnado_dry_wet_level = turnado_dry_wet_level
        plugins.setParamValue(self.__turnado_dry_wet_level, TURNADO_DRY_WET_PARAM_INDEX, self.__context.fx2_channel, TURNADO_SLOT_INDEX)

        if turnado_dry_wet_level == 0.0:
            self.__turnado_is_off = True
        else:
            self.__turnado_is_off = False

        self.__view.setTurnadoDryWetLevel(turnado_dry_wet_level)
        self.__view.turnadoOff(turnado_dry_wet_level == 0.0)

    def setTurnadoDictatorLevel(self, turnado_dictator_level):
        self.__turnado_dictator_level = turnado_dictator_level
        plugins.setParamValue(self.__turnado_dictator_level, TURNADO_DICTATOR_PARAM_INDEX, self.__context.fx2_channel, TURNADO_SLOT_INDEX)

        self.__view.setTurnadoDictatorLevel(turnado_dictator_level)

    def switchToNextTurnadoPreset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.switchToNextTurnadoPreset.__name__)
        plugins.nextPreset(self.__context.fx2_channel, TURNADO_SLOT_INDEX)
        self.__restoreParams()

        self.__view.switchToNextTurnadoPreset()

    def switchToPrevTurnadoPreset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.switchToPrevTurnadoPreset.__name__)
        plugins.prevPreset(self.__context.fx2_channel, TURNADO_SLOT_INDEX)
        self.__restoreParams()

        self.__view.switchToPrevTurnadoPreset()

    def turnadoOnOff(self):
        self.__turnado_is_off = not self.__turnado_is_off

        if self.__turnado_is_off == False:
            if self.__turnado_dry_wet_level != 0.0:
                val = self.__turnado_dry_wet_level
            else:
                val = 1.0
        else:
            val = 0.0

        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.turnadoOnOff.__name__ + ": turnado fx level - " + str(val))

        plugins.setParamValue(val, TURNADO_DRY_WET_PARAM_INDEX, self.__context.fx2_channel, TURNADO_SLOT_INDEX)

        self.__view.turnadoOff(val == 0.0)
        self.__view.setTurnadoDryWetLevel(val)

    def __restoreParams(self):
        plugins.setParamValue(self.__turnado_dictator_level, TURNADO_DICTATOR_PARAM_INDEX, self.__context.fx2_channel, TURNADO_SLOT_INDEX)
        plugins.setParamValue(self.__turnado_dry_wet_level, TURNADO_DRY_WET_PARAM_INDEX, self.__context.fx2_channel, TURNADO_SLOT_INDEX)

    def __selectFXPreset(self, preset_fx_page_id, preset_fx_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.__selectFXPreset.__name__ + ": selected page - " + \
              str(preset_fx_page_id) + ", selected FX - " + str(preset_fx_id))
        self.__fx_preset_pages[preset_fx_page_id].selectFXPreset(preset_fx_id)

        self.setFXLevel(self.__fx_level, True)

    def changeActiveFXUnit(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.changeActiveFXUnit.__name__)
        self.__fx_preset_pages[self.__selected_fx_preset_page].changeActiveFXUnit()
        self.setFXLevel(self.__fx_level, True)

    def switchActiveFXUnitToPrevPreset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.switchActiveFXUnitToPrevPreset.__name__)

        active_fx_unit = self.__fx_preset_pages[self.__selected_fx_preset_page].getActiveFXUnit()

        if active_fx_unit == FXUnit.FX_UNIT_MANIPULATOR:
            plugins.prevPreset(self.__context.fx1_channel, MANIPULATOR_SLOT_INDEX)
        elif active_fx_unit == FXUnit.FX_UNIT_FINISHER_VOODOO:
            currentProgram = fl_helper.externalParamMapping(plugins.getParamValue(FINISHER_VOODOO_MODE_PARAM_INDEX, self.__context.fx1_channel, FINISHER_VOODOO_SLOT_INDEX)) * FINISHER_VOODOO_MODE_NUMBER

            targetProgram = currentProgram - 1

            if targetProgram < -0.5:
                targetProgram = FINISHER_VOODOO_MODE_NUMBER

            print("targetProgram - " + str(targetProgram))

            plugins.setParamValue(targetProgram / FINISHER_VOODOO_MODE_NUMBER, FINISHER_VOODOO_MODE_PARAM_INDEX, self.__context.fx1_channel, FINISHER_VOODOO_SLOT_INDEX)

        self.__view.switchActiveFXUnitToPrevPreset()

        self.__fx_preset_pages[self.__selected_fx_preset_page].view_updateFXParamsFromPlugins()

    def switchActiveFXUnitToNextPreset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.switchActiveFXUnitToNextPreset.__name__)

        active_fx_unit = self.__fx_preset_pages[self.__selected_fx_preset_page].getActiveFXUnit()

        if active_fx_unit == FXUnit.FX_UNIT_MANIPULATOR:
            plugins.nextPreset(self.__context.fx1_channel, MANIPULATOR_SLOT_INDEX)
        elif active_fx_unit == FXUnit.FX_UNIT_FINISHER_VOODOO:
            currentProgram = fl_helper.externalParamMapping(plugins.getParamValue(FINISHER_VOODOO_MODE_PARAM_INDEX, self.__context.fx1_channel, FINISHER_VOODOO_SLOT_INDEX)) * FINISHER_VOODOO_MODE_NUMBER

            targetProgram = currentProgram + 1

            if targetProgram > FINISHER_VOODOO_MODE_NUMBER + 0.5:
                targetProgram = 0

            print("targetProgram - " + str(targetProgram))

            plugins.setParamValue(targetProgram / FINISHER_VOODOO_MODE_NUMBER, FINISHER_VOODOO_MODE_PARAM_INDEX, self.__context.fx1_channel, FINISHER_VOODOO_SLOT_INDEX)

        self.__view.switchActiveFXUnitToNextPreset()

        self.__fx_preset_pages[self.__selected_fx_preset_page].view_updateFXParamsFromPlugins()

    def reset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.reset.__name__)

        self.__selected_fx_preset_page = FXPresetPage.FXPresetPage_1
        self.selectFXPage(self.__selected_fx_preset_page)
        self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_1)

        self.__isSaveMode = False
        self.__view.setSaveMode(self.__isSaveMode)

        self.setTurnadoDictatorLevel(0.0)
        self.setTurnadoDryWetLevel(DEFAULT_TURNADO_DRY_WET_LEVEL)

        self.setFXLevel(1.0, True)
        self.setVolume(fl_helper.MAX_VOLUME_LEVEL_VALUE)

    def OnMidiMsg(self, event):

        #fl_helper.printAllPluginParameters(self.__context.fx1_channel, MANIPULATOR_SLOT_INDEX)

        self.onInitScript()

        event.handled = False

        if event.data1 == MIDI_CC_EFFECTS_PAGE_1 and self.getShiftPressedState():
            self.selectFXPage(FXPresetPage.FXPresetPage_1)
        elif event.data1 == MIDI_CC_EFFECTS_PAGE_2 and self.getShiftPressedState():
            self.selectFXPage(FXPresetPage.FXPresetPage_2)
        elif event.data1 == MIDI_CC_EFFECTS_PAGE_3 and self.getShiftPressedState():
            self.selectFXPage(FXPresetPage.FXPresetPage_3)
        elif event.data1 == MIDI_CC_EFFECTS_PAGE_4 and self.getShiftPressedState():
            self.selectFXPage(FXPresetPage.FXPresetPage_4)
        elif event.data1 == MIDI_CC_SHIFT:
            self.setShiftPressedState(event.data2 == fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == MIDI_CC_ENTER_SAVE_MODE and self.getShiftPressedState():
            self.setSaveMode(not self.isSaveMode())
        elif event.data1 == MIDI_CC_RESET_PRESET and self.getShiftPressedState():
            self.resetFXPreset()
        elif event.data1 == MIDI_CC_PREV_ACTIVE_FX_UNIT_PRESET and self.getShiftPressedState():
            self.switchActiveFXUnitToPrevPreset()
        elif event.data1 == MIDI_CC_NEXT_ACTIVE_FX_UNIT_PRESET and self.getShiftPressedState():
            self.switchActiveFXUnitToNextPreset()
        elif event.data1 == MIDI_CC_EFFECT_1 and self.isSaveMode():
            self.updateFXPreset(FXPreset.FXPreset_1)
            self.setSaveMode(False)
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_1)
        elif event.data1 == MIDI_CC_EFFECT_2 and self.isSaveMode():
            self.updateFXPreset(FXPreset.FXPreset_2)
            self.setSaveMode(False)
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_2)
        elif event.data1 == MIDI_CC_EFFECT_3 and self.isSaveMode():
            self.updateFXPreset(FXPreset.FXPreset_3)
            self.setSaveMode(False)
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_3)
        elif event.data1 == MIDI_CC_EFFECT_4 and self.isSaveMode():
            self.updateFXPreset(FXPreset.FXPreset_4)
            self.setSaveMode(False)
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_4)
        elif event.data1 == MIDI_CC_EFFECT_5 and self.isSaveMode():
            self.updateFXPreset(FXPreset.FXPreset_5)
            self.setSaveMode(False)
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_5)
        elif event.data1 == MIDI_CC_EFFECT_6 and self.isSaveMode():
            self.updateFXPreset(FXPreset.FXPreset_6)
            self.setSaveMode(False)
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_6)
        elif event.data1 == MIDI_CC_EFFECT_7 and self.isSaveMode():
            self.updateFXPreset(FXPreset.FXPreset_7)
            self.setSaveMode(False)
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_7)
        elif event.data1 == MIDI_CC_EFFECT_8 and self.isSaveMode():
            self.updateFXPreset(FXPreset.FXPreset_8)
            self.setSaveMode(False)
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_8)
        elif event.data1 == MIDI_CC_EFFECT_1 and not self.getShiftPressedState():
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_1)
        elif event.data1 == MIDI_CC_EFFECT_2 and not self.getShiftPressedState():
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_2)
        elif event.data1 == MIDI_CC_EFFECT_3 and not self.getShiftPressedState():
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_3)
        elif event.data1 == MIDI_CC_EFFECT_4 and not self.getShiftPressedState():
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_4)
        elif event.data1 == MIDI_CC_EFFECT_5 and not self.getShiftPressedState():
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_5)
        elif event.data1 == MIDI_CC_EFFECT_6 and not self.getShiftPressedState():
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_6)
        elif event.data1 == MIDI_CC_EFFECT_7 and not self.getShiftPressedState():
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_7)
        elif event.data1 == MIDI_CC_EFFECT_8 and not self.getShiftPressedState():
            self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_8)
        elif event.data1 == MIDI_CC_FX_LEVEL and self.getShiftPressedState():
            self.setFXLevel(event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == MIDI_CC_TURNADO_DRY_WET and self.getShiftPressedState():
            self.setTurnadoDryWetLevel(event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == MIDI_CC_TURNADO_DICTATOR:
            self.setTurnadoDictatorLevel(event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == MIDI_CC_EFFECT_PARAM_1:
            self.setFXParameterLevel(FXParameter.FXParameter_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == MIDI_CC_EFFECT_PARAM_2:
            self.setFXParameterLevel(FXParameter.FXParameter_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == MIDI_CC_EFFECT_PARAM_3:
            self.setFXParameterLevel(FXParameter.FXParameter_3, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == MIDI_CC_EFFECT_PARAM_4:
            self.setFXParameterLevel(FXParameter.FXParameter_4, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == MIDI_CC_EFFECT_PARAM_5:
            self.setFXParameterLevel(FXParameter.FXParameter_5, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == MIDI_CC_EFFECT_PARAM_6:
            self.setFXParameterLevel(FXParameter.FXParameter_6, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == MIDI_CC_EFFECT_PARAM_7:
            self.setFXParameterLevel(FXParameter.FXParameter_7, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == MIDI_CC_EFFECT_PARAM_8:
            self.setFXParameterLevel(FXParameter.FXParameter_8, event.data2 / fl_helper.MIDI_MAX_VALUE)
        elif event.data1 == MIDI_CC_SYNTH_VOLUME:
            self.setVolume((event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
        elif event.data1 == MIDI_CC_TURNADO_NEXT_PRESET and event.data2 == KP3_PLUS_ABCD_PRESSED:
            self.switchToNextTurnadoPreset()
        elif event.data1 == MIDI_CC_TURNADO_PREV_PRESET and event.data2 == KP3_PLUS_ABCD_PRESSED:
            self.switchToPrevTurnadoPreset()
        elif event.data1 == MIDI_CC_TURNADO_ON_OFF and event.data2 == KP3_PLUS_ABCD_PRESSED:
            self.turnadoOnOff()
        elif event.data1 == MIDI_CC_CHANGE_ACTIVE_FX_UNIT and not self.getShiftPressedState() and event.data2 == KP3_PLUS_ABCD_PRESSED:
            self.changeActiveFXUnit()
        elif event.data1 == MIDI_CC_CHANGE_ACTIVE_FX_UNIT and self.getShiftPressedState() and event.data2 == KP3_PLUS_ABCD_PRESSED:
            self.reset()

        event.handled = True
