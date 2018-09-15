import logging
import os
import time
import pyautogui
import subprocess
from PIL import Image


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

        # using_computer_time:
        # True: we directly call system time so it is more accurate
        # False: we get the time from web page
        if self.mode == '1':
            print "NOT using computer time"
            self.using_computer_time = False
        else:
            print "using computer time"
            self.using_computer_time = True

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
            'bid_number_region': (window_region[0] + 707, window_region[1] + 250),
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
            # Input Code Screen
            'input_code': (window_region[0] + 416, window_region[1] + 74, 250, 300),
        }

        return status_region

    def getCurrentSysTime(self, using_computer_time):
        if using_computer_time:
            return time.strftime("%H:%M:%S", time.gmtime())

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

    def getInputCodeScreen(self):
        # Add some delay
        time.sleep(1.0)

        input_code_region = pyautogui.screenshot(region=self.status_region['input_code'])
        tmp_f_name = './tmp/input_code_screen.png'

        input_code_region.save(tmp_f_name)

        # Enlarge image on screen
        enlarge_ratio = 3
        img = Image.open(tmp_f_name)
        img = img.resize((img.size[0] * enlarge_ratio, img.size[1] * enlarge_ratio),
                         Image.ANTIALIAS)
        img.show()

    def bid_amount(self, amount):
        '''
        Bid the amount
        '''
        logging.debug('paipaiBot::bid_amount - {0}'.format(amount))

        if self.window_region is None:
            self.locate()

        bid_number_region = self.action_cord['bid_number_region']

        pyautogui.click(bid_number_region[0], bid_number_region[1])
        pyautogui.click()
        pyautogui.press('del', presses=6)
        # Add sleep to avoid typing too fast
        time.sleep(0.2)
        pyautogui.typewrite(str(amount))

        do_bid_pos = self.action_cord['do_bid']
        pyautogui.click(do_bid_pos[0], do_bid_pos[1])


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

        # self.getInputCodeScreen()
        pyautogui.click(do_bid_pos[0] - 20, do_bid_pos[1])
        pyautogui.click(do_bid_pos[0] - 20, do_bid_pos[1])

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

        # self.getInputCodeScreen()

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
