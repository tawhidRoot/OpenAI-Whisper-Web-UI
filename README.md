# OpenAI Whisper Web UI

This repository provides a **simple, web-based interface** for using **OpenAI Whisper**, making it easy to transcribe audio files through a graphical interface. It is designed to be **lightweight, easy to set up, and user-friendly**.

---

## 🚀 Requirements

Before you begin, make sure you have the following installed on your machine:

✅ **Python** – Required to run the application. Download it here: [Python Official Website](https://www.python.org/downloads/)  
✅ **Git** – Used for cloning the repository. Download it here: [Git Official Website](https://git-scm.com/downloads)  
✅ **FFmpeg** – Needed for handling audio files. Download it here: [FFmpeg Official Website](https://ffmpeg.org/download.html)  
✅ **PyTorch** – Required for running OpenAI Whisper. Download it here: [PyTorch Official Website](https://pytorch.org/get-started/locally/)  
✅ **CUDA Toolkit (Optional, for GPU users)** – Boosts performance by running computations on a GPU. Install it here: [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)

---

## ✨ Features

✔️ **Easy-to-use web UI** – No command-line experience needed  
✔️ **Quick setup** – Install and start using it in minutes  
✔️ **Supports CPU & GPU** – Works on any device, but GPU acceleration is available for faster performance

---

## 📌 Installation & Usage

Follow these steps to set up and run the application:

### 🔹 Step 1: Clone the Repository

Open a terminal or command prompt and run:

```bash
git clone https://github.com/tawhidRoot/OpenAI-Whisper-Web-UI.git
```

Then navigate to the project folder:

```bash
cd OpenAI-Whisper-Web-UI
```

### 🔹 Step 2: Run the Setup

#### **For Windows users:**

Simply **double-click `setup.bat`**, and it will:  
✅ Install dependencies  
✅ Set up the environment  
✅ Check for updates

#### **For Linux/macOS users:**

1️⃣ Make the setup script executable:

```bash
chmod +x setup.sh
```

2️⃣ Run the setup script:

```bash
bash setup.sh
```

This will:

- Create a virtual environment (`venv`) if it doesn’t exist
- Install required dependencies like **Django** and **OpenAI Whisper**
- Check for CUDA and install **PyTorch** with GPU support (if available)

### 🔹 Step 3: Launch the Application

- **Windows users**: Double-click `start_app.bat`
- **Linux/macOS users**: Run:
  ```bash
  ./start_app.sh
  ```

That’s it! The web interface will open in your browser automatically.

---

## 🔥 Want to Learn More About OpenAI Whisper?

Check out the official GitHub repository:  
🔗 [OpenAI Whisper GitHub Repository](https://github.com/openai/whisper)

---

## 🛠 Troubleshooting

### ❌ Problem: GPU is Not Being Used

#### ✅ **Step 1: Check if CUDA is Installed**

Run this command in PowerShell or Command Prompt:

```powershell
where nvcc
```

If nothing appears, **CUDA is not installed properly**. Download **CUDA 12.6** from [NVIDIA's official site](https://developer.nvidia.com/cuda-12-6-0-download-archive).

#### ✅ **Step 2: Install PyTorch with CUDA Support**

Run:

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

Check if your GPU is detected:

```python
import torch
print(torch.cuda.is_available())  # Should return True
print(torch.cuda.get_device_name(0))  # Should show your GPU name
```

#### ✅ **Step 3: Force Whisper to Use GPU**

```powershell
python -m whisper --model medium --device cuda --fp16 False
```

If you still face issues, make sure your **NVIDIA drivers are up to date**.

---

## 📜 License

This project is open-source and licensed under the **MIT License**.

## 💡 Contributing

We welcome contributions! If you have improvements or bug fixes, feel free to submit a **pull request** or report an issue.

## ⚠️ Disclaimer

This project is **independent** and **not affiliated** with OpenAI. Use it at your own discretion.
