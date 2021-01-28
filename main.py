import PySimpleGUI as sg
import SAMtools as sam # todo finish SAMtools
import configparser


SAM = configparser.ConfigParser()
SAM.read('SAM.cfg')

def main():  # Initial window, disclaimer

    layout = [
        [
            sg.Text(
                "Welcome to Steward/Sysop Action Module!",
                font=("Helvetica", 16),
                size=(40, 1),
                justification='c'
            )
        ],
        [
            sg.Text(
                "By using this module, you accept responsibility for your actions...",
                justification='c',
                size=(60, 1),
            )
        ],
        [
            sg.Text(
                "and mistakes.",
                justification='c',
                size=(60, 1),
            )
        ],
        [
            sg.Button("I accept")
        ],
        [
            sg.Text(
                "By Operator873",
                size=(80, 1),
                justification='r',
                font=("Helvetica", 8),
                text_color="light gray"
            )
        ]
    ]

    start_window = sg.Window("Steward/Sysop Action Module", layout)

    start_window.Read()

    start_window.close()

    start_sam()


def start_sam():  # Main menu window
    
    if (
        SAM['OAuth']['consumer_token'] != "" and
        SAM['OAuth']['consumer_secret'] != "" and
        SAM['OAuth']['access_token'] != "" and
        SAM['OAuth']['access_secret'] != ""
    ):
        layout = [
            [
                sg.Text("Blocks")
            ],
            [
                sg.Button("Block", key='block'),
                sg.Button("Hard block", key='hardblock'),
                sg.Button("Spam bot block", key='spambot'),
                sg.Button("Global block", key='gblock')
            ],
            [
                sg.Text("Modify a block")
            ],
            [
                sg.Button("Change block", key='reblock'),
                sg.Button("Revoke TPA", key='tpa')
            ],
            [
                sg.Text("CentralAuth")
            ],
            [
                sg.Button("Lock", key='lock'),
                sg.Button("Unlock", key='unlock')
            ],
            [
                sg.Text("Mass actions (Coming soon)")
            ],
            [
                sg.Button("Mass Block", key='massblock', disabled=True),
                sg.Button("Mass Global Block", key='massgblock', disabled=True),
                sg.Button("Mass Lock", key='masslock', disabled=True)
            ],
            [
                sg.Text("Setup options")
            ],
            [
                sg.Button("Setup OAuth", key='oauth'),
                sg.Button("Add Project/API", key='addapi')
            ],
            [
                sg.Text(
                    "By Operator873",
                    size=(60, 1),
                    justification='r',
                    font=("Helvetica", 8),
                    text_color="light gray"
                )
            ]
        ]
    else:
        layout = [
            [
                sg.Text("Blocks")
            ],
            [
                sg.Button("Block", key='block', disabled=True),
                sg.Button("Hard block", key='hardblock', disabled=True),
                sg.Button("Spam bot block", key='spambot', disabled=True),
                sg.Button("Global block", key='gblock', disabled=True)
            ],
            [
                sg.Text("CentralAuth")
            ],
            [
                sg.Button("Lock", key='lock', disabled=True),
                sg.Button("Unlock", key='unlock', disabled=True)
            ],
            [
                sg.Text("Mass actions")
            ],
            [
                sg.Button("Mass Block", key='massblock', disabled=True),
                sg.Button("Mass Global Block", key='massgblock', disabled=True),
                sg.Button("Mass Lock", key='masslock', disabled=True)
            ],
            [
                sg.Text("Setup options")
            ],
            [
                sg.Button("Setup OAuth", key='oauth'),
                sg.Button("Add Project/API", key='addapi', disabled=True)
            ],
            [
                sg.Text(
                    "By Operator873",
                    size=(60, 1),
                    justification='r',
                    font=("Helvetica", 8),
                    text_color="light gray"
                )
            ]
        ]

    sam_window = sg.Window("Steward/Sysop Action Module", layout)

    while True:
        event, values = sam_window.Read()
        #  print("Event: " + event + " || Values: " + str(values)) # For debugging only
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "block":
            get_block()
        elif event == "hardblock":
            get_hardblock()
        elif event == "spambot":
            get_spambot()
        elif event == "lock":
            get_lock()
        elif event == "unlock":
            get_unlock()
        elif event == "gblock":
            get_globalblock()
        elif event == "massblock":
            get_massblock()
        elif event == "massgblock":
            get_massgblock()
        elif event == "masslock":
            get_masslock()
        elif event == "oauth":
            get_oauth()
        elif event == "addapi":
            get_addapi()
        elif event == "reblock":
            get_reblock()
        elif event == "tpa":
            get_revoketpa()
        elif event == "":
            sg.Popup("You kinda have to chose something...", title="PEBKAC Error!")
        else:
            sg.Popup("An unknown selection was received. Try again.", title="Unknown error!")


