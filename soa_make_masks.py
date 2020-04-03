import random
import os
import time
import pandas as pd
from psychopy import core, visual, misc, monitors, gui

myDlg = gui.Dlg(title="Set parameters for stimuli creation for the Sense Of Agency (SOA) task", screen=1)
myDlg.addField("Which monitor?", choices=["e330"])
myDlg.addField("line_width_prime?", choices=[2, 1,2,3,4])
myDlg.addField("target_line_width_border?", choices=["same as line width prime", 1,2,3,4])
myDlg.addField("prime_width (in cm)", 1.0)
myDlg.addField("line_length_min as a proportion of prime size", 0.15)
myDlg.addField("line_length_max as a proportion of prime size", 0.40)
myDlg.addField("line_width_min", 0.5)
myDlg.addField("line_width_max", 1.5)
myDlg.addField("grid_size as a proportion of prime size", 0.8)
myDlg.addField("line_length_tolerance, as a proportion of the grid_spacer", 0.8)
myDlg.addField("offset_range_factor", 0.05)
myDlg.addField("scale_multiplier", 1.0)
myDlg.addField("tolerance_factor", 1.1)
myDlg.addField("prime_horizon_adjustment_factor", 0.05)
myDlg.addField("max_number_of_attempts_at_a_line", 500000)

while True:
    dlg_data = myDlg.show()
    if myDlg.OK:
        if dlg_data[0] != "You must select a monitor to get the stimuli at the right size...":
           break
        else:
            print(dlg_data[0])
    else:
        print('user cancelled')
        core.quit()

which_monitor = dlg_data[0]

# set up the monitor
win = None
mon = None
xcm = None
xpx = None
ypx = None
which_screen = None
n_pixels_per_cm = None
if which_monitor == "e330":
    xpx = 1920
    ypx = 1080
    xcm = 31
    screen_distance = 53
    lenovo = monitors.Monitor("e330", width=xcm, distance=screen_distance)
    lenovo.saveMon()
    aspect_ratio = float(xpx) / float(ypx)  # is 1.7777777777777777, 16:9
    n_pixels_per_cm = float(xpx) / float(xcm)
    which_screen = 0
    win = visual.Window(fullscr=True, size=[xpx, ypx], units='pix', allowGUI=False, waitBlanking=True, color=[0, 0, 0], monitor=lenovo, screen=which_screen)

# parse the gui
scale_multiplier = dlg_data[11]
prime_width_in_cm = dlg_data[3]
prime_size = prime_width_in_cm * n_pixels_per_cm * scale_multiplier
line_width_prime = dlg_data[1]
target_line_width_border = line_width_prime if dlg_data[2] == "same as line width prime" else dlg_data[2]
line_length_min = dlg_data[4] * prime_size
line_length_max = dlg_data[5] * prime_size
line_width_min = dlg_data[6]
line_width_max = dlg_data[7]
grid_size = dlg_data[8] * prime_size
grid_spacer = grid_size / 6.0 # 6.0 because that is one less than 7 which is the number of slots in the grid and is a fixed param
line_length_tolerance = dlg_data[9] * grid_spacer
offset_range_factor = dlg_data[10] # how much the lines avoid their point on the grid by
offset_range = [offset_range_factor * grid_spacer, -offset_range_factor * grid_spacer]
tolerance_factor = dlg_data[12] # how much the lines are allowed to overlap their containing box (the grid)
prime_horizon_adjustment_factor = dlg_data[13] # how much north or south the grid for the masks is allowed to drift
max_number_of_attempts_at_a_line = dlg_data[14]

# ANGLES
theta_range = [10, 15, 20, 25, 30, 35, 55, 60, 65, 70, 75, 80, 100, 105, 110, 115, 120, 125, 145, 150, 155, 160, 165, 170, 190, 195, 200, 205, 210, 215, 235, 240, 245, 250, 255, 260, 280, 285, 290, 295, 300, 305, 325, 330, 335, 340, 345, 350]

# set up the directory to write the masks into
os.path.exists("stimuli") or os.mkdir("stimuli")
os.path.exists(os.path.join("stimuli", which_monitor)) or os.mkdir(os.path.join("stimuli", which_monitor))
os.path.exists(os.path.join("stimuli", which_monitor, "masks")) or os.mkdir(os.path.join("stimuli", which_monitor, "masks"))

