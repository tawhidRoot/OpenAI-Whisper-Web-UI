# OpenAI Whisper Web UI

This repository provides a **simple, web-based interface** for using **OpenAI Whisper**, enabling users to effortlessly transcribe audio through a graphical interface. It is designed to be lightweight, easy to set up, and user-friendly.

## Requirements

Before you start, ensure you have the following installed on your machine:

1. **Python** - A programming language required to run the application. You can download it from the official website here: [Python Official Website](https://www.python.org/downloads/).
2. **Git** - A version control system to clone the repository. You can download it from the official website here: [Git Official Website](https://git-scm.com/downloads).
3. **FFmpeg** - A multimedia framework for handling audio and video files. You can download it from the official website here: [FFmpeg Official Website](https://ffmpeg.org/download.html).
4. **CUDA Toolkit (Optional)** - If you plan to use a GPU for faster processing, ensure that the [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) is installed along with the appropriate drivers for your GPU.

## Features

- **User-friendly web UI** for seamless interaction with OpenAI Whisper.
- **Effortless installation** with a minimal setup process.
- **Local execution**, allowing you to run the app with a simple double-click.

## Installation & Usage

Follow the steps below to set up and use the application.

### 1. Clone the Repository

Start by cloning the repository to your local machine. If you don't have **Git** installed, you can download it from the official website here: [Git Official Website](https://git-scm.com/downloads).

Once Git is installed, you can clone the repository using the following command:

```bash
git clone https://github.com/tawhidRoot/OpenAI-Whisper-Web-UI.git
```

### 2. Navigate to the Project Directory

After cloning, navigate to the project folder:

```bash
cd OpenAI-Whisper-Web-UI
```

### 3. Run the Setup

For **Windows users**:

- **Double-click `setup.bat`** to automatically complete the setup process. This will:
  - Install necessary dependencies
  - Set up the environment
  - Update Python if needed

For **Linux/macOS users**:

1. Before running the setup script, you may need to **make the script executable** by running:

   ```bash
   chmod +x setup.sh
   ```

2. Then, run the setup script with the following command:

   ```bash
   bash setup.sh
   ```

The setup scripts will:

- Create a virtual environment (`venv`) if it doesn't exist.
- Install the required Python dependencies such as **Django** and **OpenAI Whisper**.
- Check if CUDA is available and install **PyTorch** with GPU support if CUDA is present. Otherwise, it will install PyTorch with CPU support.

### 4. Launch the Application

Once the setup is complete:

- **Windows users**: Simply **double-click `start_app.bat`** to launch the web application.
- **Linux/macOS users**: Double-click `start_app.sh` to run the app, or execute it from the terminal with:

  ```bash
  ./start_app.sh
  ```

### 5. Additional Tips

- If you encounter any errors during setup, rerun the setup script to ensure all dependencies are installed properly.
- For GPU support, make sure you have the **CUDA Toolkit** and **drivers** installed. If you don't have a GPU, the application will still work using CPU support.

---

## Troubleshooting

### **GPU Not Detected Issue**

If Whisper is not using your GPU, follow these steps:

#### **1. Check if CUDA is Installed**

Run the following command in PowerShell or Command Prompt:

```powershell
where nvcc
```

If no path is returned, CUDA is not installed correctly. Install **CUDA 12.6** from [NVIDIA's official site](https://developer.nvidia.com/cuda-12-6-0-download-archive).

#### **2. Set Up CUDA Path (If Installed)**

Run this command in PowerShell:

```powershell
$env:PATH += ";C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin"
```

Then, check if CUDA is detected:

```powershell
nvcc --version
```

#### **3. Install PyTorch with CUDA 12.6**

Run:

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

Verify GPU availability:

```python
import torch
print(torch.cuda.is_available())  # Should return True
print(torch.cuda.get_device_name(0))  # Should return your GPU name
```

#### **4. Run Whisper with GPU**

Use:

```powershell
python -m whisper --model medium --device cuda
```

If it still runs on CPU, force GPU usage:

```powershell
python -m whisper --model medium --device cuda --fp16 False
```

If you still face issues, ensure your **NVIDIA drivers are up to date**.

---

## License

This project is open-source and licensed under the **MIT License**.

## Contributing

Contributions are welcome! If you have any improvements or fixes, feel free to submit a **pull request** or report any issues you encounter.

## Disclaimer

This project is **independent** and **not affiliated** with OpenAI. Use this project at your own discretion.
