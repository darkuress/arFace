#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright (c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

# brow joints create
'''select left brow vertex points and pivot point. run the script
  name = centerBrowBase0l, EyeBrowBase01... '''

import maya.cmds as cmds
import Func
reload(Func)
import re

class Ctrls(Func.Func):
    def __init__(self, size, offset, rotateScale, **kw):
        """
        initializing variables
        """
        self.initialX         = 0
        self.size             = size
        self.offset           = offset
        self.rotateScale      = rotateScale
        
        #- initializing Func
        Func.Func.__init__(self, self.rotateScale, **kw)

    def createBrowCtrls(self, jnts):
        """
        create and connect brow ctrl
        """
        x, y, z, orderJnts = self.orderJnts(jnts)
        jntNum = len(orderJnts)
        reverseMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = 'browReverse_mult')
        cmds.connectAttr(self.faceFactors + '.browRotateX_scale',  reverseMult + '.input1X')
        cmds.setAttr(reverseMult + '.input2X', -1)
        cmds.connectAttr(self.faceFactors +  '.browRotateY_scale', reverseMult + '.input1Y')
        cmds.setAttr(reverseMult + '.input2Y', -1)
        
        if cmds.objExists(self.browCrvGrp):
            cmds.delete(self.browCrvGrp)        
        if not cmds.objExists(self.attachCtlGrp):
            attachCtlGrp = cmds.group(n = self.attachCtlGrp, em =True, p = self.bodyHeadTRS) 
        if cmds.objExists(self.browCtlGrp):
            cmds.delete(self.browCtlGrp)
            
        browCtlGrp = cmds.group(n = self.browCtlGrp, em =True, p = self.attachCtlGrp)    
        browCrvGrp = cmds.group(n = self.browCrvGrp, em =True, p = self.crvGrp) 
        tempBrowCrv = cmds.curve(d = 1, p =([-1,0,0],[-0.5,0,0],[0,0,0],[0.5,0,0],[1,0,0])) 
        cmds.rebuildCurve(tempBrowCrv, rebuildType = 0, spans = jntNum-1, keepRange = 0, degree = 1)    
        browCrv = cmds.rename(tempBrowCrv, 'brow' + self.crvSuffix)    
        browCrvShape = cmds.listRelatives(browCrv, c = True)
        cmds.parent(browCrv, self.browCrvGrp)     
    
        # lipTarget curve shape
        lBrowSadCrv = cmds.duplicate(browCrv, n= 'lBrowSad' + self.crvSuffix)
        rBrowSadCrv = cmds.duplicate(browCrv, n= 'rBrowSad' + self.crvSuffix)
        lBrowMadCrv = cmds.duplicate(browCrv, n= 'lBrowMad' + self.crvSuffix)
        rBrowMadCrv = cmds.duplicate(browCrv, n= 'rBrowMad' + self.crvSuffix)
        lFurrowCrv = cmds.duplicate(browCrv, n= 'lFurrow' + self.crvSuffix)
        rFurrowCrv = cmds.duplicate(browCrv, n= 'rFurrow' + self.crvSuffix)
        lRelaxCrv = cmds.duplicate(browCrv, n= 'lRelax' + self.crvSuffix)
        rRelaxCrv = cmds.duplicate(browCrv, n= 'rRelax' + self.crvSuffix)      
        lCrv = [lBrowSadCrv[0], lBrowMadCrv[0], lFurrowCrv[0], lRelaxCrv[0] ]    
        rCrv = [rBrowSadCrv[0], rBrowMadCrv[0], rFurrowCrv[0], rRelaxCrv[0] ]        
        crvLen = len(lCrv)
        
        browBS = cmds.blendShape(lBrowSadCrv[0],rBrowSadCrv[0], lBrowMadCrv[0],rBrowMadCrv[0], lFurrowCrv[0],rFurrowCrv[0], lRelaxCrv[0],rRelaxCrv[0], browCrv, n ='browBS')
        cmds.blendShape( browBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3,1),(4, 1), (5,1),(6, 1), (7,1) ])  
        self.LRBlendShapeWeight( browCrv, browBS[0])
        
        tempCtlCrv = cmds.curve(d = 2, p =([-1,0,0],[-0.5,0,0],[0,0,0],[0.5,0,0],[1,0,0]))
        browCtlCrv = cmds.rename (tempCtlCrv, self.browCtlCrvName) 
        cmds.rebuildCurve(browCtlCrv, rebuildType = 0, spans = 4, keepRange = 0, degree = 3) 
        browCtlCrvShape = cmds.listRelatives(browCtlCrv, c = True) 
        cmds.parent(browCtlCrv, self.browCrvGrp) 
        
        sumX = cmds.shadingNode('plusMinusAverage', asUtility =True, n = 'browTX_sum')
        cmds.setAttr(sumX + '.operation', 1)
        
        #connect browMain Ctrls to browCrv
        sequence =['A', 'B', 'C', 'D', 'E']
        cvs= cmds.ls(self.browCtlCrvName + ".cv[*]", fl=True)
        cvBX = cmds.getAttr(cvs[2] + '.xValue')
        cvDX = cmds.getAttr(cvs[4] + '.xValue')
        cmds.connectAttr('brow_arcB.tx', sumX + '.input2D[0].input2Dx')
        cmds.setAttr(sumX + '.input2D[1].input2Dx', cvBX)
        cmds.connectAttr(sumX + '.output2D.output2Dx', cvs[2] + '.xValue')
        cmds.connectAttr('brow_arcD.tx', sumX + '.input2D[0].input2Dy')
        cmds.setAttr(sumX + '.input2D[1].input2Dy', cvDX)
        cmds.connectAttr(sumX + '.output2D.output2Dy', cvs[4] + '.xValue')
        cmds.connectAttr ('brow_arcA.ty',  cvs[0] + '.yValue')
        cmds.connectAttr ('brow_arcE.ty',  cvs[6] + '.yValue')
        
        for num in range (1, 6):    
            cmds.connectAttr ('brow_arc' + sequence[num-1] + '.ty',  cvs[num] + '.yValue')    

        #- create detail Control in panel
        self.createBrowCtl(jntNum, orderJnts)

        browDMom = cmds.ls('browDetail*P', fl =True, type = "transform")
        browDetails = cmds.listRelatives(browDMom, c=True, type = "transform") 

        allBrowCtlGrp = []
        allBrowCrvGrp  = [browCrv]

        index = 0 
        for jnt in orderJnts:           
            basePos = cmds.xform( jnt, t = True, q = True, ws = True)
            rotYJnt = cmds.listRelatives(jnt, c=True)
            rotYJntPos = cmds.xform(rotYJnt[0], t = True, q = True, ws = True)  
            childJnt = cmds.listRelatives( rotYJnt[0], c =1)  
            jntPos = cmds.xform(childJnt[0], t = True, q = True, ws = True)
            browDetail = browDetails[index]
            #point on shapeCrv 
            shapePOC = cmds.shadingNode('pointOnCurveInfo', asUtility=True, n = 'browShapePOC'+ str(index+1).zfill(2))
            cmds.connectAttr(browCrvShape[0] + ".worldSpace",  shapePOC + '.inputCurve')
            cmds.setAttr(shapePOC + '.turnOnPercentage', 1)
            increment = 1.0/(jntNum-1)        
            cmds.setAttr(shapePOC + '.parameter', increment *index)
            #point on freeform crv
            POC = cmds.shadingNode('pointOnCurveInfo', asUtility=True, n = 'eyeBrowPOC'+ str(index+1).zfill(2))
            cmds.connectAttr(browCtlCrvShape[0] + ".worldSpace",  POC + '.inputCurve')
            cmds.setAttr(POC + '.turnOnPercentage', 1)
            increment = 1.0/(jntNum-1)        
            cmds.setAttr(POC + '.parameter', increment *index)
            # browCrv controls browDetail parent 
            cmds.connectAttr(POC + ".positionY", browDMom[index] + ".ty" )        
            initialX = cmds.getAttr (POC + '.positionX')
            
            attrs = ["sx","sy","sz","v"]        
            
            ctlName = jnt.split(self.jntSuffix)[0] + self.ctlSuffix
            if jnt in x :
                #rBrowCtrl = controller( self.prefix[1] + 'brow'+ str(re.findall('\d+', jnt)[0]) + "_ctl",(jntPos[0], jntPos[1], jntPos[2]+ self.offset), self.size, 'cc')
                rBrowCtrl, ctlP = self.circleController(ctlName,
                                        'xy',
                                        self.size*0.2,
                                        color = 17,
                                        lockAttr = [])
                cmds.xform(ctlP, t = [jntPos[0], jntPos[1], jntPos[2]+ self.offset])
                zeroGrp = cmds.duplicate(ctlP, po =1, n = ctlP.replace(self.grpSuffix,"_dummy"))
                cmds.parent(ctlP, zeroGrp[0])
                rotYGrp = cmds.group(em =1, n = rBrowCtrl.replace(self.ctlSuffix, "_browRY"), p = self.browCtlGrp)
                cmds.xform(rotYGrp, ws = True, t = rotYJntPos) 
                cmds.parent(zeroGrp[0], rotYGrp) 
                ctlBase = cmds.group(em =1, n = ctlP.replace(self.grpSuffix,"_base"), p = self.browCtlGrp) 
                cmds.xform(ctlBase, ws = True, t = basePos)            
                cmds.parent(rotYGrp, ctlBase)
                for att in attrs:            
                    cmds.setAttr(rBrowCtrl + ".%s"%att, lock =1, keyable = 0)
                self.crvCtrlToJnt(rBrowCtrl, browDetail, jnt, rotYJnt[0], ctlBase, rotYGrp, shapePOC, POC, initialX, index)
                allBrowCtlGrp.append(ctlP)
                
            elif jnt in y :
                #lBrowCtrl = controller( self.prefix[0] + 'brow'+ str(re.findall('\d+', jnt)[0]) + "_ctl",(jntPos[0], jntPos[1], jntPos[2]+ self.offset), self.size, 'cc')
                lBrowCtrl, ctlP = self.circleController(ctlName,
                                                        'xy',
                                                        self.size*0.2,
                                                        color = 6,
                                                        lockAttr = [])
                cmds.xform(ctlP, t = [jntPos[0], jntPos[1], jntPos[2]+ self.offset])
                zeroGrp = cmds.duplicate(ctlP, po =1, n = ctlP.replace(self.grpSuffix,"_dummy"))
                cmds.parent( ctlP, zeroGrp[0])
                rotYGrp = cmds.group( em =1, n = lBrowCtrl.replace(self.ctlSuffix, "_browRY"), p = self.browCtlGrp)
                cmds.xform(rotYGrp, ws = True, t = rotYJntPos)
                cmds.parent(zeroGrp[0], rotYGrp)
                ctlBase = cmds.group( em =1, n = ctlP.replace(self.grpSuffix,"_base"), p = self.browCtlGrp) 
                cmds.xform(ctlBase, ws = True, t = basePos)
                cmds.parent(rotYGrp, ctlBase)
                for att in attrs:            
                    cmds.setAttr(lBrowCtrl + ".%s"%att, lock =1, keyable = 0)
                self.crvCtrlToJnt(lBrowCtrl, browDetail, jnt, rotYJnt[0], ctlBase, rotYGrp, shapePOC, POC, initialX, index )
                allBrowCtlGrp.append(ctlP)
                
            elif jnt == z[0] :            
                #cBrowCtrl = controller( self.cPrefix + 'brow_ctl',(jntPos[0], jntPos[1], jntPos[2]+ self.offset), self.size, 'cc')
                cBrowCtrl, ctlP = self.circleController(ctlName,
                                                        'xy',
                                                        self.size*0.2,
                                                        color = 8,
                                                        lockAttr = [])
                cmds.xform(ctlP, t = [jntPos[0], jntPos[1], jntPos[2]+ self.offset])
                zeroGrp = cmds.duplicate(ctlP, po =1, n = ctlP.replace(self.grpSuffix,"_dummy"))
                cmds.parent( ctlP, zeroGrp[0])
                rotYGrp = cmds.group( em =1, n = cBrowCtrl.replace(self.ctlSuffix, "_browRY"), p = self.browCtlGrp)
                cmds.xform (rotYGrp, ws = True, t = rotYJntPos)
                ctlBase = cmds.group( em =1, n = ctlP.replace(self.grpSuffix,"_base"), p = self.browCtlGrp) 
                cmds.xform (ctlBase, ws = True, t = basePos)
                cmds.parent(zeroGrp[0], rotYGrp)
                cmds.parent(rotYGrp, ctlBase)
                for att in attrs:            
                    cmds.setAttr(cBrowCtrl + ".%s"%att, lock =1, keyable = 0)
                self.crvCtrlToJnt(cBrowCtrl, browDetail, jnt, rotYJnt[0], ctlBase, rotYGrp, shapePOC, POC, initialX, index)
                allBrowCtlGrp.append(ctlP)
                
            index = index + 1
        
        return {'browsCtlGrp' : allBrowCtlGrp, 'browsCrvGrp' : allBrowCrvGrp, 'numJnts' : jntNum, 'orderJnts' : orderJnts}
                
    def ccreateBrowCtrls(self, jnts):
        """
        select base joints and run the script
        """
        #jnts = cmds.ls(os = True, fl = True, type ='joint') 
        jntNum = len(jnts)
        jnts.sort()
        cJnt = [x for x in jnts if x.startswith(self.cPrefix)]
        lJnt = [x for x in jnts if x.startswith(self.prefix[0])]
        rJnt = [x for x in jnts if x.startswith(self.prefix[1])]
        rJnt.reverse()
        orderJnts = rJnt + cJnt + lJnt 
        
        basePos = cmds.xform( cJnt, t = True, q = True, ws = True)  
        
        browCrv = cmds.curve (n = self.browCtlCrvName, d = 2, p =([-1,0,0],[-0.5,0,0],[0,0,0],[0.5,0,0],[1,0,0]))
        cmds.rebuildCurve (browCrv, rebuildType = 0, spans = 4, keepRange = 0, degree = 3) 
        browCrvShape = cmds.listRelatives(browCrv, c = True) 

        allBrowCtlGrp = []
        allBrowCrvGrp  = [browCrv]
        
        #- create detail Control in panel
        self.createBrowCtl(jntNum, orderJnts)
        
        index = 0 
        for jnt in orderJnts:
            childJnt = cmds.listRelatives(jnt, c=True) 
            jntPos = cmds.xform(childJnt[0], t = True, q = True, ws = True) 
            self.pocNode = cmds.shadingNode('pointOnCurveInfo', asUtility=True, n = 'eyeBrowself.pocNode'+ str(index))
            cmds.connectAttr(browCrvShape[0] + ".worldSpace",  self.pocNode + '.inputCurve')
            cmds.setAttr(self.pocNode + '.turnOnPercentage', 1)
            increment = 1.0/(jntNum-1)
            cmds.setAttr(self.pocNode + '.parameter', increment *index)
            initialX = cmds.getAttr (self.pocNode + '.positionX')
            
            ctlName = jnt.split(self.jntSuffix)[0] + self.ctlSuffix
            
            if jnt in rJnt:
                rBrowCtrl, null = self.circleController(ctlName,
                                                        'xy',
                                                        self.size*0.2,
                                                        color = 17,
                                                        lockAttr = [])
                cmds.xform(null, ws = True, t = basePos)
                cmds.xform(rBrowCtrl, ws = True, t =(jntPos[0], jntPos[1], jntPos[2]+ self.offset))
                
                cmds.makeIdentity (null, apply=True, t=True, r=True, s=True, n =False) 
                self.crvCtrlToJnt (rBrowCtrl, jnt, null, self.pocNode, initialX, index, self.rotateScale)
                allBrowCtlGrp.append(null)
                
            elif jnt in lJnt :
                lBrowCtrl, null = self.circleController(ctlName,
                                                        'xy',
                                                        self.size*0.2,
                                                        color = 6,
                                                        lockAttr = [])
                cmds.xform(null, ws = True, t = basePos)
                cmds.xform(lBrowCtrl, ws = True, t =(jntPos[0], jntPos[1], jntPos[2]+ self.offset))
                
                cmds.makeIdentity (null, apply = True, t = True, r = True, s = True, n = False) 
                self.crvCtrlToJnt (lBrowCtrl, jnt, null, self.pocNode, initialX, index, self.rotateScale)
                allBrowCtlGrp.append(null)
                
            else :
                cBrowCtrl = cmds.spaceLocator(n = ctlName, p =(0,0,0)) 
                cmds.setAttr(cBrowCtrl[0]+'Shape.localScaleX', self.size * 0.3)
                cmds.setAttr(cBrowCtrl[0]+'Shape.localScaleY', self.size * 0.3)
                cmds.setAttr(cBrowCtrl[0]+'Shape.localScaleZ', self.size * 0.3)
                null = cmds.group (em=True, w =True, n = cBrowCtrl[0] + "P")
                cmds.xform(null, ws = True, t = basePos)
                cmds.xform(cBrowCtrl[0], ws = True, t =(jntPos[0], jntPos[1], jntPos[2]+ self.offset))
                cmds.parent(cBrowCtrl[0], null) 
                cmds.makeIdentity (null, apply=True, t=True, r=True, s=True, n =False) 
                self.crvCtrlToJnt(cBrowCtrl[0], jnt, null, self.pocNode, initialX, index, self.rotateScale)
                allBrowCtlGrp.append(null)
            
            index = index + 1
            
        return {'browsCtlGrp' : allBrowCtlGrp, 'browsCrvGrp' : allBrowCrvGrp, 'numJnts' : jntNum, 'orderJnts' : orderJnts}


    def connectToPanel(self):
        """
        make panel live to control eyelid
        """
        self.browControlConnect()