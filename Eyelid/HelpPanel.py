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

class HelpPanel(Base.Base):
    def __init__(self, **kw):
        """
        initializing variables
        """
        #local variables
        Base.Base.__init__(self, **kw)

    def createHelpPanel(self, ctlName, type):
        """
        create help panel base
        usage :
        ctlNames = ['eyeCtl', 'eyeBlink', 'eyeSquint', 'eyeSquach' ]
        for x in ctlNames:
            createHelpPanel(x, 'A')
        """        
        for pfx in self.prefix:
            attrs = [ pfx +'HCtl', pfx +'VCtl', pfx +'HPos', pfx +'HNeg', pfx +'VPos', pfx +'VNeg']
            if(type == 'B'):
                attrs = [ pfx +'HCtl', pfx +'VCtl', pfx +'HPos', pfx +'HNeg', pfx +'VPos', pfx +'VNeg', pfx +'HPosVPos', pfx +'HPosVNeg', pfx +'HNegVPos', pfx +'HNegVNeg']
                
            for att in attrs:
                if not cmds.objExists(ctlName + "HelpPanel"):
                    cmds.createNode('transform', n = ctlName + "HelpPanel")
                    cmds.parent(ctlName + "HelpPanel", 'helpPanel' + self.grpSuffix)
                cmds.addAttr(ctlName + "HelpPanel", longName = att , at='double', defaultValue= 0 , minValue=0, maxValue=1)
            
            negMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = pfx + ctlName + 'Neg_mult')
            posClamp = cmds.shadingNode('clamp', asUtility=True, n = pfx + ctlName + 'Pos_clamp')
            negClamp = cmds.shadingNode('clamp', asUtility=True, n = pfx + ctlName + 'Neg_clamp')
            cmds.connectAttr(pfx + ctlName +".tx", ctlName + "HelpPanel." + pfx + "HCtl")
            cmds.connectAttr(pfx + ctlName +".ty", ctlName + "HelpPanel." + pfx + "VCtl")
            cmds.connectAttr(pfx + ctlName +".tx", posClamp + ".inputR")
            cmds.connectAttr(pfx + ctlName +".ty", posClamp + ".inputG")
            cmds.setAttr(posClamp + ".maxR", 1)
            cmds.setAttr(posClamp + ".maxG", 1)
            cmds.connectAttr(posClamp + ".outputR", ctlName + "HelpPanel." + pfx + "HPos")
            cmds.connectAttr(posClamp + ".outputG", ctlName + "HelpPanel." + pfx + "VPos")
            
            cmds.connectAttr(pfx + ctlName +".tx", negMult + ".input1X")
            cmds.connectAttr(pfx + ctlName +".ty", negMult + ".input1Y")
            cmds.setAttr(negMult + ".input2X", -1)
            cmds.setAttr(negMult + ".input2Y", -1)
            cmds.connectAttr(negMult + ".outputX", negClamp + ".inputR")
            cmds.connectAttr(negMult + ".outputY", negClamp + ".inputG")            
            cmds.setAttr(negClamp  + ".maxR", 1)
            cmds.setAttr(negClamp  + ".maxG", 1)
            cmds.connectAttr(negClamp + ".outputR", ctlName + "HelpPanel." + pfx + "HNeg")
            cmds.connectAttr(negClamp + ".outputG", ctlName + "HelpPanel." + pfx + "VNeg")
            
            if(type =='B'):
                plusOne = cmds.shadingNode('plusMinusAverage', asUtility=True, n = pfx + ctlName + '_plusOne')
                vNegMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = pfx + ctlName + 'VNeg_mult')
                vPosMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = pfx + ctlName + 'VPos_mult')
                plusOneClamp = cmds.shadingNode('clamp', asUtility=True, n = pfx + ctlName + 'plusOne_clamp')
                cmds.connectAttr(pfx + ctlName +".tx", plusOne + '.input3D[0].input3Dx') 
                cmds.connectAttr(negMult + '.outputX', plusOne + '.input3D[0].input3Dy')
                cmds.setAttr(plusOne + ".operation",  1)
                cmds.setAttr(plusOne + '.input3D[1].input3Dx', 1)
                cmds.setAttr(plusOne + '.input3D[1].input3Dy', 1)
                cmds.connectAttr(plusOne + '.output3Dx', plusOneClamp + ".inputR")
                cmds.connectAttr(plusOne + '.output3Dy', plusOneClamp + ".inputG")
                cmds.setAttr(plusOneClamp + '.maxR', 1)
                cmds.setAttr(plusOneClamp + '.maxG', 1)
                cmds.connectAttr(plusOneClamp + '.outputR', vPosMult + ".input1X")
                cmds.connectAttr(plusOneClamp + '.outputG', vPosMult + ".input1Y")
                cmds.connectAttr(ctlName + "HelpPanel." + pfx + "VPos", vPosMult + ".input2X")
                cmds.connectAttr(ctlName + "HelpPanel." + pfx + "VPos", vPosMult + ".input2Y")
                cmds.connectAttr(vPosMult + ".outputX", ctlName + "HelpPanel." + pfx + 'HPosVPos')
                cmds.connectAttr(vPosMult + ".outputY", ctlName + "HelpPanel." + pfx + 'HNegVPos')
                
                cmds.connectAttr(plusOneClamp + '.outputR', vNegMult + ".input1X")
                cmds.connectAttr(plusOneClamp + '.outputG', vNegMult + ".input1Y")
                cmds.connectAttr(ctlName + "HelpPanel." + pfx + "VNeg", vNegMult + ".input2X")
                cmds.connectAttr(ctlName + "HelpPanel." + pfx + "VNeg", vNegMult + ".input2Y")
                cmds.connectAttr(vNegMult + ".outputX", ctlName + "HelpPanel." + pfx + 'HPosVNeg')
                cmds.connectAttr(vNegMult + ".outputY", ctlName + "HelpPanel." + pfx + 'HNegVNeg')

    def helpPanelToEyeCrv (self):
        """
        ctlNames = ['eyeCtl', 'eyeBlink', 'eyeSquint', 'eyeSquach' ]
        """
        cmds.group ( em=True, n = "helpPanels" )
        for pfx in self.prefix: 
            
            # set blink range 
            blinkJnts = cmds.ls ( pfx + "upLidBlink*_jnt", fl=True, type="joint" )
            blinkJnts.sort()    
            blinkGap = cmds.ls ( pfx + "loEyelidBlink*_yAdd*", fl=True, type="addDoubleLinear" )
            blinkGap.sort()
            numJnts = len (blinkJnts)
            for i in range (0, numJnts ):
                rotX = cmds.getAttr ( blinkJnts[i] +".rx" )
                cmds.setAttr ( blinkGap[i] + ".input2", rotX) 
           
            cmds.setAttr( pfx + "upLidCrvBS." + pfx + "upBlink_crv", 0 )   
            
            #Blink setup                     
            if not cmds.objExists ("eyeBlinkHelpPanel"):
                cmds.group ( em=True, p = 'helpPanels', n = "eyeBlinkHelpPanel" )
            
            attList = cmds.listAttr( "eyeBlinkHelpPanel", s=True, r=True, w=True, c=True, st = ["*Pos", "Neg"]) 
            if not ( attList ):
                createHelpPanel ( 'eyeBlink', "A" )
                    
            #blinkCtrl connect to the eyeOpen curves ( lidCurve BlendShape )
            #cmds.connectAttr ( "eyeBlinkHelpPanel." + pfx + "VPos", pfx+"upLidCrvBS." + pfx + "upEyeOpen_crv" )
            #cmds.connectAttr ( "eyeBlinkHelpPanel." + pfx + "VPos", pfx+"loLidCrvBS." + pfx + "loEyeOpen_crv" )
            
            # blinkCtrl connect to all the remapValue.inputValue / loBlink curves
            remapList = cmds.ls ( pfx + "upLid*_remap", fl =True, type = "remapValue")
            for remap in remapList:
                cmds.connectAttr ( "eyeBlinkHelpPanel." + pfx + "VNeg", remap + ".inputValue" )
        
            cmds.connectAttr ( "eyeBlinkHelpPanel." + pfx + "VNeg", pfx + "loLidCrvBS." + pfx + "loBlink_crv" )
            
                 
            #Squint Wide setup                     
            if not cmds.objExists ("eyeSquintHelpPanel"):
                cmds.group ( em=True, p = 'helpPanels', n = "eyeSquintHelpPanel" )
            
            attList = cmds.listAttr( "eyeSquintHelpPanel", s=True, r=True, w=True, c=True, st = ["*Pos", "Neg"]) 
            if not ( attList ):
                createHelpPanel ("eyeSquint", "A" )
                        
            #squint_wide ctrl connect to the eyeWideJnt curves ( WideJnt BlendShape )
            cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VPos", pfx+"upWideJntBS." + pfx + "upWide_crv" )
            cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VPos", pfx+"loWideJntBS." + pfx + "loWide_crv" )
            cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VNeg", pfx+"upWideJntBS." + pfx + "upSquint_crv" )
            cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VNeg", pfx+"loWideJntBS." + pfx + "loSquint_crv" )  
            
            if not cmds.objExists ("eyeCtlHelpPanel"):
                cmds.group ( em=True, p = 'helpPanels', n = "eyeCtlHelpPanel" )
            
            attList = cmds.listAttr( "eyeCtlHelpPanel", s=True, r=True, w=True, c=True, st = ["*Pos", "Neg"]) 
            if not ( attList ):
                createHelpPanel ( "eyeCtl", "A" )        
                                      
            #squint_wide ctrl connect to the eyeWideJnt curves ( WideJnt BlendShape )
            cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VPos", pfx+"upLidCrvBS." + pfx + "upLookUp_crv" )
            cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VPos", pfx+"loLidCrvBS." + pfx + "loLookUp_crv" )
            
            cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VNeg", pfx+"upLidCrvBS." + pfx + "upLookDn_crv" )
            cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VNeg", pfx+"loLidCrvBS." + pfx + "loLookDn_crv" )  
            
            cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "HPos", pfx+"upLidCrvBS." + pfx + "upLookLeft_crv" )
            cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "HPos", pfx+"loLidCrvBS." + pfx + "loLookLeft_crv" )
            
            cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "HNeg", pfx+"upLidCrvBS." + pfx + "upLookRight_crv" )
            cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "HNeg", pfx+"loLidCrvBS." + pfx + "loLookRight_crv" )
