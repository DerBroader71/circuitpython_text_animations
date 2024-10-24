Introduction
============

This is a CircuitPython library to perform different effects on text labels.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.

Usage Example
=============

```python

    from text_animations import TextAnimations
    animations = TextAnimations(display, terminalio.FONT, color=0xFFFFFF)

    # Create a text label
    #text_area = animations.create_text("Fading Text!", x=10, y=30)
    # Set up the fade effect
    #fade_update = animations.fade(text_area, steps=50, delay=0.05, repeat=True)

    # Create a text label
    text_area = animations.create_text("Glitching Text!", x=10, y=30)
    # Set up the glitch effect
    glitch_update = animations.glitch(text_area, steps=50, delay=0.25, pause_cycles=20)

    # Create a text label
    #text_area = animations.create_text("Matrix Effect!", x=10, y=30)
    # Set up the matrix effect
    #matrix_update = animations.matrix(text_area, delay=0.2)

    # Create a text label
    #text_area = animations.create_text("Destroying Text!", x=10, y=30)
    # Set up the destroy effect
    #destroy_update = animations.destroy(text_area, delay=0.1, pause_cycles=20)

    # Main loop
    while True:
        #fade_update() 		# works perfectly
        glitch_update() 	# works perfectly
        #matrix_update() 	# works perfectly
        #destroy_update() 	# works perfectly

```

Uncomment / comment as appropriate

There are 4 effects so far:
* fade - this will fade the text in and out in a loop
* matrix - this will create a matrix rain effect to make the text appear and disappear in a loop
* glitch = this will glitch the text to make the text appear and disappear in a loop
* destroy - this will remove / add characters until the text appears and disappears in a loop
Contributing
============

Contributions are welcome! Please read our [Code of Conduct](https://github.com/adafruit/Adafruit_CircuitPython_example/blob/master/CODE_OF_CONDUCT.md) before contributing to help this project stay welcoming.
