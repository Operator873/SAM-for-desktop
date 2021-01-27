import PySimpleGUI as sg
import SAMtools as sam # todo finish SAMtools
import configparser

SAM = configparser.ConfigParser()

SAM.read('SAM.cfg')

def main():

    read_config()

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


def start_sam():
    
    if SAM.has_ :
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
                sg.Text("CentralAuth")
            ],
            [
                sg.Button("Lock", key='lock'),
                sg.Button("Unlock", key='unlock')
            ],
            [
                sg.Text("Mass actions")
            ],
            [
                sg.Button("Mass Block", key='massblock'),
                sg.Button("Mass Global Block", key='massgblock'),
                sg.Button("Mass Lock", key='masslock')
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
        elif event == "":
            sg.Popup("You kinda have to chose something...", title="PEBKAC Error!")
        else:
            sg.Popup("An unknown selection was received. Try again.", title="Unknown error!")


def get_block():

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
            sg.InputText(key='project', default_text=sam.homewiki(), size=(15, 1))
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop"),
            sg.Text(
                "Valid duration examples: 3 days, 5months, indef, forever",
                size=(42, 1),
                justification='r',
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
                # sam.block(block_values)
                sg.Popup(
                    block_values['target'] +
                    " would be blocked for " + block_values['duration'] +
                    " on " + block_values['project'] +
                    " with reason: " + block_values['reason']
                )
                block_window.close()
                break


def get_hardblock():

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
            sg.InputText(key='project', default_text=sam.homewiki(), size=(15, 1))
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop"),
            sg.Text(
                "Valid duration examples: 3 days, 5months, indef, forever",
                size=(42, 1),
                justification='r',
                text_color="blue"
            )
        ]
    ]

    hblock_window = sg.Window("SAM: Apply Hardblock", hblock_layout)

    while True:
        block_event, block_values = hblock_window.Read()

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
            else:
                # sam.hardblock(block_values)
                sg.Popup(
                    block_values['target'] +
                    " would be blocked for " + block_values['duration'] +
                    " with reason: " + block_values['reason']
                )
                hblock_window.close()
                break


def get_spambot():  # todo Write get_spambot

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
            sg.InputText(key='project', default_text=sam.homewiki(), size=(15, 1))
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop"),
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
                result = sam.spambot(block_values)
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
######################################################################

def get_lock():  # todo write get_lock
    layout = [
        [
            sg.Text("This will be the Lock interface")
        ],
        [
            sg.Exit()
        ]
    ]

    new_window = sg.Window("SAM: Apply Lock", layout)

    while True:
        event, values = new_window.Read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    new_window.close()


def get_globalblock():  # todo write get_globalblock
    layout = [
        [
            sg.Text("This will be the Global lock interface")
        ],
        [
            sg.Exit()
        ]
    ]

    new_window = sg.Window("SAM: Apply global block", layout)

    while True:
        event, values = new_window.Read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    new_window.close()


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


def get_unlock():  # todo write get_unlock
    layout = [
        [
            sg.Text("This will be the Unlock interface")
        ],
        [
            sg.Exit()
        ]
    ]

    new_window = sg.Window("SAM: Apply Unlock", layout)

    while True:
        event, values = new_window.Read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    new_window.close()


def get_oauth():  # todo write get_oauth
    layout = [
        [
            sg.Text("This will be the OAuth interface")
        ],
        [
            sg.Exit()
        ]
    ]

    new_window = sg.Window("SAM: Add OAuth", layout)

    while True:
        event, values = new_window.Read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    new_window.close()


def get_addapi():  # todo write get_addapi
    layout = [
        [
            sg.Text("This will be the add project/API interface")
        ],
        [
            sg.Exit()
        ]
    ]

    new_window = sg.Window("SAM: Add project", layout)

    while True:
        event, values = new_window.Read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    new_window.close()


if __name__ == "__main__":
    main()
