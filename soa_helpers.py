import os
import random
from psychopy import core, event #visual, event, core, parallel

def get_response_to_mask(autopilot=False, win=None, results_directory=None):
    event.clearEvents(eventType='keyboard')
    if autopilot:
        response_button = random.sample(['d', 'l'], 1)[0]
        response_time = random.random()
        core.wait(secs=random.uniform(.500, .501))
        return response_button, response_time
    t0 = core.getTime()
    while True:
        k = event.getKeys(timeStamped=True, keyList=['d', 'l', 'escape'])
        if k and k[0][0] in ['d', 'l']:
            response_button = k[0][0]
            response_timestamp = k[0][1]
            response_time = (response_timestamp - t0) * 1000.0  # milliseconds
            return response_button, response_time
        elif k and k[0][0] == 'escape':
            msg = "user pressed escape"
            print(msg)
            endex(win, results_directory)

def get_response_for_rating(autopilot=False, win=None, results_directory=None, dur_wait_for_rating=None):
    event.clearEvents(eventType='keyboard')
    if autopilot:
        k = random.sample(['d', 'f', 'g', 'h', 'j', 'k', 'l'], 1)[0]
        response_button = 1 if k[0][0] == 'd' else 2 if k[0][0] == 'f' else 3 if k[0][0] == 'g' else 4 if k[0][0] == 'h' else 5 if k[0][0] == 'j' else 6 if k[0][0] == 'k' else 7 if k[0][0] == 'l' else None
        response_time = random.random()
        core.wait(secs=dur_wait_for_rating)
        return response_button, response_time
    t0 = core.getTime()
    while True:
        k = event.getKeys(timeStamped=True, keyList=['d', 'f', 'g', 'h', 'j', 'k', 'l', 'escape'])
        if k and k[0][0] in ['d', 'f', 'g', 'h', 'j', 'k', 'l']:
            response_button = 1 if k[0][0] == 'd' else 2 if k[0][0] == 'f' else 3 if k[0][0] == 'g' else 4 if k[0][0] == 'h' else 5 if k[0][0] == 'j' else 6 if k[0][0] == 'k' else 7 if k[0][0] == 'l' else None
            response_timestamp = k[0][1]
            response_time = (response_timestamp - t0) * 1000.0  # milliseconds
            return response_button, response_time
        elif k and k[0][0] == 'escape':
            msg = "user pressed escape"
            print(msg)
            endex(win, results_directory)

def get_response_for_ibi(autopilot=False, win=None, results_directory=None):
    event.clearEvents(eventType='keyboard')
    if autopilot:
        response_button = 'space'
        response_time = random.random()
        return response_button, response_time
    t0 = core.getTime()
    while True:
        k = event.getKeys(timeStamped=True, keyList=['space', 'escape'])
        if k and k[0][0] == 'space':
            response_button = k[0][0]
            response_timestamp = k[0][1]
            response_time = (response_timestamp - t0) * 1000.0  # milliseconds
            return response_button, response_time
        elif k and k[0][0] == 'escape':
            msg = "user pressed escape"
            print(msg)
            endex(win, results_directory)

def endex(win=None, results_directory=None):
    import subprocess
    import gc
    from psychopy import logging

    # save frame intervals to this subject's results folder
    win.saveFrameIntervals(fileName=os.path.join(results_directory, "lastFrameIntervals.log"), clear=True)

    # garbage collection on again
    gc.enable()

    # lower thread priority
    core.rush(False)

    # flush the logs
    logging.flush()

    # print various useful summary things at the end of the experiment
    summary_strings = []
    cmd = "git branch -v"
    output = subprocess.getoutput(cmd)
    msg = "versioning information: \"{}\" yields \"{}\"".format(cmd, output)
    summary_strings.append(msg)
    for s in summary_strings:
        print(s)

    # quit psychopy
    win.close()
    core.quit()


# def get_parallel_port_address():
#     if platform.system() == 'Linux':
#         try:
#             parallel_port = parallel.ParallelPort(address='/dev/parport0')
#             print(parallel_port)
#         except OSError:
#             print("Parallel port cock-up: No such device or address: '/dev/parport0': " +
#                   "Did you run 'sudo rmmod lp ; sudo modprobe ppdev' yet?: " +
#                   "Did you do 'sudo adduser matt lp' to get access to the port?\n")
#             core.quit()
#             # there_is_a_parallel_port = False
#             # parallel_port = None
#             # return there_is_a_parallel_port, parallel_port
#         else:
#             there_is_a_parallel_port = True
#             return there_is_a_parallel_port, parallel_port
#     elif platform.system() == 'Windows':
#         try:
#             parallel_port = parallel.ParallelPort(address=0x1FF8)  # eeg z440
#             psychopy.logging.flush()
#         except RuntimeError:
#             print("Parallel port cock-up:\n" +
#                   "On Windows, 64bit Python can't use inpout32's parallel port driver, which cocks everything up.\n" +
#                   "The solution is to use 32 bit python instead. Build psychopy using pip from the 32 bit python.\n" +
#                   "Make sure inpout32.dll is in the toplevel at runtime.\n")
#             there_is_a_parallel_port = False
#             parallel_port = None
#             return there_is_a_parallel_port, parallel_port
#         else:
#             there_is_a_parallel_port = True
#             return there_is_a_parallel_port, parallel_port
