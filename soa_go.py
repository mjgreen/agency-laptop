#!/home/matt/anaconda3/envs/py2/bin/python2.7

"""
using python2

trial sequence:
# gui
# experiment-initial instructions
# masked-priming sequence
# collect a kb response indicating which direction the prime was facing. Is a response-terminated blank screen.
# blank screen after direction response, for a duration sampled at random on a per-trial basis
# classify response and show outcome colour, for a duration sampled at random on a per-trial basis
# blank screen after colour show, for a duration sampled at random on a per-trial basis (for between 1000 and 2000 ms)
# response-terminated How much control?
# inter-trial-interval, during which permit dev to quit
# inter-block-interval

trigger sequence:
1; 2            record the direction of the prime: left / right
3; 4; 5; 6      condition: 3=forced compatible, 4=forced incompatible, 5=free, 6=warmup
7; 8            record the response after the mask: left-control; right-control
10; 11; 12; 13  record the compatible/incompatible;  left/right
"""

import os
import random
import datetime
import gc
import shutil
import pandas as pd
from soa_helpers import get_response_to_mask, get_response_for_rating, get_response_for_ibi, endex
from psychopy import visual, event, core, monitors, logging, gui, parallel

# get a date time stamp
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H%M')

# gui
myDlg = gui.Dlg(title="SOA", screen=1)
myDlg.addField('Participant ID:', 999)
myDlg.addField('Participant Age:', 19)
myDlg.addField('Participant Sex:', choices=['female','male'])
myDlg.addField('Practice or Experimental?:', choices=["Experimental", "Please choose which phase", "Practice", "Experimental"])
myDlg.addField('Triggers?', initial=False)
myDlg.addField('Autopilot?', initial=False)
myDlg.addField('Prime duration (in frames)?', 2)
myDlg.addField('Mask duration (in frames)?', 12)
myDlg.addField('Colour circle radius (in pixels)?', 24)
myDlg.addField('Which screen? (1 for viewpixx, 0 for right hand side screen)', 1)
myDlg.addField("Which monitor?", choices=["eeg", "e330"])
myDlg.addField("Which colour condition?", choices=["A", "B"])
dlg_data = myDlg.show()
if myDlg.OK:
    pass
else:
    print('user cancelled')
    core.quit()

# assign gui responses to variables
participant_number = dlg_data[0]
participant_code = 'P' + str(participant_number).zfill(3)
participant_age = dlg_data[1]
participant_sex = dlg_data[2]
phase = dlg_data[3]
do_triggers = dlg_data[4]
autopilot = dlg_data[5]
primes_dur = dlg_data[6]
masks_dur = dlg_data[7]
circle_radius = dlg_data[8]
which_screen = dlg_data[9]
which_monitor = dlg_data[10]
colour_condition = dlg_data[11]
# TODO process the colour condition, counterbalance it by flipping the compat and incompat colors, but it's ok to keep the same colour pair for a given block

# say whether to send triggers
if do_triggers:
    parallel_port = parallel.ParallelPort(address=0x1FF8)  # eeg z440
    there_is_a_parallel_port = True
    triggers_msg = "triggers turned on"
    print(triggers_msg)
else:
    parallel_port = None
    there_is_a_parallel_port = False
    triggers_msg = "no triggers will be sent"
    print(triggers_msg)

# handle the results directory
results_directory = os.path.join('results_soa', participant_code)
if participant_number == 999 and os.path.exists(results_directory):
    shutil.rmtree(results_directory)
    os.makedirs(results_directory)
elif (not participant_number == 999) and os.path.exists(results_directory):
    print("\nYou already used this participant number: {}, run again and choose a different one\n".format(participant_number))
    quit()
else:
    os.makedirs(results_directory)

# write gui state to file in results directory
dlg = {myDlg.__dict__["inputFieldNames"][i]: myDlg.__dict__["data"][i] for i in range(len(myDlg.__dict__["data"]))}
with open(os.path.join(results_directory, "options_selected_at_runtime.txt"), "w") as f:
    for k,v in dlg.items():
        f.write("{} {}\n".format(str(k+" ").ljust(60, "."), v))

