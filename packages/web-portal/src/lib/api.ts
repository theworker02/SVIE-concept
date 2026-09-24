const API_BASE =
  process.env.NEXT_PUBLIC_SVIE_API_URL?.replace(/\/$/, "") ||
  "http://127.0.0.1:8000";

async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`API ${path} failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`API ${path} failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export type AirFuelResult = {
  cycles_per_s: number;
  v_dot_air_m3_s: number;
  m_dot_air_kg_s: number;
  m_dot_air_g_s: number;
  m_dot_fuel_kg_s: number;
  m_dot_fuel_g_s: number;
  m_dot_fuel_kg_h: number;
  liquid_equiv_L_h: number;
  m_dot_fuel_per_bank_g_s: number;
  m_dot_per_injector_g_s: number;
  mg_per_stroke: number;
  e_in_kw: number;
};

export type HexResult = {
  q_hex_kw: number;
  q_hex_per_bank_kw: number;
  exhaust_energy_kw: number;
  exhaust_recovery_ratio: number;
  brake_power_kw: number;
  coolant_kw: number;
  e_in_kw: number;
};

export type HemResult = {
  pressure_ratio: number;
  is_choked: boolean;
  sigma_c: number;
  flash_boiling: boolean;
  a_o_required_mm2: number;
};

export type PiezoResult = {
  delta_z_um: number;
  a_o_mm2: number;
  delta_p_acoustic_mpa: number;
};

export type DriverResult = {
  e_c_mj: number;
  p_raw_w: number;
  p_total_w: number;
  l_r_uh: number;
  i_peak_a: number;
  p_dissipated_estimate_w: number;
};

export type WotBundle = {
  air_fuel: AirFuelResult;
  heat_exchanger: HexResult;
  hem: HemResult;
  piezo: PiezoResult;
  driver: DriverResult;
};

export function fetchWotBundle() {
  return apiGet<WotBundle>("/calc/wot-bundle");
}

export function postAirFuel(body: {
  displacement_m3: number;
  rpm: number;
  volumetric_efficiency: number;
  afr: number;
  air_density_kg_m3: number;
}) {
  return apiPost<AirFuelResult>("/calc/air-fuel", body);
}

export function fetchHex() {
  return apiGet<HexResult>("/calc/heat-exchanger");
}

export function fetchHem() {
  return apiGet<HemResult>("/calc/hem");
}

export function fetchPiezo() {
  return apiGet<PiezoResult>("/calc/piezo");
}

export function fetchDriver() {
  return apiGet<DriverResult>("/calc/driver");
}

export function fetchSpecList() {
  return apiGet<{ specs: string[] }>("/specs");
}

export function fetchSpec(name: string) {
  return apiGet<Record<string, unknown>>(`/specs/${name}`);
}

export { API_BASE, apiGet, apiPost };
