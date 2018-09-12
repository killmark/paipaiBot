import logging
from datetime import datetime
from paipaiBot import paipaiBot


class cmdHandler():
    def __init__(self, mode='1'):
        self.bot = paipaiBot(mode)
        self.date = datetime.now()

    def handle_show_time(self):
        time_format = '%H:%M:%S'
        return datetime.strptime(self.bot.getCurrentSysTime(self.bot.using_computer_time), time_format)

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
        sys_t = datetime.strptime(self.bot.getCurrentSysTime(self.bot.using_computer_time),
                                  time_format)
        print target_t
        print do_bid_time
        print sys_t
        logging.debug('bidding will be triggered at {0}'.format(self.bid_time_str(target_t)))

        while sys_t < target_t:
            #print 'current bidding time: {0}'.format(self.bid_time_str(sys_t))
            sys_t = datetime.strptime(self.bot.getCurrentSysTime(self.bot.using_computer_time), time_format)

        # Around to 100x
        amount = (int(amount) / 100) * 100
        self.bot.add_100x(amount)

        #
        # We need to finish typing the code before we click confirm
        #
        sys_t = datetime.strptime(self.bot.getCurrentSysTime(self.bot.using_computer_time),
                                  time_format)
        while(sys_t < do_bid_time):
            #print 'current bidding time: {0}'.format(self.bid_time_str(sys_t))
            sys_t = datetime.strptime(self.bot.getCurrentSysTime(self.bot.using_computer_time), time_format)

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

