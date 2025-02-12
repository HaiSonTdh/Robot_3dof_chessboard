from math import *

def Forward_Kinematic(t1,t2,t3,L1,L2,L3):
    t1=(t1/180)*3.14
    t2=(t2/180)*3.14
    t3=(t3/180)*3.14
    c1 = cos(radians(t1))
    s1 = sin(radians(t1))
    c2 = cos(radians(t2))
    s2 = sin(radians(t2))
    c23 = cos(radians(t2+t3))
    s23 = sin(radians(t2+t3))
    # d1=250
    # d3=55
    # L1 = 20
    # L2 = 20
    # L3 = 20
    Px= cos(t1)*(L3*(cos(t2 + t3)) + L2*cos(t2)) 
    Py= sin(t1)*(L3*(cos(t2 + t3)) + L2*cos(t2)) 
    Pz= L1 - L3*(sin(t2 + t3)) - L2*sin(t2)
    Px = round(Px,3)
    Py = round(Py,3)
    Pz = round(Pz,3)
    return Px,Py,Pz

def condition(x,y,z,goc1,goc2,goc3):
    L1 = 156.67
    L2 = 120
    L3 = 145
    # goc1,goc2,goc3 = Inverse_Kinematic_1()
    # Px, Py, Pz, goc1, goc2, goc3,L1,L2,L3 = Inverse_Kinematic_1()
    if x == cos(goc1)*(L3*(cos(goc2 + goc3)) + L2*cos(goc2)) and  y == sin(goc1)*(L3*(cos(goc2 + goc3)) + L2*cos(goc2)) and z == L1 - L3*(sin(goc2 + goc3)) - L2*sin(goc2):
        return goc1,goc2,goc3
    # if condition(Px,Py,Pz,goc1,goc2,goc3):
    #     return goc1,goc2,goc3

def Inverse_Kinematic_1(Px,Py,Pz,L1,L2,L3):
    L1 = 156.67
    L2 = 120
    L3 = 145
    theta1 = 0
    theta2 = 0
    theta3 = 0
    A = sqrt(Px*Px + Py*Py)
    theta1 = atan2(Py/A , Px/A)

    cos_theta3 = (Px*Px + Py*Py + (L1 - Pz)*(L1 - Pz) - L3*L3 - L2*L2) / (2 * L3 * L2)
    # % Đảm bảo cos_theta3 nằm trong khoảng [-1, 1]
    cos_theta3 = max(min(cos_theta3, 1), -1)

    if (1 - cos_theta3*cos_theta3) >= 0 :
        sin_theta3 = -sqrt(1 - cos_theta3*cos_theta3)
    else:
        sin_theta3 = 0

    theta3 = atan2(sin_theta3 , cos_theta3)

    det = L3*L3 + L2*L2 + 2 * L3 * L2 * cos(theta3)
    cos_theta2 = ((L3 * cos(theta3) + L2) * sqrt(Px*Px + Py*Py) + L3 * sin(theta3) * (L1 - Pz)) / det
    sin_theta2 = (-L3 * sin(theta3) * sqrt(Px*Px + Py*Py) + (L3 * cos(theta3) + L2) * (L1 - Pz)) / det
    # % Đảm bảo cos_theta2 nằm trong khoảng [-1, 1]
    cos_theta2 = max(min(cos_theta2, 1), -1)
    theta2 = atan2(sin_theta2 , cos_theta2)

    theta1 = round(theta1,2)
    theta2 = round(theta2,2)
    theta3 = round(theta3,2)
    return theta1,theta2,theta3

def Inverse_Kinematic_2(Px,Py,Pz,L1,L2,L3):
    L1 = 156.67
    L2 = 120
    L3 = 145
    theta1 = 0
    theta2 = 0
    theta3 = 0
    A = sqrt(Px*Px + Py*Py)
    theta1 = atan2(Py/(-A) , Px/(-A))

    cos_theta3 = (Px*Px + Py*Py + (L1 - Pz)*(L1 - Pz) - L3*L3 - L2*L2) / (2 * L3 * L2)
    # % Đảm bảo cos_theta3 nằm trong khoảng [-1, 1]
    cos_theta3 = max(min(cos_theta3, 1), -1)

    if (1 - cos_theta3*cos_theta3) >= 0 :
        sin_theta3 = sqrt(1 - cos_theta3*cos_theta3)
    else:
        sin_theta3 = 0

    theta3 = atan2(sin_theta3 , cos_theta3)

    det = L3*L3 + L2*L2 + 2 * L3 * L2 * cos(theta3)
    cos_theta2 = ((L3 * cos(theta3) + L2) * sqrt(Px*Px + Py*Py) + L3 * sin(theta3) * (L1 - Pz)) / det
    sin_theta2 = (-L3 * sin(theta3) * sqrt(Px*Px + Py*Py) + (L3 * cos(theta3) + L2) * (L1 - Pz)) / det
    # % Đảm bảo cos_theta2 nằm trong khoảng [-1, 1]
    cos_theta2 = max(min(cos_theta2, 1), -1)
    theta2 = atan2(sin_theta2 , cos_theta2)

    theta1 = round(theta1,2)
    theta2 = round(theta2,2)
    theta3 = round(theta3,2)
    return theta1,theta2,theta3

