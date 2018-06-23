import logging
import os
import pyautogui
import subprocess
import time
from datetime import datetime


class paipaiBot:
    def __init__(self, mode='1'):
        self.window_region = None
        self.action_cord = None
        self.status_region = None

        # System and bidding status
        self.cur_sys_time = None
        self.cur_lowest_bid = None
        self.cur_lowest_bid_time = None

        # Which mode we are currently running
        # 1) 51
        # 2) alltobid
        self.mode = mode

        try:
            self.locate()

        except Exception as ex:
            print str(ex)

    def locate(self):
        print 'Locating the bidding window'

        self.window_region = self.getWindowRegion()
        self.action_cord = self.getActionCord(self.window_region)
        self.status_region = self.getStatusRegion(self.window_region)

    def imPath(self, filename):
        return os.path.join('images', filename)

    def getWindowRegion(self):
        logging.debug('Finding bidding system window region...')

        # identify the top-left corner
        if self.mode == '1':
            region = pyautogui.locateOnScreen(self.imPath('title_51_dell.png'))
        elif self.mode == '2':
            region = pyautogui.locateOnScreen(self.imPath('title_alltobid_dell.png'))

        # region = pyautogui.locateOnScreen(self.imPath('title_alltobid_dell.png'))
        # region = pyautogui.locateOnScreen(self.imPath('green_wifi_51.png'))
        # region = pyautogui.locateOnScreen(self.imPath('green_wifi_alltobid.png'))

        if region is None:
            raise Exception('Could not find window on screen. \
            Is the window open?')

        # calculate the region of the entire window
        topLeftX = region[0] - 123
        topLeftY = region[1] - 26

        # the game screen is always 854 x 472
        window_region = (topLeftX, topLeftY, 854, 472)
        logging.debug('Window region found: %s' % (window_region,))

        return window_region

    def getActionCord(self, window_region):

        action_cord = {
            'add_100x': (window_region[0] + 620, window_region[1] + 145),
            'add_100x_btn': (window_region[0] + 780, window_region[1] + 142),
            'do_bid': (window_region[0] + 780, window_region[1] + 252),
            'add_100': (window_region[0] + 780, window_region[1] + 216),
            'add_200': (window_region[0] + 698, window_region[1] + 216),
            'add_300': (window_region[0] + 623, window_region[1] + 216),
            # Do bid related button
            'click_bid_ok': (window_region[0] + 528, window_region[1] + 336),
            'click_bid_cancel': (window_region[0] + 718, window_region[1] + 336),
            'click_bid_done': (window_region[0] + 638, window_region[1] + 322),
        }

        return action_cord

    def getStatusRegion(self, window_region):

        status_region = {
            'cur_sys_time': (window_region[0] + 103, window_region[1] + 226, 65, 16),
            'cur_lowest_bid': (window_region[0], window_region[1], 1, 1),
            'cur_lowest_bid_time': (window_region[0], window_region[1], 1, 1),
        }

        return status_region

    def getCurrentSysTime(self):
        if self.window_region is None:
            self.locate()

        logging.debug('Get current system time')
        cur_sys_time_region = self.status_region['cur_sys_time']
        time_im = pyautogui.screenshot(region=cur_sys_time_region)

        # TODO fix those paths
        tmp_f_name = './tmp/cur_sys_time.png'
        tmp_result_name = './tmp/cur_sys_time_result'
        time_im.save(tmp_f_name)
        cmd = '/usr/local/Cellar/tesseract/3.05.01/bin/tesseract {0} {1} -l eng --psm 7'.format(tmp_f_name, tmp_result_name)

        logging.debug('Running command: {0}'.format(cmd))
        subprocess.call(cmd.split())

        with open(tmp_result_name + '.txt', 'r') as result_fd:
            cur_sys_time = result_fd.read()
            logging.debug('Current System time: {0}'.format(cur_sys_time))

        return cur_sys_time.strip()

    def getCurrentLowestBid(self):
        # TODO
        pass

    def add_100x(self, amount):
        '''
        Add amount on top of current min bid price
        '''
        logging.debug('paipaiBot::add_100x - Increase {0}'.format(amount))

        if self.window_region is None:
            self.locate()

        add_100x_pos = self.action_cord['add_100x']
        add_100x_btn_pos = self.action_cord['add_100x_btn']

        pyautogui.click(add_100x_pos[0], add_100x_pos[1])
        pyautogui.click()
        pyautogui.press('del', presses=6)
        # Add sleep to avoid typing too fast
        time.sleep(0.2)
        pyautogui.typewrite(str(amount))
        pyautogui.click(add_100x_btn_pos[0], add_100x_btn_pos[1])
        do_bid_pos = self.action_cord['do_bid']
        pyautogui.click(do_bid_pos[0], do_bid_pos[1])

    def add_300(self):
        '''
        Click add_300 button to add 300 on
        top of current min bid price
        '''
        if self.window_region is None:
            self.locate()

        add_300_pos = self.action_cord['add_300']
        pyautogui.click(add_300_pos[0], add_300_pos[1])
        pyautogui.click()

        # click do_bid button
        do_bid_pos = self.action_cord['do_bid']
        pyautogui.click(do_bid_pos[0], do_bid_pos[1])

    def click_bid_ok_btn(self, is_ok):
        '''
        click ok after finishing typing the code
        '''
        if self.window_region is None:
            self.locate()

        btn_str = 'click_bid_ok'
        if not is_ok:
            btn_str = 'click_bid_cancel'

        click_btn = self.action_cord[btn_str]
        pyautogui.click(click_btn[0], click_btn[1])

        # Return to the main menu
        # click_btn = self.action_cord['click_bid_done']
        # time.sleep(0.3)
        # pyautogui.click()
        # pyautogui.click(click_btn[0], click_btn[1])
        # pyautogui.click(click_btn[0], click_btn[1])


