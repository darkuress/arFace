import maya.cmds as cmds
import os
import json
from sys import platform as _platform

class Core(object):
    """
    core class to define variables
    """
    def __init__(self,
                 cPrefix        = 'c_',
                 prefix         = ['l_', 'r_'],
                 uploPrefix     = ['up', 'lo'],
                 cnrPrefix      = 'cnr',
                 ctlSuffix      = '_ctl',
                 jntSuffix      = '_jnt',
                 grpSuffix      = '_grp',
                 crvSuffix      = '_crv',
                 jntGrp         = 'jnt_grp',
                 crvGrp         = 'crv_grp',
                 clsGrp         = 'cls_grp',
                 ctlGrp         = 'ctl_grp',
                 jsonFileName   = 'info.json',
                 jsonBasePath   = '/corp/projects/eng/jhwang/svn/test/facialTest',
                 baseMaPath     = '/corp/projects/eng/jhwang/svn/maya/arFace/maFiles',
                 configFile     = '', 
                 panelFilename  = 'panel.ma',
                 panelTopNode   = 'Panel',
                 faceMainNode   = 'faceMain',
                 faceLocTopNode = 'faceLoc_grp',
                 locFileName    = 'locators.ma',
                 faceFactors    = {},
                 **kw):
        """
        basic variables
        """
        if not configFile:
            jsonBasePath  = ''
            baseMaPath = os.path.dirname(os.path.abspath(__file__)).replace('Misc', 'maFiles')
        elif configFile and os.path.exists(configFile):
            try:
                configJsonData = open(configFile)
                self.configData = json.load(configJsonData)
                if _platform == 'win32':
                    jsonBasePath  = self.configData['windows']['jsonBasePath']
                    baseMaPath    = self.configData['windows']['baseMaPath']
                    
                elif _platform == 'linux2':
                    jsonBasePath  = self.configData['linux']['jsonBasePath']
                    baseMaPath    = self.configData['linux']['baseMaPath']
            except:
                raise ValueError("%s is not a valid pass or file is empty" %configFile)
        #else:
        #    #- checking os type in test mode
        #    if _platform == 'win32':
        #        #jsonBasePath  = os.path.join('F:', os.sep, 'facialTest')
        #        jsonBasePath  = os.path.join('j:', os.sep, 'work_place', 'facialTest')
        #        baseMaPath      = os.path.join('C:', os.sep, 'documents', 'maya', 'maya2015', 'scripts', 'arFace', 'maFiles')
        # 
        #    elif _platform == 'linux2':
        #       jsonBasePath  = '/corp/projects/eng/jhwang/svn/test/facialTest'
        
        self.cPrefix          = cPrefix
        self.prefix           = prefix
        self.uploPrefix       = uploPrefix
        self.cnrPrefix        = cnrPrefix
        self.ctlSuffix        = ctlSuffix
        self.jntSuffix        = jntSuffix
        self.grpSuffix        = grpSuffix
        self.crvSuffix        = crvSuffix
        
        self.crvGrp           = crvGrp
        self.jntGrp           = jntGrp
        self.clsGrp           = clsGrp
        self.ctlGrp           = ctlGrp
        
        self.panelPath        = os.path.join(baseMaPath, panelFilename)
        self.faceLocPath      = os.path.join(baseMaPath, locFileName)
        
        self.panelTopNode     = panelTopNode
        self.faceLocTopNode   = faceLocTopNode
        
		#- for UI
        self.eyelidCrvGrpName  = 'eyelidCrv' + self.grpSuffix
        
        #- all factors
        self.lidFactorList  = []
        self.lidFactorList = self.lidFactorList + ['lidRotateX_scale', 'lidRotateY_scale', 'eyeBallRotX_scale', 'eyeBallRotY_scale']
        for LR in self.prefix:
            if 'l_' in LR:
                XYZ = 'y'
            else: XYZ = 'x' 
            self.lidFactorList.append('range_' + LR + "eyeU")
            self.lidFactorList.append('range_' + LR + "eyeD")
            self.lidFactorList.append('range_' + LR + "eyeL")
            self.lidFactorList.append('range_' + LR + "eyeR")
            self.lidFactorList.append(LR + "loBlinkLevel")
            self.lidFactorList.append(LR + "upBlinkLevel")
        self.browFactorList = ['browUp_scale', 'browDown_scale', 'browRotateY_scale']
        self.lipFactorList  = ['swivel_lipJntP_tx', 'swivel_lipJntP_ty', 
                               'swivel_lipJntX_ry', 'swivel_lipJntX_rz', 
                               'swivel_lipJntP_sx', 'swivel_lipJntP_sz', 
                               'swivel_jawSemi_sx', 'swivel_jawSemi_sz', 
                               'UDLR_TX_scale', 'UDLR_TY_scale', 'txSum_lipJntX_tx', 'tySum_lipJntX_ty', 'UDLR_jawCloseTY', 'UDLR_jawCloseTZ', 
                               'tzSum_lipJntX_tz', 'tySum_lipJntX_rx', 'txSum_lipJntX_ry',
                               'jawOpenTX_scale', 'jawOpenTY_scale', 'jawOpen_jawCloseRX', 'jawOpen_jawCloseRY', 
                               'mouth_lipJntX_rx', 'mouth_lipJntY_ry', 'mouth_lipJntY_rz', 
                               'txSum_lipJntY_ry', 'txSum_lipJntY_rz', 'mouth_midCheekRY', 'mouth_midCheekRZ',
                               'mouth_midCheekRX', 'mouth_loCheekRY', 'mouth_loCheekRZ', 'mouth_loCheekRX', 
                               'YZPoc_rollJntT_ty', 'YZPoc_rollJntT_tz']
        self.cheekFactorList = ['midCheek_in', 'loCheek_in']
        
		#- Use this for custom setting
        #- need to read json
        #self.jsonFileName     = jsonFileName
        #self.jsonBasePath     = jsonBasePath
        #self.jsonPath         = os.path.join(jsonBasePath, jsonFileName)
        
        #- create json if not exists
        #if not os.path.exists(self.jsonPath):
        #    with open(self.jsonPath, 'a') as outfile:
        #        json.dump({}, outfile)
        #    outfile.close()
        
        #self.locData = self.updateLocdata(self.jsonPath)
        
        #jsonData = open(self.jsonPath)
        #self.locData = json.load(jsonData)
        #
		
        self.locData = {}
		
        self.faceMainNode = faceMainNode
        self.faceFactors = {'main'    : 'faceFactors',
                            'eyebrow' : 'browFactor',
                            'eyelid'  : 'lidFactor',
                            'lip'     : 'lipFactor',
                            'cheek'   : 'cheekFactor'}
        
        #if self.locData.has_key('setupLoc'):
        #    if self.locData['setupLoc'].has_key('headSkelPos'):
        #        self.headSkelPos = self.locData['setupLoc']['headSkelPos']
        #if self.locData.has_key('headGeo'):
        #    self.headGeo     = self.locData['headGeo'] 
        
    def writeLocInfoData(self, data, jsonPath = ''):
        """
        writing info data json file
        """
        if not jsonPath:
            jsonPath = self.jsonPath
        
        with open(jsonPath, 'w+') as outfile:
            json.dump(data, outfile)
        outfile.close()

    def updateLocdata(self, jsonPath):
        """
        update existing self.locData
        """       
        jsonData = open(jsonPath)
        self.locData = json.load(jsonData)
        
        if self.locData.has_key('setupLoc'):
            if self.locData['setupLoc'].has_key('headSkelPos'):
                self.headSkelPos = self.locData['setupLoc']['headSkelPos']
        if self.locData.has_key('headGeo'):
            self.headGeo     = self.locData['headGeo']
        
        return self.locData
        
    def __repr__(self):
        return "%s.%s(cPrefix=%s, prefix=%s, uplo=%s, ctlSuffix=%s, jntSuffix=%s, grpSuffix=%s, crvSuffix=%s, jntGrp=%s, crvGrp=%s, clsGrp=%s, ctlGrp=%s, jsonPath=%s, panelPath=%s, faceLocPath=%s)" % (
            self.__module__,
            self.__class__.__name__,
            `self.cPrefix`,
            `self.prefix`,            
            `self.uploPrefix`,
            `self.ctlSuffix`,
            `self.jntSuffix`,
            `self.grpSuffix`,
            `self.crvSuffix`,
            `self.jntGrp`,
            `self.crvGrp`,
            `self.clsGrp`,
            `self.ctlGrp`,
            `self.jsonPath`,
            `self.panelPath`,
            `self.faceLocPath`
        )