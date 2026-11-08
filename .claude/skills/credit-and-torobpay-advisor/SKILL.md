---
name: credit-and-torobpay-advisor
description: "Use when filtering stores by installment or credit payment options (torob_pay, snapp_pay, digi_pay, tara, azki_vam) and advising shoppers on in-person credit purchasing."
allowed-tools: ["tehran_spatial_bourse_mcp"]
---

# Instructions
1. Only `4.11%` of shops (`266` of `6,476`) declare structured `payment_options` (`190` TorobPay, `89` SnappPay, `61` DigiPay, `37` Tara, `5` AzkiVam).
2. When the user enables the `require_torobpay` or `require_installment` filter, prioritize verified stores with `torob_pay` (`in_person`), and if local matches drop below 2, display nearby same-passage stores where the AI Voice Proxy can inquire about in-person check/installment acceptance.
