from _taima.gen.screen.Color import Color as c

#------------------------------------------------------------------------------
# PROMPTER ANIMATION
#
# This module holds the keyframe for the animation, at the beginning before
# entering a taskname.

# color definitions
GRAD_7: int = c.W_PURP_7.value 
GRAD_6: int = c.W_PURP_6.value
GRAD_5: int = c.W_PURP_5.value
GRAD_4: int = c.W_PURP_4.value
GRAD_3: int = c.W_PURP_3.value
GRAD_2: int = c.W_PURP_2.value
GRAD_1: int = c.W_PURP_1.value

PROMPTER: tuple = (
(
#frame_0
((">",234),(">",234),(">",234)),
#frame_1
((">",GRAD_7),(">",234),(">",234)),
#frame_2
((">",GRAD_6),(">",GRAD_7),(">",234)),
#frame_3
((">",GRAD_5),(">",GRAD_6),(">",GRAD_7)),
#frame_4
((">",GRAD_4),(">",GRAD_5),(">",GRAD_6)),
#frame_5
((">",GRAD_3),(">",GRAD_4),(">",GRAD_5)),
#frame_6
((">",GRAD_2),(">",GRAD_3),(">",GRAD_4)),
#frame_7
((">",GRAD_1),(">",GRAD_2),(">",GRAD_3)),
#frame_8
((">",GRAD_2),(">",GRAD_1),(">",GRAD_2)),
#frame_9
((">",GRAD_3),(">",GRAD_2),(">",GRAD_1)),
#frame_10
((">",GRAD_4),(">",GRAD_3),(">",GRAD_2)),
#frame_11
((">",GRAD_5),(">",GRAD_4),(">",GRAD_3)),
#frame_12
((">",GRAD_6),(">",GRAD_5),(">",GRAD_4)),
#frame_13
((">",GRAD_7),(">",GRAD_6),(">",GRAD_5)),
#frame_14
((">",234),(">",GRAD_7),(">",GRAD_6)),
#frame_15
((">",234),(">",234),(">",GRAD_7)),
#frame_16
((">",234),(">",234),(">",234))
)
)