def Inverse_Kinematic_3(Px,Py,Pz,L1,L2,L3):
    L1 = 156.67
    L2 = 120
    L3 = 145
    theta1 = 0
    theta2 = 0
    theta3 = 0
    A = sqrt(Px*Px + Py*Py)
    theta1 = atan2(Py/(-A) , Px/(-A))

    cos_theta3 = (Px*Px + Py*Py + (L1 - Pz)*(L1 - Pz) - L3*L3 - L2*L2) / (2 * L3 * L2)
    # % Đảm bảo cos_theta3 nằm trong khoảng [-1, 1]
    cos_theta3 = max(min(cos_theta3, 1), -1)

    if (1 - cos_theta3*cos_theta3) >= 0 :
        sin_theta3 = -sqrt(1 - cos_theta3*cos_theta3)
    else:
        sin_theta3 = 0

    theta3 = atan2(sin_theta3 , cos_theta3)

    det = L3*L3 + L2*L2 + 2 * L3 * L2 * cos(theta3)
    cos_theta2 = ((L3 * cos(theta3) + L2) * sqrt(Px*Px + Py*Py) + L3 * sin(theta3) * (L1 - Pz)) / det
    sin_theta2 = (-L3 * sin(theta3) * sqrt(Px*Px + Py*Py) + (L3 * cos(theta3) + L2) * (L1 - Pz)) / det
    # % Đảm bảo cos_theta2 nằm trong khoảng [-1, 1]
    cos_theta2 = max(min(cos_theta2, 1), -1)
    theta2 = atan2(sin_theta2 , cos_theta2)

    theta1 = round(theta1,2)
    theta2 = round(theta2,2)
    theta3 = round(theta3,2)
    return theta1,theta2,theta3

def Inverse_Kinematic(Px,Py,Pz,L1,L2,L3):
    L1 = 156.67
    L2 = 120
    L3 = 145
    theta1 = 0
    theta2 = 0
    theta3 = 0
    A = sqrt(Px*Px + Py*Py)
    theta1 = atan2(Py/A , Px/A)

    cos_theta3 = (Px*Px + Py*Py + (L1 - Pz)*(L1 - Pz) - L3*L3 - L2*L2) / (2 * L3 * L2)
    # % Đảm bảo cos_theta3 nằm trong khoảng [-1, 1]
    cos_theta3 = max(min(cos_theta3, 1), -1)

    if (1 - cos_theta3*cos_theta3) >= 0 :
        sin_theta3 = sqrt(1 - cos_theta3*cos_theta3)
    else:
        sin_theta3 = 0

    theta3 = atan2(sin_theta3 , cos_theta3)

    det = L3*L3 + L2*L2 + 2 * L3 * L2 * cos(theta3)
    cos_theta2 = ((L3 * cos(theta3) + L2) * sqrt(Px*Px + Py*Py) + L3 * sin(theta3) * (L1 - Pz)) / det
    sin_theta2 = (-L3 * sin(theta3) * sqrt(Px*Px + Py*Py) + (L3 * cos(theta3) + L2) * (L1 - Pz)) / det
    # % Đảm bảo cos_theta2 nằm trong khoảng [-1, 1]
    cos_theta2 = max(min(cos_theta2, 1), -1)
    theta2 = atan2(sin_theta2 , cos_theta2)

    theta1 = round(theta1,2)
    theta2 = round(theta2,2)
    theta3 = round(theta3,2)
 
    theta_11, theta_12, theta_13 = Inverse_Kinematic_1(Px,Py,Pz,156.67,120,140)
    theta_21, theta_22, theta_23 = Inverse_Kinematic_2(Px,Py,Pz,156.67,120,140)
    theta_31, theta_32, theta_33 = Inverse_Kinematic_3(Px,Py,Pz,156.67,120,140)
    if condition(Px,Py,Pz,theta1,theta2,theta3):
        return theta1,theta2,theta3
    elif condition(Px,Py,Pz,theta_11,theta_12,theta_13):
        return theta1,theta2,theta3
    elif condition(Px,Py,Pz,theta_21,theta_22,theta_23):
        return theta1,theta2,theta3
    elif condition(Px,Py,Pz,theta_31,theta_32,theta_33):
        return theta1,theta2,theta3
    return degrees(theta1),degrees(theta2),degrees(theta3)
    
    
# def Inverse_Kinematic(Px,Py,Pz,L1,L2,L3,theta):
#     d1=250
#     d2=0
#     d3=55
#     L1 = 114
#     L2 = 162
#     L3 = 130
#     #theta=(theta/180)*3.14
#     a1 = sin(radians(theta))
#     print("theta=")
#     print(theta)
#     print("a1=")
#     print(a1)
#     h=(Pz-d1-L3*a1)/L2
#     print("h=") 
#     print(h)
#     if h<0:
#         h=h
#         #print(h)
#     if ((Px<0)&(Py<0)):
#      theta1 = asin(d3/(sqrt(Px*Px+Py*Py)))-acos(Px/sqrt((Px*Px+Py*Py)))
#     else:
    #  theta1 = asin(d3/(sqrt(Px*Px+Py*Py)))-asin(-Py/sqrt((Px*Px+Py*Py)))
    # #theta1 = atan2(Py,Px)
    # theta1 = degrees(theta1)
    # theta2 = asin(h)
    # theta2 = degrees(theta2)
    # theta3 = theta - theta2
    # theta1 = round(theta1,2)
    # theta2 = round(theta2,2)
#     theta3 = round(theta3,2)
#     return theta1,theta2,theta3