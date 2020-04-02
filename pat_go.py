"""
using python2.7 from an anaconda environment, on windows 7
"""

import os
import random
import datetime
import subprocess
# import gc
import pandas as pd
from soa_helpers import get_response_for_ibi
from psychopy import visual, event
from psychopy import prefs, monitors, gui
# logging.console.setLevel(logging.DEBUG)  # get messages about the sound lib as it loads
prefs.hardware['audioLib'] = ['pygame']
from psychopy import sound, core, logging
# print('Using %s (with %s) for sounds' % (sound.audioLib, sound.audioDriver))

# create the tone
s = sound.Sound(800, secs=0.15, sampleRate=44100, stereo=True)
s.setVolume(0.3)

# get a date time stamp
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H%M')

# gui
myDlg = gui.Dlg(title="PAT")
myDlg.addField('Participant Number:', 999)
myDlg.addField('Practice or Experimental?:', choices=["Practice", "Experimental"])
myDlg.addField("Which monitor?", choices=["eeg", "e330"])
myDlg.addField('Autopilot?', initial=False)
myDlg.addField('N frames for the prime', 2)
myDlg.addField('N frames for the mask', 12)
while True:
    dlg_data = myDlg.show()
    if myDlg.OK:
        if dlg_data[1] in ["Practice", "Experimental"]:
            break
    else:
        print('user cancelled')
        core.quit()

# set the subject number
participant_number = dlg_data[0]
phase = dlg_data[1]
which_monitor = do_triggers = dlg_data[2]
autopilot = dlg_data[3]

# handle the results directory
results_directory = os.path.join('results_pat', 'P' + str(participant_number).zfill(3))
os.path.exists(results_directory) or os.makedirs(results_directory)

# set up logging
thisLog = logging.LogFile(os.path.join(results_directory, 'P' + str(participant_number).zfill(3) + "_pat_" + phase + "_log.log"), level=logging.INFO, filemode='w')
logging.console.setLevel(logging.CRITICAL)

# process options
if autopilot:
    print("autopilot turned on: all response keys and response times will be RANDOM")
    autopilot = True
elif not autopilot:
    print("collecting real responses")
    autopilot = False

if phase == "Practice":
    print("doing practice pat")
    trial_dict = pd.read_excel("pat_trials_practice.xlsx", sheet_name="pat_trials_practice", index_col="index").transpose()
    number_of_blocks = 1
elif phase == "Experimental":
    print("doing experimental pat")
    trial_dict = pd.read_excel("pat_trials_experimental.xlsx", sheet_name="pat_trials_experimental", index_col="index").transpose()
    number_of_blocks = 2
else:
    trial_dict = None
    number_of_blocks = None
    number_of_trials_per_block = None

print(trial_dict)

# raise thread priority
# core.rush(True)

# garbage collection off
# gc.disable()

# do all monitor and screen stuff
win = None
lenovo = None
viewpixx = None
if which_monitor == "e330":
    xpx = 1920
    ypx = 1080
    xcm = 31
    screen_distance = 53
    lenovo = monitors.Monitor("e330", width=xcm, distance=screen_distance)
    lenovo.saveMon()
    aspect_ratio = float(xpx) / float(ypx)  # is 1.7777777777777777, 16:9
    n_pixels_per_cm = float(xpx) / float(xcm)
    # prime_size = prime_size_in_cm * n_pixels_per_cm  # prime_size var needs to be in units of pixel
    which_screen = 0
    win = visual.Window(fullscr=True, size=[xpx, ypx], units='pix', allowGUI=False, waitBlanking=True, color=[0, 0, 0], monitor=lenovo, screen=which_screen)
    win.recordFrameIntervals = True
if which_monitor == "eeg":
    xpx = 1920
    ypx = 1080
    xcm = 53.5
    screen_distance = 60
    viewpixx = monitors.Monitor("eeg", width=xcm, distance=screen_distance)
    viewpixx.saveMon()
    aspect_ratio = float(xpx) / float(ypx)  # is 1.7777777777777777, 16:9
    n_pixels_per_cm = float(xpx) / float(xcm)
    # prime_size = prime_size_in_cm * n_pixels_per_cm  # prime_size var needs to be in units of pixel
    which_screen = 1
    win = visual.Window(fullscr=True, size=[xpx, ypx], units='pix', allowGUI=False, waitBlanking=True, color=[0, 0, 0], monitor=viewpixx, screen=which_screen)
    win.recordFrameIntervals = True

# compute actual frame rate at runtime
actual_frame_rate = win.getActualFrameRate()
frame_rate_msg = "actual frame rate: {} Hz".format(int(round(actual_frame_rate)))
print(frame_rate_msg)
thisLog.write(txt="{}\n".format(frame_rate_msg))

# durations, specified in ticks
fixation_dur = 180  # 180 is 1500 ms at Hz
blank_dur = 24      # 24 is 200 ms at 120 Hz
primes_dur = dlg_data[4]  # 2      # 2 is 16.666 ms at 120 Hz
masks_dur = dlg_data[5]  # 12      # 12 is 100 ms at 120 Hz
sum_of_fixed_durations = fixation_dur + blank_dur + primes_dur + masks_dur
post_mask = range(600, 810, 10)  # in milliseconds
iti_dur = 1        # 120 is 1000ms at 120Hz

# intervals, specified in ticks
show_fixation = range(fixation_dur)
show_blank = range(fixation_dur, fixation_dur+blank_dur)
show_primes = range(fixation_dur+blank_dur, fixation_dur+blank_dur+primes_dur)
show_masks = range(fixation_dur+blank_dur+primes_dur, fixation_dur+blank_dur+primes_dur+masks_dur)