# set up logging
thisLog = logging.LogFile(os.path.join(results_directory, participant_code + "_soa_" + phase + "_log.log"), level=logging.INFO, filemode='w')
thisLog.write(txt="{}\n".format(triggers_msg))

# durations
if autopilot:
    # these are in frames
    fixation_dur = 2    # 180 is 1500 ms at 120 Hz
    blank_dur = 2       # 24 is 200 ms at 120 Hz
    primes_dur = 2      # 2 is 16.666 ms at 120 Hz
    masks_dur = 2       # 12 is 100 ms at 120 Hz
    sum_of_fixed_durations = fixation_dur + blank_dur + primes_dur + masks_dur
    # intervals, specified in frames
    show_fixation = range(fixation_dur)
    show_blank = range(fixation_dur, fixation_dur + blank_dur)
    show_primes = range(fixation_dur + blank_dur, fixation_dur + blank_dur + primes_dur)
    show_masks = range(fixation_dur + blank_dur + primes_dur, fixation_dur + blank_dur + primes_dur + masks_dur)
    # these are in seconds
    colour_dur_in_seconds = 0.100 # seconds
    min_dur_blank_screen_after_direction_response = 0.100 # seconds
    max_dur_blank_screen_after_direction_response = 0.100 # seconds
    min_dur_blank_screen_after_colour_show = 0.100 # seconds
    max_dur_blank_screen_after_colour_show = 0.100 # seconds
    dur_wait_for_rating = 0.100 # seconds, only applies in autopilot
    msg = "autopilot turned on: all response keys and response times will be RANDOM"
    print(msg)
    thisLog.write(txt="{}\n".format(msg))
    autopilot_wait = 0.200 # seconds, only applies in autopilot
else:
    # these are in frames
    fixation_dur = 180         # 180 is 1500 ms at 120 Hz
    blank_dur = 24             # 24 is 200 ms at 120 Hz
    primes_dur = dlg_data[6]   # 2 is 16.666 ms at 120 Hz
    masks_dur = dlg_data[7]    # 12             # 12 is 100 ms at 120 Hz
    sum_of_fixed_durations = fixation_dur + blank_dur + primes_dur + masks_dur
    # intervals, specified in frames
    show_fixation = range(fixation_dur)
    show_blank = range(fixation_dur, fixation_dur + blank_dur)
    show_primes = range(fixation_dur + blank_dur, fixation_dur + blank_dur + primes_dur)
    show_masks = range(fixation_dur + blank_dur + primes_dur, fixation_dur + blank_dur + primes_dur + masks_dur)
    # these are in seconds
    colour_dur_in_seconds = 0.600 # seconds
    min_dur_blank_screen_after_direction_response = 0.400 # seconds
    max_dur_blank_screen_after_direction_response = 0.600 # seconds
    min_dur_blank_screen_after_colour_show = 1.000 # seconds
    max_dur_blank_screen_after_colour_show = 1.500 # seconds
    dur_wait_for_rating = 0.100  # seconds, only applies in autopilot
    autopilot_wait = 0.200  # seconds, only applies in autopilot

# read in the correct trial definitions
if phase == "Practice":
    print("doing practice soa")
    trial_dict = pd.read_excel("soa_trials_practice.xlsx", sheet_name="trials_practice", index_col=0).transpose()
    number_of_blocks = 1
    number_of_trials_per_block = 24
elif phase == "Experimental":
    print("doing experimental soa")
    trial_dict = pd.read_excel("soa_trials_experimental.xlsx", sheet_name="trials", index_col=0).transpose()
    number_of_blocks = 8
    number_of_trials_per_block = 64
else:
    trial_dict = None
    number_of_blocks = None
    number_of_trials_per_block = None

# raise thread priority
core.rush(True)

# garbage collection off
gc.disable()

# set some constants
# prime_size_in_cm = 1.0
# prime_horizon_adjustment_factor = 0.05

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

# stimulus images and their directories
instructions = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "instructions.png"), name="experiment initial instructions")
fixation = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "fixation.png"), name="fixation cross")
blank = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "blank.png"), name="blank screen")
primes_left = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "prime_left.png"), name="left facing prime")
primes_right = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "prime_right.png"), name="right facing prime")
how_much_control = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "howMuchControl.png"), name="how much control?")
inter_block_message = visual.ImageStim(win, os.path.join("stimuli", which_monitor, "inter_block_message.png"), name="inter-block message")

