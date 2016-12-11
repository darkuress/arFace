#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright (c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

import maya.cmds as cmds
import Joints
reload(Joints)
import Ctrls
reload(Ctrls)

class Setup(Joints.Joints, Ctrls.Ctrls):
    def __init__(self,
                 upDown = 'up',
                 rotateScale = 10,
                 **kw):
        """
        initializing variables
        """
        Joints.Joints.__init__(self, **kw)
        Ctrls.Ctrls.__init__(self, upDown, rotateScale, **kw)
        self.upDown = upDown
        self.locData = kw.get('locData')
        
    def createJoints(self):
        """
        creating joints on selected vertaxes
        """
        lipInfo = self.createJnts(self.upDown, self.locData)
        #self.lipJntGrp = lipInfo['lipJntGrp']
        #self.lipCrvGrp = lipInfo['lipCrvGrp']
        
    def createCtrls(self):
        """
        create Controllers
        """
        cmds.select(cl = True)
        self.createLipCtrls()
    
    def prarendGrp(self):
        """
        parent things
        """
        self.group(self.lipJntGrp, 'lipJnt' + self.grpSuffix)
        self.group(self.lipCrvGrp, 'lipCrv' + self.grpSuffix)
        
        if not cmds.listRelatives('lipJnt' + self.grpSuffix, p = True):
            cmds.parent('lipJnt' + self.grpSuffix, self.jntGrp)
        if not cmds.listRelatives('lipCrv' + self.grpSuffix, p = True):
            cmds.parent('lipCrv' + self.grpSuffix, self.crvGrp)
        cmds.select(cl = True)
        