# stimulus images and their directories
instructions = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "instructions_pat.png"))
fixation = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "fixation.png"))
blank = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "blank.png"))
primes_left = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "prime_left.png"))
primes_right = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "prime_right.png"))
inter_block_message = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "inter_block_message.png"))

# instructions
instructions.draw()
win.flip()
if not autopilot:
    event.waitKeys(keyList=['space'])

# block sequence
for current_block in range(1, number_of_blocks+1):

    if phase == "Practice":
        number_of_trials_per_block = 10
        trial_sequence = random.sample([1,2,3,4,5,6,7,8,9,10], number_of_trials_per_block)
        print("trial_sequence {}".format(trial_sequence))
        running_order = 0

    elif phase == "Experimental":
        number_of_trials_per_block = 84
        block_multiplier = ((current_block - 1) * number_of_trials_per_block)
        if current_block == 1:
            warmup_trials = random.sample([1,2,3,4], 4)
            non_warmup_trials = random.sample(range(5, 85), 80)
            trial_sequence = warmup_trials + non_warmup_trials
        elif current_block ==2:
            warmup_trials = random.sample([85,86,87,88], 4)
            non_warmup_trials = random.sample(range(89, 169), 80)
            trial_sequence = warmup_trials + non_warmup_trials

        print("trial_sequence {}".format(trial_sequence))
        running_order = 0

    else:
        trial_sequence = None
        running_order = None

    # trial sequence
    for current_trial in trial_sequence:
        running_order = running_order + 1
        trial_dict[current_trial]['trial_number'] = running_order
        trial_dict[current_trial]['subject'] = participant_number
        primes = primes_left if trial_dict[current_trial]['prime'] == "left" else primes_right
        masks = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "pat_masks", trial_dict[current_trial]['mask_filename']))
        prime_direction = trial_dict[current_trial]['prime']
        condition = trial_dict[current_trial]['condition']
        triggers = list()
        actual_frame_rate = win.getActualFrameRate()

        # # parallel port initialisation, happens at the top of each trial
        # if there_is_a_parallel_port:
        #     parallel_port.setData(0)

        # masked-priming sequence in a tight loop
        for tix in range(sum_of_fixed_durations):
            if tix in show_fixation:
                fixation.draw()
            elif tix in show_blank:
                blank.draw()
            elif tix in show_primes:
                primes.draw()
            elif tix in show_masks:
                masks.draw()
            win.flip()

        # n-duration blank
        blank.draw()
        win.flip()
        core.wait(0.001*random.sample(range(600, 810, 10), 1)[0])

        # make a sound 600Hz, 150ms
        RT_onset = core.getTime()
        s.play()
        core.wait(0.20)

        # response-terminated blank screen
        if autopilot:
            resp = [[random.sample(['d', 'l'], 1)[0], RT_onset + random.uniform(1, 4)]]
        else:
            resp = []
            while not resp:
                resp = event.getKeys(keyList=['d', 'l', 'escape'], timeStamped=True)
                if resp and resp[0][0] == 'escape':
                    win.close()
                    core.quit()
        key_pressed = resp[0][0]
        response_direction = 'left' if key_pressed == 'd' else 'right' if key_pressed == 'l' else None
        RT_offset = resp[0][1]

        # calculate RT
        response_time = RT_offset - RT_onset  # in seconds

        # put end of trial variables into trial_dict
        trial_dict[current_trial]['trial_number'] = running_order
        trial_dict[current_trial]['response_direction'] = response_direction
        trial_dict[current_trial]['compatibility'] = 'compatible' if trial_dict[current_trial]['prime'] == trial_dict[current_trial]['response_direction'] else 'incompatible'
        trial_dict[current_trial]['response_time'] = round(response_time, 3)

        # experimenter-screen printout
        print("sb:{} bl:{} tr:{} id:{} Hz:{} C:{} trig:{} RT:{} cmp:{}".
              format(participant_number, current_block, str(running_order).zfill(2), str(current_trial).zfill(3),
                     int(round(actual_frame_rate, 1)), str(condition).ljust(20, " "), triggers, str(round(response_time, 3)).ljust(5, " "),
                     str(trial_dict[current_trial]['compatibility']).ljust(11, " ")))

        # write trial_dict to file at the end of each trial
        td = pd.DataFrame.from_dict(trial_dict, orient='columns')
        td = td.transpose()
        td.to_csv(path_or_buf = os.path.join(results_directory, "P" + str(participant_number).zfill(3) + "_pat_" + phase + "_trials.csv"),
                  index=False,
                  columns=["subject", "block_number", "trial_number", "condition", "prime", "target", "mask_filename", "response_direction",
                           "compatibility", "outcome_colour", "rating", "response_time", "rating_time", "triggers"])

        # inter-trial-interval
        core.wait(1)

    # inter-block-interval
    inter_block_message.draw()
    win.flip()
    response_button, response_time = get_response_for_ibi(autopilot=autopilot)
    win.flip()

# end of experiment
win.close()

# print various useful summary things at the end of the experiment
summary_strings = []
cmd = "git branch -v"
output = subprocess.getoutput(cmd)
msg = "versioning information: \"{}\" yields \"{}\"".format(cmd, output)
summary_strings.append(msg)
summary_strings.append(now_time)
for s in summary_strings:
    print(s)

# garbage collection on again
# gc.enable()

# lower thread priority
# core.rush(False)

# quit psychopy
core.quit()
