import os
from os import environ
from toolbox.config import easy_env
from toolbox.library import loader_intro, set_wallet_env, load_var_file, passphrase_status, set_var, version_checks, recheck_vars, recover_wallet, update_text_file
from toolbox.toolbox import run_regular_node, run_full_node, refresh_stats, safety_defaults

if __name__ == "__main__":
    # clear screen, show logo
    loader_intro()
    # check for .env file, if none we have a first timer.
    if os.path.exists(easy_env.dotenv_file) is None:
        # they should run the installer, goodbye!
        print("Install Harmony First!!!\nRun python3 ~/validatortoolboxinstall.py")
        raise SystemExit(0)
    # passed .env check, let's load it!
    load_var_file(easy_env.dotenv_file)
    # This section is for hard coding new settings for current users.
    safety_defaults()
    # always set conf to 13 keys, shard max
    if os.path.exists(easy_env.harmony_conf): update_text_file(easy_env.harmony_conf, "MaxKeys = 10", "MaxKeys = 13")
    # Make sure they have a wallet or wallet address in the .env file, if none, get one.
    if environ.get("VALIDATOR_WALLET") is None:
        recover_wallet()
        if environ.get("VALIDATOR_WALLET") is None:
            print(
                "* You don't currently have a validator wallet address loaded in your .env file, please edit ~/.easynode.env and add a line with the following info:\n "
                + "* VALIDATOR_WALLET='validatorONEaddress' "
            )
            input("* Press any key to exit.")
            raise SystemExit(0)
    # Check online versions of harmony & hmy and compare to our local copy.
    refresh_stats(1)
    software_versions = version_checks(easy_env.harmony_folder_name)
    # Last check on setup status, if it never finished it will try again here.
    if environ.get("SETUP_STATUS") != "2":
        recheck_vars()
        passphrase_status()
    # Run regular validator node
    if environ.get("NODE_TYPE") == "regular":
        if environ.get("VALIDATOR_WALLET") is None:
            set_wallet_env()
        run_regular_node(software_versions)
    # Run full node
    if environ.get("NODE_TYPE") == "full":
        run_full_node()
    print("Uh oh, you broke me! Contact Easy Node")
    raise SystemExit(0)