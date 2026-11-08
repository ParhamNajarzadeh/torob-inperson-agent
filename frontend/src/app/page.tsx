"use client";
import React, { useEffect, useState } from "react";

export default function TorobInPersonConciergePage() {
  const [iframeSrc, setIframeSrc] = useState("/torob_inperson_concierge.html");

  useEffect(() => {
    if (typeof window !== "undefined") {
      const qs = window.location.search || "";
      const hash = window.location.hash || "";
      if (qs || hash) {
        setIframeSrc(`/torob_inperson_concierge.html${qs}${hash}`);
      }
    }
  }, []);

  return (
    <iframe
      src={iframeSrc}
      className="w-full h-screen border-none"
      title="وب‌سایت چندصفحه‌ای و دستیار هوشمند خرید حضوری ترب در تهران"
    />
  );
}
