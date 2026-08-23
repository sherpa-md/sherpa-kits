---
status: ai-sourced-untested
source_type: ai-synthesized
testing: not-tested
human_reviewed: false
model: qwen3.8-max
provider: qwen-cloud
risk_level: low
batch: deep-candidates-batch1
---

# Multimodal Image Intake Pipeline — OCR, Vision Triage, and Metadata Sanitization

## Problem
Teams receive large volumes of screenshots, photos of documents, receipts, and
diagrams. Sending raw images directly into an LLM chat wastes quota, leaks
EXIF/location metadata, and loses the text layer that downstream automation
needs. People need a repeatable intake pipeline: strip metadata, extract text,
classify the image, and only then route it to a vision-capable model with a
purpose-built prompt.

## Who experiences it
- Ops/automation builders wiring images into agent workflows.
- Anyone forwarding phone photos of whiteboards or documents to AI assistants.
- Fleet operators where every unneeded vision call burns subscription quota.

## Claims (sourced) vs inference
CLAIM: Tesseract is an open-source OCR engine maintained with broad language
support (source: https://github.com/tesseract-ocr/tesseract).
CLAIM: exiftool reads/writes metadata for hundreds of file formats
(source: https://github.com/exiftool/exiftool).
CLAIM: ComfyUI is a node-based UI for running diffusion-model workflows locally
(source: https://github.com/comfyanonymous/ComfyUI).
INFERENCE: Combining local OCR + metadata stripping before any cloud vision
call reduces cost and metadata exposure. This is a design hypothesis to be
validated by the validation plan below; it is not a measured result.

## Workflow
1. **Ingest**: collect images into an intake directory. Fill in:
   `INTAKE_DIR=<path>` `ARCHIVE_DIR=<path>`
2. **Sanitize metadata**: run exiftool to strip EXIF/GPS before any upload:
   `exiftool -all= -overwrite_original "$INTAKE_DIR"` (review files first).
3. **Local OCR pass**: run Tesseract on each image:
   `tesseract in.png out --dpi 300 -l eng` and keep the `.txt` beside it.
4. **Classify**: bucket each image by OCR text density and size:
   - dense text -> document lane (OCR text is primary, vision optional);
   - sparse text -> diagram/UI lane (vision call with focused prompt);
   - no text -> photo lane (vision only if the task truly needs it).
5. **Vision call (only when needed)**: attach the image plus the OCR text so
   the model can cross-check. Use the prompt template below.
6. **Record**: append one JSON line per image to `intake-log.jsonl` with
   filename, lane, ocr_word_count, model_called (true/false), and cost token
   estimate. This log is the evidence for validation.

## Copy/paste vision prompt (fill-in fields marked)
```text
You are reviewing a sanitized image for a <TASK: e.g. form digitization,
UI bug triage, chart reading>. OCR text extracted locally:
<OCR_TEXT or "none">
1. State what is visible that the OCR text does not capture.
2. Output structured fields: <FIELD LIST, e.g. vendor, date, total>.
3. Flag anything ambiguous rather than guessing.
Do not speculate about people, places, or anything outside the task.
```

## Status
**AI-SOURCED / UNTESTED.** Written by an LLM from public sources. No human has
run this pipeline end-to-end or measured its outcomes. Do not treat results as
verified until a Community Lab test report exists.
