
def isInsideVolume(volume, point):
    s = volume.shape
    if point[0] < s[0] and point[1] < s[1] and point[2] < s[2] and point[0] >= 0 and point[1] >= 0 and point[2] >= 0:
        return True
    else:
        return False


def at(volume, point):
    return volume[point[0],point[1],point[2]]

