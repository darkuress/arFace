#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright (c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

import maya.cmds as cmds
import Func
reload(Func)

class Ctrls(Func.Func):
    def __init__(self, upDown, rotateScale, **kw):
        """
        initializing variables
        """
        self.upDown           = upDown
        self.rotateScale      = rotateScale
        
        #- local variables
        Func.Func.__init__(self, **kw)
    
    def createLipCtrls(self):
        self.lipCrvToJoint(self.upDown, self.rotateScale)