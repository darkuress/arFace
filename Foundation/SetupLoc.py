import maya.cmds as cmds

from ..Misc import Core
reload(Core)

class SetupLoc(Core.Core):
    def __init__(self, **kw):
        """
        initializing variables
        """
        #initializing Global variables
        Core.Core.__init__(self, **kw)
    
    @classmethod
    def saveLocPos(cls, locs):
        """
        saves all the locators xyz position and return it as dictionary
        """
        locPos = {}
        for loc in eval(locs):
            if cmds.objExists(loc):
                locPos[loc] = cmds.xform(loc, t = True, q = True, ws = True)
            else:
                print 'locator "%s" does not exists, maybe import locators' %loc
        
        return locPos
    
    