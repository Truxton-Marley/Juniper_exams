questions_bgp = [
{
"question" : """
Tables:
    Sanity Check ->
    Adj-RIB-in -> Import Policy -> RIB-local
    RIB-local -> Export Policy -> Adj-RIB-out

Adj-RIB-in: show route receive-protocol bgp <peer_ip>
Adj-RIB-out: show route advertising-protocol bgp <peer_ip>

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Regex:
    {m,n}
    {m}
    {m,}
    *       - Zero or mot
    +       - 1 or more
    ?       - 0 or 1
    |       - match of of two terms on either side of the pipe
    -       - represents a range
---

Match 2-3 repetitions of the term?

""",
"answer" : """{2,3}""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Sample complex RegEx:
    "^56:(2.*)$"

policy-options as-path mypath "42 67 68"

""",
"answer" : "policy-options as-path mypath \"42 67 68\"",
"prompt": "root@vmx1# ",
"clear_screen": False,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
eBGP Load Balancing

# TODO: start 30:00, BGP concepts

eBGP loopback -> eBGP loopback with multihop
LACP

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": False,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
# {
# "question" : """
# BGP Dampening

# Only applies to eBGP

# ---
# pass
# """,
# "answer" : """""",
# "prompt": "root@vmx1# ",
# "clear_screen": False,
# "suppress_positive_affirmation": False,
# "post_task_output": """"""
# },
]

# questions_ = [
# {
# "question" : """
# """,
# "answer" : """""",
# "prompt": "root@vmx1# ",
# "clear_screen": True,
# "suppress_positive_affirmation": False,
# "post_task_output": """"""
# },
# ]

# questions_ = [
# {
# "question" : """
# """,
# "answer" : """""",
# "prompt": "root@vmx1# ",
# "clear_screen": True,
# "suppress_positive_affirmation": False,
# "post_task_output": """"""
# },
# ]

# questions_ = [
# {
# "question" : """
# """,
# "answer" : """""",
# "prompt": "root@vmx1# ",
# "clear_screen": True,
# "suppress_positive_affirmation": False,
# "post_task_output": """"""
# },
# ]

# questions_ = [
# {
# "question" : """
# """,
# "answer" : """""",
# "prompt": "root@vmx1# ",
# "clear_screen": True,
# "suppress_positive_affirmation": False,
# "post_task_output": """"""
# },
# ]