import React from "react";

export interface BourseWidgetProps {
  bourseName: string;
  neighborhood: string;
  specialtyDescription: string;
  famousPassages: string[];
  nearestMetro: string;
  bestVisitHours: string;
  buyingTips: string[];
  directoryShops: Array<{ shop_id: string; name: string; address: string }>;
}

export const TehranBourseLocationWidget: React.FC<BourseWidgetProps> = ({
  bourseName,
  neighborhood,
  specialtyDescription,
  famousPassages,
  nearestMetro,
  bestVisitHours,
  buyingTips,
  directoryShops
}) => {
  return (
    <div className="bg-white rounded-2xl border-2 border-indigo-200 p-4 shadow-sm space-y-3">
      <div className="flex items-center justify-between">
        <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-50 text-indigo-700">
          🧭 ساب‌ایجنت بورس‌یاب تخصصی تهران (ویژه کالاهای کمیاب یا خارج از کاتالوگ آنلاین)
        </span>
        <span className="text-xs text-slate-500">محله: {neighborhood}</span>
      </div>
      <h3 className="text-base font-bold text-slate-900">{bourseName}</h3>
      <p className="text-xs text-slate-600">{specialtyDescription}</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs bg-slate-50 p-3 rounded-xl">
        <div>
          <strong>پاساژهای اصلی راسته:</strong> {famousPassages.join("، ")}
        </div>
        <div>
          <strong>دسترسی مترو و BRT:</strong> {nearestMetro} ({bestVisitHours})
        </div>
      </div>
      <div className="text-xs space-y-1">
        <div className="font-bold text-slate-800">فروشگاه‌های هم‌صنف در این بورس (فاقد کاتالوگ آنلاین — مناسب پرس‌وجوی حضوری):</div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-1">
          {directoryShops.map((ds) => (
            <div key={ds.shop_id} className="p-2 rounded-xl border border-slate-200 bg-white">
              <div className="font-bold text-slate-900">{ds.name}</div>
              <div className="text-[11px] text-slate-500">{ds.address}</div>
            </div>
          ))}
        </div>
      </div>
      <div className="text-xs bg-indigo-50/60 p-2.5 rounded-xl text-indigo-950">
        <strong>نکات طلایی خرید حضوری در این بورس:</strong> {buyingTips.join(" • ")}
      </div>
    </div>
  );
};
