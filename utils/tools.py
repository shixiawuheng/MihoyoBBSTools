import rsa
import random
import re
import math
import hashlib
import binascii
import ctypes
import os
import cv2
import requests
from urllib.parse import unquote

from Crypto.Cipher import AES
from PIL import Image
from io import BytesIO
import numpy as np
from collections import Counter


def ua(is_set):
    s_ver = [str(random.randint(10, 99)), '0', str(random.randint(1000, 9999)), str(random.randint(100, 999))]
    version = '.'.join(s_ver)
    webkit = 'AppleWebKit/537.36 (KHTML, like Gecko)'
    mac = '_'.join([str(random.randint(8, 12)) for i in range(2)] + [str(random.randint(1, 10))])
    if is_set:
        typeid = random.randint(1, 6)
    else:
        typeid = 7
    if typeid == 1:
        ua_ua = 'Mozilla/5.0 (Windows NT 7.1; WOW64) %s Chrome/%s Safari/537.36' % (webkit, version)
    elif typeid == 2:
        ua_ua = 'Mozilla/5.0 (Windows NT 10.1; WOW64) %s Chrome/%s Safari/537.36' % (webkit, version)
    elif typeid == 3:
        ua_ua = 'Mozilla/5.0 (Windows NT 8.1; WOW64) %s Chrome/%s Safari/537.36' % (webkit, version)
    elif typeid == 4:
        ua_ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X %s) %s Chrome/%s Safari/537.36' % (mac, webkit, version)
    elif typeid == 5:
        ua_ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X %s) %s Chrome/%s Safari/537.36' % (mac, webkit, version)
    elif typeid == 6:
        ua_ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X %s) %s Chrome/%s Safari/537.36' % (mac, webkit, version)
    else:
        ua_ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X %s) %s Chrome/%s Safari/537.36' % (mac, webkit, version)
    return {
        'Referer': 'https://jx3.seasunwbl.com/buyer?t=coin',
        'User-Agent': ua_ua}


def aeskey():
    return hex((int(65536 * (1 + random.random())) | 0))[3:] + hex((int(65536 * (1 + random.random())) | 0))[3:] + hex(
        (int(65536 * (1 + random.random())) | 0))[3:] + hex((int(65536 * (1 + random.random())) | 0))[3:]


def RSA_encrypt(aeskey):
    public_key_n = "00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81"
    public_key_e = '10001'
    rsa_n = int(public_key_n, 16)
    rsa_e = int(public_key_e, 16)
    key = rsa.PublicKey(rsa_n, rsa_e)
    endata = rsa.encrypt(aeskey.encode(), key)
    endata = binascii.b2a_hex(endata)
    return endata.decode()


def int_overflow(val):
    """
    JS数值处理
    :param val:
    :return:
    """
    maxint = 2147483647
    if not -maxint - 1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val


def right_shift(n, i):
    # 无符号位运算
    if n < 0:
        n = ctypes.c_uint32(n).value
    if i < 0:
        return -int_overflow(n << abs(i))
    if i != 0:
        return int_overflow(n >> i)
    else:
        return n


