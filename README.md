# MultiplEYE WG1: Psychometric Tests

## Introduction

### What are the Psychometric Tests covered in this project?

Psychometric tests are a standard and scientific method used to measure individuals' cognitive abilities and behavioural style. They identify the extent to which candidates' personality and cognitive abilities match those required to perform the role. Employers use the information collected from the psychometric test to identify the hidden aspects of candidates that are difficult to extract from a face-to-face interview.

In this repository, we will cover the following psychometric tests:

1. **Lewandowsky WMC battery** : Working Memory Capacity (WMC) is a measure of the amount of information that can be held in mind and processed at one time. It is a key component of cognitive control and is strongly related to general intelligence. The Lewandowsky WMC battery is a set of tasks that measure WMC. The battery consists of four tasks: Memory Update, Operation Span, Sentence Span, and Spatial Short-Term Memory.
2. **RAN task**: The Rapid Automatized Naming (RAN) task is a test of the speed and efficiency of naming digits. It is used to assess the speed of processing and the ability to quickly retrieve information from memory.
3. **Stroop**: The Stroop test is a test of cognitive control that measures the ability to inhibit automatic responses. The test consists of a series of trials in which participants must respond to the color of words while ignoring the color words themselves.
4. **Flanker**: The Flanker test is a test of cognitive control that measures the ability to inhibit irrelevant information. The test consists of a series of trials in which participants must respond to a central target while ignoring flanking distractors.
5. **PLAB**: The PLAB test is Pimsleur Language Aptitude Battery test. It is a test of language aptitude that is designed to measure an individual's ability to learn a foreign language.
6. **WikiVocab**: The WikiVocab test is a test of vocabulary knowledge that is based on the Wikipedia corpus. It is designed to measure the breadth of an individual's vocabulary knowledge. For English, German, Dutch, Mandarin and Cantonese Chinese, Portuguese and Estonian, the LexTALE test items are used instead because they are available in the LexTALE dataset and have been validated in each language.

## Quick Start

### Video tutorial

We will add a short video tutorial for environment setup and running the experiment launcher.

