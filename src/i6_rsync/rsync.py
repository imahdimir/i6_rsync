import os
import pathlib

import pyperclip


def make_rsync_cmds_and_copy_desired_one_to_clipboard_and_execute(hostname: str ,
                                                                  remote: pathlib.Path ,
                                                                  local: pathlib.Path ,
                                                                  cmd_number_to_cp_clipboard = None ,
                                                                  execute = False
                                                                  ) :
    """
    rsync should be installed on both local and remote machines.
    host should be accessible via ssh f'{hostname}' (by setting up ssk key and ssh config)

    parameters:
    hostname: should be known to local machine and accessible via ssh hostname (ssh key and ssh confige must be set up)
    local: Path to the local directory where files will be synced to/from
    remote: Path to the remote directory where files will be synced to/from
    cmd_number_to_cp_clipboard: int, optional
        -If provided, the corresponding rsync command will be copied to clipboard so it can be easily pasted into a terminal for execution and if execute is True, it will be executed direvctly in the terminal by running the current function.
        1: sync from remote to local
        2: sync from local to remote
        3: sync from remote to local with delete option (remove files in local not present in remote)
        4: sync from local to remote with delete option (remove files in remote not present in local)
    execute: bool, optional, if True, the selected (the one to be copied to clipboard) rsync command will be executed directly in the terminal.
    """

    cmds = {}

    print("1. sync from remote to local")
    cmds[1] = f"rsync -avz {hostname}:{remote}/ {local}"
    print(cmds[1] , '\n')

    print("2. sync from local to remote")
    cmds[2] = f"rsync -avz {local}/ {hostname}:{remote}"
    print(cmds[2] , '\n')

    _msg = '3. sync from remote to local with delete option (remove files in local not present in remote)'
    print(_msg , '\n')
    cmds[3] = f"rsync -avz --delete {hostname}:{remote}/ {local}"
    print(cmds[3] , '\n')

    _msg = '4. sync from local to remote with delete option (remove files in remote not present in local)'
    print(_msg , '\n')
    cmds[4] = f"rsync -avz --delete {local}/ {hostname}:{remote}"
    print(cmds[4] , '\n')

    if cmd_number_to_cp_clipboard is not None :
        pyperclip.copy(cmds[cmd_number_to_cp_clipboard])

        _msg = f"Command {cmd_number_to_cp_clipboard} copied to clipboard."
        print(_msg , "\n")

        if execute :
            print("Executing the command...")

            exit_status = os.system(cmds[cmd_number_to_cp_clipboard])

            # Check the exit status
            if exit_status == 0 :
                print("\nCommand executed successfully.\n")
            else :
                _msg = '\nCommand failed with exit status:\n'
                print(_msg , exit_status , "\n")

        else :
            _msg = 'Run the desired cmd (might have been copied in clipboard) in local terminal to execute the rsync command.'
            print(_msg)
