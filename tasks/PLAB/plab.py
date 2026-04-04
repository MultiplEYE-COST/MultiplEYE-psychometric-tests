"""
PLAB (Language Analysis) Task - PsychoPy implementation.
This is a custom implementation based on the paper-and-pencil PLAB test.
The original test materials were adapted from a PowerPoint template,
converted to screenshots, and presented as visual stimuli.
Copyright (C) 2024-2026 MultiplEYE Project
"""

from __future__ import absolute_import, division

import argparse
import os
import re
from datetime import datetime

import pandas as pd
import yaml
import unicodedata
from psychopy import visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, FINISHED)
from psychopy.hardware import keyboard

# Strongly recommended for Arabic/Persian/RTL rendering
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_RTL_SUPPORT = True
except ImportError:
    HAS_RTL_SUPPORT = False


date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run the PLAB task.")
parser.add_argument('--participant_folder', type=str, required=True, help="Path to the participant folder.")
args = parser.parse_args()
results_folder = args.participant_folder

# Path to the YAML file contains the language and experiment configurations
config_path = 'configs/config.yaml'
experiment_config_path = 'configs/experiment.yaml'

# Load the YAML file
with open(config_path, 'r', encoding="utf-8") as file:
    config_data = yaml.safe_load(file)

language = config_data['language']
country_code = config_data['country_code']
lab_number = config_data['lab_number']
random_seed = config_data['random_seed']
font = config_data['font']

RTL_LANGS = {'fa', 'fas', 'ar', 'he', 'ur'}
is_rtl = str(language).lower() in RTL_LANGS

# Directional marks for stabilizing mixed LTR/RTL text
LRM = "\u200E"   # left-to-right mark

if os.path.exists(experiment_config_path):
    # Load the experiment configuration if the file exists
    with open(experiment_config_path, 'r', encoding="utf-8") as file:
        expInfo = yaml.safe_load(file)
        participant_id_str = str(expInfo['participant_id'])
        while len(participant_id_str) < 3:
            participant_id_str = "0" + participant_id_str
        participant_id = participant_id_str
else:
    # Set default values if the file does not exist
    expInfo = {'participant_id': 999, 'session_id': 2}
    participant_id = "999"


def normalize_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = text.replace('\\n', '\n')
    text = unicodedata.normalize('NFC', text)
    return text


def clean_ltr_text(text):
    text = text.replace('\u200c', '')
    text = ''.join(ch for ch in text if not unicodedata.combining(ch))
    return text


def prepare_general_text(text):
    """
    For welcome/instructions/done/goodbye text.
    """
    text = normalize_text(text)

    if not is_rtl:
        return clean_ltr_text(text)

    # For RTL text do not aggressively strip joiners/marks
    if HAS_RTL_SUPPORT:
        lines = text.split('\n')
        shaped_lines = []
        for line in lines:
            reshaped = arabic_reshaper.reshape(line)
            shaped_lines.append(get_display(reshaped))
        return '\n'.join(shaped_lines)

    return text


def prepare_option_or_question_text(text):
    """
    Prepare a single question/option text fragment.
    """
    text = normalize_text(text)

    if not is_rtl:
        return clean_ltr_text(text)

    if HAS_RTL_SUPPORT:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    return text
    

def make_option_line(option_text):
    """
    Keep the option line exactly as provided in Excel, including [1], [2], etc.
    For RTL, stabilize bracket/number rendering with LRM marks.
    """
    option_text = normalize_text(option_text)

    if not is_rtl:
        return clean_ltr_text(option_text)

    if HAS_RTL_SUPPORT:
        # Stabilize labels like [1], [2] inside RTL text
        option_text = re.sub(r'\[([0-9۰-۹]+)\]', rf'{LRM}[\1]{LRM}', option_text)
        reshaped = arabic_reshaper.reshape(option_text)
        return get_display(reshaped)

    return option_text



def make_question_block(question, options):
    question = prepare_option_or_question_text(question)

    lines = [
        question,
        "",
        make_option_line(options[0]),
        make_option_line(options[1]),
        make_option_line(options[2]),
        make_option_line(options[3]),
    ]
    return "\n".join(lines)


