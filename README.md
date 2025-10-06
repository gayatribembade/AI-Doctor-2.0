
# AI Doctor 2.0 - Project Setup & Usage Guide

AI Doctor 2.0 is a multimodal AI-powered assistant for medical image analysis and voice interaction. It uses Flask for the backend, a modern Tailwind CSS frontend, and integrates LLMs for image and text analysis, speech-to-text, and text-to-speech features.

---

This guide provides step-by-step instructions to set up your project environment, including the installation of FFmpeg and PortAudio across macOS, Linux, and Windows, as well as setting up a Python virtual environment using Pipenv, pip, or conda.

## Table of Contents

1. [Installing FFmpeg and PortAudio](#installing-ffmpeg-and-portaudio)
   - [macOS](#macos)
   - [Linux](#linux)
   - [Windows](#windows)
2. [Setting Up a Python Virtual Environment](#setting-up-a-python-virtual-environment)
   - [Using Pipenv](#using-pipenv)
   - [Using pip and venv](#using-pip-and-venv)
   - [Using Conda](#using-conda)
3. [Running the application](#project-phases-and-python-commands)
4. [Docker Deployment](#docker-deployment)
5. [Project Architecture & Features](#project-architecture--features)

## Installing FFmpeg and PortAudio

### macOS

1. **Install Homebrew** (if not already installed):

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install FFmpeg and PortAudio:**

   ```bash
   brew install ffmpeg portaudio
   ```


### Linux
For Debian-based distributions (e.g., Ubuntu):

1. **Update the package list**

```
sudo apt update
```

2. **Install FFmpeg and PortAudio:**
```
sudo apt install ffmpeg portaudio19-dev
```

### Windows

#### Download FFmpeg:
1. Visit the official FFmpeg download page: [FFmpeg Downloads](https://ffmpeg.org/download.html)
2. Navigate to the Windows builds section and download the latest static build.

#### Extract and Set Up FFmpeg:
1. Extract the downloaded ZIP file to a folder (e.g., `C:\ffmpeg`).
2. Add the `bin` directory to your system's PATH:
   - Search for "Environment Variables" in the Start menu.
   - Click on "Edit the system environment variables."
   - In the System Properties window, click on "Environment Variables."
   - Under "System variables," select the "Path" variable and click "Edit."
   - Click "New" and add the path to the `bin` directory (e.g., `C:\ffmpeg\bin`).
   - Click "OK" to apply the changes.

#### Install PortAudio:
1. Download the PortAudio binaries from the official website: [PortAudio Downloads](http://www.portaudio.com/download.html)
2. Follow the installation instructions provided on the website.

---

## Setting Up a Python Virtual Environment

### Using Pipenv
1. **Install Pipenv (if not already installed):**  
```
pip install pipenv
```

2. **Install Dependencies with Pipenv:** 

```
pipenv install
```

3. **Activate the Virtual Environment:** 

```
pipenv shell
```

---

### Using `pip` and `venv`
#### Create a Virtual Environment:
```
python -m venv venv
```

#### Activate the Virtual Environment:
**macOS/Linux:**
```
source venv/bin/activate
```

**Windows:**
```
venv\Scripts\activate
```

#### Install Dependencies:
```
pip install -r requirements.txt
```

---

### Using Conda
#### Create a Conda Environment:
```
conda create --name myenv python=3.11
```

#### Activate the Conda Environment:
```
conda activate myenv
```

#### Install Dependencies:
```
pip install -r requirements.txt
```



# Project Phases and Python Commands

## Phase 1: Brain of the doctor
```
python brain_of_the_doctor.py
```

## Phase 2: Voice of the patient
```
python voice_of_the_patient.py
```

## Phase 3: Voice of the doctor
```
python voice_of_the_doctor.py
```


## Phase 4: Run the Main Flask App
```
python app.py
```

---

# Docker Deployment

You can run the entire project in a Docker container (recommended for easy deployment):

1. **Build the Docker image:**
   ```sh
   docker build -t ai-doctor-app .
   ```
2. **Run the container:**
   ```sh
   docker run -p 8000:8000 ai-doctor-app
   ```
3. **Access the app:**
   Open your browser at [http://localhost:8000](http://localhost:8000)

---

# Project Architecture & Features

**Main Components:**
- `app.py`: Flask backend, handles all user requests, file uploads, and routes.
- `brain_of_the_doctor.py`: Encodes images and sends them to a multimodal LLM for medical analysis.
- `voice_of_the_patient.py`: Converts user audio to text (speech-to-text).
- `voice_of_the_doctor.py`: Converts text responses to audio (text-to-speech).
- `templates/index.html`: Modern Tailwind CSS frontend for user interaction.

**Key Features:**
- Upload medical images and/or record/upload voice questions.
- AI analyzes images and answers questions using LLMs.
- Doctor's response is returned as both text and audio.
- Fully containerized with Docker for easy deployment anywhere.

**Architecture Flow:**

```
User (Web UI)
   |
   v
[Flask Backend (app.py)]
   |         |         |
   |         |         |
   v         v         v
Image   Audio File   (Text)
 |         |           |
 v         v           |
[brain_of_the_doctor]  |
   |                   |
   v                   |
LLM Medical Analysis   |
   |                   |
   v                   |
Text Response <--------+
   |
   v
[voice_of_the_doctor.py] (Text-to-Speech)
   |
   v
Audio Response
   |
   v
User (Web UI)
```

---

