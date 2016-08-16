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
                 uplo           = ['up', 'lo'],
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
                 panelFilename  = 'panel.ma',
                 panelTopNode   = 'Panel',
                 faceLocTopNode = 'faceLoc_grp',
                 locFileName    = 'locators.ma',
                 faceFactors    = {},
                 **kw):
        """
        basic variables
        """
        
        #- checking os type in test mode
        if _platform == 'win32':
            jsonBasePath  = os.path.join('F:', os.sep, 'facialTest')
            baseMaPath      = os.path.join('C:', os.sep, 'documents', 'maya', 'maya2015', 'scripts', 'arFace', 'maFiles')

        elif _platform == 'linux2':
            jsonBasePath  = '/corp/projects/eng/jhwang/svn/test/facialTest'
        
        self.cPrefix          = cPrefix
        self.prefix           = prefix
        self.uplo             = uplo
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
        
        #- need to read json
        self.jsonFileName     = jsonFileName
        self.jsonBasePath     = jsonBasePath
        self.jsonPath         = os.path.join(self.jsonBasePath, self.jsonFileName)
        
        #- create json if not exists
        if not os.path.exists(self.jsonPath):
            with open(self.jsonPath, 'a') as outfile:
                json.dump({}, outfile)
            outfile.close()
            
        jsonData = open(self.jsonPath)
        self.locData = json.load(jsonData)
        
        self.faceFactors = {'main'    : 'faceFactors',
                            'eyebrow' : 'browFactor',
                            'eyelid'  : 'lidFactor'}
        
        self.headSkelPos = self.locData['setupLoc']['headSkelPos']
        
    def writeLocInfoData(self, data):
        """
        writing info data json file
        """
        
        with open(self.jsonPath, 'w+') as outfile:
            json.dump(data, outfile)
        outfile.close()

    def __repr__(self):
        return "%s.%s(cPrefix=%s, prefix=%s, uplo=%s, ctlSuffix=%s, jntSuffix=%s, grpSuffix=%s, crvSuffix=%s, jntGrp=%s, crvGrp=%s, clsGrp=%s, ctlGrp=%s, jsonPath=%s, panelPath=%s, faceLocPath=%s)" % (
            self.__module__,
            self.__class__.__name__,
            `self.cPrefix`,
            `self.prefix`,            
            `self.uplo`,
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