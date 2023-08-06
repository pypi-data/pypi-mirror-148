import math
import time
import random
import numpy as np

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.remote.webelement import WebElement

class HL_Util:
    # (normal distribution)
    # Takes an element and returns coordinates somewhere in the element. If the element is not visable, it returns 0.
    def behavorial_element_coordinates(self, webdriver, element):
        x_relative = int(element.rect['x']) - webdriver.execute_script("return window.pageXOffset;")
        y_relative = int(element.rect['y']) - webdriver.execute_script("return window.pageYOffset;")
        viewport_width = webdriver.execute_script("return window.innerWidth")
        viewport_height = webdriver.execute_script("return window.innerHeight")
        counter = 0
        for i in range(100): # Try 10 random positions, as some positions are not in round buttons.
            x = x_relative + int(np.random.normal(int(element.rect['width']*0.5), int(element.rect['width']*0.2)))
            y = y_relative + int(np.random.normal(int(element.rect['height']*0.5), int(element.rect['height']*0.2)))
            coords_in_button = webdriver.execute_script(f"return document.elementFromPoint({x}, {y}) === arguments[0];", element)
            coords_in_descendant = webdriver.execute_script(f"""
                let el = document.elementFromPoint({x}, {y});
                return [...arguments[0].querySelectorAll('*')].includes(el);""", element)
            if x < 0 or y < 0 or x > viewport_width or y > viewport_height:
                coords_in_button = False # If the element is partly in the viewport, a part of the element is outside of it. In that case, try again. This is not the best solution (non-deterministic), it would be better to limit the sample space.
            if coords_in_button or coords_in_descendant:
                return (x, y)
        return None

    # Returns a number from a normal distribution that is larger or equal to parameter 'minimal'.
    # Due to the minimum value, the returned values will not form a normal distribution.
    # To minimize this effect, values that would have been smaller than the minimum are not drawn
    # again, but get added a random small value. The new number will never become larger as the mean.
    def std_positive(mean, std, minimal):
        sample = np.random.normal(mean, std)
        while sample < minimal:
            sample += random.random() * (mean - minimal)
        return sample

    # The function to replace the original Selenium function that does not support specifying the duration.
    def create_pointer_move(self, duration=50, x=None, y=None, origin=None):
        action = dict(type="pointerMove", duration=duration)
        action["x"] = x
        action["y"] = y
        if isinstance(origin, WebElement):
            action["origin"] = {"element-6066-11e4-a52e-4f735466cecf": origin.id}
        elif origin is not None:
            action["origin"] = origin

        self.add_action(action)

    # Replace a function in the original Selenium API to increase mouse movement speed.
    def increaseMousemovementSpeed():
        PointerInput.create_pointer_move = HL_Util.create_pointer_move

    
