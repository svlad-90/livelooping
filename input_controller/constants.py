'''
Created on Jan 24, 2022

@author: Dream Machines
'''

#SCENES
SCENE_EMPTY_PATTERN = 999
SCENES_PER_PRESET = 10

# MIDI CC
MIDI_CC_SCREEN_TOUCH_SCREEN_ACTION = 92
MIDI_CC_SHIFT                      = 95
MIDI_CC_ENTER_SAVE_MODE            = 53
MIDI_CC_ENTER_DELETE_MODE          = 54
MIDI_CC_PREV_ACTIVE_FX_UNIT_PRESET = 55
MIDI_CC_NEXT_ACTIVE_FX_UNIT_PRESET = 56
MIDI_CC_EFFECTS_PAGE_1             = 49
MIDI_CC_EFFECTS_PAGE_2             = 50
MIDI_CC_EFFECTS_PAGE_3             = 51
MIDI_CC_EFFECTS_PAGE_4             = 52

MIDI_CC_TRACK_SIDECHAIN_1          = 74
MIDI_CC_TRACK_SIDECHAIN_2          = 75
MIDI_CC_TRACK_SIDECHAIN_3          = 76
MIDI_CC_TRACK_SIDECHAIN_4          = 77

MIDI_CC_NEXT_SCENE                 = 70
MIDI_CC_PREV_SCENE                 = 71
MIDI_CC_TURN_OFF_SCENE             = 72
MIDI_CC_SC_LOOPERS_MODE            = 73

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
MASTER_CHANNEL                = 0

# CONSTANTS

MAX_MIXER_SLOT = 10
PERSISTENT_FX_CHANNELS_NUMBER = 2

ENTER_MIDI_MAPPING_SAVE_MODE_SHIFT = 1000

KP3_PLUS_ABCD_PRESSED         = 100
KP3_PLUS_ABCD_RELEASED        = 64

NUMBER_OF_FX_IN_PAGE          = 8

FINISHER_VOODOO_MODE_NUMBER   = 50

DEFAULT_TURNADO_DRY_WET_LEVEL = 1.0

DEFAULT_INPUT_SIDECHAIN_LEVEL = 0.0

MIDI_CC_INTERNAL_LOOP         = 123

PERSISTENCY_CURRENT_VERSION          = "2.11"
PERSISTENCY_VERSION_KEY              = "VERSION"
PERSISTENCY_PLUGIN_PARAMETERS_KEY    = "PLUGIN_PARAMS"
PERSISTENCY_ACTIVE_FX_UNIT_KEY       = "ACTIVE_FX_UNIT"
PERSISTENCY_MIDI_MAPPING_KEY         = "MIDI_MAPPING"
PERSISTENCY_TURNADO_PATCH_KEY        = "TURNADO_PATCH"

MIN_PLUGIN_NUMBER = 0
MAX_PLUGIN_NUMBER = 9

# SLOT INDICES
LOOPERS_ALL_VOCAL_SC_REACTOR_SLOT = 0

# MASTER MIXER SLOT INDICES
MIDI_ROUTING_CONTROL_SURFACE_MIXER_SLOT_INDEX = 0
INPUT_CONTROL_SURFACE_MIXER_SLOT_INDEX = 1

# FX1 CHANNEL MIXER SLOT INDICES
FX1_MULTIBAND_COMPRESSOR_SLOT_INDEX     = 0
FX1_MAXIMUX_SLOT_INDEX                  = 1
FX1_FABFILTER_PRO_Q3_SLOT_INDEX         = 2
FX1_STEREO_SHAPER_SLOT_INDEX            = 3
FX1_DISTRUCTOR_SLOT_INDEX               = 4
FX1_TURNADO_1_SLOT_INDEX                = 5
FX1_TURNADO_2_SLOT_INDEX                = 6
FX1_TURNADO_3_SLOT_INDEX                = 7
FX1_SQUEEZE_SLOT_INDEX                  = 8
FX1_ENDLESS_SMILE_SLOT_INDEX            = 9

# FX2 CHANNEL MIXER SLOT INDICES
FX2_FABFILTER_PRO_Q3_SLOT_INDEX      = 0
FX2_FINISHER_VOODOO_SLOT_INDEX       = 1
FX2_MANIPULATOR_SLOT_INDEX           = 2
FX2_FAST_DIST_SLOT_INDEX             = 3
FX2_STEREO_ENHANCER_SLOT_INDEX       = 4
FX2_WAVES_H_DELAY_SLOT_INDEX         = 5
FX2_VALHALLA_VINTAGE_VERB_SLOT_INDEX = 6
FX2_FRUITY_FILTER_SLOT_INDEX         = 7
FX2_PULSAR_1178_SLOT_INDEX           = 8
FX2_LIMITER_SLOT_INDEX               = 9

FX_ACTIVATION_STATE_CHANNEL_INDEX = 99

TURNADO_SLOT_INDEX             = 0

NO_ADJUSTABLE_EFFECT_AVAILABLE = -1

PRESET_CHANGE_PROTECTOR_PANOMATIC_SLOT_INDEX = 9

INPUT_CONTROLLER_PANOMATIC_SLOT_INDEX = 2

# PARAMS LIMITS
FABFILTER_PRO_Q3_PARAMS_LIMIT      = 360
FINISHER_VOODOO_PARAMS_LIMIT       = 10
MANIPULATOR_PARAMS_LIMIT           = 194
TURNADO_PARAMS_LIMIT               = 256
ENDLESS_SMILE_PARAMS_LIMIT         = 1
MULTIBAND_COMPRESSOR_PARAMS_LIMIT  = 56
PULSAR_1178_PARAMS_LIMIT           = 43
VALHALLA_VINTAGE_VERB_PARAMS_LIMIT = 18
WAVES_H_DELAY_PARAMS_LIMIT         = 200

# PLUGIN PARAMETERS
PANOMATIC_PAN_PARAM_INDEX = 0
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

Track_1    = 0
Track_2    = 1
Track_3    = 2
Track_4    = 3
