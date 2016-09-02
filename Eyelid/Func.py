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
        self.lrUplow = []
        for lr in self.prefix:
            self.lrUplow.append(lr + self.uploPrefix[0])
            self.lrUplow.append(lr + self.uploPrefix[1])
    
    #- new
    def jumperPanel(self):
        """
        """
        jumperPanel = 'jumperPanel'
        if not cmds.objExists(jumperPanel):
            #set the start with plusMinusAverage  
            cmds.group(n = "jumperPanel", em = 1, p = self.faceMainNode)   
        else:
            return
        if not cmds.objExists('lids_EXP'):
            #set the start with plusMinusAverage
            
            cmds.group(n = "lids_EXP", em = 1, p = "jumperPanel")    
        upJnts = cmds.ls(self.prefix[0] + "upLidBlink*" + self.jntSuffix, fl =1, type= "joint")
        loJnts = cmds.ls(self.prefix[0] + "loLidBlink*" + self.jntSuffix, fl =1, type= "joint")
        upLen = len(upJnts)    
        loLen = len(loJnts)
        cmds.select('lids_EXP') #lids_EXP: lid start/ end /open 
        #nodes for ValAB
        
        pushY_mult = cmds.shadingNode('multiplyDivide', asUtility =1, n ='lidPushY_mult')
    
        for LR in self.prefix:    
            if LR == self.prefix[0]:
                XYZ = 'X'
    
            if LR == self.prefix[1]:
                XYZ = 'Y' 
             
            for i in range(0, max(upLen, loLen)): 
                #create each push_lid point in jumperPanel
                cmds.addAttr(jumperPanel, longName= LR + "upPush_Lid%s"%str(i), attributeType='float', dv = 0)
                cmds.addAttr(jumperPanel, longName= LR + "loPush_Lid%s"%str(i), attributeType='float', dv = 0)
                
                #Start = - .cv(LUpCrv.cv) -   +  push_Lid5 + ctrl.ty* *  .squint
                cmds.addAttr('lids_EXP', longName= LR + "upEyeStart%s"%str(i), attributeType='float', dv = 0)
                ##eyeOpenCrv shape(start + blinkCtrl) : upEyeStart0 -lids_EXP.l_upGap*l_eyeBlink.ty*(1-blinkLevel)
                cmds.addAttr('lids_EXP', longName= LR +"upEyeOpen%s"%str(i), attributeType='float', dv = 0)
                #blink target POC.positionY on the loEyeCrv
                cmds.addAttr('lids_EXP', longName= LR +"EyeEnd%s"%str(i), attributeType='float', dv = 0)
            
                cmds.addAttr('lids_EXP', longName= LR +"loEyeStart%s"%str(i), attributeType='float', dv = 0)
                cmds.addAttr('lids_EXP', longName= LR +"loEyeOpen%s"%str(i), attributeType='float', dv = 0)
                 
            #Y = lookUp/Down  X = lookLeft/Right           
            cmds.addAttr(jumperPanel, longName= LR + "lidPushY", attributeType='float', dv = 0)                      
            cmds.addAttr(jumperPanel, longName= LR + "lidPushX", attributeType='float', dv = 0) 
            
            cmds.addAttr(jumperPanel, longName= LR + "valA", attributeType='float', dv = 0)
            cmds.addAttr(jumperPanel, longName= LR + "valB", attributeType='float', dv = 0)
            
            
            #make -JumperPanel.l_lidPushY into +
            cmds.connectAttr('jumperPanel.' + LR + 'lidPushY', pushY_mult + '.input1'+XYZ)
            cmds.setAttr(pushY_mult + '.input2'+XYZ, -1)
            
            #ValA and ValB define by LidPushY clamp
            pushY_clamp = cmds.shadingNode('clamp', asUtility =1, n = LR + 'lidPushY_clamp')
            cmds.setAttr(pushY_clamp + '.maxR', 1)
            cmds.setAttr(pushY_clamp + '.maxG', 1)
            #ValAB / LidPushY defined by l_eyeballRotX 
            cmds.connectAttr('jumperPanel.' + LR + 'lidPushY', pushY_clamp + '.inputR')
            cmds.connectAttr(pushY_mult + '.output'+XYZ, pushY_clamp + '.inputG')
            cmds.connectAttr(pushY_clamp + '.outputR', 'jumperPanel.' + LR + 'valA') # l_valA = + lidPushY
            cmds.connectAttr(pushY_clamp + '.outputG', 'jumperPanel.' + LR + 'valB')# l_valB = -(-lidPushY)        
            
            #l_eyeballRotX --> 'jumperPanel.l_lidPushY'
            
            eyeRotX_mult = cmds.shadingNode('multiplyDivide', asUtility =1, n = LR + 'eyeRotX_mult')
            rotX_invert = cmds.shadingNode('multiplyDivide', asUtility =1, n = LR + 'rotX_invert')
            cmds.connectAttr(self.faceFactors['eyelid'] + '.eyeBallRotX_scale', rotX_invert + '.input1X')
            cmds.setAttr(rotX_invert + '.input2X', -1)
            
            cmds.setAttr(eyeRotX_mult + '.operation', 2)
            cmds.connectAttr(LR + 'eyeballRot.rotateX', eyeRotX_mult + '.input1X')
            cmds.connectAttr(rotX_invert + '.outputX', eyeRotX_mult + '.input2X')
            
            eyeUD_mult = cmds.shadingNode('multiplyDivide', asUtility =1, n = LR + 'eyeUD_mult')
            cmds.connectAttr(eyeRotX_mult + '.outputX', eyeUD_mult + '.input1X')
            cmds.connectAttr(eyeRotX_mult + '.outputX', eyeUD_mult + '.input1Y')
            cmds.connectAttr(self.faceFactors['eyelid'] + '.range_'+LR+'eyeU', eyeUD_mult + '.input2X')
            cmds.connectAttr(self.faceFactors['eyelid'] + '.range_'+LR+'eyeD', eyeUD_mult + '.input2Y')
            
            pushY_con = cmds.shadingNode('condition', asUtility =1, n = LR + 'lidPushY_con')
            cmds.connectAttr(LR + 'eyeballRot.rotateX', pushY_con+'.firstTerm')
            cmds.setAttr(pushY_con+".secondTerm", 0)
            cmds.setAttr(pushY_con+".operation", 4)
            cmds.connectAttr(eyeUD_mult + '.outputX', pushY_con+ '.colorIfTrueR')
            cmds.connectAttr(eyeUD_mult + '.outputY', pushY_con+ '.colorIfFalseR')
            cmds.connectAttr(pushY_con+ '.outColorR', 'jumperPanel.' +LR+ 'lidPushY')
            
            #l_eyeballRotY --> 'jumperPanel.l_lidPushX'
            eyeRotY_mult = cmds.shadingNode('multiplyDivide', asUtility =1, n = LR + 'eyeRotY_mult')
            cmds.setAttr(eyeRotY_mult + '.operation', 2)
            cmds.connectAttr(self.faceFactors['eyelid'] + '.eyeBallRotY_scale', eyeRotY_mult + '.input2X')
            cmds.connectAttr(self.faceFactors['eyelid'] + '.eyeBallRotY_scale', eyeRotY_mult + '.input2Y')
            cmds.connectAttr(LR + 'eyeballRot.rotateY', eyeRotY_mult + '.input1X')
            cmds.connectAttr(LR + 'eyeballRot.rotateY', eyeRotY_mult + '.input1Y')
            
            eyeLR_mult = cmds.shadingNode('multiplyDivide', asUtility =1, n = LR + 'eyeLR_mult')
            cmds.connectAttr(eyeRotY_mult + '.outputX', eyeLR_mult + '.input1X')
            cmds.connectAttr(eyeRotY_mult + '.outputX', eyeLR_mult + '.input1Y')
            cmds.connectAttr(self.faceFactors['eyelid'] + '.range_'+LR+'eyeR', eyeLR_mult + '.input2X')
            cmds.connectAttr(self.faceFactors['eyelid'] + '.range_'+LR+'eyeL', eyeLR_mult + '.input2Y')
            
            pushX_con = cmds.shadingNode('condition', asUtility =1, n = LR + 'lidPushX_con')
            cmds.connectAttr(LR + 'eyeballRot.rotateY', pushX_con +'.firstTerm')
            cmds.setAttr(pushY_con+".secondTerm", 0)
            cmds.setAttr(pushY_con+".operation", 4)
            cmds.connectAttr(eyeLR_mult + '.outputX', pushX_con+ '.colorIfTrueG')
            cmds.connectAttr(eyeLR_mult + '.outputY', pushX_con+ '.colorIfFalseG')
            cmds.connectAttr(pushX_con+ '.outColorG', 'jumperPanel.' +LR+ 'lidPushX') 
    
        return jumperPanel

    def eyeCtlExp(self):
        """
        """
        for LR in self.prefix:
            #blink setup               
            blinkClamp = cmds.shadingNode("clamp", asUtility =1, n = LR+'blink_clamp')
            blinkMinus = cmds.shadingNode('multiplyDivide', asUtility=True, n = LR + 'blinkMinus_mult')    
            #up lid clamp seperate condition node (blinkCon +'.outColorR' : open(+)/blink (-))
            # eyeBlinkCtl open
            cmds.connectAttr(LR + "eyeBlink.ty", blinkClamp + '.inputR') 
            cmds.setAttr(blinkClamp + '.maxR', 1)
            cmds.connectAttr(LR + "eyeBlink.ty", blinkMinus + '.input1Y') 
            cmds.setAttr(blinkMinus + '.input2Y', -1)
            #eyeBlinkCtl blink
            cmds.connectAttr(blinkMinus + '.outputY', blinkClamp + '.inputG')
            cmds.setAttr(blinkClamp + '.maxG', 1)
            '''#openInvert for loOpen
            cmds.connectAttr(blinkClamp + '.outputR', blinkMinus + '.input1Z')
            cmds.setAttr(blinkMinus + '.input2Z', -1)'''
           
            #eyeDirections
            eyeBallMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = LR + 'eyeBall_mult')
            #eyeBall rotX (up/down)
            cmds.connectAttr(LR + "eyeCtl.ty", eyeBallMult + '.input1Y')
            cmds.connectAttr(self.faceFactors['eyelid'] + '.eyeBallRotX_scale', blinkMinus + '.input1X')
            cmds.setAttr(blinkMinus + '.input2X', -1 )
            cmds.connectAttr(blinkMinus + '.outputX', eyeBallMult + '.input2Y')
            cmds.connectAttr(eyeBallMult + '.outputY', LR + 'eyeballRot.rx')
            #eyeBall rotY (left/rigt)
            cmds.connectAttr(LR + "eyeCtl.tx", eyeBallMult + '.input1X')
            cmds.connectAttr(self.faceFactors['eyelid'] + '.eyeBallRotY_scale', eyeBallMult + '.input2X')
            cmds.connectAttr(eyeBallMult + '.outputX', LR + 'eyeballRot.ry') 
                       
            #squint setup
            squintInvert = cmds.shadingNode ('multiplyDivide', asUtility =1, n = LR+'squintInvert_mult')             
            cmds.connectAttr(LR+'eyeSquint.translateX', squintInvert + '.input1X')
            cmds.connectAttr(LR+'eyeSquint.translateY', squintInvert + '.input1Y')
            cmds.setAttr(squintInvert + '.input2X', -1)
            cmds.setAttr(squintInvert + '.input2Y', -1)
            #annoy : -squint ctrl
            annoyRemap = cmds.shadingNode ('remapValue', asUtility =1, n = LR +'annoy_remap')
            cmds.connectAttr(squintInvert + '.outputY', annoyRemap + '.inputValue')
            cmds.connectAttr(squintInvert + '.outputX', annoyRemap + '.inputMin')
            #squint : +squint ctrl
            squintRemap = cmds.shadingNode ('remapValue', asUtility =1, n = LR+'squint_remap')
            cmds.connectAttr(LR+'eyeSquint.translateY', squintRemap + '.inputValue')
            cmds.connectAttr(squintInvert + '.outputX', squintRemap + '.inputMin')
           
            #eyeTwist setup    
            #connect lidTwist ctrl to corner jnt
            inCornerMult = cmds.shadingNode ('multiplyDivide', asUtility =1, n = LR + 'inCorner_mult')
            outCornerMult = cmds.shadingNode ('multiplyDivide', asUtility =1, n = LR + 'outCorner_mult')
            inCornerSum = cmds.shadingNode('plusMinusAverage', asUtility=True, n = LR + 'inCornerSum')
            outCornerSum = cmds.shadingNode('plusMinusAverage', asUtility=True, n = LR + 'outCornerSum')
            minusX = cmds.shadingNode('addDoubleLinear', asUtility=True, n = LR + 'minusX')        
            rotX_invert = LR + 'rotX_invert'
           
            cornerPoc = cmds.ls(LR + 'upCornerPoc*', fl =1, type = 'pointOnCurveInfo')
            #outer corner ctl. ty/tx
            cmds.connectAttr(cornerPoc[-1]+'.positionY', outCornerSum + '.input2D[0].input2Dy')
            cmds.connectAttr(LR + 'outerLid' + self.ctlSuffix + '.ty', outCornerSum + '.input2D[1].input2Dy')
            cmds.connectAttr(LR + 'outerDetail.ty', outCornerSum + '.input2D[2].input2Dy')
            cmds.connectAttr(outCornerSum + '.output2Dy', outCornerMult + '.input1X')
            cmds.setAttr(outCornerMult + '.input2X', cmds.getAttr(rotX_invert + '.outputX')*1.1)
            cmds.connectAttr(outCornerMult + '.outputX', LR + self.cnrPrefix + self.blinkJntName + '02' + self.jntSuffix + '.rx')
           
            cmds.connectAttr(cornerPoc[-1]+'.positionX', minusX + '.input1')
            cmds.setAttr (minusX + '.input2', -1)
            cmds.connectAttr(minusX + '.output', outCornerSum + '.input2D[0].input2Dx')
            cmds.connectAttr(LR + 'outerLid' + self.ctlSuffix + '.tx', outCornerSum + '.input2D[1].input2Dx')
            cmds.connectAttr(LR + 'outerDetail.tx', outCornerSum + '.input2D[2].input2Dx')
            cmds.connectAttr(outCornerSum + '.output2Dx', outCornerMult + '.input1Y')
            cmds.setAttr(outCornerMult + '.input2Y', cmds.getAttr(self.faceFactors['eyelid'] + '.eyeBallRotY_scale')*1.1)
            cmds.connectAttr(outCornerMult + '.outputY', LR + self.cnrPrefix + self.blinkJntName + '02' + self.jntSuffix  + '.ry')
            #inner corner ctl.ty/tx 
            cmds.connectAttr(cornerPoc[0]+'.positionY', inCornerSum + '.input2D[0].input2Dy')
            cmds.connectAttr(LR + 'innerLid' + self.ctlSuffix + '.ty', inCornerSum + '.input2D[1].input2Dy')
            cmds.connectAttr(LR + 'innerDetail.ty', inCornerSum + '.input2D[2].input2Dy')
            cmds.connectAttr(inCornerSum + '.output2Dy',inCornerMult + '.input1X')
            cmds.setAttr(inCornerMult + '.input2X', cmds.getAttr(rotX_invert + '.outputX')*1.1)
            cmds.connectAttr(inCornerMult + '.outputX', LR + self.cnrPrefix + self.blinkJntName+ '01' + self.jntSuffix + '.rx')
           
            cmds.connectAttr(cornerPoc[0]+'.positionX', inCornerSum + '.input2D[0].input2Dx')
            cmds.connectAttr(LR + 'innerLid' + self.ctlSuffix + '.tx', inCornerSum + '.input2D[1].input2Dx')
            cmds.connectAttr(LR + 'innerDetail.tx', inCornerSum + '.input2D[2].input2Dx')
            cmds.connectAttr(inCornerSum + '.output2Dx', inCornerMult + '.input1Y')
            cmds.setAttr(inCornerMult + '.input2Y', cmds.getAttr(self.faceFactors['eyelid'] + '.eyeBallRotY_scale')*1.1)
            cmds.connectAttr(inCornerMult + '.outputY', LR + self.cnrPrefix + self.blinkJntName+ '01' + self.jntSuffix + '.ry') 

    def eyeCrvToJnt(self):
        """
        """
        UDLR = [self.prefix[0] + self.uploPrefix[0],
                self.prefix[0] + self.uploPrefix[1],
                self.prefix[1] + self.uploPrefix[0],
                self.prefix[1] + self.uploPrefix[1]]
        
        for UD in UDLR:
            jnts = cmds.ls(UD + self.blinkJntName + "*" + self.jntSuffix, fl =1, type="joint")
            length = len(jnts) 
            wideJnts = cmds.ls(UD + self.wideJntName + "*" + self.jntSuffix, fl =1, type="joint")       
            maxCrv = UD[2:] +"Max" + self.crvSuffix
            minCrv = UD[2:] +"Min" + self.crvSuffix
            squintCrv = UD[2:] +"Squint" + self.crvSuffix 
            annoyCrv = UD[2:] +"Annoy" + self.crvSuffix 
            squintRemap = UD[:2] +'squint_remap'  
            annoyRemap = UD[:2] +'annoy_remap'
            blinkClamp = UD[:2]+'blink_clamp'
            loLevel = self.faceFactors['eyelid'] + '.'+ UD[:2] + 'loBlinkLevel'        
            rotX_invert = UD[:2] + 'rotX_invert'
            
            for i in range(0, length):        
                #1.ty        
                #ty sum for lids_EXP.EyeStart drives eyeLid_jnt rotateX /
                startSum = cmds.shadingNode('plusMinusAverage', asUtility=True, n = UD + 'StartSum' + str(i+1).zfill(2))            
                wideSum = cmds.shadingNode('plusMinusAverage', asUtility=True, n = UD + 'WideSum' + str(i+1).zfill(2))
                #POC on the eyelids ctls curve
                ctlXPOC = UD + 'CtlXPoc' + str(i+1).zfill(2)
                ctlYPOC = UD + 'CtlYPoc' + str(i+1).zfill(2)
                ctlTX = cmds.getAttr(ctlXPOC + '.positionX')                     
                lidCtl = UD + "Lid" + str(i+1).zfill(2)
                lidCtlBase = UD + "LidBase" + str(i+1).zfill(2)              
                          
                #squintCrv * squint Ctrl for start_sum  /annoyRemap + '.outValue'/squintRemap + '.outValue'
                squint_mult = cmds.shadingNode('multiplyDivide', asUtility=True, n = UD + 'Squint_mult' + str(i+1).zfill(2)) 
                
                #upOpenCrv(squintCrv -1) . / loOpenCrv squintCrv
                if self.uploPrefix[0] in UD:
                    squint_addD = cmds.shadingNode('addDoubleLinear', asUtility=True, n = UD + 'Squint_addD' + str(i+1).zfill(2))                         
                    cmds.connectAttr(UD[2:] + 'Squint_crvShape.cv[%s].yValue'%str(i), squint_addD + '.input1')
                    cmds.setAttr(squint_addD + '.input2', -1)
                    cmds.connectAttr(squint_addD + '.output', squint_mult + '.input1Y')
                    
                    annoy_addD = cmds.shadingNode('addDoubleLinear', asUtility=True, n = UD + 'Annoy_addD' + str(i+1).zfill(2))                        
                    cmds.connectAttr(UD[2:] + 'Annoy_crvShape.cv[%s].yValue'%str(i), annoy_addD + '.input1')
                    cmds.setAttr(annoy_addD + '.input2', -1)
                    cmds.connectAttr(annoy_addD + '.output', squint_mult + '.input1X')
                    #upLid wide(+)
                    cmds.connectAttr(blinkClamp + '.outputR', startSum + '.input2D[0].input2Dy')
                    #sum for wide jnt
                    cmds.connectAttr(blinkClamp + '.outputR', wideSum + '.input1D[0]') 
                    
                elif self.uploPrefix[1] in UD:
                    invertMult = cmds.shadingNode('multiplyDivide', asUtility =1, n = UD +  'InvertMult'+ str(i+1).zfill(2))
                    cmds.connectAttr(UD[2:] + 'Squint_crvShape.cv[%s].yValue'%str(i), squint_mult + '.input1Y')
                    cmds.connectAttr(UD[2:] + 'Annoy_crvShape.cv[%s].yValue'%str(i), squint_mult + '.input1X')
                    #loLid wide(+) by blink ctrl up
                    cmds.connectAttr(blinkClamp + '.outputR', invertMult + '.input1X')
                    cmds.setAttr(invertMult + '.input2X', -1)
                    cmds.connectAttr(invertMult + '.outputX', startSum + '.input2D[0].input2Dy')
                    #add wide to sum for wide jnt
                    cmds.connectAttr(invertMult + '.outputX', wideSum + '.input1D[0]')                
                                         
                cmds.connectAttr(squintRemap + '.outValue', squint_mult + '.input2Y')
                cmds.connectAttr(squint_mult + '.outputY', startSum +'.input2D[1].input2Dy')
              
                #annoyCrv * squint ctrl for start_sum / #upOpenCrv(annoyCrv -1) . / loOpenCrv annoyCrv 
                cmds.connectAttr(annoyRemap + '.outValue', squint_mult + '.input2X') 
                cmds.connectAttr(squint_mult + '.outputX', startSum + '.input2D[2].input2Dy')
              
                #ty sum for eyeStart            
                cmds.connectAttr(ctlYPOC + '.positionY', startSum + '.input2D[3].input2Dy') 
                cmds.connectAttr(UD + 'Detail%s'%str(i+1).zfill(2) + self.ctlSuffix + '.ty', startSum + '.input2D[4].input2Dy')
                cmds.connectAttr(self.jumperPanelName + '.'+UD+'Push_Lid%s'%str(i), startSum + '.input2D[5].input2Dy')     
                    #add the lid ctls(on the body) to startSum
                cmds.connectAttr(lidCtl + self.ctlSuffix + '.ty', startSum + '.input2D[6].input2Dy')
                
                #add squint/annoy to sum for wide jnt
                cmds.connectAttr(squint_mult + '.outputY', wideSum + '.input1D[1]')                                 
                cmds.connectAttr(squint_mult + '.outputX', wideSum + '.input1D[2]')

                if self.uploPrefix[1] in UD:
                    #define lids_EXP start
                    minMaxMult = cmds.shadingNode('multiplyDivide', asUtility =1, n = UD + 'MinMax_mult'+ str(i+1).zfill(2))
                    minMaxWideMult = cmds.shadingNode('multiplyDivide', asUtility =1, n = UD + 'MinMaxWide_mult'+ str(i+1).zfill(2))
                    loStartCon = cmds.shadingNode('condition', asUtility =1, n = UD +  'StartCon'+ str(i+1).zfill(2))
                    cmds.connectAttr(startSum + '.output2Dy', loStartCon + '.firstTerm')
                    cmds.setAttr(loStartCon +'.operation', 2)
                    cmds.connectAttr(startSum + '.output2Dy', minMaxMult  + '.input1X')
                    cmds.connectAttr('loMin_crvShape.cv[%s].yValue'%str(i), minMaxMult  + '.input2X')
                    cmds.connectAttr(minMaxMult  + '.outputX', loStartCon + '.colorIfTrueR')
                    cmds.connectAttr(startSum + '.output2Dy', minMaxMult  + '.input1Y')
                    cmds.connectAttr('loMax_crvShape.cv[%s].yValue'%str(i), minMaxMult  + '.input2Y')
                    cmds.connectAttr(minMaxMult  + '.outputY', loStartCon + '.colorIfFalseR')                             
                    cmds.connectAttr(loStartCon +'.outColorR', 'lids_EXP.' + UD + 'EyeStart%s'%str(i))                
                    cmds.connectAttr('lids_EXP.' + UD + 'EyeStart%s'%str(i), UD + 'EyeStart_crvShape.controlPoints[%s].yValue'%str(i))
                    #wideSum * min / max
                    cmds.connectAttr(wideSum + '.output1D', minMaxWideMult  + '.input1X')
                    cmds.connectAttr('loMin_crvShape.cv[%s].yValue'%str(i), minMaxWideMult  + '.input2X')
                    cmds.connectAttr(minMaxWideMult  + '.outputX', loStartCon + '.colorIfTrueG')
                    cmds.connectAttr(wideSum + '.output1D', minMaxWideMult  + '.input1Y')
                    cmds.connectAttr('loMax_crvShape.cv[%s].yValue'%str(i), minMaxWideMult  + '.input2Y')
                    cmds.connectAttr(minMaxWideMult  + '.outputY', loStartCon + '.colorIfFalseG')                             
                    
                    #define lids_EXP Open
                    minLen = 'loMin_crvShape.cv[%s].yValue'%str(i)                                 
                    blinkSum = cmds.shadingNode('plusMinusAverage', asUtility=True, n = UD + 'BlinkSum' + str(i+1).zfill(2))
                    cmds.connectAttr(loStartCon +'.outColorR', blinkSum + '.input1D[0]')
                    cmds.expression(n="damp_math"+ str(i), s = "%s= %s*%s*%s;"%(blinkSum + '.input1D[1]', blinkClamp+'.outputG', minLen, loLevel), o = 'input2', ae =1) 
                    #define lids_EXP open = start + blinkRemap
                    cmds.connectAttr(blinkSum + '.output1D', 'lids_EXP.' + UD + 'EyeOpen%s'%str(i))
                    cmds.connectAttr('lids_EXP.' + UD + 'EyeOpen%s'%str(i), UD + 'EyeOpen_crvShape.controlPoints[%s].yValue'%str(i)) 
                    jntMult = cmds.shadingNode('multiplyDivide', asUtility =1, n = UD + 'JntMult'+ str(i+1).zfill(2))  
    
                    #add extra(cornerPoc) 
                    cornerPOC = UD + 'CornerPoc' + str(i+1).zfill(2)
                    cmds.connectAttr(cornerPOC + '.positionY', blinkSum + '.input1D[2]')
                                
                    cmds.connectAttr(blinkSum + '.output1D', jntMult + '.input1Y')
                    # -self.faceFactors['eyelid'] + '.lidRotateX_scale'(= rotX_invert + '.outputX')
                    cmds.connectAttr(rotX_invert + '.outputX', jntMult + '.input2Y')
                    cmds.connectAttr(jntMult +'.outputY', jnts[i] + '.rx')     
                    
                    # wideSum to wide jnt 
                    cmds.connectAttr(loStartCon +'.outColorG', jntMult + '.input1X')
                    # -self.faceFactors['eyelid'] + '.lidRotateX_scale'(= rotX_invert + '.outputX')
                    cmds.connectAttr(rotX_invert + '.outputX', jntMult + '.input2X')
                    cmds.connectAttr(jntMult +'.outputX', wideJnts[i] + '.rx')        
                            
                #2.tx
                cmds.connectAttr(ctlXPOC + '.positionX', startSum + '.input2D[0].input2Dx')
                cmds.connectAttr(UD + 'Detail%s'%str(i+1).zfill(2) + self.ctlSuffix + '.tx', startSum + '.input2D[1].input2Dx') 
                
                #get maxCrv.cv[i].xValue movement
                cvMove_addD = cmds.shadingNode('addDoubleLinear', asUtility=True, n = UD + 'MaxCV' + str(i+1).zfill(2))
                # maxCrv.cv.xValue = ctlXPOC.positionX 
                cmds.connectAttr(UD[2:] +'Max_crv' + '.cv[%s].xValue'%str(i), cvMove_addD + '.input1')
                cmds.setAttr(cvMove_addD + '.input2', -ctlTX)                     
                
                maxCv_mult = cmds.shadingNode('multiplyDivide', asUtility=True, n = UD + 'MaxCv_mult' + str(i+1).zfill(2))
                cmds.connectAttr(cvMove_addD + '.output', maxCv_mult + '.input1X')
                cmds.connectAttr(blinkClamp + '.outputR', maxCv_mult + '.input2X')
                cmds.connectAttr(maxCv_mult + '.outputX', startSum + '.input2D[2].input2Dx')
                cmds.connectAttr(lidCtl + self.ctlSuffix + '.tx', startSum + '.input2D[3].input2Dx')
                # add lidCorner crv positionX
                cornerPOC = UD + 'CornerPoc' + str(i+1).zfill(2)
                cmds.connectAttr(cornerPOC + '.positionX', startSum + '.input2D[4].input2Dx')
                cmds.setAttr(startSum + '.input2D[5].input2Dx', -ctlTX)
                             
                '''true =(ctlPoc[i]+ Detail[i].tx + lidCtl + '.tx') *180 *(maxCrv[i]-initialX)
                false =(ctlPOC+ Detail[i].tx + lidCtl + '.tx') *180 *(squintCrv[i]-initialX)'''    
                
                rotY_mult = cmds.shadingNode('multiplyDivide', asUtility=True, n = UD + 'BlinkRY_mult' + str(i+1).zfill(2))
                txForJnt = cmds.shadingNode('addDoubleLinear', asUtility=True, n = UD + 'TxForJnt_add' + str(i+1).zfill(2)) 
                cmds.connectAttr(startSum + '.output2Dx', txForJnt + '.input1')            
                cmds.setAttr(txForJnt + '.input2', -ctlTX)
                cmds.connectAttr(txForJnt + '.output', rotY_mult + '.input1X')
                cmds.connectAttr(self.faceFactors['eyelid'] + '.lidRotateY_scale', rotY_mult + '.input2X')
                cmds.connectAttr(rotY_mult + '.outputX', jnts[i] + '.ry')
                
                #Wide tx  
                cmds.connectAttr(maxCv_mult + '.outputX', rotY_mult + '.input1Y')
                cmds.connectAttr(self.faceFactors['eyelid'] + '.lidRotateY_scale', rotY_mult + '.input2Y')
                cmds.connectAttr(rotY_mult + '.outputY', wideJnts[i] + '.ry')           
                
                #eyeOpenCrv  tx  
                cmds.connectAttr(startSum + '.output2Dx', UD + 'EyeOpen_crvShape.controlPoints[%s].xValue'%str(i))









  
    def crvCtrlToJnt(self, uploPrefix, lidCtl, jnt, wideJnt, pocNode, wideJntPocNode, ctlPocNode, initialX, RotateScale ,miValue, index):
        #connect browCtrlCurve and controller to the brow joints
        shadingNodePrefix = uploPrefix + 'Eyelid'
        ctlMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = shadingNodePrefix + 'CtlMult' + str(index))
        wideJntMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = shadingNodePrefix + 'wideJntMult' + str(index))
        plusXAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = shadingNodePrefix + 'PlusX' + str(index))
        wideJntAddX = cmds.shadingNode('addDoubleLinear', asUtility=True, n = shadingNodePrefix + 'wideJntAddX' + str(index))
        plusYAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = shadingNodePrefix + 'PlusY' + str(index))
        totalY = cmds.shadingNode('addDoubleLinear', asUtility=True, n = shadingNodePrefix+ 'YAdd' + str(index))
        blinkRemap = cmds.shadingNode('remapValue', asUtility=True, n = shadingNodePrefix + 'Remap' + str(index))
        blinkGap = cmds.shadingNode('addDoubleLinear', asUtility=True, n = shadingNodePrefix + 'BlinkGap_yAdd' + str(index))
                
        #- Jonghwan fix(not sure if it is correct) for right side controller
        if uploPrefix.startswith(self.prefix[1]):
            miValue = miValue * -1
        
        #TranslateX add up
        #1. curve translateX add up 
        cmds.setAttr(plusXAvg + '.operation', 1) 
        cmds.connectAttr(pocNode + '.positionX', plusXAvg + '.input1D[0]') 
        cmds.setAttr(plusXAvg + '.input1D[1]', -initialX)
        cmds.connectAttr(ctlPocNode + '.positionX', plusXAvg + '.input1D[2]') 
        cmds.setAttr(plusXAvg + '.input1D[3]', -initialX) 
        cmds.connectAttr(wideJntPocNode + '.positionX', wideJntAddX + '.input1') 
        cmds.setAttr(wideJntAddX + '.input2', -initialX) 
        cmds.connectAttr(wideJntAddX + '.output', plusXAvg + '.input1D[4]')
        #2. add miro control translateX 
        cmds.connectAttr(lidCtl + '.tx', plusXAvg + '.input1D[5]')
        #3. multiply XRotateScale
        cmds.connectAttr(plusXAvg + '.output1D', ctlMult + '.input1X')
        cmds.setAttr(ctlMult + '.input2X', miValue * RotateScale)
        cmds.connectAttr(wideJntAddX + '.output', wideJntMult + '.input1X')
        cmds.setAttr(wideJntMult + '.input2X', miValue * RotateScale)
        
        #4. connect jnt rotateY
        cmds.connectAttr(ctlMult + '.outputX', jnt + '.ry') 
        cmds.connectAttr(wideJntMult + '.outputX', wideJnt + '.ry')   
            
        # translateY add up
        #1. curve translateY add up 
        cmds.setAttr(plusXAvg + '.operation', 1)
        cmds.connectAttr(pocNode + '.positionY', plusYAvg + '.input1D[0]')
        cmds.connectAttr(ctlPocNode + '.positionY', plusYAvg + '.input1D[1]')
        cmds.connectAttr(wideJntPocNode + '.positionY', plusYAvg + '.input1D[2]') 
        #2. add miro control translateY 
        cmds.connectAttr(lidCtl + '.ty', plusYAvg + '.input1D[3]')
        
        #3. multiply YRotateScale
        cmds.connectAttr(plusYAvg + '.output1D', ctlMult + '.input1Y')
        cmds.setAttr(ctlMult + '.input2Y', -RotateScale)
        cmds.connectAttr(wideJntPocNode + '.positionY', wideJntMult + '.input1Y')
        cmds.setAttr(wideJntMult + '.input2Y', -RotateScale)   
        
        #4. connect jnt rotateX
        if self.uplo[0] in jnt: 
            blinkRemap = cmds.shadingNode('remapValue', asUtility=True, n = jnt.split('Blink', 1)[0] + str(index+1).zfill(2)+'_remap')
            cmds.connectAttr(ctlMult + ".outputY", blinkRemap + '.outputMin') 
            cmds.connectAttr(blinkRemap + '.outValue',  jnt + '.rx')
            cmds.connectAttr(wideJntMult + '.outputY', wideJnt + '.rx') 
        
        elif self.uplo[1] in jnt: 
            #get the remap from upJoint
            upJnt = jnt.replace("_lo","_up")
            cmds.connectAttr(ctlMult + ".outputY", blinkGap + ".input1") 
            cmds.connectAttr(blinkGap + ".output",(upJnt.split('Blink',1)[0] + str(index+1).zfill(2)+'_remap'+'.outputMax'))  
            cmds.connectAttr(ctlMult + ".outputY",  jnt + '.rx') 
            cmds.connectAttr(wideJntMult + '.outputY', wideJnt + '.rx')
    
    def createLidCtl(self, miNum):
        """
        create sub controller for the control panel
        """
           
        for updn in self.lrUplow:
            ctlP = updn + "Ctrl0"
            kids = cmds.listRelatives(ctlP, ad=True, type ='transform')   
            if kids:
                cmds.delete(kids)
                    
            cntCtlP = cmds.duplicate(ctlP, po =True, n = updn + 'CntCtlP')
            cmds.parent(cntCtlP[0],ctlP)
            cntCtl = cmds.circle(n = updn + "Center", ch=False, o =True, nr =(0, 0, 1), r = 0.1)
            cntCtl[0]
            cmds.parent(cntCtl[0], cntCtlP[0])
            cmds.setAttr(cntCtl[0] + ".overrideEnabled", 1)
            cmds.setAttr(cntCtl[0] + "Shape.overrideEnabled", 1)
            cmds.setAttr(cntCtl[0] + "Shape.overrideColor", 9)
            cmds.setAttr(cntCtl[0] + '.translate', 0,0,0)
            cmds.transformLimits(cntCtl, tx =(-1, 1), etx=(True, True))
            cmds.transformLimits(cntCtl, ty =(-1, 1), ety=(True, True))
        
            inCornerP = cmds.duplicate(cntCtlP , n = updn + 'InCornerP', rc =True)
            cmds.setAttr(inCornerP[0] +'.tx', -1)
            inTemp = cmds.listRelatives(inCornerP[0], c=True, type ='transform') 
            inCorner = cmds.rename(inTemp[0], updn + 'InCorner')
            cmds.setAttr(inCorner +'.scale', .8, .8, .8)
            cmds.transformLimits(inCorner, tx =(-.25, .25), etx=(True, True))
            cmds.transformLimits(inCorner, ty =(-1,  1), ety=(True, True))
                    
            outCornerP = cmds.duplicate(cntCtlP , n = updn + 'OutCornerP', rc=True)
            cmds.setAttr(outCornerP[0] +'.tx', 1)
            outTemp = cmds.listRelatives(outCornerP[0], c=True, type ='transform') 
            outCorner = cmds.rename(outTemp[0], updn + 'OutCorner') 
            cmds.setAttr(outCorner +'.scale', .8, .8, .8) 
            cmds.transformLimits(outCorner, tx =(-.25, .25), etx=(True, True))
            cmds.transformLimits(outCorner, ty =(-1, 1), ety=(True, True))
            
            attTemp = ['scaleX','scaleY','scaleZ', 'rotateX','rotateY','rotateZ', 'tz', 'visibility' ]  
            for x in attTemp:
                cmds.setAttr(cntCtl[0] +"."+ x, lock = True, keyable = False, channelBox =False)
                cmds.setAttr(inCorner +"."+ x, lock = True, keyable = False, channelBox =False) 
                cmds.setAttr(outCorner+"."+ x, lock = True, keyable = False, channelBox =False) 
        
            for i in range(0, miNum):
                detailCtl = cmds.spaceLocator(n = updn  + 'Detail' + str(i+1).zfill(2))
                detailCtlP = cmds.group(em =True, n = updn  + 'Detail'+ str(i+1).zfill(2) + 'P')
                cmds.parent(detailCtl[0], detailCtlP)
                cmds.parent(detailCtlP, ctlP)
                cmds.setAttr(detailCtl[0] +".overrideEnabled", 1)
                cmds.setAttr(detailCtl[0] +"Shape.overrideEnabled", 1)
                cmds.setAttr(detailCtl[0]+"Shape.overrideColor", 20)
                increment = 2.0 /(miNum-1)
                cmds.setAttr(detailCtlP + ".tx", increment*i - 1.0)
                cmds.setAttr(detailCtlP + ".ty", 0)
                cmds.setAttr(detailCtlP + ".tz", 0)
                cmds.xform(detailCtl, r =True, s =(0.1, 0.1, 0.1))
                cmds.transformLimits(detailCtl , tx =(-.25, .25), etx=(True, True))
                cmds.transformLimits(detailCtl , ty =(-.5, .5), ety=(True, True))
                for y in attTemp:
                    cmds.setAttr(detailCtl[0] +"."+ y, lock = True, keyable = False, channelBox =False)

    def lidControlConnect(self): 
        """
        connect with control panel
        """
        for pos in self.lrUplow:
            ctlCrvCv = cmds.ls(pos + 'Ctl' + self.crvSuffix + '.cv[*]', fl =True)
            cvNum = len(ctlCrvCv)
        
            # lidCtl drive the center controlPoints on ctlCrv
            if not(pos + "Center") and(pos +"InCorner") and(pos + "OutCorner"):
                print "create lid main controllers"
            else :
                
                cntAddD = cmds.shadingNode('addDoubleLinear', asUtility=True, n= pos + "Cnt_AddD")            
                cmds.connectAttr(pos + "InCorner.ty" , ctlCrvCv[0] + ".yValue")
                cmds.connectAttr(pos + "InCorner.ty" , ctlCrvCv[1] + ".yValue")
                cmds.setAttr(ctlCrvCv[0] + ".xValue" , lock = True)     
                cmds.setAttr(ctlCrvCv[1] + ".xValue" , lock = True) 
                cmds.connectAttr(pos + "Center.ty" , ctlCrvCv[2] + ".yValue")  
                # center control X match to center point(lidCtl_crv)
                
                if self.prefix[0] in pos :
                    cmds.connectAttr(pos + "Center.tx", cntAddD + ".input1")
                    cmds.setAttr(cntAddD + ".input2", 0.5) 
                    cmds.connectAttr(cntAddD + ".output" , ctlCrvCv[2] + ".xValue")
                    
                if self.prefix[1] in pos :
                    cntMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = pos +'Cnt_mult')
                    cmds.connectAttr(pos + "Center.tx" , cntMult + ".input1X") 
                    cmds.setAttr(cntMult + ".input2X", -1)
                    cmds.connectAttr(cntMult + ".outputX", cntAddD + ".input1")
                    cmds.setAttr(cntAddD + ".input2", 0.5) 
                    cmds.connectAttr(cntAddD + ".output" , ctlCrvCv[2] + ".xValue")            
                 
                cmds.connectAttr(pos + "OutCorner.ty" , ctlCrvCv[3] + ".yValue")
                cmds.connectAttr(pos + "OutCorner.ty" , ctlCrvCv[4] + ".yValue")
                cmds.setAttr(ctlCrvCv[3] + ".xValue", lock = True)  
                cmds.setAttr(ctlCrvCv[4] + ".xValue", lock = True)   
        
            detailPCtls = cmds.ls(pos + "Detail*P", type = 'transform')

            details = []
            for mom in detailPCtls :
                kid= cmds.listRelatives(mom, c = True, type = 'transform')
                details.append(kid[0])
                        
            ctlNum = len(details) 
                
            for i in range(0, ctlNum):
                # POC on ctlCrv drive detail control parent  
                cntRemoveX = cmds.shadingNode('addDoubleLinear', asUtility=True, n= pos +"Cnt"+ str(i+1)+"RemoveX")
                momMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = pos +'Mom'+ str(i+1)+'_mult')
                cmds.connectAttr(pos + "CtlPoc0" +str(i+1) +".positionY", detailPCtls[i] + ".ty")
                #Xvalue match between POC and CtrlP
                cmds.connectAttr(pos + "CtlPoc0" +str(i+1) +".positionX", momMult + ".input1X")        
                cmds.connectAttr(momMult + ".outputX", cntRemoveX + ".input1")
                if "l_" in pos :
                    cmds.setAttr(momMult + ".input2X", 2)
                    cmds.setAttr(cntRemoveX  + ".input2", -1) 
                    cmds.connectAttr(cntRemoveX +".output", detailPCtls[i] + ".tx")
                if "r_" in pos :
                    cmds.setAttr(momMult + ".input2X", -2)
                    cmds.setAttr(cntRemoveX  + ".input2", 1)              
                    cmds.connectAttr(cntRemoveX +".output", detailPCtls[ctlNum-i-1] + ".tx")
                    
                # detail control drive the joint(add to the +-Average node)
                cmds.connectAttr(details[i] + ".tx", pos +"EyelidPlusX" + str(i+1) + ".input1D[6]") 
                cmds.connectAttr(details[i] + ".ty", pos +"EyelidPlusY" + str(i+1) + ".input1D[4]")
    
    def __allCrvs(self):
        crvs = []
        
        if not cmds.objExists(self.eyelidCrvGrpName):
            print "curve is not setup yet"
        else:
            topLidCrvGrp = cmds.listRelatives(self.eyelidCrvGrpName)
            for topGrp in topLidCrvGrp:
                for crv in cmds.listRelatives(topGrp):        
                    crvs.append(crv)
        return crvs
    
    def hideAlLCrv(self):
        """
        hide all curves
        """
        crvs = self.__allCrvs()
        for crv in crvs:
            cmds.setAttr(crv + '.v', 0)
                
        return crvs
        
    def showCrv(self, crv):
        """
        unhide crv
        """
        if not cmds.objExists(crv):
            print "curve does not exists"
        else:
            self.hideAlLCrv()
            cmds.setAttr(crv + '.v', 1)
    
    def saveEyelidCrvInfo(self):
        """
        save eyelid curve's info as json file
        """
        crvs = self.__allCrvs()
        allCrvInfo = {}
        for crv in crvs:
            allCrvCvs = cmds.ls(crv + '.cv[*]', fl = True)
            allCrvCvs = [x for x in allCrvCvs if 'Ctl' + self.crvSuffix not in x]
            for crvCv in allCrvCvs:
                #cmds.xform(crvCv, t = True, q = True, ws = True)
                allCrvInfo[crvCv] = cmds.xform(crvCv, t = True, q = True, ws =True)
        
        self.writeJsonFile(self.eyelidCrvJsonLoc, allCrvInfo)
        cmds.confirmDialog(title='Eyelid Curve info Saved',
                           message='Location : %s' %self.eyelidCrvJsonLoc,
                           button=['ok'],
                           defaultButton='ok')
        
        return self.eyelidCrvJsonLoc
    
    def loadEyelidCrvInfo(self):
        """
        retrieve curves with data saved
        """
        crvData = self.readJsonFile(self.eyelidCrvJsonLoc)
        for eachCrv in crvData.keys():
            cmds.xform(eachCrv, t = crvData[eachCrv], ws =True)
        
        return crvData
        