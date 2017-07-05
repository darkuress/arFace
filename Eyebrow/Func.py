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
import re

class Func(Base.Base):
    def __init__(self, rotateScale, **kw):
        """
        initializing variables
        """
        #local variables
        Base.Base.__init__(self, **kw)
    
    def orderJnts(self, browJnts):
        """
        search for sorted ojnt
        """
        jntNum = len(browJnts)
        browJnts.sort()
        z = [ browJnts[0] ]
        y = browJnts[1:jntNum/2+1]
        browJnts.reverse()
        x = browJnts[:jntNum/2]
        orderJnts = x + z + y
        
        return x, y, z, orderJnts

    def crvCtrlToJnt(self, browCtrl, browDetail, jnt, rotYJnt, ctlBase, rotYCtl, shapePOC, POC, initialX, index):
        """
        lots of utility nodes
        """
        #connect browCtrlCurve and controller to the brow joints
        ctrlMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = jnt.split('Base', 1)[0] +'CtrlMult'+ str(index) )
        jntMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = jnt.split('Base', 1)[0] +'JntMult'+ str(index) )
        browXYZSum = cmds.shadingNode('plusMinusAverage', asUtility=True, n = jnt.split('Base', 1)[0] +'BrowXYZSum'+ str(index))
        browCtlRotSum = cmds.shadingNode('plusMinusAverage', asUtility=True, n = jnt.split('Base', 1)[0] +'CtlRotSum'+ str(index))
        addBrowCtl = cmds.shadingNode('plusMinusAverage', asUtility=True, n = jnt.split('Base', 1)[0] +'AddBrowCtl'+ str(index))
         
        #brow TX sum      
        cmds.connectAttr(browDetail + '.tx', browXYZSum + '.input3D[0].input3Dx')
        #POC TX zero out 
        cmds.connectAttr(POC + '.positionX', browXYZSum + '.input3D[1].input3Dx')
        cmds.setAttr(browXYZSum + '.input3D[2].input3Dx', -initialX )
        cmds.connectAttr(shapePOC + '.positionX', browXYZSum + '.input3D[3].input3Dx')
        cmds.setAttr(browXYZSum + '.input3D[4].input3Dx', -initialX )
        #browXYZSum.tx --> ctrlMult.ry 
        cmds.connectAttr(browXYZSum + '.output3Dx', ctrlMult+'.input1X')
        cmds.connectAttr(self.faceFactors['eyebrow'] + '.browRotateY_scale', ctrlMult +'.input2X')
        cmds.connectAttr(ctrlMult+'.outputX', rotYCtl + '.ry' )    
        
        #add browCtl.tx 
        cmds.connectAttr(browXYZSum + '.output3Dx', addBrowCtl + '.input3D[0].input3Dx')
        cmds.connectAttr(browCtrl + '.tx', addBrowCtl + '.input3D[1].input3Dx')    
        #addBrowCtl.tx --> jntMult.ry 
        cmds.connectAttr(addBrowCtl + '.output3Dx', jntMult+'.input1X')
        cmds.connectAttr(self.faceFactors['eyebrow'] + '.browRotateY_scale', jntMult+'.input2X')
        cmds.connectAttr(jntMult+'.outputX', rotYJnt + '.ry' )    
                
        #brow TY sum    
        #1. POC.ty sum
        cmds.connectAttr(POC + '.positionY', browXYZSum +'.input3D[0].input3Dy')
        cmds.connectAttr(shapePOC + '.positionY', browXYZSum + '.input3D[1].input3Dy')
        #2. detail ctl.ty sum
        cmds.connectAttr(browDetail + '.ty', browXYZSum + '.input3D[2].input3Dy')
        #browXYZSum.ty --> ctrlMult.rx 
        cmds.connectAttr(browXYZSum + '.output3Dy', ctrlMult+'.input1Y')
        cmds.connectAttr('browReverse_mult.outputX', ctrlMult +'.input2Y')
        cmds.connectAttr(ctrlMult+'.outputY', ctlBase + '.rx' )
        
        #new
        browCond = cmds.shadingNode("condition", asUtility=1, n = "browScale_Cond") 
        cmds.connectAttr(browXYZSum + '.output3Dy', addBrowCtl + '.input3D[0].input3Dy')
        cmds.connectAttr(browCtrl + '.ty', addBrowCtl + '.input3D[1].input3Dy')        
        
        #add BrowCtl.ty --> jntMult.rx      
        cmds.connectAttr(addBrowCtl + ".output3Dy", browCond + ".firstTerm" )
        cmds.setAttr(browCond + ".secondTerm", 0 )
        cmds.setAttr(browCond + ".operation", 2 )  #greater than 

        if jnt.startswith(self.prefix[1]):
            cmds.connectAttr("browFactor.browUp_scale"  , browCond+".colorIfTrueR")
            cmds.connectAttr("browFactor.browDown_scale", browCond+ ".colorIfFalseR")
 
        else:    
            cmds.connectAttr('browReverse_mult.outputX', browCond+".colorIfTrueR")
            cmds.connectAttr('browReverse_mult.outputZ', browCond+".colorIfFalseR")
         
        cmds.connectAttr(addBrowCtl + ".output3Dy", jntMult + ".input1Y")
        cmds.connectAttr(browCond+".outColorR", jntMult + ".input2Y")
        cmds.connectAttr(jntMult+'.outputY',  jnt + '.rx')
        
        #brow TZ sum
        browPCtl =cmds.listRelatives( cmds.listRelatives (rotYCtl, c =1, type = 'transform')[0], c =1, type = 'transform')
        browPJnt = cmds.listRelatives(rotYJnt, c =1, type = 'joint')
        browJnt = cmds.listRelatives(browPJnt[0], c =1, type = 'joint')
        cmds.connectAttr(shapePOC + '.positionZ', browXYZSum + '.input3D[0].input3Dz')
        cmds.connectAttr(browXYZSum + '.output3Dz', browPCtl[0]+'.tz' )
         
        #addBrowCtl.tz --> browJnt[0] + ".tz"   
        cmds.connectAttr(browXYZSum + '.output3Dz', addBrowCtl + '.input3D[0].input3Dz')
        cmds.connectAttr(browCtrl + '.tz', addBrowCtl + '.input3D[1].input3Dz')  
        cmds.connectAttr(addBrowCtl + '.output3Dz', browJnt[0] + '.tz' ) 
        
        #extra rotate ctrl for browJnt[0]   
        cmds.connectAttr(browCtrl + '.rx', browCtlRotSum + '.input3D[0].input3Dx') 
        cmds.connectAttr(browDetail + '.rx', browCtlRotSum + '.input3D[1].input3Dx') 
        cmds.connectAttr(browCtrl + '.ry', browCtlRotSum + '.input3D[0].input3Dy') 
        cmds.connectAttr(browDetail + '.ry', browCtlRotSum + '.input3D[1].input3Dy')  
        cmds.connectAttr(browCtrl + '.rz', browCtlRotSum + '.input3D[0].input3Dz') 
        cmds.connectAttr(browDetail + '.rz', browCtlRotSum + '.input3D[1].input3Dz') 
    
        cmds.connectAttr(browCtlRotSum + '.output3Dx', browPJnt[0] + '.rx')
        cmds.connectAttr(browCtlRotSum + '.output3Dy', browPJnt[0] + '.ry')
        cmds.connectAttr(browCtlRotSum + '.output3Dz', browPJnt[0] + '.rz')    

    def createBrowCtl(self, jntNum, orderJnts):
        """
        create extra controllor for the panel
        """
        ctlP = "browDetailCtrl0"
        kids = cmds.listRelatives (ctlP, ad=True, type ='transform')   
        if kids:
            cmds.delete (kids)
            
        attTemp = ['scaleX','scaleY','scaleZ', 'rotateX','rotateY', 'tz', 'visibility' ]  
        index = 0

        for jnt in orderJnts:                            
            detailCtl = cmds.circle ( n = 'browDetail' + str(index+1).zfill(2), ch=False, o =True, nr = ( 0, 0, 1), r = 0.2 )
            detailPlane = cmds.nurbsPlane ( ax = ( 0, 0, 1 ), w = 0.1,  lengthRatio = 10, degree = 3, ch=False, n = 'browDetail'+ str(index+1).zfill(2) + 'P' )
            increment = 2.0/(jntNum-1)
            cmds.parent (detailCtl[0], detailPlane[0], relative=True )
            cmds.parent (detailPlane[0], ctlP, relative=True )
            cmds.setAttr (detailPlane[0] + '.tx', -2 + increment*index*2 )
            cmds.xform ( detailCtl[0], r =True, s = (0.2, 0.2, 0.2))  
            cmds.setAttr (detailCtl[0] +".overrideEnabled", 1)
            cmds.setAttr (detailCtl[0] +"Shape.overrideEnabled", 1)
            cmds.setAttr( detailCtl[0]+"Shape.overrideColor", 20)        
            
            cmds.transformLimits ( detailCtl[0] , tx = ( -.4, .4), etx=( True, True) )
            cmds.transformLimits ( detailCtl[0], ty = ( -.8, .8), ety=( True, True) )
            
            for att in attTemp:
                cmds.setAttr (detailCtl[0] +"."+ att, lock = True, keyable = False, channelBox =False)
                    
            index = index + 1

    def LRBlendShapeWeight(self, lipCrv, lipCrvBS):
        cvs = cmds.ls(lipCrv+'.cv[*]', fl =1)
        length = len (cvs)
        
        increment = 1.0/(length-1)
        targets = cmds.aliasAttr( lipCrvBS, q=1)
        tNum = len(targets)   
        
        for t in range(0, tNum, 2):
            if targets[t][0] == 'l' :
                indexL=re.findall('\d+', targets[t+1])
                cmds.setAttr(lipCrvBS + '.inputTarget[0].inputTargetGroup[%s].targetWeights[%s]'%(str(indexL[0]), str(length/2)), .5 ) 
                for i in range(0, length/2):                
                    cmds.setAttr(lipCrvBS + '.inputTarget[0].inputTargetGroup[%s].targetWeights[%s]'%(str(indexL[0]), str(i)), 0 ) 
                    cmds.setAttr(lipCrvBS + '.inputTarget[0].inputTargetGroup[%s].targetWeights[%s]'%(str(indexL[0]), str(length-i-1)), 1 )   
                    
            if targets[t][0] == 'r' :
                indexR=re.findall('\d+', targets[t+1])
                cmds.setAttr(lipCrvBS + '.inputTarget[0].inputTargetGroup[%s].targetWeights[%s]'%(str(indexR[0]), str(length/2)), .5 ) 
                for i in range(0, length/2):                
                    cmds.setAttr(lipCrvBS + '.inputTarget[0].inputTargetGroup[%s].targetWeights[%s]'%(str(indexR[0]), str(i)), 1 ) 
                    cmds.setAttr(lipCrvBS + '.inputTarget[0].inputTargetGroup[%s].targetWeights[%s]'%(str(indexR[0]), str(length-i-1)), 0 )     

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

    def createMapSurf(self, faceGeo):
        """
        create browMapMesh
        """
        #xmin ymin zmin xmax ymax zmax (face bounding box)
        facebbox    = cmds.xform (faceGeo, q =1, boundingBox =1 )
        sizeX       = facebbox[3]*2
        bboxSizeY   = facebbox[4] - facebbox[1]
        browJntLen  = len(cmds.ls("*" + self.browBase + "*", type = "joint"))
        browMapSurf = cmds.polyPlane(n = self.browMapGeo, w = sizeX, h =bboxSizeY/2, subdivisionsX = browJntLen, subdivisionsY = 1 )
        cmds.xform(browMapSurf, p = 1, rp =(0, 0, bboxSizeY/4))
        
        #place the mapSurf at the upper part of the face
        cmds.setAttr(browMapSurf[0] + ".rotateX", 90 )
        cmds.xform(browMapSurf[0], ws =1, t = (0, facebbox[1] + bboxSizeY/2, 0))
        
        return browMapSurf

    def skinBrowSurfaceMap(self):
        """
        skin joints to surface map 
        """
        if not cmds.objExists(self.browMapGeo):
            print "create browMapSurf first!!"
        else :
            browMapSurf = self.browMapGeo
        browJnts = cmds.ls ("*" + self.browP + "*", type ="joint")
        x, y, z, orderJnts = self.orderJnts(browJnts)
        jntNum = len(orderJnts)
        orderChildren = cmds.listRelatives(orderJnts, c =1, type = "joint")

        edges= cmds.polyEvaluate(browMapSurf, e =1 )
        cmds.polyBevel(browMapSurf +'.e[0:%s]'%(edges-1), offset=0.01)
        cmds.delete(browMapSurf, constructionHistory =1)

        faces = []
        for i in range(0, jntNum):
            face = browMapSurf+ ".f[%s]"% str(i)
            faces.append(face)
        faces.sort()    
        faceLen = len(faces)
        cmds.select(cl=1)
        
        #get the joints to be bound, check if "headSkel_jnt" exists
        if not cmds.objExists(self.headSkelJnt):
            headSkelPos = cmds.xform('headSkelPos', q =1, ws =1, t =1 )
            cmds.joint(n = self.headSkelJnt , p = headSkelPos )
        orderChildren.append(self.headSkelJnt )
        
        skinCls = cmds.skinCluster(orderChildren , browMapSurf, toSelectedBones=1 )
        
        # 100% skinWeight to headSkel_jnt
        cmds.skinPercent(skinCls[0], browMapSurf, transformValue = [self.headSkelJnt , 1])
                
        # skinWeight
        for i in range (0, jntNum):
            vtxs = cmds.polyListComponentConversion(faces[i], ff=True, tv=True )
            #cmds.select(vtxs, r=1)
            print faces[i], orderChildren[i]
            cmds.skinPercent( skinCls[0], vtxs, transformValue = [ orderChildren[i], 1])        
        