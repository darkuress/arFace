import maya.cmds as cmds

class RangeToolUI(object):
    def __init__(self): 
        #check to see if window exists
        if cmds.window ('RangeToolUI', exists = True):
            cmds.deleteUI('RangeToolUI')
        window = cmds.window( 'RangeToolUI', title = 'Range Tool UI', w =300, h =300) 

        cmds.rowColumnLayout(numberOfColumns = 1)
        cmds.separator( height=20, width = 300, style='in' )
        cmds.setParent('..')
        
        cmds.gridLayout(numberOfColumns=4, cellWidthHeight=(80, 20))
        self.txLabel = cmds.text(label = 'translateX')
        self.txMinFloatField = cmds.floatField()
        self.txMidText = cmds.text(label = ' ----- ', width = 10)
        self.txMaxFloatField = cmds.floatField()
        
        self.tyLabel = cmds.text(label = 'translateY')
        self.tyMinFloatField = cmds.floatField()
        self.tyMidText = cmds.text(label = ' ----- ', width = 10)
        self.tyMaxFloatField = cmds.floatField()

        self.tzLabel = cmds.text(label = 'translateZ')
        self.tzMinFloatField = cmds.floatField()
        self.tzMidText = cmds.text(label = ' ----- ', width = 10)
        self.tzMaxFloatField = cmds.floatField()
                
        self.rxLabel = cmds.text(label = 'rotateX')
        self.rxMinFloatField = cmds.floatField()
        self.rxMidText = cmds.text(label = ' ----- ', width = 10)
        self.rxMaxFloatField = cmds.floatField()
        
        self.ryLabel = cmds.text(label = 'rotateY')
        self.ryMinFloatField = cmds.floatField()
        self.ryMidText = cmds.text(label = ' ----- ', width = 10)
        self.ryMaxFloatField = cmds.floatField()

        self.rzLabel = cmds.text(label = 'rotateZ')
        self.rzMinFloatField = cmds.floatField()
        self.rzMidText = cmds.text(label = ' ----- ', width = 10)
        self.rzMaxFloatField = cmds.floatField()
        
        self.empty1 = cmds.text(label = '')
        self.empty2 = cmds.text(label = '')
        self.empty3 = cmds.text(label = '')
        self.empty4 = cmds.text(label = '')
        
        self.loadButton    = cmds.button(l = 'Load Ctl', c = self.locadCtl)      
        self.conformButton = cmds.button(l = 'Confirm', c = self.ctlSetLimits)        
        
        cmds.setParent('..')
        
        cmds.rowColumnLayout(numberOfColumns = 1)
        cmds.separator( height=20, width = 300, style='in' )
        cmds.setParent('..')
        
        cmds.showWindow()      

    def locadCtl(self, *args):
        """
        """
        ctls = cmds.ls(sl=True, fl =1, type = 'transform')
        
        tx = cmds.transformLimits(ctls[-1], tx = True, q = True)
        ty = cmds.transformLimits(ctls[-1], ty = True, q = True)
        tz = cmds.transformLimits(ctls[-1], tz = True, q = True)
        rx = cmds.transformLimits(ctls[-1], rx = True, q = True)
        ry = cmds.transformLimits(ctls[-1], ry = True, q = True)
        rz = cmds.transformLimits(ctls[-1], rz = True, q = True)
        
        cmds.floatField(self.txMinFloatField, e = True, v = tx[0])
        cmds.floatField(self.txMaxFloatField, e = True, v = tx[1])
        cmds.floatField(self.tyMinFloatField, e = True, v = ty[0])
        cmds.floatField(self.tyMaxFloatField, e = True, v = ty[1])
        cmds.floatField(self.tzMinFloatField, e = True, v = tz[0])
        cmds.floatField(self.tzMaxFloatField, e = True, v = tz[1])
        cmds.floatField(self.rxMinFloatField, e = True, v = rx[0])
        cmds.floatField(self.rxMaxFloatField, e = True, v = rx[1])
        cmds.floatField(self.ryMinFloatField, e = True, v = ry[0])
        cmds.floatField(self.ryMaxFloatField, e = True, v = ry[1])
        cmds.floatField(self.rzMinFloatField, e = True, v = rz[0])
        cmds.floatField(self.rzMaxFloatField, e = True, v = rz[1])
        
    def ctlSetLimits(self, *args):
        """
        """
        ctls = cmds.ls(sl=1, fl =1, type = 'transform')

        posTx = cmds.floatField(self.txMaxFloatField, q = True, v = True)
        negTx = cmds.floatField(self.txMinFloatField, q = True, v = True) 
        posTy = cmds.floatField(self.tyMaxFloatField, q = True, v = True) 
        negTy = cmds.floatField(self.tyMinFloatField, q = True, v = True) 
        posTz = cmds.floatField(self.tzMaxFloatField, q = True, v = True) 
        negTz = cmds.floatField(self.tzMinFloatField, q = True, v = True)
        posRx = cmds.floatField(self.rxMaxFloatField, q = True, v = True) 
        negRx = cmds.floatField(self.rxMinFloatField, q = True, v = True) 
        posRy = cmds.floatField(self.ryMaxFloatField, q = True, v = True) 
        negRy = cmds.floatField(self.ryMinFloatField, q = True, v = True) 
        posRz = cmds.floatField(self.rzMaxFloatField, q = True, v = True) 
        negRz = cmds.floatField(self.rzMinFloatField, q = True, v = True)
        
        for c in ctls:
            #set translate limits 
            if cmds.getAttr(c +'.translateX', lock =1) == False:
                cmds.transformLimits(c, translationX = (negTx, posTx), etx = (1,1)) 
            if cmds.getAttr(c +'.translateY', lock =1) == False:
                cmds.transformLimits(c, translationY = (negTy, posTy), ety =(1,1))
            if cmds.getAttr(c +'.translateZ', lock =1) == False:
                cmds.transformLimits(c, translationZ = (negTz, posTz), etz =(1,1))
            
            #set rotate limits
            if cmds.getAttr(c +'.rotateX', lock =1) == False:
                cmds.transformLimits(c, rotationX = (negRx, posRx), erx =(1,1))
            if cmds.getAttr(c +'.rotateX', lock =1) == False:
                cmds.transformLimits(c, rotationY = (negRy, posRy), ery =(1,1))        
            if cmds.getAttr(c +'.rotateX', lock =1) == False:
                cmds.transformLimits(c, rotationZ = (negRz, posRz), erz =(1,1))