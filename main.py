import PySimpleGUI as sg
# import SAM # todo write SAM with API interaction functions


def main():
    options = ['Block', 'Hard block', 'Spam bot', 'Lock', 'Global block', 'Mass block', 'Mass lock', 'Setup SAM']

    layout = [
        [
            sg.Text("Select action to take", size=(15, 1), justification='right'),
            sg.InputCombo(options, size=(15, 1), key="action"),
            sg.Submit(key="-MAIN-")
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

    window = sg.Window("Steward/Sysop Action Module", layout, size=(400, 70))

    while True:
        event, values = window.Read()
        # print(event + str(values)) # For debugging only
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "-MAIN-":
            if values['action'] == "Block":
                get_block()
            elif values['action'] == "Hard block":
                get_hardblock()
            elif values['action'] == "Spam bot":
                get_spambot()
            elif values['action'] == "Lock":
                get_lock()
            elif values['action'] == "Global block":
                get_globalblock()
            elif values['action'] == "Mass Block":
                get_massblock()
            elif values['action'] == "Mass lock":
                get_masslock()
            elif values['action'] == "":
                sg.Popup("You kinda have to chose something...", title="PEBKAC Error!")
            else:
                sg.Popup("An unknown selection was received. Try again.", title="Unknown error!")

            window['action'].update('')


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
            sg.InputText(key='duration')
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
                    block_values['duration'] == ""
            ):
                sg.Popup("All three fields are required!!")
            else:
                sg.Popup(
                    block_values['target'] +
                    " would be blocked for " + block_values['duration'] +
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
            sg.InputText(key='duration')
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
                    block_values['duration'] == ""
            ):
                sg.Popup("All three fields are required!!")
            else:
                sg.Popup(
                    block_values['target'] +
                    " would be blocked for " + block_values['duration'] +
                    " with reason: " + block_values['reason']
                )
                hblock_window.close()
                break


def get_spambot():  # todo Write get_spambot
    pass


def get_lock():  # todo write get_lock
    pass


def get_globalblock():  # todo write get_globalblock
    pass


def get_massblock():  # todo write get_massblock
    pass


def get_masslock():  # todo write get_masslock
    pass


main()
