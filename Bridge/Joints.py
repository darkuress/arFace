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

class Joints(Core.Core, Util.Util):
    def __init__(self):
        """
        initializing variables
        """
        Core.Core.__init__(self)
        Util.Util.__init__(self)
    
    def createJnts(self):    
        """
        create bridge joints
        """
        if cmds.objExists ('jawRig'):            
            jawSemi = cmds.group ( n = 'jawSemi', em =True, parent = 'jaw' ) 
            cmds.setAttr ( jawSemi + ".translate", 0,0,0 )
            jawClose = cmds.joint(n = 'jawClose' + self.jntSuffix, relative = True, p = [ 0, 0, 0] )        
            jotStable = cmds.group ( n = 'lipJotStable', em =True, parent = 'jaw' ) 
            lipJotP = cmds.group( n = 'lipJotP', em =True, parent = jotStable )
            
        else :
            print "create faceRig first!!!" 
        # create cheek joint - check the cheek/squintPush group and angle
        lEarP = cmds.group ( n = self.prefix[0] + 'earP', em =True, p = self.prefix[0] + "ear" + self.grpSuffix )
        cmds.xform (lEarP, relative = True, t = [ 0, 0, 0] )
        lEarJnt = cmds.joint(n = self.prefix[0] + 'ear' + self.jntSuffix, relative = True, p = [ 0, 0, 0] ) 
        rEarP = cmds.group ( n = self.prefix[1] + 'earP', em =True, p = self.prefix[1] + "ear" + self.grpSuffix )
        cmds.xform (rEarP, relative = True, t = [ 0, 0, 0]  )
        rEarJnt = cmds.joint(n = self.prefix[1] + 'ear' + self.jntSuffix, relative = True, p = [ 0, 0, 0] ) 
        
        noseP = cmds.group ( n = 'noseP', em =True, p = "noseRig" )
        cmds.xform (noseP, relative = True, t = [ 0, 0, 0] )
        noseJnt = cmds.joint(n = 'nose' + self.jntSuffix, relative = True, p = [ 0, 0, 0] ) 
        
        lCheekP = cmds.group ( n = self.prefix[0] + 'cheekP', em =True, p = self.prefix[0] + "cheek" + self.grpSuffix )
        cmds.xform (lCheekP, relative = True, t = [ 0, 0, 0] )
        lCheekJnt = cmds.joint(n = self.prefix[0] + 'cheek' + self.jntSuffix, relative = True, p = [ 0, 0, 0] )     
        rCheekP = cmds.group ( n = self.prefix[1] + 'cheekP', em =True, p = self.prefix[1] + "cheek" + self.grpSuffix )
        cmds.xform (rCheekP, relative = True, t = [ 0, 0, 0] )
        rCheekJnt = cmds.joint(n = self.prefix[1] + 'cheek' + self.jntSuffix, relative = True, p = [ 0, 0, 0] )
        
        lSqiuntPuff = cmds.group ( n = self.prefix[0] + 'squintPuffP', em =True, p = self.prefix[0] + "squintPuff" + self.grpSuffix )
        cmds.xform (lSqiuntPuff, relative = True, t = [ 0, 0, 0] )
        lSqiuntPuffJnt = cmds.joint(n = self.prefix[0] + 'squintPuff' + self.jntSuffix, relative = True, p = [ 0, 0, 0] ) 
        rSquintPuff = cmds.group ( n = self.prefix[1] + 'squintPuffP', em =True, p = self.prefix[1] + "squintPuff" + self.grpSuffix )
        cmds.xform (rSquintPuff, relative = True, t = [ 0, 0, 0])
        rSqiuntPuffJnt = cmds.joint(n = self.prefix[1] + 'squintPuff' + self.jntSuffix, relative = True, p = [ 0, 0, 0] ) 
        
        lLowCheek = cmds.group ( n = self.prefix[0] + 'lowCheekP', em =True, p = self.prefix[0] + "lowCheek" + self.grpSuffix )
        cmds.xform (lLowCheek, relative = True, t = [ 0, 0, 0] )
        lLowCheekJnt = cmds.joint(n = self.prefix[0] + 'lowCheek' + self.jntSuffix, relative = True, p = [ 0, 0, 0] ) 
        rLowCheek = cmds.group ( n = self.prefix[1] + 'lowCheekP', em =True, p = self.prefix[1] + "lowCheek" + self.grpSuffix )
        cmds.xform (rLowCheek,  relative = True, t = [ 0, 0, 0]  )
        rLowCheekJnt = cmds.joint(n = self.prefix[1] + 'lowCheek' + self.jntSuffix, relative = True, p = [ 0, 0, 0] ) 
        
        if cmds.objExists ( 'jawClose' + self.jntSuffix ):
            cmds.parentConstraint ('jawClose' + self.jntSuffix, self.prefix[0] + 'lowCheek_grp', maintainOffset = 1 )
            cmds.parentConstraint ('jawClose' + self.jntSuffix, self.prefix[1] + 'lowCheek_grp', maintainOffset = 1 )