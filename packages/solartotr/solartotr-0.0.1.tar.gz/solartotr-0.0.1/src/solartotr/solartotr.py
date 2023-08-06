import math
import time


def solar_to_tr(i_dir, b, sharp, ta, posture='standing', f_bes=1, a_sw=0.7, f_svv=1, t_sol=1, hr=6):
    """
    Convert a solar gain on human to radiant temperature.
    Parameters
    ----------
    i_dir : float
        Direct solar beam intensity (W/m2).
    f_bes : float
        Fraction of body surface exposed to sun (0-1).
    b : float
        Solar altitude angle (deg).
    sharp : float
        Solar horizontal angle relative to front of person (deg).
    ta : float
        Ambient temperature (degC).
    posture : str
        standing or seated.
    a_sw : float, default 0.7
        The short-wave absorptivity of the occupant will range widely, depending on the color of the occupant’s skin
        as well as the color and amount of clothing covering the body. A value of 0.7 shall be used unless more
        specific information about the clothing or skin color of the occupants is available.
         Informative Note: Shortwave absorptivity typically ranges from 0.57 to 0.84,
          depending on skin and clothing color. More information is available in Blum (1945).
    f_svv : float,default 1 outdoor
        The sky-vault view fraction ranges between 0 and 1 as shown in Table C-3. It is calculated with Equation C-7
        for windows to one side. This value depends on the dimensions of the window (width w, height h) and the
        distance d between the occupant and the window.
    t_sol : float, default 1 outdoor
        Window system glazing unit plus shade solar transmittance
    hr : float,
        Radiation heat transfer coefficient, default 6
    """
    deg2rad = math.pi / 180
    a_lw = 0.95
    i_th = i_dir * math.sin(b * deg2rad) + 0.2 * i_dir

    if posture == 'standing':
        f_eff = 0.725
    elif posture == 'seated':
        f_eff = 0.696
    else:
        f_eff = None
    f_p = get_fp(b, sharp, posture)
    # erf_solar_f_eff = erf_solar / f_eff
    erf_solar_f_eff = (0.5 * f_svv * (0.2 * i_dir + 0.6 * i_th) + f_p * f_bes * i_dir) * t_sol * (a_sw / a_lw)
    tr_result = erf_solar_f_eff / hr + ta
    return tr_result


