# Cybersecurity — AETHER-OS (ISO/SAE 21434 Design Intent)

**Release:** 1.3.0 · **SoT:** [`specs/iso21434_aether.yaml`](../../specs/iso21434_aether.yaml) · [`specs/ota_fleet_policy.yaml`](../../specs/ota_fleet_policy.yaml)

Threats: guest-glass injection, unsigned OTA, diag-port abuse, NEXUS spoof. Zones: ASIL ECU · QM glass · untrusted phone.

OTA rules: signed-only, rollback required, SENTINEL not remotely disableable, physical overrides never bypassed by glass.

**Not a certificate.** Aligns CarPlay Ultra guest policy with `physical_wins`.
