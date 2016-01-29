from math import *
path=[(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
      (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]


def newKurs():
    """returns (Kurs,Dist) to new destination"""
    start=path[0]
    zwischenziel=path[3]

    diff = (zwischenziel[0]-start[0], zwischenziel[1]-start[1])
    print(diff)

    x,y=diff
    r=sqrt(pow(x,2)+pow(y,2))

    w=atan2(y,x)
    print(r)
    print(degrees(w))

def obstacleNear():
    """Wenn obstacle in range, drive back. remove Obstacle an RoboPos"""
    x=10
    y=20
    range_near=3
    drive_back=False
    walls=[(10, 24), (12, 23), (22, 4), (2, 5)]

    if (12,23) in walls:
        walls.remove((12,23))
        print(walls)

    
    for nearx in range(x-range_near,x+range_near):
        for neary in range(y-range_near,y+range_near):
            if (nearx,neary) in walls:
                drive_back=True
            else:
                drive_back=False
    print("Back: "+str(drive_back))


def KursDiff(SollRichtung,Kompass):
    """Diff zwischen zwei Winkel 0-360grad"""
    if SollRichtung>Kompass:
        if SollRichtung-Kompass>180:
            Winkel=(abs(Kompass-SollRichtung)-360)
        else:
            Winkel=SollRichtung-Kompass
    else:     
        if Kompass-SollRichtung>180:
            Winkel=360-(Kompass-SollRichtung)
        else:
            Winkel=SollRichtung-Kompass
    return(Winkel)



newKurs()
obstacleNear()
w=KursDiff(350,30)
print(w)