# Store info about the experiment session
psychopyVersion = '2025.1.1'
expName = 'PLAB'  # from the Builder filename that created this script

# Create folder for audio and csv data
output_path = f'data/{results_folder}/PLAB/'
os.makedirs(output_path, exist_ok=True)

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = (
    f"{output_path}"
    f"{language}{country_code}{lab_number}"
    f"_{participant_id}_PT{expInfo['session_id']}_{date}"
)

instructions_df = pd.read_excel(
    f'languages/{language}/instructions/PLAB_instructions_{language.lower()}.xlsx',
    index_col='screen'
)

welcome_text = prepare_general_text(instructions_df.loc['Welcome_text', language])
done_text_str = prepare_general_text(instructions_df.loc['done_text', language])
Goodbyetext_str = prepare_general_text(instructions_df.loc['Goodbye_text', language])
PLAB_instructions_str = prepare_general_text(instructions_df.loc['PLAB_instructions', language])

language_style = 'RTL' if is_rtl else 'LTR'
display_font = font

# For RTL task text only, use centered layout.
# For LTR, keep original layout behavior.
task_text_align = 'center' if is_rtl else None
task_anchor_horiz = 'center' if is_rtl else None
task_text_x_pos = 0.0
rect_x = 0.0

task1_img = f'languages/{language}/PLAB/Plab_part4_task1_{language.lower()}.png'
task2_img = f'languages/{language}/PLAB/Plab_part4_task2_{language.lower()}.png'
PlabStim = f'languages/{language}/PLAB/PlabStim_{language.lower()}.xlsx'

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(
    name='PLAB', version='',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename
)

# save a log file for detail verbose info
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Setup the Window
win = visual.Window(
    size=[1440, 900], fullscr=True, screen=0,
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color='white', colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height'
)

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] is not None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "Blank500"
Blank500Clock = core.Clock()
blank = visual.TextStim(
    win=win, name='blank',
    text='\n\n',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
    color='black', colorSpace='rgb', opacity=None,
    languageStyle=language_style,
    depth=0.0
)

# Initialize components for Routine "FixationCross"
FixationCrossClock = core.Clock()
fix_cross = visual.TextStim(
    win=win, name='fix_cross',
    text='+',
    font='Courier New',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
    color='black', colorSpace='rgb', opacity=None,
    languageStyle=language_style,
    depth=0.0
)

# Initialize components for Routine "Done"
DoneClock = core.Clock()
done_text = visual.TextStim(
    win=win, name='done_text',
    text=done_text_str,
    font=display_font,
    pos=(0, 0), height=0.035, wrapWidth=None, ori=0.0,
    color='black', colorSpace='rgb', opacity=None,
    languageStyle=language_style,
    depth=0.0
)
done_key = keyboard.Keyboard()

# Initialize components for Routine "PLABInstruction"
PLABInstructionClock = core.Clock()
PLAB_instructions = visual.TextStim(
    win=win, name='PLAB_instructions',
    text=PLAB_instructions_str,
    font=display_font,
    pos=(0, 0), height=0.03, wrapWidth=1.3, ori=0.0,
    color='black', colorSpace='rgb', opacity=None,
    languageStyle=language_style,
    depth=0.0
)
PLAB_instruction_key = keyboard.Keyboard()

# Initialize components for Routine "PLAB Task1 Trials"
PLABTask1Clock = core.Clock()
PLAB_pics_1 = visual.ImageStim(
    win=win,
    name='plab_task1',
    image=task1_img,
    pos=(0, 0.18),  # 0.18 is the vertical position of the image from the center
    size=(1.5, 0.6),  # 1.5 is the width of the image, 0.6 is the height of the image
    color=[1, 1, 1], colorSpace='rgb',
    ori=0.0,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=False
)

if is_rtl:
    PLAB_task1 = visual.TextStim(
        win=win, name='PLAB_task1',
        text='',
        font=display_font,
        pos=(task_text_x_pos, -0.28), height=0.035, wrapWidth=1.2, ori=0.0,
        color='black', colorSpace='rgb', opacity=None,
        languageStyle=language_style,
        alignText=task_text_align,
        anchorHoriz=task_anchor_horiz,
        depth=0.0
    )