def get_block():  # GUI for executing a regular block

    block_layout = [
        [
            sg.Text(
                "Block Account/IP",
                font=("Helvetica", 25),
                justification='c',
                size=(25, 1),
                text_color="red"
            )
        ],
        [
            sg.Text(
                "Apply a standard block with no autoblock active.",
                size=(60, 1),
                text_color="light gray",
                justification='c'
            )
        ],
        [
            sg.Text("Enter account or IP:", size=(15, 1), justification='r'),
            sg.InputText(key='target')
        ],
        [
            sg.Text("Enter reason:", size=(15, 1), justification='r'),
            sg.InputText(key='reason')
        ],
        [
            sg.Text("Enter duration:", size=(15, 1), justification='r'),
            sg.InputText(key='duration', size=(15, 1)),
            sg.Text("Enter project:", size=(10, 1), justification='r'),
            sg.InputText(key='project', default_text=SAM['HomeWiki']['homewiki'], size=(15, 1))
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop"),
            sg.Checkbox('Global Sysop action', default=False, key='gs'),
            sg.Checkbox('Steward action', default=False, key='steward')
        ],
        [
            sg.Text(
                "Valid duration examples: 3 days, 5months, indef, forever",
                size=(60, 1),
                justification='c',
                text_color="blue"
            )
        ]
    ]

    block_window = sg.Window("SAM: Apply block", block_layout)

    while True:
        block_event, block_values = block_window.Read()

        if block_event == "Exit" or block_event == sg.WIN_CLOSED:
            break
        elif block_event == "stop":
            block_window.close()
            break
        else:
            if (
                    block_values['target'] == "" or
                    block_values['reason'] == "" or
                    block_values['duration'] == "" or
                    block_values['project'] == ""
            ):
                sg.Popup("Target, reason, duration, and project are required!!", title="Input Error!")
            elif block_values['project'].lower() == "examplewiki":
                sg.Popup(
                    "examplewiki is not a real wiki. Please select an appropriate project.",
                    title="Project error!"
                )
            else:
                work = sam.block(SAM, block_values)
                if work['status'] == "Success":
                    sg.Popup(work['message'], title="Success!")
                else:
                    sg.Popup(work['message'], title="Failed!!")
                block_window.close()
                break


def get_hardblock():  # GUI for executing a hard block

    hblock_layout = [
        [
            sg.Text(
                "Hardblock Account/IP",
                font=("Helvetica", 25),
                justification='c',
                size=(25, 1),
                text_color="red"
            )
        ],
        [
            sg.Text(
                "Apply a block with no email and no talk page access and autoblock active.",
                size=(60, 1),
                text_color="light gray",
                justification='c'
            )
        ],
        [
            sg.Text("Enter account or IP:", size=(15, 1), justification='r'),
            sg.InputText(key='target')
        ],
        [
            sg.Text("Enter reason:", size=(15, 1), justification='r'),
            sg.InputText(key='reason')
        ],
        [
            sg.Text("Enter duration:", size=(15, 1), justification='r'),
            sg.InputText(key='duration', size=(15, 1)),
            sg.Text("Enter project:", size=(10, 1), justification='r'),
            sg.InputText(key='project', default_text=SAM['HomeWiki']['homewiki'], size=(15, 1))
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop"),
            sg.Checkbox('Global Sysop action', default=False, key='gs'),
            sg.Checkbox('Steward action', default=False, key='steward')
        ],
        [
            sg.Text(
                "Valid duration examples: 3 days, 5months, indef, forever",
                size=(60, 1),
                justification='c',
                text_color="blue"
            )
        ]
    ]

    hblock_window = sg.Window("SAM: Apply Hardblock", hblock_layout)

    while True:
        block_event, block_values = hblock_window.Read()
        print(block_values)
        if block_event == "Exit" or block_event == sg.WIN_CLOSED:
            break
        elif block_event == "stop":
            hblock_window.close()
            break
        else:
            if (
                    block_values['target'] == "" or
                    block_values['reason'] == "" or
                    block_values['duration'] == "" or
                    block_values['project'] == ""
            ):
                sg.Popup("Target, reason, duration, and project are required!!", title="Input Error!")
            elif block_values['project'].lower() == "examplewiki":
                sg.Popup(
                    "examplewiki is not a real wiki. Please select an appropriate project.",
                    title="Project error!"
                )
            elif block_values['gs'] is True and block_values['steward'] is True:
                sg.Popup(
                    "Please only select Global sysop action or Steward action, not both.",
                    title="Error!"
                )
            else:
                result = sam.hardblock(SAM, block_values)
                if result['status'] == "Success":
                    sg.Popup(
                        result['message'],
                        title="Block successful!"
                    )
                else:
                    sg.Popup(
                        "Error! " + result['message'] + " Please try again.",
                        title="Block Failed!"
                    )
                hblock_window.close()
                break


