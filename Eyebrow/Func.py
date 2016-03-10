#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright(c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

# brow joints create
'''select left brow vertex points and pivot point. run the script
  name = centerBrowBase0l, EyeBrowBase01... '''

import maya.cmds as cmds
import Base
reload(Base)

class Func(Base.Base):
    def __init__(self, rotateScale, **kw):
        """
        initializing variables
        """
        #local variables
        Base.Base.__init__(self, **kw)

    def crvCtrlToJnt(self, browCtrl, jnt, ctrlP, pocNode, initialX, index, rotateScale):
        #connect browCtrlCurve and controller to the brow joints
        
        #- temp way
        browDMom = cmds.ls('browDetail*P', fl =True, type = "transform")
        browDetails = cmds.listRelatives(browDMom, c=True, type = "transform")
        browDetail = browDetails[index]
        
        ctrlMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = jnt.split('Base', 1)[0] +'CtrlMult'+ str(index))
        crvMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = jnt.split('Base', 1)[0] +'CrvMult'+ str(index))
        browSumY = cmds.shadingNode('plusMinusAverage', asUtility=True, n = jnt.split('Base', 1)[0] +'YSum'+ str(index))
        browSumX = cmds.shadingNode('plusMinusAverage', asUtility=True, n = jnt.split('Base', 1)[0] +'XSum'+ str(index))
        minusAvgX = cmds.shadingNode('plusMinusAverage', asUtility=True, n = jnt.split('Base', 1)[0] +'Xminus'+ str(index))
        xyTotal = cmds.shadingNode('plusMinusAverage', asUtility=True, n = jnt.split('Base', 1)[0] +'XYtotal'+ str(index))
         
        cmds.connectAttr(browCtrl + '.tx', browSumX + '.input1D[0]')
        cmds.connectAttr(browCtrl + '.ty', browSumY + '.input1D[0]')
        cmds.connectAttr(browDetail + '.tx', browSumX + '.input1D[1]')
        cmds.connectAttr(browDetail + '.ty', browSumY + '.input1D[1]')
    
        #browCrv's pocNode.tx zero out 
        cmds.connectAttr(pocNode + '.positionX', minusAvgX + '.input1D[1]')
        cmds.setAttr(minusAvgX + '.input1D[2]', -initialX)
        cmds.connectAttr(minusAvgX + '.output1D', crvMult + '.input1X')
        cmds.connectAttr(pocNode + '.positionY', crvMult + '.input1Y')
        cmds.setAttr(crvMult + '.input2X', rotateScale)
        cmds.setAttr(crvMult + '.input2Y', -rotateScale)
        cmds.connectAttr(crvMult + ".outputX", ctrlP + '.ry')
        cmds.connectAttr(crvMult + ".outputY", ctrlP + '.rx')
        #X total
        cmds.connectAttr(browSumX + '.output1D', xyTotal + '.input2D[0].input2Dx')
        cmds.connectAttr(minusAvgX + '.output1D', xyTotal + '.input2D[1].input2Dx')
        #Y total
        cmds.connectAttr(browSumY + '.output1D', xyTotal + '.input2D[0].input2Dy')   
        cmds.connectAttr(pocNode + '.positionY', xyTotal + '.input2D[1].input2Dy')  
        
        cmds.connectAttr(xyTotal + '.output2Dx', ctrlMult + '.input1X')
        cmds.connectAttr(xyTotal + '.output2Dy', ctrlMult + '.input1Y')
        cmds.setAttr(ctrlMult + '.input2X', rotateScale)
        cmds.setAttr(ctrlMult + '.input2Y', -rotateScale)
            
        cmds.connectAttr(ctrlMult + '.outputX', jnt + '.ry')
        cmds.connectAttr(ctrlMult + '.outputY', jnt + '.rx')

    def createBrowCtl(self, miNum, orderJnts):
        """
        create extra controllor for the panel
        """
        jntNum             = miNum
        ctlP               = "browDetailCtrl0"
        browDetailBaseName = 'browDetail'
        kids = cmds.listRelatives(ctlP, ad=True, type ='transform')   
        if kids:
            cmds.delete(kids)
            
        attTemp = ['scaleX','scaleY','scaleZ', 'rotateX','rotateY','rotateZ', 'tz', 'visibility']  
        index = 0
        for jnt in orderJnts:
            #- create detail control in panel                
            detailCtl = cmds.circle(n = browDetailBaseName + str(index+1).zfill(2), ch=False, o =True, nr =(0, 0, 1), r = 0.2)
            detailPlane = cmds.nurbsPlane(ax =(0, 0, 1), w = 0.1,  lengthRatio = 10, degree = 3, ch = False, n = browDetailBaseName + str(index+1).zfill(2) + 'P')
            increment = 2.0/(jntNum-1)
            cmds.parent(detailCtl[0], detailPlane[0], relative=True)
            cmds.parent(detailPlane[0], ctlP, relative=True)
            cmds.setAttr(detailPlane[0] + '.tx', -2 + increment*index*2)
            cmds.xform(detailCtl[0], r =True, s =(0.2, 0.2, 0.2))  
            cmds.setAttr(detailCtl[0] + ".overrideEnabled", 1)
            cmds.setAttr(detailCtl[0] + "Shape.overrideEnabled", 1)
            cmds.setAttr(detailCtl[0] + "Shape.overrideColor", 20)        
            
            cmds.transformLimits(detailCtl[0] , tx =(-.4, .4), etx=(True, True))
            cmds.transformLimits(detailCtl[0], ty =(-.8, .8), ety=(True, True))
            
            for att in attTemp:
                cmds.setAttr(detailCtl[0] +"."+ att, lock = True, keyable = False, channelBox =False)
                    
            index = index + 1

    def browControlConnect(self):
        """
        connect brow control with panel
        """
        #connect browMain Ctrls to browCrv
        sumX = cmds.shadingNode('plusMinusAverage', asUtility =True, n = 'browTX_sum')
        cmds.setAttr(sumX + '.operation', 1)
        
        sequence = ['A', 'B', 'C', 'D', 'E']
        cvs= cmds.ls(self.browCtlCrvName + '.cv[*]', fl=True)
        cvBX = cmds.getAttr(cvs[2] + '.xValue')
        cvDX = cmds.getAttr(cvs[4] + '.xValue')
        cmds.connectAttr('brow_arcB.tx', sumX + '.input2D[0].input2Dx')
        cmds.setAttr(sumX + '.input2D[1].input2Dx', cvBX)
        cmds.connectAttr(sumX + '.output2D.output2Dx', cvs[2] + '.xValue')
        cmds.connectAttr('brow_arcD.tx', sumX + '.input2D[0].input2Dy')
        cmds.setAttr(sumX + '.input2D[1].input2Dy', cvDX)
        cmds.connectAttr(sumX + '.output2D.output2Dy', cvs[4] + '.xValue')
        cmds.connectAttr('brow_arcA.ty',  cvs[0] + '.yValue')
        cmds.connectAttr('brow_arcE.ty',  cvs[6] + '.yValue')
        
        for num in range(1, 6):
            
            cmds.connectAttr('brow_arc' + sequence[num-1] + '.ty',  cvs[num] + '.yValue')