class cmdHandler():
    def __init__(self, mode='1'):
        self.bot = paipaiBot(mode)
        self.date = datetime.now()

    def handle_show_time(self):
        time_format = '%H:%M:%S'
        return datetime.strptime(self.bot.getCurrentSysTime(), time_format)

    def handle_add(self, num_str):
        print 'increase current bidding price'
        if not num_str.isdigit():
            print 'Invalid command, use h[help] to see the usage'
            return -1

        # Around to 100x
        amount = (int(num_str) / 100) * 100
        self.bot.add_100x(amount)

        return 0

    def handle_timer_add_wrapper(self, target_time_str, amount, do_bid_time=None):
        if ':' not in target_time_str:
            target_time_str = '11:29:{0}'.format(target_time_str)

        if do_bid_time and ':' not in do_bid_time:
            do_bid_time = '11:29:{0}'.format(do_bid_time)

        return self.handle_timer_add(target_time_str, amount, do_bid_time=do_bid_time)

    def handle_timer_add(self, target_time_str, amount, do_bid_time=None):
        print 'increase price by {0} at {1}'.format(amount, target_time_str)
        time_format = '%H:%M:%S'
        target_t = datetime.strptime(target_time_str, time_format)
        do_bid_time = datetime.strptime(do_bid_time, time_format)
        sys_t = datetime.strptime(self.bot.getCurrentSysTime(),
                                  time_format)
        logging.debug('bidding will be triggered at {0}'.format(self.bid_time_str(target_t)))

        while sys_t < target_t:
            print 'current bidding time: {0}'.format(self.bid_time_str(sys_t))
            sys_t = datetime.strptime(self.bot.getCurrentSysTime(), time_format)

        # Around to 100x
        amount = (int(amount) / 100) * 100
        self.bot.add_100x(amount)

        #
        # We need to finish typing the code before we click confirm
        #
        sys_t = datetime.strptime(self.bot.getCurrentSysTime(),
                                  time_format)
        while(sys_t < do_bid_time):
            print 'current bidding time: {0}'.format(self.bid_time_str(sys_t))
            sys_t = datetime.strptime(self.bot.getCurrentSysTime(), time_format)

        # Click bid button
        self.bot.click_bid_ok_btn(True)

    def bid_time_str(self, date):
        '''
        Adjust the year month and day to
        the correct value
        '''
        return date.replace(year=self.date.year,
                            month=self.date.month,
                            day=self.date.day)


def main():
    logging.debug('Paipai - xjin')
    help_txt = '''
    Commands:
    h[help]: help information
    a[add] increase_amount: increase price on top of current minimum value
                            if increase_amount is not there or invalid, we will
                            just increase 300
                            e.g a 300
    t[timer] increase_time increase_amount bid_time[optional]: increase price on top of minimum value on
                                                               specific time (HH:MM:SS). We can only set
                                                               one timer job instance a time
                                                               if increase_amount is not there or invalid, we will
                                                               just increase 300
                                                               e.g t [11:59:]45 600 [11:59:]55
    r[relocate] relocate the bidding window
    exit[quit]: exit the program
    '''

    print '-----------Paipai-----------'
    print 'Copyright (C) 2018 Xiaoyu Jin'
    print 'All rights reserved'
    print '----------------------------'
    print help_txt

    # We have 51 or alltobid, two simulation systems
    # We may have the official one if alltobid simulation
    # is different from the offical system
    running_mode = raw_input('''
    Which mode?
    1) 51
    2) alltobid\n''')
    if running_mode != '1' and running_mode != '2':
        print 'Mode {0} is invalid'.format(running_mode)
        print 'Default mode 1 is chosen'
        running_mode = '1'

    print "Mode {0} is running".format(running_mode)

    # Main loop
    cmd = None
    cmd_handler = cmdHandler(running_mode)

    while True:
        cmd_arr = raw_input('> ').split()

        if len(cmd_arr) <= 0:
            continue

        cmd = cmd_arr[0]
        try:
            if cmd == 'h' or cmd == 'help':
                print help_txt

            elif cmd == 'a' or cmd == 'add':
                if len(cmd_arr) > 2:
                    print 'Invalid command, use h[help] to see the usage'
                elif len(cmd_arr) == 2:
                    cmd_handler.handle_add(cmd_arr[1])
                else:
                    cmd_handler.handle_add('300')

            elif cmd == 't' or cmd == 'timer':
                if len(cmd_arr) == 1:
                    # We just show the current time
                    # if we are using system time mode, we would show
                    # the adjusted bidding time
                    print cmd_handler.handle_show_time()
                    continue

                if len(cmd_arr) < 3:
                    print 'Invalid command, use h[help] to see the usage'
                    continue

                do_bid_time = None
                if len(cmd_arr) > 3:
                    do_bid_time = cmd_arr[3]

                cmd_handler.handle_timer_add_wrapper(cmd_arr[1], cmd_arr[2], do_bid_time=do_bid_time)

            elif cmd == 'r' or cmd == 'relocate':
                cmd_handler.bot.locate()

            elif cmd == 'exit' or cmd == 'quit':
                print 'quit the program...'
                break
            else:
                print 'Invalid command!\nUsing h[help] to check the manual'

        except Exception as ex:
            print str(ex)

    print 'Bye...'


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        #level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d: %(message)s',
                        datefmt='%H:%M:%S')
    # logging.disable(logging.DEBUG) # uncomment to block debug log messages
    # bot = paipaiBot()
    # bot.test_add_300()
    # bot.test_add_100x()
    # bot.getCurrentSysTime()
    main()
