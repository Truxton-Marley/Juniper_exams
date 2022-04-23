import random

from quiz_tools import ask_questions
from quiz_tools import clear_screen_slowly

import jncis_sp_questions

juniper_jncis_sp = [
    jncis_sp_questions.questions_extras,
    jncis_sp_questions.questions_pir,
    jncis_sp_questions.questions_ospf,
    jncis_sp_questions.questions_isis,
    jncis_sp_questions.questions_bgp,
    jncis_sp_questions.questions_bgp_best_path,
    jncis_sp_questions.questions_qinq,
    jncis_sp_questions.questions_stp,
    jncis_sp_questions.questions_mpls,
    jncis_sp_questions.questions_ldp,
    jncis_sp_questions.questions_rsvp,
    jncis_sp_questions.questions_cspf,
    jncis_sp_questions.questions_lacp,
]

clear_screen_slowly(wait=2)
ask_questions(juniper_jncis_sp[11])
clear_screen_slowly(wait=2)
ask_questions(juniper_jncis_sp[10])
clear_screen_slowly(wait=2)
ask_questions(juniper_jncis_sp[9])
for i in range(4):
    clear_screen_slowly(wait=2)
    random_index = random.randint(0, len(juniper_jncis_sp) - 1)
    ask_questions(juniper_jncis_sp[random_index])

clear_screen_slowly(wait=2)
print("\nThat's it for now. Updates to follow.\n")
