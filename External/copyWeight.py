#!/bin/env python
 ###############################################################################
 #
 #  Copying weight by txt file maya python scripts. Copyleft (c) 2013 Jon Hwang
 #
 #    $HeadURL: $
 #    $Revision: $ 2
 #    $Author:  $ Jonghwan Hwang
 #    $Date: $ 2013 - 08 - 13
 #
 ###############################################################################
"""
This script is used to save skin value as a txt file, and import skin value from the txt file. 

usage : 
        
1. Select all the vertex from the skinned mesh first##########
2. This will print out name of joints attached to the skinned mesh
        You can create as many as instances depending on the skinned mesh you have
        
    #instance 1
    run1 = CopyWeightByTxt('weight1.txt')
    run1.joint()
    run1.vertex()
    
    #instance 2
    run2 = CopyWeightByTxt('weight2.txt')
    run2.joint()
    run2.vertex()
    .
    .
    .
            
3. You can detach skin and modify joint location###########

4. Skin back with the joints printed out in before, 
        select all the vertex and run next
        
    run1.paste()
    run2.paste()
    .
    .
    .

"""

import maya.cmds as cmds
import string
import sys
import os
import json


class CopyWeightByTxt(object):
    def __init__(self, home_dir, name_file, name_mesh):
        """
        Initializing txt file name and file path
        """
        # Getting txt file name
        self.name_file = name_file
        self.name_path = os.path.join(home_dir, self.name_file)
        self.name_mesh = name_mesh
        self.name_vertex = cmds.ls(self.name_mesh + '.vtx[*]')
                
    def joint(self):
        """
        Getting vertax info and saves weights into txt file
        """
        
        # Getting selected name of mesh and vertex
        #self.name_mesh = cmds.ls(sl=True)  
        #self.name_vertex = cmds.ls(sl=True)
        #self.name_vertex = cmds.ls(self.name_mesh + '.vtx[*]')
        
        # Getting number and name of vertex 
        try :
            splited_vertex = string.split(self.name_vertex[0], ':')
            self.number_of_vertex = int(splited_vertex[-1][0:-1]) + 1
            self.name_splited_vertex = string.split(self.name_vertex[0], '[')               
    
        # Check if vertex is selected
        except :
            print "please select vertex"
            
        # Getting joint from skinned mesh
        try :
            self.name_skincluster = cmds.skinCluster(self.name_mesh, q=True, dt=True)
            self.name_skincluster = self.name_skincluster[-1][0:-7]
            self.name_joint = cmds.skinCluster(self.name_mesh, q=True, inf=True)
            return self.name_joint                 
    
        # Check if proper mesh is selected
        except :
            print "please select skinned mesh"
        
    def vertex(self):
        """
        Getting vertax info and saves weights into txt file
        """
        
        # Getting skin value from selected vertexes     and write txt file
        weightsData = []
        for vertexIndex in range(self.number_of_vertex):
            transformValue = []
            for joint in self.name_joint:
                tvTemp = cmds.skinPercent(self.name_skincluster,'%s[%s]' 
                                        %(self.name_splited_vertex[0], vertexIndex), 
                                        transform='%s' %joint, query=True 
                                        )
                transformValue.append(tvTemp)
            weightsData.append(transformValue)
        data = {}
        data['joints'] = self.name_joint
        data['weights'] = weightsData
        with open(self.name_path, 'w') as outfile:
            json.dump(data, outfile)
        outfile.close
        print "Finished writing txt file at %s" %self.name_path
    
    def paste(self):        
        """
        Read txt file and paste weight
        """
        
        # Read File
        
        with open(self.name_path) as jsonFile:
            jsonData = json.load(jsonFile)
            
        skinValue = jsonData['weights']
        joints    = jsonData['joints']
        transformValuePaste = ''
        
        # Redefining skincluster to be safe from naming conflict
        self.name_skincluster = cmds.skinCluster(self.name_mesh, q=True, dt=True)
        self.name_skincluster = self.name_skincluster[-1][0:-7]

        # Making array of transform value from txt              
        vertexIndex = 0
        while(vertexIndex < len(skinValue)):
            transformValuePaste = []
            for jointIndex in range(len(joints)):
                skinValueFloat = float(skinValue[vertexIndex][jointIndex])
                jointName = str(joints[jointIndex])
                tvTemp = [jointName, skinValueFloat]
                transformValuePaste.append(tvTemp)
        
            # Assigning skin value to the mesh 
            cmds.skinPercent(self.name_skincluster, '%s[%s]' 
                            %(self.name_splited_vertex[0], vertexIndex), 
                            transformValue = transformValuePaste
                            )
                                            
            vertexIndex = vertexIndex + 1
        print "Finished transferring skin weight from %s" %self.name_path