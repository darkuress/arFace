def calDistance(a = [], b = []):
    result = sqrt((a[0]-b[0])*(a[0]-b[0]) + (a[1]-b[1])*(a[1]-b[1]) + (a[2]-b[2])*(a[2]-b[2]))
    return result

def findSkinCluster(sl = ''):
    if cmds.objectType(sl) == 'transform':
        sl = cmds.listRelatives(sl)[0]
    sels = cmds.listConnections(sl)
    for sel in sels:
        if cmds.objectType(sel) == 'skinCluster':
            skinCls = sel
    return skinCls

def copyCrvSkinWeight(src, dst):
    srcSkinCls = findSkinCluster(src)
    dstSkinCls = findSkinCluster(dst)
    allJnts = set(cmds.listConnections(srcSkinCls, type = 'joint'))
    
    dstCvs = cmds.ls(dst + '.cv[*]', fl = True)
    lenCvs = len(dstCvs)
    for i in range(lenCvs):
        transVal = []
        for jnt in allJnts:
             eachTransVal = (str(jnt), cmds.skinPercent(srcSkinCls, src +'.cv[%s][0]' %i, t = jnt , q = True))
             transVal.append(eachTransVal)
        
        cmds.skinPercent(dstSkinCls, dstCvs[i], tv = transVal)         

         
copyCrvSkinWeight('copySkinTest01:extrudedSurface1', 'copySkinTest01:curve66')