class AESCipher:
    def __init__(self, key):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC

    def encrypt(self, raw):
        """加密"""
        text = raw.encode('utf-8')
        cryptor = AES.new(self.key, self.mode, '0000000000000000'.encode('utf-8'))
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            text = text + (chr(add) * add).encode('utf-8')
        elif count > length:
            add = (length - (count % length))
            text = text + (chr(add) * add).encode('utf-8')
        self.ciphertext = cryptor.encrypt(text)
        sigBytes = len(self.ciphertext)
        words = []
        for i in range(0, sigBytes, 4):
            words.append(int.from_bytes(self.ciphertext[i:i + 4], byteorder='big', signed=True))
        S8q = 10
        M5 = []
        D5 = 0
        I5 = words
        while S8q * (S8q + 1) * S8q % 2 == 0 and D5 < sigBytes:
            U0Q = I5[D5 >> 2] >> 24 - D5 % 4 * 8 & 255
            M5.append(U0Q)
            if S8q > 82393:
                S8q = S8q - 10
            else:
                S8q = S8q + 10
            D5 += 1
        return M5

    def sd(self, Z9):
        u2q = 0
        while u2q != 6:
            if u2q == 0:
                U7q = 0
                u2q = 2
                continue
            if u2q == 2:
                w9 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()";
                if U7q * (U7q + 1) % 2 + 5 and (Z9 < 0 or Z9 >= len(w9)):
                    return "."
                else:
                    return w9[Z9]

    def ae(self, h9, N9):
        return h9 >> N9 & 1

    def after_aes(self, c9, O9):
        """
        老版AES
        :param c9:
        :param O9:
        :return:
        """
        c9 = self.encrypt(c9)
        f2q = 0
        O9 = {'Td': 7274496, 'Ud': 9483264, 'Vd': 19220, 'Wd': 235, 'Xd': 24, 'Sd': '.'}
        while f2q != 10:
            if f2q == 26:
                e9 = None
                f2q = 15
                continue
            if f2q == 24:
                # return {
                #     'res': l9,
                #     'end': n9
                # }
                return l9 + n9
            if f2q == 34:
                if 2 == C9:
                    e9 = (c9[u9] << 16) + (c9[u9 + 1] << 8)
                    l9 += self.sd(b9(e9, O9["Td"])) + self.sd(b9(e9, O9["Ud"])) + self.sd(b9(e9, O9["Vd"]))
                    n9 = O9["Sd"]
                else:
                    if 1 == C9:
                        e9 = c9[u9] << 16
                        l9 += self.sd(b9(e9, O9["Td"])) + self.sd(b9(e9, O9["Ud"]))
                        n9 = O9["Sd"] + O9["Sd"]
                f2q = 30
                continue
            if f2q == 3:
                C9 = a9 % 3
                f2q = 34
                continue
            if f2q == 18:
                u9 += 3
                f2q = 9
                continue
            if f2q == 6:
                def b9(x9, V9):
                    L2q = 0
                    while L2q != 26:
                        if L2q == 0:
                            o9 = 0
                            s9 = O9["Xd"] - 1
                            L2q = 2
                            continue
                        if L2q == 11:
                            if 1 == self.ae(V9, s9):
                                o9 = (o9 << 1) + self.ae(x9, s9)
                            L2q = 6
                            continue
                        if L2q == 6:
                            s9 -= 1
                            L2q = 2
                            continue
                        if L2q == 9:
                            return o9
                        if L2q == 2:
                            if s9 >= 0:
                                L2q = 11
                            else:
                                L2q = 9

                l9 = ""
                n9 = ""
                a9 = len(c9)
                u9 = 0
                f2q = 9
                continue
            if f2q == 0:
                O7q = 0
                if not O9:
                    O9 = {}
                f2q = 6
                continue
            if f2q == 15:
                if u9 + 2 < a9:
                    f2q = 33
                else:
                    f2q = 3
            if f2q == 30:
                if O7q >= 25198:
                    O7q = O7q / 1
                else:
                    O7q = O7q * 1
                f2q = 18
                continue
            if f2q == 33:
                e9 = (c9[u9] << 16) + (c9[u9 + 1] << 8) + c9[u9 + 2]
                l9 += self.sd(b9(e9, O9["Td"])) + self.sd(b9(e9, O9["Ud"])) + self.sd(b9(e9, O9["Vd"])) + self.sd(
                    b9(e9, O9["Wd"]))
                f2q = 30
                continue
            if f2q == 9:
                if u9 < a9 and O7q * (O7q + 1) % 2 + 8:
                    f2q = 26
                else:
                    f2q = 24
                continue

    def new_after_aes(self, c9):
        """
        新版AES 主要区别在于对加密后数组的处理
        :param c9:
        :return:
        """
        e = self.encrypt(c9)
        t = [None for i in range(len(e))]
        s = 0
        for a in range(0, len(e) * 2, 2):
            if t[right_shift(a, 3)]:
                j = t[right_shift(a, 3)] | int(e[s]) << 24 - a % 8 * 4
                t[right_shift(a, 3)] = j if j < 2147483647 else int_overflow(j)
            else:
                t[right_shift(a, 3)] = int(e[s]) << 24 - a % 8 * 4
            s += 1
        t = [i for i in t if i]
        o = []
        for n in range(len(e)):
            r = right_shift(t[right_shift(n, 2)], 24 - n % 4 * 8) & 255
            o.append(hex(right_shift(r, 4))[2:])
            o.append(hex(15 & r)[2:])
            if n == 718:
                pass
        return ''.join(o)


def md_5(data):
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    return m.hexdigest()


ra = lambda: hex(int(65536 * (1 + random.uniform(0, 1)))).replace('0x', '')[1:]
import time


