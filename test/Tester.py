import importlib
import pkgutil
import os

def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages
    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """

    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        try:
            results[full_name] = importlib.import_module(full_name)
        except:
            pass
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results

def test_dependency(name,logger):
    try:
        __import__(name)
        logger.info(name+" imported fine")
        return True
    except ImportError:
        logger.error(name+" could not be imported!")
        return False

def main():
    import sys, os
    path=os.path.abspath(os.path.dirname(__file__))+"/.."
    sys.path.append(path)
    os.chdir(path)
    loggerpath=path+"/procedural_city_generation/outputs/test.log"
    logger = Logger(loggerpath)
    logger.info("Initiating Tests")
    logger.info("path= "+path)

    import os, sys
    """
    import test
    test_funcs=import_submodules(test).items()
    test_funcs=[x[0] for x in test_funcs if (not "test.Tester" in x[0] and x[0].endswith("Test"))]
    for test in test_funcs:
        module=importlib.import_module(test)
        getattr(module, "main")()
    """

    logger.info("Python Version:")
    logger.info("\t"+sys.version)
    logger.info("\t"+str(sys.version_info))
    logger.info("OS: "+sys.platform)
    logger.info("Current Git commmit: ")
    logger.log_git_commit()

    logger.info("Testing Dependencies")

    try:
        with open(path+"/requirements.txt","r") as f:
             [test_dependency(x.split("==")[0],logger) for x in f.readlines()]
    except IOError:
        logger.error("Could not locate requirements.txt at "+os.path.abspath(path))


    logger.info("Testing \"import procedural_city_generation\"")
    import procedural_city_generation
    logger.info("Testing \"import UI\"")
    import UI
    logger.info("Testing \"import GUI\"")
    import GUI
    logger.info("Testing roadmap creation")
    UI.roadmap()
    logger.info("Roadmap creation threw no exception")

    logger.info("Testing roadmap creation")
    UI.polygons()
    logger.info("Roadmap creation threw no exception")

    logger.info("Testing roadmap creation")
    UI.building_generation()
    logger.info("Roadmap creation threw no exception")


class Logger(object):
    def __init__(self, path):
        """
        Basic logger that logs to given path
        Parameters
        ----------
        path : String path to target log file

        Returns
        -------

        """
        self.path=path
        with open(self.path,"w") as clearfile:
            clearfile.write("")
    def info(self, text):
        self.log("INFO: "+text)
    def error(self, text):
        self.log("ERROR: "+text)
    def debug(self, text):
        self.log("DEBUG: "+text)
    def log(self,text):
        print(text)
        self.write(text)
    def log_git_commit(self):
        os.system("echo \"INFO: \" >> "+self.path)
        os.system("git rev-parse --verify HEAD >> "+self.path)
    def write(self, text):
        with open(self.path,"a") as f:
            f.write(text+"\n")
if __name__ == '__main__':
    main()
