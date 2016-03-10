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

class Func(Base.Base):
    def __init__(self, **kw):
        """
        initializing variables
        """
        #local variables
        Base.Base.__init__(self, **kw)


    def createLipJoint(self, upLow, jawRigPos, lipYPos, poc, lipJotGrp, i):
        """
        """    
        lipJotX  = cmds.group( n = upLow + 'LipJotX' + str(i), em =True, parent = lipJotGrp) 
        lipJotZ  = cmds.group( n = upLow +' LipJotZ' + str(i), em =True, parent = lipJotX) 
       
        lipJotY  = cmds.group( n = upLow +'LipJotY' + str(i), em =True, parent = lipJotZ)     
        lipJot = cmds.group( n = upLow +'LipJot' + str(i), em =True, parent = lipJotY)
        lipRollJotT = cmds.group( n = upLow +'LipRollJotT' + str(i), em =True, parent = lipJot)
        cmds.setAttr(lipJotY + ".tz", lipYPos[2])
         
        #lip joint placement on the curve with verts tx        
        lipRollJotP = cmds.group( n =upLow + 'LipRollJotP' + str(i), em =True, p = lipRollJotT) 
        pocPosX = cmds.getAttr(poc + '.positionX')
        pocPosY = cmds.getAttr(poc + '.positionY')
        pocPosZ = cmds.getAttr(poc + '.positionZ')
        
        cmds.xform(lipRollJotP, ws = True, t = [ pocPosX, pocPosY, pocPosZ]) 
    
        lipRollJot = cmds.joint(n = upLow + 'lipRollJot' + str(i) + '_jnt', relative = True, p = [ 0, 0, 0]) 
    
    def createDetailCtl(self, updn, i):
        """
        create detail controller in the panel
        """
        detailCtlP = cmds.group(em =True, n = updn  + 'LipDetailP'+ str(i))
        detailCtl = cmds.circle(n = updn  + 'LipDetail' + str(i), ch=False, o =True, nr =(0, 0, 1), r = 0.05 )
        cmds.parent(detailCtl[0], detailCtlP)
        cmds.setAttr(detailCtl[0]+"Shape.overrideEnabled", 1)
        cmds.setAttr( detailCtl[0]+"Shape.overrideColor", 20)
        cmds.setAttr(detailCtl[0]+'.translate', 0,0,0)
        cmds.transformLimits(detailCtl[0], tx =(-.5, .5), etx=( True, True))
        cmds.transformLimits(detailCtl[0], ty =(-.5, .5), ety=( True, True))
        attTemp = ['scaleX','scaleY','scaleZ', 'rotateX','rotateY','rotateZ', 'tz', 'visibility' ]  
        for y in attTemp:
            cmds.setAttr(detailCtl[0] +"."+ y, lock = True, keyable = False, channelBox =False)

    def lipCrvToJoint(self, upLow, rotateScale):
        """
        connect panel and joints
        """        
        #- main lipCtrls connect with LipCtl_crv    
        mainCtrlP = cmds.listRelatives(cmds.ls('lip*Ctr*Float', fl=True, type ='transform'), c =1, type = 'transform')
        lipCtrls = [x for x in mainCtrlP if upLow.title() in x]
        lipCtrls.reverse()
        lipCtrls.insert(0, mainCtrlP[1])
        lipCtrls.insert(len(lipCtrls), mainCtrlP[0])
        
        index = 0
        for n in lipCtrls:
            #- curve cv xValue zero out
            zeroX = cmds.shadingNode('addDoubleLinear', asUtility=True, n = upLow + lipCtrls[index].split('Ctrl', 1)[1] + '_xAdd') 
            cvTx = cmds.getAttr(upLow + 'LipCtl_crv.controlPoints['+str(index)+'].xValue')
            cmds.connectAttr(n+'.tx', zeroX + '.input1')
            cmds.setAttr (zeroX + '.input2' , cvTx) 
            cmds.connectAttr(zeroX + '.output', upLow + 'LipCtl_crv.controlPoints['+str(index)+'].xValue')
            #- main ctrl's TY drive the ctrl curve point yValue
            cmds.connectAttr(n+'.ty' , upLow + 'LipCtl_crv.controlPoints['+str(index)+'].yValue')
            index = index +1  
        
        #- curve's Poc drive the joint
        lipJots= cmds.ls(upLow + 'LipJotX*', fl=True, type ='transform')
        jotNum = len (lipJots)
        
        if upLow == self.uplo[0]:
            min = 0
            max = jotNum
        elif upLow == self.uplo[1]:  
            jotNum = len (lipJots) + 2 
            min = 1
            max = jotNum-1
        
        for i in range(min, max):  
        
            jotXMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = upLow + 'lipJotX' + str(i)+'_mult')
            jotYMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = upLow + 'lipJotY' + str(i)+'_mult')
            plusTXAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = upLow + 'TX' + str(i) +'_plus')    
            plusTYAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = upLow + 'TY' + str(i)+'_plus')
          
            #blinkRemap = cmds.shadingNode('remapValue', asUtility=True, n = jnt.split('Blink', 1)[0] + str(i)+'_remap')
            #blinkGap = cmds.shadingNode('addDoubleLinear', asUtility=True, n = jnt.split('LidBlink', 1)[0] + 'BlinkGap'+str(i)+'_yAdd')
                            
            poc = upLow +'LipCrv' + str(i) + '_poc'
            initialX = cmds.getAttr(poc + '.positionX')
            
            ctlPoc = upLow +'LipCtl' + str(i) + '_poc'
            initialCtlX = cmds.getAttr(ctlPoc + '.positionX')            
            
            #- TranslateX add up for  
            #- 1. curve translateX add up for LipJotX
            cmds.setAttr(plusTXAvg + '.operation', 1) 
            cmds.connectAttr(poc + '.positionX', plusTXAvg + '.input3D[0].input3Dx') 
            cmds.setAttr (plusTXAvg + '.input3D[1].input3Dx', -initialX) 
            cmds.connectAttr(plusTXAvg + '.output3Dx', jotXMult + '.input1X') 
            cmds.setAttr(jotXMult + '.input2X', rotateScale)   
            cmds.connectAttr(jotXMult + '.outputX', upLow + 'LipJotX'+str(i)+'.ry') 
            
            #- 2. LipCtlCrv Poc.positionX + LipDetail.tx for LipJotY 
            cmds.connectAttr(ctlPoc + '.positionX', plusTXAvg + '.input3D[0].input3Dy')  
            cmds.setAttr(plusTXAvg + '.input3D[1].input3Dy', -initialCtlX)  
            cmds.connectAttr(upLow + 'LipDetail'+ str(i)+'.tx', plusTXAvg + '.input3D[2].input3Dy')  
            cmds.connectAttr(plusTXAvg + '.output3Dy', jotYMult + '.input1Y')          
            cmds.setAttr(jotYMult + '.input2Y', rotateScale)   
            cmds.connectAttr(jotYMult + '.outputY', upLow+'LipJotY'+str(i)+'.ry') 
            
            if i==0 or i==jotNum-1:
                zeroTip = cmds.shadingNode('addDoubleLinear', asUtility=True, n = 'zeroTip' + str(i) + '_plus')
                momTY = cmds.getAttr(upLow + 'LipDetailP' + str(i) +'.ty')
                cmds.connectAttr(ctlPoc + '.positionY', zeroTip + '.input1' )
                cmds.setAttr(zeroTip + '.input2', momTY)
                cmds.connectAttr(zeroTip + '.output', upLow + 'LipDetailP' +str(i) + '.ty')
                
            else:
                #- 3. LipCtl_crv connect with lipDetailP (lipDetailCtrl parents)
                cmds.connectAttr(ctlPoc + '.positionY', upLow + 'LipDetailP' +str(i) + '.ty')
            
            #- TranslateY add up
            #- 1. curve translateY add up 
            cmds.setAttr(plusTYAvg + '.operation', 1)
            cmds.connectAttr(poc + '.positionY', plusTYAvg + '.input1D[0]')
            cmds.connectAttr(ctlPoc + '.positionY', plusTYAvg + '.input1D[1]') 
            cmds.connectAttr(upLow + 'LipDetail'+ str(i) + '.ty', plusTYAvg + '.input1D[2]')
        
            #- connect translateY plusAvg to joint rotateX Mult
            
            cmds.connectAttr(plusTYAvg + '.output1D', jotXMult + '.input1Y')  
            cmds.setAttr(jotXMult + '.input2Y', -rotateScale) 
            cmds.connectAttr(jotXMult + '.outputY', upLow + 'LipJotX'+ str(i) + '.rx')  
            
            cmds.connectAttr(poc + '.positionZ', jotXMult + '.input1Z')  
            cmds.setAttr(jotXMult + '.input2Z', rotateScale) 
            cmds.connectAttr(jotXMult + '.outputZ', upLow + 'LipJotX'+ str(i) + '.tz')
    
    def copyCvWeighs(self):
        """
        copy surface cv's weight to curve's cv
        """
        sel = cmds.ls(sl = True)
        self.copyCrvSkinWeight(sel[0], sel[1])