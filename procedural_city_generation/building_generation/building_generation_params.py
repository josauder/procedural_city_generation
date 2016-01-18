"""
Module which contains all input parameters for this sudmodule, along with:
- The default (recommmended) value from the developers
- A short description of what the parameter changes
- All values that the parameter accepts without causing this program to break.

This information can also be viewed when calling the GUI and clicking the "options"
button for that specific module.

"""
from procedural_city_generation.additional_stuff.Param import Param
params=[Param("house_height", 0.15, 0.15, "The buildingheight which determines whether a building is a house or an appartment/skyscraper", "float"),
Param("floorheight_min", 0.03, 0.03, "The minimum height of each floor of a building", "float"),
Param("floorheight_max", 0.04, 0.04, "The maximum height of each floor of a building", "float"),
Param("windowwidth_min", 0.013, 0.013, "The minimum width of a window", "float"),
Param("windowwidth_max", 0.025, 0.025, "The maximum width of a window", "float"),
Param("windowheight_min", 0.015, 0.015, "The minimum height of a window", "float"),
Param("windowheight_max_house", 0.027, 0.027, "The maximum height of a window for a house", "float"),
Param("windowheight_max_not_house", 0, 0, "The maximum height of a window for not-houses, if 0 then floorheight will be used", "float"),
Param("windowdist_min_house", 0.01, 0.01, "The mininum distance between two windows for a house", "float"),
Param("windowdist_min_not_house", 0, 0, "The minimum distance between two windows for not-houses", "float"),
Param("windowdist_max_house", 0.03, 0.03, "The maximum distance between two windows for a house", "float"),
Param("windowdist_max_not_house", 0.03, 0.03, "The maximum distance between two windows for not-houses", "float"),
Param("scalefactor_min_house", 0.4, 0.4, "The minimum size to which a house can be scaled down to", "float"),
Param("scalefactor_min_not_house", 0.7, 0.7, "The minimum size to which not-houses can be scaled down to", "float"),
Param("scalefactor_max_house", 0.7, 0.7, "The maximum size to which a house can be scaled down to", "float"),
Param("scalefactor_max_not_house", 0.95, 0.95, "The maximum size to which not-houses can be scaled down to", "float"),
Param("prob_ledge", 0.5, 0.5, "Probability that a houses' ledges will be scaled outwards", "float"),
Param("ledgefactor_min", 1.01, 1.01, "Minimum factor to be used when scaling ledges outwards", "float"),
Param("ledgefactor_max", 1.05, 1.05, "Maximum factor to be used when scaling ledges outwards", "float"),
Param("offset", 0.03, 0.03, "Distance from Floor-mesh in Blender. Advisable to use same value in visualization", "float"),
Param("diffuse_iterations", 72, 72, "How many iterations of diffuse will be called in Surface.py", "int"),
Param("diffuse_power", 1.8, 1.8, "To which power each value of the diffused image will be raised", "float"),
Param("roofheight_min", 0.03, 0.03, "Minimum height of roof", "float"),
Param("roofheight_max", 0.07, 0.07, "Maximum height of roof", "float")]
