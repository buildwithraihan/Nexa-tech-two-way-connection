# Network Topology — NexaTech Solutions

## Physical Topology Diagram

```
KOCHI HQ                                    BENGALURU BRANCH
============                                ================

  [HR-PC1]  [HR-PC2]                          [HR-PC1]  [HR-PC2]
  Fa0/1     Fa0/2                             Fa0/1     Fa0/2
     \         /                                 \         /
  [IT-PC1]  [IT-PC2]                          [IT-PC1]  [IT-PC2]
  Fa0/3     Fa0/4                             Fa0/3     Fa0/4
        \   /                                       \   /
    [SW1-KOCHI]                               [SW1-BENGALURU]
    G0/1  G0/2                                G0/1  G0/2
      |      \                                  |      \
   [R1-KOCHI] \                           [R2-BENGALURU] \
   G0/0  G0/1  \                          G0/0  G0/1      \
                [SW2-KOCHI]                               [SW2-BENGALURU]
                Fa0/1  Fa0/2                              Fa0/1  Fa0/2
                Fa0/3  Fa0/4                              Fa0/3  Fa0/4
                  |      |     |    |                       |      |    |    |
              [Fin] [Fin] [Srv] [Prt]                   [Fin] [Fin] [Srv] [Prt]

    R1 G0/1 ────────────── WAN Link ────────────── R2 G0/1
              10.10.10.1/30            10.10.10.2/30
```

## Physical Cable Connections

### Kochi HQ

| From Device | From Port | To Device | To Port | Cable Type |
|---|---|---|---|---|
| R1-KOCHI | G0/0 | SW1-KOCHI | G0/1 | Straight-through |
| SW1-KOCHI | G0/2 | SW2-KOCHI | G0/1 | Straight-through |
| SW1-KOCHI | Fa0/1 | HR-PC1 | NIC | Straight-through |
| SW1-KOCHI | Fa0/2 | HR-PC2 | NIC | Straight-through |
| SW1-KOCHI | Fa0/3 | IT-PC1 | NIC | Straight-through |
| SW1-KOCHI | Fa0/4 | IT-PC2 | NIC | Straight-through |
| SW2-KOCHI | Fa0/1 | Finance-PC1 | NIC | Straight-through |
| SW2-KOCHI | Fa0/2 | Finance-PC2 | NIC | Straight-through |
| SW2-KOCHI | Fa0/3 | Server | NIC | Straight-through |
| SW2-KOCHI | Fa0/4 | Printer | NIC | Straight-through |

### WAN Link

| From Device | From Port | To Device | To Port | Cable Type |
|---|---|---|---|---|
| R1-KOCHI | G0/1 | R2-BENGALURU | G0/1 | Crossover (or Straight) |

### Bengaluru Branch

| From Device | From Port | To Device | To Port | Cable Type |
|---|---|---|---|---|
| R2-BENGALURU | G0/0 | SW1-BENGALURU | G0/1 | Straight-through |
| SW1-BENGALURU | G0/2 | SW2-BENGALURU | G0/1 | Straight-through |
| SW1-BENGALURU | Fa0/1 | HR-PC1 | NIC | Straight-through |
| SW1-BENGALURU | Fa0/2 | HR-PC2 | NIC | Straight-through |
| SW1-BENGALURU | Fa0/3 | IT-PC1 | NIC | Straight-through |
| SW1-BENGALURU | Fa0/4 | IT-PC2 | NIC | Straight-through |
| SW2-BENGALURU | Fa0/1 | Finance-PC1 | NIC | Straight-through |
| SW2-BENGALURU | Fa0/2 | Finance-PC2 | NIC | Straight-through |
| SW2-BENGALURU | Fa0/3 | Server | NIC | Straight-through |
| SW2-BENGALURU | Fa0/4 | Printer | NIC | Straight-through |

## VLAN Assignments

| VLAN | Name | SW1 Ports | SW2 Ports |
|---|---|---|---|
| 10 | HR | Fa0/1, Fa0/2 | — |
| 20 | IT | Fa0/3, Fa0/4 | — |
| 30 | Finance | — | Fa0/1, Fa0/2 |
| 40 | Servers | — | Fa0/3, Fa0/4 |
| 99 | Management | SVI only | SVI only |

## Trunk Links

All inter-device links (Router–Switch, Switch–Switch) carry:
`VLANs: 10, 20, 30, 40, 99` with `native VLAN 99`

## Packet Tracer — Step-by-Step Topology Build

1. Open Cisco Packet Tracer
2. Add devices from the toolbar:
   - 2× Cisco 2911 Router
   - 4× Cisco 2960-24TT Switch
   - 8× PC (Generic)
   - 2× Server (Generic)
   - 2× Printer (Generic)
3. Label all devices as shown in the topology
4. Connect using copper straight-through cables per the tables above
5. For R1 G0/1 → R2 G0/1, use a copper crossover cable
   (Packet Tracer auto-detects MDI/MDI-X so straight-through may also work)
