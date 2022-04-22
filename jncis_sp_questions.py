# 1. Extras (Logical Instances)
# 2. advanced routing / Protocol Independent Routing
# 3. ospf
# 4. isis
# 5. qinq
# 6. lacp
# 7. mc-lag
# 8. stp
# 9. mpls 101
# 10. LDP / RSVP
# 11. CSPF
# 12. BGP
# 13. Best Path
# 14. Tunneling
# 15. Chassis HA
# 16. IPv6

questions_extras = [
{
"question" : """
# notes for EVE-NG vMX startup:
# delete chassis auto-image-upgrade
# set chassis fpc 0 lite-mode
# set system syslog user * pfe none

# Did not find this in the Junos documentation, but seems needed
# to get the logical tunnels:
root# show chassis | display set
set chassis fpc 0 pic 0 tunnel-services bandwidth 10g
set chassis fpc 0 number-of-ports 8
set chassis network-services enhanced-ip

https://www.juniper.net/documentation/us/en/software/junos/logical-systems/index.html

Logical-Systems
    -Your answer to maxing out your CPU in the lab
    -Multiple "Routers" on one vMX

# set logical-systems R1
# commit and-quit
> set cli logical-system R1
> clear cli logical-system
----
set logical-system R1
""",
"answer" : """set logical-system R1""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """

Logical-Systems
    -Your answer to maxing out your CPU in the lab
    -Multiple "Routers" on one vMX

# set logical-systems R1
# commit and-quit
> set cli logical-system R1
----
set cli logical-system R1
""",
"answer" : """set cli logical-system R1""",
"prompt": "root@vmx1> ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Set up Logical-Tunnels between Logical-Systems:

set logical-systems R1 interfaces lt-0/0/0 unit 12 encapsulation ethernet 
set logical-systems R1 interfaces lt-0/0/0 unit 12 peer-unit 21
set logical-systems R1 interfaces lt-0/0/0 unit 12 family inet address 10.0.1.10/31
set logical-systems R1 interfaces lt-0/0/0 unit 12 family iso
set logical-systems R2 interfaces lt-0/0/0 unit 21 encapsulation ethernet 
set logical-systems R2 interfaces lt-0/0/0 unit 21 peer-unit 12
set logical-systems R2 interfaces lt-0/0/0 unit 21 family inet address 10.0.1.11/31
set logical-systems R2 interfaces lt-0/0/0 unit 21 family iso

show route logical-system all
---
set logical-systems R1 interfaces lt-0/0/0 unit 12 encapsulation ethernet 
set logical-systems R1 interfaces lt-0/0/0 unit 12 peer-unit 21
""",
"answer" : """set logical-systems R1 interfaces lt-0/0/0 unit 12 encapsulation ethernet
set logical-systems R1 interfaces lt-0/0/0 unit 12 peer-unit 21""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """root> show configuration logical-systems     
R1 {
    interfaces {
        lt-0/0/0 {
            unit 12 {
                encapsulation ethernet;
                peer-unit 21;
                family inet {
                    address 10.0.1.10/31;
                }
                family iso;
            }
        }
    }
}
R2 {
    interfaces {
        lt-0/0/0 {
            unit 21 {
                encapsulation ethernet;
                peer-unit 12;
                family inet {
                    address 10.0.1.11/31;
                }
                family iso;             
            }
        }
    }
}
"""
},
]


questions_pir = [
{
"question" : """
Protocols Independent Routing

Load Balancing:
-Off by default in Junos
-Per Packet vs Per Flow (nowadays only Per Flow, but command still reads Per Packet)

show route forwarding-table destination 1.1.1.1/32
show routing-options
---
set policy-options policy-statement LB term 1 then load-balance per-packet
set routing-options forwarding-table export LB

""",
"answer" : """set policy-options policy-statement LB term 1 then load-balance per-packet
set routing-options forwarding-table export LB""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """policy-options {
    policy-statement LB {
        then {
            load-balance per-packet;
        }
    }
}
routing-options {
    forwarding-table {
        export LB;
    }
}"""
},
{
"question" : """
Protocols Independent Routing

Load Balancing with Static Routes

# Enable Per Flow Load Balancing first.
set routing-options static route 1.1.1.1/32 next-hop [2.2.2.2 3.3.3.3]

Qualified Next-Hop (Floating Static Route)

set routing-options static route 1.1.1.1/32 next-hop 2.2.2.2
set routing-options static route 1.1.1.1/32 quaflied-next-hop 2.2.2.2 preference 6

Default Options:
set routing-options static defaults ?

---
set routing-options static route 1.1.1.1/32 next-hop 2.2.2.2
""",
"answer" : """set routing-options static route 1.1.1.1/32 next-hop 2.2.2.2""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
---
set routing-options static route 1.1.1.1/32 qualified-next-hop 2.2.2.2 preference 6
""",
"answer" : """set routing-options static route 1.1.1.1/32 qualified-next-hop 2.2.2.2 preference 6""",
"prompt": "root@vmx1# ",
"clear_screen": False,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Protocols Independent Routing

Martian Routes:
-Invalid Addresses or Prefixes

show route martians

set routing-options martians 240.0.0.0/4 orlonger allow
---
show route martians
""",
"answer" : """show route martians""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Protocols Independent Routing

Aggregate Routes
    -Create a summary route in the RIB
    -There must be a contributing route in the RIB
    -Used to attract traffic to the router, not to forward traffic
    -Use Discard Flag to avoid sending ICMP Unreachables

set routing-options aggregate route 10.10.0.0/16

# Default is reject, but we can set it discard:
set routing-options aggregate route 10.10.0.0/16 discard

set policy-options policy-statement AGG term 1 from protocol aggregate
set policy-options policy-statement AGG term 1 then accept

set protocols isis export AGG
---
set routing-options aggregate route 10.10.0.0/16 discard
""",
"answer" : """set routing-options aggregate route 10.10.0.0/16 discard""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """192.168.1.0/24     *[Aggregate/130] 00:00:07
                      Reject
#
#
#
root@SP-LAB:R1# run show route 192.168.1.0 detail

inet.0: 10 destinations, 10 routes (9 active, 0 holddown, 1 hidden)
192.168.1.0/24 (1 entry, 1 announced)
        *Aggregate Preference: 130
                Next hop type: Reject, Next hop index: 0
                Address: 0xa1dd428
                Next-hop reference count: 3
                State: <Active Int Ext>
                Age: 1:30
                Validation State: unverified
                Task: Aggregate
                Announcement bits (1): 0-KRT
                AS path: I  (LocalAgg)
                Flags:                  Depth: 0        Active
                AS path list:
                AS path: I Refcount: 2
                Contributing Routes (2):
                        192.168.1.1/32 proto Direct
                        192.168.1.3/32 proto Static
"""
},
{
"question" : """
Protocols Independent Routing

Generate Route
    -Create a summary like an aggregate,
    but we control the creation with policy
    -Most common is 0.0.0.0/0
    -Traffic without destination is sent to
    the primary contributing route next-hop!!!

set policy-options policy-statement BGP-GEN term 1 from protocol bgp
set routing-options generate route 0.0.0.0/0 policy BGP-GEN

""",
"answer" : """set policy-options policy-statement BGP-GEN term 1 from protocol bgp
set routing-options generate route 0.0.0.0/0 policy BGP-GEN""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Protocols Independent Routing

Routing-Instances
    -Default Master Routing Instances (inet.0, inet.3, inet6.0, etc)
    -Different Types (virtual-router, virtual-switch, vrf, etc)

set routing-instances foo instance-type virtual-router
set routing-instances foo interface xe-0/0/0:0.231

set routing-instances foo protocols ospf area 0 interface xe-0/0/0:0.231

show configuration routing-instances

show route table foo.inet.0
ping 1.1.1.1 routing-instance foo
----
set routing-instances foo instance-type virtual-router

""",
"answer" : """set routing-instances foo instance-type virtual-router""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Protocols Independent Routing

Sharing Routes and/or Route Leaking options:
    -Physical Connection
    -Rib-Groups
    -Instance Import
    -Logical Tunnel

Rib-Group

set routing-options rib-groups <NAME> import-rib [ <source.inet.0> <dest.inet.0> ]
set routing-options rib-groups foo-to-global import-rib [ foo.inet.0 inet.0> ]

#export-rib would be used in a multicast ennvironment

# Export routes learned from foo via OSPF into the global routing table:
set routing-instances foo protocols ospf rib-group KOTEK-TO-GLOBAL

---
set routing-options rib-groups foo-to-global import-rib [ foo.inet.0 inet.0 ]
set routing-instances foo protocols ospf rib-group foo-to-global
""",
"answer" : """set routing-options rib-groups foo-to-global import-rib [ foo.inet.0 inet.0 ]
set routing-instances foo protocols ospf rib-group foo-to-global""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Protocols Independent Routing

Sharing Routes and/or Route Leaking options:
    -Physical Connection
    -Rib-Groups
    -Instance Import
    -Logical Tunnel

Rib-Group

Copy interface routes from the global routing table into foo.inet.0:

routing-instances {
    foo {
        instance-type virtual-router;
        interface lt-0/0/0.13;
    }
}
routing-options {
    interface-routes {
        rib-group inet COPY-ROUTES;
    }
    rib-groups {
        COPY-ROUTES {
            import-rib [ inet.0 foo.inet.0 ];
        }
    }
}
set routing-instances R1-R3 instance-type virtual-router
set routing-instances R1-R3 interface lt-0/0/0.13

set routing-options rib-groups COPY-ROUTES import-rib inet.0
set routing-options rib-groups COPY-ROUTES import-rib R1-R3.inet.0

# "inet" is automatically added if not given with the command:
set routing-options interface-routes rib-group inet global-ints
---
set routing-options interface-routes rib-group global-ints

""",
"answer" : """set routing-options interface-routes rib-group global-ints""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
}
]


questions_ospf = [
{
"question" : """
OSPF

RP: {internal: 10, external: 150}

Down (Attempt) -> Init -> 2-Way -> ExStart -> ExChange -> Loading -> Full

DR/BDR: non-deterministic
    -Priority, Router-ID
    -Priority: 0-255
    -Router Priority Default: 128
    -Cisco Default Priority: 1

set routing-options router-id 1.1.1.1
set protocols ospf area 0 interface ge-0/0/0.0
set protocols ospf area 0 interface ge-0/0/0.0 priority 130
set protocols ospf area 0 interface ge-0/0/0.0 interface-type p2p

set protocols ospf area 0 interface ge-0/0/0.0 authentication md5 1 key cisco123

set protocols ospf area 0 interface ge-0/0/3.0 passive

set protocols ospf area 2 stub
set protocols ospf area 2 stub no-summaries
set protocols ospf area 2 nssa
set protocols ospf area 2 nssa no-summaries

show opsf neighbor
show ospf interface
show ospf database
----
show ospf database

""",
"answer" : """show ospf database""",
"prompt": "root@vmx1> ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """
    OSPF database, Area 0.0.0.1
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len
Router  *192.168.1.1      192.168.1.1      0x80000004   123  0x22 0x7e38  48
Router   192.168.1.3      192.168.1.3      0x80000004   156  0x22 0x8c9f  36
Network  10.0.1.9         192.168.1.3      0x80000001   156  0x22 0x8957  32
Summary  10.0.1.12        192.168.1.3      0x80000003   899  0x22 0x5e58  28
Summary  10.0.1.16        192.168.1.3      0x80000004  1616  0x22 0x347d  28
Summary  10.0.1.20        192.168.1.3      0x80000003  1622  0x22 0xea0   28
Summary  10.0.1.22        192.168.1.3      0x80000002   647  0x22 0x6a6   28
Summary  192.168.1.2      192.168.1.3      0x80000001   899  0x22 0x9dc4  28
Summary  192.168.1.3      192.168.1.3      0x80000002   436  0x22 0x87d9  28
Summary  192.168.1.4      192.168.1.3      0x80000001  1616  0x22 0x89d6  28
Summary  192.168.1.5      192.168.1.3      0x80000002   385  0x22 0x7de0  28
Summary  192.168.1.6      192.168.1.3      0x80000002   129  0x22 0x7dde  28"""
},
{
"question" : """
OSPF

Down (Attempt) -> Init -> 2-Way -> ExStart -> ExChange -> Loading -> Full

LSAs:
Type 1: Router
Type 2: Network
Type 3: Summary
Type 4: Router-Summary (ASBR)
Type 5: External
Type 7: NSSA
---
show ospf database detail
""",
"answer" : """show ospf database detail""",
"prompt": "root@vmx1> ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """
    OSPF database, Area 0.0.0.1
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len
Router  *192.168.1.1      192.168.1.1      0x80000004   247  0x22 0x7e38  48
  bits 0x0, link count 2
  id 192.168.1.1, data 255.255.255.255, Type Stub (3)
    Topology count: 0, Default metric: 0
  id 10.0.1.9, data 10.0.1.8, Type Transit (2)
    Topology count: 0, Default metric: 1
  Topology default (ID 0)
    Type: Transit, Node ID: 10.0.1.9
      Metric: 1, Bidirectional
Router   192.168.1.3      192.168.1.3      0x80000004   280  0x22 0x8c9f  36
  bits 0x1, link count 1
  id 10.0.1.9, data 10.0.1.9, Type Transit (2)
    Topology count: 0, Default metric: 1
  Topology default (ID 0)
    Type: Transit, Node ID: 10.0.1.9
      Metric: 1, Bidirectional
Network  10.0.1.9         192.168.1.3      0x80000001   280  0x22 0x8957  32
  mask 255.255.255.254
  attached router 192.168.1.3
  attached router 192.168.1.1
  Topology default (ID 0)
    Type: Transit, Node ID: 192.168.1.1
      Metric: 0, Bidirectional
    Type: Transit, Node ID: 192.168.1.3
      Metric: 0, Bidirectional
Summary  10.0.1.12        192.168.1.3      0x80000003  1023  0x22 0x5e58  28
  mask 255.255.255.254
  Topology default (ID 0) -> Metric: 1
Summary  10.0.1.16        192.168.1.3      0x80000004  1740  0x22 0x347d  28
  mask 255.255.255.254
  Topology default (ID 0) -> Metric: 1
Summary  10.0.1.20        192.168.1.3      0x80000004    23  0x22 0xca1   28
  mask 255.255.255.254
  Topology default (ID 0) -> Metric: 1
Summary  10.0.1.22        192.168.1.3      0x80000002   771  0x22 0x6a6   28
  mask 255.255.255.254
  Topology default (ID 0) -> Metric: 2
Summary  192.168.1.2      192.168.1.3      0x80000001  1023  0x22 0x9dc4  28
  mask 255.255.255.255
  Topology default (ID 0) -> Metric: 1
Summary  192.168.1.3      192.168.1.3      0x80000002   560  0x22 0x87d9  28
  mask 255.255.255.255
  Topology default (ID 0) -> Metric: 0
Summary  192.168.1.4      192.168.1.3      0x80000001  1740  0x22 0x89d6  28
  mask 255.255.255.255
  Topology default (ID 0) -> Metric: 1
Summary  192.168.1.5      192.168.1.3      0x80000002   509  0x22 0x7de0  28
  mask 255.255.255.255
  Topology default (ID 0) -> Metric: 1
Summary  192.168.1.6      192.168.1.3      0x80000002   253  0x22 0x7dde  28
  mask 255.255.255.255
  Topology default (ID 0) -> Metric: 2

root@SP-LAB:R1>"""
},
{
"question" : """
OSPF

Redistribution:

set policy-options policy-statement int-to-ospf term 1 from route-filter 10.0.1.2/31 exact
set policy-options policy-statement int-to-ospf term 1 then accept

set protocols ospf export int-to-ospf
---
set protocols ospf export int-to-ospf

""",
"answer" : """set protocols ospf export int-to-ospf""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """

protocols {
    ospf {
        export int-to-ospf;
    }
}
policy-options {
    policy-statement int-to-ospf {
        term 1 {
            from {
                route-filter 10.0.1.2/31 exact;
            }
            then accept;
        }
    }
}

root@SP-LAB:R2> show route

inet.0: 18 destinations, 18 routes (18 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

10.0.1.2/31        *[OSPF/150] 00:00:11, metric 0, tag 0
                    > to 10.0.1.13 via lt-0/0/0.23

###

ASBRSum  192.168.1.1      192.168.1.3      0x80000001    44  0x22 0x99c8  28
    OSPF AS SCOPE link state database
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len
Extern   10.0.1.2         192.168.1.1      0x80000001   100  0x22 0x40fa  36

###

ASBRSum  192.168.1.1      192.168.1.3      0x80000001    79  0x22 0x99c8  28
  mask 0.0.0.0
  Topology default (ID 0) -> Metric: 1
    OSPF AS SCOPE link state database
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len
Extern   10.0.1.2         192.168.1.1      0x80000001   135  0x22 0x40fa  36
  mask 255.255.255.254
  Topology default (ID 0)
    Type: 2, Metric: 0, Fwd addr: 0.0.0.0, Tag: 0.0.0.0

"""
},
{
"question" : """
OSPF

Troubleshooting:

monitor traffic interface lt-0/0/0.31 matching "ip src 1.1.1.1"

set protocols ospf traceoptions file ospf.log
set protocols ospf traceoptions flag error
set protocols ospf traceoptions flag event

show log ospf.log | match "1.1.1.1"
---
show log ospf.log
""",
"answer" : """show log ospf.log""",
"prompt": "root@vmx1> ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """Apr 20 06:02:15.509579 OSPF packet ignored: area mismatch (0.0.0.22) from 10.0.1.12 on intf lt-0/0/0.32 area 0.0.0.2
Apr 20 06:02:15.509596 OSPF rcvd Hello 10.0.1.12 -> 224.0.0.5 (lt-0/0/0.32 IFL 373 area 0.0.0.2)
Apr 20 06:02:15.509608   dead_ivl 40, DR 10.0.1.12, BDR 0.0.0.0
Apr 20 06:02:24.770377 OSPF packet ignored: area mismatch (0.0.0.22) from 10.0.1.12 on intf lt-0/0/0.32 area 0.0.0.2
Apr 20 06:02:24.770416 OSPF rcvd Hello 10.0.1.12 -> 224.0.0.5 (lt-0/0/0.32 IFL 373 area 0.0.0.2)
Apr 20 06:02:24.770429   dead_ivl 40, DR 10.0.1.12, BDR 0.0.0.0
"""
}
]


questions_isis = [
{
"question" : """
IS-IS
    -Distributed Databases
    -Route Preference: 15, 18
    -Integrated IS-IS: IS-IS with IP
    -ES: End System, IS: Intermediate System
    -CLNS: Connectionless-mode Network Service
    -Levels: 0, 1, 2, 3
        1: IS-IS within the same area (Intra-area)
        2: IS-IS between different areas (Inter-area)
        3: AS to AS, external
    -Common to make entire core Level-2
    -TLVs

PDUS:
    -IIH: IS-IS IS-IS Hello
        *Sent to IS-IS MAC address
    -CSNP: Complete Sequence Number PDU (like a DBD in OSPF)
    -PSNP: Partial Sequence Number PDU (a bit like a LSR)
    -LS-PDU (A bit like LSU)

Attach-bit
    -L1/L2 Router sends to L1 neighbors
    -Installs a default route on other L1 routers

NET: Network Entity Title
    49.<Area-ID(16-bits)>.<area-identifier(48-bits)>.00
    49.0001.abab.cdcd.dede.00

___

The Network Entity Title always begins with which number?

""",
"answer" : "49",
"prompt": ">>> ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
TLVs:
    -1:     Area Address
    -2:     Neighbor Metric
    -6:     LAN ID
    -22:    Extended Metric (extended version of 2)
    -128:   IP Prefix Metric
    -130:   External IP Info
    -132:   IP Interface
    -135:   Extended IP Metric (extended version of 128)
    -137:   Hostname

Default maxium metric is 63
    -TLVs: 2 & 128
wide-metrics-only maximum is 2**24
    -TLVs: 22 and 135

TLV with the hostname?

""",
"answer" : "137",
"prompt": ">>> ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """

TLV with the neighbor metric (non-extended)?
""",
"answer" : "2",
"prompt": ">>> ",
"clear_screen": False,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """

TLV with the area address?
""",
"answer" : "1",
"prompt": ">>> ",
"clear_screen": False,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
TLV with the IP Prefix Metric (non-extended)?
""",
"answer" : "128",
"prompt": ">>> ",
"clear_screen": False,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """

Extended version of TLV 2?
""",
"answer" : "22",
"prompt": ">>> ",
"clear_screen": False,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
DIS
    -No backup
    -Priority (higher wins) 0-127, default of 64
    -Tie break on the MAC/SNPA (Subnetwork Point of Attachment address)
    -Deterministic (preempts)
    -Routers represented as "pseudonode", summarizing the broadcast topology

Default priority for Juniper IS-IS?

""",
"answer" : "64",
"prompt": ">>> ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """

set interfaces lo0 unit 0 family iso address 49.0001.aaaa.bbbb.cccc.00

set interfaces ge-0/0/0 unit 0 family iso
set protocols isis interface ge-0/0/0.0

# Set to level 1 or level 2 only:
set protocols isis level 1 disable
set protocols isis interface ge-0/0/0.0 level 2 disable
set protocols isis interface ge-0/0/0.0 level 1 disable

# Setup authentication for IS-IS
set protocols isis authentication-type <[simple | md5]>
set protocols isis authentication-key 
set protocols isis level 2 authentication-key-chain ISIS


# Create a passive interface
set protocols isis iterface ge-0/0/1.0 passive

# Wide Metrics
set protocols isis wide-metrics-only

show isis adjacency
show isis database
---
set interfaces lo0 unit 0 family iso address 49.0001.aaaa.bbbb.cccc.00
""",
"answer" : """set interfaces lo0 unit 0 family iso address 49.0001.aaaa.bbbb.cccc.00""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
---
Next:
set interfaces ge-0/0/0 unit 0 family iso
set protocols isis interface ge-0/0/0.0

""",
"answer" : """set interfaces ge-0/0/0 unit 0 family iso
set protocols isis interface ge-0/0/0.0""",
"prompt": "root@vmx1# ",
"clear_screen": False,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
]


questions_bgp = [
{
"question" : """
BGP

TCP 179
RP: 170 (vs Cisco AD: 20/200)
States: Idle, Active, Connect, OpenSent, OpenConfirm, Established
Messages: Open, Keepalive, Update, Notification, Refresh

set routing-options autonomous-system 42
set routing-options router-id 24.24.24.24
set protocols bgp group EXTERNAL-PEERS peer-as 65001
set protocols bgp group EXTERNAL-PEERS type external
set protocols bgp group EXTERNAL-PEERS local-as 42
set protocols bgp group EXTERNAL-PEERS neighbor 42.65.42.65

set protocols bgp group INTERNAL-PEERS type internal
set protocols bgp group INTERNAL-PEERS export NHS
set protocols bgp group INTERNAL-PEERS local-address 24.24.24.24
set protocols bgp group INTERNAL-PEERS neighbor 33.33.33.33

---
set routing-options autonomous-system 42

""",
"answer" : """set routing-options autonomous-system 42""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
BGP

set policy-options policy-statement PS-CONN-TO-BGP term 10 from protocol direct
set policy-options policy-statement PS-CONN-TO-BGP term 10 from route-filter 33.33.33.33/32 exact
set policy-options policy-statement PS-CONN-TO-BGP term 10 then accept

set policy-options policy-statement PS-EXT-TO-BGP term nhs from protocol bgp
set policy-options policy-statement PS-EXT-TO-BGP term nhs from route-type external
set policy-options policy-statement PS-EXT-TO-BGP term nhs from prefix-list PL-EXT-TO-BGP
set policy-options policy-statement PS-EXT-TO-BGP term nhs then next-hop self
set policy-options policy-statement PS-EXT-TO-BGP term nhs then accept

set protocols bgp group INTERNAL-PEERS export PS-CONN-TO-BGP
set protocols bgp group INTERNAL-PEERS export PS-EXT-TO-BGP

show route receive-protocol bgp 33.33.33.33
show route advertising-protocol bgp 24.24.24.24

---
show route advertising-protocol bgp 24.24.24.24

""",
"answer" : """show route advertising-protocol bgp 24.24.24.24""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
BGP

show bgp summary
""",
"answer" : """show bgp summary""",
"prompt": "root@vmx1> ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
]

questions_bgp_best_path = [
{
"question" : """
BGP Best Path

1) Local Preference (Highest)
2) AIGP (Accumulated IGP)
3) AS_PATH length
4) Origin (I>E>?)
5) MED (lowest)
6) eBGP > iBGP
7) Best Exit (Lowest IGP Metric)
8) Current Active Router / Lowest RID
9) Shortest Cluster Length
10) Lowest Peer ID

