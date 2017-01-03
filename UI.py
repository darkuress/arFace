#- author
#- Jonghwan Hwang

from functools import partial
import maya.cmds as cmds
from Misc import Core
reload(Core)
import json
import os

if cmds.window('faceSetupUI', ex = True):
    cmds.deleteUI('faceSetupUI')    
cmds.window('faceSetupUI',menuBar=True, widthHeight=(600, 500), bgc = [0.25, 0.3, 0.3] )

class UI(Core.Core):
    def __init__(self, configFile = ''):
        
        """
        UI Main function
        """
        Core.Core.__init__(self, configFile = configFile)
        
        self.configFile = configFile
		
        #- some color definition
        self.textColor = [0.8, 0.7, 0.6]
        self.buttonColor = [0.64, 0.42, 0.33]
        self.buttonColor2 = [0.44, 0.23, 0.8]
        
        #- constructing Menu Items
        cmds.menu(label='File')
        cmds.menuItem(label='Open Info.json', c = partial(self.openInfoFile))
        cmds.menuItem(label='Save Info.json', c = partial(self.saveInfoFile))

        cmds.menu(label='Tools')
        cmds.menuItem(label = 'NG Skin Tool', c = partial(self.openNgSkinTool))
        cmds.menuItem(label = 'Copy Layer Tool', c = partial(self.openCopyLayersTool))
        
        cmds.menu(label='Help')
        cmds.menuItem(label='Ask sshin')
                        
        form = cmds.formLayout()
        
        #- creating tabs
        tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        cmds.formLayout(form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

        #- first tab{
        runAllTab = cmds.columnLayout()
        
        cmds.rowColumnLayout(numberOfColumns=3)
        cmds.text(label='Head Geo : ', w = 150, bgc = self.textColor)
        if self.locData.get('headGeo'):
            insertText = str(self.locData['headGeo'])
        else:
            insertText = ''
        self.headGeoTextField = cmds.textField('headGeoTextField', ed = False, tx = insertText, w = 300)
        cmds.button(label = '        <<        ', bgc = self.buttonColor, c = self.updateHeadGeoTextField)
        cmds.setParent('..' )
        
        #- select and save vertexes text field menus 
        cmds.rowColumnLayout(numberOfColumns=3)
        cmds.text(label='Setup Locators : ', w = 150, bgc = self.textColor)
        if self.locData.get('setupLoc'):
            insertText = str(self.locData['setupLoc'].keys())
        else:
            insertText = ''
        self.setupLocTextField = cmds.textField('setupLocTextField', ed = False, tx = insertText, w = 300)
        cmds.button(label = '        <<        ', bgc = self.buttonColor, c = self.updateSetupLocTextField)
        cmds.setParent('..' )

        cmds.rowColumnLayout(numberOfColumns=4)       
        cmds.text(label='Eyebrow Vertexes : ', w = 150, bgc = self.textColor)
        if self.locData.has_key('eyebrowVtxs'):
            insertText = self.locData['eyebrowVtxs']
        else:
            insertText = ''
        self.eyebrowVertsTextField = cmds.textField('eyebrowVertsTextField', ed = False, tx = insertText, w = 300)
        cmds.button(label = '        <<        ', bgc = self.buttonColor, c = self.updateEyebrowVtxTextField)
        cmds.button(label = 'Select', bgc = self.buttonColor2, c = partial(self.selectVertexes, self.eyebrowVertsTextField))
        cmds.setParent('..' )

        cmds.rowColumnLayout(numberOfColumns=4)       
        cmds.text(label='Up Eyelid Vertexes : ', w = 150, bgc = self.textColor)
        if self.locData.has_key('upEyelidVtxs'):
            insertText = self.locData['upEyelidVtxs']
        else:
            insertText = ''            
        self.upEyelidVertsTextField = cmds.textField('upEyelidVertsTextField', ed = False, tx = insertText, w = 300)
        cmds.button(label = '        <<        ', bgc = self.buttonColor, c = self.updateUpEyelidVtxTextField)
        cmds.button(label = 'Select', bgc = self.buttonColor2, c = partial(self.selectVertexes, self.upEyelidVertsTextField))
        cmds.setParent('..' )

        cmds.rowColumnLayout(numberOfColumns=4)       
        cmds.text(label='Low Eyelid Vertexes : ', w = 150, bgc = self.textColor)
        if self.locData.has_key('loEyelidVtxs'):
            insertText = self.locData['loEyelidVtxs']
        else:
            insertText = ''      
        self.loEyelidVertsTextField = cmds.textField('loEyelidVertsTextField', ed = False, tx = insertText, w = 300)
        cmds.button(label = '        <<        ', bgc = self.buttonColor, c = self.updateLoEyelidVtxTextField)
        cmds.button(label = 'Select', bgc = self.buttonColor2, c = partial(self.selectVertexes, self.loEyelidVertsTextField))
        cmds.setParent('..' )

        cmds.rowColumnLayout(numberOfColumns=4)
        cmds.text(label='Corner Eyelid Vertexes : ', w = 150, bgc = self.textColor)
        if self.locData.has_key('cnrEyelidVtxs'):
            insertText = self.locData['cnrEyelidVtxs']
        else:
            insertText = ''      
        self.cnrEyelidVertsTextField = cmds.textField('cnrEyelidVertsTextField', ed = False, tx = insertText, w = 300)
        cmds.button(label = '        <<        ', bgc = self.buttonColor, c = self.updateCnrEyelidVtxTextField)
        cmds.button(label = 'Select', bgc = self.buttonColor2, c = partial(self.selectVertexes, self.cnrEyelidVertsTextField))
        cmds.setParent('..' )

        cmds.rowColumnLayout(numberOfColumns=4)
        cmds.text(label='Up lip Vertexes : ', w = 150, bgc = self.textColor)
        if self.locData.has_key('upLipVtxs'):
            insertText = self.locData['upLipVtxs']
        else:
            insertText = ''      
        self.upLipVertsTextField = cmds.textField('upLipVertsTextField', ed = False, tx = insertText, w = 300)
        cmds.button(label = '        <<        ', bgc = self.buttonColor, c = self.updateUpLipVtxTextField)
        cmds.button(label = 'Select', bgc = self.buttonColor2, c = partial(self.selectVertexes, self.upLipVertsTextField))
        cmds.setParent('..' )

        cmds.rowColumnLayout(numberOfColumns=4)
        cmds.text(label='Low lip Vertexes : ', w = 150, bgc = self.textColor)
        if self.locData.has_key('loLipVtxs'):
            insertText = self.locData['loLipVtxs']
        else:
            insertText = ''      
        self.loLipVertsTextField = cmds.textField('loLipVertsTextField', ed = False, tx = insertText, w = 300)
        cmds.button(label = '        <<        ', bgc = self.buttonColor, c = self.updateLoLipVtxTextField)
        cmds.button(label = 'Select', bgc = self.buttonColor2, c = partial(self.selectVertexes, self.loLipVertsTextField))
        cmds.setParent('..' )
        
        
        ##- Global controller size, offset and rotate scale menu
        #cmds.rowColumnLayout(numberOfColumns=1)
        #cmds.separator( height=20, width = 600, style='in' )
        #cmds.setParent('..')
        
        #cmds.rowColumnLayout(numberOfColumns=3)
        #
        #cmds.rowColumnLayout(numberOfColumns = 2)
        #cmds.text(label='Controller Size : ', w = 100)
        #self.globCtrlSizeTextField = cmds.textField('globCtrlSizeTextField', tx = 1, w = 30)
        #cmds.setParent('..')
        #
        #cmds.rowColumnLayout(numberOfColumns = 2)
        #cmds.text(label='Controller Offset : ', w = 100)
        #self.globCtrlOffsetTextField = cmds.textField('globCtrlOffsetTextField', tx = 1, w = 30)
        #cmds.setParent('..')
        #
        #cmds.rowColumnLayout(numberOfColumns = 2)
        #cmds.text(label='Rotate Scale : ', w = 100)
        #self.globRotateScaleTextField = cmds.textField('globRotateScaleTextField', tx = 10, w = 30)
        #cmds.setParent('..')
        #
        #cmds.setParent('..')
        
        #- run all buttons
        cmds.rowColumnLayout(numberOfColumns=1)
        cmds.separator( height=20, width = 600, style='in' )
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns = 3)
        cmds.button(label = 'Build Foundation', c = self.buildFoundation)
        cmds.button(label = 'Build/Rebuild')
        cmds.setParent('..')

        cmds.setParent('..')
        #-}

        #- second tab{
        foundationTab = cmds.columnLayout()
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Import Locators', w = 200, c = partial(self.importFacialLoc))
        cmds.setParent('..')

        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Create Hierarchy', w = 200, c = partial(self.createHierarchy))
        cmds.setParent('..')

        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Import Control Panel', w = 200, c = partial(self.importControlPanel))
        cmds.setParent('..')

        cmds.setParent('..' )
        #-}
        
        #- thrid tab{
        eyelidTab = cmds.columnLayout()
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Create Joints', c = partial(self.createEyelidJoint))
        cmds.setParent('..')
        
        cmds.separator( height=20, width = 600, style='in' )
        
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Create Controller', c = partial(self.createEyelidCtrl))
        cmds.columnLayout()
        
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.text('Controller Size    : ' )
        self.eyelidCtrlSizeTextField = cmds.textField('eyelidCtrlSizeTextField', tx = 1)
        cmds.setParent('..')
        
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.text(label='Controller Offset : ' )
        self.eyelidCtrlOffsetTextField = cmds.textField('eyelidCtrlOffsetTextField', tx = 1)
        cmds.setParent('..')
        
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.text(label='Rotate Scale       : ' )
        self.eyelidRotateScaleTextField = cmds.textField('eyelidRotateScaleTextField', tx = 10)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        
        cmds.separator( height=20, width = 600, style='in' )
        
        cmds.rowColumnLayout(numberOfColumns = 1)
        cmds.button(label = 'Create Curve Camera', c = partial(self.createCurveCam))
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns = 2)
        self.lUpLidCrvOptionMenu = cmds.optionMenu(label='Left   Up',
                                                   changeCommand = partial(self.runLidCrvDropdownMenu, 'lUp'))
        self.rUpLidCrvOptionMenu = cmds.optionMenu(label='Right  Up',
                                                   changeCommand = partial(self.runLidCrvDropdownMenu, 'rUp'))
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns = 2)
        self.lLoLidCrvOptionMenu = cmds.optionMenu(label='Left Low',
                                                   changeCommand = partial(self.runLidCrvDropdownMenu, 'lLo'))
        
        self.rLoLidCrvOptionMenu = cmds.optionMenu(label='Right Low',
                                                   changeCommand = partial(self.runLidCrvDropdownMenu, 'rLo'))
        self.updateLidCrvDropdownMenu()
        cmds.setParent('..')
        
        cmds.separator( height=20, width = 600, style='in' )
        
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Save Curves', c = partial(self.saveEyelidCurve), en = False)
        cmds.button(label = 'Load Curves', c = partial(self.loadEyelidCurve), en = False)
        cmds.setParent('..')
        
        cmds.setParent('..')
        #-}
        
        #- forth tab{
        eyebrowTab = cmds.columnLayout()
        
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Create Joints', c = partial(self.createEyebrowJoint))
        cmds.setParent('..')
        
        cmds.separator( height=20, width = 600, style='in' )
        
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Create Controller', c = partial(self.createEyebrowCtrl))
        cmds.columnLayout()
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.text('Controller Size    : ' )
        self.eyebrowCtrlSizeTextField = cmds.textField('eyebrowCtrlSizeTextField', tx = 1)
        cmds.setParent('..' )
        
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.text(label='Controller Offset : ' )
        self.eyebrowCtrlOffsetTextField = cmds.textField('eyebrowCtrlOffsetTextField', tx = 1)
        cmds.setParent('..' )
        
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.text(label='Rotate Scale       : ' )
        self.eyebrowRotateScaleTextField = cmds.textField('eyebrowRotateScaleTextField', tx = 10)
        cmds.setParent('..' )
        cmds.setParent('..' )
        cmds.setParent('..' )       
        
        cmds.separator( height=20, width = 600, style='in' )
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Create Surface Map Geo', w = 200, c = partial(self.createBrowSurfaceMapGeo))
        cmds.setParent('..')
        
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Skin Eyebrow Map Surface', w = 200, c = partial(self.skinBrowSurfaceMapGeo))
        cmds.setParent('..')
        
        cmds.setParent('..' )
        #-}

        #- fifth tab{
        lipTab = cmds.columnLayout()
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Create Joints', c = partial(self.createLipJoint))
        cmds.setParent('..')
        
        cmds.separator( height=20, width = 600, style='in' )
        
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Create Controller', c = partial(self.createLipCtrl))
        cmds.setParent('..')

        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.text(label='Rotate Scale       : ' )
        self.lipRotateScaleTextField = cmds.textField('lipRotateScaleTextField', tx = 10)
        cmds.setParent('..' )
        cmds.setParent('..' )

        cmds.separator( height=20, width = 600, style='in' )
        
        cmds.button(label = 'Curve on edge loop', c = partial(self.curveOnEdgeLoop))
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Loft Face Part',     c = partial(self.loftFacePart))
        self.loftFacePartTextField = cmds.textField('loftFacepartTextField', tx = '')
        cmds.setParent('..' )
        
        cmds.separator( height=20, width = 600, style='in' )

        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Copy CV weight', c = partial(self.copyCvWeights), en = False)
        cmds.setParent('..')
        
        cmds.separator( height=20, width = 600, style='in' )
        
        cmds.setParent('..' )
        
        #- sixth tab{
        skinningTab = cmds.columnLayout()
        cmds.rowColumnLayout(numberOfColumns = 2)      
        cmds.text('External Tool ', bgc = [0.5, 0.5, 0])
        cmds.separator( height=20, width = 600, style='in' )
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns = 1)      
        cmds.button(label = 'NG Skin Tool', c = partial(self.openNgSkinTool))
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns = 1)      
        cmds.button(label = 'Copy Layer Tool', c = partial(self.openCopyLayersTool))                
        cmds.setParent('..')
        
        cmds.rowColumnLayout(numberOfColumns = 2)    
        cmds.text('Eyelid ', bgc = [0.5, 0.5, 0])
        cmds.separator( height=20, width = 600, style='in')
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns = 1)
        cmds.button(label = 'Create Curve Camera', c = partial(self.createCurveCam))
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns = 2)
        self.lUpLidCrvOptionMenu = cmds.optionMenu(label='Left   Up',
                                                   changeCommand = partial(self.runLidCrvDropdownMenu, 'lUp'))
        self.rUpLidCrvOptionMenu = cmds.optionMenu(label='Right  Up',
                                                   changeCommand = partial(self.runLidCrvDropdownMenu, 'rUp'))
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns = 2)
        self.lLoLidCrvOptionMenu = cmds.optionMenu(label='Left Low',
                                                   changeCommand = partial(self.runLidCrvDropdownMenu, 'lLo'))
        
        self.rLoLidCrvOptionMenu = cmds.optionMenu(label='Right Low',
                                                   changeCommand = partial(self.runLidCrvDropdownMenu, 'rLo'))
        self.updateLidCrvDropdownMenu()
        cmds.setParent('..')
        
        
        cmds.rowColumnLayout(numberOfColumns = 2)    
        cmds.text('Eyebrow ', bgc = [0.5, 0.5, 0])
        cmds.separator( height=20, width = 600, style='in' )
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Create Surface Map Geo', w = 200, c = partial(self.createBrowSurfaceMapGeo))
        cmds.setParent('..')
        
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Skin Eyebrow Map Surface', w = 200, c = partial(self.skinBrowSurfaceMapGeo))
        cmds.setParent('..')        
        
        cmds.rowColumnLayout(numberOfColumns = 2)    
        cmds.text('Lip ', bgc = [0.5, 0.5, 0])
        cmds.separator( height=20, width = 600, style='in')
        cmds.setParent('..')
        cmds.button(label = 'Curve on edge loop', c = partial(self.curveOnEdgeLoop))
        cmds.rowColumnLayout(numberOfColumns = 2)
        cmds.button(label = 'Loft Face Part',     c = partial(self.loftFacePart))
        self.loftFacePartTextField = cmds.textField('loftFacepartTextField', tx = '')
        cmds.setParent('..' )
        
        cmds.setParent('..')
        #-}
        
        cmds.tabLayout(tabs,
                       edit=True,
                       tabLabel=((foundationTab, 'foundation'),
                                 (runAllTab, 'Run It All'),
                                 (eyelidTab, 'eyelid'),
                                 (eyebrowTab, 'eyebrow'),
                                 (lipTab, 'lip'),
                                 (skinningTab, 'skinning'))
                      )
        
        self.updateSelfLocData()
    
    def importFacialLoc(self, *args):
        """
        importing the locators to start
        """
        from Foundation import ImportMa
        reload(ImportMa)        
        ifl = ImportMa.Create(configFile = self.configFile)
        FacialLocTopNode = ifl.importLocators()
        FacialLocTopNode = ifl.placeLocators()
        
    def createHierarchy(self, *args):
        """
        create basic container structure for face rig
        with FaceFactors
        """
        from Foundation import Container
        reload(Container)        
        ch = Container.Container(configFile = self.configFile)
        ch.placeFaceRig()

        from Foundation import FaceFactor
        reload(FaceFactor)
        fcf = FaceFactor.FaceFactor(configFile = self.configFile)
        faceFactorNode = fcf.create()

    def importControlPanel(self, *args):
        """
        importing the halp panel
        """
        from Foundation import ImportMa
        reload(ImportMa)
        ihp = ImportMa.Create(configFile = self.configFile)
        panelTopNode = ihp.importHelpPanel()

    def buildFoundation(self, *args):
        """
        build all foundation together
        """
        self.importFacialLoc()
        self.createHierarchy()
        self.importControlPanel()

    def updateSelfLocData(self, *args):
        """
        update self.locData with Text Field's value
        """
        from Foundation import SetupLoc
        reload(SetupLoc)
        
        self.locData = {}
        locNameData                   = cmds.textField(self.setupLocTextField, q = True, tx = True)
        self.locData['headGeo']       = cmds.textField(self.headGeoTextField, q = True, tx = True) 
        self.locData['setupLoc']      = SetupLoc.SetupLoc.saveLocPos(locNameData) if locNameData else {}
        self.locData['eyebrowVtxs']   = cmds.textField(self.eyebrowVertsTextField, q = True, tx = True)
        self.locData['upEyelidVtxs']  = cmds.textField(self.upEyelidVertsTextField, q = True, tx = True)
        self.locData['loEyelidVtxs']  = cmds.textField(self.loEyelidVertsTextField, q = True, tx = True)
        self.locData['cnrEyelidVtxs'] = cmds.textField(self.cnrEyelidVertsTextField, q = True, tx = True)
        self.locData['upLipVtxs']     = cmds.textField(self.upLipVertsTextField, q = True, tx = True)
        self.locData['loLipVtxs']     = cmds.textField(self.loLipVertsTextField, q = True, tx = True)
        
        return self.locData

    def saveInfoFile(self, *args):
        """
        save/update info file
        """       
        locData = self.updateSelfLocData()
        
        try:
            filename = cmds.fileDialog2(fileMode=0, caption="Save Info.json")[0]
                    
            self.writeLocInfoData(locData, jsonPath = filename)
            cmds.confirmDialog(title='Info Saved',
                               message='Location : %s' %filename,
                               button=['ok'],
                               defaultButton='ok')
        except:
            pass

    def openInfoFile(self, *args):
        """
        manually load info.json
        """
        filename = str(cmds.fileDialog2(fileMode=1, caption="Import Info.json")[0])
        self.locData = self.updateLocdata(filename)
        self.updateLocFields(self.locData)

    def updateLocFields(self, locData, *args):
        """
        update locator data in the text field
        """        
        if locData.get('headGeo'):
            self.headGeoTextField = cmds.textField(self.headGeoTextField, e = True, tx = locData['headGeo'])
        else:
            self.headGeoTextField = cmds.textField(self.headGeoTextField, e = True, tx = '')
        
        
        if locData.get('setupLoc'):
            insertText = str(self.locData['setupLoc'].keys())
        else:
            insertText = ''
        cmds.textField(self.setupLocTextField, e = True, tx = insertText)
        
        if locData.has_key('eyebrowVtxs'):
            insertText = locData['eyebrowVtxs']
        else:
            insertText = ''
        cmds.textField(self.eyebrowVertsTextField, e = True, tx = insertText)
        
        if locData.has_key('upEyelidVtxs'):
            insertText = locData['upEyelidVtxs']
        else:
            insertText = ''            
        cmds.textField(self.upEyelidVertsTextField, e = True, tx = insertText)
        
        if locData.has_key('loEyelidVtxs'):
            insertText = locData['loEyelidVtxs']
        else:
            insertText = ''      
        cmds.textField(self.loEyelidVertsTextField, e = True, tx = insertText)
        
        if locData.has_key('cnrEyelidVtxs'):
            insertText = self.locData['cnrEyelidVtxs']
        else:
            insertText = ''      
        cmds.textField(self.cnrEyelidVertsTextField, e = True, tx = insertText)
        
        if locData.has_key('upLipVtxs'):
            insertText = locData['upLipVtxs']
        else:
            insertText = ''      
        cmds.textField(self.upLipVertsTextField, e = True, tx = insertText)
        
        if locData.has_key('loLipVtxs'):
            insertText = locData['loLipVtxs']
        else:
            insertText = ''      
        cmds.textField(self.loLipVertsTextField, e = True, tx = insertText)
        
    def updateEyebrowVtxTextField(self, *args):
        """
        updating save TextField
        """
        #- selected vertexes
        vtx = str(cmds.ls(sl = True, fl = True))
        cmds.textField(self.eyebrowVertsTextField, e = True, tx = vtx)

    def updateHeadGeoTextField(self, *args):
        """
        updating save TextField
        """
        #- selected vertexes
        headGeo = str(cmds.ls(sl = True, fl = True)[0])
        cmds.textField(self.headGeoTextField, e = True, tx = headGeo)

    def updateSetupLocTextField(self, *args):
        """
        updating save TextField
        """
        #- selected vertexes
        loc = str(cmds.ls(sl = True, fl = True))
        cmds.textField(self.setupLocTextField, e = True, tx = loc)

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

    def updateCnrEyelidVtxTextField(self, *args):
        """
        updating save TextField
        """
        #- selected vertexes
        vtx = str(cmds.ls(sl = True, fl = True))
        cmds.textField(self.cnrEyelidVertsTextField, e = True, tx = vtx)
        
    def updateUpLipVtxTextField(self, *args):
        """
        updating save TextField
        """
        #- selected vertexes
        vtx = str(cmds.ls(sl = True, fl = True))
        cmds.textField(self.upLipVertsTextField, e = True, tx = vtx)

    def updateLoLipVtxTextField(self, *args):
        """
        updating save TextField
        """
        #- selected vertexes
        vtx = str(cmds.ls(sl = True, fl = True))
        cmds.textField(self.loLipVertsTextField, e = True, tx = vtx)        
        
    def selectVertexes(self, txtField, *args):
        """
        select vertexes in text field
        """
        parts = cmds.textField(txtField, q = True, tx = True)
        if parts:
            cmds.select(eval(parts), r = True)
        else:
            cmds.select(cl = True)
    
    def __eyelidInstance(self, *args):
        """
        making eyelidSetup instance
        """
        #- somehow it's not working when everything is imported at the top
        locData = self.updateSelfLocData()
        from Eyelid import Setup as EyelidSetup
        reload(EyelidSetup)
        eyelidCtrlSize    = cmds.textField(self.eyelidCtrlSizeTextField, q = True, tx = True)
        eyelidCtrlOffset  = cmds.textField(self.eyelidCtrlOffsetTextField, q = True, tx = True)
        eyelidRotateScale = cmds.textField(self.eyelidRotateScaleTextField, q = True, tx = True)
        
        upperEyelid = EyelidSetup.Setup(size        = float(eyelidCtrlSize),
                                        offset      = float(eyelidCtrlOffset),
                                        rotateScale = float(eyelidRotateScale),
                                        upDown      = self.uploPrefix[0],
                                        locData     = locData
                                        )
        lowerEyelid = EyelidSetup.Setup(size        = float(eyelidCtrlSize),
                                        offset      = float(eyelidCtrlOffset),
                                        rotateScale = float(eyelidRotateScale),
                                        upDown      = self.uploPrefix[1],
                                        locData     = locData
                                        )
        cornerEyelid = EyelidSetup.Setup(size       = float(eyelidCtrlSize),
                                        offset      = float(eyelidCtrlOffset),
                                        rotateScale = float(eyelidRotateScale),
                                        upDown      = self.cnrPrefix,
                                        locData     = locData
                                        )
        
        return upperEyelid, lowerEyelid, cornerEyelid
        
    def createEyelidJoint(self, *args):
        """
        creating eyelid jnt
        """
        self.upperEyelid = self.__eyelidInstance()[0]
        self.lowerEyelid = self.__eyelidInstance()[1]
        self.cornerEyelid = self.__eyelidInstance()[2]
        self.upperEyelid.createJoints()
        self.lowerEyelid.createJoints()
        self.cornerEyelid.createJoints()
        
    def createEyelidCtrl(self, *args):
        """
        creating eyelid controllr
        """
        self.upperEyelid.createCtrls(self.upperEyelid.baseJnts + self.lowerEyelid.baseJnts)
        #self.lowerEyelid.createCtrls(self.lowerEyelid.baseJnts)

        self.updateLidCrvDropdownMenu()
    
    def connectToEyelidControlPanel(self, *args):
        """
        connect eyelid setup with control panel
        """
        self.lowerEyelid.connectToControlPanel()
        self.updateLidCrvDropdownMenu()
    
    def updateLidCrvDropdownMenu(self, *args):
        """
        update the curve list on drop down menu in eyelid panel
        """
        if cmds.objExists(self.eyelidCrvGrpName):
            topLidCrvGrp = cmds.listRelatives(self.eyelidCrvGrpName)
            for crv in topLidCrvGrp:
                if self.prefix[0] + self.uploPrefix[0] in crv:
                    cmds.optionMenu(self.lUpLidCrvOptionMenu, e = True)
                    cmds.menuItem(label = str(crv), p = self.lUpLidCrvOptionMenu)
                elif self.prefix[0] + self.uploPrefix[1] in crv:
                    cmds.optionMenu(self.lLoLidCrvOptionMenu, e = True)
                    cmds.menuItem(label = str(crv), p = self.lLoLidCrvOptionMenu)
                elif self.prefix[1] + self.uploPrefix[0] in crv:
                    cmds.optionMenu(self.rUpLidCrvOptionMenu, e = True)
                    cmds.menuItem(label = str(crv), p = self.rUpLidCrvOptionMenu)
                elif self.prefix[1] + self.uploPrefix[1] in crv:
                    cmds.optionMenu(self.rLoLidCrvOptionMenu, e = True)
                    cmds.menuItem(label = str(crv), p = self.rLoLidCrvOptionMenu)
    
    def createCurveCam(self, *args):
        """
        create orthographic camera for eyelid curve
        """
        curveCam = 'curveCam'
        if not cmds.objExists(curveCam + '*'):
            curveCam = cmds.camera(n = curveCam, orthographic = True)[0]
            curveCamShape = cmds.listRelatives(curveCam)[0]
            cmds.xform(curveCam, t = [0,0,5])
        else:
            curveCam = cmds.ls('curveCam*')
            curveCamShape = cmds.listRelatives(curveCam)[0]
        
        myLabel = 'Curve Panel'
        cmds.window(w = 500, h = 500, title='Curve Window')
        cmds.frameLayout(lv=0 )
        panel = cmds.modelPanel(l=myLabel )
        cmds.showWindow()

        cmds.lookThru(curveCamShape, panel)
                    
    def runLidCrvDropdownMenu(self, lrUplo, *args):
        """
        show only selected crv
        """
        from Eyelid import Func
        reload(Func)
        eyelidFunc = Func.Func()
        if lrUplo == 'lUp':
            if cmds.optionMenu(self.lUpLidCrvOptionMenu, q = True, v = True) == 'None':
                eyelidFunc.hideAlLCrv()
            else:
                eyelidFunc.showCrv(cmds.optionMenu(self.lUpLidCrvOptionMenu, q = True, v = True))
        elif lrUplo == 'lLo':
            if cmds.optionMenu(self.lLoLidCrvOptionMenu, q = True, v = True) == 'None':
                eyelidFunc.hideAlLCrv()
            else:
                eyelidFunc.showCrv(cmds.optionMenu(self.lLoLidCrvOptionMenu, q = True, v = True))
        elif lrUplo == 'rUp':
            if cmds.optionMenu(self.rUpLidCrvOptionMenu, q = True, v = True) == 'None':
                eyelidFunc.hideAlLCrv()
            else:
                eyelidFunc.showCrv(cmds.optionMenu(self.rUpLidCrvOptionMenu, q = True, v = True))
        elif lrUplo == 'rLo':
            if cmds.optionMenu(self.rLoLidCrvOptionMenu, q = True, v = True) == 'None':
                eyelidFunc.hideAlLCrv()
            else:
                eyelidFunc.showCrv(cmds.optionMenu(self.rLoLidCrvOptionMenu, q = True, v = True))
    
    def saveEyelidCurve(self, *args):
        """
        save all eyelid Curve's cv info as json file
        """
        from Eyelid import Func
        reload(Func)
        eyelidFunc = Func.Func()
        eyelidFunc.saveEyelidCrvInfo()
    
    def loadEyelidCurve(self, *args):
        """
        load all eyelid Curve's info from json file
        """
        from Eyelid import Func
        reload(Func)
        eyelidFunc = Func.Func()
        eyelidFunc.loadEyelidCrvInfo()
    
    def __eyebrowInstance(self, *args):
        """
        making eyebrowSetup instance
        """
        locData = self.updateSelfLocData()
        from Eyebrow import Setup as EyebrowSetup
        reload(EyebrowSetup)
        eyebrowCtrlSize    = cmds.textField(self.eyebrowCtrlSizeTextField, q = True, tx = True)
        eyebrowCtrlOffset  = cmds.textField(self.eyebrowCtrlOffsetTextField, q = True, tx = True)
        eyebrowRotateScale = cmds.textField(self.eyebrowRotateScaleTextField, q = True, tx = True)
        eyebrow = EyebrowSetup.Setup(size        = float(eyebrowCtrlSize),
                                     offset      = float(eyebrowCtrlOffset),
                                     rotateScale = float(eyebrowRotateScale),
                                     locData     = locData
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
        
    def connectToEyebrowControlPanel(self, *args):
        """
        connect eyebrow setup to control Panel
        """
        self.eyebrow.connectToControlPanel()

    def openNgSkinTool(self, *args):
        """
        open ngskin tool
        """
        cmds.loadPlugin('ngSkinTools', quiet = True)
        from ngSkinTools.ui.mainwindow import MainWindow
        MainWindow.open()        

    def openCopyLayersTool(self, *args):
        """
        open copyLayersTool
        """
        from External import copySkinLayers
        reload(copySkinLayers)
        cslWin = copySkinLayers.CopySkinLayersWindow.getInstance()
        cslWin.showWindow()

    def createBrowSurfaceMapGeo(self, *args):
        """
        create eyebrow surface map geo for skinning
        """
        self.eyebrow = self.__eyebrowInstance()
        headGeo = cmds.textField(self.headGeoTextField, q = True, tx = True)
        self.eyebrow.createSurfMapGeo(headGeo)
    
    def skinBrowSurfaceMapGeo(self, *args):
        """
        skin brow surface geo 
        """
        self.eyebrow = self.__eyebrowInstance()
        self.eyebrow.browMapSkinning()
        
    def __lipInstance(self, *args):
        """
        making lipSetup instance
        """
        locData = self.updateSelfLocData()
        from Lip import Setup as LipSetup
        reload(LipSetup)
        lipRotateScale = cmds.textField(self.lipRotateScaleTextField, q = True, tx = True)
        
        upLip = LipSetup.Setup(upDown = self.uploPrefix[0],
                               rotateScale = float(lipRotateScale),
                               locData = locData)
        loLip = LipSetup.Setup(upDown = self.uploPrefix[1],
                               rotateScale = float(lipRotateScale),
                               locData = locData)
        
        return upLip, loLip
    
    def createLipJoint(self, *args):
        """
        creating lip jnt
        """
        self.upLip = self.__lipInstance()[0]
        self.loLip = self.__lipInstance()[1]
        self.upLip.createJoints()
        self.loLip.createJoints()

    def createLipCtrl(self, *args):
        """
        creating eyebrow controllr
        """
        self.upLip.createCtrls()
        self.loLip.createCtrls()
        #self.upLip.prarendGrp()
        #self.loLip.prarendGrp()

    def curveOnEdgeLoop(self, *args):
        """
        curve on edge loop tool
        making it as static function? 
        """
        from Lip import Func
        reload(Func)
        lipFunc = Func.Func()
        lipFunc.curveOnEdgeLoop()
        
    def loftFacePart(self, *args):
        """
        curve on edge loop tool
        making it as static function? 
        """
        from Lip import Func
        reload(Func)
        lipFunc = Func.Func()
        facePart = cmds.textField(self.loftFacePartTextField, q = True, tx = True)
        lipFunc.loftFacePart()        
        
    def copyCvWeights(self, *args):
        """
        copy cv weights
        """
        from Lip import Func
        reload(Func)
        lipFunc = Func.Func()
        lipFunc.copyCvWeighs()
    
    def __bridgeInstance(self, *args):
        """
        making bridgeSetup instance
        """
        from Bridge import Setup as BridgeSetup
        reload(BridgeSetup)
        bridge = BridgeSetup.Setup()
        
        return bridge
    
    def createBridgeJoint(self, *args):
        """
        creating bridge Joints
        """
        self.bridge = self.__bridgeInstance()
        self.bridge.createJoints()
        
        
    def loadInMaya(self, *args):
        """
        """
        cmds.showWindow()
        