def get_spambot():  # GUI for blocking Spambot

    block_layout = [
        [
            sg.Text(
                "Spambot Block",
                font=("Helvetica", 25),
                justification='c',
                size=(25, 1),
                text_color="red"
            )
        ],
        [
            sg.Text(
                "Applies an indef block with no tpa or email access.",
                size=(60, 1),
                text_color="light gray",
                justification='c'
            )
        ],
        [
            sg.Text("Enter account:", size=(15, 1), justification='r'),
            sg.InputText(key='target')
        ],
        [
            sg.Text("Enter project:", size=(15, 1), justification='r'),
            sg.InputText(key='project', default_text=SAM['HomeWiki']['homewiki'], size=(15, 1))
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop"),
            sg.Checkbox('Global Sysop action', default=False, key='gs'),
            sg.Checkbox('Steward action', default=False, key='steward')
        ]
    ]

    block_window = sg.Window("SAM: Apply Spambot block", block_layout)

    while True:
        block_event, block_values = block_window.Read()

        if block_event == "Exit" or block_event == sg.WIN_CLOSED:
            break
        elif block_event == "stop":
            block_window.close()
            break
        else:
            if (
                    block_values['target'] == "" or
                    block_values['project'] == ""
            ):
                sg.Popup("Target and project are required!!", title="Input Error!")
            elif block_values['project'].lower() == "examplewiki":
                sg.Popup(
                    "examplewiki is not a real wiki. Please select an appropriate project.",
                    title="Project error!"
                )
            else:
                result = sam.spambot(SAM, block_values)
                if result['status'] == "Success":
                    sg.Popup(
                        result['message'],
                        title="Block successful!"
                    )
                else:
                    sg.Popup(
                        "Error! " + result['message'] + " Please try again.",
                        title="Block Failed!"
                    )
                block_window.close()
                break


def get_reblock():  # GUI for changing a block

    intel = [
        [
            sg.Text("Reblock target:", size=(12, 1), justification='r'),
            sg.InputText(key='target', size=(20, 1))
        ],
        [
            sg.Text("Enter project:", size=(12, 1), justification='r'),
            sg.InputText(key='project', size=(20, 1))
        ],
        [
            sg.Submit(),
            sg.Cancel(key='stop')
        ]
    ]

    intel_window = sg.Window("SAM: Reblock", intel)

    while True:
        intel_event, intel_values = intel_window.Read()

        if (
            intel_event == "Exit" or
            intel_event == sg.WIN_CLOSED or
            intel_event == 'stop'
        ):
            info = None
            break
        else:
            info = sam.blockinfo(sam.get_creds(SAM), intel_values)
            break

    intel_window.close()

    if info is None:
        return
    elif info['status'] == "notblocked":
        sg.Popup(
            "That Account/IP is not currently blocked. Exiting...",
            title="Status error!"
        )
    elif info['status'] == "Failed":
        sg.Popup(
            info['message'],
            title="Error!"
        )
    else:
        do_reblock(info)


