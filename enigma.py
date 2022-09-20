# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I": {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21
    }
}

UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}


def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))

    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)


# Enigma Logics Start

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input


# ETW
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]


# Wheels
# 반사판까지 가기 위해 세개의 바퀴들을 지나가는 과정에서 암호화하는 과정
def pass_wheels(input, reverse=False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    ch1 = ord(input) - ord('A')
    firstletter = WHEELS['I']["wire"][ord(input) - ord('A')]
    secondletter = WHEELS['II']["wire"][ord(firstletter) - ord('A')]
    thirdletter = WHEELS['III']["wire"][ord(secondletter) - ord('A')]
    input = thirdletter
    return input

# Reverse Pass Wheels -> reverse = True
# 반사판을 통과한 후 세개의 바퀴들로 돌아오는 과정을 나타내는 함수
def pass_reverse_wheels(input):
    firstletter = WHEELS['III']["wire"][ord(input) - ord('A')]
    secondletter = WHEELS['II']["wire"][ord(firstletter) - ord('A')]
    thirdletter = WHEELS['I']["wire"][ord(secondletter) - ord('A')]
    input = thirdletter
    return input
# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]


# Wheel Rotation
# 바퀴를 한 칸씩 움직이게 하는 함수
def rotate_wheels():
    # Implement Wheel Rotation Logics
    WHEELS['I']["wire"] = WHEELS['I']["wire"][-1] + WHEELS['I']["wire"][:-1]
    if (WHEELS['I']["wire"][0] == 'X'):        #가장 오른쪽의 바퀴가 한 바퀴를 모두 돌게 되면
        WHEELS['II']["wire"] = WHEELS['II']["wire"][-1] + WHEELS['II']["wire"][:-1] #가운데 바퀴를 한 칸 움직이게 한다.
        if (WHEELS['II']["wire"] == 'S'):      #가운데 바퀴도 한 바퀴를 돌게 되면
            WHEELS['III']["wire"] = WHEELS['II']["wire"][-1] + WHEELS['II']["wire"][:-1] #가장 왼쪽 바퀴도 한 칸 움직이게한다.


# Enigma Exec Start

plaintext = input("Plaintext to Encode: ")
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")

#apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

for ch in plaintext:

    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    #encoded_ch = pass_wheels(encoded_ch, reverse=True)  이 함수는 사용하지 않고 제가 새로 작성한 pass_reverse_wheels에서
    #                                                    위 함수의 기능을 구현
    encoded_ch = pass_reverse_wheels(encoded_ch)    #pass_wheels(encoded_ch, reverse=True) 대신 생성한 함수
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='')