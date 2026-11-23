"""Shared local NLLB inference engine used by the web API and Streamlit UI."""
from __future__ import annotations
import threading
from pathlib import Path
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from language_support import detect_nllb_language, get_language_labels, get_supported_language_codes
from mt_config import BASE_MODEL_DIR, FINETUNED_DIR, SRC_LANG, TGT_LANG

def model_files_exist(model_dir: Path) -> bool:
    has_weights = any(model_dir.glob("*.safetensors")) or any(model_dir.glob("pytorch_model*.bin"))
    return model_dir.is_dir() and (model_dir / "config.json").is_file() and has_weights

class TranslationEngine:
    """Lazy-load local model files and serialize inference on the shared tokenizer."""
    def __init__(self, base_dir=BASE_MODEL_DIR, finetuned_dir=FINETUNED_DIR):
        self.base_dir = Path(base_dir)
        self.finetuned_dir = Path(finetuned_dir)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._lock = threading.RLock()
        self._tokenizers = {}
        self._models = {}

    def _model_dir_for_pair(self, source_language=None, target_language=None):
        if model_files_exist(self.finetuned_dir) and source_language == SRC_LANG and target_language == TGT_LANG:
            return self.finetuned_dir
        if model_files_exist(self.base_dir):
            return self.base_dir
        if model_files_exist(self.finetuned_dir):
            if source_language and target_language and (source_language, target_language) != (SRC_LANG, TGT_LANG):
                raise RuntimeError(f"Only the fine-tuned pair {SRC_LANG} -> {TGT_LANG} is installed. Install the base NLLB model to translate other pairs.")
            return self.finetuned_dir
        raise RuntimeError(f"No local translation model was found. Run python download_model.py first (expected: {self.base_dir}).")

    def _load_tokenizer(self, model_dir):
        key = str(model_dir.resolve())
        if key not in self._tokenizers:
            self._tokenizers[key] = AutoTokenizer.from_pretrained(key, local_files_only=True)
        return self._tokenizers[key]

    def _load_model(self, model_dir):
        key = str(model_dir.resolve())
        if key not in self._models:
            tokenizer = self._load_tokenizer(model_dir)
            model = AutoModelForSeq2SeqLM.from_pretrained(key, local_files_only=True)
            self._models[key] = (tokenizer, model.to(self.device).eval())
        return self._models[key]

    def languages(self):
        model_dir = self._model_dir_for_pair()
        with self._lock:
            tokenizer = self._load_tokenizer(model_dir)
            codes = get_supported_language_codes(tokenizer)
            labels = get_language_labels(codes)
        return [{"code": code, "label": labels[code]} for code in codes]

    def detect(self, text):
        if not isinstance(text, str) or len(text.strip()) < 4:
            return None
        model_dir = self._model_dir_for_pair()
        with self._lock:
            tokenizer = self._load_tokenizer(model_dir)
            supported = get_supported_language_codes(tokenizer)
        code = detect_nllb_language(text, supported)
        if not code:
            return None
        return {"code": code, "label": get_language_labels((code,))[code]}

    def translate(self, text, source_language, target_language, num_beams=4):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Enter text to translate.")
        if len(text) > 10000:
            raise ValueError("Text is too long. Keep each request under 10,000 characters.")
        if not isinstance(source_language, str) or not isinstance(target_language, str):
            raise ValueError("Choose both source and target languages.")
        if not isinstance(num_beams, int) or isinstance(num_beams, bool) or not 1 <= num_beams <= 6:
            raise ValueError("Beam search width must be between 1 and 6.")
        model_dir = self._model_dir_for_pair(source_language, target_language)
        with self._lock:
            tokenizer, model = self._load_model(model_dir)
            supported = set(get_supported_language_codes(tokenizer))
            if source_language not in supported:
                raise ValueError(f"Unsupported source language: {source_language}")
            if target_language not in supported:
                raise ValueError(f"Unsupported target language: {target_language}")
            tokenizer.src_lang = source_language
            inputs = tokenizer(text.strip(), return_tensors="pt", truncation=True, max_length=256).to(self.device)
            target_id = tokenizer.convert_tokens_to_ids(target_language)
            if target_id is None or target_id == tokenizer.unk_token_id:
                raise ValueError(f"{target_language!r} is not supported by the installed tokenizer.")
            with torch.inference_mode():
                output = model.generate(**inputs, forced_bos_token_id=target_id, max_new_tokens=256, num_beams=num_beams)
            translation = tokenizer.decode(output[0], skip_special_tokens=True)
            tokens = tokenizer.tokenize(text.strip())
        return {"translation": translation, "tokens": tokens, "model": str(model_dir)}
