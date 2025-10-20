#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

import yaml
from gooey import Gooey, GooeyParser
from psychopy import core

from tasks.WMC.wmc_mac import run_wmc_mac

PARENT_FOLDER = Path(__file__).parent

# Path to the YAML file contains the language and experiment configurations
config_path = f'{PARENT_FOLDER}/configs/config.yaml'
experiment_config_path = f'{PARENT_FOLDER}/configs/experiment.yaml'

# Load the YAML file
with open(config_path, 'r', encoding="utf-8") as file:
    config_data = yaml.safe_load(file)
language = config_data['language']
full_language = config_data['full_language']
country_code = config_data['country_code']
lab_number = config_data['lab_number']
random_seed = config_data['random_seed']
wmc = config_data['wmc']
ran = config_data['ran']
stroop_flanker = config_data['stroop_flanker']
plab = config_data['plab']
wiki_vocab = config_data['wiki_vocab']

LANG_DIR = f'{PARENT_FOLDER}/languages/{language}/ui_data/interface_language/'
IMAGE_DIR = f'{PARENT_FOLDER}/languages/{language}/ui_data/interface_icons/'
if not os.path.exists(f'{LANG_DIR}/experiment_interface_{language.lower()}.json'):
    GUI_LANG = 'experiment_interface_en'
else:
    GUI_LANG = f'experiment_interface_{language.lower()}'

with open(f'{LANG_DIR}/{GUI_LANG}.json', 'r', encoding='utf-8') as translation_file:
    translations = json.load(translation_file)


@Gooey(
    language=GUI_LANG,
    program_name=translations['program_name'],
    program_description=translations['program_description'],
    image_dir=str(IMAGE_DIR),
    default_size=(900, 800),
    language_dir=str(LANG_DIR),
    show_preview_warning=False,
)
def parse_args():
    parser = GooeyParser(
        description=translations['parser_description'],
    )

    lab_settings = parser.add_argument_group(
        translations['lab_settings'],
        description=translations['lab_settings_desc'],
        # gooey_options={
        #     'show_underline': False,
        # },
    )
    lab_settings.add_argument(
        '--language',
        widget='TextField',
        metavar=translations['language'],
        help=translations['language_help'],
        default=language,
        required=True,
        gooey_options={'visible': True},
    )
    lab_settings.add_argument(
        '--full_language',
        widget='TextField',
        help=translations['full_language_help'],
        metavar=translations['full_language'],
        default=full_language,
        required=True,
        gooey_options={'visible': True},
    )
    lab_settings.add_argument(
        '--country_code',
        help=translations['country_code_help'],
        metavar=translations['country_code'],
        widget='TextField',
        default=country_code,
        required=True,
        gooey_options={'visible': True},
    )
    lab_settings.add_argument(
        '--lab_number',
        metavar=translations['lab_number'],
        help=translations['lab_number_help'],
        widget='TextField',
        default=1,
        type=int,
        required=True,
        gooey_options={'visible': True}
    )

    lab_settings.add_argument(
        '--year',
        metavar=translations['year'],
        help=translations['year_help'],
        widget='TextField',
        default=config_data['year'],
        type=int,
        required=True,
        gooey_options={'visible': True}
    )

    participants = parser.add_argument_group(translations['participants'])
    participants.add_argument(
        '--participant-id',
        metavar=translations['participant_id'],
        # default=1,
        type=int,
        widget='TextField',
        help=translations['participant_id_help'],
        required=True,
        gooey_options={'visible': True}
    )
    participants.add_argument(
        '--session-id',
        metavar=translations['session_id'],
        default=1,
        type=int,
        widget='TextField',
        help=translations['session_id_help'],
        required=True,
        gooey_options={'visible': False}
    )
    # participants.add_argument(
    #     '--random_seed',
    #     metavar='Random Seed',
    #     default=random_seed,
    #     type=int,
    #     widget='TextField',
    #     help='Random seed has to be a number between 1 and 9999.'
    #          'It is used to reproduce the same random sequence and numbers for the WMC and RAN experiments.'
    #          'If you want to change the random seed, please edit the config.yaml file in the configs folder.',
    #     required=True,
    #     gooey_options={'visible': True}
    # )
    # add an argument for each test. Tests are WMC, Peabody, PLAB, RAN, StroopFlanker
    tests = parser.add_argument_group('Psychometric Tests',
                                      description='If you want to change the tests that you want to run, please edit the config.yaml file in the configs folder.')
    # parser.set_defaults(ran=ran)
    # parser.set_defaults(stroop_flanker=stroop_flanker)
    # parser.set_defaults(plab=plab)
    # Main tests checkbox
    tests.add_argument(
        '--wmc',
        metavar=translations['wmc'],
        help=translations['wmc_help'],
        default=wmc,
        required=False,
        action='store_true' if not wmc else 'store_false',
        gooey_options={'visible': wmc}
    )

    tests.add_argument(
        '--ran',
        metavar=translations['ran'],
        help=translations['ran_help'],
        default=ran,
        required=False,
        action='store_true' if not ran else 'store_false',
        gooey_options={'visible': ran}
    )

    tests.add_argument(
        '--stroop_flanker',
        metavar=translations['stroop_flanker'],
        help=translations['stroop_flanker_help'],
        default=stroop_flanker,
        required=False,
        action='store_true' if not stroop_flanker else 'store_false',
        gooey_options={'visible': stroop_flanker}
    )
    tests.add_argument(
        '--plab',
        metavar=translations['plab'],
        help=translations['plab_help'],
        default=plab,
        required=False,
        action='store_true' if not plab else 'store_false',
        gooey_options={'visible': plab}
    )
    tests.add_argument(
        '--wiki_vocab',
        metavar=translations['wiki_vocab'],
        help=translations['wiki_vocab_help'],
        default=wiki_vocab,
        required=False,
        action='store_true' if not wiki_vocab else 'store_false',
        gooey_options={'visible': wiki_vocab}
    )
    args = vars(parser.parse_args())
    print(args)
    return args


