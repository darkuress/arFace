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
import Base
reload(Base)

class Ctrls(Func.Func, Base.Base):
    def __init__(self,
                 upDown = 'up',
                 ctlSize = 1,
                 offset  = 1, 
                 rotateScale = 10,
                 **kw):
        """
        initializing variables
        """
        self.initialX         = 0
        self.ctlSize          = ctlSize
        self.offset           = offset
        self.rotateScale      = rotateScale
        self.upDown           = upDown
        
        #- local variables
        Func.Func.__init__(self, **kw)
        Base.Base.__init__(self, **kw)

    def createLidCtrls(self, baseJnts):
        """
        create controller for lid
        """       
        if not (self.lEyeLoc):
            print "create the face locators"
            
        else: 
            eyeRotY = cmds.getAttr (self.lEyeLoc + '.ry' ) 
            eyeCenterPos = cmds.xform(self.lEyeLoc, t = True, q = True, ws = True) 
        
        allLidsCtlGrp = []
        allLidsCrvGrp  = []
        for lr in self.prefix:
            #- left right + upper lower prefix
            uploPrefix = lr + self.upDown
            
            #- creating crv group nodes
            lidCrvGrp = cmds.group ( n = uploPrefix + 'crv' + self.grpSuffix, em =True )
            allLidsCrvGrp.append(lidCrvGrp)
            #topJnt = [jnt for jnt in baseJnts if jnt.startswith(lr)]
            #tempJnts = cmds.listRelatives ( topJnt, ad =True )
            childJnts = cmds.ls (uploPrefix + '*%s*%s' %(self.blinkJntName, self.jntSuffix)) 
            wideJnts = cmds.ls (uploPrefix + '*%s*%s' %(self.wideJntName, self.jntSuffix))
            childJnts.sort()
            wideJnts.sort()
            jntNum = len(childJnts)
            
            #- making lids Ctrl group
            lidsCtrlGrp = cmds.group (em=True, w =True, n = uploPrefix + 'Eyelid' + self.ctlSuffix + self.grpSuffix)
            allLidsCtlGrp.append(lidsCtrlGrp)
            
            if lr == self.prefix[0]:
                cmds.xform (lidsCtrlGrp, ws = True, t = eyeCenterPos)
                cmds.setAttr (lidsCtrlGrp + ".ry", eyeRotY)
            else:
                cmds.xform (lidsCtrlGrp, ws = True, t = (-eyeCenterPos[0], eyeCenterPos[1], eyeCenterPos[2]))
                cmds.setAttr (lidsCtrlGrp + ".ry", -eyeRotY)                
            
            #- final lid shape curve
            lidCrv = cmds.curve ( d = 3, p =([0,0,0],[0.33,0,0],[0.66,0,0],[1,0,0])) 
            cmds.rebuildCurve ( rt = 0, d = 1, kr = 0, s = jntNum-1 )  
            tempCrv = cmds.rename (lidCrv, uploPrefix +'Lid' + self.crvSuffix)
            cmds.parent (tempCrv, lidCrvGrp)
            lidCrvShape = cmds.listRelatives (tempCrv, c = True )
            
            wideJntCrv = cmds.duplicate ( tempCrv, n= uploPrefix +'WideJnt' + self.crvSuffix) 
            wideJntCrvShape = cmds.listRelatives ( wideJntCrv, c = True ) 

            #- eyelids controller curve shape ( different number of points, so can not be target of the blendShape)      
            lidCtlCrv = cmds.curve ( d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0], [1,0,0]))
            #- rebuildCurve? 
            #cmds.rebuildCurve ( rt = 0, d = 1, kr = 0, s = jntNum-1 )  
            tempCtlCrv = cmds.rename (lidCtlCrv, uploPrefix +'Ctl' + self.crvSuffix)
            lidCtlCrvShape = cmds.listRelatives ( tempCtlCrv, c = True ) 
            cmds.parent (tempCtlCrv, lidCrvGrp) 

            #- eyeClose(blink) lid shape        
            blinkCrv = cmds.duplicate ( tempCrv, n= uploPrefix +'Blink' + self.crvSuffix)
            
            #- eyeWide(suprise) lid shape        
            wideCrv = cmds.duplicate ( tempCrv, n= uploPrefix +'Wide' + self.crvSuffix)
                        
            #- eyeSquint lid shape        
            squintCrv = cmds.duplicate ( tempCrv, n= uploPrefix +'Squint' + self.crvSuffix) 
                        
            if lr == self.prefix[1]: 
                cmds.hide (blinkCrv, wideCrv, squintCrv)
                        
            #- eyeDirection lid shape        
            lookUp = cmds.duplicate ( tempCrv, n= uploPrefix +'LookUp' + self.crvSuffix) 


            lookDn = cmds.duplicate ( tempCrv, n= uploPrefix +'LookDn' + self.crvSuffix) 
            lookLeft = cmds.duplicate ( tempCrv, n= uploPrefix +'LookLeft' + self.crvSuffix)                 
            lookRight = cmds.duplicate ( tempCrv, n= uploPrefix +'LookRight' + self.crvSuffix) 

            crvBS = cmds.blendShape ( blinkCrv[0], lookUp[0], lookDn[0], lookLeft[0], lookRight[0], tempCrv, n = uploPrefix + 'LidCrvBS')
            cmds.blendShape( crvBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)] )
              
            wideBS = cmds.blendShape ( wideCrv[0], squintCrv[0], wideJntCrv, n = uploPrefix + 'WideJntBS' )
            cmds.blendShape( wideBS[0], edit=True, w=[(0, 1), (1, 1)] )
            
            index = 0 
            indices = 0

            for jnt in childJnts:
                print 'jnt : ', jnt
                miValue = 1
                wideJnt = wideJnts[index]
                childJnt = cmds.listRelatives (jnt, c =True)
                childPos = cmds.xform ( childJnt[0], t = True, q = True, ws = True)
                jntIndex = jnt.split(self.jntSuffix)[0].split('Blink')[1]
                #pocNode on the final lid curve 
                pocNode = cmds.shadingNode ( 'pointOnCurveInfo', asUtility=True, n = uploPrefix + 'Poc' + jntIndex)
                cmds.connectAttr ( lidCrvShape[0] + ".worldSpace",  pocNode + '.inputCurve')   
                cmds.setAttr ( pocNode + '.turnOnPercentage', 1 )        
                increment = 1.0/(jntNum-1)
                cmds.setAttr ( pocNode + '.parameter', increment *index )     
                initialX = cmds.getAttr (pocNode + '.positionX')
                
                #- pocNode on the wideJnt curve
                wideJntPocNode = cmds.shadingNode ( 'pointOnCurveInfo', asUtility=True, n = uploPrefix + 'wideJntPoc' + jntIndex)
                cmds.connectAttr ( wideJntCrvShape[0] + ".worldSpace",  wideJntPocNode + '.inputCurve')   
                cmds.setAttr ( wideJntPocNode + '.turnOnPercentage', 1 )        
                cmds.setAttr ( wideJntPocNode + '.parameter', increment *index )  
                
                #- pocNode on the eyelids ctls curve
                ctlPocNode = cmds.shadingNode ( 'pointOnCurveInfo', asUtility=True, n = uploPrefix + 'CtlPoc' + jntIndex)
                cmds.connectAttr ( lidCtlCrvShape[0] + ".worldSpace", ctlPocNode + '.inputCurve')   
                cmds.setAttr ( ctlPocNode + '.turnOnPercentage', 1 )        
                cmds.setAttr ( ctlPocNode + '.parameter', increment *index ) 
                
                #- creating controller 
                if lr == self.prefix[0]:
                    cColor = 6
                else:
                    cColor = 17
                lidCtl, lidCtlP = self.circleController(uploPrefix + 'EyeLid' + jntIndex + self.ctlSuffix,
                                                        'xy',
                                                        self.ctlSize * 0.2,
                                                        color = cColor,
                                                           lockAttr = [])
                cmds.xform(lidCtlP, ws = True, t =(childPos[0], childPos[1], childPos[2] + self.offset))
                cmds.parent (lidCtlP, lidsCtrlGrp )

                index = index + 1
                
                self.crvCtrlToJnt ( uploPrefix, lidCtl, jnt, wideJnt, pocNode, wideJntPocNode, ctlPocNode, initialX, self.rotateScale , miValue, index )
    
        return {'lidsCtlGrp' : allLidsCtlGrp, 'lidsCrvGrp' : allLidsCrvGrp, 'numJnts' : jntNum}
        
    def connectToPanel(self, jntNum):
        """
        make panel live to control eyelid
        """
        self.createLidCtl(jntNum)
        self.lidControlConnect()