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
        #self.lidJnt = 'lidJntP'
        #self.lEyeLoc = self.prefix[0] + 'EyePos'
        self.lEyeLoc      = 'lEyePos'
        self.lidJntPName  = 'LidP' + self.jntSuffix
        self.lidJntName   = 'Lid'
        self.lidJntTXName = 'LidTx' 
        self.blinkJntName = 'LidBlink'
        self.wideJntName  = 'Wide'
        self.scaleJntName = 'Scale'
        