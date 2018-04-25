import logging
import os
import pyautogui
import subprocess
# import time


class paipaiBot:
    def __init__(self):
        self.window_region = self.getWindowRegion()
        self.action_cord = self.getActionCord(self.window_region)
        self.status_region = self.getStatusRegion(self.window_region)

        # System and bidding status
        self.cur_sys_time = None
        self.cur_lowest_bid = None
        self.cur_lowest_bid_time = None

    def imPath(self, filename):
        return os.path.join('images', filename)

    def getWindowRegion(self):
        logging.debug('Finding bidding system window region...')

        # identify the top-left corner
        region = pyautogui.locateOnScreen(self.imPath('green_wifi_51.png'))
        # region = pyautogui.locateOnScreen(self.imPath('green_wifi_alltobid.png'))

        if region is None:
            raise Exception('Could not find window on screen. \
            Is the window open?')

        # calculate the region of the entire window
        topLeftX = region[0] - 72
        topLeftY = region[1] - 23

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
        }

        return action_cord

    def getStatusRegion(self, window_region):

        status_region = {
            'cur_sys_time': (window_region[0] + 103, window_region[1] + 226, 65, 16),
            'cur_lowest_bid': (window_region[0], window_region[1], 1, 1), # TODO
            'cur_lowest_bid_time': (window_region[0], window_region[1], 1, 1), # TODO
        }

        return status_region

    def getCurrentSysTime(self):
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

    def getCurrentLowestBid(self):
        # TODO
        pass

    # Test Functions
    # TODO move them out of this class

    def test_add_300(self):
        # click add_300 button
        add_300_pos = self.action_cord['add_300']
        pyautogui.click(add_300_pos[0], add_300_pos[1])
        pyautogui.click()

        # click do_bid button
        do_bid_pos = self.action_cord['do_bid']
        pyautogui.click(do_bid_pos[0], do_bid_pos[1])

    def test_add_100x(self):
        add_100x_pos = self.action_cord['add_100x']
        add_100x_btn_pos = self.action_cord['add_100x_btn']

        pyautogui.click(add_100x_pos[0], add_100x_pos[1])
        pyautogui.click()
        pyautogui.press('del', presses=5)
        pyautogui.typewrite('400')
        pyautogui.click(add_100x_btn_pos[0], add_100x_btn_pos[1])
        do_bid_pos = self.action_cord['do_bid']
        pyautogui.click(do_bid_pos[0], do_bid_pos[1])

    def add_100x(self, amount):
        '''
        Add amount on top of current min bid price
        '''
        logging.debug('paipaiBot::add_100x - Increase {0}'.format(amount))
        add_100x_pos = self.action_cord['add_100x']
        add_100x_btn_pos = self.action_cord['add_100x_btn']

        pyautogui.click(add_100x_pos[0], add_100x_pos[1])
        pyautogui.click()
        pyautogui.press('del', presses=5)
        pyautogui.typewrite(str(amount))
        pyautogui.click(add_100x_btn_pos[0], add_100x_btn_pos[1])
        do_bid_pos = self.action_cord['do_bid']
        pyautogui.click(do_bid_pos[0], do_bid_pos[1])

    def add_300(self):
        '''
        Click add_300 button to add 300 on
        top of current min bid price
        '''
        add_300_pos = self.action_cord['add_300']
        pyautogui.click(add_300_pos[0], add_300_pos[1])
        pyautogui.click()

        # click do_bid button
        do_bid_pos = self.action_cord['do_bid']
        pyautogui.click(do_bid_pos[0], do_bid_pos[1])


class cmdHandler():
    def __init__(self):
        self.bot = paipaiBot()

    def handle_add(self, num_str):
        print 'increase current bidding price'
        if not num_str.isdigit():
            print 'Invalid command, use h[help] to see the usage'
            return -1

        # Around to 100x
        amount = (int(num_str) / 100) * 100
        self.bot.add_100x(amount)

        return 0


def main():
    logging.debug('Paipai - xjin')
    help_txt = '''
    Commands:
    h[help]: help information
    a[add] increase_amount: increase price on top of current minimum value
                            if increase_amount is not there or invalid, we will
                            just increase 300
                            e.g a 300
    t[timer] time increase_amount: increase price on top of minimum value on
                                   specific time (HH:MM:SS). We can only set
                                   one timer job instance a time
                                   if increase_amount is not there or invalid, we will
                                   just increase 300
                                   e.g t 11:59:45 600
    q[quit]: exit the program
    '''

    print '-----------Paipai-----------'
    print 'Copyright (C) 2018 Xiaoyu Jin'
    print 'All rights reserved'
    print '----------------------------'
    print help_txt

    # Main loop
    cmd = None
    cmd_handler = cmdHandler()
    while cmd != 'quit' and cmd != 'q':
        cmd_arr = raw_input('> ').split()

        if len(cmd_arr) <= 0:
            continue

        cmd = cmd_arr[0]
        if cmd == 'h' or cmd == 'help':
            print help_txt

        elif cmd == 'a' or cmd == 'add':
            if len(cmd_arr) > 2:
                print 'Invalid command, use h[help] to see the usage'
            elif len(cmd_arr) == 1:
                cmd_handler.handle_add(cmd_arr[1])
            else:
                cmd_handler.handle_add('300')

        elif cmd == 't' or cmd == 'timer':
            print 'set a timer and automatically increase the price by certain amount'

        elif cmd == 'q' or cmd == 'quit':
            print 'quit the program...'

        else:
            print 'Invalid command!\nUsing h[help] to check the manual'

    print 'Bye...'


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)03d: %(message)s',
                        datefmt='%H:%M:%S')
    # logging.disable(logging.DEBUG) # uncomment to block debug log messages
    # bot = paipaiBot()
    # bot.test_add_300()
    # bot.test_add_100x()
    # bot.getCurrentSysTime()
    main()
