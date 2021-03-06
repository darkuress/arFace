#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright (c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

import maya.cmds as cmds

from arFace.Misc import Core 
reload(Core)
from arFace.Misc import Util
reload(Util)
from arFace.Misc import Controller
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
        
        #initializing local variables
        self.jntName          = 'brow0'
        self.browBase         = 'browBase'
        self.browRotY         = 'browRotY'
        self.browP            = 'browP'
        self.baseCntJntName   = self.cPrefix + self.browBase
        self.browRotYJntName  = self.cPrefix + self.browRotY
        self.parentCntJntName = self.cPrefix + 'browP'
        self.ljntName         = self.prefix[0] + self.jntName
        self.baseJntName      = self.prefix[0] + self.browBase
        self.parentJntName    = self.prefix[0] + self.browP
        self.browRotYJntName  = self.prefix[0] + self.browRotY
        self.browCtlCrvName   = 'browCtrl' + self.crvSuffix

        self.eyebrowJntGrpName = 'eyebrowJnt' + self.grpSuffix
        self.eyebrowCtlGrpName = 'eyebrowCtl' + self.grpSuffix
        self.eyebrowCrvGrpName = 'eyebrowCrv' + self.grpSuffix
        
        #self.eyeBrowVtxs      = self.locData['eyebrowVtxs']
        
        if kw.get('locData'):
            self.locData = kw.get('locData')
		
        #new
        self.browRotXCrv      = [x for x in self.locData['setupLoc'] if 'rotXPivot' in x][0]
        self.browRotYCrv      = [x for x in self.locData['setupLoc'] if 'rotYPivot' in x][0]
        
        self.browCrvGrp       = 'browCrv' + self.grpSuffix
        self.attachCtlGrp     = 'attachCtl' + self.grpSuffix
        self.browCtlGrp       = 'browCtl' + self.grpSuffix
        self.bodyHeadTRS      = 'faceMain|spn|headSkel|bodyHeadTRSP|bodyHeadTRS|'
        
        self.browMapGeo       = "browMapSurf"
        self.headSkelJnt      = "headSkel" + self.jntSuffix
