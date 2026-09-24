# SVIE Physics Engine

Runnable thermodynamic and fluid-dynamics models for the Supercritical Vapor-Injection Engine (SVIE) architecture.

**Package version:** 1.2.0

## Install

```bash
pip install -e "./packages/physics-engine[dev]"
```

## Guided demo

```bash
python -m svie_physics.demo
python -m svie_physics.demo --json
# or: svie-demo
```

## Modules

See the root [README.md](../../README.md) for the full module index (air/fuel through BLEND/MIRAGE/VECTOR).

## CLI examples

```bash
python -m svie_physics.air_fuel --spec specs/svie_v8_52L.yaml
python -m svie_physics.heat_exchanger --spec specs/svie_v8_52L.yaml --sfv specs/sfv_fuel_system.yaml
```

## API

```bash
uvicorn svie_physics.api:app --reload --app-dir packages/physics-engine/src --port 8000
```

- OpenAPI: http://127.0.0.1:8000/docs  
- Demo bundle: `GET /demo`

## Tests

```bash
pytest packages/physics-engine/tests -v
```
