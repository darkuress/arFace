#- author
#- Jonghwan Hwang

from functools import partial
import maya.cmds as cmds
from Eyelid import Setup as EyelidSetup
reload(EyelidSetup)
from Eyebrow import Setup as EyebrowSetup
reload(EyebrowSetup)
from Misc import Core
import json
import os

if cmds.window('faceSetupUI', ex = True):
    cmds.deleteUI('faceSetupUI')    
cmds.window('faceSetupUI', widthHeight=(600, 500) )

class UI(Core.Core):
    def __init__(self):
        
        """
        UI Main function
        """
        Core.Core.__init__(self)
        
        form = cmds.formLayout()
        #- creating tabs
        tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        cmds.formLayout(form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

        #- first tab{
        runAllTab = cmds.columnLayout()
            
        #- select and save vertexes text field menus 
        cmds.rowColumnLayout(numberOfColumns=3)       
        cmds.text(label='Eyebrow Vertexes : ', w = 150)
        if self.locData.has_key('eyebrowVtxs'):
            insertText = self.locData['eyebrowVtxs']
        else:
            insertText = ''
        self.eyebrowVertsTextField = cmds.textField('eyebrowVertsTextField', tx = insertText, w = 300)
        cmds.button(label = '        <<        ', c = self.updateEyebrowVtxTextField)
        cmds.setParent('..' )

        cmds.rowColumnLayout(numberOfColumns=3)
        cmds.text(label='Eyebrow Locator : ', w = 150)
        if self.locData.has_key('eyebrowLoc'):
            insertText = self.locData['eyebrowLoc']
        else:
            insertText = ''
        self.eyebrowLocTextField = cmds.textField('eyebrowLocTextField', tx = insertText, w = 300)
        cmds.button(label = '        <<        ', c = self.updateEyebrowLocTextField)
        cmds.setParent('..' )

        cmds.rowColumnLayout(numberOfColumns=3)       
        cmds.text(label='Up Eyelid Vertexes : ', w = 150)
        if self.locData.has_key('upEyelidVtxs'):
            insertText = self.locData['upEyelidVtxs']
        else:
            insertText = ''            
        self.upEyelidVertsTextField = cmds.textField('upEyelidVertsTextField', tx = insertText, w = 300)
        cmds.button(label = '        <<        ', c = self.updateUpEyelidVtxTextField)
        cmds.setParent('..' )

        cmds.rowColumnLayout(numberOfColumns=3)       
        cmds.text(label='Low Eyelid Vertexes : ', w = 150)
        if self.locData.has_key('loEyelidVtxs'):
            insertText = self.locData['loEyelidVtxs']
        else:
            insertText = ''      
        self.loEyelidVertsTextField = cmds.textField('loEyelidVertsTextField', tx = insertText, w = 300)
        cmds.button(label = '        <<        ', c = self.updateLoEyelidVtxTextField)
        cmds.setParent('..' )
        
        #- Global controller size, offset and rotate scale menu
        cmds.rowColumnLayout(numberOfColumns=1)
        cmds.separator( height=20, width = 600, style='in' )
        cmds.setParent('..')
        
        cmds.rowColumnLayout(numberOfColumns=3)
        
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.text(label='Controller Size : ', w = 100)
        self.globCtrlSizeTextField = cmds.textField('globCtrlSizeTextField', tx = 1, w = 30)
        cmds.setParent('..')
        
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.text(label='Controller Offset : ', w = 100)
        self.globCtrlOffsetTextField = cmds.textField('globCtrlOffsetTextField', tx = 1, w = 30)
        cmds.setParent('..')
        
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.text(label='Rotate Scale : ', w = 100)
        self.globRotateScaleTextField = cmds.textField('globRotateScaleTextField', tx = 10, w = 30)
        cmds.setParent('..')
        
        cmds.setParent('..')
        
        #- run all buttons
        cmds.rowColumnLayout(numberOfColumns=1)
        cmds.separator( height=20, width = 600, style='in' )
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.button(label = 'Save', c = self.saveInfoFile)
        cmds.button(label = 'Build/Rebuild')
        cmds.setParent('..')
        
        cmds.setParent('..')
        #-}
        
        #- second tab{
        eyelidTab = cmds.columnLayout()
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.button(label = 'Create Joints', c = partial(self.createEyebrowJoint))
        cmds.setParent('..')
        
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.button(label = 'Create Controller', c = partial(self.createEyebrowCtrl))
        cmds.columnLayout()
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.text('Controller Size    : ' )
        self.eyelidCtrlSizeTextField = cmds.textField('eyelidCtrlSizeTextField', tx = 1)
        cmds.setParent('..' )
        
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.text(label='Controller Offset : ' )
        self.eyelidCtrlOffsetTextField = cmds.textField('eyelidCtrlOffsetTextField', tx = 1)
        cmds.setParent('..' )
        
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.text(label='Rotate Scale       : ' )
        self.rotateScaleTextField = cmds.textField('eyelidRotateScaleTextField', tx = 10)
        cmds.setParent('..' )
        cmds.setParent('..' )
        cmds.setParent('..' )
        
        cmds.setParent('..' )
        #-}
        
        #- third tab{
        eyebrowTab = cmds.columnLayout()
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.button(label = 'Create Joints', c = partial(self.createEyebrowJoint))
        cmds.setParent('..')
        
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.button(label = 'Create Controller', c = partial(self.createEyebrowCtrl))
        cmds.columnLayout()
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.text('Controller Size    : ' )
        self.eyebrowCtrlSizeTextField = cmds.textField('eyebrowCtrlSizeTextField', tx = 1)
        cmds.setParent('..' )
        
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.text(label='Controller Offset : ' )
        self.eyebrowCtrlOffsetTextField = cmds.textField('eyebrowCtrlOffsetTextField', tx = 1)
        cmds.setParent('..' )
        
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.text(label='Rotate Scale       : ' )
        self.rotateScaleTextField = cmds.textField('eyebrowRotateScaleTextField', tx = 10)
        cmds.setParent('..' )
        cmds.setParent('..' )
        cmds.setParent('..' )
        
        cmds.setParent('..' )
        #-}
            
        cmds.tabLayout(tabs,
                       edit=True,
                       tabLabel=((runAllTab, 'Run It All'),
                                 (eyelidTab, 'eyelid'),
                                 (eyebrowTab, 'eyebrow'))
                       )
        
        cmds.showWindow()

           
    def saveInfoFile(self, *args):
        """
        save/update info file
        """
        locData = {}
        locData['eyebrowVtxs']   =  cmds.textField(self.eyebrowVertsTextField, q = True, tx = True)
        locData['eyebrowLoc']    =  cmds.textField(self.eyebrowLocTextField, q = True, tx = True)
        locData['upEyelidVtxs']  =  cmds.textField(self.upEyelidVertsTextField, q = True, tx = True)
        locData['loEyelidVtxs']  =  cmds.textField(self.loEyelidVertsTextField, q = True, tx = True)
        self.writeLocInfoData(locData)
    
    def updateEyebrowVtxTextField(self, *args):
        """
        updating save TextField
        """
        #- selected vertexes
        vtx = str(cmds.ls(sl = True, fl = True))
        cmds.textField(self.eyebrowVertsTextField, e = True, tx = vtx)

    def updateEyebrowLocTextField(self, *args):
        """
        updating save TextField
        """
        #- selected vertexes
        loc = str(cmds.ls(sl = True, fl = True))
        cmds.textField(self.eyebrowLocTextField, e = True, tx = loc)

    def updateUpEyelidVtxTextField(self, *args):
        """
        updating save TextField
        """
        #- selected vertexes
        vtx = str(cmds.ls(sl = True, fl = True))
        cmds.textField(self.upEyelidVertsTextField, e = True, tx = vtx)

    def updateLoEyelidVtxTextField(self, *args):
        """
        updating save TextField
        """
        #- selected vertexes
        vtx = str(cmds.ls(sl = True, fl = True))
        cmds.textField(self.loEyelidVertsTextField, e = True, tx = vtx)
    
    def __eyelidInstance(self, *args):
        """
        making eyelidSetup instance
        """
        eyelidCtrlSize    = cmds.textField(self.eyelidCtrlSizeTextField, q = True, tx = True)
        eyelidCtrlOffset  = cmds.textField(self.eyelidCtrlOffsetTextField, q = True, tx = True)
        eyelidRotateScale = cmds.textField(self.rotateScaleTextField, q = True, tx = True)
        
        eyelid = EyebrowSetup.Setup(size        = int(eyelidCtrlSize),
                                     offset      = int(eyelidCtrlOffset),
                                     rotateScale = int(eyelidRotateScale)
                                    )
        
        return eyelid
    
    def createEyebrowJoint(self, *args):
        """
        creating eyelid jnt
        """
        self.eyelid = self.__eyelidInstance()
        self.eyelid.createJoints()
        
    def createEyebrowCtrl(self, *args):
        """
        creating eyelid controllr
        """
        self.eyelid.createCtrls(self.eyelid.baseJnts)
    
    
    def __eyebrowInstance(self, *args):
        """
        making eyebrowSetup instance
        """
        eyebrowCtrlSize    = cmds.textField(self.eyebrowCtrlSizeTextField, q = True, tx = True)
        eyebrowCtrlOffset  = cmds.textField(self.eyebrowCtrlOffsetTextField, q = True, tx = True)
        eyebrowRotateScale = cmds.textField(self.rotateScaleTextField, q = True, tx = True)
        
        eyebrow = EyebrowSetup.Setup(size        = int(eyebrowCtrlSize),
                                     offset      = int(eyebrowCtrlOffset),
                                     rotateScale = int(eyebrowRotateScale)
                                    )
        
        return eyebrow
    
    def createEyebrowJoint(self, *args):
        """
        creating eyebrow jnt
        """
        self.eyebrow = self.__eyebrowInstance()
        self.eyebrow.createJoints()
        
    def createEyebrowCtrl(self, *args):
        """
        creating eyebrow controllr
        """
        self.eyebrow.createCtrls(self.eyebrow.baseJnts)