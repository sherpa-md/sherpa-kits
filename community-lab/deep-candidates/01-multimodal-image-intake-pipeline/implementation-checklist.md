# Implementation checklist
- [ ] Install tesseract and exiftool on the test machine.
- [ ] Create INTAKE_DIR and ARCHIVE_DIR outside any synced/cloud folder.
- [ ] Run exiftool strip on a copy; diff metadata before/after.
- [ ] OCR each image; store .txt next to image.
- [ ] Implement lane classifier (word-count thresholds; fill in thresholds).
- [ ] Wire vision calls for non-document lanes only.
- [ ] Append intake-log.jsonl records.
- [ ] Run the validation plan and fill TEST-RESULT-TEMPLATE.md.
