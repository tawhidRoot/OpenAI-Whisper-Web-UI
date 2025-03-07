# OpenAI Whisper Web UI

This repository provides a simple, web-based interface for using OpenAI Whisper, enabling users to transcribe audio effortlessly through a graphical interface.

## Features

- User-friendly web UI for OpenAI Whisper.
- Straightforward setup with minimal installation steps.
- Local execution with a simple double-click to launch.

## Installation & Usage

### 1. **Clone the Repository**

Start by cloning the repository:

```bash
git clone https://github.com/tawhidRoot/OpenAI-Whisper-Web-UI.git
```

### 2. **Navigate to the Project Directory**

Change into the project folder:

```bash
cd OpenAI-Whisper-Web-UI
```

### 3. **Run the Setup**

Run the appropriate setup file for your operating system:

- **Windows**: Double-click `setup.bat` to automatically set up the environment, install dependencies, and update Python if necessary.
- **Linux/macOS**: Run `setup.sh` by executing the following command in your terminal:

  ```bash
  bash setup.sh
  ```

This will create a virtual environment, install required dependencies, and update Python if needed.

### 4. **Start the Application**

Once the setup is complete:

- **Windows**: Simply **double-click** `start_app.bat` to run the application.
- **Linux/macOS**: Double-click `start_app.sh` to start the app, or run it in the terminal:

  ```bash
  ./start_app.sh
  ```

### 5. **Additional Tips**

- If you encounter an error related to Python, ensure Python is installed on your system.
- You can update Python manually if needed using the provided installation instructions below.

---

## How to Install Python

If Python is not installed, follow these steps to install it:

- **Windows**: You can install Python via Windows Package Manager:

  ```bash
  winget install Python.Python.3.9
  ```

- **Linux (Ubuntu/Debian-based)**: Run the following commands to install Python:

  ```bash
  sudo apt update
  sudo apt install python3
  ```

- **macOS**: Use Homebrew to install Python:

  ```bash
  brew install python
  ```

---

## License

This project is open-source and licensed under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit pull requests or report issues.

## Disclaimer

This project is independent and not affiliated with OpenAI. Use at your own discretion.
