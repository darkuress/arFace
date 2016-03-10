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
        self.lipCrvToJoint()
    
    def indiShapeCrvRig(name, posX, posY):
        #select upLip curves that need joints control ('upJawOpen_crv', 'upUDLR_crv'...)  
        upLCrv = 'upL'+ name + self.crvSuffix
        loLCrv = upLCrv.replace('up', 'lo', 1)
    
        crvShape = cmds.listRelatives(upLCrv, c= 1, type = 'nurbsCurve')
        crvCVs = cmds.ls(upLCrv + '.cv[*]', fl = 1)
        cvNum = len(crvCVs) 
           
        lipCrvStartPos = cmds.xform (crvCVs[0], q= 1, ws = 1, t = 1)
        lipCrvEndPos = cmds.xform (crvCVs[cvNum-1], q= 1, ws = 1, t = 1)   
        nCrvPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = 'cnt' + name + '_poc')
        cmds.connectAttr(crvShape[0]+'.worldSpace',  nCrvPoc + '.inputCurve')   
        cmds.setAttr(nCrvPoc + '.turnOnPercentage', 1)    
        cmds.setAttr(nCrvPoc + '.parameter', .5)    
        lipCrvMidPos = cmds.getAttr(nCrvPoc + '.position')    
        
        lipCrvStart = cmds.group (em = 1, n = name + 'Start_grp')
        cmds.xform(lipCrvStart, ws = 1, t = lipCrvStartPos)
        upRCorner = cmds.joint(n= 'upRCorner'+ name+self.jntSuffix, p= lipCrvStartPos)
        cmds.select(lipCrvStart, r= 1)
        loRCorner = cmds.joint(n= 'loRCorner'+ name+self.jntSuffix, p= lipCrvStartPos)  
        
        lipCrvMid = cmds.group (em = 1, n = name + 'Mid_grp') 
        cmds.xform(lipCrvMid, ws = 1, t = list(lipCrvMidPos[0])) 
        midUpJnt = cmds.joint(n = 'cntUp' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0]) 
        cmds.select(lipCrvMid, r= 1) 
        midLoJnt = cmds.joint(n = 'cntLo' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0])
    
        lipCrvEnd = cmds.group (em = 1, n = name + 'End_grp') 
        cmds.xform(lipCrvEnd, ws = 1, t = lipCrvEndPos) 
        upLCorner = cmds.joint(n= 'upLCorner' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0])
        cmds.select (lipCrvEnd, r = 1)
        loLCorner = cmds.joint(n= 'loLCorner' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0])  
        
        cmds.parent(lipCrvStart, lipCrvMid, lipCrvEnd, name+'Crv_indiGrp') 
        cmds.parent (indiGrp, 'lipCrv_grp')
        cmds.setAttr(indiGrp + '.tx', posX)
        cmds.setAttr(indiGrp + '.ty', posY)
        #skinning (cv skin weight input)
        cmds.skinCluster(upRCorner, midUpJnt, upLCorner, upLCrv, toSelectedBones = 1)  
        cmds.skinCluster(loRCorner, midLoJnt, loLCorner, loLCrv, toSelectedBones = 1)