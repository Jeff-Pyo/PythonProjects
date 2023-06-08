def sound_dist(dist, lms):

    sdist = -dist(
            lms.landmark[4].x, 
            lms.landmark[4].y,
            lms.landmark[8].x,
            lms.landmark[8].y
            ) / (dist(
            lms.landmark[2].x,
            lms.landmark[2].y,
            lms.landmark[5].x,
            lms.landmark[5].y) * 2)
    #referenced by https://developeralice.tistory.com/11
    return sdist

def clk_len(dist, lms):

    cdist = dist(
            lms.landmark[8].x,
            lms.landmark[8].y,
            lms.landmark[12].x,
            lms.landmark[12].y)*100
    #검지 손가락 끝과 중지 손가락 끝의 거리를 잼.
    #coded by Junho Pyo

    return cdist

def brightness_dist(dist, lms):

    bdist = int(dist(
            lms.landmark[8].x,
            lms.landmark[8].y,
            lms.landmark[20].x,
            lms.landmark[20].y
            ) / (dist(
            lms.landmark[2].x,
            lms.landmark[2].y,
            lms.landmark[5].x, 
            lms.landmark[5].y) * 2))
    #
    #coded by Donghyeon Lim

    return bdist