def run_script(script_path, part_folder=None):
         
    result = subprocess.run(
        [sys.executable, script_path, '--participant_folder', part_folder], 
        check=True, 
        text=True, 
        capture_output=False,
        cwd=script_dir  # Set working directory to project root
    )
    print("Output:", result.stdout)
    print("Errors:", result.stderr)




if __name__ == '__main__':
    system = platform.system()

    arguments = parse_args()
    arguments['system'] = system

    data_collection_folder = f'{PARENT_FOLDER}/data/MultiplEYE_{arguments["language"].upper()}_{arguments["country_code"].upper()}_{arguments["lab_number"]}_{arguments["year"]}'
    participant_folder = (f'{data_collection_folder}/{arguments["participant_id"]:03}_{arguments["language"].upper()}_'
                          f'{arguments["country_code"].upper()}_{arguments["lab_number"]}_PT{arguments["session_id"]}/')

    participant_folder_relative = (f'MultiplEYE_{arguments["language"].upper()}_{arguments["country_code"].upper()}_{arguments["lab_number"]}_{arguments["year"]}/{arguments["participant_id"]:03}_{arguments["language"].upper()}_'
                                f'{arguments["country_code"].upper()}_{arguments["lab_number"]}_PT{arguments["session_id"]}/')


    os.makedirs(participant_folder, exist_ok=True)
    participant_config_path = f'{participant_folder}/' \
                              f'{arguments["participant_id"]:03}_{arguments["language"].upper()}_{arguments["country_code"].upper()}' \
                              f'_{arguments["lab_number"]}_PT{arguments["session_id"]}.yaml'

    with open(experiment_config_path, 'w', encoding='utf-8') as file:  # cache the arguments
        yaml.dump(arguments, file)

    path_to_tasks = os.path.abspath('tasks/')
    sys.path.insert(0, path_to_tasks)  # Add tasks directory to Python path

    # this is some work around to make sure that the arguments are set correctly.
    # see https://github.com/chriskiehl/Gooey/issues/148
    arguments['wmc'] = not arguments['wmc']
    arguments['ran'] = not arguments['ran']
    arguments['stroop_flanker'] = not arguments['stroop_flanker']
    arguments['plab'] = not arguments['plab']
    arguments['wiki_vocab'] = not arguments['wiki_vocab']

    # save the random seed used for the participant
    arguments['random_seed'] = random_seed

    with open(participant_config_path, 'w') as file:
        yaml.dump(arguments, file)

    if arguments['wmc']:
        print("Running WMC")
        if system == 'Windows':
            print("Running WMC on Windows")
            run_script('tasks/WMC/wmc_windows.py', participant_folder_relative)
        elif system == 'Linux':
            print("Running WMC on Linux")
            run_script('tasks/WMC/wmc_linux.py', participant_folder_relative)
        else:
            print("Running WMC on Mac")
            run_wmc_mac(result_folder=participant_folder_relative)
        arguments['run_wmc'] = 'success'

        with open(participant_config_path, 'w') as file:
            yaml.dump(arguments, file)

    if arguments['ran']:
        print("Running RAN")
        run_script('tasks/RAN/ran_task.py', part_folder=participant_folder_relative)
        arguments['run_ran'] = 'success'

        with open(participant_config_path, 'w') as file:
            yaml.dump(arguments, file)

    if arguments['stroop_flanker']:
        print("Running Stroop Flanker")
        run_script('tasks/Stroop-Flanker/stroop_flanker.py', part_folder=participant_folder_relative)
        arguments['run_stroop_flanker'] = 'success'

        with open(participant_config_path, 'w') as file:
            yaml.dump(arguments, file)

    if arguments['plab']:
        print("Running PLAB")
        run_script('tasks/PLAB/plab.py', participant_folder_relative)
        arguments['run_plab'] = 'success'

        with open(participant_config_path, 'w') as file:
            yaml.dump(arguments, file)

    if arguments['wiki_vocab']:
        print("Running WikiVocab")
        run_script('tasks/WikiVocab/app.py', participant_folder_relative)
        arguments['run_wiki_vocab'] = 'success'

        with open(participant_config_path, 'w') as file:
            yaml.dump(arguments, file)

    with open(participant_config_path, 'w') as file:
        yaml.dump(arguments, file)

    core.quit()
