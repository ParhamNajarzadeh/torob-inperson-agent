import React from "react";

export interface OutreachApprovalDialogProps {
  shopName: string;
  channel: "ai_voice_call" | "seller_1tap_webhook";
  onChangeChannel: (ch: "ai_voice_call" | "seller_1tap_webhook") => void;
  customQuestion: string;
  onChangeQuestion: (q: string) => void;
  onApprove: () => void;
  onCancel: () => void;
}

export const OutreachApprovalDialog: React.FC<OutreachApprovalDialogProps> = ({
  shopName,
  channel,
  onChangeChannel,
  customQuestion,
  onChangeQuestion,
  onApprove,
  onCancel
}) => {
  return (
    <div className="bg-white rounded-2xl border-2 border-[#D73948] p-4 shadow-md">
      <div className="flex items-center justify-between mb-2">
        <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-[#FFF1F2] text-[#D73948]">
          دروازه تأیید انسانی (LangGraph interrupt() HITL Gate)
        </span>
        <span className="text-xs text-slate-500">حریم خصوصی شماره شما ۱۰۰٪ محفوظ است</span>
      </div>
      <h4 className="font-bold text-base text-slate-900 mb-1">
        نیاز نیست خودتان زنگ بزنید! وکیل صوتی و پیامکی ترب به‌جای شما با «{shopName}» صحبت می‌کند
      </h4>
      <p className="text-xs text-slate-600 mb-3">
        کانال استعلام خودکار و سؤالات مدنظرتان را تأیید یا ویرایش کنید:
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-3 text-xs">
        <button
          type="button"
          onClick={() => onChangeChannel("ai_voice_call")}
          className={`p-2.5 rounded-xl border text-right font-bold ${
            channel === "ai_voice_call"
              ? "border-[#D73948] bg-[#FFF1F2] text-[#D73948]"
              : "border-slate-200 text-slate-700"
          }`}
        >
          📞 تماس صوتی هوشمند AI با مغازه‌دار + میکرو-لینک ۱ کلیکی
        </button>
        <button
          type="button"
          onClick={() => onChangeChannel("seller_1tap_webhook")}
          className={`p-2.5 rounded-xl border text-right font-bold ${
            channel === "seller_1tap_webhook"
              ? "border-[#D73948] bg-[#FFF1F2] text-[#D73948]"
              : "border-slate-200 text-slate-700"
          }`}
        >
          💬 ارسال میکرو-لینک ۱ کلیکی در واتساپ / بله / پیامک فروشنده
        </button>
      </div>
      <input
        type="text"
        value={customQuestion}
        onChange={(e) => onChangeQuestion(e.target.value)}
        className="w-full p-2.5 rounded-xl border border-slate-300 text-xs mb-3"
        placeholder="سؤال تکمیلی از فروشنده (مثلاً: آیا پلمپ شرکتی رنگ مشکی موجوده و ترب‌پی حضوری دارید؟)"
      />
      <div className="flex gap-2">
        <button
          type="button"
          onClick={onApprove}
          className="flex-1 py-2 px-4 rounded-xl bg-[#D73948] text-white font-bold text-xs hover:bg-[#BE123C]"
        >
          ✅ تأیید و شروع استعلام خودکار توسط ایجنت
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="py-2 px-4 rounded-xl border border-slate-300 text-slate-700 font-semibold text-xs"
        >
          انصراف
        </button>
      </div>
    </div>
  );
};
