### ERRORS
EDUBOK = 0
EDUBCOCONFIGS = 1  # Colocated configurations
EDUBPARAM = 2  # Path parameterisitation error */
EDUBBADRHO = 3  # the rho value is invalid */
EDUBNOPATH = 4  #

import math
from enum import IntEnum

EPSILON = 10e-10


class DubinsPathType(IntEnum):
    L_SEG = 0
    S_SEG = 1
    R_SEG = 2


DIRDATA = [
    [DubinsPathType.L_SEG, DubinsPathType.S_SEG, DubinsPathType.L_SEG],
    [DubinsPathType.L_SEG, DubinsPathType.S_SEG, DubinsPathType.R_SEG],
    [DubinsPathType.R_SEG, DubinsPathType.S_SEG, DubinsPathType.L_SEG],
    [DubinsPathType.R_SEG, DubinsPathType.S_SEG, DubinsPathType.R_SEG],
    [DubinsPathType.R_SEG, DubinsPathType.L_SEG, DubinsPathType.R_SEG],
    [DubinsPathType.L_SEG, DubinsPathType.R_SEG, DubinsPathType.L_SEG],
]


class DubinPathStuffIDKMAN(IntEnum):
    LSL = 0
    LSR = 1
    RSL = 2
    RSR = 3
    RLR = 4
    LRL = 5


class DubinsIntermediateResults:
    def __init__(self):
        self.alpha = 0.0
        self.beta = 0.0
        self.d = 0.0
        self.sa = 0.0
        self.sb = 0.0
        self.ca = 0.0
        self.cb = 0.0
        self.c_ab = 0.0
        self.d_sq = 0.0


class DubinsPath:
    def __init__(self):
        self.qi = [0.0, 0.0, 0.0]
        self.rho = 0.0  # Turning radius
        self.param = [0.0, 0.0, 0.0]
        self.type = DubinsPathType.L_SEG

    def __str__(self) -> str:
        return f"<DubinsPath qi: {self.qi}  rho: {self.rho}  param:{self.param}  type:{self.type}(aka: {DubinPathStuffIDKMAN(self.type).name}) >"


def fmodr(x, y):
    return x - y * math.floor(x / y)


def mod2pi(theta):
    return fmodr(theta, 2 * math.pi)


def dubins_shortest_path(path, q0, q1, rho):
    in_ = DubinsIntermediateResults()
    errcode = dubins_intermediate_results(in_, q0, q1, rho)
    if errcode != EDUBOK:
        return errcode
    # print(path)
    path.qi[0] = q0[0]
    path.qi[1] = q0[1]
    path.qi[2] = q0[2]
    path.rho = rho

    best_cost = float("inf")
    best_word = -1

    for i in range(6):
        pathType = DubinPathStuffIDKMAN(i)  # DubinsPathType(i) # NOTE I changed this
        params = [0.0, 0.0, 0.0]
        errcode = dubins_word(in_, pathType, params)
        if errcode == EDUBOK:
            cost = params[0] + params[1] + params[2]
            if cost < best_cost:
                best_word = i
                best_cost = cost
                path.param[0] = params[0]
                path.param[1] = params[1]
                path.param[2] = params[2]
                path.type = pathType

    if best_word == -1:
        return EDUBNOPATH
    return EDUBOK


def dubins_path(path, q0, q1, rho, pathType):
    in_ = DubinsIntermediateResults()
    errcode = dubins_intermediate_results(in_, q0, q1, rho)
    if errcode == EDUBOK:
        params = [0.0, 0.0, 0.0]
        errcode = dubins_word(in_, pathType, params)
        if errcode == EDUBOK:
            path.param[0] = params[0]
            path.param[1] = params[1]
            path.param[2] = params[2]
            path.qi[0] = q0[0]
            path.qi[1] = q0[1]
            path.qi[2] = q0[2]
            path.rho = rho
            path.type = pathType
    return errcode


def dubins_path_length(path):
    length = 0.0
    length += path.param[0]
    length += path.param[1]
    length += path.param[2]
    length = length * path.rho
    return length


def dubins_segment_length(path, i):
    if i < 0 or i > 2:
        return float("inf")
    return path.param[i] * path.rho


