#!/usr/bin/env python3

import pyglet
from railroad.app import App
from railroad.modes import AddTrackMode

app = App()
app.change_mode(AddTrackMode)
pyglet.app.run()