def get_fp(b, sharp, posture='standing'):
    b_range = [0, 15, 30, 45, 60, 75, 90]
    sharp_range = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180]
    b_i = find_span(b, b_range)
    sharp_i = find_span(sharp, sharp_range)
    if posture == 'standing':
        fp_table = [
            [0.35, 0.35, 0.314, 0.258, 0.206, 0.144, 0.082],
            [0.342, 0.342, 0.31, 0.252, 0.2, 0.14, 0.082],
            [0.33, 0.33, 0.3, 0.244, 0.19, 0.132, 0.082],
            [0.31, 0.31, 0.275, 0.228, 0.175, 0.124, 0.082],
            [0.283, 0.283, 0.251, 0.208, 0.16, 0.114, 0.082],
            [0.252, 0.252, 0.228, 0.188, 0.15, 0.108, 0.082],
            [0.23, 0.23, 0.214, 0.18, 0.148, 0.108, 0.082],
            [0.242, 0.242, 0.222, 0.18, 0.153, 0.112, 0.082],
            [0.274, 0.274, 0.245, 0.203, 0.165, 0.116, 0.082],
            [0.304, 0.304, 0.27, 0.22, 0.174, 0.121, 0.082],
            [0.328, 0.328, 0.29, 0.234, 0.183, 0.125, 0.082],
            [0.344, 0.344, 0.304, 0.244, 0.19, 0.128, 0.082],
            [0.347, 0.347, 0.308, 0.246, 0.191, 0.128, 0.082]
        ]
    elif posture == 'seated':
        fp_table = [
            [0.29, 0.324, 0.305, 0.303, 0.262, 0.224, 0.177],
            [0.292, 0.328, 0.294, 0.288, 0.268, 0.227, 0.177],
            [0.288, 0.332, 0.298, 0.29, 0.264, 0.222, 0.177],
            [0.274, 0.326, 0.294, 0.289, 0.252, 0.214, 0.177],
            [0.254, 0.308, 0.28, 0.276, 0.241, 0.202, 0.177],
            [0.23, 0.282, 0.262, 0.26, 0.233, 0.193, 0.177],
            [0.216, 0.26, 0.248, 0.244, 0.22, 0.186, 0.177],
            [0.234, 0.258, 0.236, 0.227, 0.208, 0.18, 0.177],
            [0.262, 0.26, 0.224, 0.208, 0.196, 0.176, 0.177],
            [0.28, 0.26, 0.21, 0.192, 0.184, 0.17, 0.177],
            [0.298, 0.256, 0.194, 0.174, 0.168, 0.168, 0.177],
            [0.306, 0.25, 0.18, 0.156, 0.156, 0.166, 0.177],
            [0.3, 0.24, 0.168, 0.152, 0.152, 0.164, 0.177]
        ]
    else:
        fp_table = []
    fp11 = fp_table[sharp_i][b_i]
    fp12 = fp_table[sharp_i][b_i + 1]
    fp21 = fp_table[sharp_i + 1][b_i]
    fp22 = fp_table[sharp_i + 1][b_i + 1]
    sharp1 = sharp_range[sharp_i]
    sharp2 = sharp_range[sharp_i + 1]
    b1 = b_range[b_i]
    b2 = b_range[b_i + 1]

    # Bilinear interpolation
    fp = fp11 * (sharp2 - sharp) * (b2 - b)
    fp += fp21 * (sharp - sharp1) * (b2 - b)
    fp += fp12 * (sharp2 - sharp) * (b - b1)
    fp += fp22 * (sharp - sharp1) * (b - b1)
    fp /= (sharp2 - sharp1) * (b2 - b1)
    return fp


def find_span(x, x_range):
    # for ordered array arr and value x, find the left index of the closed interval that the value falls in.
    for i in range(len(x_range) - 1):
        if x <= x_range[i + 1] & x >= x_range[i]:
            return i
    return -1


def get_i_dir(b, height):
    b_range = [0, 15, 30, 45, 60, 75, 90]
    b_i = find_span(b, b_range)
    i_dir_arr = [210, 390, 620, 740, 810, 860, 890, 910, 920, 925]
    i_dir_item = i_dir_arr[b_i]
    if height > 1800:
        i_dir_item *= 1.21
    elif height > 1500:
        i_dir_item *= 1.18
    elif height > 1200:
        i_dir_item *= 1.15
    elif height > 900:
        i_dir_item *= 1.12
    else:
        i_dir_item = i_dir_item
    return i_dir_item

    return i_dir_item


def get_h(t, latitude, sun_angle):
    """
    get the Solar altitude angle
    :param t: Hour Angle. 地方时(时角)
    :param latitude: Geographic Latitude. 地理纬度，北纬为正，南纬为负
    :param sun_angle: Sun Declination angle. 赤纬角又称太阳赤纬，是地球赤道平面与太阳和地球中心的连线之间的夹角。北纬为正，南纬为负
    :return:
    """
    deg2rad = math.pi / 180
    h = math.asin(math.sin(latitude * deg2rad) * math.sin(sun_angle * deg2rad) + math.cos(latitude * deg2rad) *
                  math.cos(sun_angle * deg2rad) * math.cos(t * deg2rad))
    h = h * 180 / math.pi
    if h < 0:
        return '当前太阳角为负'
    elif h > 90:
        h -= 90
        return h
    else:
        return h


def get_hour_angle():
    localtime = time.localtime(time.time())
    hour = localtime.tm_hour
    min = localtime.tm_min
    hour_angle = hour * 15 + min * 15 / 60
    hour_angle -= 180
    return hour_angle


def get_sun_angle():
    localtime = time.localtime(time.time())
    day_index = localtime.tm_yday
    sun_angle = 23.45 * math.sin(2 * math.pi * (284 + day_index) / 365)
    return int(sun_angle)