else:
    PLAB_task1 = visual.TextStim(
        win=win, name='PLAB_task1',
        text='',
        font=display_font,
        pos=(0, -0.28), height=0.035, wrapWidth=None, ori=0.0,
        color='black', colorSpace='rgb', opacity=None,
        languageStyle=language_style,
        depth=0.0
    )

PLAB_task1_key = keyboard.Keyboard()

# Rectangles for highlighting options
highlight_rects = []
option_positions = [
    (rect_x, -0.26),
    (rect_x, -0.31),
    (rect_x, -0.35),
    (rect_x, -0.40)
]
for pos in option_positions:
    rect = visual.Rect(
        win=win,
        width=0.8, height=0.035,
        pos=pos,
        lineColor='red',
        lineWidth=2,
        fillColor=None
    )
    highlight_rects.append(rect)

# Initialize components for Routine "PLAB Task2 Trials"
PLABTask2Clock = core.Clock()
PLAB_pics_2 = visual.ImageStim(
    win=win,
    name='plab_task2',
    image=task2_img,
    pos=(0, 0.18),
    size=(1.5, 0.6),
    color=[1, 1, 1], colorSpace='rgb',
    ori=0.0,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=False
)

if is_rtl:
    PLAB_task2 = visual.TextStim(
        win=win, name='PLAB_task2',
        text='',
        font=display_font,
        pos=(task_text_x_pos, -0.28), height=0.035, wrapWidth=1.2, ori=0.0,
        color='black', colorSpace='rgb', opacity=None,
        languageStyle=language_style,
        alignText=task_text_align,
        anchorHoriz=task_anchor_horiz,
        depth=0.0
    )
else:
    PLAB_task2 = visual.TextStim(
        win=win, name='PLAB_task2',
        text='',
        font=display_font,
        pos=(0, -0.28), height=0.035, wrapWidth=None, ori=0.0,
        color='black', colorSpace='rgb', opacity=None,
        languageStyle=language_style,
        depth=0.0
    )

PLAB_task2_key = keyboard.Keyboard()

# Initialize components for Routine "GoodbyeScreen"
GoodbyeScreenClock = core.Clock()
Goodbyetext = visual.TextStim(
    win=win, name='Goodbyetext',
    text=Goodbyetext_str,
    font=display_font,
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0,
    color='black', colorSpace='rgb', opacity=None,
    languageStyle=language_style,
    depth=0.0
)
key_goodbye = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# Display welcome message
welcome_stim = visual.TextStim(
    win=win,
    text=welcome_text,
    alignHoriz='center',
    alignVert='center',
    font=display_font,
    pos=(0, 0),
    height=0.05,
    ori=0.0,
    color='black',
    colorSpace='rgb',
    opacity=None,
    languageStyle=language_style,
    depth=0.0
)
welcome_stim.draw()
win.flip()
event.waitKeys()

# ------Prepare to start Routine "PLABInstruction"-------
continueRoutine = True
PLAB_instruction_key.keys = []
PLAB_instruction_key.rt = []
_PLAB_instruction_key_allKeys = []

PLABInstructionComponents = [PLAB_instructions, PLAB_instruction_key]
for thisComponent in PLABInstructionComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
PLABInstructionClock.reset(-_timeToFirstFrame)
frameN = -1

# -------Run Routine "PLABInstruction"-------
while continueRoutine:
    t = PLABInstructionClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=PLABInstructionClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1

    if PLAB_instructions.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        PLAB_instructions.frameNStart = frameN
        PLAB_instructions.tStart = t
        PLAB_instructions.tStartRefresh = tThisFlipGlobal
        win.timeOnFlip(PLAB_instructions, 'tStartRefresh')
        PLAB_instructions.setAutoDraw(True)

    waitOnFlip = False
    if PLAB_instruction_key.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        PLAB_instruction_key.frameNStart = frameN
        PLAB_instruction_key.tStart = t
        PLAB_instruction_key.tStartRefresh = tThisFlipGlobal
        win.timeOnFlip(PLAB_instruction_key, 'tStartRefresh')
        PLAB_instruction_key.status = STARTED
        waitOnFlip = True
        win.callOnFlip(PLAB_instruction_key.clock.reset)
        win.callOnFlip(PLAB_instruction_key.clearEvents, eventType='keyboard')

    if PLAB_instruction_key.status == STARTED and not waitOnFlip:
        theseKeys = PLAB_instruction_key.getKeys(keyList=['space'], waitRelease=False)
        _PLAB_instruction_key_allKeys.extend(theseKeys)
        if len(_PLAB_instruction_key_allKeys):
            PLAB_instruction_key.keys = _PLAB_instruction_key_allKeys[-1].name
            PLAB_instruction_key.rt = _PLAB_instruction_key_allKeys[-1].rt
            continueRoutine = False

    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

    if not continueRoutine:
        break

    continueRoutine = False
    for thisComponent in PLABInstructionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break

    if continueRoutine:
        win.flip()

