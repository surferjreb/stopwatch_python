# A simple stopwatch script

from datetime import datetime
from multiprocessing import Process, Event, Manager
import logging
import subprocess
import argparse
import time


# Setup logging for the script
logging.basicConfig(filename='loggy.log',
                level=logging.INFO,
                format='%(asctime)s %(message)s')
    
logger = logging.getLogger(__name__)


def single_timer(start_time, stop_event):
    '''Is a single timer, the stop_event causes the loop
    to exit.'''
    while not stop_event.is_set():
        display_timer(start_time)
        time.sleep(0.001)

    elap_time = datetime.now() - start_time
    logger.info(f"Total Time: {elap_time}")
    print(f"Final time: {elap_time}")

def arg_timer(start_time, arg, ex_times):
    '''Times the execution of the commands, then updates the dict'''
    try:
        subprocess.run(arg, shell=True)
        elap_time = datetime.now() - start_time
        ex_times.update({arg: elap_time})
    except Exception as err:
        logger.error(f"{err.__context__} in arg timer")

def display_timer(start_time):
    '''Displays time to console for single timer'''
    elap_time = datetime.now() - start_time
    print(f"\rtime: {elap_time}", end="\r")

def time_commands(args):
    '''Starts the timing process for command timing'''

    # A Manager was used here in order to update the dict between
    # child and parent.  
    with Manager() as manager:
        ex_times = manager.dict()
        for arg in args.command:
            start_time = datetime.now()
            p = Process(target=arg_timer,
                        args=(start_time, arg, ex_times))
            p.start()
            p.join()

        for key,value in ex_times.items():
            logger.info(f"Command: \"{key}\" executed in: {value}")
            print(f"{key} executed in: {value}")

def run_single_timer():
    '''Runs Single Timer'''
    start_time = datetime.now()
    # Event is shared amongs the processes
    stop_event=Event()
    print("Timer Started")
    print("=======================================================")
    start_time = datetime.now()
    # Setup process to run
    p = Process(target=single_timer, args=(start_time, stop_event))
    print("Press return or enter to stop....")
    p.start()
    input()
    '''After user presses enter, the event is set causing the loop to 
    terminate in the running process.''' 
    stop_event.set()
    p.join()

def main():
    '''Uses argparse to get command line arguments.  Can also be used to 
    setup a menu for command line help instruction.'''
    parser = argparse.ArgumentParser(
        description='Time command line execution')
    parser.add_argument('-c', '--command',
                        metavar='command',
                        action='extend',
                        nargs='*',
                        type=str,
                        help='when present will time the execution of cmd/s'
                        )
    args = parser.parse_args()

    if args.command != None:
        time_commands(args)
    else:
        run_timer()


if __name__ == '__main__':
    main()
