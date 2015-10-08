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
Param("axiom", [[0,0],[1,0],[0,-2],[0,-3]], "Initial Vertices with which the program starts", "List of 2D-Coordinates"),
Param("minor_road_delay",80, "How many iterations a seed waits until minor roads start growing from it", "integer"),
Param("mindestabstand",0.6, "Minimal distance a suggested Vertex has to be away from all existing vertices", "float"),
Param("rule_image_name","nicebild.png", "Name of image in /inputs/rule_pictures to be used to decide which rules will be used", "filename-String"),
Param("density_image_name", "abnehmend.png", "Name of image in /inputs/density_pictures to be used to determine population density", "filename-String"),
Param("heightmap_name", "randommap.png", "Name of image in /inputs/heightmaps/ to be used to determine elevation in 3D-Model", "filename-String"),
Param("bildaufloesung",10, "TODO", "integer"),
Param("border", [15,15], "Maximum x and y value for any Vertex", "List or tuple of 2 integers"),
Param("plot",0,"If 1, the program will show the Growth of the roadmap during runtime", "1 or 0"),
Param("plot_counter",2, "How many iterations have to pass before the plot showing growth of roadmap updates itself", "integer"),
Param("savefig",1, "If 1, the program will save an image showing the roadmap to /outputs/", "1 or 0"),
Param("pSeed",40, "Probability that a minor road starts growing from a major road", "integer between 0 and 100"),
Param("seedlMin",1.0, "Minimum length of a seed-road", "float"),
Param("seedlMax",1.0, "Maximum length of a seed-road", "float"),
Param("minor_roadpForward",5, "Probability that a minor road will continue straight in the next iteration", "integer between 0 and 100"),
Param("minor_roadpTurn",85, "Probability that a minor road will turn in the next iteration", "integer between 0 and 100"),
Param("minor_roadlMin",1.0, "Minimum length of a minor road", "float"),
Param("minor_roadlMax", 1.0, "Maxium length of a minor road", "float"),
Param("organicpForward",100, "Probability that an organic road will continue straight in the next iteration", "integer between 0 and 100"),
Param("organicpTurn",7, "Probability that an organic road will turn in the next iteration", "integer between 0 and 100"),
Param("organiclMin",0.8, "Minimum length of an organic road", "float"),
Param("organiclMax", 1.6, "Maxium length of an organic road", "float"),
Param("gridpForward",100, "Probability that a grid road will continue straight in the next iteration", "integer between 0 and 100"),
Param("gridpTurn",9, "Probability that a grid road will turn in the next iteration", "integer between 0 and 100"),
Param("gridlMin",1.0, "Minimum length of a grid road", "float"),
Param("gridlMax", 1.0, "Maxium length of a grid road", "float"),
Param("radialpForward",100, "Probability that a radial road will continue straight in the next iteration", "integer between 0 and 100"),
Param("radialpTurn",7, "Probability that a radial road will turn in the next iteration", "integer between 0 and 100"),
Param("radiallMin",0.8, "Minimum length of a radial road", "float"),
Param("radiallMax", 1.6, "Maxium length of a radial road", "float"),
Param("heightDif", 2, "Difference between the highest and the lowest point if a previously unknown heightmap is used", "float")]
