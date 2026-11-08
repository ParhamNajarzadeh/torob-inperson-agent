import React from "react";

export interface ProductItem {
  product_id: string;
  persian_title: string;
  category_name: string;
  extracted_brand: string;
  clean_offer_count: number;
  distinct_shop_count: number;
  min_clean_price_toman: number;
  median_clean_price_toman: number;
  hedonic_fair_price_estimate: number;
  match_reason_badge: string;
}

export interface ProductComparisonCarouselProps {
  products: ProductItem[];
  selectedProductId: string;
  onSelectProduct: (id: string) => void;
  onOpenReview: (id: string) => void;
}

export const ProductComparisonCarousel: React.FC<ProductComparisonCarouselProps> = ({
  products,
  selectedProductId,
  onSelectProduct,
  onOpenReview
}) => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-base font-bold text-slate-900">
          کاندیداهای دقیق از جدول BaseProduct (موتور دوگانه قیمت منصفانه)
        </h3>
        <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 font-medium">
          تطابق ۱۰۰٪ با دیتاست ترب
        </span>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {products.map((p) => {
          const isSelected = p.product_id === selectedProductId;
          const savingPct = Math.round(
            ((p.median_clean_price_toman - p.min_clean_price_toman) / p.median_clean_price_toman) * 100
          );
          return (
            <div
              key={p.product_id}
              className={`rounded-2xl border p-3.5 flex flex-col justify-between transition ${
                isSelected ? "border-2 border-[#D73948] bg-[#FFF1F2]/40" : "border-slate-200 bg-white"
              }`}
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="text-[11px] font-bold px-2 py-0.5 rounded-md bg-[#FFF1F2] text-[#D73948]">
                    {p.match_reason_badge}
                  </span>
                  <span className="text-[11px] text-slate-500 font-mono">{p.product_id.slice(0, 14)}</span>
                </div>
                <h4 className="font-bold text-sm text-slate-900 leading-snug mb-2">{p.persian_title}</h4>
                <div className="text-xs text-slate-600 space-y-1 mb-3">
                  <div className="flex justify-between">
                    <span>فروشندگان حضوری تهران:</span>
                    <span className="font-bold text-slate-900">
                      {p.distinct_shop_count.toLocaleString("fa-IR")} مغازه ({p.clean_offer_count.toLocaleString("fa-IR")} آفر تمیز)
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>کمترین قیمت تمیز:</span>
                    <span className="font-bold text-emerald-700">
                      {p.min_clean_price_toman.toLocaleString("fa-IR")} تومان ({savingPct}٪ زیر میانه)
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>قیمت منصفانه هدونیک:</span>
                    <span className="font-semibold text-slate-800">
                      {p.hedonic_fair_price_estimate.toLocaleString("fa-IR")} تومان
                    </span>
                  </div>
                </div>
              </div>
              <div className="flex gap-2 pt-2 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => onSelectProduct(p.product_id)}
                  className="flex-1 py-1.5 px-2.5 rounded-xl bg-[#D73948] text-white text-xs font-bold hover:bg-[#BE123C]"
                >
                  نمایش مغازه‌ها روی نقشه
                </button>
                <button
                  type="button"
                  onClick={() => onOpenReview(p.product_id)}
                  className="py-1.5 px-2.5 rounded-xl border border-slate-300 text-slate-700 text-xs font-semibold hover:bg-slate-50"
                >
                  نقد و چک‌لیست تست
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
