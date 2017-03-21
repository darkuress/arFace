#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright (c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

import maya.cmds as cmds

from ..Misc import Core
reload(Core)

class Create(Core.Core):
    def __init__(self, **kw):
        """
        initializing variables
        """
        #initializing Global variables
        Core.Core.__init__(self, **kw)
        self.locData = kw.get('locData')
        
    def importHelpPanel(self):
        """
        importing the halp panel
        """
        if not cmds.objExists(self.panelTopNode):
            cmds.file(self.panelPath,
                      i = True,
                      type = 'mayaAscii',
                      mergeNamespacesOnClash = False,
                      rpr = 'panel',
                      options = "v=0",
                      pr = True)
        
        return self.panelTopNode
    
    def importLocators(self):
        """
        importing the halp panel
        """
        print '......', self.faceLocPath
        if not cmds.objExists(self.faceLocTopNode):
            cmds.file(self.faceLocPath,
                      i = True,
                      type = 'mayaAscii',
                      mergeNamespacesOnClash = False,
                      rpr = 'faceLoc',
                      options = "v=0",
                      pr = True)
        
        return self.faceLocPath
    
    def placeLocators(self):
        """
        place the locators by the value in json file
        """
        if self.locData.get('setupLoc'):
            cmds.xform('allPos', t = self.locData['setupLoc']['allPos'], ws = True)
            
            for loc in self.locData['setupLoc'].keys():
                if not loc == 'allPos':
                    print loc + '.......',  self.locData['setupLoc'][loc]
                    cmds.xform(loc, t = self.locData['setupLoc'][loc], ws = True)