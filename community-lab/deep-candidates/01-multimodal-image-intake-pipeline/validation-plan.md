# Validation plan
1. Prepare 20 synthetic test images (screenshots, generated receipts with fake
   data, diagrams). Never use real personal documents.
2. Run the full pipeline; record per-image lane decisions.
3. Measure: images skipped for vision calls / total (target: >=40% for a
   document-heavy batch).
4. Spot-check OCR accuracy on 5 images against manual transcription.
5. Verify no EXIF remains after sanitization (exiftool read-back).
6. Compare vision-call token cost estimate vs naive all-images-to-vision.
Outcome is Pass/Partial/Fail recorded in the community test result template.
