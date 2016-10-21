#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright (c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

import maya.cmds as cmds
import Joints
reload(Joints)
import Ctrls
reload(Ctrls)

class Setup(Joints.Joints, Ctrls.Ctrls):
    def __init__(self,
                 size = 1,
                 offset = 1,
                 rotateScale = 10,
                 upDown = 'up',
                 **kw):
        """
        initializing variables
        """
        Joints.Joints.__init__(self, **kw)
        Ctrls.Ctrls.__init__(self, upDown, size, offset, rotateScale, **kw)
        self.upDown = upDown
        if kw.get('locData'):
            self.locData = kw.get('locData')

        #eyelid joints and location position 
        self.upEyelidVtxs    = self.locData.get('upEyelidVtxs', [])
        self.loEyelidVtxs    = self.locData.get('loEyelidVtxs', [])
        self.cnrEyelidVtxs   = self.locData.get('cnrEyelidVtxs', [])
        if self.locData.get('setupLoc'):
            self.lEyeLoc     = str([x for x in self.locData['setupLoc'] if 'eye' in x.lower()][0])
        else:
            self.lEyeLoc     = ''

    def createJoints(self):
        """
        creating joints on selected vertaxes
        """
        baseJntsP = self.createJnts(updown        = self.upDown,
                                    upEyelidVtxs  = self.upEyelidVtxs,
                                    loEyelidVtxs  = self.loEyelidVtxs,
                                    cnrEyelidVtxs = self.cnrEyelidVtxs)
        self.group(baseJntsP, self.eyelidJntGrpName)
        if not cmds.listRelatives(self.eyelidJntGrpName, p = True):
            cmds.parent(self.eyelidJntGrpName, self.jntGrp)
        
        return self.eyelidJntGrpName
    
    def createCtrls(self, jnts):
        """
        select base joints and run the script
        """
        cmds.select(cl = True)
        self.ctrlInfo = self.createLidCtrls(jnts, self.lEyeLoc)
        #self.group(self.ctrlInfo['lidsCtlGrp'], self.eyelidCtlGrpName)
        #self.group(self.ctrlInfo['lidsCrvGrp'], self.eyelidCrvGrpName)
        #
        #if not cmds.listRelatives(self.eyelidCtlGrpName, p = True):
        #    cmds.parent(self.eyelidCtlGrpName, self.ctlGrp)
        #if not cmds.listRelatives(self.eyelidCrvGrpName, p = True):
        #    cmds.parent(self.eyelidCrvGrpName, self.crvGrp)        
        #
        #self.allCrvs = self.hideAlLCrv()
        
        #return self.eyelidCtlGrpName, self.eyelidCrvGrpName
    
    def connectToControlPanel(self):
        """
        connect lid control to panel
        """
        self.connectToPanel(self.ctrlInfo['numJnts'])
    
    def helpPanel(self):
        """
        doing the helpPanel Thing
        """
        ctlNames = ['eyeCtl', 'eyeBlink', 'eyeSquint', 'eyeSquach' ]
        for ctlName in ctlNames:
            self.createHelpPanel(ctlName, type = 'A')
        self.helpPanelToEyeCrv()
    
    def blinkConnect(self):
        """
        connect blink after adjusting blink curve
        feeding joint's X rotateion value into EyelidBlinkGap_yAdd
        """
        for lr in self.prefix:
            index = 1
            blinkGapNodes = cmds.ls(lr + self.uplo[1] + 'EyelidBlinkGap_yAdd*')
            for blinkGapNode in blinkGapNodes:
                blinkJnt = self.prefix[0] + self.uplo[0] + 'LidBlink' + str(index).zfill(2) + self.jntSuffix
                blinJntRo = cmds.xform(blinkJnt, ro = True, q = True)
                cmds.setAttr(blinkGapNode + '.input2', blinJntRo[0])
                index = index + 1
        
        
    def saveVertaxPos(self):
        pass
    
    