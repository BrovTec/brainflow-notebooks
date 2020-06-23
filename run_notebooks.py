import os
from eegnb.devices.eeg import EEG
from eegnb.experiments.visual_n170 import n170
from eegnb.experiments.visual_p300 import p300
from eegnb.experiments.visual_ssvep import ssvep


def generate_save_fn(board_name, experiment, subject_id):
    '''Generates a file name with the proper trial number for the current subject/experiment combo'''
    data_dir = os.path.join('data', experiment)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    # Check currently existing files to iterate to most recent trial number for the session/subject
    trial_num = 0
    file_name = f"{subject_id}_TRIAL_{trial_num}_{board_name}.csv"
    save_fp = os.path.join(data_dir, file_name)
    while os.path.exists(save_fp):
        trial_num += 1
        file_name = f"{subject_id}_TRIAL_{trial_num}_{board_name}.csv"
        save_fp = os.path.join(data_dir, file_name)

    return save_fp


def intro_prompt():
    boards = [
        'None', 'Muse', 'OpenBCI Ganglion', 'OpenBCI Cyton',
        'OpenBCI Cyton + Daisy', 'G.Tec Unicorn', 'BrainBit', 'Synthetic'
    ]

    board_codes = [
        'none', 'muse', 'ganglion', 'cyton', 'cyton_daisy', 'unicorn', 'brainbit', 'synthetic'
    ]

    open_bci_list = ['cyton', 'cyton_daisy', 'ganglion']

    experiments = ['visual_n170', 'visual_p300', 'visual_ssvep']

    print("Welcome to NeurotechX EEG Notebooks. \n"
          "Please select enter the integer value corresponding to your EEG device: \n"
          f"[0] {boards[0]} \n"
          f"[1] {boards[1]} \n"
          f"[2] {boards[2]} \n"
          f"[3] {boards[3]} \n"
          f"[4] {boards[4]} \n"
          f"[5] {boards[5]} \n"
          f"[6] {boards[6]} \n"
          f"[7] {boards[7]} \n")

    board_idx = int(input('Enter Board Selection:'))
    board_selection = board_codes[board_idx]
    print(f"Selected board {boards[board_idx]} \n")

    # Handles wifi shield connectivity selection if an OpenBCI board is being used
    if board_selection in open_bci_list:
        print("Please select your connection method:\n"
              "[0] usb dongle \n"
              "[1] wifi shield \n")
        connect_idx = input("Enter connection method:")
        if connect_idx == 1:
            board_selection = board_selection + "_wifi"

    # Experiment selection
    print("Please select which experiment you would like to run: \n"
          "[0] visual n170 \n"
          "[1] visual p300 \n"
          "[2] ssvep \n")

    exp_idx = int(input('Enter Experiment Selection:'))
    exp_selection = experiments[exp_idx]
    print(f"Selected experiment {exp_selection} \n")

    # record duration
    print("Now, enter the duration of the recording (in seconds). \n")
    duration = int(input("Enter duration:"))

    # Subject ID/Name specification
    print("Finally, enter the name/ID of the subject you are recording data from. \n")
    subj_id = input("Enter subject name/ID:")

    return board_selection, exp_selection, duration, subj_id

if __name__=="__main__":
    board_name, experiment, record_duration, subject = intro_prompt()


    # Create save file name
    save_fn = generate_save_fn(board_name, experiment, subject)
    print(save_fn)

    # Start EEG device
    eeg_device = EEG(device=board_name)

    # run experiment
    if experiment == 'visual_n170':
        n170.present(duration=record_duration, eeg=eeg_device, save_fn=save_fn)
    elif experiment == 'visual_p300':
        p300.present(duration=record_duration, eeg=eeg_device, save_fn=save_fn)
    elif experiment == 'ssvep':
        ssvep.present(duration=record_duration, eeg=eeg_device, save_fn=save_fn)