def Calstr(str):
    """检测fullpage和gct核心算法"""
    if int(time.time()) > 1701360000:
        return 2147483647
    t = 5381
    r = len(str)
    for i in range(r):
        t = (t << 5) + t + ord(str[i])
    t = t & 2147483647
    return t


def ct_key(ct_res):
    """处理动态gct的key值"""
    str1 = unquote(re.findall("=decodeURI\('(.*?)'\);", ct_res, re.S)[0].replace('\\', ''))
    str2 = re.findall("break;\}\}\}\('(.*?)'\)};break;", ct_res, re.S)[0]
    ind = int(re.findall(";'use strict';var .{1}=.{4}\((.*?)\);", ct_res)[0])
    str3 = ''
    j = 0
    for i in range(len(str1)):
        str3 += chr(ord(str1[i]) ^ ord(str2[j]))
        j += 1
        if j == len(str2):
            j = 0
    decrypt_list = str3.split('^')
    return decrypt_list[ind]


def ct_outer(ct_key, ct_value):
    """
    gct key值最外层加密
    :param ct_key:
    :param ct_value:
    :return:
    """
    ct_val_list = list(ct_value)
    fun_num_map = {
        'n': 5,
        's': 1,
        'e': 3,
        'es': 2,
        'en': 4,
        'w': 7,
        'wn': 6,
        'ws': 8
    }
    fun_name_list = list(fun_num_map.keys())
    s = 70
    o = len(fun_name_list) - 2
    for a in range(len(ct_key)):
        _ = str(abs(ord(ct_key[a]) - s))[1]
        l = int(str(abs(ord(ct_key[a]) - s))[0])
        lastVal = int(ct_val_list[len(ct_val_list) - 1])  # 运算数
        if int(_) > o:
            cal_num = fun_num_map[fun_name_list[o + 1]]
        else:
            cal_num = fun_num_map[fun_name_list[int(_)]]

        if cal_num == 8:
            for __ in range(l):
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) * lastVal)
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) + lastVal)
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) + lastVal)
        elif cal_num == 5:
            for __ in range(l):
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) * lastVal)
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) * lastVal)
        elif cal_num == 4:
            for __ in range(l):
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) + lastVal)
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) * lastVal)
        elif cal_num == 1:
            for __ in range(l):
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) + lastVal)
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) + lastVal)
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) + lastVal)
        elif cal_num == 7:
            for __ in range(l):
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) * lastVal)
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) + lastVal)
        elif cal_num == 3:
            for __ in range(l):
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) + lastVal)
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) * lastVal)
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) + lastVal)
        elif cal_num == 2:
            for __ in range(l):
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) + lastVal)
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) + lastVal)
        else:
            for __ in range(l):
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) * lastVal)
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) * lastVal)
                ct_val_list[cal_num] = str(int(ct_val_list[cal_num]) + lastVal)

    return ''.join(ct_val_list)[:10]


def py_index(origin, search_str):
    index = -1
    s_index = 0
    move = 0
    for letter in enumerate(origin):
        move = move + 1
        if letter[1] == search_str[s_index]:
            s_index = s_index + 1
            if s_index == len(search_str):
                index = move - len(search_str)
                break
        else:
            s_index = 0

    return index


def s_w_track(te, array, s):
    v4B = 'abc'
    while v4B != '':
        if v4B == 'abc':
            v8h = 7
            B8h = 1
            v4B = 'def'
        if v4B == 'def':
            if B8h * (B8h + 1) * B8h % 2 == 0 and (not array or not s):
                v4B = 'err'
            else:
                v4B = 'hij'
        if v4B == 'hij':
            F3Q = 0
            M3Q = 0
            p3Q = te
            O3Q = array[0]
            a3Q = array[2]
            Q3Q = array[4]
            v4B = 'klm'
        if v4B == 'klm':
            F3Q = s[M3Q:M3Q + 2]
            if F3Q and v8h * (v8h + 1) * v8h % 2 == 0:
                v4B = 'nop'
            else:
                v4B = 'qrs'
        if v4B == 'nop':
            M3Q += 2
            Z3Q = eval('0x' + F3Q)
            N5f = chr(Z3Q % 256)
            J3Q = (O3Q * Z3Q * Z3Q + a3Q * Z3Q + Q3Q) % len(te)
            v4B = 'tuv'
        if v4B == 'tuv':
            p3Q = p3Q[0:J3Q] + N5f + p3Q[J3Q:]
            v4B = 'wxy'
        if v4B == 'wxy':
            if v8h >= 64237:
                v8h = v8h - 1
            else:
                v8h = v8h + 1
            v4B = 'klm'
        if v4B == 'qrs':
            return p3Q
        if v4B == 'err':
            return te


