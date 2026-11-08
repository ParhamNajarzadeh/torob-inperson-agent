import React from "react";

export interface StoreOfferItem {
  offer_id: string;
  shop_id: string;
  shop_name: string;
  is_real_entity: boolean;
  seller_title: string;
  registered_price_toman: number | null;
  last_price_changed_at: string;
  freshness_tier: "fresh_under_7d" | "moderate_7_to_30d" | "stale_over_30d" | "unpriced";
  probabilistic_stock_confidence_pct: number;
  crowdsourced_last_checkin_note: string | null;
  warranty_tier: "corporate" | "local_shop" | "none_or_unknown";
  shop_median_price_ratio: number;
  distance_km: number;
  passage_indoor_info: {
    passage_name: string;
    floor: string;
    corridor: string;
    unit_number: string;
  };
  today_hours_label: string;
  payment_capabilities: string[];
  verification_state: string;
  verified_live_price_toman: number | null;
  composite_store_score: number;
  why_recommended_badge: string;
}

export interface StoreComparisonMatrixProps {
  stores: StoreOfferItem[];
  onTriggerOutreach: (shopId: string) => void;
  onOpenIndoorNav: (shopId: string) => void;
}

export const StoreComparisonMatrix: React.FC<StoreComparisonMatrixProps> = ({
  stores,
  onTriggerOutreach,
  onOpenIndoorNav
}) => {
  return (
    <div className="space-y-3">
      {stores.map((s) => {
        const isVerified = s.verification_state.startsWith("verified");
        return (
          <div
            key={s.offer_id}
            className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm hover:border-slate-300 transition"
          >
            <div className="flex flex-wrap items-start justify-between gap-2 mb-2">
              <div>
                <div className="flex flex-wrap items-center gap-1.5">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-[#FFF1F2] text-[#D73948]">
                    {s.why_recommended_badge}
                  </span>
                  {s.is_real_entity && (
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-purple-100 text-[#7C3AED]">
                      🌐 هویت واقعی در دیتاست (وب‌سایت / اینستاگرام)
                    </span>
                  )}
                  {s.shop_median_price_ratio < 0.9 && (
                    <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700">
                      خوش‌قیمت سیستماتیک (نسبت به میانه: {s.shop_median_price_ratio})
                    </span>
                  )}
                </div>
                <h4 className="text-base font-bold text-slate-900 mt-1.5">{s.shop_name}</h4>
                <p className="text-xs text-slate-500 mt-0.5">عنوان فروشنده: {s.seller_title}</p>
              </div>
              <div className="text-left">
                <div className="text-xs text-slate-500">امتیاز مرکب StoreScore</div>
                <div className="text-lg font-extrabold text-slate-900">
                  {(s.composite_store_score * 100).toFixed(0)}٪
                </div>
              </div>
            </div>

            {/* 3-Tier Price Transparency Panel */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5 p-3 rounded-xl bg-slate-50 border border-slate-100 mb-3 text-xs">
              <div>
                <span className="text-slate-500 block">۱. قیمت ثبت‌شده در دیتاست:</span>
                <span className="font-bold text-slate-800 text-sm">
                  {s.registered_price_toman
                    ? `${s.registered_price_toman.toLocaleString("fa-IR")} تومان`
                    : "نامشخص — نیازمند استعلام تلفنی"}
                </span>
              </div>
              <div>
                <span className="text-slate-500 block">۲. زمان آخرین تغییر قیمت:</span>
                <span className="font-semibold text-amber-700">{s.last_price_changed_at}</span>
              </div>
              <div>
                <span className="text-slate-500 block">۳. قیمت و موجودی تأییدشده امروز:</span>
                {isVerified && s.verified_live_price_toman ? (
                  <span className="font-extrabold text-emerald-600 text-sm">
                    ✅ {s.verified_live_price_toman.toLocaleString("fa-IR")} تومان (موجود و باز)
                  </span>
                ) : (
                  <span className="font-semibold text-slate-600">
                    ⏳ نیازمند استعلام نهایی (توسط وکیل صوتی ترب)
                  </span>
                )}
              </div>
            </div>

            {/* Pointy Stock Confidence & Waze Shopper Check-in */}
            <div className="flex flex-wrap items-center justify-between gap-2 text-xs mb-3">
              <div className="flex items-center gap-2">
                <span className="font-medium text-slate-700">رادار احتمال موجودی زنده (Pointy Score):</span>
                <span className="font-bold text-emerald-700">{s.probabilistic_stock_confidence_pct}٪</span>
              </div>
              {s.crowdsourced_last_checkin_note && (
                <span className="px-2.5 py-1 rounded-lg bg-blue-50 text-blue-800 font-medium">
                  👋 گزارش جمعی خریداران (Waze Check-in): {s.crowdsourced_last_checkin_note}
                </span>
              )}
            </div>

            <div className="flex flex-wrap items-center justify-between gap-2 pt-2.5 border-t border-slate-100 text-xs">
              <div className="text-slate-600">
                📍 {s.passage_indoor_info.passage_name} • {s.passage_indoor_info.floor} •{" "}
                {s.passage_indoor_info.unit_number} ({s.distance_km} کیلومتری شما) | 🕒 {s.today_hours_label}
              </div>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => onTriggerOutreach(s.shop_id)}
                  className="px-3 py-1.5 rounded-xl bg-[#D73948] hover:bg-[#BE123C] text-white font-bold transition"
                >
                  🎙️ به‌جای من از مغازه‌دار بپرس (بدون تماس شما)
                </button>
                <button
                  type="button"
                  onClick={() => onOpenIndoorNav(s.shop_id)}
                  className="px-3 py-1.5 rounded-xl border border-slate-300 text-slate-800 font-semibold hover:bg-slate-50"
                >
                  🧭 نقشه داخل پاساژ و رزرو QR
                </button>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