def dubins_segment_length_normalized(path, i):
    if i < 0 or i > 2:
        return float("inf")
    return path.param[i]


def dubins_path_type(path):
    return path.type


def dubins_segment(t, qi, qt, type_):
    st = math.sin(qi[2])
    ct = math.cos(qi[2])
    if type_ == DubinsPathType.L_SEG:
        qt[0] = math.sin(qi[2] + t) - st
        qt[1] = -math.cos(qi[2] + t) + ct
        qt[2] = t
    elif type_ == DubinsPathType.R_SEG:
        qt[0] = -math.sin(qi[2] - t) + st
        qt[1] = math.cos(qi[2] - t) - ct
        qt[2] = -t
    elif type_ == DubinsPathType.S_SEG:
        qt[0] = ct * t
        qt[1] = st * t
        qt[2] = 0.0
    qt[0] += qi[0]
    qt[1] += qi[1]
    qt[2] += qi[2]


def dubins_path_sample(path, t, q):
    tprime = t / path.rho
    qi = [0.0, 0.0, 0.0]
    q1 = [0.0, 0.0, 0.0]
    q2 = [0.0, 0.0, 0.0]
    types = DIRDATA[path.type]

    if t < 0 or t > dubins_path_length(path):
        return EDUBPARAM

    qi[0] = 0.0
    qi[1] = 0.0
    qi[2] = path.qi[2]

    p1 = path.param[0]
    p2 = path.param[1]
    dubins_segment(p1, qi, q1, types[0])
    dubins_segment(p2, q1, q2, types[1])

    if tprime < p1:
        dubins_segment(tprime, qi, q, types[0])
    elif tprime < (p1 + p2):
        dubins_segment(tprime - p1, q1, q, types[1])
    else:
        dubins_segment(tprime - p1 - p2, q2, q, types[2])

    q[0] = q[0] * path.rho + path.qi[0]
    q[1] = q[1] * path.rho + path.qi[1]
    q[2] = mod2pi(q[2])

    return EDUBOK


def dubins_path_sample_many(path, stepSize, cb, user_data):
    retcode = 0
    q = [0.0, 0.0, 0.0]
    x = 0.0
    length = dubins_path_length(path)
    while x < length:
        dubins_path_sample(path, x, q)
        retcode = cb(q, x, user_data)
        if retcode != 0:
            return retcode
        x += stepSize
    return 0


def dubins_path_endpoint(path, q):
    return dubins_path_sample(path, dubins_path_length(path) - EPSILON, q)


def dubins_extract_subpath(path, t, newpath):
    tprime = t / path.rho

    if t < 0 or t > dubins_path_length(path):
        return EDUBPARAM

    newpath.qi[0] = path.qi[0]
    newpath.qi[1] = path.qi[1]
    newpath.qi[2] = path.qi[2]
    newpath.rho = path.rho
    newpath.type = path.type

    newpath.param[0] = min(path.param[0], tprime)
    newpath.param[1] = min(path.param[1], tprime - newpath.param[0])
    newpath.param[2] = min(path.param[2], tprime - newpath.param[0] - newpath.param[1])
    return 0


def dubins_intermediate_results(in_, q0, q1, rho):
    dx = q1[0] - q0[0]
    dy = q1[1] - q0[1]
    D = math.sqrt(dx * dx + dy * dy)
    d = D / rho
    theta = 0

    if d > 0:
        theta = mod2pi(math.atan2(dy, dx))
    alpha = mod2pi(q0[2] - theta)
    beta = mod2pi(q1[2] - theta)

    in_.alpha = alpha
    in_.beta = beta
    in_.d = d
    in_.sa = math.sin(alpha)
    in_.sb = math.sin(beta)
    in_.ca = math.cos(alpha)
    in_.cb = math.cos(beta)
    in_.c_ab = math.cos(alpha - beta)
    in_.d_sq = d * d

    return EDUBOK


def dubins_LSL(in_, out):
    tmp0 = in_.d + in_.sa - in_.sb
    p_sq = 2 + in_.d_sq - (2 * in_.c_ab) + (2 * in_.d * (in_.sa - in_.sb))

    if p_sq >= 0:
        tmp1 = math.atan2((in_.cb - in_.ca), tmp0)
        out[0] = mod2pi(tmp1 - in_.alpha)
        out[1] = math.sqrt(p_sq)
        out[2] = mod2pi(in_.beta - tmp1)
        return EDUBOK
    return EDUBNOPATH


