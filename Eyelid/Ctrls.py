#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright(c) 2015 Sukwon Shin, Jonghwan Hwang
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
        self.__createEyeRig()
        self.__createPanelCtrls(baseJnts)
        self.__jumperPanel()
        self.__eyeLidsCrvs()

    def __createEyeRig(self):
        """
        create Eye Rig
        """
        lEyePos = cmds.xform('lEyePos', t = True, q = True, ws = True)
        if not(self.eyeRigP):
            eyeRigP = cmds.group(em=True, n = self.eyeRigP, p= self.eyeRig)      
     
        eyeRigTR = cmds.group(em=True, n = 'eyeRigTR', p= 'eyeRigP') 
        ffdSquachLattice = cmds.group(em =1, n = 'ffdSquachLattice', p = 'eyeRigP')
        lEyeP = cmds.group(em=True, n = self.prefix[0] + 'eyeP', p= eyeRigTR) 
        cmds.xform(lEyeP, ws =1, t =(lEyePos[0], lEyePos[1], lEyePos[2])) 
        lEyeRP = cmds.group(em=True, n = self.prefix[0] + 'eyeRP', p= lEyeP)
        lEyeScl = cmds.group(em=True, n = self.prefix[0] + 'eyeScl', p= lEyeRP)
        lEyeRot = cmds.group(em=True, n = self.prefix[0] + 'eyeRot', p= lEyeScl)
        lEyeballRot = cmds.group(em=True, n = self.prefix[0] + 'eyeballRot', p= lEyeRot)
     
         
        rEyeP = cmds.group(em=True, n = self.prefix[1] + 'eyeP', p= eyeRigTR) 
        cmds.xform(rEyeP, ws =1, t =(-lEyePos[0], lEyePos[1], lEyePos[2])) 
        rEyeRP = cmds.group(em=True, n = self.prefix[1] + 'eyeRP', p= rEyeP) 
        rEyeScl = cmds.group(em=True, n = self.prefix[1] + 'eyeScl', p= rEyeRP)
        rEyeRot = cmds.group(em=True, n = self.prefix[1] + 'eyeRot', p= rEyeScl)
        rEyeballRot = cmds.group(em=True, n = self.prefix[1] + 'eyeballRot', p= rEyeRot)

    def __createPanelCtrls(self, baseJnts):
        """
        create controller for panel
        """       
        if not(self.lEyeLoc):
            print "create the face locators"
        if not cmds.objExists(self.eyelidCrvGrpName):
            eyeLidCrvGrp = cmds.group(em =1, n = self.eyelidCrvGrpName, p = self.crvGrp)
            
        allLidsCtlGrp = []
        
        for lr in self.prefix:
            #- left right + upper lower prefix
            uploPrefix = lr + self.upDown
            ctlP = uploPrefix + "Ctrl0"
            kids = cmds.listRelatives(ctlP, ad=True, type ='transform')   
            if kids:
                cmds.delete(kids)
            lidJnts = cmds.ls(uploPrefix +  self.blinkJntName + "*" + self.jntSuffix, type = 'joint')
            lidJntsLen = len(lidJnts)

            #- making lids Ctrl group
            lidsCtrlGrp = cmds.group(em=True, w =True, n = uploPrefix + self.eyelidName + self.ctlSuffix + self.grpSuffix)
            allLidsCtlGrp.append(lidsCtrlGrp)
            cntPos = cmds.xform(ctlP, q=1, ws =1, t = 1)
            
            #- creating controller 
            if lr == self.prefix[0]:
                cColor = 6
            else:
                cColor = 17
                
            for pos in ['Center', 'InCorner', 'OutCorner']:
                lidCtl, lidCtlP = self.circleController(uploPrefix + pos + self.ctlSuffix,
                                                        'xy',
                                                        self.ctlSize * 0.1,
                                                        color = cColor,
                                                        lockAttr = ['tz',
                                                                    'sc',
                                                                    'ro',
                                                                    'vi'])
                cmds.xform(lidCtlP, ws = True, t =(cntPos[0], cntPos[1], cntPos[2]))
                cmds.parent(lidCtlP, lidsCtrlGrp)
                if pos == 'InCorner':
                    cmds.setAttr(lidCtl +'.tx', -1)
                elif pos == 'OutCorner':
                    cmds.setAttr(lidCtl +'.tx', 1)
            
            details = []
            for i in range(1, lidJntsLen+1):
                detailCtl = self.circleController(uploPrefix + 'Detail'+ str(i).zfill(2),
                                                  'xy',
                                                  self.ctlSize * 0.05,
                                                  color = cColor,
                                                  lockAttr = ['tz',
                                                              'sc',
                                                              'ro',
                                                              'vi'])
                details.append(detailCtl[0])
                detailCtlP = detailCtl[1]
                cmds.parent(detailCtlP, ctlP)
                increment = 2.0 /(lidJntsLen+1)
                cmds.setAttr(detailCtlP + ".tx", increment*i - 1.0)
                cmds.setAttr(detailCtlP + ".ty", 0)
                cmds.setAttr(detailCtlP + ".tz", 0)

            #- eyelids controller curve shape(different number of points)          
            tempCtlCrv = cmds.curve(d = 3, p =([0,0,0],[0.33,0,0],[0.66,0,0],[1,0,0])) 
            cmds.rebuildCurve(tempCtlCrv, rt = 0, d = 3, kr = 0, s = 2)   
            lidCtlCrv = cmds.rename(tempCtlCrv, uploPrefix +'Ctl' + self.crvSuffix)
            cmds.parent(lidCtlCrv, self.eyelidCrvGrpName) 
            ctlCrvCv = cmds.ls(lidCtlCrv + '.cv[*]', fl =True)#!!check same curve exist if Error : list index out of range
                    
            #- corner twist curves setup(curves for corner Adjust 06/23/2016)
            cornerCrv = cmds.duplicate(lidCtlCrv, n = uploPrefix +'Corner' + self.crvSuffix)
            cornerCrvCv = cmds.ls(cornerCrv[0] + '.cv[*]', fl =True)

            if self.uploPrefix[0] in uploPrefix:
                inCls = cmds.cluster(cornerCrvCv[0:2], n = uploPrefix[:2] +'inTwistCls')
                cmds.percent(inCls[0], cornerCrvCv[1],  v = 0.3)    
                outCls = cmds.cluster(cornerCrvCv[3:5], n = uploPrefix[:2] +'outTwistCls')
                cmds.percent(outCls[0], cornerCrvCv[3], v = 0.3) 
        
            elif self.uploPrefix[1] in uploPrefix:
                cmds.sets(cornerCrvCv[0:2], add = uploPrefix[:2] +'inTwistClsSet')
                cmds.percent(uploPrefix[:2] +'inTwistCls', cornerCrvCv[1], v = 0.3) 
                cmds.sets(cornerCrvCv[3:5], add = uploPrefix[:2] +'outTwistClsSet')
                cmds.percent(uploPrefix[:2] +'outTwistCls', cornerCrvCv[3], v = 0.3)
                
                #- corner twist setup(no need to use ClsHandle.rotateZ)
                cmds.connectAttr(uploPrefix[:2] + "innerLidTwist.tx" , uploPrefix[:2] +'inTwistClsHandle.tx')
                cmds.connectAttr(uploPrefix[:2] + "innerLidTwist.ty" , uploPrefix[:2] +'inTwistClsHandle.ty')
                
                cmds.connectAttr(uploPrefix[:2] + "outerLidTwist.tx" , uploPrefix[:2] +'outTwistClsHandle.tx')
                cmds.connectAttr(uploPrefix[:2] + "outerLidTwist.ty" , uploPrefix[:2] +'outTwistClsHandle.ty')

            #- lidCtl drive the center controlPoints on ctlCrv
            #corner ctls setup                    
            cmds.connectAttr(uploPrefix + "InCorner" + self.ctlSuffix + ".ty" , ctlCrvCv[0] + ".yValue")
            cmds.connectAttr(uploPrefix + "InCorner" + self.ctlSuffix + ".ty" , ctlCrvCv[1] + ".yValue")
            cmds.setAttr(ctlCrvCv[0] + ".xValue" , lock = True)     
            cmds.setAttr(ctlCrvCv[1] + ".xValue" , lock = True) 

            cmds.connectAttr(uploPrefix + "OutCorner" + self.ctlSuffix + ".ty" , ctlCrvCv[3] + ".yValue")
            cmds.connectAttr(uploPrefix + "OutCorner" + self.ctlSuffix + ".ty" , ctlCrvCv[4] + ".yValue")
            cmds.setAttr(ctlCrvCv[3] + ".xValue", lock = True)  
            cmds.setAttr(ctlCrvCv[4] + ".xValue", lock = True)
                                 
            cntAddD = cmds.shadingNode('addDoubleLinear', asUtility=True, n= uploPrefix + "Cnt_AddD")    
            if self.prefix[0] in uploPrefix: #left
                #- center ctrl.tx drives center point(lidCtl_crv) 
                lCntMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = uploPrefix +'Cnt_mult') 
                cmds.connectAttr(uploPrefix + "Center" + self.ctlSuffix + ".tx", cntAddD + ".input1")
                cmds.setAttr(cntAddD + ".input2", 0.5) 
                cmds.connectAttr(cntAddD + ".output" , ctlCrvCv[2] + ".xValue")
                #- center ctrl.ty drives ctlCrv center cv[2].yValue
                cmds.connectAttr(uploPrefix + "Center" + self.ctlSuffix + ".ty" , lCntMult + ".input1Y")
                cmds.setAttr(lCntMult + ".input2Y", 2) 
                cmds.connectAttr(lCntMult + ".outputY", ctlCrvCv[2] + ".yValue")                
                
            if self.prefix[1] in uploPrefix: #right
                #- center ctrl.tx drives ctlCrv center cv[2].xValue 
                rCntMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = uploPrefix +'Cnt_mult')
                cmds.connectAttr(uploPrefix + "Center" + self.ctlSuffix + ".tx" , rCntMult + ".input1X") 
                cmds.setAttr(rCntMult + ".input2X", -1)
                cmds.connectAttr(rCntMult + ".outputX", cntAddD + ".input1")
                cmds.setAttr(cntAddD + ".input2", 0.5) 
                cmds.connectAttr(cntAddD + ".output" , ctlCrvCv[2] + ".xValue")            
                #center ctrl.ty drives ctlCrv center cv[2].yValue 
                cmds.connectAttr(uploPrefix + "Center" + self.ctlSuffix + ".ty" , rCntMult + ".input1Y")
                cmds.setAttr(rCntMult + ".input2Y", 2) 
                cmds.connectAttr(rCntMult + ".outputY", ctlCrvCv[2] + ".yValue") 

            detailPCtls = cmds.ls(uploPrefix + "Detail*" + self.grpSuffix, type = 'transform')
            incrementYPoc = 1.0/(lidJntsLen +1)
            incrementXPoc = 1.0/(lidJntsLen -1)    
            for i in range(1, lidJntsLen+1):
                #- POC for positionX on the eyelids ctl curve 
                ctlXPOC = cmds.shadingNode('pointOnCurveInfo', asUtility=True, n = uploPrefix + 'CtlXPoc' + str(i).zfill(2)) 
                cmds.connectAttr(uploPrefix + "Ctl_crvShape.worldSpace", ctlXPOC + '.inputCurve')   
                cmds.setAttr(ctlXPOC + '.turnOnPercentage', 1)        
                cmds.setAttr(ctlXPOC + '.parameter', incrementXPoc *(i-1))
                
                #- POC for positionY on the eyelids ctl curve
                ctlYPOC = cmds.shadingNode('pointOnCurveInfo', asUtility=True, n = uploPrefix + 'CtlYPoc' + str(i).zfill(2)) 
                cmds.connectAttr(uploPrefix + "Ctl_crvShape.worldSpace", ctlYPOC + '.inputCurve')   
                cmds.setAttr(ctlYPOC + '.turnOnPercentage', 1)        
                cmds.setAttr(ctlYPOC + '.parameter', incrementYPoc *i)
                
                #- POC on ctlCrv drive detail control parent  
                cntRemoveX = cmds.shadingNode('addDoubleLinear', asUtility=True, n= uploPrefix +"RemoveX"+ str(i).zfill(2))
                momMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = uploPrefix +'Mom'+ str(i).zfill(2)+'_mult')
                cmds.connectAttr(ctlYPOC +".positionY", detailPCtls[i-1] + ".ty")
                
                #- Xvalue match between POC and CtrlP(detailPCtls[i] = 2*ctlPoc -1)
                cmds.connectAttr(ctlXPOC +".positionX", momMult + ".input1X")
                cmds.setAttr(momMult + ".input2X", 2)        
                cmds.connectAttr(momMult + ".outputX", cntRemoveX + ".input1")            
                cmds.setAttr(cntRemoveX  + ".input2", -1)
                cmds.connectAttr(cntRemoveX +".output", detailPCtls[i-1] + ".tx")
                
                #- curves for corner Adjust 06/23/2016
                cornerPOC = cmds.shadingNode('pointOnCurveInfo', asUtility=True, n = uploPrefix + 'CornerPoc' + str(i).zfill(2)) 
                cmds.connectAttr(uploPrefix +"Corner" + self.crvSuffix + ".worldSpace", cornerPOC + '.inputCurve')   
                cmds.setAttr(cornerPOC + '.turnOnPercentage', 1)        
                cmds.setAttr(cornerPOC + '.parameter', incrementXPoc*(i-1))   


    def __jumperPanel(self):
        """
        create JumpPanel
        """
        self.jumperPanel()

    def __eyeLidsCrvs(self, ctlSize = 0.1):
        """
        create
        """
        eyeRotY = cmds.getAttr('lEyePos.ry') 
        eyeCenterPos = cmds.xform('lEyePos', t = True, q = True, ws = True)
     
        if not cmds.objExists('eyeLidCrv' + self.grpSuffix):
            eyeLidCrvGrp = cmds.group(em =1, n = 'eyeLidCrv' + self.grpSuffix, p = self.crvGrp)
        
        if not cmds.objExists('eyeLidCtl' + self.grpSuffix):
            eyeLidCtlGrp = cmds.group(em =1, n = 'eyeLidCtl' + self.grpSuffix, p = 'attachCtl' + self.grpSuffix)        
      
        prefix = [self.prefix[0] + "up", self.prefix[1] + "lo" ]
        for pre in prefix:
            #- left right + upper lower prefix           
            jnts = cmds.ls(pre + "LidBlink*" + self.jntSuffix, fl =1, type="joint")
            leng = len(jnts)
            print leng    
            preR = pre.replace("l_", "r_")
            #create ctrl group 
            lLidCtlGrp = cmds.group(em=True, n = pre + "LidCtl" + self.grpSuffix, p= 'eyeLidCtl' + self.grpSuffix) 
            cmds.xform(lLidCtlGrp, ws = True, t = eyeCenterPos) 
            cmds.setAttr(lLidCtlGrp + ".ry", eyeRotY) 
            rLidCtlGrp = cmds.duplicate(lLidCtlGrp, n = preR +"LidCtl" + self.grpSuffix)
            cmds.setAttr(rLidCtlGrp[0] + ".tx", -eyeCenterPos[0])
            cmds.setAttr(rLidCtlGrp[0] + ".ry", -eyeRotY)
            cmds.setAttr(rLidCtlGrp[0] + ".sx", -1)
            
            #minYCrv /maxYCrv  
            tempMinCrv = cmds.curve(d = 3, p = [(0,0,0),(.25,0,0),(.5,0,0),(.75,0,0),(1,0,0)])
            cmds.rebuildCurve(tempMinCrv, d = 1, rt=0, kr =0, s = leng -1 )
            lMinCrv = cmds.rename(tempMinCrv,  pre[2:] +"Min" + self.crvSuffix)
                
            tempMaxCrv = cmds.curve(d = 3, p = [(0,0,0),(.25,0,0),(.5,0,0),(.75,0,0),(1,0,0)])
            cmds.rebuildCurve(tempMaxCrv, d = 1, rt=0, kr = 0, s = leng -1 ) 
            lMaxCrv = cmds.rename(tempMaxCrv, pre[2:] +"Max" + self.crvSuffix) 
     
            squintCrv = cmds.duplicate(lMaxCrv, n= pre[2:] +"Squint" + self.crvSuffix)
            annoyCrv = cmds.duplicate(squintCrv, n= pre[2:] +'Annoy' + self.crvSuffix)
            #put curves in the eyeLidCrv_grp  
            cmds.parent(lMinCrv,  lMaxCrv, squintCrv, annoyCrv, 'eyeLidCrv' + self.grpSuffix) 
                    
            #shape crvs for eyeDirections
            pushA_crv = cmds.duplicate(lMinCrv,  n = pre +'LidPushA' + self.crvSuffix)
            pushB_crv = cmds.duplicate(pushA_crv, n= pre +'LidPushB' + self.crvSuffix)
            pushC_crv = cmds.duplicate(pushA_crv, n= pre +'LidPushC' + self.crvSuffix)
            pushC_crv = cmds.duplicate(pushA_crv, n= pre +'LidPushD' + self.crvSuffix)
                    
        for lr in self.prefix:
            uploPrefix = lr + self.upDown
            if "up" in uploPrefix:      
                ty = 1               
    
            elif "lo" in uploPrefix: 
                ty = 0
                
            jnts = cmds.ls(uploPrefix + "LidBlink*" + self.jntSuffix, fl =1, type="joint")
            length = len(jnts)
            
            #eyeOpenCrv with math expression
            if not cmds.objExists(uploPrefix +"EyeOpen" + self.crvSuffix): 
                tempCrv = cmds.curve(d = 3, p = [(0,ty,0),(.25,ty,0),(.5,ty,0),(.75,ty,0),(1,ty,0) ])
                cmds.rebuildCurve(tempCrv, d = 1, rt=0, kr = 0, s = length -1 )
                openCrv = cmds.rename(tempCrv,  uploPrefix +"EyeOpen" + self.crvSuffix)
                startCrv = cmds.duplicate(openCrv, n = uploPrefix +"EyeStart" + self.crvSuffix)
                cmds.parent(openCrv,startCrv, 'eyeLidCrv' + self.grpSuffix) 
                       
            #uploPrefix / i /  ctlSize /  ctlPOC? /   
            for i in range(0, length):                  
                #eyeLid ctrls attach to body
                #- creating controller 
                if lr == self.prefix[0]:
                    cColor = 6
                else:
                    cColor = 17
                childPos = cmds.xform(cmds.listRelatives(jnts[i], c=1, type ='joint')[0], t = True, q = True, ws = True)
                lidCtl, lidCtlP  = self.circleController(uploPrefix + 'Lid'+ str(i+1).zfill(2),
                                                        'xy',
                                                        ctlSize,
                                                        color = cColor,
                                                        lockAttr = ['tz',
                                                                    'sc',
                                                                    'ro',
                                                                    'vi'])
                cmds.xform(lidCtlP, t = [childPos[0], childPos[1], childPos[2]])
                cmds.setAttr(lidCtlP + ".tz", cmds.getAttr(lidCtlP + '.tz') + ctlSize*0.2)
                #cmds.setAttr(lidCtlP + ".ry", 0)     
             
                #jumperPanel.l_upPush_Lid# define 
                '''
                LUpPush_Lid0 =  PushLid_EXP.ValA *((-jumperPanel.LLidPushX + 1) / 2 * LUpDetail0.pushA +(jumperPanel.LLidPushX + 1) / 2 * LUpDetail0.pushB) + 
                                PushLid_EXP.ValB *((-jumperPanel.LLidPushX + 1) / 2 * LUpDetail0.pushC +(jumperPanel.LLidPushX + 1) / 2 * LUpDetail0.pushD);
                '''
                AB = ['A','B'] 
                CD = ['C','D']
                lid0 = self.jumperPanelName + '.' + uploPrefix + 'Push_Lid%s'%str(i) 
                valA = self.jumperPanelName + '.' + uploPrefix[:2] + 'valA'
                valB = self.jumperPanelName + '.' + uploPrefix[:2] + 'valB'
                pushX = self.jumperPanelName + '.'+ uploPrefix[:2] + "lidPushX"
                pushA0 = self.prefix[0] + uploPrefix[2:] +'LidPush'+ AB[0] +'_crvShape.cv[%s].yValue'%str(i)  
                pushB0 = self.prefix[0] + uploPrefix[2:] +'LidPush'+ AB[1] + '_crvShape.cv[%s].yValue'%str(i)  
                pushC0 = self.prefix[0] + uploPrefix[2:] +'LidPush'+ CD[0] + '_crvShape.cv[%s].yValue'%str(i)  
                pushD0 = self.prefix[0] + uploPrefix[2:] +'LidPush'+ CD[1] + '_crvShape.cv[%s].yValue'%str(i)  
                
                pushMath = cmds.expression(n=uploPrefix+"pushCrv_math%s"%str(i+1), s=" %s=%s*((-%s+1)/2*%s +(%s+1)/2*%s) + %s*((-%s+1)/2*%s +(%s+1)/2*%s)"%(lid0, valA, pushX, pushA0, pushX, pushB0, valB, pushX, pushC0, pushX, pushD0), 
                o = self.jumperPanelName + '.' + uploPrefix + 'Push_Lid%s'%str(i), ae =1) 
        
        cornerLidGrp = cmds.group(em =1, n = 'cornerLid' + self.grpSuffix, p = 'eyeLidCtl' + self.grpSuffix)          
        corners = [self.prefix[0] + 'inner',self.prefix[0] + 'outer', self.prefix[1] + 'inner',self.prefix[1] + 'outer']
        
        for cn in corners:
            # eyeLid ctrls attach to body
            #- creating controller 
            if lr == self.prefix[0]:
                cColor = 6
            else:
                cColor = 17
            childPos = cmds.xform(cn + "Lid" + self.jntSuffix, t = True, q = True, ws = True)   
            lidCtl, lidCtlP  = self.circleController(cn + "Lid",
                                                    'xy',
                                                    ctlSize,
                                                    color = cColor,
                                                    lockAttr = ['tz',
                                                                'sc',
                                                                'ro',
                                                                'vi'])
            cmds.xform(lidCtlP, t = [childPos[0], childPos[1], childPos[2]])
            cmds.parent(lidCtlP, cornerLidGrp)
            cmds.setAttr(lidCtlP + ".tz", cmds.getAttr(lidCtlP + '.tz') + ctlSize*0.2)
            cmds.setAttr(lidCtlP + ".ry", 0)

    def createLidCtrls2(self, baseJnts):
        """
        create controller for lid
        """       
        if not(self.lEyeLoc):
            print "create the face locators"
            
        else: 
            eyeRotY = cmds.getAttr(self.lEyeLoc + '.ry') 
            eyeCenterPos = cmds.xform(self.lEyeLoc, t = True, q = True, ws = True) 
        
        allLidsCtlGrp = []
        allLidsCrvGrp  = []
        for lr in self.prefix:
            #- left right + upper lower prefix
            uploPrefix = lr + self.upDown
            
            #- creating crv group nodes
            lidCrvGrp = cmds.group(n = uploPrefix + 'crv' + self.grpSuffix, em =True)
            allLidsCrvGrp.append(lidCrvGrp)
            #topJnt = [jnt for jnt in baseJnts if jnt.startswith(lr)]
            #tempJnts = cmds.listRelatives(topJnt, ad =True)
            childJnts = cmds.ls(uploPrefix + '*%s*%s' %(self.blinkJntName, self.jntSuffix)) 
            wideJnts = cmds.ls(uploPrefix + '*%s*%s' %(self.wideJntName, self.jntSuffix))
            childJnts.sort()
            wideJnts.sort()
            jntNum = len(childJnts)
            
            #- making lids Ctrl group
            lidsCtrlGrp = cmds.group(em=True, w =True, n = uploPrefix + 'Eyelid' + self.ctlSuffix + self.grpSuffix)
            allLidsCtlGrp.append(lidsCtrlGrp)
            
            if lr == self.prefix[0]:
                cmds.xform(lidsCtrlGrp, ws = True, t = eyeCenterPos)
                cmds.setAttr(lidsCtrlGrp + ".ry", eyeRotY)
            else:
                cmds.xform(lidsCtrlGrp, ws = True, t =(-eyeCenterPos[0], eyeCenterPos[1], eyeCenterPos[2]))
                cmds.setAttr(lidsCtrlGrp + ".ry", -eyeRotY)                
            
            #- final lid shape curve
            lidCrv = cmds.curve(d = 3, p =([0,0,0],[0.33,0,0],[0.66,0,0],[1,0,0])) 
            cmds.rebuildCurve(rt = 0, d = 1, kr = 0, s = jntNum-1)  
            tempCrv = cmds.rename(lidCrv, uploPrefix +'Lid' + self.crvSuffix)
            cmds.parent(tempCrv, lidCrvGrp)
            lidCrvShape = cmds.listRelatives(tempCrv, c = True)
            
            wideJntCrv = cmds.duplicate(tempCrv, n= uploPrefix +'WideJnt' + self.crvSuffix) 
            wideJntCrvShape = cmds.listRelatives(wideJntCrv, c = True) 

            #- eyelids controller curve shape(different number of points, so can not be target of the blendShape)      
            lidCtlCrv = cmds.curve(d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0], [1,0,0]))
            #- rebuildCurve? 
            #cmds.rebuildCurve(rt = 0, d = 1, kr = 0, s = jntNum-1)  
            tempCtlCrv = cmds.rename(lidCtlCrv, uploPrefix +'Ctl' + self.crvSuffix)
            lidCtlCrvShape = cmds.listRelatives(tempCtlCrv, c = True) 
            cmds.parent(tempCtlCrv, lidCrvGrp) 

            #- eyeClose(blink) lid shape        
            blinkCrv = cmds.duplicate(tempCrv, n= uploPrefix +'Blink' + self.crvSuffix)
            
            #- eyeWide(suprise) lid shape        
            wideCrv = cmds.duplicate(tempCrv, n= uploPrefix +'Wide' + self.crvSuffix)
                        
            #- eyeSquint lid shape        
            squintCrv = cmds.duplicate(tempCrv, n= uploPrefix +'Squint' + self.crvSuffix) 
                        
            if lr == self.prefix[1]: 
                cmds.hide(blinkCrv, wideCrv, squintCrv)
                        
            #- eyeDirection lid shape        
            lookUp = cmds.duplicate(tempCrv, n= uploPrefix +'LookUp' + self.crvSuffix) 


            lookDn = cmds.duplicate(tempCrv, n= uploPrefix +'LookDn' + self.crvSuffix) 
            lookLeft = cmds.duplicate(tempCrv, n= uploPrefix +'LookLeft' + self.crvSuffix)                 
            lookRight = cmds.duplicate(tempCrv, n= uploPrefix +'LookRight' + self.crvSuffix) 

            crvBS = cmds.blendShape(blinkCrv[0], lookUp[0], lookDn[0], lookLeft[0], lookRight[0], tempCrv, n = uploPrefix + 'LidCrvBS')
            cmds.blendShape(crvBS[0], edit=True, w=[(0, 1),(1, 1),(2, 1),(3, 1),(4, 1)])
              
            wideBS = cmds.blendShape(wideCrv[0], squintCrv[0], wideJntCrv, n = uploPrefix + 'WideJntBS')
            cmds.blendShape(wideBS[0], edit=True, w=[(0, 1),(1, 1)])
            
            index = 0 
            indices = 0

            for jnt in childJnts:
                miValue = 1
                wideJnt = wideJnts[index]
                childJnt = cmds.listRelatives(jnt, c =True)
                childPos = cmds.xform(childJnt[0], t = True, q = True, ws = True)
                jntIndex = jnt.split(self.jntSuffix)[0].split('Blink')[1]
                #pocNode on the final lid curve 
                pocNode = cmds.shadingNode('pointOnCurveInfo', asUtility=True, n = uploPrefix + 'Poc' + jntIndex)
                cmds.connectAttr(lidCrvShape[0] + ".worldSpace",  pocNode + '.inputCurve')   
                cmds.setAttr(pocNode + '.turnOnPercentage', 1)        
                increment = 1.0/(jntNum-1)
                cmds.setAttr(pocNode + '.parameter', increment *index)     
                initialX = cmds.getAttr(pocNode + '.positionX')
                
                #- pocNode on the wideJnt curve
                wideJntPocNode = cmds.shadingNode('pointOnCurveInfo', asUtility=True, n = uploPrefix + 'wideJntPoc' + jntIndex)
                cmds.connectAttr(wideJntCrvShape[0] + ".worldSpace",  wideJntPocNode + '.inputCurve')   
                cmds.setAttr(wideJntPocNode + '.turnOnPercentage', 1)        
                cmds.setAttr(wideJntPocNode + '.parameter', increment *index)  
                
                #- pocNode on the eyelids ctls curve
                ctlPocNode = cmds.shadingNode('pointOnCurveInfo', asUtility=True, n = uploPrefix + 'CtlPoc' + jntIndex)
                cmds.connectAttr(lidCtlCrvShape[0] + ".worldSpace", ctlPocNode + '.inputCurve')   
                cmds.setAttr(ctlPocNode + '.turnOnPercentage', 1)        
                cmds.setAttr(ctlPocNode + '.parameter', increment *index) 
                
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
                cmds.parent(lidCtlP, lidsCtrlGrp)

                index = index + 1
                
                self.crvCtrlToJnt(uploPrefix, lidCtl, jnt, wideJnt, pocNode, wideJntPocNode, ctlPocNode, initialX, self.rotateScale , miValue, index)
    
        return {'lidsCtlGrp' : allLidsCtlGrp, 'lidsCrvGrp' : allLidsCrvGrp, 'numJnts' : jntNum}
        
    def connectToPanel(self, jntNum):
        """
        make panel live to control eyelid
        """
        self.createLidCtl(jntNum)
        self.lidControlConnect()