# -------Ending Routine "PLABInstruction"-------
for thisComponent in PLABInstructionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('PLAB_instructions.started', PLAB_instructions.tStartRefresh)
thisExp.addData('PLAB_instructions.stopped', PLAB_instructions.tStopRefresh)

if PLAB_instruction_key.keys in ['', [], None]:
    PLAB_instruction_key.keys = None
thisExp.addData('PLAB_instruction_key.keys', PLAB_instruction_key.keys)
if PLAB_instruction_key.keys is not None:
    thisExp.addData('PLAB_instruction_key.rt', PLAB_instruction_key.rt)
thisExp.addData('PLAB_instruction_key.started', PLAB_instruction_key.tStartRefresh)
thisExp.addData('PLAB_instruction_key.stopped', PLAB_instruction_key.tStopRefresh)
thisExp.nextEntry()
routineTimer.reset()

# ------Prepare to start Routine "Blank500"-------
continueRoutine = True
routineTimer.addTime(0.500000)

Blank500Components = [blank]
for thisComponent in Blank500Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Blank500Clock.reset(-_timeToFirstFrame)
frameN = -1

# -------Run Routine "Blank500"-------
while continueRoutine and routineTimer.getTime() > 0:
    t = Blank500Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Blank500Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1

    if blank.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        blank.frameNStart = frameN
        blank.tStart = t
        blank.tStartRefresh = tThisFlipGlobal
        win.timeOnFlip(blank, 'tStartRefresh')
        blank.setAutoDraw(True)
    if blank.status == STARTED:
        if tThisFlipGlobal > blank.tStartRefresh + .5 - frameTolerance:
            blank.tStop = t
            blank.frameNStop = frameN
            win.timeOnFlip(blank, 'tStopRefresh')
            blank.setAutoDraw(False)

    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

    if not continueRoutine:
        break

    continueRoutine = False
    for thisComponent in Blank500Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break

    if continueRoutine:
        win.flip()

# -------Ending Routine "Blank500"-------
for thisComponent in Blank500Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('blank.started', blank.tStartRefresh)
thisExp.addData('blank.stopped', blank.tStopRefresh)

full_trial_list = data.importConditions(PlabStim)

# task1 contains the first 4 rows of the trial list
PLAB_task1_list = full_trial_list[:4]

# task2 contains the rest rows of the trial list
PLAB_task2_list = full_trial_list[4:]

# set up handler to look after randomisation of conditions etc
PLAB_task1_trials = data.TrialHandler(
    nReps=1.0, method='sequential',
    trialList=PLAB_task1_list,
    seed=random_seed, name='PLAB_task1_trials'
)
thisExp.addLoop(PLAB_task1_trials)

mouse = event.Mouse(win=win)
continueRoutine = True
routineTimer = core.CountdownTimer()

