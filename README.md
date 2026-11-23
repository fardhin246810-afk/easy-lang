# Easy Lang — Offline Translator

Easy Lang is a simple Google Translate-style interface powered by Meta NLLB-200. Translation runs on the computer hosting the model. Text is not sent to Google, Meta, or another translation API.

## What you need

- Python 3.10 or newer
- Several GB of free disk space for the NLLB-200 distilled 600M model
- Enough RAM to load the model; a supported CUDA GPU can improve speed
- Internet for the one-time model download and dependency installation

## Install and start on Windows

Open PowerShell in the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python download_model.py
python api_server.py
```

Then open **http://localhost:8000** on the computer. The app provides automatic source-language detection, manual language selection, language swapping, copy, clear, and translation.

## Use it on a phone

1. Keep `api_server.py` running on the computer that has the model.
2. Connect the phone and computer to the same trusted Wi-Fi network.
3. Open the local network address printed by the server (for example `http://192.168.1.20:8000`) on the phone.
4. Translate normally. The phone sends text to your computer over the local network; the model runs on the computer.

The phone is a remote interface, not a standalone NLLB device. The computer must remain on and connected to the local network. Do not expose this development server to the public internet or an untrusted network. For PWA installation on a phone, browsers generally require HTTPS; ordinary HTTP on a LAN may work as a website but may not allow service-worker installation.

## Streamlit alternative

```powershell
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Open `http://localhost:8501` on the computer, or use the computer's local IP on a phone connected to the same Wi-Fi.

## Fine-tune for a low-resource language pair

Create a `data` folder containing:

- `train_parallel.csv` and `val_parallel.csv`, each with `src` and `tgt` columns.
- Optional `mono_target.txt`, one target-language sentence per line.

Set `MT_SRC_LANG` and `MT_TGT_LANG` to NLLB language codes before training. Optional model-path settings are `MT_BASE_MODEL_NAME`, `MT_BASE_MODEL_DIR`, and `MT_FINETUNED_DIR`.

```powershell
python train_mt.py
```

The training script uses multilingual transfer learning, optional back-translation, and LoRA. Restart the app after training to use the fine-tuned model. Model weights are not included in the Git repository.

## Tests

```powershell
python -m unittest discover -s tests -v
```

GitHub Actions also runs Python compilation and the language-support unit tests. A full translation check requires downloading the model and running it on a suitable machine.
