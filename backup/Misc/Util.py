import maya.cmds as cmds

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