for thisPLAB_task1_trial in PLAB_task1_trials:
    valid_answer = False
    chosen_key = None
    currentLoop = PLAB_task1_trials
    question_id = thisPLAB_task1_trial['question_id']
    question = thisPLAB_task1_trial['question']
    options = (
        thisPLAB_task1_trial['option_a'],
        thisPLAB_task1_trial['option_b'],
        thisPLAB_task1_trial['option_c'],
        thisPLAB_task1_trial['option_d']
    )
    correct_key = thisPLAB_task1_trial['correct_key']
    display_text = make_question_block(question, options)

    # ------Prepare to start Routine "PLAB Task1 Trials"-------
    continueRoutine = True
    PLAB_task1.setText(display_text)
    PLAB_task1_Components = [PLAB_task1] + highlight_rects

    # Reset keyboard
    PLAB_task1_key.keys = []
    PLAB_task1_key.rt = []
    _PLAB_task1_key_allKeys = []
    PLAB_task1_key.clock.reset()
    PLAB_task1_key.clearEvents()
    task_start_time = globalClock.getTime()

    # -------Run Routine "PLAB Task1 Trials"-------
    while continueRoutine:
        PLAB_pics_1.draw()
        PLAB_task1.draw()

        for rect in highlight_rects:
            if rect.autoDraw:
                rect.draw()

        theseKeys = PLAB_task1_key.getKeys(
            keyList=['1', '2', '3', '4', 'space', 'escape'],
            waitRelease=False
        )

        for key in theseKeys:
            if key.name in ['1', '2', '3', '4']:
                valid_answer = True
                chosen_key = key.name

                # Highlight the selected option
                selected_option_index = int(key.name) - 1
                for i, rect in enumerate(highlight_rects):
                    if i == selected_option_index:
                        rect.setAutoDraw(True)
                    else:
                        rect.setAutoDraw(False)

            if key.name == 'space' and valid_answer:
                PLAB_task1_key.keys = chosen_key
                PLAB_task1_key.rt = globalClock.getTime() - task_start_time

                PLAB_task1.setAutoDraw(False)
                for rect in highlight_rects:
                    rect.setAutoDraw(False)

                continueRoutine = False
                break

            if key.name == 'escape':
                core.quit()

        if not continueRoutine:
            break

        continueRoutine = False
        for thisComponent in PLAB_task1_Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break

        if continueRoutine:
            win.flip()

    # -------Ending Routine "PLAB Task1 Trials"-------
    if PLAB_task1_key.keys in ['', [], None]:
        PLAB_task1_key.keys = None
        PLAB_task1_key.corr = int(str(correct_key).lower() == 'none')
    else:
        PLAB_task1_key.corr = int(PLAB_task1_key.keys == str(correct_key))

    # Save trial data
    thisExp.addData('task', 'task1')
    thisExp.addData('question_id', question_id)
    thisExp.addData('chosen_key', PLAB_task1_key.keys)
    thisExp.addData('correctness', PLAB_task1_key.corr)
    thisExp.addData('rt', PLAB_task1_key.rt)

    routineTimer.reset()
    thisExp.nextEntry()

    # Add a fixation screen between trials
    continueRoutine = True
    fix_cross.tStart = None
    fix_cross.tStop = None
    fix_cross.tStartRefresh = None
    fix_cross.tStopRefresh = None
    routineTimer.reset()
    routineTimer.addTime(0.5)

    while continueRoutine and routineTimer.getTime() > 0:
        fix_cross.draw()
        win.flip()
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

# completed 'PLAB task 1 trials'

# set up handler to look after randomisation of conditions etc
PLAB_task2_trials = data.TrialHandler(
    nReps=1.0, method='sequential',
    trialList=PLAB_task2_list,
    seed=random_seed, name='PLAB_task2_trials'
)
thisExp.addLoop(PLAB_task2_trials)