def do_reblock(info):
    block_layout = [
        [
            sg.Text(
                "Reblock Account/IP",
                font=("Helvetica", 25),
                justification='c',
                size=(25, 1),
                text_color="red"
            )
        ],
        [
            sg.Text(
                "Change the existing block for an account or IP.",
                size=(60, 1),
                text_color="light gray",
                justification='c'
            )
        ],
        [
            sg.Text("Enter account or IP:", size=(15, 1), justification='r'),
            sg.InputText(key='target', default_text=info['message']['user'])
        ],
        [
            sg.Text("Enter reason:", size=(15, 1), justification='r'),
            sg.InputText(key='reason', default_text=info['message']['reason'])
        ],
        [
            sg.Text("Enter duration:", size=(15, 1), justification='r'),
            sg.InputText(key='duration', size=(15, 1), default_text=info['message']['expiry']),
            sg.Text("Enter project:", size=(10, 1), justification='r'),
            sg.InputText(key='project', default_text=info['project'], size=(15, 1))
        ],
        [
            sg.Text('Revoke TPA?', size=(15, 1), justification='r'),
            sg.Radio('Yes', 'R1', default=False, key='notpa'),
            sg.Radio('No', 'R1', default=True)
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop"),
            sg.Checkbox('Global Sysop action', default=False, key='gs'),
            sg.Checkbox('Steward action', default=False, key='steward')
        ],
        [
            sg.Text(
                "Valid duration examples: 3 days, 5months, indef, forever",
                size=(60, 1),
                justification='c',
                text_color="blue"
            )
        ]
    ]

    block_window = sg.Window("SAM: Apply block", block_layout)

    while True:
        block_event, block_values = block_window.Read()

        if block_event == "Exit" or block_event == sg.WIN_CLOSED:
            break
        elif block_event == "stop":
            block_window.close()
            break
        else:
            if (
                    block_values['target'] == "" or
                    block_values['reason'] == "" or
                    block_values['duration'] == "" or
                    block_values['project'] == ""
            ):
                sg.Popup("Target, reason, duration, and project are required!!", title="Input Error!")
            else:
                work = sam.reblock(SAM, block_values)

                if work['status'] == "Success":
                    sg.Popup(work['message'], title="Success!")
                else:
                    sg.Popup(work['message'], title="Failed!!")
                block_window.close()
                break

def get_revoketpa():
    intel = [
        [
            sg.Text("Account:", size=(12, 1), justification='r'),
            sg.InputText(key='target', size=(20, 1))
        ],
        [
            sg.Text("Project:", size=(12, 1), justification='r'),
            sg.InputText(key='project', size=(20, 1))
        ],
        [
            sg.Submit(),
            sg.Cancel(key='stop')
        ]
    ]

    intel_window = sg.Window("SAM: Reblock", intel)

    while True:
        intel_event, intel_values = intel_window.Read()

        if (
                intel_event == "Exit" or
                intel_event == sg.WIN_CLOSED or
                intel_event == 'stop'
        ):
            info = None
            break
        else:
            info = sam.blockinfo(sam.get_creds(SAM), intel_values)
            break

    intel_window.close()

    if info is None:
        return
    elif info['status'] == "notblocked":
        sg.Popup(
            "Target is not currently blocked. Can't revoke Talk Page access.",
            title="Not blocked!!"
        )
    elif info['status'] == "Failed":
        sg.Popup(
            info['message'],
            title="Error!"
        )
    else:
        do_revoketpa(info, intel_values)


def do_revoketpa(info, values):
    tpa_reason = info['message']['reason'] + " // revoke TPA"
    block_values = {
        'project': values['project'],
        'target': values['target'],
        'duration': info['message']['expiry'],
        'reason': tpa_reason,
        'notpa': True
    }

    work = sam.reblock(SAM, block_values)

    if work['status'] == "Success":
        sg.Popup(work['message'], title="Success!")
    else:
        sg.Popup(work['message'], title="Failed!!")