Weight is only for Cisco

----

Criteria that comes after AS_PATH?

""",
"answer" : """origin""",
"prompt": ">>> ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
]


questions_qinq = [
{
"question" : """
L2 Bridging

802.1q Tag: [<TPID 16-bits(0x8100)><Priority 3-bits><CFI 1-bit><VID 12-bits>]

Functions: Learning, Forwarding, Flooding, Filtering, Aging

C-Tag: (0x88A8)
S-Tag: (0x8100)

Bridge Domain - a collection of ports that share the same flooding and
broadcast criteria

Virtual-Switch: Seperate L2 namespace / VLANs, Seperate MAC Tables
    -Interconnect virtual-switches with IRB interfaces (placed in the master routing table, inet.0)
    -Interconnect via a physical cable

MVRP - Multiple VLAN Registration Protocol
---
pass

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Basic Bridge Domain on vMX

set bridge-domains client vlan-id 42

set interfaces ge-0/0/4 unit 0 family bridge interface-mode trunk
set interfaces ge-0/0/4 unit 0 family bridge vlan-id-list 42
set interfaces ge-0/0/5 unit 0 family bridge interface-mode trunk
set interfaces ge-0/0/5 unit 0 family bridge vlan-id-list 42
set interfaces ge-0/0/6 unit 0 family bridge interface-mode access
set interfaces ge-0/0/6 unit 0 family bridge vlan-id-list 42

