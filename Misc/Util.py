import maya.cmds as cmds
import json
import os
import re

class Util(object):
    def __init__(self):
        pass
        
    def mirrorJoints(self, topJoint = '', prefix = ['l_', 'r_']):
        """
        mirroring joint, top node needs to contain 'l_' as prefix
        """

        lPrefix = prefix[0]
        rPrefix = prefix[1]
        
        cmds.select(cl = True)
        cmds.joint(n = 'temp_jnt')
        cmds.select(topJoint, r = True)
        cmds.select('temp_jnt', tgl = True)
        self.toggleSelect(topJoint, 'temp_jnt')
        cmds.parent()
        
        cmds.select(topJoint, r = True)
        cmds.mirrorJoint(mirrorYZ = True, mirrorBehavior  = True, myz = True, searchReplace =  prefix)
        
        rJoint = rPrefix + topJoint.split(lPrefix)[-1]
        cmds.select(topJoint, rJoint)
        cmds.parent(w = True)
        
        cmds.delete('temp_jnt')
        
        return rJoint
        
    def group(self, children = [], parent = ''):
        """
        create parent node and parent children under it
        """
        if not cmds.objExists(parent):
            cmds.createNode('transform', n = parent)
        self.toggleSelect(r = children, tgl = parent)
        cmds.parent()
        
        return parent
        
    def parent(self, children = [], parent = ''):
        """
        parent children to parent
        """
        cmds.select(children, r = True)
        cmds.select(parent, tgl = True)
        cmds.parent()
        
        return parent
        
    def match(self, dest = '', source = ''):
        """
        dest = thing to match
        run orient, point constraint to match tr and orientation
        """
        self.toggleSelect(source, dest)
        orc = cmds.orientConstraint(mo = False, weight = 1)
        self.toggleSelect(source, dest)
        ptc = cmds.pointConstraint(mo = False, weight = 1)
        
        cmds.delete(orc)
        cmds.delete(ptc)
    
    def toggleSelect(self, r = [], tgl = ''):
        """
        toggle select two object
        """
        cmds.select(r, r = True)
        cmds.select(tgl, tgl = True)

    def sortSelected(self, selVerts = []):
        """
        sorting selected object from -x to x
        """
        for x in range(len(selVerts)):
            for i in range(len(selVerts)-1):
                vert1 = cmds.xform(selVerts[i], q = True, t = True, ws = True)
                vert2 = cmds.xform(selVerts[i+1], q = True, t = True, ws = True)
                if vert2[0] < vert1[0]:
                    temp = selVerts[i]
                    selVerts[i] = selVerts[i+1]
                    selVerts[i+1] = temp
        return selVerts
    
    def createPocNode(self, name, crvShape, parameter):
        """
        create Point on Curve node
        """
        pocNode = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = name)
        cmds.connectAttr(crvShape +'.worldSpace',  pocNode + '.inputCurve')   
        cmds.setAttr(pocNode+ '.turnOnPercentage', 1)    
        cmds.setAttr(pocNode + '.parameter', parameter)
        
        return pocNode
    
    @classmethod
    def writeJsonFile(cls, jsonFile, data):
        """
        writing json file
        """
        #- create json if not exists
        if not os.path.exists(jsonFile):
            with open(jsonFile, 'a') as outfile:
                json.dump({}, outfile)
            outfile.close()
        
        with open(jsonFile, 'w+') as outfile:
            json.dump(data, outfile)
        outfile.close()
    
    @classmethod
    def readJsonFile(cls, jsonFile):
        """
        read json file and return data
        """
        jsonData = json.load(open(jsonFile))
        
        return jsonData

    @classmethod
    def findSkinCluster(cls, sl = ''):
        """
        finding skin cluster of sl object
        """
        if cmds.objectType(sl) == 'transform':
            sl = cmds.listRelatives(sl)[0]
        sels = cmds.listConnections(sl)
        for sel in sels:
            if cmds.objectType(sel) == 'skinCluster':
                skinCls = sel
        return skinCls
    
    @classmethod
    def copyCrvSkinWeight(cls, src, dst):
        """
        copy cv weight from surface to curve
        src = surface
        dst = curve
        """
        srcSkinCls = cls.findSkinCluster(src)
        dstSkinCls = cls.findSkinCluster(dst)
        allJnts = set(cmds.listConnections(srcSkinCls, type = 'joint'))
        
        dstCvs = cmds.ls(dst + '.cv[*]', fl = True)
        lenCvs = len(dstCvs)
        for i in range(lenCvs):
            transVal = []
            for jnt in allJnts:
                 eachTransVal = (str(jnt), cmds.skinPercent(srcSkinCls, src +'.cv[%s][0]' %i, t = jnt , q = True))
                 transVal.append(eachTransVal)
            
            cmds.skinPercent(dstSkinCls, dstCvs[i], tv = transVal)

    @classmethod
    def regexMatch(cls, expression = '', source = []):
        """
        doing a regex match for list
        return matching element
        """
        result = []
        for ctl in source:
            regex = re.match(expression, ctl)
            if regex:
                result.append( str(regex.group()) )
        return result