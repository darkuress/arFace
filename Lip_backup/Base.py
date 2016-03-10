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
from ..Misc import Util
reload(Util)
from ..Misc import Controller
reload(Controller)

class Base(Core.Core, Util.Util, Controller.Controller):
    def __init__(self, **kw):
        """
        initializing variables
        """
        
        #initializing Global variables
        #super(Core.Core, self, **kw).__init__()
        Core.Core.__init__(self, **kw)
        Util.Util.__init__(self)
        Controller.Controller.__init__(self)
        
        self.lipEPos   = self.locData['setupLoc']['lipEPos']
        self.lipNPos   = self.locData['setupLoc']['lipNPos']
        self.lipSPos   = self.locData['setupLoc']['lipSPos']
        self.lipYPos   = self.locData['setupLoc']['lipYPos']
        self.jawRigPos = self.locData['setupLoc']['jawRigPos']

        #self.lipEPos   = cmds.xform('lipEPos', t = True, q = True, ws = True) 
        #self.lipNPos   = cmds.xform('lipNPos', t = True, q = True, ws = True) 
        #self.lipSPos   = cmds.xform('lipSPos', t = True, q = True, ws = True) 
        #self.lipYPos   = cmds.xform('lipYPos', t = True, q = True, r = True) 
        #self.jawRigPos = cmds.xform('jawRigPos', t = True, q = True, ws = True) 

        #lip joints and location position 
        self.uplipVtxs    = eval(self.locData['upLipVtxs'])
        self.lolipVtxs    = eval(self.locData['loLipVtxs'])
        