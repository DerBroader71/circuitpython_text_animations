"""Module providing Function to generate UUID version 4."""
################################################################################
# The MIT License (MIT)
#
# Author: DerBroader71 (Tudor Davies)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
################################################################################
import time
import displayio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect

class Timer:
    def __init__(self, interval):
        self.interval = interval
        self.start_time = time.monotonic()

    def has_elapsed(self):
        """Check if the interval has elapsed."""
        return time.monotonic() - self.start_time >= self.interval

    def reset(self):
        """Reset the timer to start again."""
        self.start_time = time.monotonic()

class TextAnimations:
    def __init__(self, display, font, color=0xFFFFFF, background_color=None):
        self.display = display
        self.font = font
        self.color = color
        self.background_color = background_color
        self.group = displayio.Group()
        self.display.root_group = self.group
        
    def create_text(self, text, x, y):
        """Creates a label object and adds it to the display group"""
        text_area = label.Label(self.font, text=text, color=self.color, background_color=self.background_color)
        text_area.x = x
        text_area.y = y
        self.group.append(text_area)
        return text_area

    def fade(self, text_area, steps=50, delay=0.05, repeat=True):
        """Smooth fade-out and fade-in effect for text, alternating between full brightness and black."""
        step = 0
        direction = 1  # 1 for fading in, -1 for fading out
        timer = Timer(delay)

        # Extract the original color components (RGB)
        original_color = text_area.color
        orig_r = (original_color >> 16) & 0xFF
        orig_g = (original_color >> 8) & 0xFF
        orig_b = original_color & 0xFF

        def clamp(value, min_value=0, max_value=255):
            """Ensure that the RGB values remain in the valid range."""
            return max(min_value, min(value, max_value))

        def update_fade():
            nonlocal step, direction

            if timer.has_elapsed():
                # Calculate fade factor for smooth fading between 0 and 1
                fade_factor = step / steps

                # Calculate each RGB channel based on the fade factor
                r = clamp(int(orig_r * fade_factor))
                g = clamp(int(orig_g * fade_factor))
                b = clamp(int(orig_b * fade_factor))

                # Combine RGB into a single color value
                faded_color = (r << 16) | (g << 8) | b
                text_area.color = faded_color  # Apply the new color
                self.display.refresh()  # Refresh the display to show the updated color

                # Update step and direction for smooth transition
                step += direction
                if step >= steps:
                    # When fully bright, start fading out
                    direction = -1
                elif step <= 0:
                    # When fully dark, start fading in
                    direction = 1

                # Reset the timer for the next fade step
                timer.reset()

        return update_fade


    def glitch(self, text_area, steps=20, delay=0.1, pause_cycles=20):
        """Glitch effect with non-blocking time, glitch randomization, and a pause after restoring the text."""
        import random
        original_text = text_area.text
        step = 0
        max_glitch_rate = 0.3  # Adjust the rate at which characters are glitched
        timer = Timer(delay)
        pause_counter = 0  # Counter to handle pause phase

        def update_glitch():
            nonlocal step, max_glitch_rate, pause_counter

            if timer.has_elapsed():
                if step < steps:
                    # Glitch phase: Randomly glitch the text
                    glitched_text = ''.join(
                        random.choice([char, chr(random.randint(33, 126))]) for char in original_text
                    )
                    text_area.text = glitched_text
                    step += 1

                else:
                    # Pause phase: Display the original text
                    text_area.text = original_text

                    # Increment pause counter
                    pause_counter += 1

                    # If pause is done, reset to start glitching again
                    if pause_counter >= pause_cycles:
                        step = 0  # Reset glitch steps
                        pause_counter = 0  # Reset pause counter
                        max_glitch_rate = random.uniform(0.2, 0.4)  # Re-randomize glitch intensity

                self.display.refresh()
                timer.reset()  # Reset the timer for the next update

        return update_glitch


    def matrix(self, text_area, delay=0.1):
        """Matrix effect where the original text is slowly generated, erased, and repeated."""
        import random
        original_text = text_area.text
        current_text = [' '] * len(original_text)  # Start with an empty text (spaces)
        columns = len(original_text)
        building = True  # True when building the text, False when erasing
        timer = Timer(delay)

        def random_character():
            """Generate a random character (e.g., numbers, symbols, or letters)."""
            return chr(random.randint(33, 126))  # ASCII characters between 33 and 126

        def update_matrix():
            nonlocal building, current_text

            if timer.has_elapsed():
                if building:
                    # Build phase: gradually reveal the text
                    if current_text != list(original_text):
                        # Pick a random empty or random character to replace with the correct one
                        random_indices = [i for i, char in enumerate(current_text) if char != original_text[i]]
                        add_index = random.choice(random_indices)

                        # Transition from random to the correct character
                        if random.random() > 0.2:
                            current_text[add_index] = random_character()
                        else:
                            current_text[add_index] = original_text[add_index]

                        text_area.text = ''.join(current_text)
                    else:
                        # If the text is fully revealed, switch to destroy phase
                        building = False

                else:
                    # Destroy phase: gradually hide the text
                    if any(char != ' ' for char in current_text):
                        non_empty_indices = [i for i, char in enumerate(current_text) if char != ' ']
                        remove_index = random.choice(non_empty_indices)

                        # Randomly either erase the character or show a random one
                        if random.random() > 0.2:
                            current_text[remove_index] = random_character()
                        else:
                            current_text[remove_index] = ' '

                        text_area.text = ''.join(current_text)
                    else:
                        # If the text is fully erased, switch to build phase
                        building = True

                self.display.refresh()
                timer.reset()  # Reset the timer for the next update

        return update_matrix



    def destroy(self, text_area, delay=0.1, pause_cycles=20):
        """Destroy effect where one random character is removed at a time and then rebuilt with a pause."""
        import random
        original_text = text_area.text
        current_text = list(original_text)  # Start with the full text in a list (modifiable)
        removed_chars = []  # To store the removed characters during destroy
        timer = Timer(delay)
        is_destroying = True  # Flag to switch between destroy and rebuild modes
        pause_counter = 0  # Counter to handle the pause before destruction starts

        def update_destroy():
            nonlocal is_destroying, current_text, removed_chars, pause_counter

            if timer.has_elapsed():
                if is_destroying:
                    # Destroy phase: Randomly remove one character
                    if len(current_text) > 0:
                        remove_index = random.randint(0, len(current_text) - 1)
                        # Remove the character and store it for the rebuild phase
                        removed_chars.append((remove_index, current_text[remove_index]))
                        del current_text[remove_index]
                        text_area.text = ''.join(current_text)
                    else:
                        # If all characters are removed, switch to rebuild mode
                        is_destroying = False

                else:
                    # Rebuild phase: Randomly add one character back in the correct place
                    if len(removed_chars) > 0:
                        add_index, char = removed_chars.pop(random.randint(0, len(removed_chars) - 1))
                        current_text.insert(add_index, char)
                        text_area.text = ''.join(current_text)
                    else:
                        # If the text is fully rebuilt, show the original text and start the pause
                        text_area.text = original_text  # Ensure the original text is shown during the pause
                        pause_counter += 1
                        if pause_counter >= pause_cycles:
                            # After the pause, reset to start destruction again
                            is_destroying = True
                            current_text = list(original_text)  # Reset the text to full
                            removed_chars = []  # Clear the removed characters
                            pause_counter = 0  # Reset pause counter

                self.display.refresh()
                timer.reset()  # Reset the timer for the next update

        return update_destroy

 
