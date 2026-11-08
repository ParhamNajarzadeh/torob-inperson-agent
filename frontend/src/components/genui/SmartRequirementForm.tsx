import React from "react";

export interface SmartRequirementFormProps {
  selectedCategory: string;
  onSelectCategory: (cat: string) => void;
  budgetMax: number;
  onBudgetChange: (val: number) => void;
  selectedTags: string[];
  onToggleTag: (tag: string) => void;
  onSubmitNeed: () => void;
}

export const SmartRequirementForm: React.FC<SmartRequirementFormProps> = ({
  selectedCategory,
  onSelectCategory,
  budgetMax,
  onBudgetChange,
  selectedTags,
  onToggleTag,
  onSubmitNeed
}) => {
  const categories = [
    { id: "mobile", label: "گوشی موبایل و شارژر (بورس جمهوری)", median: "۵۵.۹M تومان" },
    { id: "sneakers", label: "کفش پیاده‌روی و کتانی (بورس منیریه)", median: "۶.۸M تومان" },
    { id: "laptop", label: "لپ‌تاپ مهندسی و گیمینگ (بورس ولیعصر)", median: "۱۴۷.۰M تومان" },
    { id: "cable", label: "سیم و کابل و تجهیزات برقی (بورس لاله‌زار)", median: "۱.۱۱M تومان" }
  ];
  const quickTags = [
    "ضمانت اصالت و رجیستری شرکتی",
    "پذیرنده حضوری ترب‌پی (۴ قسط)",
    "موجود در طبقه همکف پاساژ",
    "تأیید موجودی امروز بدون تماس تلفنی من"
  ];

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <div>
          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold bg-[#FFF1F2] text-[#D73948]">
            گام ۱ • فرم هوشمند شناسایی نیاز (Declarative A2UI)
          </span>
          <h3 className="text-base font-bold text-slate-900 mt-1">
            بدون تایپ طولانی، ویژگی‌های خرید حضوری خود را انتخاب کنید
          </h3>
        </div>
        <span className="text-xs text-slate-500">بر اساس ۲۲۵,۹۰۳ محصول دیتاست ترب</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-4">
        {categories.map((c) => (
          <button
            key={c.id}
            type="button"
            onClick={() => onSelectCategory(c.id)}
            className={`text-right p-2.5 rounded-xl border transition-all ${
              selectedCategory === c.id
                ? "border-[#D73948] bg-[#FFF1F2] text-[#D73948] font-bold"
                : "border-slate-200 hover:border-slate-300 text-slate-700"
            }`}
          >
            <div className="text-sm">{c.label}</div>
            <div className="text-xs text-slate-500 mt-0.5">میانه قیمت تمیز دیتاست: {c.median}</div>
          </button>
        ))}
      </div>

      <div className="mb-4">
        <div className="flex justify-between text-xs font-medium text-slate-700 mb-1">
          <span>سقف بودجه خرید حضوری:</span>
          <span className="text-[#D73948] font-bold">{budgetMax.toLocaleString("fa-IR")} تومان</span>
        </div>
        <input
          type="range"
          min={500000}
          max={180000000}
          step={500000}
          value={budgetMax}
          onChange={(e) => onBudgetChange(Number(e.target.value))}
          className="w-full accent-[#D73948]"
        />
      </div>

      <div className="flex flex-wrap gap-1.5 mb-4">
        {quickTags.map((tag) => {
          const active = selectedTags.includes(tag);
          return (
            <button
              key={tag}
              type="button"
              onClick={() => onToggleTag(tag)}
              className={`px-3 py-1 rounded-full text-xs border transition ${
                active
                  ? "bg-slate-900 text-white border-slate-900"
                  : "bg-slate-50 text-slate-700 border-slate-200"
              }`}
            >
              {active ? "✓ " : "+ "}
              {tag}
            </button>
          );
        })}
      </div>

      <button
        type="button"
        onClick={onSubmitNeed}
        className="w-full py-2.5 px-4 rounded-xl bg-[#D73948] hover:bg-[#BE123C] text-white font-bold text-sm transition shadow-sm"
      >
        مشاهده بهترین مدل‌های کاتالوگ ترب و مغازه‌های اطراف من ←
      </button>
    </div>
  );
};