def get_lock():  # GUI for globally locking an account
    lock_layout = [
        [
            sg.Text(
                "Lock Account",
                font=("Helvetica", 25),
                justification='c',
                size=(25, 1),
                text_color="red"
            )
        ],
        [
            sg.Text(
                "Locks the account.",
                size=(60, 1),
                text_color="light gray",
                justification='c'
            )
        ],
        [
            sg.Text("Enter account:", size=(15, 1), justification='r'),
            sg.InputText(key='target')
        ],
        [
            sg.Text("Enter reason:", size=(15, 1), justification='r'),
            sg.InputText(key='reason')
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop")
        ]
    ]

    lock_window = sg.Window("SAM: Lock account", lock_layout)

    while True:
        lock_event, lock_values = lock_window.Read()

        if lock_event == "Exit" or lock_event == sg.WIN_CLOSED:
            break
        elif lock_event == "stop":
            lock_window.close()
            break
        else:
            result = sam.lock(SAM, lock_values)
            if result['status'] == "Success":
                sg.Popup(
                    result['message'],
                    title="Lock successful!"
                )
            else:
                sg.Popup(
                    "Error! " + result['message'] + " Please try again.",
                    title="Lock Failed!"
                )
            lock_window.close()
            break


def get_unlock():  # todo write get_unlock
    unlock_layout = [
        [
            sg.Text(
                "Unlock Account",
                font=("Helvetica", 25),
                justification='c',
                size=(25, 1),
                text_color="red"
            )
        ],
        [
            sg.Text(
                "Unlocks the account.",
                size=(60, 1),
                text_color="light gray",
                justification='c'
            )
        ],
        [
            sg.Text("Enter account:", size=(15, 1), justification='r'),
            sg.InputText(key='target')
        ],
        [
            sg.Text("Enter reason:", size=(15, 1), justification='r'),
            sg.InputText(key='reason')
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop")
        ]
    ]

    unlock_window = sg.Window("SAM: Unlock account", unlock_layout)

    while True:
        unlock_event, unlock_values = unlock_window.Read()

        if unlock_event == "Exit" or unlock_event == sg.WIN_CLOSED:
            break
        elif unlock_event == "stop":
            unlock_window.close()
            break
        else:
            result = sam.lock(SAM, unlock_values)
            if result['status'] == "Success":
                sg.Popup(
                    result['message'],
                    title="Unlock successful!"
                )
            else:
                sg.Popup(
                    "Error! " + result['message'] + " Please try again.",
                    title="Unlock Failed!"
                )
            unlock_window.close()
            break


def get_globalblock():  # Globally blocks provided IP address with reason/duration
    gblock_layout = [
        [
            sg.Text(
                "Globally Block IP",
                font=("Helvetica", 25),
                justification='c',
                size=(25, 1),
                text_color="red"
            )
        ],
        [
            sg.Text(
                "Globally blocks (including meta) the IP.",
                size=(60, 1),
                text_color="light gray",
                justification='c'
            )
        ],
        [
            sg.Text("Enter IP:", size=(15, 1), justification='r'),
            sg.InputText(key='target', size=(15, 1)),
            sg.Text("Enter duration:", size=(12, 1), justification='r'),
            sg.InputText(key='duration', size=(12, 1))
        ],
        [
            sg.Text("Enter reason:", size=(15, 1), justification='r'),
            sg.InputText(key='reason')
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop")
        ]
    ]

    gblock_window = sg.Window("SAM: Lock account", gblock_layout)

    while True:
        block_event, block_values = gblock_window.Read()

        if block_event == "Exit" or block_event == sg.WIN_CLOSED:
            break
        elif block_event == "stop":
            gblock_window.close()
            break
        else:
            result = sam.gblock(SAM, block_values)
            if result['status'] == "Success":
                sg.Popup(
                    result['message'],
                    title="Global block successful!"
                )
            else:
                sg.Popup(
                    "Error! " + result['message'] + " Please try again.",
                    title="Global block Failed!"
                )
            gblock_window.close()
            break


def get_massblock():  # todo write get_massblock
    layout = [
        [
            sg.Text("This will be the mass block interface")
        ],
        [
            sg.Exit()
        ]
    ]

    new_window = sg.Window("SAM: Apply mass blocks", layout)

    while True:
        event, values = new_window.Read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    new_window.close()


def get_masslock():  # todo write get_masslock
    layout = [
        [
            sg.Text("This will be the Mass lock interface")
        ],
        [
            sg.Exit()
        ]
    ]

    new_window = sg.Window("SAM: Apply mass locks", layout)

    while True:
        event, values = new_window.Read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    new_window.close()


