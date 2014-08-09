ROTATING_ART = 0 # 00000000

MOVING_ART = 2 # 00000010

FONT_ART = 5 # 00000101

FACADE_ART = 9 # 00001001

STATIC_ART = 1 # 00000001
STATIC_ART_2 = 17 # only in eye candy. # 00010001

# We use number values instead of flags right now because right now additional parsing of flags is no necessary
# (There is no not rotating moving font art, fonts are always 5, facade always 9, etc..)
# flag & 0x0001 = isNotRotating
# flag & 0x0002 = isMoving
# flag & 0x0004 = isFont
# flag & 0x0008 = isFacade
# flag & 0x0010 = ??? # only in eye candy
