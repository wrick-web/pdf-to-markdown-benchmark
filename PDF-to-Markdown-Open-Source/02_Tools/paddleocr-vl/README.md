# PaddleOCR-VL / PP-StructureV3

Apache-2.0 · Python · https://github.com/PaddlePaddle/PaddleOCR

**Status: attempted-blocked.** Installed cleanly (`paddleocr[doc-parser]==3.7.0`),
but both its default (Hugging Face) and documented fallback (Baidu Object
Storage, `PADDLE_PDX_MODEL_SOURCE=BOS`) model sources are blocked by this
sandbox's network policy. 0 of 3 benchmark PDFs could be tested. See
`observations.md` for the exact evidence (`logs/init_attempt_*.log`) and
`setup/` for full install/reproduce instructions on an unrestricted
machine.
