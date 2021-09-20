import os
import pathlib
import time
from os import environ
from utils.installer import *
from utils.shared import loaderIntro, getValidatorInfo


if __name__ == "__main__":
    envFile = pathlib.Path(dotenv_file)
    os.system("clear")
    loaderIntro()
    try:
        with envFile.open() as f:
            setupStatus = environ.get("SETUP_STATUS")
        print("* Configuration file detected, loading the validator-toolbox menu application.")
        printStars()
        time.sleep(1)
        load_dotenv(dotenv_file)
        setupStatus = environ.get("SETUP_STATUS")
        dotenv.set_key(dotenv_file, "EASY_VERSION", easyVersion)
    except OSError:
        print("* This is the first time you've launched start.py, loading config menus.")
        printStars()
        time.sleep(1)
        dotenv.set_key(dotenv_file, "SETUP_STATUS", "2")
        dotenv.set_key(dotenv_file, "EASY_VERSION", easyVersion)
    setupStatus = environ.get("SETUP_STATUS")
    checkEnvStatus(setupStatus)
    if setupStatus == "1":
        nodeType = environ.get("NODE_TYPE")
        if nodeType == "regular":
            if environ.get("VALIDATOR_WALLET") is None:
                setWalletEnv(dotenv_file, hmyAppPath, activeUserName)
            runRegularNode()
        if nodeType == "full":
            runFullNode()      
    printStars()
    print("* Initial run completed, ~/.easynode.env built.\n* Re-run python3 ~/validator-toolbox/toolbox/start.py to load management menu.")
    printStars()
