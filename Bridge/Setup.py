import maya.cmds as cmds
import Joints
reload(Joints)

class Setup(Joints.Joints):
    def __init__(self):
        """
        initializing variables
        """
        Joints.Joints.__init__(self)
        
    def createJoints(self):
        """
        creating joints on face locators
        """
        self.createJnts()
        