def get_massgblock():  # todo write get_massgblock
    layout = [
        [
            sg.Text("This will be the mass global block interface")
        ],
        [
            sg.Exit()
        ]
    ]

    new_window = sg.Window("SAM: Apply mass global block", layout)

    while True:
        event, values = new_window.Read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    new_window.close()


def get_oauth():  # todo write get_oauth
    oauth_layout = [
        [
            sg.Text(
                "Add OAuth tokens",
                font=("Helvetica", 25),
                justification='c',
                size=(25, 1),
                text_color="red"
            )
        ],
        [
            sg.Text(
                "Follow the instructions at https://github.com/Operator873/SAM-for-desktop",
                size=(60, 1),
                text_color="light gray",
                justification='c'
            )
        ],
        [
            sg.Text(
                "and add your OAuth tokens below.",
                size=(60, 1),
                text_color="light gray",
                justification='c'
            )
        ],
        [
            sg.Text("Consumer Token", size=(15, 1), justification='r'),
            sg.InputText(key='c-token')
        ],
        [
            sg.Text("Consumer Secret", size=(15, 1), justification='r'),
            sg.InputText(key='c-secret')
        ],
        [
            sg.Text("Access Token", size=(15, 1), justification='r'),
            sg.InputText(key='a-token')
        ],
        [
            sg.Text("Access Secret", size=(15, 1), justification='r'),
            sg.InputText(key='a-secret')
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop")
        ]
    ]

    oauth_window = sg.Window("SAM: Lock account", oauth_layout)

    while True:
        event, values = oauth_window.Read()

        if event == "Exit" or event == sg.WIN_CLOSED or event == "stop":
            break
        else:
            if SAM['OAuth']['consumer_token'] != "":
                if sg.popup_yes_no(
                    "OAuth already configured! Reconfigure?"
                ) == "No":
                    break

            if (
                values['c-token'] != "" and
                values['c-secret'] != "" and
                values['a-token'] != "" and
                values['a-secret'] != ""
            ):
                SAM['OAuth']['consumer_token'] = values['c-token']
                SAM['OAuth']['consumer_secret'] = values['c-secret']
                SAM['OAuth']['access_token'] = values['a-token']
                SAM['OAuth']['access_secret'] = values['a-secret']

                with open('SAM.cfg', 'w') as configfile:
                    SAM.write(configfile)

                sg.Popup(
                    "OAuth tokens saved!",
                    title="Tokens saved"
                )

                break

    oauth_window.close()


def get_addapi():  # todo write get_addapi
    api_layout = [
        [
            sg.Text(
                "Add Project/API",
                font=("Helvetica", 25),
                justification='c',
                size=(25, 1),
                text_color="red"
            )
        ],
        [
            sg.Text(
                "Add a new project with the appropriate api url.",
                size=(60, 1),
                text_color="light gray",
                justification='c'
            )
        ],
        [
            sg.Text("Enter project:", size=(15, 1), justification='r'),
            sg.InputText(key='project', default_text="somewiki")
        ],
        [
            sg.Text("Enter API URL:", size=(15, 1), justification='r'),
            sg.InputText(key='api', default_text="https://some.wikipedia.org/w/api.php")
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop")
        ]
    ]

    api_window = sg.Window("SAM: Lock account", api_layout)

    while True:
        api_event, api_values = api_window.Read()

        if (
            api_event == "Exit" or
            api_event == sg.WIN_CLOSED or
            api_event == "stop"
        ):
            break
        elif (
            api_values['project'] == "somewiki" or
            api_values['api'] == "https://some.wikipedia.org/w/api.php"
        ):
            sg.Popup(
                "You should actually enter a valid project and API.",
                title="No values entered"
            )
            continue
        else:
            result = sam.addapi(SAM, api_values)
            if result['status'] == "Success":
                sg.Popup(
                    result['message'],
                    title="Project added successful!",
                    line_width=100
                )
            else:
                sg.Popup(
                    "Error! " + result['message'] + " Please try again.",
                    title="Project add failed!"
                )

            break

    api_window.close()

if __name__ == "__main__":
    main()