show bridge mac-table
clear bridge mac-table
show arp interface irb.0

set interfaces irb.0 family inet address 10.10.10.254/24
set bridge-domains client routing-interface irb.0

""",
"answer" : """set interfaces irb.0 family inet address 10.10.10.254/24
set bridge-domains client routing-interface irb.0""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
802.1ad | Q-in-Q | Provider Bridge Network

C-Tag: 202
S-Tag: 300

CE vMX Router:

show bridge domain
show bridge mac-table

set bridge-domains ce-vlan vlan-id 202

set interfaces ge-0/0/0 description "TO PE"
set interfaces ge-0/0/0 unit 0 family bridge interface-mode trunk
set interfaces ge-0/0/0 unit 0 family bridge vlan-id 202

set interfaces ge-0/0/2 description "Client LAN"
set interfaces ge-0/0/2 unit 0 family bridge interface-mode access
set interfaces ge-0/0/2 unit 0 family bridge vlan-id 202
---
set bridge-domains ce-vlan vlan-id 202
set interfaces ge-0/0/0 unit 0 family bridge interface-mode trunk
set interfaces ge-0/0/0 unit 0 family bridge vlan-id 202
""",
"answer" : """set bridge-domains ce-vlan vlan-id 202
set interfaces ge-0/0/0 unit 0 family bridge interface-mode trunk
set interfaces ge-0/0/0 unit 0 family bridge vlan-id 202""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
802.1ad | Q-in-Q | Provider Bridge Network