# create a skeletal trial structure by calling a function that sets up a dict and dumps that to an excel file
def get_trial_structure():

    n_blocks = 8
    n_trials_per_block = 64

    trial_dict_init = {}
    for j in range(1, n_blocks+1):
        for i in range(1, n_trials_per_block+1):
            t = i + ((j-1) * n_trials_per_block)
            if 1 <= i <= 4:
                trial_dict_init[t] = {
                    'unique_id': t,
                    'outcome_colour': None,
                    'compatibility': None,
                    'trial_number': None,
                    'block_number': j,
                    'response_direction': None,
                    'response_time': None,
                    'rating': None,
                    'rating_time': None,
                    'condition': 'warmup',
                    'prime': 'left' if i in [1, 2] else 'right',
                    'target': 'left' if i in [1, 3] else 'right',
                    'mask_filename': "no_filename",
                    'subject': None,
                    'triggers': list()
                }
            if 5 <= i <= 52:
                trial_dict_init[t] = {
                    'unique_id': t,
                    'outcome_colour': None,
                    'compatibility': None,
                    'trial_number': None,
                    'block_number': j,
                    'response_direction': None,
                    'response_time': None,
                    'rating': None,
                    'rating_time': None,
                    'condition': 'free',
                    'prime': 'left' if i in range(5, 29) else 'right',
                    'target': 'border',
                    'mask_filename': "no_filename",
                    'subject': None,
                    'triggers': list()
                }
            if 53 <= i <= 58:
                trial_dict_init[t] = {
                    'unique_id': t,
                    'outcome_colour': None,
                    'compatibility': None,
                    'trial_number': None,
                    'block_number': j,
                    'response_direction': None,
                    'response_time': None,
                    'rating': None,
                    'rating_time': None,
                    'condition': 'forced_compatible',
                    'prime': 'left' if i in range(53, 56) else 'right',
                    'target': 'left' if i in range(53, 56) else 'right',
                    'mask_filename': "no_filename",
                    'subject': None,
                    'triggers': list()
                }
            if 59 <= i <= 64:
                trial_dict_init[t] = {
                    'unique_id': t,
                    'outcome_colour': None,
                    'compatibility': None,
                    'trial_number': None,
                    'block_number': j,
                    'response_direction': None,
                    'response_time': None,
                    'rating': None,
                    'rating_time': None,
                    'condition': 'forced_incompatible',
                    'prime': 'left' if i in range(59, 62) else 'right',
                    'target': 'right' if i in range(59, 62) else 'left',
                    'mask_filename': "no_filename",
                    'subject': None,
                    'triggers': list()
                }

    return trial_dict_init

# get the trial_dict, which will be filled with mask filenames in this file
trial_dict = get_trial_structure()  # 1-indexed because a dict of dicts and 1 is the key not a row number (no row numbers in a dict of dicts)

# if the masks were generated in the last 10 minutes then skip those masks
criterion = 1000  # minutes ago
now = time.time()
mask_time = 0.0
starting_mask = 1
for n_masks in range(1, 512+1):
    mask_filename = os.path.join("stimuli", which_monitor, "masks", "mask" + str(n_masks).zfill(3) + ".png")
    exists = os.path.isfile(mask_filename)
    if exists:
        mask_time = os.path.getmtime(mask_filename)
        trial_dict[n_masks]['mask_filename'] = "mask" + str(n_masks).zfill(3) + ".png"
        if (now - mask_time) / 60. < criterion:
            print("skipping mask {} because file exists and was modified {} minutes ago, less than the criterion of {} minutes ago".format(n_masks, round(((now - mask_time) / 60), 1), criterion))
            starting_mask = n_masks + 1
    else:
        break