for thisPLAB_task2_trial in PLAB_task2_trials:
    valid_answer = False
    chosen_key = None
    currentLoop = PLAB_task2_trials
    question_id = thisPLAB_task2_trial['question_id']
    question = thisPLAB_task2_trial['question']
    options = (
        thisPLAB_task2_trial['option_a'],
        thisPLAB_task2_trial['option_b'],
        thisPLAB_task2_trial['option_c'],
        thisPLAB_task2_trial['option_d']
    )
    correct_key = thisPLAB_task2_trial['correct_key']
    display_text = make_question_block(question, options)

    # ------Prepare to start Routine "PLAB Task2 Trials"-------
    continueRoutine = True
    PLAB_task2.setText(display_text)
    PLAB_task2_Components = [PLAB_task2] + highlight_rects

    # Reset keyboard
    PLAB_task2_key.keys = []
    PLAB_task2_key.rt = []
    _PLAB_task2_key_allKeys = []
    PLAB_task2_key.clock.reset()
    PLAB_task2_key.clearEvents()
    task_start_time = globalClock.getTime()

    # -------Run Routine "PLAB Task2 Trials"-------
    while continueRoutine:
        PLAB_pics_2.draw()
        PLAB_task2.draw()

        for rect in highlight_rects:
            if rect.autoDraw:
                rect.draw()

        theseKeys = PLAB_task2_key.getKeys(
            keyList=['1', '2', '3', '4', 'space', 'escape'],
            waitRelease=False
        )

        for key in theseKeys:
            if key.name in ['1', '2', '3', '4']:
                valid_answer = True
                chosen_key = key.name

                # Highlight the selected option
                selected_option_index = int(key.name) - 1
                for i, rect in enumerate(highlight_rects):
                    if i == selected_option_index:
                        rect.setAutoDraw(True)
                    else:
                        rect.setAutoDraw(False)

            if key.name == 'space' and valid_answer:
                PLAB_task2_key.keys = chosen_key
                PLAB_task2_key.rt = globalClock.getTime() - task_start_time

                PLAB_task2.setAutoDraw(False)
                for rect in highlight_rects:
                    rect.setAutoDraw(False)

                continueRoutine = False
                break

            if key.name == 'escape':
                core.quit()

        if not continueRoutine:
            break

        continueRoutine = False
        for thisComponent in PLAB_task2_Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break

        if continueRoutine:
            win.flip()

    # -------Ending Routine "PLAB Task2 Trials"-------
    if PLAB_task2_key.keys in ['', [], None]:
        PLAB_task2_key.keys = None
        PLAB_task2_key.corr = int(str(correct_key).lower() == 'none')
    else:
        PLAB_task2_key.corr = int(PLAB_task2_key.keys == str(correct_key))

    # Save trial data
    thisExp.addData('task', 'task2')
    thisExp.addData('question_id', question_id)
    thisExp.addData('chosen_key', PLAB_task2_key.keys)
    thisExp.addData('correctness', PLAB_task2_key.corr)
    thisExp.addData('rt', PLAB_task2_key.rt)

    routineTimer.reset()
    thisExp.nextEntry()

    # Add a fixation screen between trials
    continueRoutine = True
    fix_cross.tStart = None
    fix_cross.tStop = None
    fix_cross.tStartRefresh = None
    fix_cross.tStopRefresh = None
    routineTimer.reset()
    routineTimer.addTime(0.5)

    while continueRoutine and routineTimer.getTime() > 0:
        fix_cross.draw()
        win.flip()
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

# completed 'PLAB Task2 trials'

# ------Prepare to start Routine "Done"-------
continueRoutine = True
done_key.keys = []
done_key.rt = []
_done_key_allKeys = []

DoneComponents = [done_text, done_key]
for thisComponent in DoneComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
DoneClock.reset(-_timeToFirstFrame)
frameN = -1

# -------Run Routine "Done"-------
while continueRoutine:
    t = DoneClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=DoneClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1

    if done_text.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        done_text.frameNStart = frameN
        done_text.tStart = t
        done_text.tStartRefresh = tThisFlipGlobal
        win.timeOnFlip(done_text, 'tStartRefresh')
        done_text.setAutoDraw(True)

    waitOnFlip = False
    if done_key.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        done_key.frameNStart = frameN
        done_key.tStart = t
        done_key.tStartRefresh = tThisFlipGlobal
        win.timeOnFlip(done_key, 'tStartRefresh')
        done_key.status = STARTED
        waitOnFlip = True
        win.callOnFlip(done_key.clock.reset)
        win.callOnFlip(done_key.clearEvents, eventType='keyboard')

    if done_key.status == STARTED and not waitOnFlip:
        theseKeys = done_key.getKeys(keyList=['space'], waitRelease=False)
        _done_key_allKeys.extend(theseKeys)
        if len(_done_key_allKeys):
            done_key.keys = _done_key_allKeys[-1].name
            done_key.rt = _done_key_allKeys[-1].rt
            continueRoutine = False

    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

    if not continueRoutine:
        break

    continueRoutine = False
    for thisComponent in DoneComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break

    if continueRoutine:
        win.flip()

