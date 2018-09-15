import logging
import readline
from paipaiHelper import cmdHandler


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
    b[bid] increase_time bid_number bid_time[optional]: bid the price on specific time.
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
    2) alltobid
    with alltobid, we will use system time instead of on-screen time by default\n''')

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
                else:
                    do_bid_time = "58"

                cmd_handler.handle_timer_wrapper(cmd_arr[1], cmd_arr[2], do_bid_time, True)

            elif cmd == 'b' or cmd == 'bid':
                if len(cmd_arr) < 3:
                    print 'Invalid command, use h[help] to see the usage'
                    continue

                do_bid_time = None
                if len(cmd_arr) > 3:
                    do_bid_time = cmd_arr[3]
                else:
                    do_bid_time = '58'
                
                cmd_handler.handle_timer_wrapper(cmd_arr[1], cmd_arr[2], do_bid_time, False)

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
                        # level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d: %(message)s',
                        datefmt='%H:%M:%S')
    # logging.disable(logging.DEBUG) # uncomment to block debug log messages
    # bot = paipaiBot()
    # bot.test_add_300()
    # bot.test_add_100x()
    # bot.getCurrentSysTime()

    # Enable Up/Down/C-p/C-n
    readline.parse_and_bind('"\\C-p": previous-history')
    readline.parse_and_bind('"\\C-n": next-history')
    readline.parse_and_bind('"\\e[A": previous-history')
    readline.parse_and_bind('"\\e[B": next-history')
    main()
