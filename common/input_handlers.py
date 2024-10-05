'''
Created on Sep 29, 2024

@author: Dream Machines
'''

class ClickReleaseHandler():
    STATE_INITITAL   = 0
    STATE_CLICK_DONE = 1
    def __init__(self,
                 action_click,
                 action_click_released):
        self.__action_click = action_click
        self.__action_click_released = action_click_released
        self.__state = ClickReleaseHandler.STATE_INITITAL

    def click(self):
        if self.__state == ClickReleaseHandler.STATE_INITITAL:
            self.__action_click()
            self.__state = ClickReleaseHandler.STATE_CLICK_DONE
                
    def release(self):
        if self.__state == ClickReleaseHandler.STATE_CLICK_DONE:
            self.__action_click_released()
            self.__state = ClickReleaseHandler.STATE_INITITAL
