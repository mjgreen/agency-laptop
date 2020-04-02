"""
make text stimuli, and stims like blank screen, fixation cross, etc, but not primes or masks
"""

import os
from psychopy import core, visual, gui, monitors

myDlg = gui.Dlg(title="Set parameters for *fixed* stimuli creation for the Sense Of Agency (SOA) task", screen=1)
myDlg.addField("Which monitor?", choices=["eeg", "e330"])
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
if which_monitor == "eeg":
    xpx = 1920
    ypx = 1080
    xcm = 53.5
    screen_distance = 60
    viewpixx = monitors.Monitor("eeg", width=xcm, distance=screen_distance)
    viewpixx.saveMon()
    aspect_ratio = float(xpx) / float(ypx)  # is 1.7777777777777777, 16:9
    n_pixels_per_cm = float(xpx) / float(xcm)
    which_screen = 1
    win = visual.Window(fullscr=True, size=[xpx, ypx], units='pix', allowGUI=False, waitBlanking=True, color=[0, 0, 0], monitor=viewpixx, screen=which_screen)

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


# set stimuli path
os.path.exists("stimuli" + os.path.sep + which_monitor) or os.makedirs("stimuli" + os.path.sep + which_monitor)

for n_fixation_crosses in range(1):
    fixation_cross = []
    fixation_height = 0.25*prime_size
    fixation_cross_stimulus = visual.ShapeStim(win=win, vertices=((0, -fixation_height), (0, fixation_height), (0, 0), (-fixation_height, 0), (fixation_height, 0)), lineWidth=line_width_prime, closeShape=False, lineColor="black")
    fixation_cross.append(fixation_cross_stimulus)
    fixation_stimulus = visual.BufferImageStim(autoLog=False, win=win, stim=fixation_cross)
    fixation_stimulus.draw()
    win.getMovieFrame(buffer='back')
    win.saveMovieFrames(os.path.join("stimuli", which_monitor, "fixation" + ".png"))


for times in range(1):
    inter_block_message = []
    inter_block_message_text = visual.TextStim(win, "You have finished that block.\nPlease take a short break, and press 'spacebar' when you are ready to start the next block", color="black", height=20, wrapWidth=1000)
    inter_block_message.append(inter_block_message_text)
    inter_block_message_stimulus = visual.BufferImageStim(autoLog=False, win=win, stim=inter_block_message)
    inter_block_message_stimulus.draw()
    win.getMovieFrame(buffer='back')
    win.saveMovieFrames(os.path.join("stimuli", which_monitor, "inter_block_message.png"))
    win.flip()
    core.wait(2)
    win.flip()

for times in range(1):
    instructions = []
    instructions_text = visual.TextStim(win, "Use the 'd' and 'l' keys to respond 'left' and 'right';\nand use the keys 'd, f, g, h, j, k, l' to represent 1,2,3,4,5,6,7, when you respond to the rating.\nPress 'spacebar' to dismiss this message when you are ready to start", color="black", height=20, wrapWidth=1000)
    instructions.append(instructions_text)
    instructions_stimulus = visual.BufferImageStim(autoLog=False, win=win, stim=instructions)
    instructions_stimulus.draw()
    win.getMovieFrame(buffer='back')
    win.saveMovieFrames(os.path.join("stimuli", which_monitor, "instructions.png"))
    win.flip()
    core.wait(2)
    win.flip()

for times in range(1):
    instructions_pat = []
    instructions_pat_text = visual.TextStim(win, "Respond to the question 'What direction were the arrows pointing?' using 'd' for left and 'l' for right\nPress 'space' to start", color="black", height=20, wrapWidth=1000)
    instructions_pat.append(instructions_pat_text)
    instructions_pat_stimulus = visual.BufferImageStim(autoLog=False, win=win, stim=instructions_pat)
    instructions_pat_stimulus.draw()
    win.getMovieFrame(buffer='back')
    win.saveMovieFrames(os.path.join("stimuli", which_monitor, "instructions_pat.png"))
    win.flip()
    core.wait(2)
    win.flip()

for times in range(1):
    control = []
    main = visual.TextStim(win, "How much control?", pos=(0, 100), color="black", height=20, wrapWidth=1000)
    scale_left = visual.TextStim(win, "No\ncontrol", pos=(-300, 0), color="black", height=20, wrapWidth=1000)
    scale_right = visual.TextStim(win, "Total\ncontrol", pos=(300, 0), color="black", height=20, wrapWidth=1000)
    scale_numbers = visual.TextStim(win, "1     2     3     4     5     6     7", pos=(0, 0), color="black", height=20, wrapWidth=1000)
    control.append(main)
    control.append(scale_left)
    control.append(scale_right)
    control.append(scale_numbers)
    control_stimulus = visual.BufferImageStim(autoLog=False, win=win, stim=control)
    control_stimulus.draw()
    win.getMovieFrame(buffer='back')
    win.saveMovieFrames(os.path.join("stimuli", which_monitor, "howMuchControl.png"))
    win.flip()
    core.wait(2)
    win.flip()

for n_blanks in range(1):
    blanks = []
    blank = visual.ImageStim(win)
    blanks.append(blank)
    blank_stimulus = visual.BufferImageStim(autoLog=False, win=win, stim=blanks)
    blank_stimulus.draw()
    win.getMovieFrame(buffer='back')
    win.saveMovieFrames(os.path.join("stimuli", which_monitor, "blank" + ".png"))
    win.flip()
    core.wait(2)
    win.flip()


