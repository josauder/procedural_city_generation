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
Param("minor_factor", 0.08, "Width of minor roads", "Float"),
Param("main_factor", 0.17, "Width of main roads", "Float"),
Param("max_area", 12, "Number of road segments after which a lot is considered too big for a building to be built on it", "Float"),
Param("split_poly_min_area", 0.3, "TODO", "Float"),
Param("split_poly_min_length", 0.2, "TODO", "Float"),
Param("split_poly_half_tolerance", 0.05, "TODO", "Float"),
Param("plotbool",False,"Decides if stuff should be plotted","boolean")
]
