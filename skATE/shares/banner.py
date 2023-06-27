# coding=utf-8
# author xin.he

from skATE.static_info import __version__

logo = f"""\033[92m
-------------------------------------------------------------------------------
  ______                __     ______                            __            
 /_  __/_______  ____  / /_   / ____/  ___________ __   ______ _/ /_____  _____
  / / / ___/ _ \/ __ \/ __/  / __/ | |/_/ ___/ __ `/ | / / __ `/ __/ __ \/ ___/
 / / / /  /  __/ / / / /_   / /____>  </ /__/ /_/ /| |/ / /_/ / /_/ /_/ / /    
/_/ /_/   \___/_/ /_/\__/  /_____/_/|_|\___/\__,_/ |___/\__,_/\__/\____/_/     

           -- Version {__version__} --
-------------------------------------------------------------------------------\033[0m
"""


def show_logo(sleep_second=0.8):
    import time
    print(logo)
    time.sleep(sleep_second)