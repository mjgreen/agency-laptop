#!/home/matt/anaconda3/envs/py2/bin/python2.7
import os
from psychopy import visual, core, gui, monitors, event

myDlg = gui.Dlg(title="Set prime parameters", screen=1)
myDlg.addField("Which monitor?", choices=["e330"])
myDlg.addField("line_width_prime", choices=[2, 1,2,3,4])

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

# defensively init some vars to None
mon = None
xpx = None
ypx = None
which_screen = None
prime_size = None

# set some constants
prime_size_in_cm = 1.0
prime_horizon_adjustment_factor = 0.05

# set runtime vars
which_monitor = dlg_data[0]
win = None
if which_monitor == "e330":
    xpx = 1920
    ypx = 1080
    xcm = 31
    screen_distance = 53
    lenovo = monitors.Monitor("e330", width=xcm, distance=screen_distance)
    lenovo.saveMon()
    aspect_ratio = float(xpx) / float(ypx)  # is 1.7777777777777777, 16:9
    n_pixels_per_cm = float(xpx) / float(xcm)
    prime_size = prime_size_in_cm * n_pixels_per_cm  # prime_size var needs to be in units of pixel
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
    prime_size = prime_size_in_cm * n_pixels_per_cm  # prime_size var needs to be in units of pixel
    which_screen = 1
    win = visual.Window(fullscr=True, size=[xpx, ypx], units='pix', allowGUI=False, waitBlanking=True, color=[0, 0, 0], monitor=viewpixx, screen=which_screen)

line_width_prime = dlg_data[1]
print("\nYou chose this line width for the prime: {}".format(line_width_prime))

# set stimuli path
os.path.exists("stimuli" + os.path.sep + which_monitor) or os.makedirs("stimuli" + os.path.sep + which_monitor)

# defensively init some vars to None
north_prime_left = None
south_prime_left = None
north_prime_right = None
south_prime_right = None