C-Tag: 202
S-Tag: 300

PEB vMX Router:

set bridge-domains kunde1 vlan-id 300

set interfaces ge-0/0/2 description "TO S-VLAN Bridge"
set interfaces ge-0/0/2 unit 0 family bridge interface-mode trunk
set interfaces ge-0/0/2 unit 0 family bridge vlan-id 300

set interfaces ge-0/0/0 description "To CE Router"
set interfaces ge-0/0/0 unit 0 family bridge interface-mode access
set interfaces ge-0/0/0 unit 0 family bridge vlan-id 300

---

set interfaces ge-0/0/2 unit 0 family bridge interface-mode trunk

""",
"answer" : """set interfaces ge-0/0/2 unit 0 family bridge interface-mode trunk""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
802.1ad | Q-in-Q | Provider Bridge Network

C-Tag: 202
S-Tag: 300

S-VLAN Bridge vMX Router:

set bridge-domains kunde1 vlan-id 300
show bridge domain

set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 flexible-vlan-tagging

set interfaces ge-0/0/0 unit 0 family bridge interface-mode trunk
set interfaces ge-0/0/0 unit 0 family bridge vlan-id 300

---
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 flexible-vlan-tagging
""",
"answer" : """set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 flexible-vlan-tagging""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Limiting C-Tags
802.1ad | Q-in-Q | Provider Bridge Network

