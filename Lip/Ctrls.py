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
        self.__mouthCtlToCrv()

    def __mouthCtlToCrv(self):    
        """
        """
        #- 1. swivel setup
        if not cmds.listConnections('lipJotP', s=1):
            swivelTranXMult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'swivelTranX_mult')
            cmds.connectAttr('swivel_ctrl.tx', swivelTranXMult + '.input1X')
            cmds.connectAttr('swivel_ctrl.tx', swivelTranXMult + '.input1Y')
            cmds.connectAttr('swivel_ctrl.tx', swivelTranXMult + '.input1Z')
            # tx*0.5 = lipJotP.tx / tx*6 = LipJotX*.ry / tx*20 = 'jawSemi.rz'
            cmds.connectAttr(self.faceFactors['lip'] + '.swivel_lipJntP_tx', swivelTranXMult + '.input2X')
            cmds.connectAttr(self.faceFactors['lip'] + '.swivel_lipJntX_ry', swivelTranXMult + '.input2Y')
            cmds.connectAttr(self.faceFactors['lip'] + '.swivel_lipJntX_rz', swivelTranXMult + '.input2Z')
            cmds.connectAttr(swivelTranXMult + '.outputX', 'lipJotP.tx')
            
            swivelTranYMult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'swivelTranY_mult')
            cmds.connectAttr('swivel_ctrl.ty', swivelTranYMult + '.input1X') # for scale
            cmds.connectAttr('swivel_ctrl.ty', swivelTranYMult + '.input1Y')
            cmds.connectAttr('swivel_ctrl.ty', swivelTranYMult + '.input1Z') # for scale
            cmds.connectAttr(self.faceFactors['lip'] + '.swivel_lipJntP_ty', swivelTranYMult + '.input2Y')
            cmds.connectAttr(swivelTranYMult + '.outputY', 'lipJotP.ty')
    
            # mouth_move setup
            mouthTxMult    = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'mouthTranX_mult')
            loCheekY_mult  = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'loCheekY_mult')
            midCheekY_Mult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'midCheekY_mult')
            cmds.connectAttr('mouth_move.tx', mouthTxMult + '.input1X')
            cmds.connectAttr('mouth_move.tx', mouthTxMult + '.input1Z')
            cmds.connectAttr(self.faceFactors['lip'] + '.mouth_lipJntY_ry', mouthTxMult + '.input2X')  
            cmds.connectAttr(self.faceFactors['lip'] + '.mouth_lipJntY_rz', mouthTxMult + '.input2Z')  
            cmds.connectAttr('mouth_move.tx', loCheekY_mult + '.input1X')
            cmds.connectAttr('mouth_move.tx', loCheekY_mult + '.input1Y')    
            cmds.connectAttr('mouth_move.tx', midCheekY_Mult + '.input1X')
            cmds.connectAttr('mouth_move.tx', midCheekY_Mult + '.input1Y') 
            cmds.connectAttr(self.faceFactors['lip'] + '.mouth_loCheekRY',  loCheekY_mult + '.input2X')
            cmds.connectAttr(self.faceFactors['lip'] + '.mouth_loCheekRZ',  loCheekY_mult + '.input2Y')
            cmds.connectAttr(self.faceFactors['lip'] + '.mouth_midCheekRY', midCheekY_Mult + '.input2X')# for cheekRotY
            cmds.connectAttr(self.faceFactors['lip'] + '.mouth_midCheekRZ', midCheekY_Mult + '.input2Y')# for cheekRotY
            midCheekRY = [self.prefix[0] + 'midCheekRotY', self.prefix[1] + 'midCheekRotY' ]
            loCheekRY  = [self.prefix[0] + 'loCheekRotY',  self.prefix[1] + 'loCheekRotY' ]
            for lo in loCheekRY:            
                cmds.connectAttr(loCheekY_mult + '.outputX', lo + '.ry')
                cmds.connectAttr(loCheekY_mult + '.outputY', lo + '.rz')
            for mid in midCheekRY:
                cmds.connectAttr(midCheekY_Mult + '.outputX', mid + '.ry')
                cmds.connectAttr(midCheekY_Mult + '.outputY', mid + '.rz')
            
            mouthTyMult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'mouthTranY_mult')
            cmds.connectAttr('mouth_move.ty', mouthTyMult + '.input1X')
            cmds.connectAttr('mouth_move.ty', mouthTyMult+ '.input1Y')
            cmds.connectAttr('mouth_move.ty', mouthTyMult + '.input1Z')
            cmds.connectAttr(self.faceFactors['lip'] + '.mouth_lipJntX_rx', mouthTyMult + '.input2X')
            cmds.connectAttr(self.faceFactors['lip'] + '.mouth_midCheekRX', mouthTyMult + '.input2Y')# for cheekRotX
            cmds.connectAttr(self.faceFactors['lip'] + '.mouth_loCheekRX',  mouthTyMult + '.input2Z')
            
            #jawSemi setup
            cmds.connectAttr(swivelTranXMult + '.outputX', 'jawSemi.tx')
            cmds.connectAttr(swivelTranXMult + '.outputY', 'jawSemi.ry')
            cmds.connectAttr(swivelTranXMult + '.outputZ', 'jawSemi.rz')
            # swivel.ty mainly control lipJotP.ty
            lipPScale_sum = cmds.shadingNode('plusMinusAverage', asUtility= True, n = 'lipPScale_sum')			
            cmds.connectAttr(swivelTranYMult + '.outputY', 'jawSemi.ty')        
            #lipP scale down as lipP/jawSemi goes down
            cmds.setAttr(lipPScale_sum+'.input2D[0].input2Dx', 1)
            cmds.setAttr(lipPScale_sum+'.input2D[0].input2Dy', 1)             
            cmds.connectAttr(self.faceFactors['lip'] + ".swivel_lipJntP_sx", swivelTranYMult + '.input2X')        
            cmds.connectAttr(self.faceFactors['lip'] + ".swivel_lipJntP_sz", swivelTranYMult + '.input2Z')
            cmds.connectAttr(swivelTranYMult + '.outputX', lipPScale_sum+'.input2D[1].input2Dx')
            cmds.connectAttr(swivelTranYMult + '.outputZ', lipPScale_sum+'.input2D[1].input2Dy')
            cmds.connectAttr(lipPScale_sum + '.output2Dx', 'lipJotP.sx')
            cmds.connectAttr(lipPScale_sum + '.output2Dy', 'lipJotP.sz')
                    
            #jawSemi scale down for swivel/UDLR ctrl
            jawSemiScaleMult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'jawSemiScale_mult')
            cmds.connectAttr('swivel_ctrl.ty', jawSemiScaleMult + '.input1X') # for scale
                    
            cmds.connectAttr('swivel_ctrl.ty', jawSemiScaleMult + '.input1Y')
            cmds.connectAttr('swivel_ctrl.ty', jawSemiScaleMult + '.input1Z') # for scale
            
            jawSemiScale_sum = cmds.shadingNode('plusMinusAverage', asUtility= True, n = 'jawSemiScale_sum')
            cmds.setAttr(jawSemiScale_sum+'.input2D[0].input2Dx', 1)
            
            cmds.setAttr(jawSemiScale_sum+'.input2D[0].input2Dy', 1)             
            cmds.connectAttr(self.faceFactors['lip'] + ".swivel_jawSemi_sx", jawSemiScaleMult + '.input2X')        
            cmds.connectAttr(self.faceFactors['lip'] + ".swivel_jawSemi_sz", jawSemiScaleMult + '.input2Z')
            cmds.connectAttr(jawSemiScaleMult + '.outputX', jawSemiScale_sum+'.input2D[1].input2Dx')
            cmds.connectAttr(jawSemiScaleMult + '.outputZ', jawSemiScale_sum+'.input2D[1].input2Dy')
            cmds.connectAttr(jawSemiScale_sum + '.output2Dx', 'jawSemi.sx')
            cmds.connectAttr(jawSemiScale_sum + '.output2Dy', 'jawSemi.sz')        
            
        #jaw_UDLRIO.ty --> 1.lipJotX0.ty / 2. lipJotP.sx. sz / jaw_UDLRIO.tx --> lipJotX0.tz
        if not cmds.listConnections('lowJaw_dir', d =1):	
            jawOpenMult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'jawOpen_mult')         
            jawOpenJnt = self.indiCrvSetup('JawOpen')
            cmds.connectAttr('lowJaw_dir.tx',  jawOpenMult + '.input1X')
            cmds.connectAttr(self.faceFactors['lip'] + ".jawOpenTX_scale",  jawOpenMult + '.input2X')
            cmds.connectAttr(jawOpenMult + '.outputX', jawOpenJnt + '.tx')
        
            cmds.connectAttr('lowJaw_dir.ty',  jawOpenMult + '.input1Y')
            cmds.connectAttr(self.faceFactors['lip'] + ".jawOpenTY_scale",  jawOpenMult + '.input2Y')
            cmds.connectAttr(jawOpenMult + '.outputY', jawOpenJnt + '.ty')
    
            jawCloseRotMult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'jawCloseRot_mult')        
            # jawClose' + self.jntSuffix + '.rx = lowJaw_dir.ty * 36  
            cmds.connectAttr('lowJaw_dir.ty', jawCloseRotMult + '.input1X')
            cmds.connectAttr(self.faceFactors['lip'] + '.jawOpen_jawCloseRX', jawCloseRotMult + '.input2X')   	
            cmds.connectAttr(jawCloseRotMult + '.outputX', 'jawClose' + self.jntSuffix + '.rx')
            
            cmds.connectAttr('lowJaw_dir.tx', jawCloseRotMult + '.input1Y')
            cmds.connectAttr(self.faceFactors['lip'] + '.jawOpen_jawCloseRY', jawCloseRotMult + '.input2Y')   	
            cmds.connectAttr(jawCloseRotMult + '.outputY', 'jawClose' + self.jntSuffix + '.ry')        
        
        if not cmds.listConnections('jaw_UDLR', d =1):
            UDLRTMult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'UDLR_mult')
            UDLRTscaleMult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'UDLRscale_mult')
            jawCloseTranMult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'jawCloseTran_mult')
            jawUDLRJnt = self.indiCrvSetup('TyLip')
            cmds.connectAttr('jaw_UDLR.tx',  UDLRTMult + '.input1X')
            cmds.connectAttr(self.faceFactors['lip'] + ".UDLR_TX_scale",  UDLRTMult + '.input2X')
            cmds.connectAttr(UDLRTMult + '.outputX', jawUDLRJnt + '.tz')
    
            cmds.connectAttr('jaw_UDLR.ty',  UDLRTMult + '.input1Y')
            cmds.connectAttr(self.faceFactors['lip'] + ".UDLR_TY_scale",  UDLRTMult + '.input2Y')
            cmds.connectAttr(UDLRTMult + '.outputY', jawUDLRJnt + '.ty')
               
            # jaw_UDLRIO.ty --> 1.lipJotX0.ty / 2. lipJotP.sx. sz / jaw_UDLRIO.tx --> lipJotX0.tz                
            cmds.connectAttr('jaw_UDLR.ty', UDLRTscaleMult + '.input1X')
            cmds.connectAttr('jaw_UDLR.ty', UDLRTscaleMult + '.input1Z')
            cmds.connectAttr(self.faceFactors['lip'] + ".swivel_lipJntP_sx", UDLRTscaleMult + '.input2X')        
            cmds.connectAttr(self.faceFactors['lip'] + ".swivel_lipJntP_sz", UDLRTscaleMult + '.input2Z')
            cmds.connectAttr(UDLRTscaleMult + '.outputX', lipPScale_sum+'.input2D[2].input2Dx')
            cmds.connectAttr(UDLRTscaleMult + '.outputZ', lipPScale_sum+'.input2D[2].input2Dy') 
    
            # jaw_UDLR.ty --> jawSemiScale
            UDLRJawSemi_mult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'UDLRJawSemi_mult')
            cmds.connectAttr('jaw_UDLR.ty', UDLRJawSemi_mult + '.input1X')
            cmds.connectAttr('jaw_UDLR.ty', UDLRJawSemi_mult + '.input1Z')
    
            cmds.connectAttr(self.faceFactors['lip'] + ".UDLR_jawSemi_sx", UDLRJawSemi_mult + '.input2X')        
            cmds.connectAttr(self.faceFactors['lip'] + ".UDLR_jawSemi_sz", UDLRJawSemi_mult + '.input2Z')
            cmds.connectAttr(UDLRJawSemi_mult + '.outputX', jawSemiScale_sum+'.input2D[2].input2Dx')
            cmds.connectAttr(UDLRJawSemi_mult + '.outputZ', jawSemiScale_sum+'.input2D[2].input2Dy')
            
            # jawClose' + self.jntSuffix + '.ty = UDLR.ty * 2   / jawClose' + self.jntSuffix + '.tz = UDLR.tx * 1.1 	
            cmds.connectAttr('jaw_UDLR.tx', jawCloseTranMult + '.input1X')
            cmds.connectAttr(self.faceFactors['lip'] + '.UDLR_jawCloseTZ', jawCloseTranMult + '.input2X')   	
            cmds.connectAttr(jawCloseTranMult + '.outputX', 'jawClose' + self.jntSuffix + '.tz')     
            
            cmds.connectAttr('jaw_UDLR.ty', jawCloseTranMult + '.input1Y')
            cmds.connectAttr(self.faceFactors['lip'] + '.UDLR_jawCloseTY', jawCloseTranMult + '.input2Y')   	
            cmds.connectAttr(jawCloseTranMult + '.outputY', 'jawClose' + self.jntSuffix + '.ty')
            
        tySum_cheekIn = cmds.shadingNode('plusMinusAverage', asUtility = 1, n = 'cheekXIn_sum')
        cmds.connectAttr(UDLRTscaleMult + '.outputX', tySum_cheekIn + '.input2D[0].input2Dx') 
        cmds.connectAttr(swivelTranYMult + '.outputX', tySum_cheekIn + '.input2D[1].input2Dx')
        cmds.connectAttr(UDLRTscaleMult + '.outputZ', tySum_cheekIn + '.input2D[0].input2Dy')
        cmds.connectAttr(swivelTranYMult + '.outputZ', tySum_cheekIn + '.input2D[1].input2Dy')
    
        cheekIn_reverse = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'cheekTX_reverse')
        cmds.connectAttr(tySum_cheekIn + '.output2Dx', cheekIn_reverse + '.input1X')
        cmds.setAttr(cheekIn_reverse + '.input2X', -1)
        
        midCheekRX = [ 'l_midCheekRotX', 'r_midCheekRotX' ]
        loCheekRX = [ 'l_loCheekRotX', 'r_loCheekRotX' ]    
        for cheek in midCheekRX + loCheekRX:
            cheek_sum = cmds.shadingNode('plusMinusAverage', asUtility= True, n = cheek[ :-4] + '_sum')
            cheekRx_addD = cmds.shadingNode('addDoubleLinear', asUtility= True, n = cheek[ :-4] + '_add')
            cmds.connectAttr(swivelTranXMult + '.outputX', cheek_sum + '.input3D[0].input3Dx')
            cmds.connectAttr(cheek_sum + '.output3Dx', cheek + '.tx') # swivel.tx        
            cmds.connectAttr(swivelTranYMult + '.outputY', cheek_sum + '.input3D[0].input3Dy')
            cmds.connectAttr(jawCloseTranMult + '.outputY', cheek_sum + '.input3D[1].input3Dy') #jaw_UDLRIO.ty --> jawClose' + self.jntSuffix + '.ty 
            cmds.connectAttr(cheek_sum + '.output3Dy', cheek + '.ty') # swivel.ty   
            cmds.connectAttr(swivelTranXMult + '.outputY', cheek_sum + '.input3D[0].input3Dz')
            cmds.connectAttr(jawCloseRotMult + '.outputY', cheek_sum + '.input3D[1].input3Dz') # jawClose' + self.jntSuffix + '.ry <--jawOpen.tx *(jawOpen_jawCloseRY) 
            cmds.connectAttr(cheek_sum + '.output3Dz', cheek + '.ry') # swivel.tx
            cmds.connectAttr(swivelTranXMult + '.outputZ', cheek + '.rz') # swivel.tx
            cmds.connectAttr(jawCloseRotMult + '.outputX', cheekRx_addD + '.input1') #'jawClose' + self.jntSuffix + '.rx' <--'lowJaw_dir.ty'          
            cmds.connectAttr(jawCloseTranMult + '.outputX', cheek + '.tz')  #jaw_UDLRIO.tx --> jawClose' + self.jntSuffix + '.tz
            
            if 'l_' in cheek:
                cmds.connectAttr(tySum_cheekIn + '.output2Dx',  cheek_sum + '.input3D[1].input3Dx')
            elif 'r_' in cheek:
                cmds.connectAttr( cheekIn_reverse + '.outputX',  cheek_sum + '.input3D[1].input3Dx')
                
            if '_mid' in cheek:
                cmds.connectAttr(mouthTyMult + '.outputY', cheekRx_addD + '.input2')              
            elif '_lo' in cheek:
                cmds.connectAttr(mouthTyMult + '.outputZ', cheekRx_addD + '.input2')            
            cmds.connectAttr(cheekRx_addD + '.output', cheek + '.rx')  # jawClose' + self.jntSuffix + '.rx <-- jawOpen.ty *(jawOpen_jawCloseRX) 



    
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