import random
import maya.api.OpenMaya as om
import unicodedata

def list_random_sample(src, num):
    return random.sample(src, k=num)


def list_random_shuffle(src):
    ret = list(src)
    return random.shuffle(ret)


def sampleInFace(vPositions, num):
    num = int(num)
    ret = []
    if len(vPositions) == 3:
        ret = samplePointsInTriangle(vPositions[0], vPositions[1], vPositions[2], num)
    elif len(vPositions) == 4:
        if num % 2 == 0:
            sample1 = samplePointsInTriangle(vPositions[0], vPositions[1], vPositions[2], num/2)
            sample2 = samplePointsInTriangle(vPositions[1], vPositions[2], vPositions[3], num/2)
            ret = sample1 + sample2
        else:
            ret = [((vPositions[0][0]+vPositions[2][0])/2.0, (vPositions[0][1]+vPositions[2][1])/2.0, (vPositions[0][2]+vPositions[2][2])/2.0)]
            sample1 = samplePointsInTriangle(vPositions[0], vPositions[1], vPositions[2], int(num/2))
            sample2 = samplePointsInTriangle(vPositions[1], vPositions[2], vPositions[3], int(num/2))
            ret.extend(sample1 + sample2)

    return ret


def samplePointsInTriangle(v0, v1, v2, num):
    # get matrix of transforming from a ((1,0,0), (0,0,0), (0,0,1)) uv triangle to the given triangle
    p0 = om.MFloatPoint(v0[0], v0[1], v0[2])
    p1 = om.MFloatPoint(v1[0], v1[1], v1[2])
    p2 = om.MFloatPoint(v2[0], v2[1], v2[2])
    e1 = p1 - p0
    e2 = p2 - p0
    e3 = (e2 ^ e1).normal()
    M = om.MFloatMatrix([e1.x,e1.y,e1.z,0.0,
                        e3.x,e3.y,e3.z,0.0,
                        e2.x,e2.y,e2.z,0.0,
                        p0.x,p0.y,p0.z,1.0])
    M = M.transpose()
    
    ret = []
    # sample points in uv triangle
    xValues = random.sample([float(k)/1000.0 for k in range(1000)], num)
    zValues = random.sample([float(k)/1000.0 for k in range(1000)], num)
    for i in range(num):
        if xValues[i] + zValues[i] > 1.0:
            xValues[i] = 1.0 - xValues[i]
            zValues[i] = 1.0 - zValues[i]
        randPoint = om.MFloatPoint(xValues[i], 0.0, zValues[i])
        targetPoint = M * randPoint
        ret.append((targetPoint.x, targetPoint.y, targetPoint.z))

    return ret


# get the middle direction between two given directions
def getMiddleDirection(d1, d2):
    v1 = om.MFloatVector(d1[0], d1[1], d1[2]).normal()
    v2 = om.MFloatVector(d2[0], d2[1], d2[2]).normal()
    return [(v1.x+v2.x)/2.0, (v1.y+v2.y)/2.0, (v1.z+v2.z)/2.0]


def unicode2str(unicodeStr):
    return unicodedata.normalize('NFKD', unicodeStr).encode('ascii', 'ignore')