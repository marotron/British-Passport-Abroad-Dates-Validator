# syntax:
#   styled and colored font on colored background:
#     {font color}_{background color}_{style}
#   styled and colored font on original background:
#     {font color}_{style}
#   normal style colored font on original background:
#     {font color}
#   original font on styled and colored background:
#     _{font color}_{style}
#   original font on colored background:  
#     _{font color}
#
# font/background color:
# WHT - white
# BLK - black
# ORG - orange
# YLW - yellow
# RED - red
# GRN - green
# BLU - blue
# PNK - pink
#
# style:
# B - bold
# C - crossed
# U - underline
# L - light
# D - dark
# R - reversed colors

class ctyle:
    RED = '\033[91m'
    GRN = '\033[92m'
    YEL = '\033[93m'
    BLU = '\033[94m'
    PNK = '\033[95m'
    RED_D = '\033[31m'
    GRN_D = '\033[32m'
    YEL_D = '\033[33m'
    BLU_D = '\033[34m'
    PNK_D = '\033[35m'
    _GRN_L = '\x1b[6;30;42m'
    _RED = '\x1b[2;22;41m'
    RED_L = '\x1b[1;31;40'
    GRN_L = '\x1b[1;32;40'
    YEL_L = '\x1b[1;33;40'
    BLU_N = '\x1b[1;34;40'
    PNK_L = '\x1b[1;35;40'
    BLU_L = '\x1b[1;36;40'
    WHT_L = '\x1b[1;37;40'
    END = '\033[0m'
    B = '\033[1m'
    G = '\033[2m'
    I = '\033[3m'
    U = '\033[4m'
    R = '\033[7m'
