def adjust_sound(dist, lms):
    adjust_sound = dist(
                lms.landmark[0].x,
                lms.landmark[0].y,
                lms.landmark[14].x,
                lms.landmark[14].y
            ) < dist(
                lms.landmark[0].x,
                lms.landmark[0].y,
                lms.landmark[16].x,
                lms.landmark[16].y)
    #referenced by https://developeralice.tistory.com/11
    return adjust_sound

def thumb_folded(dist, lms) :

    thumb_folded = dist(
                lms.landmark[4].x,
                lms.landmark[4].y,
                lms.landmark[10].x,
                lms.landmark[10].y
            ) < dist(
                lms.landmark[3].x,
                lms.landmark[3].y,
                lms.landmark[10].x,
                lms.landmark[10].y
            )
    #엄지의 끝과 중지의 첫번째 마디와의 거리가 엄지의 첫번째 마디와 중지의 첫번째 마디의 거리보다 짧을 때, 엄지가 접힌 것으로 인식
    #coded by Junho Pyo
    return thumb_folded

def index_folded(dist, lms):
            
    index_folded = dist(
                lms.landmark[8].x,
                lms.landmark[8].y,
                lms.landmark[0].x,
                lms.landmark[0].y
            ) < dist(
                lms.landmark[5].x,
                lms.landmark[5].y,
                lms.landmark[0].x,
                lms.landmark[0].y
            )
    #검지의 끝과 손바닥 아래의 거리가 검지의 0번째 마디와 손바닥 아래의 거리보다 짧을 때, 검지가 접힌 것으로 인식
    #coded by Junho Pyo
    return index_folded

def middle_folded(dist, lms):
            
    middle_folded = dist(
                lms.landmark[12].x,
                lms.landmark[12].y,
                lms.landmark[0].x,
                lms.landmark[0].y
            ) < dist(
                lms.landmark[9].x,
                lms.landmark[9].y,
                lms.landmark[0].x,
                lms.landmark[0].y
            )
    #검지의 접힘 인식과 비슷하다.
    #coded by Junho Pyo
    return middle_folded

def ring_folded(dist, lms):
            
    ring_folded = dist(
                lms.landmark[16].x,
                lms.landmark[16].y,
                lms.landmark[0].x,
                lms.landmark[0].y
            ) < dist(
                lms.landmark[13].x,
                lms.landmark[13].y,
                lms.landmark[0].x,
                lms.landmark[0].y
            )
    #검지의 접힘 인식과 비슷하다.
    #coded by Junho Pyo
    return ring_folded

def pinky_folded(dist, lms):
            
    pinky_folded = dist(
                lms.landmark[20].x,
                lms.landmark[20].y,
                lms.landmark[0].x,
                lms.landmark[0].y
            ) < dist(
                lms.landmark[17].x,
                lms.landmark[17].y,
                lms.landmark[0].x,
                lms.landmark[0].y
            )
    #검지의 접힘 인식과 비슷하다.
    #coded by Junho Pyo
    return pinky_folded