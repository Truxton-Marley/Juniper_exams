import random

from quiz_tools import ask_questions
from quiz_tools import clear_screen_slowly

import jncis_sp_questions

juniper_jncis_sp = [
    jncis_sp_questions.questions_extras,
    jncis_sp_questions.questions_pir,
    jncis_sp_questions.questions_ospf,
    jncis_sp_questions.questions_isis,
    jncis_sp_questions.questions_lacp,
    #jncis_sp_questions.questions_qinq
]

clear_screen_slowly(wait=2)
ask_questions(juniper_jncis_sp[2])
clear_screen_slowly(wait=2)
ask_questions(juniper_jncis_sp[1])
random_index = random.randint(0, len(juniper_jncis_sp) - 1)
ask_questions(juniper_jncis_sp[random_index])
clear_screen_slowly(wait=2)

print("\nThat's it for now. Updates to follow.\n")