def dubins_RSR(in_, out):
    tmp0 = in_.d - in_.sa + in_.sb
    p_sq = 2 + in_.d_sq - (2 * in_.c_ab) + (2 * in_.d * (in_.sb - in_.sa))
    if p_sq >= 0:
        tmp1 = math.atan2((in_.ca - in_.cb), tmp0)
        out[0] = mod2pi(in_.alpha - tmp1)
        out[1] = math.sqrt(p_sq)
        out[2] = mod2pi(tmp1 - in_.beta)
        return EDUBOK
    return EDUBNOPATH


def dubins_LSR(in_, out):
    p_sq = -2 + (in_.d_sq) + (2 * in_.c_ab) + (2 * in_.d * (in_.sa + in_.sb))
    if p_sq >= 0:
        p = math.sqrt(p_sq)
        tmp0 = math.atan2((-in_.ca - in_.cb), (in_.d + in_.sa + in_.sb)) - math.atan2(
            -2.0, p
        )
        out[0] = mod2pi(tmp0 - in_.alpha)
        out[1] = p
        out[2] = mod2pi(tmp0 - mod2pi(in_.beta))
        return EDUBOK
    return EDUBNOPATH


def dubins_RSL(in_, out):
    p_sq = -2 + in_.d_sq + (2 * in_.c_ab) - (2 * in_.d * (in_.sa + in_.sb))
    if p_sq >= 0:
        p = math.sqrt(p_sq)
        tmp0 = math.atan2((in_.ca + in_.cb), (in_.d - in_.sa - in_.sb)) - math.atan2(
            2.0, p
        )
        out[0] = mod2pi(in_.alpha - tmp0)
        out[1] = p
        out[2] = mod2pi(in_.beta - tmp0)
        return EDUBOK
    return EDUBNOPATH


def dubins_RLR(in_, out):
    tmp0 = (6.0 - in_.d_sq + 2 * in_.c_ab + 2 * in_.d * (in_.sa - in_.sb)) / 8.0
    phi = math.atan2(in_.ca - in_.cb, in_.d - in_.sa + in_.sb)
    if abs(tmp0) <= 1:
        p = mod2pi((2 * math.pi) - math.acos(tmp0))
        t = mod2pi(in_.alpha - phi + mod2pi(p / 2.0))
        out[0] = t
        out[1] = p
        out[2] = mod2pi(in_.alpha - in_.beta - t + mod2pi(p))
        return EDUBOK
    return EDUBNOPATH


def dubins_LRL(in_, out):
    tmp0 = (6.0 - in_.d_sq + 2 * in_.c_ab + 2 * in_.d * (in_.sb - in_.sa)) / 8.0
    phi = math.atan2(in_.ca - in_.cb, in_.d + in_.sa - in_.sb)
    if abs(tmp0) <= 1:
        p = mod2pi(2 * math.pi - math.acos(tmp0))
        t = mod2pi(-in_.alpha - phi + p / 2.0)
        out[0] = t
        out[1] = p
        out[2] = mod2pi(mod2pi(in_.beta) - in_.alpha - t + mod2pi(p))
        return EDUBOK
    return EDUBNOPATH


def dubins_word(in_, pathType, out):
    # print(pathType)
    # print("There might be a bug here...")
    result = 0
    if pathType == DubinPathStuffIDKMAN.LSL:
        result = dubins_LSL(in_, out)
    elif pathType == DubinPathStuffIDKMAN.RSL:
        result = dubins_RSL(in_, out)
    elif pathType == DubinPathStuffIDKMAN.LSR:
        result = dubins_LSR(in_, out)
    elif pathType == DubinPathStuffIDKMAN.RSR:
        result = dubins_RSR(in_, out)
    elif pathType == DubinPathStuffIDKMAN.LRL:
        result = dubins_LRL(in_, out)
    elif pathType == DubinPathStuffIDKMAN.RLR:
        result = dubins_RLR(in_, out)
    else:
        result = EDUBNOPATH
    return result
