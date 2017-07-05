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

    def setLipJntLabel(self):
        """
        labeling for liyY_jnt mirror weight
        """
        upJntY = cmds.ls('upLipY*' + self.jntSuffix, fl=1, type = 'joint')
        loJntY = cmds.ls('loLipY*' + self.jntSuffix, fl=1, type = 'joint')
        upJntNum = len(upJntY)
        loJntNum = len(loJntY)
        rightUp = upJntY[0:upJntNum/2]
        leftUp = upJntY[upJntNum/2+1: ]
        rightLo =loJntY[0: loJntNum/2] 
        leftLo = loJntY[loJntNum/2+1: ]
        leftLo.reverse()
        rightUp.reverse()
        leftJnt = leftUp + leftLo
        rightJnt = rightUp + rightLo
        for i, j in enumerate(leftJnt):
            cmds.setAttr(j + '.side', 1)
            cmds.setAttr(j + '.type', 18)
            cmds.setAttr(j + '.otherType', str(i).zfill(2), type = "string")
        for id, k in enumerate(rightJnt):
            cmds.setAttr(k + '.side', 2)
            cmds.setAttr(k + '.type', 18)
            cmds.setAttr(k + '.otherType', str(id).zfill(2), type = "string")    
        
        return True
        
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

    def indiCrvSetup(self, name):
        """
        indivisual curve setup
        """
        upCrv = 'up'+ name + self.crvSuffix
        loCrv = 'lo'+ name + self.crvSuffix
        crvShape = cmds.listRelatives(upCrv, c=1, type = 'nurbsCurve')
        upCVs = cmds.ls(upCrv + '.cv[*]', fl = 1)
        loCVs = cmds.ls(loCrv + '.cv[*]', fl = 1)
        cvNum = len(upCVs) 
        
        lipCrvStartPos = cmds.xform (upCVs[0], q=1, ws =1, t = 1)
        lipCrvEndPos = cmds.xform (upCVs[cvNum-1], q=1, ws =1, t = 1)
        nCrvPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = 'cnt' + name + '_poc')
        cmds.connectAttr(crvShape[0]+'.worldSpace',  nCrvPoc + '.inputCurve')   
        cmds.setAttr(nCrvPoc + '.turnOnPercentage', 1)    
        cmds.setAttr(nCrvPoc + '.parameter', .5)
        lipCrvMidPos = cmds.getAttr(nCrvPoc + '.position')
        
        lipCrvStart = cmds.group (em = 1, n = name + 'Start' + self.grpSuffix)
        cmds.xform(lipCrvStart, ws = 1, t = lipCrvStartPos)
        rCorner = cmds.joint(n= self.prefix[1] + 'Corner'+ name + self.jntSuffix, p= lipCrvStartPos)
        
        uplipCrvMid = cmds.group (em = 1, n = 'up' + name + 'Mid' + self.grpSuffix) 
        cmds.xform(uplipCrvMid, ws = 1, t = list(lipCrvMidPos[0])) 
        midUpJnt = cmds.joint(n = 'cntUp' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0])  
      
        lolipCrvMid = cmds.group (em = 1, n = 'lo' + name + 'Mid' + self.grpSuffix) 
        cmds.xform(lolipCrvMid, ws = 1, t = list(lipCrvMidPos[0])) 
        midLoJnt = cmds.joint(n = 'cntLo' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0])
        
        lipCrvEnd = cmds.group (em = 1, n = name + 'End' + self.grpSuffix) 
        cmds.xform(lipCrvEnd, ws = 1, t = lipCrvEndPos) 
        lCorner = cmds.joint(n= self.prefix[0] + 'Corner' + name + self.jntSuffix, relative = True, p = [ 0, 0, 0])  
              
        indiGrp = cmds.group(lipCrvStart, uplipCrvMid, lolipCrvMid, lipCrvEnd, upCrv, loCrv, n = name + '_indiGrp') 
        cmds.parent(indiGrp, 'upLipCrv' + self.grpSuffix)
       
        #skinning
        upSkin = cmds.skinCluster(rCorner, midUpJnt, lCorner, upCrv, toSelectedBones = 1)    
        loSkin = cmds.skinCluster(rCorner, midLoJnt, lCorner, loCrv, toSelectedBones = 1)

        numVal = { 0: 0.15, 1:0.85, 2:0.98, 4: 0.98, 5:0.85, 6:0.15 }
        for key, val in numVal.items():
            cmds.skinPercent(upSkin[0], upCVs[key], tv =(midUpJnt, val))
            cmds.skinPercent(loSkin[0], loCVs[key], tv =(midLoJnt, val))    

        ctlCrvs = { 'JawOpen':'lowJaw_dir', 'TyLip':'jaw_UDLR' }
        
        if name in ctlCrvs.keys():
            cornerMult = cmds.shadingNode ('multiplyDivide', asUtility = True, n = name + 'Corner_mult' )
            dampMult = cmds.shadingNode('multiplyDivide', asUtility = True, n = name + 'damp_mult' )
            #endAvg = cmds.shadingNode('plusMinusAverage', asUtility = True, n = name + 'TY' + str(i) +'_plus')  
            
            #- corner tx value
            cmds.connectAttr(midLoJnt+ '.tx', cornerMult + '.input1X' )  
            cmds.connectAttr(midLoJnt+ '.ty', cornerMult + '.input1Y' )  
            cmds.connectAttr(midLoJnt+ '.ty', cornerMult + '.input1Z' )  
            
            cmds.setAttr(cornerMult + '.input2X',  .5)   #lipCorners.tx follow midLoJnt.tx
            cmds.setAttr(cornerMult + '.input2Y',  .06)  #lipLCorner.tx inner when jaw open 
            cmds.setAttr(cornerMult + '.input2Z', -.06)  #lipRCorner.tx inner when jaw open
            
            if name == "JawOpen":
                txAvg = cmds.shadingNode('plusMinusAverage', asUtility = True, n = name + 'TX_plus')
                cmds.connectAttr(cornerMult + '.outputY', txAvg + '.input3D[0].input3Dy' )
                cmds.connectAttr(cornerMult + '.outputZ', txAvg + '.input3D[0].input3Dz' )
                cmds.connectAttr(cornerMult + '.outputX', txAvg + '.input3D[1].input3Dy' )
                cmds.connectAttr(cornerMult + '.outputX', txAvg + '.input3D[1].input3Dz' )
                cmds.connectAttr(txAvg + '.output3Dy', lCorner + '.tx' )
                cmds.connectAttr(txAvg + '.output3Dz', rCorner + '.tx' )
            
            else:
                cmds.connectAttr(cornerMult + '.outputY', lCorner + '.tx', f=1  )
                cmds.connectAttr(cornerMult + '.outputZ', rCorner + '.tx', f=1  )
                cmds.connectAttr(cornerMult + '.outputX', lCorner + '.tz', f=1  )  
                cmds.connectAttr(cornerMult + '.outputX', rCorner + '.tz', f=1  )            
            
            #- corner ty value
            cmds.connectAttr(midLoJnt+ '.tx', dampMult + '.input1X' )  
            cmds.connectAttr(midLoJnt+ '.ty', dampMult + '.input1Y' )  
            cmds.connectAttr(midLoJnt+ '.ty', dampMult + '.input1Z' ) 
            
            cmds.setAttr(dampMult+ '.input2X', .1)  # lipCenter.tx follow jaw
            cmds.setAttr(dampMult+ '.input2Y', .5)  # lipCorners.ty follow jaw
            cmds.setAttr(dampMult+ '.input2Z', .01) # lipCenter.ty follow jaw
            if name == "JawOpen":        
                cmds.connectAttr(dampMult + '.outputX',  midUpJnt+'.tx')
            else:
                cmds.connectAttr(dampMult + '.outputX',  midUpJnt+'.tz')
                
            cmds.connectAttr(dampMult + '.outputZ',  midUpJnt+'.ty')
            cmds.connectAttr(dampMult + '.outputY',  lCorner+'.ty')
            cmds.connectAttr(dampMult + '.outputY',  rCorner+'.ty')        
            
            #- connect curve joint with controller 
            '''
            cmds.connectAttr ( ctlCrvs[name] + '.tx', midLoJnt + '.tx')
            cmds.connectAttr ( ctlCrvs[name] + '.ty', midLoJnt + '.ty')
            cmds.connectAttr ( ctlCrvs[name] + '.tz', midLoJnt + '.tz')
            '''
        
        return midLoJnt

    def curveOnEdgeLoop(self):
        """
        first two edge selection are important( it determines the first vertex)
        create curve based on the ordered vertices list
        """
        myList = cmds.ls(os=1, fl=1)
        allVerts = self.orderedVertsEdgeLoop(myList)
        vertsPos = []
        for v in allVerts:
            pos = cmds.xform(v, q =1, ws =1, t =1)
            vertsPos.append(pos)
        cmds.curve(n= 'loftCurve01', d =1, per =1, p = vertsPos)
    
    def orderedVertsEdgeLoop(self, myList):
        """
        select two adjasent edges( second edge is the curve direction)
        return list of verts on edgeLoop
        """        
        cmds.select(myList[0], r =1)
        cmds.ConvertSelectionToVertices()
        firstVert = cmds.ls(sl=1, fl=1)
        cmds.select(myList[1], r =1)
        cmds.ConvertSelectionToVertices()
        secondVert = cmds.ls(sl=1, fl=1)
        repeatVert = [i for i in firstVert if i in secondVert]
        secondVert.remove(repeatVert[0])
        nextVert = secondVert[0] 
        firstVert.remove(repeatVert[0])
        
        cmds.polySelectSp(myList[1], loop =1)
        sel = cmds.ls( sl=1, fl=1 )
        edgeLen = len(sel)-2
        orderedVerts = []    
        for i in range(edgeLen):
            selEdges = [x for x in sel if x not in myList]        
            nextVert_edge = self.findConnectVert(selEdges, nextVert)
            
            orderedVerts.append(nextVert) 
            nextVert = nextVert_edge[0]               
            myList.append(nextVert_edge[1])
        
        orderedVerts.append(firstVert[0])
        orderedVerts.insert(0,repeatVert[0]) 
        orderedVerts.insert(0,firstVert[0])
        
        return orderedVerts        
            
    def findConnectVert(self, selEdges, nextVert):
        """
        """
        nextVertEdge =[]
        for edge in selEdges:
            cmds.select(edge, r =1)
            cmds.ConvertSelectionToVertices()
            tempVert = cmds.ls(sl=1, fl=1)        
            if nextVert in tempVert:
                tempVert.remove(nextVert)
                nextVertEdge =[tempVert[0], edge ]            
        return nextVertEdge


    def loftFacePart(self, facePart):
        """
        making poligon map
        """
        crvSel = cmds.ls(os=1, fl=1, type = 'transform')
        loft_suf = cmds.loft(crvSel, n = facePart + 'Tip_map', ch =1, u=1, c=0, ar= 1, d=1, ss= 1, rn= 0, po= 1, rsn = 1)
        suf_inputs = cmds.listHistory( loft_suf[0])
        tessel = [x for x in suf_inputs if cmds.nodeType(x) == 'nurbsTessellate']
        cmds.setAttr(tessel[0]+".format", 3)
        cmds.delete(loft_suf[0], ch =1)
        wide_suf = cmds.duplicate(loft_suf[0], n = facePart + 'Wide_map')

    def copyCvWeighs(self):
        """
        copy surface cv's weight to curve's cv
        """
        sel = cmds.ls(sl = True)
        Util.Util.copyCrvSkinWeight(sel[0], sel[1])
        
