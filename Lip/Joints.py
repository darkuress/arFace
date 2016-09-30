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

class Joints(Func.Func):
    def __init__(self, **kw):
        """
        initializing variables
        """
        #- local variables
        Func.Func.__init__(self, **kw)
        
        self.allBaseJnts = list()

    def createJnts(self, upLow):
        """
        creating joints
        """
        if upLow == self.uploPrefix[0]:
            verts = self.uplipVtxs
        elif upLow == self.uploPrefix[1]:
            verts = self.lolipVtxs
        vNum = len (verts) + 2       
        
        if upLow == self.uploPrefix[0]:
            lipCntPos = self.lipNPos
            vMin = 0
            vMax = vNum
                
        elif upLow == self.uploPrefix[1]:
            lipCntPos = self.lipSPos
            vMin = 1
            vMax = vNum - 1
        
        #increment = 1.0/(vNum-1)
        #
        #- create lip joint guide curve
        tempCrv       = cmds.curve(d= 3, ep= [(-self.lipEPos[0], self.lipEPos[1], self.lipEPos[2]),(lipCntPos), (self.lipEPos)]) 
        guideCrv      = cmds.rename(tempCrv, upLow + "Guide" + self.crvSuffix)
        guideCrvShape = cmds.listRelatives(guideCrv, c = True) 
        cmds.rebuildCurve(guideCrv, d = 3, rebuildType = 0, keepRange = 0) 
                
        #- final lip shape ctrl curve
        templipCrv    = cmds.curve(d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
        cmds.rebuildCurve(rt = 0, d = 3, kr = 0, s = 2)    
        lipCrv        = cmds.rename (templipCrv, upLow + 'Lip' + self.crvSuffix)
        lipCrvShape   = cmds.listRelatives(lipCrv, c = True)
        lipCrvGrp     = self.group([lipCrv, guideCrv], upLow + 'LipCrv' + self.grpSuffix)

        #- lip curve for LipJotX tx,ty for UDLR ctrl
        tempTyCrv = cmds.curve(d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
        cmds.rebuildCurve(rt = 0, d = 3, kr = 0, s = 4)    
        tyLipCrv = cmds.rename(tempTyCrv, upLow +'TyLip' + self.crvSuffix) 
        tylipCrvShape = cmds.listRelatives(tyLipCrv, c = True) 
        cmds.parent(tyLipCrv, lipCrvGrp)

        
        #- lipTarget curve shape
        lUpLow = self.prefix[0] + upLow
        rUpLow = self.prefix[1] + upLow
        
        jawOpenCrv = cmds.duplicate(lipCrv,     n = upLow + 'JawOpen' + self.crvSuffix)
        
        lLipWideCrv   = cmds.duplicate(lipCrv,  n = lUpLow + 'lipWide' + self.crvSuffix)
        rLipWideCrv   = cmds.duplicate(lipCrv,  n = rUpLow + 'lipWide' + self.crvSuffix)
        self.mirrorCurve(lLipWideCrv[0], rLipWideCrv[0])
        cmds.hide(rLipWideCrv[0])
        
        lLipECrv      = cmds.duplicate(lipCrv,  n = lUpLow + 'lipE' + self.crvSuffix)
        rLipECrv      = cmds.duplicate(lipCrv,  n = rUpLow + 'lipE' + self.crvSuffix)  
        self.mirrorCurve(lLipECrv[0], rLipECrv[0])
        cmds.hide(rLipECrv[0])
        
        lUCrv         = cmds.duplicate(lipCrv,  n = lUpLow + 'U' + self.crvSuffix)
        rUCrv         = cmds.duplicate(lipCrv,  n = rUpLow + 'U' + self.crvSuffix) 
        self.mirrorCurve(lUCrv[0], rUCrv[0])
        cmds.hide(rUCrv[0])
        
        lOCrv         = cmds.duplicate(lipCrv,  n = lUpLow + 'O' + self.crvSuffix) 
        rOCrv         = cmds.duplicate(lipCrv,  n = rUpLow + 'O' + self.crvSuffix)
        self.mirrorCurve(lOCrv[0], rOCrv[0])
        cmds.hide(rOCrv[0])
        
        lHappyCrv  = cmds.duplicate(lipCrv,    n = lUpLow + 'Happy' + self.crvSuffix) 
        rHappyCrv  = cmds.duplicate(lipCrv,    n = rUpLow + 'Happy' + self.crvSuffix)
        self.mirrorCurve(lHappyCrv[0], rHappyCrv[0])
        cmds.hide(rHappyCrv[0])
        
        lSadCrv    = cmds.duplicate(lipCrv,    n = lUpLow + 'Sad' + self.crvSuffix) 
        rSadCrv    = cmds.duplicate(lipCrv,    n = rUpLow + 'Sad' + self.crvSuffix) 
        self.mirrorCurve(lSadCrv[0], rSadCrv[0])
        cmds.hide(rSadCrv[0])
        
        lipCrvBS = cmds.blendShape(jawOpenCrv[0],
                                   lLipWideCrv[0],rLipWideCrv[0],
                                   lLipECrv[0],rLipECrv[0],
                                   lUCrv[0], rUCrv[0],
                                   lOCrv[0], rOCrv[0],
                                   lHappyCrv[0],rHappyCrv[0],
                                   lSadCrv[0],rSadCrv[0],
                                   lipCrv, n = upLow + 'LipCrvBS')
        cmds.blendShape(lipCrvBS[0],
                        edit=True,
                        w=[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1),(9, 1), (10, 1), (11, 1), (12, 1)])
        
        ##- lip curve for LipJotX translateYZ
        #tempTylipCrv  = cmds.curve(d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
        #cmds.rebuildCurve(rt = 0, d = 3, kr = 0, s = 4)    
        #tyLipCrv      = cmds.rename (tempTylipCrv, upLow + 'LipTY' + self.crvSuffix)  
        #tylipCrvShape = cmds.listRelatives(tyLipCrv, c = True)  
        #cmds.parent(tyLipCrv, lipCrvGrp)
        #
        ##- lip Swivel crv Target for LipJotX tx,ty
        #UDlrCrv       = cmds.duplicate(tyLipCrv, n = upLow + 'UDlr' + self.crvSuffix) 
        #jawOpenTyCrv  = cmds.duplicate(tyLipCrv, n = upLow + 'JawOpenTY' + self.crvSuffix) #lipJotX translateY when jawOpen 
        #lipTYBS       = cmds.blendShape(UDlrCrv[0], jawOpenTyCrv[0], tyLipCrv, n =upLow + 'LipTYBS')
        #cmds.blendShape(lipTYBS[0], edit=True, w=[(0, 1), (1, 1)]) 
        #    
        ##- lip controller curve shape(different number of points (4), so can not be target of the blendShape)      
        #templipCtlCrv  = cmds.curve(d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
        #cmds.rebuildCurve(rt = 0, d = 3, kr = 0, s = 2)   
        #lipCtlCrv      = cmds.rename(templipCtlCrv, upLow + 'LipCtl' + self.crvSuffix)
        #lipCtlCrvShape = cmds.listRelatives(lipCtlCrv, c = True) 
        #cmds.parent (lipCtlCrv, lipCrvGrp)
        #
        ##- lip Roll control curve shape(different number of points (4), so can not be target of the blendShape)      
        #tempRollCrv     = cmds.curve(d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
        #cmds.rebuildCurve(rt = 0, d = 3, kr = 0, s = 2)   
        #lipRollCrv      = cmds.rename(tempRollCrv, upLow + 'LipRoll' + self.crvSuffix) 
        #lipRollCrvShape = cmds.listRelatives(lipRollCrv, c = True) 
        #cmds.parent(lipRollCrv, lipCrvGrp)
        #
        ##- targets for lip Roll crv
        #rollCtlCrv = cmds.duplicate(lipRollCrv, n = upLow + 'RollCtl' + self.crvSuffix) 
        #lURollCrv  = cmds.duplicate(lipRollCrv, n = upLow + 'LURoll' + self.crvSuffix)
        #rURollCrv  = cmds.duplicate(lURollCrv,  n = upLow + 'RURoll' + self.crvSuffix) 
        #self.rCrvTolCrv(lURollCrv[0], rURollCrv[0], 'U', lipCrvGrp, hideR = True)
        #
        #lORollCrv  = cmds.duplicate(lipRollCrv, n = upLow + 'LORoll' + self.crvSuffix)
        #rORollCrv  = cmds.duplicate(lORollCrv,  n = upLow + 'RORoll' + self.crvSuffix) 
        #self.rCrvTolCrv(lORollCrv[0], rORollCrv[0], 'O', lipCrvGrp, hideR = True)
        #
        #lShRollCrv = cmds.duplicate(lipRollCrv, n = upLow + 'LShRoll' + self.crvSuffix)
        #rShRollCrv = cmds.duplicate(lShRollCrv, n = upLow + 'RShRoll' + self.crvSuffix)
        #self.rCrvTolCrv(lShRollCrv[0], rShRollCrv[0], 'Sh', lipCrvGrp, hideR = True)
        #
        #lMRollCrv  = cmds.duplicate(lipRollCrv, n = upLow + 'LMRoll' + self.crvSuffix)
        #rMRollCrv  = cmds.duplicate(lipRollCrv, n = upLow + 'RMRoll' + self.crvSuffix)
        #self.rCrvTolCrv(lMRollCrv[0], rMRollCrv[0], 'M', lipCrvGrp, hideR = True)
        #
        #lipRollBS = cmds.blendShape(rollCtlCrv[0], lURollCrv[0],rURollCrv[0], rORollCrv[0],rORollCrv[0], lShRollCrv[0],lShRollCrv[0], lMRollCrv[0],rMRollCrv[0], lipRollCrv, n = upLow + 'LipRollBS')
        #cmds.blendShape(lipRollBS[0], edit=True, w=[(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1), (7,1), (8,1)]) 
        #
        ##- lip RollYZ control curve shape
        #lipRollYZCrv      = cmds.duplicate(lipRollCrv, n = upLow + 'RollYZ' + self.crvSuffix)
        #lipRollYZCrvShape = cmds.listRelatives(lipRollYZCrv, c = True)
        #
        ##- targets for lip RollYZ crv
        #RollYZCtrlCrv   = cmds.duplicate(lipRollYZCrv,    n = upLow + 'RollYZCtl' + self.crvSuffix)
        #lURollYZCrv     = cmds.duplicate(lipRollYZCrv,    n = upLow + 'LURollYZ' + self.crvSuffix) 
        #rURollYZCrv     = cmds.duplicate(lURollYZCrv,     n = upLow + 'RURollYZ' + self.crvSuffix)
        #self.rCrvTolCrv(lURollYZCrv[0], rURollYZCrv[0], 'U', lipCrvGrp, hideR = True)
        #
        #lORollYZCrv     = cmds.duplicate(lipRollYZCrv,    n = upLow + 'LORollYZ' + self.crvSuffix) 
        #rORollYZCrv     = cmds.duplicate(lORollYZCrv,     n = upLow + 'RORollYZ' + self.crvSuffix)
        #self.rCrvTolCrv(lORollYZCrv[0], rORollYZCrv[0], 'O', lipCrvGrp, hideR = True)
        #
        #lShRollYZCrv    = cmds.duplicate(lipRollYZCrv,    n = upLow + 'LShRollYZ' + self.crvSuffix)
        #rShRollYZCrv    = cmds.duplicate(lShRollYZCrv,    n = upLow + 'RShRollYZ' + self.crvSuffix)
        #self.rCrvTolCrv(lShRollYZCrv[0], rShRollYZCrv[0], 'Sh', lipCrvGrp, hideR = True)
        #
        #lHappyRollYZCrv = cmds.duplicate(lipRollYZCrv,    n = upLow + 'LHappyRollYZ' + self.crvSuffix)
        #rHappyRollYZCrv = cmds.duplicate(lHappyRollYZCrv, n = upLow + 'RHappyRollYZ' + self.crvSuffix)
        #self.rCrvTolCrv(lHappyRollYZCrv[0], rHappyRollYZCrv[0], 'Happy', lipCrvGrp, hideR = True)
        #
        #lWideRollYZCrv  = cmds.duplicate(lipRollYZCrv,    n = upLow + 'lWideRollYZ' + self.crvSuffix)
        #rWideRollYZCrv  = cmds.duplicate(lWideRollYZCrv,  n = upLow + 'rWideRollYZ' + self.crvSuffix)
        #self.rCrvTolCrv(lWideRollYZCrv[0], rWideRollYZCrv[0], 'Wide', lipCrvGrp, hideR = True)
        #
        #lERollYZCrv     = cmds.duplicate(lipRollYZCrv,    n = upLow + 'LERollYZ' + self.crvSuffix)
        #rERollYZCrv     = cmds.duplicate(lERollYZCrv,     n = upLow + 'RERollYZ' + self.crvSuffix)
        #self.rCrvTolCrv(lERollYZCrv[0], rERollYZCrv[0], 'E', lipCrvGrp, hideR = True)
        #
        #lMRollYZCrv     = cmds.duplicate(lipRollYZCrv,    n = upLow + 'LMRollYZ' + self.crvSuffix)
        #rMRollYZCrv     = cmds.duplicate(lMRollYZCrv,     n = upLow + 'RMRollYZ' + self.crvSuffix)
        #self.rCrvTolCrv(lMRollYZCrv[0], rMRollYZCrv[0], 'M', lipCrvGrp, hideR = True)
        #
        #RollYZBS = cmds.blendShape(RollYZCtrlCrv[0], lURollYZCrv[0],rURollYZCrv[0], rORollYZCrv[0],rORollYZCrv[0], lShRollYZCrv[0],rShRollYZCrv[0], lHappyRollYZCrv[0],lHappyRollYZCrv[0], lERollYZCrv[0],rERollYZCrv[0], lMRollYZCrv[0],rMRollYZCrv[0], lipRollYZCrv[0], n = upLow + 'RollYZBS')
        #cmds.blendShape(RollYZBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3,1), (4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1)])     
        #
        ##- lip RollYZ control curve shape!!!!!!!!!!!! center pivot / place the group in world to mirror 
        #if not cmds.objExists('cheekCrv' + self.grpSuffix):
        #    cheekCrvGrp     = cmds.group(n = 'cheekCrv' + self.grpSuffix, em =True, p = 'faceMain|crv' + self.grpSuffix)  
        #    cheekTempCrv    = cmds.curve(d= 1, p = [(self.lowCheekPos), (self.lipEPos), (self.cheekPos), (self.squintPuffPos)])  
        #    lCheekCrv       = cmds.rename(cheekTempCrv, self.prefix[0] + "cheek_crv") 
        #    rCheekCrv       = cmds.duplicate(lCheekCrv, n = self.prefix[1] + 'cheek' + self.crvSuffix)
        #    cmds.setAttr(rCheekCrv[0] + '.scaleX', -1)
        #    cmds.parent(lCheekCrv,rCheekCrv, 'faceMain|crv_grp|cheekCrv' + self.grpSuffix)
        #    cmds.xform (lCheekCrv,rCheekCrv, centerPivots = 1)
        #    
        #    #- cheek inward movement(downward movement by jawSemi)
        #    #- left right control seperately using blendShape
        #    lJawSwivelCheek = cmds.duplicate(lCheekCrv,      n = 'lCheekJawSwivel' + self.crvSuffix)
        #    rJawSwivelCheek = cmds.instance(lJawSwivelCheek, n = 'rCheekJawSwivel' + self.crvSuffix) 
        #    
        #    #- cheek inward movement(downward movement by jawSemi)
        #    #cheek inward movement(downward movement by jawSemi) 
        #    lJawOpenCheek   = cmds.duplicate(lCheekCrv,      n = 'lCheekJawOpen' + self.crvSuffix)
        #    rJawOpenCheek   = cmds.instance(lJawOpenCheek,   n = 'rCheekJawOpen' + self.crvSuffix)
        #    lJawUDlrCheek   = cmds.duplicate(lCheekCrv,      n = 'lCheekJawUDlr' + self.crvSuffix)
        #    rJawUDlrCheek   = cmds.instance(lJawUDlrCheek,   n = 'rCheekJawUDlr' + self.crvSuffix)
        #    lHappyCheekCrv  = cmds.duplicate(lCheekCrv,      n = 'lHappyCheek' + self.crvSuffix) 
        #    rHappyCheekCrv  = cmds.instance(lHappyCheekCrv,  n = 'rHappyCheek' + self.crvSuffix)
        #    cmds.parent(lHappyCheekCrv, rHappyCheekCrv, 'HappyCrv' + self.grpSuffix)
        #    lWideCheekCrv   = cmds.duplicate(lCheekCrv,      n = 'lWideCheek' + self.crvSuffix) 
        #    rWideCheekCrv   = cmds.instance(lWideCheekCrv,   n = 'rWideCheek' + self.crvSuffix)
        #    cmds.parent(lWideCheekCrv, rWideCheekCrv, 'WideCrv' + self.grpSuffix)
        #    lSadCheekCrv    = cmds.duplicate(lCheekCrv,      n = 'lSadCheek' + self.crvSuffix) 
        #    rSadCheekCrv    = cmds.instance(lSadCheekCrv,    n = 'rSadCheek' + self.crvSuffix)
        #    cmds.parent(lSadCheekCrv, rSadCheekCrv, 'SadCrv' + self.grpSuffix)
        #    lECheekCrv      = cmds.duplicate(lCheekCrv,      n = 'lECheek' + self.crvSuffix) 
        #    rECheekCrv      = cmds.instance(lECheekCrv,      n = 'rECheek' + self.crvSuffix) 
        #    cmds.parent(lECheekCrv, rECheekCrv, 'ECrv' + self.grpSuffix)
        #    lUCheekCrv      = cmds.duplicate(lCheekCrv,      n = 'lUCheek' + self.crvSuffix) 
        #    rUCheekCrv      = cmds.instance(lUCheekCrv,      n = 'rUCheek' + self.crvSuffix) 
        #    cmds.parent(lUCheekCrv, rUCheekCrv, 'UCrv' + self.grpSuffix)
        #    lOCheekCrv      = cmds.duplicate(lCheekCrv,      n = 'lOCheek' + self.crvSuffix) 
        #    rOCheekCrv      = cmds.instance(lOCheekCrv,      n = 'rOCheek' + self.crvSuffix) 
        #    cmds.parent(lOCheekCrv, rOCheekCrv, 'OCrv' + self.grpSuffix)
        #    lShCheekCrv     = cmds.duplicate(lCheekCrv,      n = 'lShCheek' + self.crvSuffix) 
        #    rShCheekCrv     = cmds.instance(lShCheekCrv,     n = 'rShCheek' + self.crvSuffix) 
        #    cmds.parent(lShCheekCrv, rShCheekCrv, 'ShCrv' + self.grpSuffix)
        #    lCheekBS        = cmds.blendShape(lJawSwivelCheek[0], lJawOpenCheek[0], lJawUDlrCheek[0],lHappyCheekCrv[0],lWideCheekCrv[0],lSadCheekCrv[0],lECheekCrv[0],lUCheekCrv[0],lOCheekCrv[0], lShCheekCrv[0], lCheekCrv, n ='lCheekBS')
        #    cmds.blendShape(lCheekBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1)])   
        #    rCheekBS        = cmds.blendShape(rJawSwivelCheek[0], rJawOpenCheek[0], rJawUDlrCheek[0],rHappyCheekCrv[0],rWideCheekCrv[0],rSadCheekCrv[0],rECheekCrv[0],rUCheekCrv[0],rOCheekCrv[0], rShCheekCrv[0], rCheekCrv, n ='rCheekBS')
        #    cmds.blendShape(rCheekBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1)])    
        #    cmds.move(2,0,0, lJawSwivelCheek, lJawOpenCheek, lJawUDlrCheek, lHappyCheekCrv, lWideCheekCrv, lSadCheekCrv, lECheekCrv, lOCheekCrv, lShCheekCrv, rotatePivotRelative = 1 )
        #    cmds.move(-2,0,0, rJawSwivelCheek, rJawOpenCheek, rJawUDlrCheek, rHappyCheekCrv, rWideCheekCrv, rSadCheekCrv, rECheekCrv, rOCheekCrv, rShCheekCrv, rotatePivotRelative = 1 )
        #    
        #    #- attach ctrls to main cheek curves
        #    for lr in self.prefix:
        #        cvLs = cmds.ls(lr + '_cheek_crv.cv[*]', fl = 1)
        #        cvLen = len(cvLs)
        #        lipCorner = cmds.group (em = 1, n = lr+'_lipCorner', p ='supportRig') 
        #        cheekList = [lr + '_lowCheek' + self.grpSuffix, str(lipCorner), lr + '_cheek' + self.grpSuffix, lr + '_squintPuff' + self.grpSuffix] 
        #     
        #        for v in range(0, cvLen):
        #            cheekPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = 'cheek' + str(v) + '_poc')
        #            cmds.connectAttr(lr+'_cheek_crvShape.worldSpace', cheekPoc + '.inputCurve')   
        #            cmds.setAttr (cheekPoc + '.parameter', v)            
        #            cmds.connectAttr (cheekPoc + '.positionX', cheekList[v] + '.tx')
        #            cmds.connectAttr (cheekPoc + '.positionY', cheekList[v] + '.ty')
        #            cmds.connectAttr (cheekPoc + '.positionZ', cheekList[v] + '.tz')
        #
        ##- create lip joints parent group
        #lipJotGrp = cmds.group(n = upLow + 'LipJnt' + self.grpSuffix, em =True)
        #
        ##cmds.parent(lipJotGrp, 'lipJotP')
        #cmds.xform (lipJotGrp, ws = 1, t = self.jawRigPos) 
        #
        ##- delete detail lip ctrls 
        ##lipDetailP = upLow + 'LipDetailP'
        #lipDetailP = 'lipDetailP'
        ##if not cmds.objExists(lipDetailP):
        ##    cmds.createNode('transform', n = lipDetailP)
        ##kids = cmds.listRelatives (lipDetailP, ad=True, type ='transform')   
        ##if kids:
        ##    cmds.delete (kids)     
        #    
        #if upLow == self.uploPrefix[0]:
        #    min = 0
        #    max = vNum
        #elif upLow == self.uploPrefix[1]:    
        #    min = 1
        #    max = vNum-1           
        #      
        #for i in range (min, max):
        #    poc = self.createPocNode(upLow + 'Lip' + str(i) + '_poc', guideCrvShape[0], increment*i)
        #    
        #    self.createLipJoint(upLow, self.jawRigPos, self.lipYPos, poc, lipJotGrp, i)
        #    
        #    #- create detail lip ctrl        
        #    if i == 0 or i == vNum-1:
        #        self.createDetailCtl(upLow, i)
        #        cmds.parent(upLow +'LipDetailP'+ str(i), lipDetailP)
        #        cmds.setAttr(upLow +'LipDetailP'+ str(i)+'.tx', increment*i)
        #        cmds.setAttr(upLow +'LipDetailP'+ str(i)+'.ty', -1.5)
        #        cmds.setAttr(upLow +'LipDetailP'+ str(i)+'.tz', 0)
        #        cmds.setAttr(upLow +'LipDetailP'+ str(i)+'.sx', 0.25)
        #    else:
        #        self.createDetailCtl(upLow, i)           
        #        cmds.parent(upLow +'LipDetailP'+ str(i), lipDetailP)
        #        cmds.setAttr(upLow +'LipDetailP'+ str(i) + '.tx', increment*i) 
        #        cmds.setAttr(upLow +'LipDetailP'+ str(i) + '.ty', 0)
        #        cmds.setAttr(upLow +'LipDetailP'+ str(i) + '.tz', 0)
        #    
        #    #- create lip curve POC
        #    lipCrvPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = upLow +'LipCrv' + str(i) + '_poc' )
        #    cmds.connectAttr(lipCrvShape[0] + ".worldSpace",  lipCrvPoc + '.inputCurve')   
        #    cmds.setAttr(lipCrvPoc  + '.turnOnPercentage', 1)    
        #    cmds.setAttr(lipCrvPoc  + '.parameter', increment*i)
        #    
        #    #- create lip Ty curve POC
        #    lipTYPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = upLow +'LipTY' + str(i) + '_poc' )
        #    cmds.connectAttr(tylipCrvShape[0] + ".worldSpace",  lipTYPoc + '.inputCurve')   
        #    cmds.setAttr(lipTYPoc  + '.turnOnPercentage', 1)    
        #    cmds.setAttr(lipTYPoc  + '.parameter', increment*i)
        #    
        #    #- create lipCtrl curve POC
        #    ctlPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = upLow +'LipCtl' + str(i) + '_poc')
        #    cmds.connectAttr(lipCtlCrvShape[0] + ".worldSpace",  ctlPoc + '.inputCurve')   
        #    cmds.setAttr(ctlPoc  + '.turnOnPercentage', 1)    
        #    cmds.setAttr(ctlPoc  + '.parameter', increment*i)
        #    
        #    #- create lipRoll curve POC  lipRollCrv, lipRollYZCrv,
        #    
        #    lipRollPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = upLow +'LipRoll' + str(i) + '_poc' )
        #    cmds.connectAttr(lipRollCrvShape[0] + ".worldSpace",  lipRollPoc + '.inputCurve')   
        #    cmds.setAttr(lipRollPoc + '.turnOnPercentage', 1)    
        #    cmds.setAttr(lipRollPoc + '.parameter', increment*i)  
        #    
        #    lipRollYZPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = upLow +'LipRollYZ' + str(i) + '_poc' )
        #    cmds.connectAttr(lipRollYZCrvShape[0] + ".worldSpace",  lipRollYZPoc + '.inputCurve')   
        #    cmds.setAttr(lipRollYZPoc  + '.turnOnPercentage', 1)    
        #    cmds.setAttr(lipRollYZPoc  + '.parameter', increment*i) 
        #
        #return {'lipJntGrp' : lipJotGrp , 'lipCrvGrp' : lipCrvGrp}
