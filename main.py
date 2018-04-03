import logging
import os
import pyautogui


def imPath(filename):
    return os.path.join('images', filename)


def getWindowRegion():
    logging.debug('Finding bidding system window region...')

    # identify the top-left corner
    region = pyautogui.locateOnScreen(imPath('green_wifi.png'))
    if region is None:
        raise Exception('Could not find window on screen. Is the window open?')

    # calculate the region of the entire window
    topLeftX = region[0] - 72
    topLeftY = region[1] - 23

    # the game screen is always 854 x 472
    GAME_REGION = (topLeftX, topLeftY, 854, 472)
    logging.debug('Game region found: %s' % (GAME_REGION,))

    return GAME_REGION


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)03d: %(message)s',
                        datefmt='%H:%M:%S')
    # logging.disable(logging.DEBUG) # uncomment to block debug log messages
    getWindowRegion()
