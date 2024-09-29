'''
Created on Sep 28, 2024

@author: Dream Machines
'''

import time

class UpdateableMux:
    def __init__(self):
        self.__updateables = set()

    def add_updateable(self,  updateable):
        self.__updateables.add(updateable)

    def remove_updateable(self, updateable):
        self.__updateables.discard(updateable)

    def update(self):
        time_val = time.time()
        for updateable in self.__updateables:
            updateable.update(time_val)

class Updateable:
    def update(self, update_time):
        pass

class DoubleClickTimeoutHandler(Updateable):
    STATE_INITITAL = 0
    STATE_FIRST_CLICK_DONE      = 1
    STATE_FIRST_CLICK_RELEASED  = 2
    STATE_SECOND_CLICK_DONE     = 3
    def __init__(self,
                 action_first_click,
                 action_first_click_released,
                 action_double_click,
                 action_double_click_released,
                 action_timeout,
                 double_click_timeout):
        self.__action_first_click = action_first_click
        self.__action_first_click_released = action_first_click_released
        self.__action_double_click = action_double_click
        self.__action_double_click_released = action_double_click_released
        self.__double_click_timeout = double_click_timeout
        self.__action_timeout = action_timeout
        self.__first_click_time = 0.0
        self.__state = DoubleClickTimeoutHandler.STATE_INITITAL

    def click(self):
        if self.__state == DoubleClickTimeoutHandler.STATE_INITITAL:
            self.__action_first_click()
            self.__state = DoubleClickTimeoutHandler.STATE_FIRST_CLICK_DONE
        elif self.__state == DoubleClickTimeoutHandler.STATE_FIRST_CLICK_RELEASED:
            if time.time() - self.__first_click_time < self.__double_click_timeout:
                self.__action_double_click()
                self.__state = DoubleClickTimeoutHandler.STATE_SECOND_CLICK_DONE
            else:
                self.__first_click_time = 0.0
                self.__state = DoubleClickTimeoutHandler.STATE_INITITAL
                
    def release(self):
        if self.__state == DoubleClickTimeoutHandler.STATE_FIRST_CLICK_DONE:
            self.__action_first_click_released()
            self.__state = DoubleClickTimeoutHandler.STATE_FIRST_CLICK_RELEASED
            self.__first_click_time = time.time()
        elif self.__state == DoubleClickTimeoutHandler.STATE_SECOND_CLICK_DONE:
            self.__first_click_time = 0.0
            self.__action_timeout()
            self.__state = DoubleClickTimeoutHandler.STATE_INITITAL

    def update(self, update_time):
        if self.__state == DoubleClickTimeoutHandler.STATE_FIRST_CLICK_RELEASED and \
        update_time - self.__first_click_time >= self.__double_click_timeout:
            self.__first_click_time = 0.0
            self.__action_timeout()
            self.__state = DoubleClickTimeoutHandler.STATE_INITITAL

class DelayedActionHandler(Updateable):
    STATE_INITITAL = 0
    STATE_CLICK_DONE      = 1
    STATE_CLICK_RELEASED  = 2
    def __init__(self,
                 action_click,
                 action_click_released,
                 action_delayed,
                 delay):
        self.__action_click = action_click
        self.__action_click_released = action_click_released
        self.__action_delayed = action_delayed
        self.__delay = delay
        self.__click_time = 0.0
        self.__state = DelayedActionHandler.STATE_INITITAL

    def click(self):
        if self.__state == DelayedActionHandler.STATE_INITITAL:
            self.__action_click()
            self.__state = DelayedActionHandler.STATE_CLICK_DONE
            self.__click_time = time.time()
                
    def release(self):
        if self.__state == DelayedActionHandler.STATE_CLICK_DONE:
            self.__action_click_released()
            self.__state = DelayedActionHandler.STATE_CLICK_RELEASED

    def update(self, update_time):
        if self.__state == DelayedActionHandler.STATE_CLICK_RELEASED and \
        update_time - self.__click_time >= self.__delay:
            self.__click_time = 0.0
            self.__action_delayed()
            self.__state = DelayedActionHandler.STATE_INITITAL