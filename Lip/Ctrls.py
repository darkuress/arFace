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
import re

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
        if self.upDown == self.uploPrefix[0]:
            self.__mouthCtlToCrv()
        self.__lipCrvToJoint()

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
            lipPScaleSum = cmds.shadingNode('plusMinusAverage', asUtility= True, n = 'lipPScaleSum')			
            cmds.connectAttr(swivelTranYMult + '.outputY', 'jawSemi.ty')        
            #lipP scale down as lipP/jawSemi goes down
            cmds.setAttr(lipPScaleSum+'.input2D[0].input2Dx', 1)
            cmds.setAttr(lipPScaleSum+'.input2D[0].input2Dy', 1)             
            cmds.connectAttr(self.faceFactors['lip'] + ".swivel_lipJntP_sx", swivelTranYMult + '.input2X')        
            cmds.connectAttr(self.faceFactors['lip'] + ".swivel_lipJntP_sz", swivelTranYMult + '.input2Z')
            cmds.connectAttr(swivelTranYMult + '.outputX', lipPScaleSum+'.input2D[1].input2Dx')
            cmds.connectAttr(swivelTranYMult + '.outputZ', lipPScaleSum+'.input2D[1].input2Dy')
            cmds.connectAttr(lipPScaleSum + '.output2Dx', 'lipJotP.sx')
            cmds.connectAttr(lipPScaleSum + '.output2Dy', 'lipJotP.sz')
            cmds.connectAttr(lipPScaleSum + '.output2Dx', 'jawSemi.sx')
            cmds.connectAttr(lipPScaleSum + '.output2Dy', 'jawSemi.sz')
            
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
        
        #if not cmds.listConnections('jaw_UDLR', d =1):
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
        cmds.connectAttr(UDLRTscaleMult + '.outputX', lipPScaleSum +'.input2D[2].input2Dx')
        cmds.connectAttr(UDLRTscaleMult + '.outputZ', lipPScaleSum +'.input2D[2].input2Dy') 

        # jawClose' + self.jntSuffix + '.ty = UDLR.ty * 2   / jawClose' + self.jntSuffix + '.tz = UDLR.tx * 1.1 	
        cmds.connectAttr('jaw_UDLR.tx', jawCloseTranMult + '.input1X')
        cmds.connectAttr(self.faceFactors['lip'] + '.UDLR_jawCloseTZ', jawCloseTranMult + '.input2X')   	
        cmds.connectAttr(jawCloseTranMult + '.outputX', 'jawClose' + self.jntSuffix + '.tz')     
        
        cmds.connectAttr('jaw_UDLR.ty', jawCloseTranMult + '.input1Y')
        cmds.connectAttr(self.faceFactors['lip'] + '.UDLR_jawCloseTY', jawCloseTranMult + '.input2Y')   	
        cmds.connectAttr(jawCloseTranMult + '.outputY', 'jawClose' + self.jntSuffix + '.ty')
            
        tySumCheekIn = cmds.shadingNode('plusMinusAverage', asUtility = 1, n = 'cheekXIn_sum')
        midCheekMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = "midCheekIn" )
        loCheekMult  = cmds.shadingNode('multiplyDivide', asUtility=True, n = "loCheekIn" )
        
        #- midCheek in plus 
        cmds.connectAttr("lowJaw_dir.ty", midCheekMult +".input1X")
        cmds.connectAttr(self.faceFactors['cheek'] + ".midCheek_in", midCheekMult +".input2X")
        cmds.connectAttr(midCheekMult +".outputX",  tySumCheekIn+".input3D[0].input3Dx")
        cmds.connectAttr("jaw_UDLR.ty", midCheekMult +".input1Y")
        cmds.connectAttr(self.faceFactors['cheek'] + ".midCheek_in", midCheekMult +".input2Y")
        cmds.connectAttr(midCheekMult +".outputY", tySumCheekIn+".input3D[1].input3Dx")
        cmds.connectAttr("swivel_ctrl.ty", midCheekMult +".input1Z")
        cmds.connectAttr(self.faceFactors['cheek'] + ".midCheek_in", midCheekMult +".input2Z")
        cmds.connectAttr(midCheekMult +".outputZ", tySumCheekIn+".input3D[2].input3Dx")

        #- loCheek in plus 
        cmds.connectAttr("lowJaw_dir.ty", loCheekMult +".input1X" )
        cmds.connectAttr(self.faceFactors['cheek'] + ".loCheek_in", loCheekMult +".input2X" )
        cmds.connectAttr(loCheekMult +".outputX",  tySumCheekIn+".input3D[0].input3Dy" )
        cmds.connectAttr("jaw_UDLR.ty", loCheekMult +".input1Y" )
        cmds.connectAttr(self.faceFactors['cheek'] + ".loCheek_in", loCheekMult +".input2Y" )
        cmds.connectAttr(loCheekMult +".outputY", tySumCheekIn+".input3D[1].input3Dy" )
        cmds.connectAttr("swivel_ctrl.ty", loCheekMult +".input1Z" )
        cmds.connectAttr(self.faceFactors['cheek'] + ".loCheek_in", loCheekMult +".input2Z" )
        cmds.connectAttr(loCheekMult +".outputZ", tySumCheekIn+".input3D[2].input3Dy" )

        #- reverse to right side
        cheekInReverse = cmds.shadingNode ('multiplyDivide', asUtility = 1, n = 'cheekTX_reverse')
        cmds.connectAttr(tySumCheekIn + '.output3Dx', cheekInReverse + '.input1X' )
        cmds.connectAttr(tySumCheekIn + '.output3Dy', cheekInReverse + '.input1Y' )
        cmds.setAttr(cheekInReverse + '.input2', -1,-1,-1 )
        
        midCheekRX = [self.prefix[0] + 'midCheekRotX', self.prefix[1] + 'midCheekRotX' ]
        loCheekRX = [self.prefix[0] + 'loCheekRotX', self.prefix[1] + 'loCheekRotX' ]    
        
        for cheek in midCheekRX + loCheekRX:
            cheekSum = cmds.shadingNode ('plusMinusAverage', asUtility= True, n = cheek[ :-4] + '_sum')
            #lowCheekSum = cheek[:2] + "lowCheekMinus"
            lowCheekSum = cmds.shadingNode ('plusMinusAverage', asUtility= True, n = cheek[:2] + "lowCheekMinus")
            cheekRxAddD = cmds.shadingNode ('addDoubleLinear', asUtility= True, n = cheek[ :-4] + '_add')
            cmds.connectAttr(swivelTranXMult + '.outputX', cheekSum + '.input3D[0].input3Dx')
            cmds.connectAttr(cheekSum + '.output3Dx', cheek + '.tx') # swivel.tx        
            cmds.connectAttr(swivelTranYMult + '.outputY', cheekSum + '.input3D[0].input3Dy')
            cmds.connectAttr(jawCloseTranMult + '.outputY', cheekSum + '.input3D[1].input3Dy') #jaw_UDLRIO.ty --> jawClose_jnt.ty 
            cmds.connectAttr(cheekSum + '.output3Dy', cheek + '.ty') # swivel.ty   
            cmds.connectAttr(swivelTranXMult + '.outputY', cheekSum + '.input3D[0].input3Dz')
            cmds.connectAttr(jawCloseRotMult + '.outputY', cheekSum + '.input3D[1].input3Dz') # jawClose_jnt.ry <--jawOpen.tx *(jawOpen_jawCloseRY) 
            cmds.connectAttr(cheekSum + '.output3Dz', cheek + '.ry') # swivel.tx
            cmds.connectAttr(swivelTranXMult + '.outputZ', cheek + '.rz') # swivel.tx
            cmds.connectAttr(jawCloseRotMult + '.outputX', cheekRxAddD + '.input1') #'jawClose_jnt.rx' <--'lowJaw_dir.ty'          
            cmds.connectAttr(jawCloseTranMult + '.outputX', cheek + '.tz')  #jaw_UDLRIO.tx --> jawClose_jnt.tz
            
            if self.prefix[0] + 'mid' in cheek:
                cmds.connectAttr(tySumCheekIn + '.output3Dx',  cheekSum + '.input3D[1].input3Dx')
                cmds.connectAttr(mouthTyMult + '.outputY', cheekRxAddD + '.input2')
                cmds.connectAttr(cheekRxAddD + '.output', cheek + '.rx' )            
            elif self.prefix[1] + 'mid' in cheek:
                cmds.connectAttr(cheekInReverse + '.outputX',  cheekSum + '.input3D[1].input3Dx')
                cmds.connectAttr(mouthTyMult + '.outputY', cheekRxAddD + '.input2')
                cmds.connectAttr(cheekRxAddD + '.output', cheek + '.rx')# jawClose_jnt.rx <-- jawOpen.ty *(jawOpen_jawCloseRX)  
                
            elif self.prefix[0] + 'lo' in cheek:
                cmds.connectAttr(tySumCheekIn + '.output3Dy',  lowCheekSum + '.input3D[4].input3Dx')
            else:
                cmds.connectAttr(cheekInReverse + '.outputY',  lowCheekSum + '.input3D[4].input3Dx')

    def __lipCrvToJoint(self):
        """
        """
        #main lipCtrls connect with LipCtl_crv   
        UD = self.upDown.title()
        lipCtrls=['lip' + UD + 'CtrlRB', 'lip' + UD + 'CtrlRA', 'lip' + UD + 'CtrlMid', 'lip' + UD + 'CtrlLA', 'lip' + UD + 'CtrlLB']
        lipCtrls.insert(0, 'lipCtrlRTip')
        lipCtrls.append('lipCtrlLTip')
        lipCtrlLen = len(lipCtrls)
        
        for x in range( 0, lipCtrlLen):
            # curve cv xValue zero out
            zeroX = cmds.shadingNode('addDoubleLinear', asUtility=True, n = self.upDown + lipCtrls[x].split('Ctrl', 1)[1] + '_xAdd') 
            cvTx = cmds.getAttr(self.upDown + 'LipCtl_crv.controlPoints['+str(x)+'].xValue') 
            cmds.connectAttr(lipCtrls[x] +'.tx', zeroX + '.input1')
            cmds.setAttr(zeroX + '.input2' , cvTx) 
            cmds.connectAttr(zeroX + '.output', self.upDown + 'LipCtl_crv.controlPoints['+str(x)+'].xValue')
            # main ctrl's TY drive the ctrl curve point yValue
            cmds.connectAttr(lipCtrls[x] +'.ty' , self.upDown + 'LipCtl_crv.controlPoints['+str(x)+'].yValue') 
        
        #main lipRoll Ctrls connect with 'LipRollCtl_crv' /'RollYZCtl_crv' 
        mainRollCtrlP = cmds.listRelatives('Lip'+ self.upDown.title() + 'RollCtrl', ad =1, type = 'transform')
        regex = re.compile(r'Roll_ctl')
        lipRollCtls = []
        for x in mainRollCtrlP:        
            if re.search(regex, x):
                lipRollCtls.append(x)
                
        rollCtlDict = { 0:2, 1:3, 2:1 }
        for q, p in rollCtlDict.items(): 
            # lipRollCtrl  to 'RollCtl_crv' 
            cmds.connectAttr(lipRollCtls[q]+ '.rz', self.upDown + 'LipRoll_crv.controlPoints[%s].yValue'%p) 
            # lipRollCtrl  to 'RollYZCtl_crv' 
            cmds.connectAttr(lipRollCtls[q]+ '.ty', self.upDown + 'RollYZ_crv.controlPoints[%s].yValue'%p)
            cmds.connectAttr(lipRollCtls[q]+ '.tx', self.upDown + 'RollYZ_crv.controlPoints[%s].zValue'%p)
        
        # curve's Poc drive the joint
        lipJots= cmds.ls(self.upDown + 'LipJotX*', fl=True, type ='transform')
        jotNum = len(lipJots)
          
        if self.upDown == 'up':
            min = 0
            max = jotNum
        elif self.upDown == 'lo':  
            min = 1
            max = jotNum+1
            
        for i in range(min, max):
            jotXMult     = cmds.shadingNode('multiplyDivide',   asUtility=True, n = self.upDown + 'JotXRot' + str(i)+'_mult')
            jotX_AddD    = cmds.shadingNode('addDoubleLinear',  asUtility=True, n = self.upDown + 'JotXRY' + str(i) + '_add')
            jntYMult     = cmds.shadingNode('multiplyDivide',   asUtility=True, n = self.upDown + 'JotYRot' + str(i)+'_mult')
            jntY_AddD    = cmds.shadingNode('addDoubleLinear',  asUtility=True, n = self.upDown + 'JotYRZ' + str(i) + '_add')
            mouthTX_AddD = cmds.shadingNode('addDoubleLinear',  asUtility=True, n = self.upDown + 'MouthTX' + str(i) + '_add')
            mouthTY_AddD = cmds.shadingNode('addDoubleLinear',  asUtility=True, n = self.upDown + 'MouthTY' + str(i) + '_add')
            jotXPosMult  = cmds.shadingNode('multiplyDivide',   asUtility=True, n = self.upDown + 'LipJotXPos' + str(i)+'_mult')
            plusTXAvg    = cmds.shadingNode('plusMinusAverage', asUtility=True, n = self.upDown + 'TX' + str(i) +'_plus')   
            plusTYAvg    = cmds.shadingNode('plusMinusAverage', asUtility=True, n = self.upDown + 'TY' + str(i) +'_plus')  
            jotXPosAvg   = cmds.shadingNode('plusMinusAverage', asUtility=True, n = self.upDown + 'LipJotXPos' + str(i)+'_plus')        
            jotX_rzAddD  = cmds.shadingNode('addDoubleLinear',  asUtility=True, n = self.upDown + 'RZ' + str(i) + '_add')
            rollYZMult   = cmds.shadingNode('multiplyDivide',   asUtility=True, n = self.upDown + 'RollYZ' + str(i)+'_mult')
            poc = self.upDown +'LipCrv' + str(i) + '_poc'
            initialX = cmds.getAttr(poc + '.positionX')
            
            TYpoc = self.upDown +'LipTy' + str(i) + '_poc'
            initialTYX = cmds.getAttr(TYpoc + '.positionX')
            
            ctlPoc = self.upDown +'LipCtl' + str(i) + '_poc'
            initialCtlX = cmds.getAttr(ctlPoc + '.positionX')
            
            lipRollPoc = self.upDown +'LipRoll' + str(i) + '_poc'
            rollYZPoc = self.upDown +'LipRollYZ' + str(i) + '_poc'     
            
            if i==0 or i==jotNum-1:
                zeroTip = cmds.shadingNode('addDoubleLinear', asUtility=True, n = 'zeroTip' + str(i) + '_plus')
                momTY = cmds.getAttr(self.upDown + 'LipDetailP' + str(i) +'.ty')
                cmds.connectAttr(ctlPoc + '.positionY', zeroTip + '.input1' )
                cmds.setAttr(zeroTip + '.input2', momTY)
                cmds.connectAttr(zeroTip + '.output', self.upDown + 'LipDetailP' +str(i) + '.ty')
                
            else:
                # LipCtl_crv connect with lipDetailP(lipDetailCtrl parents)
                cmds.connectAttr(ctlPoc + '.positionY', self.upDown + 'LipDetailP' +str(i) + '.ty')        
            
            #TranslateX add up for        
            #1. curve translateX add up for LipJotX       swivelTranX_mult.outputY - ry
            swivelTranXMult = 'swivelTranX_mult'
            swivelTranYMult = 'swivelTranY_mult'
            mouthTxMult = 'mouthTranX_mult'
            mouthTyMult = 'mouthTranY_mult'
            
            cmds.connectAttr(poc + '.positionX', plusTXAvg + '.input3D[0].input3Dx') 
            cmds.setAttr(plusTXAvg + '.input3D[1].input3Dx', -initialX) 
            #swivel.tx --> not lipJotX.tx but lipJotP.tx   
            cmds.connectAttr(plusTXAvg + '.output3Dx', jotXMult + '.input1X') 
            cmds.connectAttr(self.faceFactors['lip'] + '.txSum_lipJntX_ry', jotXMult + '.input2X')       
            cmds.connectAttr(jotXMult + '.outputX', jotX_AddD + '.input1')
            cmds.connectAttr(swivelTranXMult + '.outputY', jotX_AddD + '.input2')
            cmds.connectAttr(jotX_AddD + '.output', self.upDown + 'LipJotX'+str(i)+'.ry') 
            
            #swivel.tx / rz --> lipJotX.rz        
            cmds.connectAttr('swivel_ctrl.rz',  jotX_rzAddD+ '.input1') 
            cmds.connectAttr(swivelTranXMult + '.outputZ', jotX_rzAddD + '.input2') 
            cmds.connectAttr(jotX_rzAddD + '.output', self.upDown + 'LipJotX'+str(i)+'.rz')
            
            # curve translateY add up(joint(LipJotX)"rx" driven by both curves(lipCrv, lipCtlCrv))
            # ty(input3Dy) / extra ty(input3Dx) seperate out for jawSemi
           
            cmds.setAttr(plusTYAvg + '.operation', 1)
            cmds.connectAttr(poc + '.positionY', plusTYAvg + '.input1D[0]')
            cmds.connectAttr(ctlPoc + '.positionY', plusTYAvg + '.input1D[1]') 
            cmds.connectAttr(self.upDown + 'LipDetail'+ str(i) + '.ty', plusTYAvg + '.input1D[2]')    
            #connect translateY plusAvg to joint rotateX Mult        
            cmds.connectAttr(plusTYAvg + '.output1D', jotXMult + '.input1Y')  
            cmds.connectAttr(self.faceFactors['lip'] + '.tySum_lipJntX_rx', jotXMult + '.input2Y') 
            cmds.connectAttr(jotXMult + '.outputY', mouthTY_AddD + '.input1')
            cmds.connectAttr(mouthTyMult + '.outputX', mouthTY_AddD + '.input2')  
            cmds.connectAttr(mouthTY_AddD + '.output', self.upDown + 'LipJotX'+ str(i) + '.rx')   
            
            #joint(LipJotX) translateX driven by poc positionX sum
            cmds.connectAttr(TYpoc + '.positionX', jotXPosAvg + '.input3D[0].input3Dx') 
            cmds.setAttr(jotXPosAvg + '.input3D[1].input3Dx', -initialTYX)        
            cmds.connectAttr(jotXPosAvg + '.output3Dx', jotXPosMult + '.input1X')  
            cmds.connectAttr(self.faceFactors['lip'] + '.txSum_lipJntX_tx', jotXPosMult + '.input2X') 
            cmds.connectAttr(jotXPosMult + '.outputX', self.upDown + 'LipJotX'+ str(i) + '.tx')
             
            #2. poc positionY,Z sum drive joint("lipJotX") translateY,Z
            cmds.connectAttr(TYpoc + '.positionY',  jotXPosAvg + '.input3D[0].input3Dy')
            
            cmds.connectAttr(jotXPosAvg + '.output3Dy', jotXPosMult + '.input1Y')
            cmds.connectAttr(self.faceFactors['lip'] + '.tySum_lipJntX_ty', jotXPosMult + '.input2Y')  
            cmds.connectAttr(jotXPosMult + '.outputY', self.upDown + 'LipJotX'+str(i)+'.ty')     
            
            # joint(LipJotX) translateZ driven by poc positionZ sum
            cmds.connectAttr(TYpoc + '.positionZ', jotXPosAvg + '.input3D[0].input3Dz')
            cmds.connectAttr(poc + '.positionZ', jotXPosAvg + '.input3D[1].input3Dz') 
            cmds.connectAttr(rollYZPoc + '.positionZ', jotXPosAvg + '.input3D[2].input3Dz') 
            cmds.connectAttr(jotXPosAvg + '.output3Dz', jotXPosMult + '.input1Z')
            cmds.connectAttr(self.faceFactors['lip'] + '.tzSum_lipJntX_tz', jotXPosMult + '.input2Z') 
            cmds.connectAttr(jotXPosMult + '.outputZ', self.upDown + 'LipJotX'+ str(i) + '.tz')          
            
            #3. LipCtlCrv Poc.positionX + LipDetail.tx for LipJotY 
            # mouth_move.tx --> lipJotY0.ry .rz /mouth_move.rz --> lipJotY0.rz
            cmds.connectAttr(ctlPoc + '.positionX', plusTXAvg + '.input3D[0].input3Dy')  
            cmds.setAttr(plusTXAvg + '.input3D[1].input3Dy', -initialCtlX)  
            cmds.connectAttr(self.upDown + 'LipDetail'+ str(i)+'.tx', plusTXAvg + '.input3D[2].input3Dy')
            cmds.connectAttr(plusTXAvg + '.output3Dy', jntYMult + '.input1Y')          
            cmds.connectAttr(self.faceFactors['lip'] + '.txSum_lipJntY_ry', jntYMult + '.input2Y')   
            cmds.connectAttr(jntYMult + '.outputY', mouthTX_AddD+ '.input1')
            cmds.connectAttr(mouthTxMult + '.outputX', mouthTX_AddD+ '.input2')  
            cmds.connectAttr(mouthTX_AddD+ '.output', self.upDown+'LipJotY'+str(i)+'.ry') 
           
            cmds.connectAttr('mouth_move.rz', jntY_AddD + '.input1')          
            cmds.connectAttr(mouthTxMult + '.outputZ', jntY_AddD + '.input2')   
            cmds.connectAttr(jntY_AddD + '.output', self.upDown+'LipJotY'+str(i)+'.rz') 
            
            #lipRollYZCrv --> lipRollJotT* .ty / tz
            cmds.connectAttr(rollYZPoc + '.positionY', rollYZMult + '.input1Y')
            cmds.connectAttr(self.faceFactors['lip'] + '.YZPoc_rollJntT_ty', rollYZMult + '.input2Y') 
            cmds.connectAttr(rollYZMult + '.outputY', self.upDown+'LipRollJotT'+str(i)+'.ty')
            
            cmds.connectAttr(rollYZPoc + '.positionZ', rollYZMult + '.input1Z')
            cmds.connectAttr(self.faceFactors['lip'] + '.YZPoc_rollJntT_tz', rollYZMult + '.input2Z') 
            cmds.connectAttr(rollYZMult + '.outputZ', self.upDown+'LipRollJotT' + str(i)+'.tz')
            
            #lipRollCrv --> lipRollJot*_jnt 
            cmds.connectAttr(lipRollPoc + '.positionY', self.upDown+'LipRollJot' + str(i) + self.jntSuffix + '.rx')
