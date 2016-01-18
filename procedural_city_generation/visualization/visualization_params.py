"""
Module which contains all input parameters for this submodule, along with:
- The default (recommmended) value from the developers
- A short description of what the parameter changes
- All values that the parameter accepts without causing this program to break.

This information can also be viewed when calling the GUI and clicking the "options"
button for that specific module.

"""
from procedural_city_generation.additional_stuff.Param import Param
params=[
Param("offset", 0.03, 0.03, "Offset", "float"),
]