# -------Ending Routine "Done"-------
for thisComponent in DoneComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('done_text.started', done_text.tStartRefresh)
thisExp.addData('done_text.stopped', done_text.tStopRefresh)

if done_key.keys in ['', [], None]:
    done_key.keys = None
thisExp.addData('done_key.keys', done_key.keys)
if done_key.keys is not None:
    thisExp.addData('done_key.rt', done_key.rt)
thisExp.addData('done_key.started', done_key.tStartRefresh)
thisExp.addData('done_key.stopped', done_key.tStopRefresh)
thisExp.nextEntry()

routineTimer.reset()

# ------Prepare to start Routine "GoodbyeScreen"-------
continueRoutine = True
routineTimer.addTime(10.000000)
key_goodbye.keys = []
key_goodbye.rt = []
_key_goodbye_allKeys = []

GoodbyeScreenComponents = [Goodbyetext, key_goodbye]
for thisComponent in GoodbyeScreenComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
GoodbyeScreenClock.reset(-_timeToFirstFrame)
frameN = -1

# -------Run Routine "GoodbyeScreen"-------
while continueRoutine and routineTimer.getTime() > 0:
    t = GoodbyeScreenClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=GoodbyeScreenClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1

    if Goodbyetext.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        Goodbyetext.frameNStart = frameN
        Goodbyetext.tStart = t
        Goodbyetext.tStartRefresh = tThisFlipGlobal
        win.timeOnFlip(Goodbyetext, 'tStartRefresh')
        Goodbyetext.setAutoDraw(True)
    if Goodbyetext.status == STARTED:
        if tThisFlipGlobal > Goodbyetext.tStartRefresh + 10 - frameTolerance:
            Goodbyetext.tStop = t
            Goodbyetext.frameNStop = frameN
            win.timeOnFlip(Goodbyetext, 'tStopRefresh')
            Goodbyetext.setAutoDraw(False)

    waitOnFlip = False
    if key_goodbye.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        key_goodbye.frameNStart = frameN
        key_goodbye.tStart = t
        key_goodbye.tStartRefresh = tThisFlipGlobal
        win.timeOnFlip(key_goodbye, 'tStartRefresh')
        key_goodbye.status = STARTED
        waitOnFlip = True
        win.callOnFlip(key_goodbye.clock.reset)
        win.callOnFlip(key_goodbye.clearEvents, eventType='keyboard')
    if key_goodbye.status == STARTED:
        if tThisFlipGlobal > key_goodbye.tStartRefresh + 10 - frameTolerance:
            key_goodbye.tStop = t
            key_goodbye.frameNStop = frameN
            win.timeOnFlip(key_goodbye, 'tStopRefresh')
            key_goodbye.status = FINISHED
    if key_goodbye.status == STARTED and not waitOnFlip:
        theseKeys = key_goodbye.getKeys(keyList=['space'], waitRelease=False)
        _key_goodbye_allKeys.extend(theseKeys)
        if len(_key_goodbye_allKeys):
            key_goodbye.keys = _key_goodbye_allKeys[-1].name
            key_goodbye.rt = _key_goodbye_allKeys[-1].rt
            continueRoutine = False

    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

    if not continueRoutine:
        break

    continueRoutine = False
    for thisComponent in GoodbyeScreenComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break

    if continueRoutine:
        win.flip()

# -------Ending Routine "GoodbyeScreen"-------
for thisComponent in GoodbyeScreenComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('Goodbyetext.started', Goodbyetext.tStartRefresh)
thisExp.addData('Goodbyetext.stopped', Goodbyetext.tStopRefresh)

if key_goodbye.keys in ['', [], None]:
    key_goodbye.keys = None
thisExp.addData('key_goodbye.keys', key_goodbye.keys)
if key_goodbye.keys is not None:
    thisExp.addData('key_goodbye.rt', key_goodbye.rt)
thisExp.addData('key_goodbye.started', key_goodbye.tStartRefresh)
thisExp.addData('key_goodbye.stopped', key_goodbye.tStopRefresh)
thisExp.nextEntry()

# Flip one final time so any remaining win.callOnFlip()
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename + '.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()

# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
# core.quit()