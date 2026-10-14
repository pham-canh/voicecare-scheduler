# DEVKIT — Devpost: Nebius x NVIDIA Global AI Hackathon (paste-ready)

> File này là nguồn duy nhất để điền form Devpost. Copy từng BOX vào đúng ô.
> Demo URL duy nhất: `ajthuna54`. Link cũ `lmzkozkdf4rssh4w6vz8p6` đã chết — không dùng.

---

## BOX 1 — DEMO URL (ô "Try it out / Demo URL")

```text
https://voicecare-scheduler-ajthuna54dqqhpqtt52n2b.streamlit.app/
```

Judge self-run (dán vào ô "Testing instructions" nếu có):

```text
Open the link, press RUN FULL DEMO (no key needed — Nemotron NLU runs
server-side). Then open the "Technical" panel and check the line
"NLU: nemotron". One click, full visit: listen → understand → book.
```

---

## BOX 2 — VIDEO URL (ô "Video URL", Devpost chỉ nhận YouTube/Vimeo)

File nguồn: `~/Desktop/voicecare-nemotron-submit.mp4` (1.5 MB, ~1:51, dưới 3 phút).

```text
YOUTUBE_URL_CHUA_UP
```

Sau khi upload YouTube Unlisted (Not-for-Kids), thay dòng trên bằng link thật,
đồng thời cập nhật cùng link đó vào `README.md` dòng Video.

---

## BOX 3 — IMAGE GALLERY (upload 3 ảnh, caption gợi ý)

1. `streamlit2.png` — caption: `One-click demo: cardiology 9:00 booked with ID (NLU: nemotron)`
2. `streamlit.png` — caption: `Voice-first scheduling UI — typed try-out, same pipeline as voice`
3. `nemotron-dashboard.png` (bạn tự chụp từ Nebius console, CHE KEY) — caption:
   `Live Nemotron inference on Nebius (nvidia/NVIDIA-Nemotron-3-NanoB-A3B) — real runtime, key redacted`

---

## BOX 4 — NEBIUS / NVIDIA FEEDBACK (ô bắt buộc, viết thật)

```text
Smooth: Nemotron-3-Nano via Nebius is OpenAI-compatible, so our NLU layer
needed no custom adapter — strict-JSON prompts returned stable entities and
the offline 3-case booking take passed unchanged.

Hard: 20s timeouts with no retry/structured-output meant we had to write our
own fallback chain (Nemotron -> Gemini -> regex) and surface the active
backend on screen so judges never mistake a fallback for the real thing.
```

---

## Ghi chú nội bộ (không dán lên Devpost)

- `SUBMIT_DRAFT.md` bản lablab.ai cũ đã xóa — không dùng link `lmzkozkdf4rssh4w6vz8p6` ở bất cứ đâu.
- Trước khi bấm Submit: mở app live → RUN FULL DEMO → expander Technical → phải thấy `NLU: nemotron`. Thấy `gemini` = `NEBIUS_API_KEY` chưa có trong Streamlit Secrets → sửa rồi redeploy.
- Submit là một chiều. Đủ 4 ô + source repo GitHub đã push mới bấm.
