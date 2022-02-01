'''
Created on Jan 24, 2022

@author: Dream Machines
'''

import time

import device
import plugins
import mixer

from input_controller import constants
from input_controller.view import View
from input_controller.fx_preset_page import FXPresetPage
from input_controller.fx import FX
from input_controller.fx_preset import FXPreset
from input_controller.fx_unit import FXUnit
from input_controller.fx_parameter import FXParameter
from input_controller.i_midi_mapping_input_client import IMidiMappingInputClient
from input_controller.midi_mapping_input_dialog import MidiMappingInputDialog
from common import fl_helper

class KorgKaossPad3Plus_InputController(IMidiMappingInputClient):

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
        self.__is_save_mode = False
        self.__is_delete_mode = False
        self.__is_midi_mapping_save_mode = False
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
        self.__midi_loop_started = False
        self.__should_start_midi_loop = False
        self.__midi_mapping_input_dialog = None

    def onInitScript(self, event):

        if False == self.__initialized:

            print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.onInitScript.__name__)

            #try:
            for preset_page_id in self.__fx_preset_pages:
                self.__fx_preset_pages[preset_page_id].onInitScript()

            if False == self.__midi_loop_started and True == self.__should_start_midi_loop:
                old_event_data = event.data1
                event.data1 = constants.MIDI_CC_INTERNAL_LOOP
                device.repeatMidiEvent(event, 16, 16)
                event.data1 = old_event_data
                self.__midi_loop_started = True

            self.reset()
            self.__initialized = True

            #except Exception as e:
            #    print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.onInitScript.__name__ + ": failed to initialize the script.")
            #    print(e)

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
        return self.__is_save_mode
    
    def isDeleteMode(self):
        return self.__is_delete_mode

    def setSaveMode(self, save_mode):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.setSaveMode.__name__ + ": save mode - " + str(save_mode))
        self.__is_save_mode = save_mode
        self.__view.setSaveMode(save_mode)

        if True == save_mode and True == self.isDeleteMode():
            self.setDeleteMode(False)

    def setDeleteMode(self, delete_mode):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.setDeleteMode.__name__ + ": save mode - " + str(delete_mode))
        self.__is_delete_mode = delete_mode
        self.__view.setDeleteMode(delete_mode)
        
        if True == delete_mode and True == self.isSaveMode():
            self.setSaveMode(False)

    def isMidiMappingSaveMode(self):
        return self.__is_midi_mapping_save_mode

    def setMidiMappingSaveMode(self, midi_mapping_save_mode):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.setMidiMappingSaveMode.__name__ + ": midi mapping save mode - " + str(midi_mapping_save_mode))
        
        if True == midi_mapping_save_mode:
            self.__midi_mapping_input_dialog = MidiMappingInputDialog(self.__context.fx1_channel, self)
            self.__fx_preset_pages[self.__selected_fx_preset_page].setActiveFXUnit(FXUnit.FX_UNIT_CUSTOM)
        else:
            self.__midi_mapping_input_dialog = None
        
        self.__is_midi_mapping_save_mode = midi_mapping_save_mode
        self.__view.setMidiMappingSaveMode(midi_mapping_save_mode)

    def selectFXPage(self, preset_fx_page_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.selectFXPage.__name__ + ": fx page id - " + str(preset_fx_page_id))
        self.__selected_fx_preset_page = preset_fx_page_id;
        self.__fx_preset_pages[self.__selected_fx_preset_page].select(not self.isSaveMode())
        
        self.setFXLevel(self.__fx_level, True)

    def setShiftPressedState(self, shift_pressed):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.setShiftPressedState.__name__ + ": shift pressed - " + str(shift_pressed))
        self.__view.setShiftPressedState(shift_pressed)
        self.__shift_pressed = shift_pressed

        if(True == shift_pressed):
            self.actionOnDoubleClick(constants.MIDI_CC_SHIFT, self.randomizeTurnado)

    def randomizeTurnado(self):
        print(self.__context.device_name + ': ' + self.randomizeTurnado.__name__)
        plugins.setParamValue(0.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__context.fx2_channel, constants.TURNADO_SLOT_INDEX)
        plugins.setParamValue(1.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__context.fx2_channel, constants.TURNADO_SLOT_INDEX)
        plugins.setParamValue(0.0, constants.TURNADO_RANDOMIZE_PARAM_INDEX, self.__context.fx2_channel, constants.TURNADO_SLOT_INDEX)
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

    def resetFXPreset(self, fx_preset_id):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.resetFXPreset.__name__)
        self.__fx_preset_pages[self.__selected_fx_preset_page].resetFXPreset(fx_preset_id)

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
        plugins.setParamValue(self.__turnado_dry_wet_level, constants.TURNADO_DRY_WET_PARAM_INDEX, self.__context.fx2_channel, constants.TURNADO_SLOT_INDEX)

        if turnado_dry_wet_level == 0.0:
            self.__turnado_is_off = True
        else:
            self.__turnado_is_off = False

        self.__view.setTurnadoDryWetLevel(turnado_dry_wet_level)
        self.__view.turnadoOff(turnado_dry_wet_level == 0.0)

    def setTurnadoDictatorLevel(self, turnado_dictator_level):
        self.__turnado_dictator_level = turnado_dictator_level
        plugins.setParamValue(self.__turnado_dictator_level, constants.TURNADO_DICTATOR_PARAM_INDEX, self.__context.fx2_channel, constants.TURNADO_SLOT_INDEX)

        self.__view.setTurnadoDictatorLevel(turnado_dictator_level)

    def switchToNextTurnadoPreset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.switchToNextTurnadoPreset.__name__)
        plugins.nextPreset(self.__context.fx2_channel, constants.TURNADO_SLOT_INDEX)
        self.__restoreParams()

        self.__view.switchToNextTurnadoPreset()

    def switchToPrevTurnadoPreset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.switchToPrevTurnadoPreset.__name__)
        plugins.prevPreset(self.__context.fx2_channel, constants.TURNADO_SLOT_INDEX)
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

        plugins.setParamValue(val, constants.TURNADO_DRY_WET_PARAM_INDEX, self.__context.fx2_channel, constants.TURNADO_SLOT_INDEX)

        self.__view.turnadoOff(val == 0.0)
        self.__view.setTurnadoDryWetLevel(val)

    def __restoreParams(self):
        plugins.setParamValue(self.__turnado_dictator_level, constants.TURNADO_DICTATOR_PARAM_INDEX, self.__context.fx2_channel, constants.TURNADO_SLOT_INDEX)
        plugins.setParamValue(self.__turnado_dry_wet_level, constants.TURNADO_DRY_WET_PARAM_INDEX, self.__context.fx2_channel, constants.TURNADO_SLOT_INDEX)

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
            plugins.prevPreset(self.__context.fx1_channel, constants.MANIPULATOR_SLOT_INDEX)
        elif active_fx_unit == FXUnit.FX_UNIT_FINISHER_VOODOO:
            currentProgram = fl_helper.externalParamMapping(plugins.getParamValue(constants.FINISHER_VOODOO_MODE_PARAM_INDEX, self.__context.fx1_channel, constants.FINISHER_VOODOO_SLOT_INDEX)) * constants.FINISHER_VOODOO_MODE_NUMBER

            targetProgram = currentProgram - 1

            if targetProgram < -0.5:
                targetProgram = constants.FINISHER_VOODOO_MODE_NUMBER

            print("targetProgram - " + str(targetProgram))

            plugins.setParamValue(targetProgram / constants.FINISHER_VOODOO_MODE_NUMBER, constants.FINISHER_VOODOO_MODE_PARAM_INDEX, self.__context.fx1_channel, constants.FINISHER_VOODOO_SLOT_INDEX)

        self.__view.switchActiveFXUnitToPrevPreset()

        self.__fx_preset_pages[self.__selected_fx_preset_page].view_updateFXParamsFromPlugins()

    def switchActiveFXUnitToNextPreset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.switchActiveFXUnitToNextPreset.__name__)

        active_fx_unit = self.__fx_preset_pages[self.__selected_fx_preset_page].getActiveFXUnit()

        if active_fx_unit == FXUnit.FX_UNIT_MANIPULATOR:
            plugins.nextPreset(self.__context.fx1_channel, constants.MANIPULATOR_SLOT_INDEX)
        elif active_fx_unit == FXUnit.FX_UNIT_FINISHER_VOODOO:
            currentProgram = fl_helper.externalParamMapping(plugins.getParamValue(constants.FINISHER_VOODOO_MODE_PARAM_INDEX, self.__context.fx1_channel, constants.FINISHER_VOODOO_SLOT_INDEX)) * constants.FINISHER_VOODOO_MODE_NUMBER

            targetProgram = currentProgram + 1

            if targetProgram > constants.FINISHER_VOODOO_MODE_NUMBER + 0.5:
                targetProgram = 0

            print("targetProgram - " + str(targetProgram))

            plugins.setParamValue(targetProgram / constants.FINISHER_VOODOO_MODE_NUMBER, constants.FINISHER_VOODOO_MODE_PARAM_INDEX, self.__context.fx1_channel, constants.FINISHER_VOODOO_SLOT_INDEX)

        self.__view.switchActiveFXUnitToNextPreset()

        self.__fx_preset_pages[self.__selected_fx_preset_page].view_updateFXParamsFromPlugins()

    def reset(self):
        print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.reset.__name__)

        self.__selected_fx_preset_page = FXPresetPage.FXPresetPage_1
        self.selectFXPage(self.__selected_fx_preset_page)
        self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_1)

        self.__is_save_mode = False
        self.__view.setSaveMode(self.__is_save_mode)
        
        self.__is_delete_mode = False
        self.__view.setDeleteMode(self.__is_delete_mode)

        self.setTurnadoDictatorLevel(0.0)
        self.setTurnadoDryWetLevel(constants.DEFAULT_TURNADO_DRY_WET_LEVEL)

        self.setFXLevel(1.0, True)
        self.setVolume(fl_helper.MAX_VOLUME_LEVEL_VALUE)

    def midi_loop(self):
        #print(self.__context.device_name + ': ' + KorgKaossPad3Plus_InputController.midi_loop.__name__)
        pass

    def MidiMappingInputDone(self, fx_parameter_number, midi_mapping):
        self.__fx_preset_pages[self.__selected_fx_preset_page].setMidiMapping(fx_parameter_number, midi_mapping)
        self.setMidiMappingSaveMode(False)
    
    def MidiMappingInputCancelled(self):
        self.setMidiMappingSaveMode(False)

    def OnMidiMsg(self, event):

        #fl_helper.printAllPluginParameters(self.__context.fx1_channel, constants.MANIPULATOR_SLOT_INDEX)

        event.handled = False

        self.onInitScript(event)
        
        if True == self.__midi_loop_started and constants.MIDI_CC_INTERNAL_LOOP == event.data1:
            self.midi_loop()
        else:
            if True == self.isMidiMappingSaveMode():
                if event.data1 == constants.MIDI_CC_ENTER_SAVE_MODE and self.getShiftPressedState():
                    action = lambda self = self: ( self.setMidiMappingSaveMode(not self.isMidiMappingSaveMode()), \
                                                   self.setSaveMode(False), \
                                                   self.setDeleteMode(False) )
                    self.actionOnDoubleClick(constants.MIDI_CC_ENTER_SAVE_MODE + constants.ENTER_MIDI_MAPPING_SAVE_MODE_SHIFT, action)
                elif event.data1 == constants.MIDI_CC_SHIFT:
                    self.setShiftPressedState(event.data2 == fl_helper.MIDI_MAX_VALUE)
                else:
                    if self.__midi_mapping_input_dialog:
                        self.__midi_mapping_input_dialog.OnMidiMsg(event)
            else:
                if event.data1 == constants.MIDI_CC_EFFECTS_PAGE_1 and self.getShiftPressedState():
                    self.selectFXPage(FXPresetPage.FXPresetPage_1)
                elif event.data1 == constants.MIDI_CC_EFFECTS_PAGE_2 and self.getShiftPressedState():
                    self.selectFXPage(FXPresetPage.FXPresetPage_2)
                elif event.data1 == constants.MIDI_CC_EFFECTS_PAGE_3 and self.getShiftPressedState():
                    self.selectFXPage(FXPresetPage.FXPresetPage_3)
                elif event.data1 == constants.MIDI_CC_EFFECTS_PAGE_4 and self.getShiftPressedState():
                    self.selectFXPage(FXPresetPage.FXPresetPage_4)
                elif event.data1 == constants.MIDI_CC_SHIFT:
                    self.setShiftPressedState(event.data2 == fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_ENTER_SAVE_MODE and self.getShiftPressedState():
                    self.setSaveMode(not self.isSaveMode())

                    action = lambda self = self: ( self.setMidiMappingSaveMode(not self.isMidiMappingSaveMode()), \
                                                   self.setSaveMode(False) )
                    self.actionOnDoubleClick(constants.MIDI_CC_ENTER_SAVE_MODE + constants.ENTER_MIDI_MAPPING_SAVE_MODE_SHIFT, action)
                elif event.data1 == constants.MIDI_CC_ENTER_DELETE_MODE and self.getShiftPressedState():
                    self.setDeleteMode(not self.isDeleteMode())
                elif event.data1 == constants.MIDI_CC_PREV_ACTIVE_FX_UNIT_PRESET and self.getShiftPressedState():
                    self.switchActiveFXUnitToPrevPreset()
                elif event.data1 == constants.MIDI_CC_NEXT_ACTIVE_FX_UNIT_PRESET and self.getShiftPressedState():
                    self.switchActiveFXUnitToNextPreset()
                elif event.data1 == constants.MIDI_CC_EFFECT_1 and self.isDeleteMode():
                    self.resetFXPreset(FXPreset.FXPreset_1)
                    self.setDeleteMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_1)
                elif event.data1 == constants.MIDI_CC_EFFECT_2 and self.isDeleteMode():
                    self.resetFXPreset(FXPreset.FXPreset_2)
                    self.setDeleteMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_2)
                elif event.data1 == constants.MIDI_CC_EFFECT_3 and self.isDeleteMode():
                    self.resetFXPreset(FXPreset.FXPreset_3)
                    self.setDeleteMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_3)
                elif event.data1 == constants.MIDI_CC_EFFECT_4 and self.isDeleteMode():
                    self.resetFXPreset(FXPreset.FXPreset_4)
                    self.setDeleteMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_4)
                elif event.data1 == constants.MIDI_CC_EFFECT_5 and self.isDeleteMode():
                    self.resetFXPreset(FXPreset.FXPreset_5)
                    self.setDeleteMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_5)
                elif event.data1 == constants.MIDI_CC_EFFECT_6 and self.isDeleteMode():
                    self.resetFXPreset(FXPreset.FXPreset_6)
                    self.setDeleteMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_6)
                elif event.data1 == constants.MIDI_CC_EFFECT_7 and self.isDeleteMode():
                    self.resetFXPreset(FXPreset.FXPreset_7)
                    self.setDeleteMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_7)
                elif event.data1 == constants.MIDI_CC_EFFECT_8 and self.isDeleteMode():
                    self.resetFXPreset(FXPreset.FXPreset_8)
                    self.setDeleteMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_8)
                elif event.data1 == constants.MIDI_CC_EFFECT_1 and self.isSaveMode():
                    self.updateFXPreset(FXPreset.FXPreset_1)
                    self.setSaveMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_1)
                elif event.data1 == constants.MIDI_CC_EFFECT_2 and self.isSaveMode():
                    self.updateFXPreset(FXPreset.FXPreset_2)
                    self.setSaveMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_2)
                elif event.data1 == constants.MIDI_CC_EFFECT_3 and self.isSaveMode():
                    self.updateFXPreset(FXPreset.FXPreset_3)
                    self.setSaveMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_3)
                elif event.data1 == constants.MIDI_CC_EFFECT_4 and self.isSaveMode():
                    self.updateFXPreset(FXPreset.FXPreset_4)
                    self.setSaveMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_4)
                elif event.data1 == constants.MIDI_CC_EFFECT_5 and self.isSaveMode():
                    self.updateFXPreset(FXPreset.FXPreset_5)
                    self.setSaveMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_5)
                elif event.data1 == constants.MIDI_CC_EFFECT_6 and self.isSaveMode():
                    self.updateFXPreset(FXPreset.FXPreset_6)
                    self.setSaveMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_6)
                elif event.data1 == constants.MIDI_CC_EFFECT_7 and self.isSaveMode():
                    self.updateFXPreset(FXPreset.FXPreset_7)
                    self.setSaveMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_7)
                elif event.data1 == constants.MIDI_CC_EFFECT_8 and self.isSaveMode():
                    self.updateFXPreset(FXPreset.FXPreset_8)
                    self.setSaveMode(False)
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_8)
                elif event.data1 == constants.MIDI_CC_EFFECT_1 and not self.getShiftPressedState():
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_1)
                elif event.data1 == constants.MIDI_CC_EFFECT_2 and not self.getShiftPressedState():
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_2)
                elif event.data1 == constants.MIDI_CC_EFFECT_3 and not self.getShiftPressedState():
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_3)
                elif event.data1 == constants.MIDI_CC_EFFECT_4 and not self.getShiftPressedState():
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_4)
                elif event.data1 == constants.MIDI_CC_EFFECT_5 and not self.getShiftPressedState():
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_5)
                elif event.data1 == constants.MIDI_CC_EFFECT_6 and not self.getShiftPressedState():
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_6)
                elif event.data1 == constants.MIDI_CC_EFFECT_7 and not self.getShiftPressedState():
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_7)
                elif event.data1 == constants.MIDI_CC_EFFECT_8 and not self.getShiftPressedState():
                    self.selectFXPresetOnTheVisiblePage(FXPreset.FXPreset_8)
                elif event.data1 == constants.MIDI_CC_FX_LEVEL and self.getShiftPressedState():
                    self.setFXLevel(event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_TURNADO_DRY_WET and self.getShiftPressedState():
                    self.setTurnadoDryWetLevel(event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_TURNADO_DICTATOR:
                    self.setTurnadoDictatorLevel(event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_1:
                    self.setFXParameterLevel(FXParameter.FXParameter_1, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_2:
                    self.setFXParameterLevel(FXParameter.FXParameter_2, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_3:
                    self.setFXParameterLevel(FXParameter.FXParameter_3, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_4:
                    self.setFXParameterLevel(FXParameter.FXParameter_4, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_5:
                    self.setFXParameterLevel(FXParameter.FXParameter_5, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_6:
                    self.setFXParameterLevel(FXParameter.FXParameter_6, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_7:
                    self.setFXParameterLevel(FXParameter.FXParameter_7, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_EFFECT_PARAM_8:
                    self.setFXParameterLevel(FXParameter.FXParameter_8, event.data2 / fl_helper.MIDI_MAX_VALUE)
                elif event.data1 == constants.MIDI_CC_SYNTH_VOLUME:
                    self.setVolume((event.data2 / fl_helper.MIDI_MAX_VALUE) * fl_helper.MAX_VOLUME_LEVEL_VALUE)
                elif event.data1 == constants.MIDI_CC_TURNADO_NEXT_PRESET and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                    self.switchToNextTurnadoPreset()
                elif event.data1 == constants.MIDI_CC_TURNADO_PREV_PRESET and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                    self.switchToPrevTurnadoPreset()
                elif event.data1 == constants.MIDI_CC_TURNADO_ON_OFF and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                    self.turnadoOnOff()
                elif event.data1 == constants.MIDI_CC_CHANGE_ACTIVE_FX_UNIT and not self.getShiftPressedState() and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                    self.changeActiveFXUnit()
                elif event.data1 == constants.MIDI_CC_CHANGE_ACTIVE_FX_UNIT and self.getShiftPressedState() and event.data2 == constants.KP3_PLUS_ABCD_PRESSED:
                    self.reset()

        event.handled = True
