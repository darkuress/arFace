#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright (c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

import maya.cmds as cmds
import os

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

        self.lrUplow = []
        for lr in self.prefix:
            self.lrUplow.append(lr + self.uplo[0])
            self.lrUplow.append(lr + self.uplo[1])
        
        #initializing local variables
        #self.lidJnt = 'lidJntP'
        #self.lEyeLoc = self.prefix[0] + 'EyePos'
        self.lidJntPName  = 'LidP' + self.jntSuffix
        self.lidJntName   = 'Lid'
        self.lidJntTXName = 'LidTx' 
        self.blinkJntName = 'LidBlink'
        self.wideJntName  = 'Wide'
        self.scaleJntName = 'Scale'
        
        self.eyelidJntGrpName  = 'eyelidJnt' + self.grpSuffix
        self.eyelidCtlGrpName  = 'eyelidCtl' + self.grpSuffix
        self.eyelidCrvGrpName  = 'eyelidCrv' + self.grpSuffix
        
        #eyelid joints and location position 
        self.upEyelidVtxs    = self.locData['upEyelidVtxs']
        self.loEyelidVtxs    = self.locData['loEyelidVtxs']
        self.lEyeLoc         = str([x for x in self.locData['setupLoc'] if 'eye' in x.lower()][0])
        
        self.eyelidCrvJsonLoc = os.path.join(self.jsonBasePath, 'eyelidCrvData.json')
    