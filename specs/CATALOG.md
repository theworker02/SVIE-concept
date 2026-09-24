# SVIE Spec Catalog

Thirty-five+ YAML source-of-truth files (see `python -m svie_physics.inventory` for live count). Physics modules and golden tests read these — do not hard-code numbers in docs without updating the matching YAML + pytest.

| Spec | Domain | Licensing package |
|------|--------|-------------------|
| `svie_v8_52L.yaml` | 5.2 L SFV V8 WOT baseline | SFV-CORE |
| `sfv_fuel_system.yaml` | Pressure ladder + HEX golden | SFV-CORE |
| `piezo_injector.yaml` | Piezo stroke / orifice / driver | SFV-CORE |
| `svie_v8_hr_357.yaml` | 3.57 L high-RPM H₂ DI V8-HR | DEVA-HR |
| `deva_valvetrain.yaml` | Camless electromagnetic valves | DEVA-HR |
| `h2_combustion_control.yaml` | λ / water-DI / NOx indices | DEVA-HR |
| `12m_ds_transmission.yaml` | 12-speed splitter manual | AXIOM-DRIVE |
| `9a_mc_transmission.yaml` | 9-speed multi-clutch auto | AXIOM-DRIVE |
| `hert_transaxle.yaml` | HERT expansion + GDSA + gears | AXIOM-DRIVE |
| `axiom_drive.yaml` | Anti-CVT KPIs (RBI = 0) | AXIOM-DRIVE |
| `ehe_v_bridge.yaml` | Belt-free hybrid bridge | AXIOM-DRIVE |
| `cvt_evidence.yaml` | Slip / efficiency evidence | AXIOM-DRIVE |
| `nexus_48.yaml` | 48 V energy bus budget | OPS-STACK |
| `sonic_nvh.yaml` | Secondary imbalance index | OPS-STACK |
| `sentinel_safety.yaml` | H₂ leak / isolation sensing | OPS-STACK |
| `chronos_cold_start.yaml` | Cold-start phase timeline | OPS-STACK |
| `trl_roadmap.yaml` | TRL stages + license packs | OPS-STACK |
| `blend_brake.yaml` | Brake blending | CONTROL |
| `mirage_twin.yaml` | Twin-path torque | CONTROL |
| `vector_hcp.yaml` | Hybrid control policy | CONTROL |
| `chassis_monocoque.yaml` | Torsion / bending nodes | STRUCTURE |
| `breakthrough_subsystems.yaml` | CCD / DKIS / CASMIR | STRUCTURE |
| `bom_cost_estimate.yaml` | Order-of-magnitude BOM | STRUCTURE |
| `thermal_oil_system.yaml` | Oil / thermal circuit | STRUCTURE |
| `engine_cryo_rail.yaml` | CRYO-RAIL buffered SFV rail | ENGINE-PLUS |
| `ring_zero.yaml` | RING-ZERO PTWA ring pack | ENGINE-PLUS |
| `oil_spine.yaml` | OIL-SPINE girdle gallery | ENGINE-PLUS |
| `aether_ign.yaml` | AETHER-IGN plasma/spark | ENGINE-PLUS |
| `flux_shift.yaml` | FLUX-SHIFT preselect | TRANS-PLUS |
| `gear_mesh_am.yaml` | GEAR-MESH-AM lattice carrier | TRANS-PLUS |
| `jet_bearing.yaml` | JET-BEARING HERT cooling | TRANS-PLUS |
| `node_cast_body.yaml` | NODE-CAST hybrid body | BODY-PLUS |
| `aero_skin.yaml` | AERO-SKIN active aero | BODY-PLUS |
| `cell_vault.yaml` | CELL-VAULT energy vault | BODY-PLUS |
| `thermal_skin.yaml` | THERMAL-SKIN heat rejection | BODY-PLUS |
| `manufacturing_master.yaml` | Process routes & cells | MFG-PLAN |
| `dry_sump_x.yaml` | DRY-SUMP-X scavenge | ADDONS |
| `pulse_egr.yaml` | PULSE-EGR NOx control | ADDONS |
| `silk_mount.yaml` | SILK-MOUNT active NVH | ADDONS |
| `range_bridge.yaml` | RANGE-BRIDGE series RE | ADDONS |
| `kers_blend.yaml` | KERS-BLEND recovery | ADDONS |
| `validation_matrix.yaml` | Validation SoT | ADDONS |
| `body_exterior.yaml` | Exterior body design | DESIGN |
| `lighting_headlamp.yaml` | Headlamp signature | DESIGN |
| `cabin_layout.yaml` | Cabin layout | DESIGN |
| `packaging_layout.yaml` | Internal zones | DESIGN |
| `wiring_harness.yaml` | Zone harness | DESIGN |
| `design_system.yaml` | Design rollup | DESIGN |
| `aether_os.yaml` | AETHER-OS analog-first vehicle OS | DESIGN |
| `carplay_ultra.yaml` | CarPlay Ultra guest policy | DESIGN |
| `analog_hmi.yaml` | Analog luxury HMI map | DESIGN |
| `homologation_path.yaml` | Homologation path (design) | COMPLIANCE |
| `iso26262_sentinel.yaml` | SENTINEL ASIL draft map | COMPLIANCE |
| `iso21434_aether.yaml` | AETHER cyber design map | COMPLIANCE |
| `ota_fleet_policy.yaml` | OTA / fleet policy | COMPLIANCE |
| `durability_gate.yaml` | Durability gate hours | COMPLIANCE |
| `supply_chain_tier1.yaml` | Critical Tier-1 map | COMPLIANCE |
| `acquisition_readiness.yaml` | Acquisition scorecard | ACQUIRE |
| `deal_structure.yaml` | Deal structures | ACQUIRE |
| `data_room_index.yaml` | Virtual data room | ACQUIRE |

Regenerate counts anytime:

```bash
python -m svie_physics.inventory
```
