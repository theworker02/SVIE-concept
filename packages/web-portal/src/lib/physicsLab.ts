/** Client-side SVIE physics lab — same maps as svie_physics.physics_lab for offline/Pages. */

const R_AIR = 287.05;
const DELTA_H = 820;
const GOLDEN_RPM = 8500;
const GOLDEN_ETA = 1.05;
const GOLDEN_AFR = 16.2;
const GOLDEN_BTE = 0.42;

export type LabInputs = {
  rpm: number;
  afr: number;
  load: number;
  tempC: number;
  pressureKpa: number;
  boostKpa: number;
  displacementM3?: number;
  cylinders?: number;
};

export type LabPoint = {
  rpm: number;
  afr: number;
  load: number;
  air_density_kg_m3: number;
  eta_v: number;
  eta_v_effective: number;
  m_dot_air_kg_s: number;
  m_dot_fuel_g_s: number;
  mg_per_stroke: number;
  e_in_kw: number;
  bte: number;
  brake_power_kw: number;
  brake_power_hp: number;
  torque_nm: number;
  q_hex_kw: number;
  exhaust_kw: number;
  hex_recovery: number;
  injector_pw_ms: number;
  injector_duty: number;
  choked_orifice_ok: boolean;
};

function airDensity(tempC: number, pressureKpa: number): number {
  return (pressureKpa * 1000) / (R_AIR * (tempC + 273.15));
}

function volumetricEfficiency(rpm: number, peakEta = GOLDEN_ETA, peakRpm = GOLDEN_RPM): number {
  const x = (rpm - peakRpm) / 2400;
  const eta = peakEta * Math.exp(-0.5 * x * x);
  return Math.max(0.72, Math.min(1.18, eta));
}

function bte(afr: number, load: number): number {
  const afrTerm = Math.exp(-(((afr - GOLDEN_AFR) / 7.5) ** 2));
  const loadTerm = 0.78 + 0.22 * Math.max(0.2, Math.min(1, load));
  return GOLDEN_BTE * afrTerm * loadTerm;
}

export function computePoint(inp: LabInputs): LabPoint {
  const displacement = inp.displacementM3 ?? 0.005204;
  const cylinders = inp.cylinders ?? 8;
  const pIntake = inp.pressureKpa + inp.boostKpa;
  const rho = airDensity(inp.tempC, pIntake);
  const etaV = volumetricEfficiency(inp.rpm);
  const etaEff = etaV * Math.max(0.15, Math.min(1, inp.load));
  const cps = inp.rpm / 120;
  const vDot = displacement * cps * etaEff;
  const mAir = vDot * rho;
  const mFuel = mAir / inp.afr;
  const mFuelGs = mFuel * 1000;
  const eIn = mFuel * 44000;
  const efficiency = bte(inp.afr, inp.load);
  const pBrake = eIn * efficiency;
  const torque = (pBrake * 1000 * 60) / (2 * Math.PI * inp.rpm);
  const qHex = mFuel * DELTA_H;
  const exhaust = eIn * 0.3;
  const perInj = mFuelGs / cylinders;
  const mg = (perInj / cps) * 1000;
  const cycleMs = (120 / inp.rpm) * 1000;
  const pw = mg * 0.084;
  const duty = pw / cycleMs;

  return {
    rpm: inp.rpm,
    afr: inp.afr,
    load: inp.load,
    air_density_kg_m3: Number(rho.toFixed(4)),
    eta_v: Number(etaV.toFixed(4)),
    eta_v_effective: Number(etaEff.toFixed(4)),
    m_dot_air_kg_s: Number(mAir.toFixed(5)),
    m_dot_fuel_g_s: Number(mFuelGs.toFixed(3)),
    mg_per_stroke: Number(mg.toFixed(2)),
    e_in_kw: Number(eIn.toFixed(1)),
    bte: Number(efficiency.toFixed(4)),
    brake_power_kw: Number(pBrake.toFixed(1)),
    brake_power_hp: Number((pBrake / 0.7457).toFixed(0)),
    torque_nm: Number(torque.toFixed(1)),
    q_hex_kw: Number(qHex.toFixed(2)),
    exhaust_kw: Number(exhaust.toFixed(1)),
    hex_recovery: Number((qHex / exhaust).toFixed(4)),
    injector_pw_ms: Number(pw.toFixed(2)),
    injector_duty: Number(duty.toFixed(3)),
    choked_orifice_ok: duty < 0.85 && mg > 0,
  };
}

export function computeSweep(
  inp: Omit<LabInputs, "rpm">,
  rpmMin = 1500,
  rpmMax = 9000,
  points = 40,
): LabPoint[] {
  const n = Math.max(5, Math.min(80, points));
  const step = (rpmMax - rpmMin) / (n - 1);
  const out: LabPoint[] = [];
  for (let i = 0; i < n; i++) {
    out.push(computePoint({ ...inp, rpm: rpmMin + step * i }));
  }
  return out;
}