C-Tag: 202
S-Tag: 300
Allowed C-Tags: 200-204

Restricting VLANs on the PEB:

set bridge-domains kunde1allowedvlans vlan-id-list 200-204
set bridge-domains kunde1-STAG-VLAN vlan-id 300

set interfaces ge-0/0/2 description "TO S-VLAN Bridge"
set interfaces ge-0/0/2 unit 0 family bridge interface-mode trunk

# NEW / CHANGED
set interfaces ge-0/0/2 encapsulation flexible-ethernet-services
set interfaces ge-0/0/2 flexible-vlan-tagging
delete interfaces ge-0/0/2 unit 0 family bridge vlan-id 300
set interfaces ge-0/0/2 unit 0 vlan-id 300
set interfaces ge-0/0/2 unit 0 family bridge inner-vlan-id-list 200 204

set interfaces ge-0/0/0 description "To CE Router"
set interfaces ge-0/0/0 unit 0 family bridge interface-mode access
set interfaces ge-0/0/0 unit 0 family bridge vlan-id 300
---
pass
""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
C-TAG Normalization
802.1ad | Q-in-Q | Provider Bridge Network

C-Tag: 200-204, normalized to VLAN 200 within the PEB Network
S-Tag: 300

On the PEB:
set bridge-domains kunde1allowedvlans vlan-id none  <---Pop the C-TAG
set bridge-domains kunde1allowedvlans interface ge-0/0/0.200
set bridge-domains kunde1allowedvlans interface ge-0/0/0.201
set bridge-domains kunde1allowedvlans interface ge-0/0/0.202
set bridge-domains kunde1allowedvlans interface ge-0/0/0.203
set bridge-domains kunde1allowedvlans interface ge-0/0/0.204

set interfaces ge-0/0/0 description "To CE Router"
set interfaces ge-0/0/0 encapsulation flexible-ethernet-services
set interfaces ge-0/0/0 flexible-vlan-tagging
delete interfaces ge-0/0/0 unit 0 family bridge interface-mode access
delete interfaces ge-0/0/0 unit 0 family bridge vlan-id 300
set interfaces ge-0/0/0 unit 200 encapsulation vlan-bridge
set interfaces ge-0/0/0 unit 200 vlan-id 200
set interfaces ge-0/0/0 unit 201 encapsulation vlan-bridge
set interfaces ge-0/0/0 unit 201 vlan-id 201
set interfaces ge-0/0/0 unit 202 encapsulation vlan-bridge
set interfaces ge-0/0/0 unit 202 vlan-id 202
set interfaces ge-0/0/0 unit 203 encapsulation vlan-bridge
set interfaces ge-0/0/0 unit 203 vlan-id 203
set interfaces ge-0/0/0 unit 204 encapsulation vlan-bridge
set interfaces ge-0/0/0 unit 204 vlan-id 204


set interfaces ge-0/0/2 description "TO S-VLAN Bridge"
delete interfaces ge-0/0/2 unit 0 family bridge interface-mode trunk
delete interfaces ge-0/0/2 unit 0 family bridge vlan-id 300
set interfaces ge-0/0/2 encapsulation flexible-ethernet-services
set interfaces ge-0/0/2 flexible-vlan-tagging
set interfaces ge-0/0/2 unit 300 encapsulation vlan-bridge
set interfaces ge-0/0/2 unit 300 vlan-tags outer 300 inner 200

set bridge-domains kunde1allowedvlans interface ge-0/0/2.300
---
pass
""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
S-VLAN Translation
802.1ad | Q-in-Q | Provider Bridge Network

SP1 (us):    300
SP2 (them):  396

set interfaces ge-0/0/2 description "To SP2"
set interfaces ge-0/0/2 encapsulation flexible-ethernet-services
set interfaces ge-0/0/2 flexible-vlan-tagging
set interfaces ge-0/0/2 unit 0 family bridge interface-mode trunk
delete interfaces ge-0/0/2 unit 0 family bridge vlan-id 300
set interfaces ge-0/0/2 unit 0 family bridge vlan-id-list 300
set interfaces ge-0/0/2 unit 0 family bridge vlan-translate 396 300

---
set interfaces ge-0/0/2 unit 0 family bridge vlan-translate 396 300
""",
"answer" : """set interfaces ge-0/0/2 unit 0 family bridge vlan-translate 396 300""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
}
]