# make the primes in this loop
for n_prime_loops in range(1):
    for prime_direction in ["left", "right"]:
        primes_guides_list = []
        for compass in ["north", "south"]:
            if compass in "north":
                prime_north_list = []
                prime_horizon = 1.0 * prime_size + (prime_size * prime_horizon_adjustment_factor)
                prime_zenith = 0
                prime_size = 1.0 * prime_size
                prime_half = 0.5 * prime_size
                prime_top = prime_horizon + prime_half
                prime_bottom = prime_horizon - prime_half
                prime_left_edge = - prime_half
                prime_right_edge = prime_half
                prime_box = visual.Rect(win, pos=(prime_zenith, prime_horizon), height=prime_size, width=prime_size, lineColor="yellow")
                primes_guides_list.append(prime_box)
                if prime_direction == "left" and compass in "north":
                    north_prime_left = []
                    north_chevron_l_hi_1 = visual.Line(win, start=(prime_left_edge, prime_horizon), end=(prime_zenith, prime_top), lineColor="black", lineWidth=line_width_prime)
                    north_prime_left.append(north_chevron_l_hi_1)
                    north_chevron_l_lo_1 = visual.Line(win, start=(prime_left_edge, prime_horizon), end=(prime_zenith, prime_bottom), lineColor="black", lineWidth=line_width_prime)
                    north_prime_left.append(north_chevron_l_lo_1)
                    north_chevron_l_hi_2 = visual.Line(win, start=(prime_zenith, prime_horizon), end=(prime_right_edge, prime_top), lineColor="black", lineWidth=line_width_prime)
                    north_prime_left.append(north_chevron_l_hi_2)
                    north_chevron_l_lo_2 = visual.Line(win, start=(prime_zenith, prime_horizon), end=(prime_right_edge, prime_bottom), lineColor="black", lineWidth=line_width_prime)
                    north_prime_left.append(north_chevron_l_lo_2)
                elif prime_direction == "right" and compass in "north":
                    north_prime_right = []
                    north_chevron_r_hi_1 = visual.Line(win, start=(prime_left_edge, prime_top), end=(prime_zenith, prime_horizon), lineColor="black", lineWidth=line_width_prime)
                    north_prime_right.append(north_chevron_r_hi_1)
                    north_chevron_r_lo_1 = visual.Line(win, start=(prime_left_edge, prime_bottom), end=(prime_zenith, prime_horizon), lineColor="black", lineWidth=line_width_prime)
                    north_prime_right.append(north_chevron_r_lo_1)
                    north_chevron_r_hi_2 = visual.Line(win, start=(prime_zenith, prime_top), end=(prime_right_edge, prime_horizon), lineColor="black", lineWidth=line_width_prime)
                    north_prime_right.append(north_chevron_r_hi_2)
                    north_chevron_r_lo_2 = visual.Line(win, start=(prime_zenith, prime_bottom), end=(prime_right_edge, prime_horizon), lineColor="black", lineWidth=line_width_prime)
                    north_prime_right.append(north_chevron_r_lo_2)
            elif compass in "south":
                prime_horizon = -1.0 * prime_size - (prime_size * prime_horizon_adjustment_factor)
                prime_zenith = 0
                prime_size = 1.0 * prime_size
                prime_half = 0.5 * prime_size
                prime_top = prime_horizon + prime_half
                prime_bottom = prime_horizon - prime_half
                prime_left_edge = - prime_half
                prime_right_edge = prime_half
                prime_box = visual.Rect(win, pos=(prime_zenith, prime_horizon), height=prime_size, width=prime_size, lineColor="green")
                primes_guides_list.append(prime_box)
                if prime_direction == "left" and compass in "south":
                    south_prime_left = []
                    south_chevron_l_hi_1 = visual.Line(win, start=(prime_left_edge, prime_horizon), end=(prime_zenith, prime_top), lineColor="black", lineWidth=line_width_prime)
                    south_prime_left.append(south_chevron_l_hi_1)
                    south_chevron_l_lo_1 = visual.Line(win, start=(prime_left_edge, prime_horizon), end=(prime_zenith, prime_bottom), lineColor="black", lineWidth=line_width_prime)
                    south_prime_left.append(south_chevron_l_lo_1)
                    south_chevron_l_hi_2 = visual.Line(win, start=(prime_zenith, prime_horizon), end=(prime_right_edge, prime_top), lineColor="black", lineWidth=line_width_prime)
                    south_prime_left.append(south_chevron_l_hi_2)
                    south_chevron_l_lo_2 = visual.Line(win, start=(prime_zenith, prime_horizon), end=(prime_right_edge, prime_bottom), lineColor="black", lineWidth=line_width_prime)
                    south_prime_left.append(south_chevron_l_lo_2)
                elif prime_direction == "right" and compass in "south":
                    south_prime_right = []
                    south_chevron_r_hi_1 = visual.Line(win, start=(prime_left_edge, prime_top), end=(prime_zenith, prime_horizon), lineColor="black", lineWidth=line_width_prime)
                    south_prime_right.append(south_chevron_r_hi_1)
                    south_chevron_r_lo_1 = visual.Line(win, start=(prime_left_edge, prime_bottom), end=(prime_zenith, prime_horizon), lineColor="black", lineWidth=line_width_prime)
                    south_prime_right.append(south_chevron_r_lo_1)
                    south_chevron_r_hi_2 = visual.Line(win, start=(prime_zenith, prime_top), end=(prime_right_edge, prime_horizon), lineColor="black", lineWidth=line_width_prime)
                    south_prime_right.append(south_chevron_r_hi_2)
                    south_chevron_r_lo_2 = visual.Line(win, start=(prime_zenith, prime_bottom), end=(prime_right_edge, prime_horizon), lineColor="black", lineWidth=line_width_prime)
                    south_prime_right.append(south_chevron_r_lo_2)

    # make the left-facing prime and save to disk
    prime_left = north_prime_left + south_prime_left
    prime_left_stimulus = visual.BufferImageStim(autoLog=False, win=win, stim=prime_left)
    prime_left_stimulus.draw()
    win.getMovieFrame(buffer='back')
    win.saveMovieFrames(os.path.join("stimuli", which_monitor, "prime_left" + ".png"))
    # pop the left-facing prime to screen (not needed but allows us to the what we just wrote to disk)
    txt = visual.TextStim(win, text="This is what it looks like at width {}\nPress any key to continue".format(line_width_prime), pos=(0, 250), color='black')
    txt.draw()
    win.flip()
    event.waitKeys()
    win.flip()

    # make the right-facing prime and save to disk
    prime_right = north_prime_right + south_prime_right
    prime_right_stimulus = visual.BufferImageStim(autoLog=False, win=win, stim=prime_right)
    prime_right_stimulus.draw()
    win.getMovieFrame(buffer='back')
    win.saveMovieFrames(os.path.join("stimuli", which_monitor, "prime_right" + ".png"))
    # pop the right-facing prime to screen (not needed but allows us to the what we just wrote to disk)
    txt=visual.TextStim(win,text="This is what it looks like at width {}\nPress any key to continue".format(line_width_prime), pos=(0,250), color='black')
    txt.draw()
    win.flip()
    event.waitKeys()
    win.flip()



print("")