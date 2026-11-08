export const INITIAL_TOROB_STATE = {
  thread_id: "thread_torob_tehran_2026",
  user_id: "user_tehran_shopper_01",
  current_step: "step_1_advisory",
  user_location: {
    lat: 35.7012,
    lon: 51.4075,
    label: "میدان ولیعصر"
  },
  planned_visit_datetime: "2026-10-22T17:30:00+03:30",
  budget_range_toman: { min: 1500000, max: 65000000 },
  active_filters: {
    max_radius_km: 5.5,
    require_installment: false,
    require_torobpay: false,
    open_now_only: true,
    real_shops_demo_mode: false
  },
  last_system_one_trace: {
    provider: "metis_jev",
    latency_ms: 38.4,
    intent_choice: "need_advisory_node",
    intent_confidence: 0.94,
    nouls: {
      has_exact_model: 0.88,
      needs_review_synthesis: 0.92,
      requires_credit_or_torobpay: 0.76,
      is_prompt_injection: 0.01
    },
    scores: {
      query_ambiguity: 0.18,
      value_for_money: 9.1,
      in_store_inspection_criticality: 9.5
    }
  }
};
