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




    def createLipJoint(self, upLow, jawRigPos, lipYPos, poc, lipJotGrp, i):
        """
        """    
        lipJotX  = cmds.group(n = upLow + 'LipJotX' + str(i), em =True, parent = lipJotGrp) 
        lipJotZ  = cmds.group(n = upLow +' LipJotZ' + str(i), em =True, parent = lipJotX) 
       
        lipJotY  = cmds.group(n = upLow +'LipJotY' + str(i), em =True, parent = lipJotZ)     
        lipJot   = cmds.group(n = upLow +'LipJot' + str(i), em =True, parent = lipJotY)
        lipRollJotT = cmds.group(n = upLow +'LipRollJotT' + str(i), em =True, parent = lipJot)
        cmds.setAttr(lipJotY + ".tz", lipYPos[2])
         
        #lip joint placement on the curve with verts tx        
        lipRollJotP = cmds.group(n =upLow + 'LipRollJotP' + str(i), em =True, p = lipRollJotT) 
        pocPosX = cmds.getAttr(poc + '.positionX')
        pocPosY = cmds.getAttr(poc + '.positionY')
        pocPosZ = cmds.getAttr(poc + '.positionZ')
        
        cmds.xform(lipRollJotP, ws = True, t = [ pocPosX, pocPosY, pocPosZ]) 
    
        lipRollJot = cmds.joint(n = upLow + 'LipRollJot' + str(i) + self.jntSuffix, relative = True, p = [ 0, 0, 0]) 
    
    def createDetailCtl(self, updn, i):
        """
        create detail controller in the panel
        """
        detailCtlP = cmds.group(em =True, n = updn  + 'LipDetailP'+ str(i))
        detailCtl = cmds.circle(n = updn  + 'LipDetail' + str(i), ch=False, o =True, nr =(0, 0, 1), r = 0.05)
        cmds.parent(detailCtl[0], detailCtlP)
        cmds.setAttr(detailCtl[0]+"Shape.overrideEnabled", 1)
        cmds.setAttr(detailCtl[0]+"Shape.overrideColor", 20)
        cmds.setAttr(detailCtl[0]+'.translate', 0,0,0)
        cmds.transformLimits(detailCtl[0], tx =(-.5, .5), etx=(True, True))
        cmds.transformLimits(detailCtl[0], ty =(-.5, .5), ety=(True, True))
        attTemp = ['scaleX','scaleY','scaleZ', 'rotateX','rotateY','rotateZ', 'tz', 'visibility' ]  
        for y in attTemp:
            cmds.setAttr(detailCtl[0] +"."+ y, lock = True, keyable = False, channelBox =False)

    def lipCrvToJoint(self):
        """
        connect panel and joints
        """        
        swivelTranXMult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'swivelTranX_mult')
        cmds.connectAttr('Swivel_ctrl.tx', swivelTranXMult + '.input1X')
        cmds.connectAttr('Swivel_ctrl.tx', swivelTranXMult + '.input1Y')
        cmds.connectAttr('Swivel_ctrl.tx', swivelTranXMult + '.input1Z')
        # x:2 = lipJotP.tx / y*0.5 = LipJotX*.ry / z*20 = 'jawSemi.rz'
        cmds.setAttr(swivelTranXMult + '.input2', 2, .5, 20)
        cmds.connectAttr(swivelTranXMult + '.outputX', 'lipJotP.tx')
        cmds.connectAttr(swivelTranXMult + '.outputZ', 'lipJotP.rz')
        
        swivelTranYMult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'swivelTranY_mult')
        cmds.connectAttr('Swivel_ctrl.ty', swivelTranYMult + '.input1X')
        cmds.connectAttr('Swivel_ctrl.ty', swivelTranYMult + '.input1Z')
        cmds.setAttr(swivelTranYMult + '.input2', 2, 0 ,1)
        cmds.connectAttr(swivelTranYMult + '.outputX', 'lipJotP.ty')
        
        # connect the 'jawSemiAdd'        
        jawSemiAddPosMult = cmds.shadingNode ('multiplyDivide', asUtility = 1, n = 'jawSemiAddPos_mult')
        jawSemiAddRotMult = cmds.shadingNode ('multiplyDivide', asUtility = 1, n = 'jawSemiAddRot_mult')
        cmds.connectAttr('jawSemi.translate', jawSemiAddPosMult + '.input1')
        cmds.setAttr(jawSemiAddPosMult + '.input2', .5,.5,.5)
        cmds.connectAttr(jawSemiAddPosMult + '.output', 'jawSemiAdd.translate')
        cmds.connectAttr('jawSemi.rotate', jawSemiAddRotMult + '.input1')
        cmds.setAttr(jawSemiAddRotMult + '.input2', .5,.5,.5)
        cmds.connectAttr(jawSemiAddRotMult + '.output', 'jawSemiAdd.rotate')

        for upLow in self.uplo:        
            #main lipCtrls connect with LipCtl_crv    
            mainCtrlP = cmds.listRelatives(cmds.ls('lip*Ctr*Float', fl=True, type ='transform'), c = 1, type = 'transform')
            lipCtrls = Util.Util.regexMatch('^lip[%s%s].*' %(upLow.upper(), upLow.lower()), mainCtrlP)
            lipCtrls.reverse()
            lipCtrls.insert(0, mainCtrlP[1])
            lipCtrls.insert(len(lipCtrls), mainCtrlP[0])
            
            index = 0
            for n in lipCtrls:
                # curve cv xValue zero out
                zeroX = cmds.shadingNode('addDoubleLinear', asUtility=True, n = upLow + lipCtrls[index].split('Ctrl', 1)[1] + '_xAdd') 
                cvTx = cmds.getAttr(upLow + 'LipCtl' + self.crvSuffix + '.controlPoints['+str(index)+'].xValue') 
                cmds.connectAttr(n+'.tx', zeroX + '.input1')
                cmds.setAttr(zeroX + '.input2' , cvTx)  
                cmds.connectAttr(zeroX + '.output', upLow + 'LipCtl' + self.crvSuffix + '.controlPoints['+str(index)+'].xValue')
                # main ctrl's TY drive the ctrl curve point yValue
                cmds.connectAttr(n+'.ty' , upLow + 'LipCtl' + self.crvSuffix + '.controlPoints['+str(index)+'].yValue')
                index = index +1      
        
            #- main lipRoll Ctrls connect with 'LipRollCtl_crv' /'RollYZCtl_crv'
            mainRollCtrlP = cmds.listRelatives('Lip'+ upLow.title() + 'RollCtrl', ad = 1, type = 'transform')
            lipRollCtls = Util.Util.regexMatch('.*Roll_ctl$', mainRollCtrlP)
            
            #- lipRollCtrl  to 'RollCtl_crv' 
            cmds.connectAttr(lipRollCtls[0]+ '.rz', upLow + 'RollCtl' + self.crvSuffix + '.controlPoints[2].yValue')
            cmds.connectAttr(lipRollCtls[1]+ '.rz', upLow + 'RollCtl' + self.crvSuffix + '.controlPoints[3].yValue') 
            cmds.connectAttr(lipRollCtls[2]+ '.rz', upLow + 'RollCtl' + self.crvSuffix + '.controlPoints[1].yValue')
            
            #- lipRollCtrl  to 'RollYZCtl_crv' 
            cmds.connectAttr(lipRollCtls[0]+ '.ty', upLow + 'RollYZCtl' + self.crvSuffix + '.controlPoints[2].yValue')
            cmds.connectAttr(lipRollCtls[1]+ '.ty', upLow + 'RollYZCtl' + self.crvSuffix + '.controlPoints[3].yValue')
            cmds.connectAttr(lipRollCtls[2]+ '.ty', upLow + 'RollYZCtl' + self.crvSuffix + '.controlPoints[1].yValue')
            cmds.connectAttr(lipRollCtls[0]+ '.tx', upLow + 'RollYZCtl' + self.crvSuffix + '.controlPoints[2].zValue')
            cmds.connectAttr(lipRollCtls[1]+ '.tx', upLow + 'RollYZCtl' + self.crvSuffix + '.controlPoints[3].zValue')
            cmds.connectAttr(lipRollCtls[2]+ '.tx', upLow + 'RollYZCtl' + self.crvSuffix + '.controlPoints[1].zValue') 
     
            # curve's Poc drive the joint
            lipJots= cmds.ls(upLow + 'LipJotX*', fl=True, type ='transform')
            jotNum = len(lipJots)    
            
            if upLow == self.uplo[0]:
                min = 0
                max = jotNum
            elif upLow == self.uplo[1]:  
                jotNum = len(lipJots) + 2 
                min = 1
                max = jotNum-1
            
            for i in range(min, max):  
            
                jotXMult    = cmds.shadingNode('multiplyDivide',   asUtility=True, n = upLow + 'JotXRot' + str(i)+'_mult')
                jotYMult    = cmds.shadingNode('multiplyDivide',   asUtility=True, n = upLow + 'JotYRot' + str(i)+'_mult')
                jotXPosMult = cmds.shadingNode('multiplyDivide',   asUtility=True, n = upLow + 'LipJotXPos' + str(i)+'_mult')
                plusTXAvg   = cmds.shadingNode('plusMinusAverage', asUtility=True, n = upLow + 'TX' + str(i) +'_plus')   
                plusTYAvg   = cmds.shadingNode('plusMinusAverage', asUtility=True, n = upLow + 'TY' + str(i) +'_plus')  
                jotXPosAvg  = cmds.shadingNode('plusMinusAverage', asUtility=True, n = upLow + 'LipJotXPos' + str(i)+'_plus')        
                jotXTYaddD  = cmds.shadingNode('addDoubleLinear',  asUtility=True, n = upLow + 'TY' + str(i) + '_add')
                lipRollMult = cmds.shadingNode('multiplyDivide',   asUtility=True, n = upLow + 'LipRoll' + str(i)+'_mult')
                lipRollAvg  = cmds.shadingNode('plusMinusAverage', asUtility=True, n = upLow + 'LipRoll' + str(i) +'_plus')   
                
                #blinkRemap = cmds.shadingNode('remapValue', asUtility=True, n = jnt.split('Blink', 1)[0] + str(i)+'_remap')
                #blinkGap = cmds.shadingNode('addDoubleLinear', asUtility=True, n = jnt.split('LidBlink', 1)[0] + 'BlinkGap'+str(i)+'_yAdd')
                                
                poc = upLow +'LipCrv' + str(i) + '_poc'
                initialX = cmds.getAttr(poc + '.positionX')
                
                TYpoc = upLow +'LipTY' + str(i) + '_poc'
                initialTYX = cmds.getAttr(TYpoc + '.positionX')
                
                ctlPoc = upLow +'LipCtl' + str(i) + '_poc'
                initialCtlX = cmds.getAttr(ctlPoc + '.positionX')            
                
                rollPoc = upLow +'LipRoll' + str(i) + '_poc'
                rollYZPoc = upLow +'LipRollYZ' + str(i) + '_poc'
                #ty tz = Ucrv.tz + happyCrv.tz + 'LipRoll_poc.positionZ' / rx = Ucrv + 'LipRoll_poc.positionY'
                #lipRoll_crv to lipRoll_joint !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                cmds.setAttr(lipRollAvg + '.operation', 1) 
                cmds.setAttr(lipRollMult + '.input2', 2,2,2)
                cmds.connectAttr(rollPoc + '.positionY', lipRollMult+'.input1X')
                cmds.connectAttr(lipRollMult+'.outputX', upLow + 'LipRollJot'+str(i)+'_jnt.rx') 
                
                cmds.connectAttr(rollYZPoc + '.positionY', lipRollMult+'.input1Y')
                cmds.connectAttr(lipRollMult+'.outputY', upLow + 'LipRollJot'+str(i)+'_jnt.ty')
                
                cmds.connectAttr(rollYZPoc + '.positionZ', lipRollMult+'.input1Z')            
                cmds.connectAttr(lipRollMult+'.outputZ', upLow + 'LipRollJot'+str(i)+'_jnt.tz')
                
                #TranslateX add up for  
                #1. curve translateX add up for LipJotX
                cmds.setAttr(plusTXAvg + '.operation', 1) 
                cmds.connectAttr(poc + '.positionX', plusTXAvg + '.input3D[0].input3Dx') 
                cmds.setAttr(plusTXAvg + '.input3D[1].input3Dx', -initialX) 
                cmds.connectAttr(swivelTranXMult + '.outputY',  plusTXAvg + '.input3D[2].input3Dx')
                cmds.connectAttr(plusTXAvg + '.output3Dx', jotXMult + '.input1X') 
                cmds.setAttr(jotXMult + '.input2X', 30)   
                cmds.connectAttr(jotXMult + '.outputX', upLow + 'LipJotX'+str(i)+'.ry') 
                
                #2. poc positionY,Z sum drive joint("lipJotX") translateY,Z
                cmds.connectAttr(TYpoc + '.positionY',  jotXPosAvg + '.input3D[0].input3Dy')
                cmds.connectAttr(jotXPosAvg + '.output3Dy', jotXPosMult + '.input1Y')
                cmds.setAttr(jotXPosMult + '.input2Y', 5)   
                cmds.connectAttr(jotXPosMult + '.outputY', upLow + 'LipJotX'+str(i)+'.ty')        
                cmds.connectAttr(TYpoc + '.positionZ', jotXPosAvg + '.input3D[0].input3Dz')  
                
                #3. LipCtlCrv Poc.positionX + LipDetail.tx for LipJotY 
                cmds.connectAttr(ctlPoc + '.positionX', plusTXAvg + '.input3D[0].input3Dy')  
                cmds.setAttr(plusTXAvg + '.input3D[1].input3Dy', -initialCtlX)  
                cmds.connectAttr(upLow + 'LipDetail'+ str(i)+'.tx', plusTXAvg + '.input3D[2].input3Dy')             
                cmds.connectAttr(plusTXAvg + '.output3Dy', jotYMult + '.input1Y')          
                cmds.setAttr(jotYMult + '.input2', -30, 30, 30)   
                cmds.connectAttr(jotYMult + '.outputY', upLow+'LipJotY'+str(i)+'.ry') 
                #mouth ctrl to LipJotY rx, ry
                cmds.connectAttr('mouth_move.tx', plusTXAvg + '.input3D[3].input3Dy') 
                cmds.connectAttr('mouth_move.ty', jotYMult + '.input1X')            
                cmds.connectAttr(jotYMult + '.outputX', upLow+'LipJotY'+str(i)+'.rx')             
                
                if i==0 or i==jotNum-1:
                    zeroTip = cmds.shadingNode('addDoubleLinear', asUtility=True, n = 'zeroTip' + str(i) + '_plus')
                    momTY = cmds.getAttr(upLow + 'LipDetailP' + str(i) +'.ty')
                    cmds.connectAttr(ctlPoc + '.positionY', zeroTip + '.input1')
                    cmds.setAttr(zeroTip + '.input2', momTY)
                    cmds.connectAttr(zeroTip + '.output', upLow + 'LipDetailP' +str(i) + '.ty')
                    
                else:
                    #3. LipCtl_crv connect with lipDetailP(lipDetailCtrl parents)
                    cmds.connectAttr(ctlPoc + '.positionY', upLow + 'LipDetailP' +str(i) + '.ty')
                
                # curve translateY add up(joint(LipJotX)"rx" driven by both curves(lipCrv, lipCtlCrv))
                # ty(input3Dy) / extra ty(input3Dx) seperate out for jawSemi
                cmds.setAttr(plusTYAvg + '.operation', 1)
                cmds.connectAttr(poc + '.positionY', plusTYAvg + '.input3D[0].input3Dy')
                cmds.connectAttr(swivelTranYMult + '.outputZ', plusTYAvg + '.input3D[1].input3Dy')
                
                cmds.connectAttr(ctlPoc + '.positionY', plusTYAvg + '.input3D[0].input3Dx') 
                cmds.connectAttr(upLow + 'LipDetail'+ str(i) + '.ty', plusTYAvg + '.input3D[1].input3Dx')
                cmds.connectAttr(plusTYAvg + '.output3Dx', jotXTYaddD+'.input1')
                cmds.connectAttr(plusTYAvg + '.output3Dy', jotXTYaddD+'.input2')
            
                #connect translateY plusAvg to joint rotateX Mult        
                cmds.connectAttr(jotXTYaddD + '.output', jotXMult + '.input1Y')  
                cmds.setAttr(jotXMult + '.input2Y', -20) 
                cmds.connectAttr(jotXMult + '.outputY', upLow + 'LipJotX'+ str(i) + '.rx') 
                
                # joint(LipJotX) translateX driven by poc positionX sum
                cmds.connectAttr(TYpoc + '.positionX', jotXPosAvg + '.input3D[0].input3Dx') 
                cmds.setAttr(jotXPosAvg + '.input3D[1].input3Dx', -initialTYX)
                cmds.connectAttr(jotXPosAvg + '.output3Dx', jotXPosMult + '.input1X')  
                cmds.setAttr(jotXPosMult + '.input2X', 5) 
                cmds.connectAttr(jotXPosMult + '.outputX', upLow + 'LipJotX'+ str(i) + '.tx')
                 
                # joint(LipJotX) translateZ driven by poc positionZ sum
                cmds.connectAttr(poc + '.positionZ', jotXPosAvg + '.input3D[1].input3Dz') 
                cmds.connectAttr(jotXPosAvg + '.output3Dz', jotXPosMult + '.input1Z')  
                cmds.setAttr(jotXPosMult + '.input2Z', 2) 
                cmds.connectAttr(jotXPosMult + '.outputZ', upLow + 'LipJotX'+ str(i) + '.tz')  
                
        #jawSemi movement define
        if not upLow == self.uplo[0]:
            cntTXAvg = 'loTX' + str(jotNum/2) + '_plus' 
            cntTYAvg = 'loTY' + str(jotNum/2) + '_plus'
            jawSemiRotMult = cmds.shadingNode('multiplyDivide', asUtility = 1, n = 'jawSemiRot_mult')        
            cmds.connectAttr(cntTXAvg + '.output3Dx',  jawSemiRotMult + '.input1X')  
            cmds.connectAttr(cntTYAvg + '.output3Dy',  jawSemiRotMult + '.input1Y')
            # jawSemi rotateX move as same as the joint7. rotateX 
            rotXScale = cmds.getAttr(jotXMult + '.input2Y') 
            cmds.setAttr(jawSemiRotMult + '.input2', 10, rotXScale, 0)
            cmds.connectAttr(jawSemiRotMult + '.outputX', 'jawSemi.ry') 
            cmds.connectAttr(jawSemiRotMult + '.outputY', 'jawSemi.rx')           
            # jawSemi rotateZ driven by swivel     
            cmds.connectAttr(swivelTranXMult + '.outputZ', 'jawSemi.rz')
            # jawSemi translate driven by TYcrv / Swivel
            cntPosAvg = 'loLipJotXPos' + str(jotNum/2) + '_plus' 
            jawSemiPosPlus = cmds.shadingNode('plusMinusAverage', asUtility = 1, n = 'jawSemiPos_plus')        
            jawSemiPosMult = cmds.shadingNode('multiplyDivide', asUtility = True, n = 'jawSemiPos_mult')            
            cmds.connectAttr(cntPosAvg + '.output3Dx', jawSemiPosPlus + '.input3D[0].input3Dx')           
            cmds.connectAttr(swivelTranXMult + '.outputX', jawSemiPosPlus + '.input3D[1].input3Dx')
            cmds.connectAttr(cntPosAvg + '.output3Dy', jawSemiPosPlus + '.input3D[0].input3Dy')
    
            #swivel ty   * 1(swivelTranY_mult.outputZ)  jawSemi. ty 
            #, swivel ty   * 1(swivelTranY_mult.outputX)   lipJotP. ty                      
            cmds.connectAttr(swivelTranYMult + '.outputZ', jawSemiPosPlus + '.input3D[1].input3Dy')            
            cmds.connectAttr(jawSemiPosPlus + '.output3Dx',  jawSemiPosMult + '.input1X')     
            cmds.connectAttr(jawSemiPosPlus + '.output3Dy',  jawSemiPosMult + '.input1Y')
            cmds.connectAttr(cntPosAvg + '.output3Dz',  jawSemiPosMult + '.input1Z')
            # jawSemi follow rate = tx: 1.5/2 , ty: move as same as the joint7. translateY
            tranYScale=cmds.getAttr(swivelTranYMult + '.input2X')
            cmds.setAttr(jawSemiPosMult + '.input2', 1.2, tranYScale, 1) 
            cmds.connectAttr(jawSemiPosMult + '.outputX', 'jawSemi.tx') 
            cmds.connectAttr(jawSemiPosMult + '.outputY', 'jawSemi.ty')  
            cmds.connectAttr(jawSemiPosMult + '.outputZ', 'jawSemi.tz') 
            #jawSemi ScaleX driven by jawOpen/ jawSwivel / jawUDLR / E / Happy / Sad
            jawSemiScaleXRemap = cmds.shadingNode('remapValue', asUtility = True, n = 'jawSemiScale_remap')
            jawSemiScalePlus = cmds.shadingNode('plusMinusAverage', asUtility = 1, n = 'jawSemiScale_plus')
            jawScaleDownMult = cmds.shadingNode('multiplyDivide', asUtility = True, n = 'jawScaleDown_mult')  
    
            cmds.setAttr(jawSemiScaleXRemap + ".outputMin", 0.8)
            cmds.setAttr(jawSemiScaleXRemap + ".outputMax", 1.2)
            cmds.setAttr(jawSemiScaleXRemap + ".inputMin", -1)
            cmds.connectAttr(jawSemiScaleXRemap + '.outValue', 'jawSemi.sx') 
            
            cmds.connectAttr('lowJaw_dir.ty', jawScaleDownMult+'.input1X')
            cmds.connectAttr('Swivel_ctrl.ty', jawScaleDownMult+'.input1Y')
            cmds.connectAttr('jaw_UDLR.ty', jawScaleDownMult+'.input1Z')
            cmds.setAttr(jawScaleDownMult+'.input2', .2,.5,.3)
            cmds.connectAttr(jawScaleDownMult + '.outputX', jawSemiScalePlus + '.input1D[0]')
            cmds.connectAttr(jawScaleDownMult + '.outputY', jawSemiScalePlus + '.input1D[1]')
            cmds.connectAttr(jawScaleDownMult + '.outputZ', jawSemiScalePlus + '.input1D[2]')  
            cmds.connectAttr(jawSemiScalePlus + '.output1D', jawSemiScaleXRemap + '.inputValue') 
            
            #lowCheekP follow jawSemi + loCheekCtls
            semiPos = cmds.xform('jawSemi', q= 1, ws = 1, t = 1)
            cmds.xform(self.prefix[0] + 'lowCheek' + self.grpSuffix,\
                       self.prefix[1] + 'lowCheek'  + self.grpSuffix, ws = 1, rotatePivot = semiPos)        
            lowCheekCtl = 'loCheek_ctl'
            
            for lr in self.prefix:
                lowCheekAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = lr + 'lowCheek' + '_plus')
                cmds.connectAttr('jawSemi.tx', lowCheekAvg + '.input3D[0].input3Dx')
                cmds.connectAttr(lr + lowCheekCtl + '.tx', lowCheekAvg + '.input3D[1].input3Dx')
                cmds.connectAttr('jawSemi.ty', lowCheekAvg + '.input3D[0].input3Dy')
                cmds.connectAttr(lr + lowCheekCtl + '.ty', lowCheekAvg + '.input3D[1].input3Dy')
                cmds.connectAttr('jawSemi.tz', lowCheekAvg + '.input3D[0].input3Dz')
                cmds.connectAttr('jawSemi.rotate', lr + 'lowCheek' + self.grpSuffix + '.rotate')
                cmds.connectAttr(lowCheekAvg + '.output3D', lr + 'lowCheek' + self.grpSuffix + '.translate') 


    def indiCrvSetup(self, name, posX, posY, typeAB):
        #select upLip curves that need joints control ('upJawOpen_crv', 'upUDLR_crv'...)  
        crv = self.uplo[0] + name + self.crvSuffix
        loCrv = crv.replace(self.uplo[0], self.uplo[1], 1)
        crvShape = cmds.listRelatives(crv, c= 1, type = 'nurbsCurve')
        crvCVs = cmds.ls(crv + '.cv[*]', fl = 1)
        cvNum = len(crvCVs) 
           
        lipCrvStartPos = cmds.xform (crvCVs[0], q= 1, ws = 1, t = 1)
        lipCrvEndPos = cmds.xform (crvCVs[cvNum-1], q= 1, ws = 1, t = 1)
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
        crvList = cmds.listRelatives('crv' + self.grpSuffix, allDescendents = 1, type = 'transform')
        #??????
        if name in crvList:
            indiCrvs = fnmatch.filter(crvList, '*%s*'% name)
            indiGrp = cmds.group(lipCrvStart, uplipCrvMid, lolipCrvMid, lipCrvEnd, indiCrvs, n = name + '_indiGrp') 
            cmds.parent (indiGrp, 'lipCrv' + self.grpSuffix)
            cmds.setAttr(indiGrp + '.tx', posX)
            cmds.setAttr(indiGrp + '.ty', posY)
            #skinning (cv skin weight input)
            cmds.skinCluster(rCorner, midUpJnt, lCorner, crv, toSelectedBones = 1)    
            cmds.skinCluster(rCorner, midLoJnt, lCorner, loCrv, toSelectedBones = 1)
    
        if type == 'B':
            cornerMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = name +'_mult')
            dampMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = name + 'damp_mult')
            txAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = name + 'TX_plus')  
            
            #?ty? ? ?? ????? inputX,Y?  ??? tx ? tz?  inputZ ? ??.
            txzPick = ['.' + myAttr ]
            cmds.connectAttr(midLoJnt+ '.ty', cornerMult+ '.input1X')  
            cmds.connectAttr(midLoJnt+ '.ty', cornerMult+ '.input1Y')  
            cmds.connectAttr(midLoJnt + txzPick, cornerMult+ '.input1Z') 
            cmds.setAttr(cornerMult + '.input2X', .1) #= lCorner jnts move inside(tx) as jaw open
            cmds.setAttr(cornerMult + '.input2Y', .1) #= rCorner jnts move inside(tx) as jaw open 
            cmds.setAttr(cornerMult + '.input2Z', -.3) #= corner jnts (tx or tz) go along as jaw moving tx
    
            cmds.connectAttr(cornerMult + '.outputX', txAvg + '.input3D[0].input3Dx')
            cmds.connectAttr(cornerMult + '.outputY', txAvg + '.input3D[0].input3Dy')
            cmds.connectAttr(cornerMult + '.outputZ', txAvg + '.input3D[1].input3Dx')
            cmds.connectAttr(cornerMult + '.outputZ', txAvg + '.input3D[1].input3Dy')
            cmds.connectAttr(txAvg + '.output3Dx', lCorner +  txzPick)
            cmds.connectAttr(txAvg + '.output3Dy', rCorner + txzPick)
    
            # lip corners translateY go along with jaw open
            cmds.connectAttr(midLoJnt+ '.ty', dampMult + '.input1X')  
            cmds.connectAttr(midLoJnt+ '.ty', dampMult + '.input1Y')  
            cmds.connectAttr(midLoJnt + txzPick, dampMult + '.input1Z') 
    
            cmds.setAttr(dampMult+ '.input2X', .05) #= ??? ??? ??? ?ty?
            cmds.setAttr(dampMult+ '.input2Y', .35) #= corner jnts ?ty? go along with jaw open
            cmds.setAttr(dampMult+ '.input2Z', .05) #=  ??? ??? ??? ?tx? or ?tz?
    
           
            cmds.connectAttr(dampMult + '.outputX',  midUpJnt+'.ty')
            cmds.connectAttr(dampMult + '.outputY',  lCorner+'.ty')
            cmds.connectAttr(dampMult + '.outputY',  rCorner+'.ty')
            cmds.connectAttr(dampMult + '.outputZ',  midUpJnt + txzPick)

    def indiShapeCrvRig(self, name, posX, posY):
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
        
        lipCrvStart = cmds.group (em = 1, n = name + 'Start' + self.grpSuffix)
        cmds.xform(lipCrvStart, ws = 1, t = lipCrvStartPos)
        upRCorner = cmds.joint(n= 'upRCorner'+ name + self.jntSuffix, p= lipCrvStartPos)
        cmds.select(lipCrvStart, r= 1)
        loRCorner = cmds.joint(n= 'loRCorner'+ name + self.jntSuffix, p= lipCrvStartPos)  
        
        lipCrvMid = cmds.group (em = 1, n = name + 'Mid' + self.grpSuffix) 
        cmds.xform(lipCrvMid, ws = 1, t = list(lipCrvMidPos[0])) 
        midUpJnt = cmds.joint(n = 'cntUp' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0]) 
        cmds.select(lipCrvMid, r= 1) 
        midLoJnt = cmds.joint(n = 'cntLo' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0])
    
        lipCrvEnd = cmds.group (em = 1, n = name + 'End' + self.grpSuffix) 
        cmds.xform(lipCrvEnd, ws = 1, t = lipCrvEndPos) 
        upLCorner = cmds.joint(n= 'upLCorner' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0])
        cmds.select (lipCrvEnd, r = 1)
        loLCorner = cmds.joint(n= 'loLCorner' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0])  
        
        cmds.parent(lipCrvStart, lipCrvMid, lipCrvEnd, name+'Crv_indiGrp') 
        cmds.parent (indiGrp, 'lipCrv' + self.grpSuffix)
        cmds.setAttr(indiGrp + '.tx', posX)
        cmds.setAttr(indiGrp + '.ty', posY)
        #skinning (cv skin weight input)
        cmds.skinCluster(upRCorner, midUpJnt, upLCorner, upLCrv, toSelectedBones = 1)  
        cmds.skinCluster(loRCorner, midLoJnt, loLCorner, loLCrv, toSelectedBones = 1)        

    def rCrvTolCrv(self, lCrv, rCrv, name, pCrvGrp, hideL = False, hideR = False):
        """
        curve grouping
        """
        grpName = name + 'Crv' + self.grpSuffix
        if not cmds.objExists(grpName): 
            crvGrp = cmds.group(n =  grpName, em =True, p = pCrvGrp) 
        cmds.parent(lCrv, rCrv, grpName) 
        cvLs = cmds.ls(lCrv + '.cv[*]', fl = 1)
        cvLen = len(cvLs)
        for x in range(0, cvLen):  
            cmds.connectAttr(lCrv + 'Shape.controlPoints[' + str(x) + ']', rCrv + 'Shape.controlPoints[' + str(x) + ']', f= 1)
        
        if hideL:
            cmds.hide(lCrv)
        
        if hideR:
            cmds.hide(rCrv)
    
    def copyCvWeighs(self):
        """
        copy surface cv's weight to curve's cv
        """
        sel = cmds.ls(sl = True)
        Util.Util.copyCrvSkinWeight(sel[0], sel[1])
        