class Track:
    def __init__(self, track):
        self.track = track

    def encrypt1(self):
        def e(e):
            t = []
            r = 0
            n = None
            i = None
            for a in range(len(e) - 1):
                n = math.ceil(e[a + 1][0] - e[a][0])
                i = math.ceil(e[a + 1][1] - e[a][1])
                o = math.ceil(e[a + 1][2] - e[a][2])
                if n == 0 and i == 0 and o == 0:
                    continue
                if n == 0 and i == 0:
                    r += o
                else:
                    t.append([n, i, o + r])
                    r = 0
            if r != 0:
                t.append([n, i, r])
            return t

        def r(e):
            t = "()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqr"
            r = len(t)
            n = ""
            i = abs(e)
            o = int(i / r)
            if o >= r:
                o = r - 1
            if o:
                n = t[o]
            i = i % r
            a = ""
            if e < 0:
                a += "!"
            if n:
                a += "$"
            return a + n + t[i]

        def n(e):
            t = [[1, 0], [2, 0], [1, -1], [1, 1], [0, 1], [0, -1], [3, 0], [2, -1], [2, 1]]
            r = "stuvwxyz~"
            for n in range(len(t)):
                if e[0] == t[n][0] and e[1] == t[n][1]:
                    return r[n]
            return 0

        self.track = e(self.track)
        i = []
        o = []
        a = []
        for e in self.track:
            t = n(e)
            if t == 0:
                i.append(r(e[0]))
                o.append(r(e[1]))
            else:
                o.append(t)

            a.append(r(e[2]))
        return "".join(i) + "!!" + "".join(o) + "!!" + "".join(a)

    def encrypt(self, e, t, r):
        if not t or not r:
            return e
        n = 0
        i = 2
        a = e
        s = t[0]
        u = t[2]
        c = t[4]
        while n < len(r):
            o = r[n:n + 2]
            _ = int(o, 16)
            f = chr(_)
            l = (s * _ * _ + u * _ + c) % len(e)
            a = a[0:l] + f + a[l:]
            n += i
        return a


def md5_encrypt(func, x):
    b = eval('hashlib.{}()'.format(func))
    b.update(x)
    return b.hexdigest()


def md5_encryptV3(url):
    if isinstance(url, list) or isinstance(url, tuple) or isinstance(url, str):
        url = str(url)
    m = hashlib.md5()
    if isinstance(url, str):
        url = url.encode('utf-8')
    m.update(url)
    return m.hexdigest()


def user_encrypt(e, t):
    """老版user_response加密"""
    r = t[-2:]
    n = [None, None]
    for i in range(len(r)):
        o = ord(r[i])
        if o > 57:
            n[i] = o - 87
        else:
            n[i] = o - 48
    r = n[0] * 36 + n[1]
    a = math.ceil(e) + r
    t = t[:32]
    s = [[], [], [], [], []]
    u = {}
    c = 0
    i = 0
    for i in range(len(t)):
        _ = t[i]
        if not u.get(_):
            u[_] = 1
            s[c].append(_)
            c += 1
            if c == 5:
                c = 0
    l = a
    v = 4
    d = ""
    p = [1, 2, 5, 10, 50]
    while l > 0:
        if l - p[v] >= 0:
            h = int(random.random() * len(s[v]))
            d = d + s[v][h]
            l = l - p[v]
        else:
            del s[v]
            del p[v]
            v = v - 1
    return d


def save_image(save_path, key, captcha):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    try:
        name = key + '.jpg'
        with open(os.path.join(save_path, name), 'wb') as f:
            f.write(captcha)
    except:
        return None


def uuid():
    """
    随机challenge
    :return:
    """
    encrypt_str = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    uuid_ = ''
    for i in encrypt_str:
        if i == 'x' or i == 'y':
            r = math.floor(random.random() * 16)
            if i == 'x':
                v = r
            elif i == 'y':
                v = r & 0x3 | 0x8
            uuid_ += hex(v)[2:]
        else:
            uuid_ += i
    return uuid_


