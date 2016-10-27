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

class Joints(Func.Func):
    def __init__(self, **kw):
        """
        initializing variables
        """
        #- local variables
        Func.Func.__init__(self, **kw)
        
        self.allBaseJnts = list()

    def createJnts(self, upLow, locData = ''):
        """
        creating joints
        """
        if locData:
            self.locData        = locData
            #- lip joints and location position
            self.lipEPos        = self.locData['setupLoc']['lipEPos']
            self.lipWPos        = [-self.lipEPos[0], self.lipEPos[1], self.lipEPos[2]]
            self.lipNPos        = self.locData['setupLoc']['lipNPos']
            self.lipSPos        = self.locData['setupLoc']['lipSPos']
            self.lipYPos        = self.locData['setupLoc']['lipYPos']
            self.jawRigPos      = self.locData['setupLoc']['jawRigPos']
            self.cheekPos       = self.locData['setupLoc']['cheekPos']
            self.squintPuffPos  = self.locData['setupLoc']['squintPuffPos']
            self.lowCheekPos    = self.locData['setupLoc']['lowCheekPos']
    
            self.uplipVtxs    = eval(self.locData['upLipVtxs'])
            self.lolipVtxs    = eval(self.locData['loLipVtxs'])
            self.uplipVtxs    = self.sortSelected(self.uplipVtxs)
            self.lolipVtxs    = self.sortSelected(self.lolipVtxs)            
            
        if upLow == self.uploPrefix[0]:
            verts = self.uplipVtxs
        elif upLow == self.uploPrefix[1]:
            verts = self.lolipVtxs
        vNum = len(verts)# + 2       
        
        if upLow == self.uploPrefix[0]:
            lipCntPos = self.lipNPos
            #vMin = 0
            #vMax = vNum
                
        elif upLow == self.uploPrefix[1]:
            lipCntPos = self.lipSPos

        vMin = 0
        vMax = vNum
        
        #increment = 1.0/(vNum-1)
        #
        #- create lip joint guide curve
        tempCrv       = cmds.curve(d= 3, ep= [(-self.lipEPos[0], self.lipEPos[1], self.lipEPos[2]),(lipCntPos),(self.lipEPos)]) 
        guideCrv      = cmds.rename(tempCrv, upLow + "Guide" + self.crvSuffix)
        guideCrvShape = cmds.listRelatives(guideCrv, c = True) 
        cmds.rebuildCurve(guideCrv, d = 3, rebuildType = 0, keepRange = 0) 
                
        #- final lip shape ctrl curve
        templipCrv    = cmds.curve(d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
        cmds.rebuildCurve(rt = 0, d = 3, kr = 0, s = 4)    
        lipCrv        = cmds.rename(templipCrv, upLow + 'Lip' + self.crvSuffix)
        lipCrvShape   = cmds.listRelatives(lipCrv, c = True)
        lipCrvGrp     = self.group([lipCrv, guideCrv], upLow + 'LipCrv' + self.grpSuffix)

        #- lip curve for LipJotX tx,ty for UDLR ctrl
        tempTyCrv = cmds.curve(d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
        cmds.rebuildCurve(rt = 0, d = 3, kr = 0, s = 4)    
        tyLipCrv = cmds.rename(tempTyCrv, upLow +'TyLip' + self.crvSuffix) 
        tylipCrvShape = cmds.listRelatives(tyLipCrv, c = True) 
        cmds.parent(tyLipCrv, lipCrvGrp)

        
        #- lipTarget curve shape
        lUpLow = self.prefix[0] + upLow
        rUpLow = self.prefix[1] + upLow
        
        jawOpenCrv = cmds.duplicate(lipCrv,     n = upLow + 'JawOpen' + self.crvSuffix)
        
        lLipWideCrv   = cmds.duplicate(lipCrv,  n = lUpLow + 'lipWide' + self.crvSuffix)
        rLipWideCrv   = cmds.duplicate(lipCrv,  n = rUpLow + 'lipWide' + self.crvSuffix)
        self.mirrorCurve(lLipWideCrv[0], rLipWideCrv[0])
        cmds.hide(rLipWideCrv[0])
        
        lLipECrv      = cmds.duplicate(lipCrv,  n = lUpLow + 'lipE' + self.crvSuffix)
        rLipECrv      = cmds.duplicate(lipCrv,  n = rUpLow + 'lipE' + self.crvSuffix)  
        self.mirrorCurve(lLipECrv[0], rLipECrv[0])
        cmds.hide(rLipECrv[0])
        
        lUCrv         = cmds.duplicate(lipCrv,  n = lUpLow + 'U' + self.crvSuffix)
        rUCrv         = cmds.duplicate(lipCrv,  n = rUpLow + 'U' + self.crvSuffix) 
        self.mirrorCurve(lUCrv[0], rUCrv[0])
        cmds.hide(rUCrv[0])
        
        lOCrv         = cmds.duplicate(lipCrv,  n = lUpLow + 'O' + self.crvSuffix) 
        rOCrv         = cmds.duplicate(lipCrv,  n = rUpLow + 'O' + self.crvSuffix)
        self.mirrorCurve(lOCrv[0], rOCrv[0])
        cmds.hide(rOCrv[0])
        
        lHappyCrv  = cmds.duplicate(lipCrv,    n = lUpLow + 'Happy' + self.crvSuffix) 
        rHappyCrv  = cmds.duplicate(lipCrv,    n = rUpLow + 'Happy' + self.crvSuffix)
        self.mirrorCurve(lHappyCrv[0], rHappyCrv[0])
        cmds.hide(rHappyCrv[0])
        
        lSadCrv    = cmds.duplicate(lipCrv,    n = lUpLow + 'Sad' + self.crvSuffix) 
        rSadCrv    = cmds.duplicate(lipCrv,    n = rUpLow + 'Sad' + self.crvSuffix) 
        self.mirrorCurve(lSadCrv[0], rSadCrv[0])
        cmds.hide(rSadCrv[0])
        
        lipCrvBS = cmds.blendShape(jawOpenCrv[0],
                                   lLipWideCrv[0],rLipWideCrv[0],
                                   lLipECrv[0],rLipECrv[0],
                                   lUCrv[0], rUCrv[0],
                                   lOCrv[0], rOCrv[0],
                                   lHappyCrv[0],rHappyCrv[0],
                                   lSadCrv[0],rSadCrv[0],
                                   lipCrv, n = upLow + 'LipCrvBS')
        cmds.blendShape(lipCrvBS[0],
                        edit=True,
                        w=[(0, 1),(1, 1),(2, 1),(3, 1),(4, 1),(5, 1),(6, 1),(7, 1),(8, 1),(9, 1),(10, 1),(11, 1),(12, 1)])

        #- lip freeform Ctrls curve(different number of points(4), so can not be target of the blendShape)      
        templipCtlCrv = cmds.curve(d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
        cmds.rebuildCurve(rt = 0, d = 3, kr = 0, s = 4)   
        lipCtlCrv = cmds.rename(templipCtlCrv, upLow +'LipCtl' + self.crvSuffix)
        lipCtlCrvShape = cmds.listRelatives(lipCtlCrv, c = True) 
        cmds.parent(lipCtlCrv, lipCrvGrp) 

        # lip Roll control curve shape(different number of points(4), so can not be target of the blendShape)      
        tempRollCrv = cmds.curve(d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
        cmds.rebuildCurve(rt = 0, d = 3, kr = 0, s = 2)   
        lipRollCrv = cmds.rename(templipCtlCrv, upLow + 'LipRoll' + self.crvSuffix)  
        lipRollCrvShape = cmds.listRelatives(lipRollCrv, c = True) 
        cmds.parent(lipRollCrv, lipCrvGrp) 

        #lip RollYZ control curve shape
        lipRollYZCrv = cmds.duplicate(lipRollCrv, n= upLow +'RollYZ' + self.crvSuffix)
        lipRollYZCrvShape = cmds.listRelatives(lipRollYZCrv, c = True)

        if not cmds.objExists(self.cheekCrvGrp):
            cheekCrvGrp = cmds.group(n = self.cheekCrvGrp, em =True, p = 'faceMain|crv_grp') 

            cheekTempCrv = cmds.curve(d=1, p = [(self.lowCheekPos),(self.lipEPos),(self.cheekPos),(self.squintPuffPos)]) 
            lCheekCrv = cmds.rename(cheekTempCrv, self.prefix[0] + "cheek" + self.crvSuffix)
            rCheekCrv = cmds.duplicate(lCheekCrv, n = self.prefix[1] + "cheek" + self.crvSuffix)
            cmds.setAttr(rCheekCrv[0] + '.scaleX', -1)
            cmds.parent(lCheekCrv,rCheekCrv, self.cheekCrvGrp)
            cmds.xform(lCheekCrv,rCheekCrv, centerPivots = 1)   

            lHappyCheekCrv = cmds.duplicate(lCheekCrv, n= self.prefix[0] + 'happyCheek' + self.crvSuffix)
            rHappyCheekCrv = cmds.instance(lHappyCheekCrv, n= self.prefix[1] + 'happyCheek' + self.crvSuffix)
            lWideCheekCrv = cmds.duplicate(lCheekCrv, n= self.prefix[0] + 'wideCheek' + self.crvSuffix)
            rWideCheekCrv = cmds.instance(lWideCheekCrv, n= self.prefix[1] + 'wideCheek' + self.crvSuffix)
            lECheekCrv = cmds.duplicate(lCheekCrv, n= self.prefix[0] + 'eCheek' + self.crvSuffix)
            rECheekCrv = cmds.instance(lECheekCrv, n= self.prefix[1] + 'eCheek' + self.crvSuffix)

            lSadCheekCrv = cmds.duplicate(lCheekCrv, n= self.prefix[0] + 'sadCheek' + self.crvSuffix)
            rSadCheekCrv = cmds.instance(lSadCheekCrv, n= self.prefix[1] + 'sadCheek' + self.crvSuffix)
            lUCheekCrv = cmds.duplicate(lCheekCrv, n= self.prefix[0] + 'uCheek' + self.crvSuffix)
            rUCheekCrv = cmds.instance(lUCheekCrv, n= self.prefix[1] + 'uCheek' + self.crvSuffix)
            lOCheekCrv = cmds.duplicate(lCheekCrv, n= self.prefix[0] + 'oCheek' + self.crvSuffix)
            rOCheekCrv = cmds.instance(lOCheekCrv, n= self.prefix[1] + 'oCheek' + self.crvSuffix)

            lCheekBS = cmds.blendShape(lHappyCheekCrv[0],lWideCheekCrv[0],
                                       lECheekCrv[0],lSadCheekCrv[0],
                                       lUCheekCrv[0],lOCheekCrv[0],
                                       lCheekCrv, n ='lCheekBS')
            cmds.blendShape(lCheekBS[0], edit=True, w=[(0, 1),(1, 1),(2, 1),(3,1),(4,1),(5,1)])  
            rCheekBS = cmds.blendShape(rHappyCheekCrv[0],rWideCheekCrv[0],rECheekCrv[0],rSadCheekCrv[0],rUCheekCrv[0],rOCheekCrv[0], rCheekCrv, n ='rCheekBS')
            cmds.blendShape(rCheekBS[0], edit=True, w=[(0, 1),(1, 1),(2, 1),(3,1),(4,1),(5,1)])   
            cmds.move(2,0,0, lHappyCheekCrv, lWideCheekCrv, lSadCheekCrv, lECheekCrv, lUCheekCrv[0], lOCheekCrv, rotatePivotRelative = 1)
            cmds.move(-2,0,0, rHappyCheekCrv, rWideCheekCrv, rSadCheekCrv, rECheekCrv, rUCheekCrv[0], rOCheekCrv, rotatePivotRelative = 1)

            #attach ctrls to main cheek curves
            for lr in self.prefix:
               cvLs = cmds.ls(lr + '_cheek%s.cv[*]' %self.crvSuffix, fl = 1)
               cvLen = len(cvLs)
               lipCorner = cmds.group(em =1, n= lr +'_lipCorner', p ='supportRig')
               cheekList = [lr + '_lowCheek' + self.grpSuffix, lipCorner, lr + '_cheek' + self.grpSuffix, lr + '_squintPuff' + self.grpSuffix]
            
               for v in range(0, cvLen):
                   cheekPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = 'cheek' + str(v) + '_poc')
                   cmds.connectAttr(lr+'_cheek%sShape.worldSpace' %self.crvSuffix, cheekPoc + '.inputCurve')  
                   cmds.setAttr(cheekPoc + '.parameter', v)           
                   cmds.connectAttr(cheekPoc + '.positionX', cheekList[v] + '.tx')
                   cmds.connectAttr(cheekPoc + '.positionY', cheekList[v] + '.ty')
                   cmds.connectAttr(cheekPoc + '.positionZ', cheekList[v] + '.tz')  

        #- create lip joints parent group
        lipJotGrp = cmds.group(n = upLow + 'Lip' + self.grpSuffix, em =True) 
        cmds.parent(lipJotGrp, 'lipJotP')
        cmds.xform(lipJotGrp, ws = 1, t = self.jawRigPos) 
        
        #- delete detail lip ctrls 
        lipDetailP = upLow + 'LipDetailGrp' 
        kids = cmds.listRelatives(lipDetailP, ad=True, type ='transform')   
        if kids: cmds.delete(kids)

        vPos = []
        for vert in verts:
            voc = cmds.xform(vert, t =1, q=1, ws = 1)
            vPos.append(voc)
        vrtsDist = []
        for p in range(0, vNum-1):
            vDist = self.distance(vPos[p], vPos[p+1])
            vrtsDist.append(vDist)
        vrtsDist.insert(0,0)
        vLength = sum(vrtsDist)

        linearDist = 1.0/(vNum-1)
        increment = 0
        distSum = 0.0
        for i in range(vMin, vMax):
            distSum += vrtsDist[i]
            #increment = distSum / vLength
            poc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = upLow + 'Lip' + str(i) + '_poc')
            cmds.connectAttr(guideCrvShape[0]+'.worldSpace',  poc + '.inputCurve')   
            cmds.setAttr(poc + '.turnOnPercentage', 1)    
            cmds.setAttr(poc + '.parameter', increment)        
            
            #- create detail lip ctrl        
            if i==0 or i== vNum-1:
                if upLow == self.uploPrefix[0]:
                    corners = self.createLipJoint(upLow, self.lipYPos, poc, lipJotGrp, i)
                    print corners
                    self.createDetailCtl(upLow, i)
                    cmds.parent(upLow +'LipDetailP'+ str(i), lipDetailP)
                    cmds.setAttr(upLow +'LipDetailP'+ str(i)+'.tx', linearDist*i)
                    cmds.setAttr(upLow +'LipDetailP'+ str(i)+'.ty', -1.5)
                    cmds.setAttr(upLow +'LipDetailP'+ str(i)+'.tz', 0)
                    cmds.setAttr(upLow +'LipDetailP'+ str(i)+'.sx', 0.25)
            else:
                self.createLipJoint(upLow, self.lipYPos, poc, lipJotGrp, i) 
                self.createDetailCtl(upLow, i)           
                cmds.parent(upLow +'LipDetailP'+ str(i), lipDetailP)
                cmds.setAttr(upLow +'LipDetailP'+ str(i) + '.tx', linearDist*i) 
                cmds.setAttr(upLow +'LipDetailP'+ str(i) + '.ty', 0)
                cmds.setAttr(upLow +'LipDetailP'+ str(i) + '.tz', 0)

            #- create lipCtrl curve POC
            lipCrvPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = upLow +'LipCrv' + str(i) + '_poc')
            cmds.connectAttr(lipCrvShape[0] + ".worldSpace",  lipCrvPoc + '.inputCurve')   
            cmds.setAttr(lipCrvPoc  + '.turnOnPercentage', 1)    
            cmds.setAttr(lipCrvPoc  + '.parameter', increment)
            
            lipTYPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = upLow +'LipTy' + str(i) + '_poc')
            cmds.connectAttr(tylipCrvShape[0] + ".worldSpace",  lipTYPoc + '.inputCurve')
            cmds.setAttr(lipTYPoc  + '.turnOnPercentage', 1)    
            cmds.setAttr(lipTYPoc  + '.parameter', increment) 
                    
            #- create lipCtrl curve POC
            ctlPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = upLow +'LipCtl' + str(i) + '_poc')
            cmds.connectAttr(lipCtlCrvShape[0] + ".worldSpace",  ctlPoc + '.inputCurve')   
            cmds.setAttr(ctlPoc  + '.turnOnPercentage', 1)    
            cmds.setAttr(ctlPoc  + '.parameter', increment) 
            
            #- create lipRoll curve POC  lipRollCrv, lipRollYZCrv
            lipRollPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = upLow +'LipRoll' + str(i) + '_poc')
            cmds.connectAttr(lipRollCrvShape[0] + ".worldSpace",  lipRollPoc + '.inputCurve')  
            cmds.setAttr(lipRollPoc + '.turnOnPercentage', 1)   
            cmds.setAttr(lipRollPoc + '.parameter', increment) 
            
            lipRollYZPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = upLow +'LipRollYZ' + str(i) + '_poc')
            cmds.connectAttr(lipRollYZCrvShape[0] + ".worldSpace",  lipRollYZPoc + '.inputCurve')  
            cmds.setAttr(lipRollYZPoc  + '.turnOnPercentage', 1)   
            cmds.setAttr(lipRollYZPoc  + '.parameter', increment)
            
            increment = increment + linearDist
        
        if upLow == self.uploPrefix[1]:
            self.__bridgeJoints()
            #self.indiCrvSetup('lip')
            
    def createLipJoint(self, upLow, lipYPos, poc, lipJotGrp, i):   
        """
        draw joints
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
        
        cmds.xform(lipRollJotP, ws = True, t = [pocPosX, pocPosY, pocPosZ])
        lipRollJot = cmds.joint(n = upLow + 'LipRollJot' + str(i) + self.jntSuffix, relative = True, p = [ 0, 0, 0])
        
        return lipRollJot
    
    def createDetailCtl(self, updn, i):
        """
        draw detail control
        """
        detailCtlP = cmds.group(em =True, n = updn  + 'LipDetailP'+ str(i))
        detailCtl = cmds.circle(n = updn  + 'LipDetail' + str(i), ch=False, o =True, nr =(0, 0, 1), r = 0.05 )
        cmds.parent(detailCtl[0], detailCtlP)
        cmds.setAttr(detailCtl[0]+"Shape.overrideEnabled", 1)
        cmds.setAttr(detailCtl[0]+"Shape.overrideColor", 20)
        cmds.setAttr(detailCtl[0]+'.translate', 0,0,0)
        cmds.transformLimits(detailCtl[0], tx =(-.5, .5), etx=(True, True))
        cmds.transformLimits(detailCtl[0], ty =(-.5, .5), ety=(True, True))
        attTemp = ['scaleX','scaleY','scaleZ', 'rotateX','rotateY','rotateZ', 'tz', 'visibility' ]  
        for y in attTemp:
            cmds.setAttr(detailCtl[0] +"."+ y, lock = True, keyable = False, channelBox =False) 

    def __bridgeJoints(self):    
        """
        bridge joints
        """
        noseP = cmds.group(n = 'noseP', em =True, p = "noseRig")
        cmds.xform(noseP, relative = True, t = [ 0, 0, 0])
        noseJnt = cmds.joint(n = 'nose' + self.jntSuffix, relative = True, p = [ 0, 0, 0])
        
        for prefix in self.prefix:
            # ear / nose joint
            lEarP = cmds.group(n = prefix + 'earP', em =True, p = prefix + "ear" + self.grpSuffix)
            cmds.xform(lEarP, relative = True, t = [ 0, 0, 0])
            lEarJnt = cmds.joint(n = prefix + 'ear' + self.jntSuffix, relative = True, p = [ 0, 0, 0]) 
            
            # cheek joint - check the cheek/squintPush group and angle
            cheekP = cmds.group(n = prefix + 'cheekP', em =True, p = prefix + "cheek" + self.grpSuffix)
            cmds.xform(cheekP, relative = True, t = [ 0, 0, 0])
            upCheekP = cmds.duplicate(cheekP, n = prefix + 'upCheekP')
            cmds.parent(upCheekP[0], cheekP)
            upCheekJnt = cmds.joint(n = prefix + 'upCheek' + self.jntSuffix, relative = True, p = [ 0, 0, 0])
            
            midCheekP = cmds.duplicate(upCheekP, po =1, n = prefix + 'midCheekP')
            midCheekRotY = cmds.group(midCheekP, n= prefix + 'midCheekRotY', p = cheekP)
            cmds.xform(midCheekRotY, piv = self.lipYPos, ws =1)
            midCheekRotX = cmds.group(midCheekRotY, n= prefix + 'midCheekRotX', p = cheekP)
            cmds.xform(midCheekRotX, piv = self.jawRigPos, ws =1)
            cmds.select(midCheekP[0])
            midCheekJnt = cmds.joint(n = prefix + 'midCheek' + self.jntSuffix, relative = True, p = [ 0, 0, 0]) 
               
            #- squintPuff joint
            sqiuntPuff = cmds.group(n = prefix + 'squintPuffP', em =True, p = prefix + "squintPuff" + self.grpSuffix)
            cmds.xform(sqiuntPuff, relative = True, t = [ 0, 0, 0])
            sqiuntPuffJnt = cmds.joint(n = prefix + 'squintPuff' + self.jntSuffix, relative = True, p = [ 0, 0, 0]) 

            #- lowCheek joint
            lowCheek = cmds.group(n = prefix + 'lowCheekP', em =True, p = prefix + "lowCheek" + self.grpSuffix)
            cmds.xform(lowCheek, relative = True, t = [ 0, 0, 0])
            loCheekRotY = cmds.group(lowCheek, n= prefix + 'loCheekRotY', p = prefix + "lowCheek" + self.grpSuffix)
            cmds.xform(loCheekRotY, piv = self.lipYPos, ws =1)
            loCheekRotX = cmds.group(loCheekRotY, n= prefix + 'loCheekRotX', p = prefix + "lowCheek" + self.grpSuffix)
            cmds.xform(loCheekRotX, piv = self.jawRigPos, ws =1)
            cmds.select(lowCheek)    
            lowCheekJnt = cmds.joint(n = prefix + 'lowCheek' + self.jntSuffix, relative = True, p = [ 0, 0, 0]) 
        
        return True

        #return {'lipJntGrp' : lipJotGrp , 'lipCrvGrp' : lipCrvGrp}
