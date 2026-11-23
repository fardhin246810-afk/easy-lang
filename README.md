# Easy Lang — Offline Neural Machine Translator

A private, on-device neural machine translation application supporting 200+ languages and script variants powered by Meta's NLLB-200. It performs source language auto-detection, tokenization, and Seq2Seq neural inference 100% offline without third-party cloud APIs.

## 📱 Mobile App & 💻 PC Desktop App (100% Secure & Zero Warnings)

Easy Lang is engineered for zero-vulnerability, trusted execution across mobile and desktop devices without triggering antivirus false positives or Play Protect warning banners:

### 1. 💻 Windows PC Desktop App (`EasyLang.exe`)
- **Native Executable:** Compiled native desktop launcher (`EasyLang.exe`) with embedded custom logo icon.
- **Standalone Window:** Launches the app in borderless application mode with custom window controls and no browser clutter.
- **Trusted Security:** Powered by Microsoft's built-in, digitally signed Edge/Chromium engine (`msedge --app`). Triggers **zero SmartScreen/antivirus warnings** and creates no temp-file security risks.
- **One-Click Desktop Shortcut:** Run `Create-Desktop-Shortcut.bat` to place an icon directly on your Windows desktop.

### 2. 📱 Mobile App (Android & iPhone / iPad)
- **Progressive Web App (PWA):** Compliant with Google and Apple PWA standards (`manifest.json` + `sw.js`).
- **Zero Harmful Warnings:** Unlike unsigned third-party `.apk` files that get blocked by Google Play Protect or show scary *"This file might be harmful"* banners, PWA installs natively from your browser with full security verification.
- **Home Screen Launcher & Splash Screen:** Installs directly to the home screen with your custom icon and launches full-screen with the custom opening animation.
- **Full Offline Caching:** Assets are cached locally via the Service Worker, functioning seamlessly in offline/airplane mode.

---

## 🚀 How to Run

### Option A: Launch PC Desktop App
Double-click `EasyLang.exe` or run:
```powershell
.\EasyLang.exe
```

### Option B: Run Mobile & Local Network Server
Run `Start-Mobile-Server.bat` or:
```powershell
python api_server.py
```
Open the displayed local IP address (e.g. `http://192.168.1.XX:8000`) on your phone, then tap **"Install App"** or **"Add to Home Screen"**.

### Option C: Run Native Python Streamlit Engine
```powershell
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## Install and prepare the model

Use Python 3.10 or newer. The pretrained NLLB-200 distilled 600M model needs several GB of disk space and substantial RAM; a CUDA-capable GPU makes training and translation faster.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python download_model.py
```

The one-time model download requires internet. Keep the generated `models\nllb-200-distilled-600M` directory on the computer that will host the app. Once it is present, model loading and translation use local files only.

## Run on a laptop and phone

Run the app on the hosting computer:

```powershell
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

On the laptop, open `http://localhost:8501`. For a phone, connect it to the same Wi-Fi/local network, find the laptop's IPv4 address with `ipconfig`, and open `http://<laptop-ip>:8501` in the phone browser. The layout adapts to narrow screens. Keep the hosting computer and app running while translating from the phone; translation is computed on that computer. This setup needs no internet once installed, but it is not a standalone mobile app and the phone cannot translate when disconnected from the host or local network. Do not expose the unauthenticated Streamlit server to an untrusted or public network.

## Fine-tune for a low-resource language pair

Create a `data` directory with:

- `train_parallel.csv` and `val_parallel.csv`, each with `src` and `tgt` columns.
- Optional `mono_target.txt`, one target-language sentence per line.

The app's language selectors use the language codes present in the installed NLLB tokenizer. Automatic source detection uses the offline `langid` package; short or unsupported text can be ambiguous, so users can choose the source language manually. The training script still defaults to `eng_Latn` and `hin_Deva`; set `MT_SRC_LANG` and `MT_TGT_LANG` for another training pair. `MT_BASE_MODEL_NAME`, `MT_BASE_MODEL_DIR`, and `MT_FINETUNED_DIR` can override model paths; set the same values when downloading, training, and running the app.

```powershell
python train_mt.py
```

The training pipeline uses multilingual transfer learning, tagged stochastic back-translation from target-side monolingual text, and LoRA to update a small set of attention parameters. It cleans blank and duplicate pairs, caps synthetic examples at the size of the real parallel corpus to limit noise, uses dynamic batch padding and gradient accumulation, selects the best checkpoint by validation chrF, and reports BLEU and chrF. Back-translation is skipped when no monolingual file is provided. Training uses only the local base model and local metric implementations; it does not fetch models or evaluation scripts from the internet.

After fine-tuning, restart the app to use the fine-tuned model. If it is absent, the app uses the pretrained model. The selected model's weights are not bundled with this source code.

Run the language detection tests with `py -m unittest discover -s tests`.