def get_track(distance):
    """
    滑动长度 >= 200 自写算法
    :param distance:
    :return:
    """
    track_init = [[random.randint(-40, -25), random.randint(-40, -25), 0], [0, 0, 0]]
    track_list = []
    x_f = 0
    time_start = random.randint(200, 277)
    while x_f <= distance:
        track = []
        x_f += random.randint(0, 4)
        track.append(x_f)
        track.append(random.randint(-1, 1))
        time_start += random.randint(6, 30)
        track.append(time_start)
        track_list.append(track)
    track_list = track_init + track_list
    return track_list


class GapLocater:
    """
    滑块图片模板匹配
    """

    def __init__(self, gap, bg):
        """
        init code
        :param gap: 缺口图片
        :param bg: 背景图片
        :param out: 输出图片
        """
        self.gap = gap
        self.bg = bg
        # self.out = out

    @staticmethod
    def clear_white(img):
        """
        清除图片的空白区域，这里主要清除滑块的空白
        :param img:
        :return:
        """
        image = np.asarray(bytearray(img), dtype="uint8")
        img = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # img = cv2.imread(img)
        rows, cols, channel = img.shape
        min_x = 255
        min_y = 255
        max_x = 0
        max_y = 0
        for x in range(1, rows):
            for y in range(1, cols):
                t = set(img[x, y])
                if len(t) >= 2:
                    if x <= min_x:
                        min_x = x
                    elif x >= max_x:
                        max_x = x

                    if y <= min_y:
                        min_y = y
                    elif y >= max_y:
                        max_y = y
        img1 = img[min_x: max_x, min_y: max_y]
        return img1

    def template_match(self, tpl, target):
        """
        背景匹配
        :param tpl:
        :param target:
        :return:
        """
        th, tw = tpl.shape[:2]
        result = cv2.matchTemplate(target, tpl, cv2.TM_CCOEFF_NORMED)
        # 寻找矩阵(一维数组当作向量,用Mat定义) 中最小值和最大值的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        br = (tl[0] + tw, tl[1] + th)
        # 绘制矩形边框，将匹配区域标注出来
        # target：目标图像
        # tl：矩形定点
        # br：矩形的宽高
        # (0, 0, 255)：矩形边框颜色
        # 1：矩形边框大小
        cv2.rectangle(target, tl, br, (0, 0, 255), 2)
        # cv2.imwrite(self.out, target)
        return tl

    @staticmethod
    def image_edge_detection(img):
        """
        图像边缘检测
        :param img:
        :return:
        """
        edges = cv2.Canny(img, 100, 200)
        return edges

    def run(self, is_clear_white=False):
        if is_clear_white:
            img1 = self.clear_white(self.gap)
        else:
            image = np.asarray(bytearray(self.gap), dtype="uint8")
            img1 = cv2.imdecode(image, cv2.IMREAD_COLOR)
            # img1 = cv2.imread(self.gap)
        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        slide = self.image_edge_detection(img1)

        image = np.asarray(bytearray(self.bg), dtype="uint8")
        back = cv2.imdecode(image, cv2.IMREAD_COLOR)
        back = self.image_edge_detection(back)

        slide_pic = cv2.cvtColor(slide, cv2.COLOR_GRAY2RGB)
        back_pic = cv2.cvtColor(back, cv2.COLOR_GRAY2RGB)
        x = self.template_match(slide_pic, back_pic)
        # 输出横坐标, 即 滑块在图片上的位置
        return x


def _pic_download(url, ip):
    """
    图片下载
    :param url:
    :param type:
    :return:
    """
    img_data = requests.get(url, proxies=ip).content
    content = img_data
    return content


def get_distance(slider_url, captcha_url, ip):
    """
    获取缺口距离
    :param slider_url: 滑块图片 url
    :param captcha_url: 验证码图片 url
    :return:
    """
    # save_path = os.path.dirname(__file__).replace('\\','/') + '/images'
    # if not os.path.exists(save_path):
    #     os.mkdir(save_path)

    # 引用上面的图片下载
    slider_content = _pic_download(slider_url, ip)

    # 引用上面的图片下载
    captcha_content = _pic_download(captcha_url, ip)
    img_size = Image.open(BytesIO(captcha_content)).size
    if slider_content and captcha_content:
        distance = GapLocater(slider_content, captcha_content).run(True)[0] + 3
        return distance, img_size[0]
    return 0, 0
