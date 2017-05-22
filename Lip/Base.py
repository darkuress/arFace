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
        
        #- initializing Global variables
        Core.Core.__init__(self, **kw)
        Util.Util.__init__(self)
        Controller.Controller.__init__(self)

        if kw.get('locData'):
            self.locData = kw.get('locData')
            self.headGeo = self.locData['headGeo']		

        print '....', self.locData
        #- lip joints and location position
        self.lipEPos        = self.locData['setupLoc']['lipEPos']
        self.lipWPos        = [-self.lipEPos[0], self.lipEPos[1], self.lipEPos[2]]
        self.lipNPos        = self.locData['setupLoc']['lipNPos']
        self.lipSPos        = self.locData['setupLoc']['lipSPos']
        self.lipYPos        = self.locData['setupLoc']['lipYPos']
        self.jawRigPos      = self.locData['setupLoc']['jawRigPos']
        self.cheekPos       = self.locData['setupLoc']['cheekPos']
        self.squintPuffPos  = self.locData['setupLoc']['squintPuffPos']
        self.lowCheekPos    = self.locData['setupLoc']['lowCheekPos']
        
        self.cheekCrvGrp  = 'cheekCrv' + self.grpSuffix
        
        self.lipPCrvGrp = 'lipCrv' + self.grpSuffix