questions_stp = [
{
"question" : """

BPUs
Root elected by lowest priority

STP 802.1d
 States:
  Disable, Blocking, Listening
  Learning, Forwarding

RSTP 802.1w
 States:
  Discarding, Learning, Forwarding
 Introduces Edge Ports
 Backup Port (Backup Designated Ports)
 Alternate Port (Backup Root Ports)

VSTP
 Juniper Proprietary
 Compatible with PVST+

MSTP
 Standards Based
 Map VLANs to instances
 Regions
 CST (Common Spanning-Tree) - intermix with none MSTP Bridges
---
pass
""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """

Root Protection
 Prevent unwanted Bridges from becoming Root, place port in blocking
Loop Protection
 One way failures, for ports that should never be designated
 Disable port if it stops receiving BPDUs
BPDU Protection
 Shutdown port if it receives BPDUs, for Edge Ports
---
pass

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """

set protocols mstp revision-level 1
set protocols mstp interface xe-0/0/1
set protocols mstp interface xe-0/0/2
set protocols mstp msti 1 vlan 121
set protocols mstp msti 1 bridge-priority 16k
set protocols mstp msti 2 vlan 242
set protocols mstp msti 2 bridge-priority 8k

set bridge-domains client vlan-id-list [ 121 242 ]

show spanning-tree interface
---
set protocols mstp msti 1 vlan 121
set protocols mstp msti 1 bridge-priority 16k

""",
"answer" : """set protocols mstp msti 1 vlan 121
set protocols mstp msti 1 bridge-priority 16k""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
]


questions_mpls = [
{
"question" : """
MPLS

Label (20-bits) | CoS (3-bits) | Stack-bit | TTL (8-bits)

MPLs, LDP, CSPf, SR (SPRING)

inet.3      <--- inet <-> mpls
mpls.0

MPLS (and RSVP) do not allow fragmentation by default

set interfaces ge-0/0/0 unit 0 family mpls
set interfaces ge-0/0/1 unit 0 family mpls
set interfaces lo0 unit 0 family mpls

set protocols mpls interface all
set protocols mpls interface lo0.0

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
MPLS

Labels:
  3: implicit Null (PHP)
  4: explict Null (Retain the label for last hop)

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
MPLS
Static LSP:

# Ingress Router
set protocols mpls static-label-switched-path ToBunny ingress to 4.4.4.4
set protocols mpls static-label-switched-path ToBunny ingress next-hop 10.12.12.2
set protocols mpls static-label-switched-path ToBunny ingress push 1000002

set routing-options static route 6.6.6.6/32 static-lsp-next-hop ToBunny

# Transit Router
set protocols mpls static-label-switched-path ToBunny transit 1000002 swap 1000003
set protocols mpls static-label-switched-path ToBunny transit 1000002 next-hop 10.23.23.3

# PHP Router
set protocols mpls static-label-switched-path ToBunny transit 1000003 pop
set protocols mpls static-label-switched-path ToBunny transit 1000003 next-hop 10.34.34.4

show mpls static-lsp

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
]

questions_ldp = [
{
"question" : """
MPLS LDP

No TE

Hellos: 224.0.0.2, UDP 646 -> TCP 646
Junos only shares Loopback addresses by default!!!
    (egress policies to advertise other addresses)

set protocols ldp interface ge-0/0/0.0
set protocols ldp interface lo0.0

show ldp neighbor
show ldp interface
show ldp session
show ldp database session 4.4.4.4
traceroute mpls ldp 4.4.4.4
---
set protocols ldp interface ge-0/0/0.0
set protocols ldp interface lo0.0

""",
"answer" : """set protocols ldp interface ge-0/0/0.0
set protocols ldp interface lo0.0""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
]

questions_rsvp = [
{
"question" : """
MPLS RSVP

Route Preference: 7 (vs LDP RP of 9)
Uses extensions in the IGP (OSPF / IS-IS)
Can be bound to BFD
Protocol 46

Define ingress and egress routers, RSVP will create a unidirectional path

PATH Object (Ingress -downstream-> Egress)
    RRO: Resource Record Object, list of routers transversed
         Origin reachability is verified by the egress router
         Loop Detection
    Refreshed every 30 seconds, PathTear (ingress to egress)
    ERO: (Explicit Route Object)
         Configure on Ingress Router
         Define path to take
         Strict | Loose
            Loose: go towards an IP address
            Strict: define the next-hop (no choice)
         PATHERR: requirements cannot be satisfied


RESV Object (Egress -upstream-> Ingress)

    ResvTear (egress to ingress)



""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
MPLS RSVP

# Turn off CSPF (if needed)
set protocols mpls no-cspf

set protocols rsvp interface ae0.0
set protocols rsvp interface lo0.0

# Follow the IGP
set protocols mpls label-switched-path MyRSVP1 to 6.6.6.6

# Create an ERO
set protocols mpls path via-PE-55 10.44.55.55 strict
set protocols mpls path via-PE-55 10.55.66.55 loose

# Tie some stuff together :)
set protocols mpls label-switched-path MyRSVP1 primary via-PE-55
set protocols mpls label-switched-path MyRSVP1 bandwidth 100m

# Create an automatic return path; CSPF must be enabled
set mpls label-switched-path MyRSVP1 corouted-bidirectional

# RSVP authentication
set protocols rsvp interface xe-0/0/0.0 authentication-key cisco123

# Ultimate Hop Pop
set mpls label-switched-path MyRSVP1 ultimate-hop-popping

# Enable BFD (be wary of this one in the lab)
set mpls label-switched-path MyRSVP1 oam bfd-liveness-detection minimum-interval 50
set mpls label-switched-path MyRSVP1 oam bfd-liveness-detection multiplier 3
set mpls label-switched-path MyRSVP1 oam bfd-liveness-detection failure-action <[make-before-break | teardown]>

# MTU Path discovery and Fragmentation
set protocols mpls path-mtu allow-fragmentation
set protocols mpls path-mtu rsvp mtu-signaling

# Manually reset all RSVP sessions; good for labs
clear rsvp session all

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
MPLS RSVP

Validation:

show mpls lsp
    ActivePath: ERO
    LSPName: LSP

show rsvp session
show rsvp interface
show mpls lsp ingress name MyRSVP1 extensive

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
]

questions_cspf = [
{
"question" : """
MPLS CSPF

CSPF: define constraints and the IGP creates the EROs

OSPF:  Opaque LSAs (Type-10)
    Within the area, but expandable with extra commands
IS-IS: TLVs
    Within level 1

TED: Traffic Engineering Database
    Bandwidth Reservations
    Admin-Groups
    State Info
    SLA Info

# Turn on Type-10 LSAs
set protocols ospf traffic-engineering

show ted database [extensive]
show ted database 1.1.1.1

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
MPLS CSPF

1.) Prune non-qualifying paths
2.) Calculate SPF based on pruned tree

Tie-Breaking for Equal Cost Paths Options:
    A) Random
    B) Least-Fill (Path with the least reserved BW, based on !!!percent!!!)
    C) Most-Fill (Path with the most reserved BW)

set protocols label-switched-path MyRSVP1 most-fill
set protocols label-switched-path MyRSVP1 least-fill

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
MPLS CSPF

Admin Groups (colors)
    32-bit value
    Each bit has a color / name
    Used to label interfaces

set protocols mpls admin-groups puce 31
set protocols mpls admin-groups or 0
set protocols mpls admin-groups argent 1
set protocols mpls admin-groups <NAME> <0..31>

set protocols mpls label-switched-path MyRSVP1 admin-group ?
    exclude
    include-all
    include-any

set protocols mpls label-switched-path MyRSVP1 admin-group exclude argent
set protocols mpls label-switched-path MyRSVP1 admin-group include-any [ puce or ]

set protocols mpls interface xe-0/0/1.0 admin-group [ puce purple ]

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
MPLS CSPF

Bidirectional LSPs (does not work on vMX)

set protocols mpls label-switched-path MyRSVP1 corouted-bidirectional

# Bidirectional Performance
set protocols mpls statistics traffic-class-statistics
set protocols mpls label-switched-path MyRSVP1 ultimate-hop-popping
set protocols mpls label-switched-path MyRSVP1 associate-lsp MyRSVP1-Return-lsp
set protocols mpls label-switched-path MyRSVP1 oam mpls-tp-mode
set protocols mpls label-switched-path MyRSVP1 oam performance-monitoring querier loss-delay traffic-class tc-0 query-interval 1000

# The other side
set protocols mpls statistics traffic-class-statistics
set protocols mpls label-switched-path MyRSVP1-Return-lsp ultimate-hop-popping
set protocols mpls label-switched-path MyRSVP1-Return-lsp associate-lsp MyRSVP1
set protocols mpls label-switched-path MyRSVP1-Return-lsp oam mpls-tp-mode
set protocols mpls label-switched-path MyRSVP1-Return-lsp oam performance-monitoring responder loss min-query-interval 1000
set protocols mpls label-switched-path MyRSVP1-Return-lsp oam performance-monitoring responder delay min-query-interval 1000

# Verify
show performance-monitoring mpls lsp

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
]


questions_lacp = [
{
"question" : """
LACP | 802.3ad | 802.1ax

803.3ad:    Original Link Aggregation RFC
802.1AX:    Moved LAG here later

Redundancy and Aggregation

Up to 8 uplinks on most platforms

LACP: Active | Passive

set chassis aggregated-devices ethernet device-count 1
    + creates a single "ae" interface, ae0

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """chassis {
    aggregated-devices {
        ethernet {
            device-count 1;
        }
    }
}
"""
},
{
"question" : """
LACP | 802.3ad | 802.1ax

EX-Switch:

set chassis aggregated-devices ethernet device-count 1

Get rid of all "unit" configuration on the physical interfaces, including unit 0

set interfaces xe-0/0/0 gigether-options 803.ad ae0
set interfaces xe-0/0/1 gigether-options 803.ad ae0

set interfaces ae0 aggregated-ether-options lacp active
set interfaces ae0 aggregated-ether-options lacp periodic <[fast | slow]>
    fast    every second
    slow    every 30 seconds

# Set ae0 to be a trunk port:
set interfaces ae0 unit 0 family ethernet-switching port-mode trunk

# Verify
show lacp interfaces

""",
"answer" : """""",
"prompt": "root@vEX# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """Aggregated interface: ae0
    LACP state:       Role   Exp   Def  Dist  Col  Syn  Aggr  Timeout  Activity
      ge-0/0/1       Actor    No    No   Yes  Yes  Yes   Yes     Fast    Active
      ge-0/0/1     Partner    No    No   Yes  Yes  Yes   Yes     Fast    Active
      ge-0/0/4       Actor    No    No   Yes  Yes  Yes   Yes     Fast    Active
      ge-0/0/4     Partner    No    No   Yes  Yes  Yes   Yes     Fast    Active
    LACP protocol:        Receive State  Transmit State          Mux State 
      ge-0/0/1                  Current   Fast periodic Collecting distributing
      ge-0/0/4                  Current   Fast periodic Collecting distributing"""
},
{
"question" : """
LACP | 802.3ad | 802.1ax

QFC-Switch

set chassis aggregated-devices ethernet device-count 1

set interfaces xe-0/0/0 gigether-options 803.ad ae0
set interfaces xe-0/0/1 gigether-options 803.ad ae0

set interfaces ae0 aggregated-ether-options lacp active

# Set ae0 to be a trunk port:
set interfaces ae0 unit 0 family ethernet-switching interface-mode trunk
set interfaces ae0 unit 0 family ethernet-switching vlan members all

# Verify
show lacp interfaces

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
LACP | 802.3ad | 802.1ax

MX-Router

set chassis aggregated-devices ethernet device-count 1

set interfaces ge-0/0/2 ether-options 802.3ad ae0
set interfaces ge-0/0/4 ether-options 802.3ad ae0

set interfaces ae0 aggregated-ethernet-options lacp active

set interface ae0 unit 0 family bridge vlan-id-list 300

show lacp interfaces

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """interfaces {
    ge-0/0/2 {
        gigether-options {              
            802.3ad ae0;
        }
    }
    ge-0/0/4 {
        gigether-options {
            802.3ad ae0;
        }
    }
    ae0 {
        aggregated-ether-options {
            lacp {
                active;
            }
        }
        unit 0 {
            family bridge {
                interface-mode trunk;
                vlan-id-list 300;
            }
        }
    }"""
},
{
"question" : """
LACP | 802.3ad | 802.1ax

Cisco-Router

interface range GigabitEthernet 0/3-4
 channel-group 1 mode active
 lacp rate fast
!
interface Port1
 switchport mode trunk
!

""",
"answer" : """""",
"prompt": "mycisco-rtr(config)# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
]

questions_mc_lag = [
{
"question" : """
MC-LAG

Just look like LAG to client.

ICL - Inter-Chassis Link

State Modes:
    -Active-Standby
    -Active-Active

Client:
set chassis aggregated-devices ethernet device-count 1
set interfaces xe-0/0/0 ether-options 802.3ad ae0
set interfaces xe-0/0/1 ether-options 802.3ad ae0
set interfaces ae0 aggregated-ether-options lacp active
set interfaces ae0 unit 0 family bridge interface-mode trunk
set interfaces ae0 unit 0 family bridge vlan-id-list 42
set bridge-domains MYBRIDGEVLANS vlan-id 42


""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
MC-LAG

Just look like LAG to client.

ICL - Inter-Chassis Link

State Modes:
    -Active-Standby
    -Active-Active

ICL:
set bridge-domains MGMT vlan-id 11
set interfaces irb unit 11 family inet address 10.11.11.1/24
set bridge-domains MGMT routing-interface irb.11

set interfaces xe-0/0/1 unit 0 family bridge interface-mode trunk
set interfaces xe-0/0/1 unit 0 family bridge vlan-id-list [ 11 300 ]

set interfaces interface lo0 unit 0 family inet address 1.1.1.1/32

set protocols ospf area 0 interface irb.11
set protocols ospf area 0 interface lo0.0

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
MC-LAG

ICL - Inter-Chassis Link
ICCP - Intercontrol Center Communications Protocol

State Modes:
    -Active-Standby
    -Active-Active

ICCP:
    -Peer between Loopback addresses
    -Combine with BFD

PE-Routers ICCP:
set switch-options service-id 1
set protocols iccp local-ip-addr 1.1.1.1
set protocols iccp peer 2.2.2.2
set protocols iccp peer 2.2.2.2 redundancy-group-id-list 1
set protocols iccp peer 2.2.2.2 liveness-dectection minimium-interval 50
set protocols iccp peer 2.2.2.2 liveness-dectection multiplier 3

show bfd session

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
MC-LAG

ICL - Inter-Chassis Link
ICCP - Intercontrol Center Communications Protocol

State Modes:
    -Active-Standby
    -Active-Active

Active-Standby

set chassis aggregated-devices ethernet device-count 1
set interfaces ge-0/0/0 ether-options 802.3ad ae0

# Must match on both sides:
set interfaces ae0 aggregated-ether-options lacp active
set interfaces ae0 aggregated-ether-options lacp periodic fast
set interfaces ae0 aggregated-ether-options admin-key 22
set interfaces ae0 aggregated-ether-options lacp system-id aa:aa:bb:bb:cc

set interfaces ae0 aggregated-ether-options mc-ae mode active-standby
set interfaces ae0 aggregated-ether-options mc-ae mc-ae-id 1
set interfaces ae0 aggregated-ether-options mc-ae redundancy-group 1

# Must be different on both sides:
set interfaces ae0 aggregated-ether-options mc-ae chassis-id 0
set interfaces ae0 aggregated-ether-options mc-ae status-control active

# Bridge configs on the AE0 interface
set interfaces ae0 unit 0 family bridge interface-mode trunk
set interfaces ae0 unit 0 family bridge vlan-id-list 300

# Verify PE-Side
show interfaces mc-ae

# Verify Client
show lacp interfaces

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
MC-LAG

ICL - Inter-Chassis Link
ICCP - Intercontrol Center Communications Protocol

State Modes:
    -Active-Standby
    -Active-Active

Active-Active

set interfaces ae0 multi-chassis-protection 2.2.2.2 interface xe-0/0/1
set interfaces ae0 aggregated-ether-options mc-ae mode active-active
# One Side
set interfaces ae0 aggregated-ether-options mc-ae status-control active
# Other Side
set interfaces ae0 aggregated-ether-options mc-ae status-control standby

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
]

questions_tunneling = [
{
"question" : """
Tunneling

GRE
    gr-0/0/0
IP-over-IP
    ip-0/0/0

# Enable Tunneling
set chassis fpc 0 pic 0 tunnel-services
set chassis fpc 0 pic 0 tunnel-services bandwidth 1g
show chassis

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Tunneling
IP-over-IP
    ip-0/0/0

WAN IPs:
|vMX1: 12.12.12.12| <-> |vMX2: 22.22.22.22|

set interfaces ip-0/0/0 unit 0 tunnel source 12.12.12.12
set interfaces ip-0/0/0 unit 0 tunnel destination 22.22.22.22
set interfaces ip-0/0/0 unit 0 family inet address 10.0.0.1/24

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Tunneling
GRE
    gr-0/0/0

Multicast support

32-bit GRE Header + IP Header
    4-bytes + 20 bytes
|IP(20-bytes)|GRE(4-bytes)|IP|TCP/UDP|L2|Data|L2-CRC|

WAN IPs:
|vMX1: 12.12.12.12| <-> |vMX2: 22.22.22.22|

set interfaces gr-0/0/0 unit 0 tunnel source 12.12.12.12
set interfaces gr-0/0/0 unit 0 tunnel destination 22.22.22.22
set interfaces gr-0/0/0 unit 0 family inet address 10.0.0.1/24
set interfaces gr-0/0/0 unit 0 family inet6 address 2001:cccc:aaaa::aacc/64

set protocols ospf area 2 gr-0/0/0.0

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Tunneling
GRE
    gr-0/0/0

Frames over GRE

set chassis network-services enhanced-ip
set interfaces gr-0/0/0 unit 0 tunnel source
set interfaces gr-0/0/0 unit 0 tunnel destination
set interfaces gr-0/0/0 unit 0 family bridge interface-mode trunk
set interfaces gr-0/0/0 unit 0 family bridge vlan-id-list 100
set interfaces gr-0/0/0 unit 0 family bridge core-facing

set routing-instances vSW instance-type virtual-switch
set routing-instances vSW interface gr-0/0/0.0
set routing-instances vSW bridge-domains 100 vlan-id 100

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Tunneling
GRE
    gr-0/0/0

MPLS over GRE

set interfaces gr-0/0/0 unit 0 tunnel source
set interfaces gr-0/0/0 unit 0 tunnel destination
set interfaces gr-0/0/0 unit 0 family inet address 10.0.0.1/24
set interfaces gr-0/0/0 unit 0 family mpls

set protocols mpls interface gr-0/0/0.0
set protocols ldp interface gr-0/0/0.0
set protocols ospf area 0 interface gr-0/0/0.0

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
]

questions_chassis_ha = [
{
"question" : """
VRRP
    -Master | Backup
        -Priority: 1-254, or 255 if saving an IP
        -Highest IP Address
    -224.0.0.18
    -Group-ID (0-255, 8-bit)
    -VIP
    -VMAC: 0000.5e00.01xx
    -VRRP (version 2 or version 3 (subsecond timers and IPv6))


set interfaces xe-0/0/0 unit 231 inet address 10.12.12.1/29 vrrp-group 12 virtual-address 10.12.12.6
set interfaces xe-0/0/0 unit 231 inet address 10.12.12.1/29 vrrp-group 12 priority 120

show vrrp

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Graceful Restart
    -Cisco: Non-Stop Forwarding != Juniper NSR
    -Helpers, keep a copy of your neighbors control plane

set routing-options graceful-restart

show ospf overview

""",
"answer" : """set routing-options graceful-restart""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
GRES (Graceful Routing Engine Switchover)
    RE- Routing Engine (re0 and re1)
    PFE - Attach and Reattach to the running RE
    Does not support Control Plane failover
        Combine with Graceful Restart to speed up control plane convergence

set chassis redundancy graceful-switchover

show system switchover
request chassis routing-engine master switch check

""",
"answer" : """set chassis redundancy graceful-switchover""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
NSR (Nonstop Active Routing)
    Better alternative to Graceful Restart (either Graceful Restart or NSR)
    Works with GRES
    Control Plane replecation across re0 and re1

delete routing-options graceful-restart

# Duplicate the Control Plane
set routing-options nonstop-routing

# Duplicate Commits
set system commit synchronize

show task replication

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
ISSU (In-Service Software Upgrade)

Full of bugs and holds up production!

Requires GRES and NRS
Update REs one-by-one

request system software in-service-upgrade /var/tmp/junos-19.2R4.8.tgz reboot

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
{
"question" : """
Virtual Chassis

Combine multiple EXs into one logical chassis
""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
]

questions_ipv6 = [
{
"question" : """
OSPF

""",
"answer" : """""",
"prompt": "root@vmx1# ",
"clear_screen": True,
"suppress_positive_affirmation": False,
"post_task_output": """"""
},
]
