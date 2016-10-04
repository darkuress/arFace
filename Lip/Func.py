#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright(c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

import maya.cmds as cmds
import Base
reload(Base)
import math
import fnmatch
import re

class Func(Base.Base):
    def __init__(self, **kw):
        """
        initializing variables
        """
        #local variables
        Base.Base.__init__(self, **kw)


    def mirrorCurve(self, lCrv, rCrv):
        """
        mirroring curve
        """
        lCrvCv = cmds.ls(lCrv + '.cv[*]', fl =1)
        rCrvCv = cmds.ls(rCrv + '.cv[*]', fl =1)
        cvLeng = len(lCrvCv)
        
        for i in range(cvLeng):
            mirrorAdd = cmds.shadingNode('addDoubleLinear', asUtility=True, n = 'mirror' + str(i) + '_add')
            cmds.setAttr(mirrorAdd + '.input1', 1)
            reversMult = cmds.shadingNode('multiplyDivide', asUtility =1, n = 'reverse%s_mult'%str(i).zfill(2))
            cmds.connectAttr(lCrvCv[i] + '.xValue', reversMult+ '.input1X')
            cmds.setAttr(reversMult+ '.input2X', -1)
            cmds.connectAttr(reversMult+ '.outputX', mirrorAdd + '.input2')
            cmds.connectAttr(mirrorAdd + '.output', rCrvCv[cvLeng-i-1] + '.xValue')
            cmds.connectAttr(lCrvCv[i] + '.yValue', rCrvCv[cvLeng-i-1] + '.yValue')
            cmds.connectAttr(lCrvCv[i] + '.zValue', rCrvCv[cvLeng-i-1] + '.zValue')

    def distance(self, inputA=[1,1,1], inputB=[2,2,2]):
        """
        distance func
        inputA = [x, x, x]
        inputB = [y, y, y]
        """
        return math.sqrt(pow(inputB[0]-inputA[0], 2) + pow(inputB[1]-inputA[1], 2) + pow(inputB[2]-inputA[2], 2))

    def indiCrvSetup(self, name):
        """
        indivisual curve setup
        """
        upCrv = 'up'+ name + self.crvSuffix
        loCrv = 'lo'+ name + self.crvSuffix
        crvShape = cmds.listRelatives(upCrv, c=1, type = 'nurbsCurve')
        upCVs = cmds.ls(upCrv + '.cv[*]', fl = 1)
        loCVs = cmds.ls(loCrv + '.cv[*]', fl = 1)
        cvNum = len(upCVs) 
           
        lipCrvStartPos = cmds.xform (upCVs[0], q=1, ws =1, t = 1)
        lipCrvEndPos = cmds.xform (upCVs[cvNum-1], q=1, ws =1, t = 1)
        nCrvPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = 'cnt' + name + '_poc')
        cmds.connectAttr(crvShape[0]+'.worldSpace',  nCrvPoc + '.inputCurve')   
        cmds.setAttr(nCrvPoc + '.turnOnPercentage', 1)    
        cmds.setAttr(nCrvPoc + '.parameter', .5)
        lipCrvMidPos = cmds.getAttr(nCrvPoc + '.position')
        
        lipCrvStart = cmds.group (em = 1, n = name + 'Start' + self.grpSuffix)
        cmds.xform(lipCrvStart, ws = 1, t = lipCrvStartPos)
        rCorner = cmds.joint(n= 'rCorner'+ name + self.jntSuffix, p= lipCrvStartPos)
        
        uplipCrvMid = cmds.group (em = 1, n = 'up' + name + 'Mid' + self.grpSuffix) 
        cmds.xform(uplipCrvMid, ws = 1, t = list(lipCrvMidPos[0])) 
        midUpJnt = cmds.joint(n = 'cntUp' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0])  
    
        lolipCrvMid = cmds.group (em = 1, n = 'lo' + name + 'Mid' + self.grpSuffix) 
        cmds.xform(lolipCrvMid, ws = 1, t = list(lipCrvMidPos[0])) 
        midLoJnt = cmds.joint(n = 'cntLo' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0])
    
        lipCrvEnd = cmds.group (em = 1, n = name + 'End' + self.grpSuffix) 
        cmds.xform(lipCrvEnd, ws = 1, t = lipCrvEndPos) 
        lCorner = cmds.joint(n= 'lCorner' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0])  
    
        indiGrp = cmds.group(lipCrvStart, uplipCrvMid, lolipCrvMid, lipCrvEnd, upCrv, loCrv, n = name + '_indiGrp') 
        cmds.parent (indiGrp, 'upLipCrv' + self.grpSuffix)
    
        #skinning
        upSkin = cmds.skinCluster(rCorner, midUpJnt, lCorner, upCrv, toSelectedBones = 1)    
        loSkin = cmds.skinCluster(rCorner, midLoJnt, lCorner, loCrv, toSelectedBones = 1)
        
    
        numVal = { 0: 15, 1:0.85, 2:0.98, 4: 0.98, 5:0.85, 6:0.15 }
        for key, val in numVal.items():    
            cmds.skinPercent(upSkin[0], upCVs[key], tv =(midUpJnt, val))
            cmds.skinPercent(loSkin[0], loCVs[key], tv =(midLoJnt, val))         
        
        ctlCrvs = { 'JawOpen':'lowJaw_dir', 'TyLip':'jaw_UDLR' }
        if name in ctlCrvs.keys():
            cornerMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = name +'Corner_mult')
            dampMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = name + 'damp_mult')
            txAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = name + 'TX_plus')
            #endAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = name + 'TY' + str(i) +'_plus')  
            # corner tx value
            cmds.connectAttr(midLoJnt+ '.tx', cornerMult+ '.input1X')  
            cmds.connectAttr(midLoJnt+ '.ty', cornerMult+ '.input1Y')  
            cmds.connectAttr(midLoJnt+ '.ty', cornerMult+ '.input1Z')  
            
            cmds.setAttr(cornerMult + '.input2X', .5)#lipCorners.tx follow midLoJnt.tx
            cmds.setAttr(cornerMult + '.input2Y', .06)#lipLCorner.tx inner when jaw open 
            cmds.setAttr(cornerMult + '.input2Z', -.06)#lipRCorner.tx inner when jaw open
            
            cmds.connectAttr(cornerMult + '.outputY', txAvg + '.input3D[0].input3Dy')
            cmds.connectAttr(cornerMult + '.outputZ', txAvg + '.input3D[0].input3Dz')
            cmds.connectAttr(cornerMult + '.outputX', txAvg + '.input3D[1].input3Dy')
            cmds.connectAttr(cornerMult + '.outputX', txAvg + '.input3D[1].input3Dz')
            cmds.connectAttr(txAvg + '.output3Dy', lCorner + '.tx')
            cmds.connectAttr(txAvg + '.output3Dz', rCorner + '.tx')
            
            # corner ty value
            cmds.connectAttr(midLoJnt+ '.tx', dampMult + '.input1X')  
            cmds.connectAttr(midLoJnt+ '.ty', dampMult + '.input1Y')  
            cmds.connectAttr(midLoJnt+ '.ty', dampMult + '.input1Z') 
            
            cmds.setAttr(dampMult+ '.input2X', .1) # lipCenter.tx follow jaw
            cmds.setAttr(dampMult+ '.input2Y', .5) # lipCorners.ty follow jaw
            cmds.setAttr(dampMult+ '.input2Z', .01) # lipCenter.ty follow jaw
            
            cmds.connectAttr(dampMult + '.outputX',  midUpJnt+'.tx')
            cmds.connectAttr(dampMult + '.outputZ',  midUpJnt+'.ty')
            cmds.connectAttr(dampMult + '.outputY',  lCorner+'.ty')
            cmds.connectAttr(dampMult + '.outputY',  rCorner+'.ty')        
            # connect curve joint with controller 
            '''cmds.connectAttr(ctlCrvs[name] + '.tx', midLoJnt + '.tx')
            cmds.connectAttr(ctlCrvs[name] + '.ty', midLoJnt + '.ty')
            cmds.connectAttr(ctlCrvs[name] + '.tz', midLoJnt + '.tz')'''
        return midLoJnt

    def copyCvWeighs(self):
        """
        copy surface cv's weight to curve's cv
        """
        sel = cmds.ls(sl = True)
        Util.Util.copyCrvSkinWeight(sel[0], sel[1])
        