# this is the main loop for mask creation
for n_masks in range(starting_mask, 1+512):
    mask_filename = "mask" + str(n_masks).zfill(3) + ".png"
    trial_dict[n_masks]['mask_filename'] = mask_filename
    current_trial = trial_dict[n_masks]
    # target maker
    target_type = current_trial['target']
    target_horizon = 0
    target_zenith = 0
    target_size = 1.0 * prime_size
    target_half = 0.5 * target_size
    target_top = target_horizon + target_half
    target_bottom = target_horizon - target_half
    target_left = - target_half
    target_right = target_half
    target_type_left = None
    target_type_right = None
    target_type_border = None
    if target_type == "left":
        target_type_left = []
        north_chevron_l_hi_1 = visual.Line(win, start=(target_left, target_horizon), end=(target_zenith, target_top), lineColor="black", lineWidth=line_width_prime)
        target_type_left.append(north_chevron_l_hi_1)
        north_chevron_l_lo_1 = visual.Line(win, start=(target_left, target_horizon), end=(target_zenith, target_bottom), lineColor="black", lineWidth=line_width_prime)
        target_type_left.append(north_chevron_l_lo_1)
        north_chevron_l_hi_2 = visual.Line(win, start=(target_zenith, target_horizon), end=(target_right, target_top), lineColor="black", lineWidth=line_width_prime)
        target_type_left.append(north_chevron_l_hi_2)
        north_chevron_l_lo_2 = visual.Line(win, start=(target_zenith, target_horizon), end=(target_right, target_bottom), lineColor="black", lineWidth=line_width_prime)
        target_type_left.append(north_chevron_l_lo_2)
    elif target_type == "right":
        target_type_right = []
        north_chevron_r_hi_1 = visual.Line(win, start=(target_left, target_top), end=(target_zenith, target_horizon), lineColor="black", lineWidth=line_width_prime)
        target_type_right.append(north_chevron_r_hi_1)
        north_chevron_r_lo_1 = visual.Line(win, start=(target_left, target_bottom), end=(target_zenith, target_horizon), lineColor="black", lineWidth=line_width_prime)
        target_type_right.append(north_chevron_r_lo_1)
        north_chevron_r_hi_2 = visual.Line(win, start=(target_zenith, target_top), end=(target_right, target_horizon), lineColor="black", lineWidth=line_width_prime)
        target_type_right.append(north_chevron_r_hi_2)
        north_chevron_r_lo_2 = visual.Line(win, start=(target_zenith, target_bottom), end=(target_right, target_horizon), lineColor="black", lineWidth=line_width_prime)
        target_type_right.append(north_chevron_r_lo_2)
    elif target_type == "border":
        target_type_border = []
        target_border = visual.Rect(win=win, pos=(target_zenith, target_horizon), height=prime_size, width=prime_size, lineColor="black", lineWidth=target_line_width_border)
        target_type_border.append(target_border)
    # mask maker
    north_mask = []
    north_horizon = 0 + prime_size + (prime_size * prime_horizon_adjustment_factor)
    north_tolerance_size = tolerance_factor * prime_size
    north_tolerance_half = 0.5 * north_tolerance_size
    north_tolerance_top = north_horizon + north_tolerance_half
    north_tolerance_bottom = north_horizon - north_tolerance_half
    north_tolerance_left = - north_tolerance_half
    north_tolerance_right = + north_tolerance_half
    north_tolerance_box = visual.Rect(win, pos=(0, north_horizon), height=north_tolerance_size, width=north_tolerance_size, lineColor="blue")
    north_prime_size = 1.0 * prime_size
    north_prime_half = 0.5 * prime_size
    north_prime_top = north_horizon + north_prime_half
    north_prime_bottom = north_horizon - north_prime_half
    north_prime_box = visual.Rect(win, pos=(0, north_horizon), height=prime_size, width=prime_size, lineColor="white")
    north_grid_size = 0.8 * prime_size
    north_grid_half = 0.5 * north_grid_size
    north_grid_top = north_horizon + north_grid_half
    north_grid_bottom = north_horizon - north_grid_half
    north_grid_left = - north_grid_half
    north_grid_right = + north_grid_half
    north_grid_box = visual.Rect(win, pos=(0, north_horizon), height=north_grid_size, width=north_grid_size, lineColor="red")
    for row in range(7):
        for col in range(7):
            grid_x = north_grid_left + (col * grid_spacer)
            grid_y = north_grid_bottom + (row * grid_spacer)
            n_attempts = 0
            t0 = core.getTime()
            while True:
                n_attempts += 1
                line_length = random.uniform(line_length_min, line_length_max)
                line_width = random.uniform(line_width_min, line_width_max)
                polar_x, polar_y = misc.pol2cart(theta=random.sample(theta_range, 1)[0], radius=line_length)
                offset_x = random.sample(offset_range, 1)[0]
                grid_x = grid_x + offset_x
                offset_y = random.sample(offset_range, 1)[0]
                grid_y = grid_y + offset_y
                line_start = (grid_x + polar_x, grid_y + polar_y)
                line_end = (grid_x - polar_x, grid_y - polar_y)
                if north_tolerance_box.contains(line_start) and north_tolerance_box.contains(line_end):
                    break
                if n_attempts > max_number_of_attempts_at_a_line:
                    print("{} is too many attempts, it took {} seconds".format(n_attempts, core.getTime()-t0))
                    quit()
            line = visual.Line(win=win, start=line_start, end=line_end, lineColor="black", lineWidth=line_width)
            north_mask.append(line)
    south_mask = []
    south_horizon = 0 - (prime_size + (prime_size * prime_horizon_adjustment_factor))
    south_tolerance_size = tolerance_factor * prime_size
    south_tolerance_half = 0.5 * south_tolerance_size
    south_tolerance_top = south_horizon + south_tolerance_half
    south_tolerance_bottom = south_horizon - south_tolerance_half
    south_tolerance_left = - south_tolerance_half
    south_tolerance_right = + south_tolerance_half
    south_tolerance_box = visual.Rect(win, pos=(0, south_horizon), height=south_tolerance_size, width=south_tolerance_size, lineColor="yellow")
    south_prime_size = 1.0 * prime_size
    south_prime_half = 0.5 * prime_size
    south_prime_top = south_horizon + south_prime_half
    south_prime_bottom = south_horizon - south_prime_half
    south_prime_box = visual.Rect(win, pos=(0, south_horizon), height=prime_size, width=prime_size, lineColor="white")
    south_grid_size = 0.8 * prime_size
    south_grid_half = 0.5 * south_grid_size
    south_grid_top = south_horizon + south_grid_half
    south_grid_bottom = south_horizon - south_grid_half
    south_grid_left = - south_grid_half
    south_grid_right = + south_grid_half
    south_grid_box = visual.Rect(win, pos=(0, south_horizon), height=south_grid_size, width=south_grid_size, lineColor="red")
    for row in range(7):
        for col in range(7):
            grid_x = south_grid_left + (col * grid_spacer)
            grid_y = south_grid_bottom + (row * grid_spacer)
            n_attempts = 0
            t0 = core.getTime()
            while True:
                n_attempts += 1
                line_length = random.uniform(line_length_min, line_length_max)
                line_width = random.uniform(line_width_min, line_width_max)
                polar_x, polar_y = misc.pol2cart(theta=random.sample(theta_range, 1)[0], radius=line_length)
                offset_x = random.sample(offset_range, 1)[0]
                grid_x = grid_x + offset_x
                offset_y = random.sample(offset_range, 1)[0]
                grid_y = grid_y + offset_y
                line_start = (grid_x + polar_x, grid_y + polar_y)
                line_end = (grid_x - polar_x, grid_y - polar_y)
                if south_tolerance_box.contains(line_start) and south_tolerance_box.contains(line_end):
                    break
                if n_attempts > max_number_of_attempts_at_a_line:
                    print("{} is too many attempts, it took {} seconds".format(n_attempts, core.getTime() - t0))
                    quit()
            line = visual.Line(win=win, start=line_start, end=line_end, lineColor="black", lineWidth=line_width)
            south_mask.append(line)
    # combine mask with target
    current_target = target_type_left if target_type == "left" else target_type_right if target_type == "right" else target_type_border if target_type == "border" else None
    mask_and_target_list = current_target + north_mask + south_mask
    mask_and_target = visual.BufferImageStim(autoLog=False, win=win, stim=mask_and_target_list)
    mask_and_target.draw()
    win.getMovieFrame(buffer='back')
    win.saveMovieFrames(os.path.join("stimuli", which_monitor, "masks", mask_filename))
    win.flip()  
    print("finished creating mask # {}".format(n_masks))

for do_spreadsheet in range(1):
    # this just saves a spreadsheet containing the trial_dict now that the mask_filename has been added
    td = pd.DataFrame.from_dict(trial_dict, orient='columns')
    td = td.transpose()
    writer = pd.ExcelWriter("soa_trials_experimental.xlsx", engine='xlsxwriter')
    # index should be True if you want pandas to be able to read it in later and then be able to refer to rows by their index in the normal way. index = False drops the extra column for index, which is better for human viewing like results files
    td.to_excel(writer, "trials", index=True, columns=["subject", "unique_id", "block_number", "trial_number", "condition", "prime", "target", "mask_filename", "response_direction", "compatibility", "outcome_colour", "rating", "response_time", "rating_time", "triggers"])
    writer.save()

print("n_pixels_per_cm = {}".format(n_pixels_per_cm))

win.close()
core.quit()
