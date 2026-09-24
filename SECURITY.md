# Security & Handling

## Classification

This repository is **proprietary concept engineering**. It is not a consumer product and not a production vehicle ECU.

## Handling expectations

- Distribute only under NDA or executed license / SPA exhibits  
- Do not publish internal YAML golden blocks or unpublished claim charts to public forums without rights-holder approval  
- Treat H₂ safety narratives (SENTINEL) as **design intent**, not certified functional-safety work products  

## Export control

Powertrain thermodynamics, injector orifice sizing, and hybrid control architectures can be dual-use. **Buyer and seller trade counsel** own jurisdiction-specific classification (e.g. EAR / EU dual-use). This file does not constitute an export classification.

## Dependencies

Third-party packages (NumPy, SciPy, FastAPI, Next.js, React, etc.) remain under their upstream licenses. Run your own SCA / SBOM process before enterprise deployment.

## Reporting

Security issues in the *software surface* (API, portal) should be reported privately to the repository owner — not via public issues if exploitation is possible.

## Disclaimer

Models are unsuitable for safety-critical closed-loop vehicle control without OEM V&V. The portal and API are local diligence tools.