- Installation and run walkthrough: [Video link coming soon](https://example.com/multipleye-psychometric-tests-install-run)

### Clone the repository

```bash
git clone git@github.com:MultiplEYE-COST/MultiplEYE-psychometric-tests.git
```
or
```bash
git clone https://github.com/MultiplEYE-COST/MultiplEYE-psychometric-tests.git
```

You can also download the repository as a zip file and unzip it to your desired location from the [GitHub repository](https://github.com/MultiplEYE-COST/MultiplEYE-psychometric-tests) by clicking the `Code` button and then `Download ZIP`. We recommend that you change the repository name to `MultiplEYE-psychometric-tests` after unzipping to avoid confusion.

### Create an environment, e.g with [miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/).
Please first check whether you have conda installed. If you have installed it, please skip installing.

**Note**: The steps of creating an environment is similar to the steps in the wg1-experiment-implementation repository. For details, please refer to the guidelines in the [wg1-experiment-implementation repository](https://github.com/MultiplEYE-COST/wg1-experiment-implementation)

1. In the root directory of the repository, create a new environment with the following command:
```bash
conda create --name psychopy python=3.10
```

**Note**: The environment name is `psychopy`. You can change it to your desired name. For example, if you want to create an environment named `psytest3.10`, you can run the following command:
```bash
conda create --name psytest3.10 python=3.10
```
However, then you need to change the environment names in the following steps to `psytest3.10`.

2. Activate the environment:
```bash
conda activate psychopy
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

**Note**:
Mac user may encounter error saying "subprocess-exited-with-error" and "Could not find a local HDF5 installation". If you encounter this error, please run the following command first to install the HDF5 package before running the above command to install the required packages:
```bash
conda install -c anaconda hdf5
```
Then you can simply rerun the above command to install the required packages.

**Note**:
Windows user may encounter error saying "ERROR: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/". If you encounter this error, please download the Microsoft C++ Build Tools from the link provided in the error message and install it. Then you can simply rerun the above command to install the required packages.
You can find detailed instructions on this stackoverflow [post](https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst).


Some more environment related errors may occur, and you can find more detailed documentation of how to handle possible errors in the [MultiplEYE WG1 Experiment Implementation Guidelines](https://github.com/MultiplEYE-COST/wg1-experiment-implementation/blob/main/guidelines/markdown/HANDLING_ERRORS.md).

### Run the tests in English

We provide the English materials for you to test the tests in English. First, download the English language data from the [MultiplEYE SwitchDrive data repository](https://drive.switch.ch/index.php/s/i9ecUhd8ygcRDMg?path=%2FPsychometric%20tests%2Flanguages%2FEN) if you have a password an an account. You can also download the data from the [MultiplEYE PsychArchives data repository](https://pasa.psycharchives.org/reviewonly/c46cc0928e2a20454cd5ad101f5b7c0e22ddb34085691e419743538f0e02327b) which does not require a password. After downloading, unzip the data and place `languages/EN` in the repository root.

Run the launcher from the root directory of the repository:
```bash
python run_multipleye_psychometric_tests.py
```
The launcher opens a GUI where you confirm participant and lab metadata (participant ID, session ID, language, country code, lab number, and year).

The experiment-level default settings are read from `configs/config.yaml`:
```yaml
language: EN
full_language: English
country_code: X
lab_number: 1
random_seed: 123
font: Segoe UI
```  
Task availability at experiment-level is also defined in `configs/config.yaml`:
```yaml
wmc: True
ran: True
stroop_flanker: True
plab: True
wiki_vocab: True
```

- Tasks set to `True` are shown in the GUI and can be deselected for a specific participant by unchecking the corresponding checkbox in the GUI.
- Tasks set to `False` are hidden and cannot be selected at runtime.
- The `config.yaml` file is used to define the default settings for the tests at a lab level, supposing that all partcipants in the same lab are doing the same tests. If you want to run specific tests for a specific participant, we recommend you to check/uncheck the corresponding checkbox in the GUI.
- After clicking `Start`, selected tasks run sequentially.
- If WMC is enabled, a second WMC window appears where you can choose WMC subtasks. By default, all 4 tasks are selected. You can deselect the tasks that you don't want to run. Click `OK` to start the selected tasks.
- Outputs are saved under `data/MultiplEYE_<LANG>_<COUNTRY>_<LAB>_<YEAR>/<PARTICIPANT>_<LANG>_<COUNTRY>_<LAB>_PT<SESSION>/`.

**Note**:
- Depends on your computer system (Mac, Windows, Linux) and the language you are going to run (e.g., English, Chinese, Persian, etc.), you may need to choose a suitable font for the experiment. The default font is `Segoe UI`, which supports most Latin and Cyrillic languages. If you are running Chinese in a Windows machine, you may need to choose a Chinese font like `Microsoft YaHei` or `SimSun`. We suggest you first try `Segoe UI` or `Arial Unicode MS` to see whether it can display all the characters correctly, and then try other fonts if you encounter any issues.
- Depends on your computer system, you may need to enable the audio input and output for the RAN task. If you encounter any issues with the audio input and output, please refer to the [PsychoPy documentation](https://www.psychopy.org/).
  - For Mac users, you may need to go to `System Preferences` -> `Security & Privacy` -> `Privacy` -> `Microphone` and enable your terminal or IDE to access the microphone.
  - For Windows users, you may need to go to `Settings` -> `Privacy` -> `Microphone` and enable your terminal or IDE to access the microphone.
  - For Linux users, you may need to go to `Settings` -> `Privacy` -> `Microphone` and enable your terminal or IDE to access the microphone.
- Depends on your computer system, you may need to enable the keyboard input. If you encounter any issues with the keyboard input, please refer to the [PsychoPy documentation](https://www.psychopy.org/).
  - For Mac users, you may need to go to `System Preferences` -> `Security & Privacy` -> `Privacy` -> `Input Monitoring` and add your terminal or IDE to the list.
  - For Windows users, you may need to go to `Settings` -> `Privacy` -> `Keyboard` and add your terminal or IDE to the list.
  - For Linux users, you may need to go to `Settings` -> `Privacy` -> `Keyboard` and add your terminal or IDE to the list.
- WMC currently supports macOS and Windows; Linux is not supported for WMC.
### Run the tests in other languages

**Note**: The current release (April 2026) includes 25 language versions, namely Albanian, Arabic, Basque, Cantonese, Catalan, Croatian, Czech, Danish, English, Estonian, Farsi, Finnish, German, Hebrew, Italian, Kalaallisut, Latvian, Mandarin, Portuguese, Romansh, Russian, Serbian, Slovenian, Swedish, and Turkish, spanning multiple writing systems and typological language families.

For more detailed instructions on what and how to prepare and translate the materials for other languages, please refer to Section 6 in [MultiplEYE Data Collection Guidelines](https://multipleye.eu/wp-content/uploads/MultiplEYE-Data-Collection-Guidelines.pdf). It contains the most up-to-date and official guideline for preparing and translating the materials. Here are some simplified instructions for you to follow:

1. To run the tests in other languages, first go to the `languages/EN` folder. Copy the `EN` folder and paste it in the `languages` folder. Rename the copied folder to the desired language code, e.g. `DE` for German.
2. Translate all the instructions and stimuli in the copied folder to the desired language.
- In the `instructions/` folder, for the instruction files (supported formats: `.xlsx` or `.csv`), add a new column with the desired language code (e.g., `DE`) and translate the instructions from the `EN` column to the desired language.
- Specifically, after translating the PLAB instruction, we suggestion you copy the texts in a slide or doc file and screenshot them since PLAB tasks take the form of images as some of its inputs. You can follow the screenshotting in the `EN/PLAB/` folder.
- In the `instructions/` folder, for the WMC instruction which is a doc file, you need to translate the whole file and then screenshot the instruction according to the English version and put them in the `DE/WMC/instructions` folder as png files. Name them exactly the same as the English version.
- You need to translate the stimuli for WMC tasks in the `WMC/` folder, which are yaml files.
- You don't need to translate anything for RAN tasks. This is why `RAN` folder is empty. Feel free to delete the empty `RAN` folder or keep it as it is.
- You have to translate the xlsx/csv stimuli for Stroop and Flanker tasks in the `Stroop-Flanker/` folders, respectively.
- You need to translate the xlsx/csv stimuli for PLAB tasks in the `PLAB/` folder. 
- If you want a different language from English to be used in the GUI, you need to translate the `english.json` file in the `ui_data` folder, and save it as `language_name.json`, e.g. `german.json`. Please make sure that the language name you are using matches the language full name in the `config.yaml` file, but in lowercase.
3. Rename the files in the copied folder to the desired language code so that instead of ending with `en`, they end with the desired language code, e.g. `de`.
4. In the `config.yaml` file, change the `language` and `full_language` to the desired language code and the full language name, respectively. Also change the `country_code` and the `lab_number` to the desired values. For example, for German data collected in University of Zurich at DiLi lab, which is the 2nd lab collecting MultipLEYE data in Switzerland, the settings would be:
```yaml
language: DE
full_language: German
country_code: CH
lab_number: 2
random_seed: 123
font: Segoe UI
```
5. If you want to run only some of the tests, change the corresponding values to `False` in the `config.yaml` file. For example, if you only want to run the WMC battery and the PLAB test throughout the whole experiment, the settings would be:
```yaml
wmc: True
ran: False
stroop_flanker: False
plab: True
wiki_vocab: False
```
6. Run the launcher:
```bash
python run_multipleye_psychometric_tests.py
```
7. In the GUI, enter or confirm participant metadata (`participant-id`, language, country code, lab number, and year). Then click `Start`.
8. Task visibility is controlled by `configs/config.yaml`:
- Tasks set to `True` are shown and can be deselected for an individual participant.
- Tasks set to `False` are hidden and cannot be selected at runtime.
9. If WMC is enabled, a second WMC window appears to select WMC subtasks.
10. Results are saved in:
```text
data/MultiplEYE_<LANG>_<COUNTRY>_<LAB>_<YEAR>/<PARTICIPANT>_<LANG>_<COUNTRY>_<LAB>_PT<SESSION>/
```
The participant-specific YAML config is also saved in the participant folder.

## Data Collection
1. When collecting data from each participant, please follow the [MultiplEYE Experimenter Script - Eye-Tracking Session](https://multipleye.eu/wp-content/uploads/MultiplEYE-Experimenter-Script-Eye-Tracking-Session.pdf) and [MultiplEYE Experimenter Script - Psychometric Tests Session](https://multipleye.eu/wp-content/uploads/MultiplEYE-Experimenter-Script-Psychometric-Tests-Session.pdf) and please always check the Participant ID and Session ID (if applicable) before starting the tests.
2. Upload the whole data folder as a zip/rar file to the MultipLEYE data repository for the corresponding lab.

## Repository Structure
```
├── .github                   <- Github Actions workflows
│
├── configs                   <- Configuration files
│   ├── config.yaml           <- Lab-level defaults (language, lab metadata, random seed, task toggles)
│   └── experiment.yaml       <- Runtime cache of arguments from the latest launcher run
│
├── data                      <- Runtime output folder (participant folders, task outputs, logs, configs)
│
├── languages                 <- Language-specific instructions, stimuli, and GUI translations
│
├── tasks                     <- Task implementations
│   ├── PLAB                  <- PLAB scripts and assets
│   ├── RAN                   <- RAN scripts and audio handling
│   ├── Stroop-Flanker        <- Stroop and Flanker scripts and stimuli readers
│   ├── WikiVocab             <- WikiVocab scripts (and LexTALE for supported languages)
│   ├── WMC                   <- WMC launcher/task scripts (OS-specific entry points)
│   └── __init__.py
│
├── run_multipleye_psychometric_tests.py <- Main launcher (GUI, participant folder setup, sequential task execution)
│
├── .gitignore                <- Git ignore rules
├── .project-root             <- Marker file used to infer repository root
├── requirements.txt          <- Python dependencies
└── README.md                 <- Project setup and usage documentation
```

### Directory guide

- `configs/`: edit this before data collection; `config.yaml` should stay stable within a lab/language study.
- `languages/`: translation workspace. Each language folder mirrors the task structure and includes UI text resources.
- `tasks/`: code for each psychometric task. Update this when changing task logic, stimuli loading, or task-specific outputs.
- `run_multipleye_psychometric_tests.py`: entrypoint used by experimenters; handles GUI input, task selection, and run order.
- `data/`: generated during execution. Keep participant outputs for upload/archiving, but avoid committing raw data to Git.

### Task folder guide

- `tasks/WMC/`: Lewandowsky WMC battery (Memory Update, Operation Span, Sentence Span, Spatial Short-Term Memory), with OS-specific launch scripts for macOS and Windows plus shared task/common modules.
- `tasks/RAN/`: Rapid Automatized Naming task, including task flow and audio recording handling.
- `tasks/Stroop-Flanker/`: Stroop and Flanker implementations, including trial generation/loading and response logging.
- `tasks/PLAB/`: PLAB task implementation and scoring/output logic used during test execution.
- `tasks/WikiVocab/`: WikiVocab/LexTALE app-style flow (welcome, item/table loading, result handling).
## Contact
Please contact [multipleye.project@gmail.com](mailto:multipleye.project@gmail.com) for more information.
