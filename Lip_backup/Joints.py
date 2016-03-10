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

class Joints(Func.Func):
    def __init__(self, **kw):
        """
        initializing variables
        """
        #local variables
        Func.Func.__init__(self, **kw)
        
        self.allBaseJnts = list()

    def createJnts(self, upLow):
        """
        creating joints
        """
        if upLow == self.uplo[0]:
            verts = self.uplipVtxs
        elif upLow == self.uplo[1]:
            verts = self.lolipVtxs
        vNum = len (verts) + 2       
        
        if upLow == self.uplo[0]:
            lipCntPos = self.lipNPos 
                
        elif upLow == self.uplo[1]:
            lipCntPos = self.lipSPos
                
        increment = 1.0/(vNum-1)
        
        #- create lip joint guide curve
        tempCrv = cmds.curve(d= 3, ep= [(-self.lipEPos[0], self.lipEPos[1], self.lipEPos[2]),(lipCntPos), (self.lipEPos)]) 
        guideCrv = cmds.rename(tempCrv, upLow + "Guide" + self.crvSuffix)
        guideCrvShape = cmds.listRelatives(guideCrv, c = True) 
        cmds.rebuildCurve(guideCrv, d = 3, rebuildType = 0, keepRange = 0) 
        
        #- final lip shape ctrl curve
        templipCrv = cmds.curve(d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
        cmds.rebuildCurve(rt = 0, d = 3, kr = 0, s = 2)    
        lipCrv = cmds.rename (templipCrv, upLow +'Lip' + self.crvSuffix)
        lipCrvShape = cmds.listRelatives(lipCrv, c = True)
        lipCrvGrp = self.group([lipCrv, guideCrv], upLow +'LipCrv' + self.grpSuffix)
    
        #- lipTarget curve shape
        jawOpenCrv = cmds.duplicate(lipCrv, n= upLow +'jawOpen' + self.crvSuffix) 
        lipwideCrv = cmds.duplicate(lipCrv, n= upLow +'lipWide' + self.crvSuffix) 
        OCrv = cmds.duplicate(lipCrv, n= upLow +'U' + self.crvSuffix) 
        happyCrv = cmds.duplicate(lipCrv, n= upLow +'Happy' + self.crvSuffix) 
        lipCrvBS = cmds.blendShape(jawOpenCrv[0], lipwideCrv[0], OCrv[0], happyCrv[0], lipCrv, n =upLow + 'LipCrvBS')
        cmds.blendShape(lipCrvBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3, 1)])   
        
        #- lip controller curve shape(different number of points (4), so can not be target of the blendShape)      
        templipCtlCrv = cmds.curve(d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
        cmds.rebuildCurve(rt = 0, d = 3, kr = 0, s = 2)   
        lipCtlCrv = cmds.rename(templipCtlCrv, upLow +'LipCtl' + self.crvSuffix)
        lipCtlCrvShape = cmds.listRelatives(lipCtlCrv, c = True) 
        cmds.parent (lipCtlCrv, lipCrvGrp) 
        #- create lip joints parent group
        lipJotGrp = cmds.group(n = upLow + 'LipJnt' + self.grpSuffix, em =True)
        #cmds.parent(lipJotGrp, 'lipJotP')
        cmds.xform (lipJotGrp, ws = 1, t = self.jawRigPos) 
        #- delete detail lip ctrls 
        lipDetailP = upLow + 'LipDetailP'
        #if not cmds.objExists(lipDetailP):
        #    cmds.createNode('transform', n = lipDetailP)
        kids = cmds.listRelatives (lipDetailP, ad=True, type ='transform')   
        if kids:
            cmds.delete (kids)     
            
        if upLow == self.uplo[0]:
            min = 0
            max = vNum
        elif upLow == self.uplo[1]:    
            min = 1
            max = vNum-1           
              
        for i in range (min, max):
            poc = self.createPocNode(upLow + 'Lip' + str(i) + '_poc', guideCrvShape[0], increment*i)
            
            self.createLipJoint(upLow, self.jawRigPos, self.lipYPos, poc, lipJotGrp, i)
            
            #- create detail lip ctrl        
            if i==0 or i== vNum-1:
                self.createDetailCtl(upLow, i)
                cmds.parent(upLow +'LipDetailP'+ str(i), lipDetailP)
                cmds.setAttr (upLow +'LipDetailP'+ str(i)+'.tx', increment*i)
                cmds.setAttr (upLow +'LipDetailP'+ str(i)+'.ty', -1.5)
                cmds.setAttr (upLow +'LipDetailP'+ str(i)+'.tz', 0)
                cmds.setAttr (upLow +'LipDetailP'+ str(i)+'.sx', 0.25)
            else: 
                self.createDetailCtl(upLow, i)           
                cmds.parent(upLow +'LipDetailP'+ str(i), lipDetailP)
                cmds.setAttr (upLow +'LipDetailP'+ str(i) + '.tx', increment*i) 
                cmds.setAttr (upLow +'LipDetailP'+ str(i) + '.ty', 0)
                cmds.setAttr (upLow +'LipDetailP'+ str(i) + '.tz', 0)
            
            #- create lipCtrl curve POC
            lipCrvPoc = self.createPocNode(upLow +'LipCrv' + str(i) + '_poc', lipCtlCrvShape[0], increment*i)
            
            #- create lipCtrl curve POC
            ctlPoc = self.createPocNode(upLow +'LipCtl' + str(i) + '_poc', lipCrvShape[0], increment*i)

        return {'lipJntGrp' : lipJotGrp , 'lipCrvGrp' : lipCrvGrp}