#
# experiment starts here
#
# instructions
instructions.draw()
win.flip()
event.clearEvents(eventType='keyboard')
if autopilot:
    core.wait(secs=autopilot_wait)
else:
    event.waitKeys(keyList=['space', 'escape'])
win.flip()

# block sequence
for current_block in range(1, number_of_blocks+1):

    trial_sequence = None
    running_order = None
    if phase == "Practice":
        block_multiplier = ((current_block - 1) * number_of_trials_per_block)
        non_warmup_trials = list(range(1 + block_multiplier, number_of_trials_per_block+1 + block_multiplier))
        random.shuffle(non_warmup_trials)
        trial_sequence = non_warmup_trials
        running_order = 0
    elif phase == "Experimental":
        block_multiplier = ((current_block - 1) * number_of_trials_per_block)
        warmup_trials = list(range(1 + block_multiplier, 5 + block_multiplier))
        random.shuffle(warmup_trials)
        non_warmup_trials = list(range(5 + block_multiplier, number_of_trials_per_block+1 + block_multiplier))
        random.shuffle(non_warmup_trials)
        trial_sequence = warmup_trials + non_warmup_trials
        running_order = 0

    # trial sequence
    for current_trial in trial_sequence:

        # parallel port initialisation, happens at the top of each trial
        if there_is_a_parallel_port:
            parallel_port.setData(0)

        # set up the variables for this particular trial
        running_order = running_order + 1
        trial_dict[current_trial]['trial_number'] = running_order
        trial_dict[current_trial]['subject'] = participant_number
        primes = primes_left if trial_dict[current_trial]['prime'] == "left" else primes_right
        masks = visual.ImageStim(win=win, image=os.path.join("stimuli", which_monitor, "masks", trial_dict[current_trial]['mask_filename']), name=trial_dict[current_trial]['mask_filename'])
        prime_direction = trial_dict[current_trial]['prime']
        prime_trigger_code = 1 if prime_direction == 'left' else 2 if prime_direction == 'right' else None
        condition = trial_dict[current_trial]['condition']
        mask_trigger_code = 3 if condition == 'forced_compatible' else 4 if condition == 'forced_incompatible' else 5 if condition == 'free' else 6 if condition == 'warmup' else None
        triggers = list()
        actual_frame_rate = win.getActualFrameRate()

        # masked-priming sequence in a tight loop
        for frames in range(sum_of_fixed_durations):
            if frames in show_fixation:
                fixation.draw()
            elif frames in show_blank:
                blank.draw()
            elif frames in show_primes:
                primes.draw()
                if frames == fixation_dur+blank_dur:
                    triggers.append(prime_trigger_code)
                    if there_is_a_parallel_port:
                        parallel_port.setData(prime_trigger_code)
            elif frames in show_masks:
                masks.draw()
                if frames == fixation_dur+blank_dur+primes_dur:
                    triggers.append(mask_trigger_code)
                    if there_is_a_parallel_port:
                        parallel_port.setData(mask_trigger_code)
            win.flip()
            # this is the "palette-cleanser" trigger_code
            if there_is_a_parallel_port:
                parallel_port.setData(0)
        blank.draw()
        win.flip()

        # get the kb response to the mask
        # response-terminated blank screen; classify and record vars
        blank.draw()
        win.flip()
        response_button, response_time = get_response_to_mask(autopilot=autopilot, win=win, results_directory=results_directory)
        trigger_code = 7 if response_button == 'd' else 8 if response_button == 'l' else None
        triggers.append(trigger_code)
        if there_is_a_parallel_port:
            parallel_port.setData(trigger_code)
        trial_dict[current_trial]['response_time'] = response_time
        response_direction = 'left' if response_button == 'd' else 'right' if response_button == 'l' else None
        trial_dict[current_trial]['response_direction'] = response_direction
        if trial_dict[current_trial]['condition'] == 'free':
            trial_dict[current_trial]['compatibility'] = 'compatible' if trial_dict[current_trial]['prime'] == trial_dict[current_trial]['response_direction'] else 'incompatible'
        elif trial_dict[current_trial]['condition'] in ['forced_compatible', 'forced_incompatible', 'warmup']:
            trial_dict[current_trial]['compatibility'] = 'compatible' if trial_dict[current_trial]['prime'] == trial_dict[current_trial]['target'] else 'incompatible'
        blank.draw()
        win.flip()
        if there_is_a_parallel_port:
            parallel_port.setData(0)

        # blank screen after direction response.
        # should be a random sample between 400 and 600 milliseconds
        blank.draw()
        win.flip()
        core.wait(secs=random.uniform(min_dur_blank_screen_after_direction_response, max_dur_blank_screen_after_direction_response))


        # counterbalance the colours

        if colour_condition == "A":
            colour_1_compatible   = 'PaleVioletRed'
            colour_1_incompatible = 'CadetBlue'
            colour_2_compatible   = 'PaleVioletRed'
            colour_2_incompatible = 'CadetBlue'
            colour_3_compatible   = 'DarkOrange'
            colour_3_incompatible = 'SlateBlue'
            colour_4_compatible   = 'DarkOrange'
            colour_4_incompatible = 'SlateBlue'
            colour_5_compatible   = 'GoldenRod'
            colour_5_incompatible = 'DodgerBlue'
            colour_6_compatible   = 'GoldenRod'
            colour_6_incompatible = 'DodgerBlue'
            colour_7_compatible   = 'BlueViolet'
            colour_7_incompatible = 'LightGreen'
            colour_8_compatible   = 'BlueViolet'
            colour_8_incompatible = 'LightGreen'
        if colour_condition == "B":
            # same, just cut in half and the last half goes in as the first half
            colour_1_compatible   = 'GoldenRod'
            colour_1_incompatible = 'DodgerBlue'
            colour_2_compatible   = 'GoldenRod'
            colour_2_incompatible = 'DodgerBlue'
            colour_3_compatible   = 'BlueViolet'
            colour_3_incompatible = 'LightGreen'
            colour_4_compatible   = 'BlueViolet'
            colour_4_incompatible = 'LightGreen'
            colour_5_compatible = 'PaleVioletRed'
            colour_5_incompatible = 'CadetBlue'
            colour_6_compatible = 'PaleVioletRed'
            colour_6_incompatible = 'CadetBlue'
            colour_7_compatible = 'DarkOrange'
            colour_7_incompatible = 'SlateBlue'
            colour_8_compatible = 'DarkOrange'
            colour_8_incompatible = 'SlateBlue'



        # classify response and show outcome

        if trial_dict[current_trial]['block_number'] == 1:
            trial_dict[current_trial]['outcome_colour'] = colour_1_compatible if trial_dict[current_trial]['compatibility'] is 'compatible' else colour_1_incompatible
        if trial_dict[current_trial]['block_number'] == 2:
            trial_dict[current_trial]['outcome_colour'] = colour_2_compatible if trial_dict[current_trial]['compatibility'] is 'compatible' else colour_2_incompatible
        if trial_dict[current_trial]['block_number'] == 3:
            trial_dict[current_trial]['outcome_colour'] = colour_3_compatible if trial_dict[current_trial]['compatibility'] is 'compatible' else colour_3_incompatible
        if trial_dict[current_trial]['block_number'] == 4:
            trial_dict[current_trial]['outcome_colour'] = colour_4_compatible if trial_dict[current_trial]['compatibility'] is 'compatible' else colour_4_incompatible
        if trial_dict[current_trial]['block_number'] == 5:
            trial_dict[current_trial]['outcome_colour'] = colour_5_compatible if trial_dict[current_trial]['compatibility'] is 'compatible' else colour_5_incompatible
        if trial_dict[current_trial]['block_number'] == 6:
            trial_dict[current_trial]['outcome_colour'] = colour_6_compatible if trial_dict[current_trial]['compatibility'] is 'compatible' else colour_6_incompatible
        if trial_dict[current_trial]['block_number'] == 7:
            trial_dict[current_trial]['outcome_colour'] = colour_7_compatible if trial_dict[current_trial]['compatibility'] is 'compatible' else colour_7_incompatible
        if trial_dict[current_trial]['block_number'] == 8:
            trial_dict[current_trial]['outcome_colour'] = colour_8_compatible if trial_dict[current_trial]['compatibility'] is 'compatible' else colour_8_incompatible

        outcome_colour_stimulus = visual.Circle(win, radius=circle_radius, color=trial_dict[current_trial]['outcome_colour'], name="outcome_colour_circle")

        trigger_code = \
            10 if trial_dict[current_trial]['compatibility'] == 'compatible' and trial_dict[current_trial]['prime'] == 'left' \
                else 11 if trial_dict[current_trial]['compatibility'] == 'incompatible' and trial_dict[current_trial]['prime'] == 'left' \
                else 12 if trial_dict[current_trial]['compatibility'] == 'compatible' and trial_dict[current_trial]['prime'] == 'right' \
                else 13 if trial_dict[current_trial]['compatibility'] == 'incompatible' and trial_dict[current_trial]['prime'] == 'right' \
                else None

        # show the outcome colour for a fixed duration previously defined, and send a trigger
        outcome_colour_stimulus.draw()
        win.flip()
        if there_is_a_parallel_port:
            parallel_port.setData(trigger_code)
        outcome_colour_stimulus.draw()
        win.flip()
        if there_is_a_parallel_port:
            parallel_port.setData(0)
        core.wait(secs=colour_dur_in_seconds)

        # blank screen after colour show for between 1000 and 1500 ms
        blank.draw()
        win.flip()
        core.wait(secs=random.uniform(min_dur_blank_screen_after_colour_show, max_dur_blank_screen_after_colour_show))

        # response-terminated How much control?
        how_much_control.draw()
        win.flip()
        rating_response, rating_time = get_response_for_rating(autopilot=autopilot, win=win, results_directory=results_directory, dur_wait_for_rating=dur_wait_for_rating)
        trigger_code = 20 + rating_response
        triggers.append(trigger_code)
        if there_is_a_parallel_port:
            parallel_port.setData(trigger_code)
        how_much_control.draw()
        win.flip()
        if there_is_a_parallel_port:
            parallel_port.setData(0)

        #
        # ok, we are done presenting stuff for the current trial at this point
        #

        # save some trial vars into the trial dict
        trial_dict[current_trial]['rating'] = rating_response
        trial_dict[current_trial]['rating_time'] = rating_time
        trial_dict[current_trial]['triggers'] = triggers

        # write (partial) trial_dict to excel at the end of each trial to avoid data loss
        td = pd.DataFrame.from_dict(trial_dict, orient='columns')
        td = td.transpose()
        f_out = os.path.join(results_directory, participant_code + "_soa_" + phase + "_trials.xlsx")
        writer = pd.ExcelWriter(f_out, engine='xlsxwriter')
        td.to_excel(excel_writer=writer, sheet_name=str(now_time), index=False, columns=["subject", "unique_id", "block_number", "trial_number", "condition", "prime", "target", "mask_filename", "response_direction", "compatibility", "outcome_colour", "rating", "response_time", "rating_time", "triggers"])
        writer.save()

        # flush the logs
        logging.flush()

        # permit experimenter to quit between trials
        k = event.getKeys(keyList=['escape'])
        if k:
            print("quitting because experimenter pressed escape")
            endex(win, results_directory)

        # clear any kb events so that any sticky key stuff doesn't make it into the next trial
        event.clearEvents(eventType='keyboard')

        # experimenter-screen printout
        end_of_trial_summary = "sb:{} bl:{} of {} tr:{} of {} id:{} Hz:{} C:{} trig:{} RT:{} cmp:{}".format(participant_number, current_block, number_of_blocks, str(running_order).zfill(2), number_of_trials_per_block, str(current_trial).zfill(3), (round(actual_frame_rate, 1)), str(condition).ljust(20, " "), triggers, str(round(response_time, 3)).ljust(5, " "), str(trial_dict[current_trial]['compatibility']).ljust(11, " "))
        print(end_of_trial_summary)
        thisLog.write(end_of_trial_summary+"\n")
        # Go for the next trial now

    #
    # OK, we are done with the current block
    #

    # inter-block-interval
    inter_block_message.draw()
    win.flip()
    response_button, response_time = get_response_for_ibi(autopilot=autopilot, win=win, results_directory=results_directory)
    win.flip()

    # Go for another block now

#
# end of experiment
#
print("we got to the end")
endex(win, results_directory)