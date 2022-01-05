import random
import maya.cmds as cmds
import GeneratorUtil as util

reload(util)

def generateObj(objType, _density, _minScale, _maxScale, _dirOpt, _isNaturalGrw, rockSizeTurb=0, rockShapeTurb=1, customizedDir=[0.0, 1.0, 0.0]):
    slFaces = getFaces()
    if slFaces == [] or slFaces == None:
        return
    
    # create or select the specific group of generation type
    groupName = 'group' + objType
    targetGroup = cmds.ls(groupName, typ='transform')
    if targetGroup == []:
        targetGroup = cmds.group(em=True, name=groupName)
    operatedGrp = cmds.group(em=True, name='history1', parent=groupName)
    
    posList, directions = scatter_position(slFaces, _density)
    # Growing Direction Index: 1-Up, 2-Surface Normal, 3-Customized
    if _dirOpt == 1: # not Surface Normal
        directions = (0.0, 1.0, 0.0)
    elif _dirOpt == 3: # Customized
        directions = tuple(customizedDir)
    
    numPos = len(posList)
    if objType == 'Rock':
        for i in range(numPos):
            generalRad = random.uniform(_minScale, _maxScale)
            singleRock = createRock(generalRad, rockSizeTurb, rockShapeTurb)
            if _dirOpt == 2 and type(directions) == list: # Surface Normal
                dir = directions[i]
            elif type(directions) == tuple:
                dir = directions
            if _isNaturalGrw:
                dir = util.getMiddleDirection((0.0, 1.0, 0.0), dir)
            rotation = cmds.angleBetween(er=True, v1=[0.0,1.0,0.0], v2=dir)
            transformObj(singleRock, posList[i], rotation=rotation)
    else:
        unitObjNames = {'Grass':'grass_unit', 
                        'Bush':'bush_unit',
                        'Tree':'tree_unit',}
        unitObj = cmds.ls(unitObjNames[objType], o=True)
        for i in range(numPos):
            unitScale = random.uniform(_minScale, _maxScale)
            if _dirOpt == 2 and type(directions) == list: # Surface Normal
                dir = directions[i]
            elif type(directions) == tuple:
                dir = directions
            
            if _isNaturalGrw:
                dir = util.getMiddleDirection([0.0, 1.0, 0.0], dir)
            rotation = cmds.angleBetween(er=True, v1=[0.0,1.0,0.0], v2=dir)
            newInstance = instanceObj(unitObj, posList[i], unitScale=unitScale, rotation=rotation)
            cmds.showHidden(newInstance)
            cmds.parent(newInstance, operatedGrp)
    
    cmds.select(slFaces)
    return operatedGrp


def getFaces():
    sel = cmds.ls(sl=True)
    target_faces = cmds.filterExpand(sel, sm=34)
    # print(target_faces)
    if target_faces == [] or target_faces == None:
        cmds.error('No face selected!')
    
    return target_faces


def scatter_position(faces, _density):
    numFaces = len(faces)

    target_positions = []
    target_normals = []
    if numFaces >= _density:
        target_faces = util.list_random_sample(faces, _density)
        for face in target_faces:
            cmds.select(face)
            xRange, yRange, zRange = cmds.polyEvaluate(face, bc=True)
            pos_x = xRange[0]+(xRange[1]-xRange[0])/2.0
            pos_y = yRange[0]+(yRange[1]-yRange[0])/2.0
            pos_z = zRange[0]+(zRange[1]-zRange[0])/2.0
            pos = (pos_x, pos_y, pos_z)        
            target_positions.append(pos)
            fn = getPolyFaceNormal()[0]
            target_normals.append(fn)
    else:
        fAreaList = cmds.polyEvaluate(faces, fa=True)
        totalArea = sum(fAreaList)
        probabilityList = []
        for area in fAreaList:
            probability = area / totalArea
            probabilityList.append(probability)
        for i in range(numFaces):
            sampleNum = int(round(float(_density)*probabilityList[i]))
            face = faces[i]
            cmds.select(face)
            vertices = cmds.filterExpand(cmds.polyListComponentConversion(face, ff=True, tv=True), sm=31)
            vpList = []
            for vertex in vertices:
                vp = tuple(cmds.pointPosition(vertex))
                vpList.append(vp)
            sample_positions = util.sampleInFace(vpList, sampleNum)
            target_positions.extend(sample_positions)
            fn = getPolyFaceNormal()[0]
            target_normals.extend([fn]*sampleNum)
    # print(target_positions)
    cmds.select(faces)
    return target_positions, target_normals


def instanceObj(targetObj, pos, unitScale=1.0, rotation=(0.0, 0.0, 0.0)):
    newObj = cmds.instance(targetObj)
    return transformObj(newObj, pos, unitScale, rotation)


def transformObj(obj, pos, unitScale=1.0, rotation=(0.0, 0.0, 0.0)):
    originalScale = cmds.xform(obj, q=True, ws=True, s=True)
    cmds.move(pos[0], pos[1], pos[2], obj, a=True)
    cmds.rotate(rotation[0], rotation[1], rotation[2], obj)
    cmds.scale(originalScale[0]*unitScale, originalScale[1]*unitScale, originalScale[2]*unitScale, obj)
    return obj


# Get the normal of current selected face(s)
def getPolyFaceNormal():
    faces = cmds.filterExpand(cmds.ls(sl=True), sm=34)
    if faces == [] or faces == None:
        return

    infoList = cmds.polyInfo(fn=True)
    normal_list = []
    for info in infoList:
        infoStr = util.unicode2str(info)
        tokens = infoStr.strip().split(' ')
        numTokens = len(tokens)
        if numTokens > 3 and tokens[0] == 'FACE_NORMAL':
            faceNormal = (float(tokens[numTokens-3]), float(tokens[numTokens-2]), float(tokens[numTokens-1]))
            normal_list.append(faceNormal)
    return normal_list


######### The start of generating rocks ###########
# Note: Part of following code is translated from the Mel script of generating rocks in CGI Tools class
def createSphere(minRad, maxRad):
    radius = random.uniform(minRad, maxRad)
    sphere = cmds.polySphere(name='rockTool1', sx=8, sy=8, r=radius)
    cmds.move(random.uniform(-minRad, minRad), random.uniform(-minRad, minRad), random.uniform(-minRad, minRad), sphere)
    cmds.rotate(random.random()*360, random.random()*360, random.random()*360, sphere, os=True)
    cmds.scale(random.uniform(minRad, maxRad)/radius, random.uniform(minRad, maxRad)/radius, random.uniform(minRad, maxRad)/radius, sphere)
    return sphere


def createRock(generalRad, sizeTurb, shapeTurb):
    sphereList = []
    for i in range(shapeTurb):
        sphere = createSphere(generalRad-sizeTurb, generalRad+sizeTurb)
        sphereList.append(sphere[0])
    cmds.select(sphereList)
    rockNode = cmds.polyCBoolOp(op=1, ch=1, pcr=0, cls=1, name='rock_instance')
    cmds.polyTriangulate(ch=1, name=rockNode[0])
    cmds.polyReduce(p=50, replaceOriginal=True, name=rockNode[0])
    cmds.polySmooth(name=rockNode[0])
    cmds.delete(rockNode[0], ch=True)
######### The end of generating rocks #############
