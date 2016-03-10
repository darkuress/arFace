import maya.cmds as cmds
import os
import json

class Core(object):
    """
    core class to define variables
    """
    def __init__(self,
                 cPrefix       = 'c_',
                 prefix        = ['l_', 'r_'],
                 uplo          = ['up', 'lo'],
                 ctlSuffix     = '_ctl',
                 jntSuffix     = '_jnt',
                 grpSuffix     = '_grp',
                 jsonFileName  = 'info.json',
                 jsonBasePath  = '/corp/projects/eng/jhwang/svn/test/facialTest',
                 **kw):
        """
        basic variables
        """

        self.cPrefix          = cPrefix
        self.prefix           = prefix
        self.uplo             = uplo
        self.ctlSuffix        = ctlSuffix
        self.jntSuffix        = jntSuffix
        self.grpSuffix        = grpSuffix

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
    
    def writeLocInfoData(self, data):
        """
        writing info data json file
        """
        
        with open(self.jsonPath, 'w+') as outfile:
            json.dump(data, outfile)
        outfile.close()