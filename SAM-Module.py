import PySimpleGUI as sg
import SAMtools as sam
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
    
    layout = sam.build_sam(SAM)

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
            sam_window.close()
            get_oauth()
        elif event == "addapi":
            get_addapi()
        elif event == "reblock":
            get_reblock()
        elif event == "tpa":
            get_revoketpa()
        elif event == "modgblock":
            get_modgblock()
        elif event == "setup":
            sam_window.close()
            get_setup()
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
            sg.InputText(key='project', default_text=SAM['Settings']['homewiki'], size=(15, 1))
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop"),
            sg.Checkbox('Global Sysop action', default=False, key='gs', disabled=sam.check_gs(SAM)),
            sg.Checkbox('Steward action', default=False, key='steward', disabled=sam.check_stew(SAM))
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
            sg.InputText(key='project', default_text=SAM['Settings']['homewiki'], size=(15, 1))
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop"),
            sg.Checkbox('Global Sysop action', default=False, key='gs', disabled=sam.check_gs(SAM)),
            sg.Checkbox('Steward action', default=False, key='steward', disabled=sam.check_stew(SAM))
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
            sg.InputText(key='project', default_text=SAM['Settings']['homewiki'], size=(15, 1))
        ],
        [
            sg.Submit(),
            sg.Button("Cancel", key="stop"),
            sg.Checkbox('Global Sysop action', default=False, key='gs', disabled=sam.check_gs(SAM)),
            sg.Checkbox('Steward action', default=False, key='steward', disabled=sam.check_stew(SAM))
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
            sg.Checkbox('Global Sysop action', default=False, key='gs', disabled=sam.check_gs(SAM)),
            sg.Checkbox('Steward action', default=False, key='steward', disabled=sam.check_stew(SAM))
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
            sg.Text("Account:", size=(11, 1), justification='r'),
            sg.InputText(key='target', size=(25, 1))
        ],
        [
            sg.Text("Project:", size=(11, 1), justification='r'),
            sg.InputText(key='project', size=(25, 1))
        ],
        [
            sg.Checkbox('Global Sysop action', default=False, key='gs', disabled=sam.check_gs(SAM)),
            sg.Checkbox('Steward action', default=False, key='steward', disabled=sam.check_stew(SAM))
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
        'notpa': True,
        'gs': values['gs'],
        'steward': values['steward']
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


def get_unlock():  # Unlocks an account
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


def get_massblock():  # This gathers the information for and processes a mass block on a single project
    data = []

    left = [
        [
            sg.Text(
                "Account/IP to block",
                size=(15, 1)
            )
        ],
        [
            sg.InputText(
                key='target',
                size=(30, 1)
            )
        ],
        [
            sg.Button("Block All", key='_done_'),
            sg.Cancel(key='stop')

        ],
        [
            sg.Checkbox('Global Sysop action', default=False, key='gs', disabled=sam.check_gs(SAM)),
            sg.Checkbox('Steward action', default=False, key='steward', disabled=sam.check_stew(SAM))
        ]
    ]

    center = [
        [
            sg.Button(">", key="_add_", bind_return_key=True)
        ],
        [
            sg.Button("<", key="_rmv_")
        ]
    ]

    right = [
        [
            sg.Listbox(
                data,
                size=(30, 10),
                key='thelist',
                enable_events=True
            )
        ],
        [
            sg.InputText(
                key='project',
                default_text=SAM['Settings']['homewiki'],
                size=(15, 1)
            ),
            sg.InputText(
                key='duration',
                default_text="Duration",
                size=(15, 1)
            )
        ],
        [
            sg.InputText(
                key='reason',
                default_text="Reason",
                size=(32, 1)
            )
        ]
    ]

    layout = [[
        sg.Column(left),
        sg.VerticalSeparator(),
        sg.Column(center),
        sg.VerticalSeparator(),
        sg.Column(right)
    ]]

    mass_window = sg.Window('Mass block', layout)

    while True:
        event, values = mass_window.read()

        if (
                event == "Exit" or
                event == sg.WIN_CLOSED or
                event == "stop"
        ):
            break

        elif event == "_add_":
            if values['target'] in data:
                sg.Popup(
                    "That is already in the list."
                )
                mass_window.FindElement('target').Update("")
            elif values['target'].strip() == "":
                mass_window.FindElement('target').Update("")
            else:
                data.append(values['target'])
                mass_window.FindElement('target').Update("")
                mass_window.FindElement('thelist').Update(data)

        elif event == "thelist":
            rmv_target = values['thelist'][0]

        elif event == "_rmv_":

            try:
                data.remove(rmv_target)
            except UnboundLocalError:
                continue
            except ValueError:
                continue
            finally:
                mass_window.FindElement('thelist').Update(data)

        elif event == "_done_":

            if values['project'] == "" or values['project'] == "examplewiki":
                sg.Popup(
                    "Please enter a valid project for the mass block...",
                    title="Project not valid!"
                )
                continue
            elif (
                values['reason'] == "" or
                values['reason'] == "Reason" or
                values['duration'] == "" or
                values['duration'] == "Duration"
            ):
                sg.Popup(
                    "Please check your reason and duration...",
                    title="Error!"
                )
                continue
            elif len(data) == 0:
                sg.Popup(
                    "No accounts to block! Nothing to do...",
                    title="Error!"
                )
                continue

            targets = ", "

            if sg.popup_yes_no(
                    "Accounts to block: " + targets.join(data)
            ) == "Yes":

                for item in data:
                    values['target'] = item

                    resp = sam.block(SAM, values)

                    if resp['status'] == "Error":
                        sg.Popup(
                            resp['status'] + " " + resp['message'],
                            title="Error!"
                        )

                data = []
                mass_window.FindElement('thelist').Update(data)
                mass_window.FindElement('target').Update("")

                sg.Popup(
                    "Mass block complete.",
                    title="Complete!"
                )

            else:
                if sg.popup_yes_no(
                        "Keep current list?"
                ) == "No":
                    data = []
                    mass_window.FindElement('thelist').Update(data)
                    mass_window.FindElement('target').Update("")

    mass_window.close()


def get_masslock():  # Process a mass lock
    data = []

    left = [
        [
            sg.Text(
                "Account to lock",
                size=(15, 1)
            )
        ],
        [
            sg.InputText(
                key='target',
                size=(30, 1)
            )
        ],
        [
            sg.Button("Lock All", key='_done_'),
            sg.Cancel(key='stop')

        ]
    ]

    center = [
        [
            sg.Button(">", key="_add_", bind_return_key=True)
        ],
        [
            sg.Button("<", key="_rmv_")
        ]
    ]

    right = [
        [
            sg.Listbox(
                data,
                size=(30, 10),
                key='thelist',
                enable_events=True
            )
        ],
        [
            sg.InputText(
                key='reason',
                default_text="Reason",
                size=(32, 1)
            )
        ]
    ]

    layout = [[
        sg.Column(left),
        sg.VerticalSeparator(),
        sg.Column(center),
        sg.VerticalSeparator(),
        sg.Column(right)
    ]]

    lock_window = sg.Window('Mass lock', layout)

    while True:
        event, values = lock_window.read()

        if (
                event == "Exit" or
                event == sg.WIN_CLOSED or
                event == "stop"
        ):
            break

        elif event == "_add_":
            if values['target'] in data:
                sg.Popup(
                    "That is already in the list."
                )
                lock_window.FindElement('target').Update("")
            elif values['target'].strip() == "":
                lock_window.FindElement('target').Update("")
            else:
                data.append(values['target'])
                lock_window.FindElement('target').Update("")
                lock_window.FindElement('thelist').Update(data)

        elif event == "thelist":
            rmv_target = values['thelist'][0]

        elif event == "_rmv_":

            try:
                data.remove(rmv_target)
            except UnboundLocalError:
                continue
            except ValueError:
                continue
            finally:
                lock_window.FindElement('thelist').Update(data)

        elif event == "_done_":

            if (
                    values['reason'] == "" or
                    values['reason'] == "Reason"
            ):
                sg.Popup(
                    "Please check your reason...",
                    title="Error!"
                )
                continue
            elif len(data) == 0:
                sg.Popup(
                    "No accounts to lock! Nothing to do...",
                    title="Error!"
                )
                continue

            targets = ", "

            if sg.popup_yes_no(
                    "Accounts to lock: " + targets.join(data)
            ) == "Yes":

                for item in data:
                    values['target'] = item

                    resp = sam.lock(SAM, values)

                    if resp['status'] == "Error":
                        sg.Popup(
                            resp['status'] + " " + resp['message'],
                            title="Error!"
                        )

                data = []
                lock_window.FindElement('thelist').Update(data)
                lock_window.FindElement('target').Update("")

                sg.Popup(
                    "Mass lock complete.",
                    title="Complete!"
                )

            else:
                if sg.popup_yes_no(
                        "Keep current list?"
                ) == "No":
                    data = []
                    lock_window.FindElement('thelist').Update(data)
                    lock_window.FindElement('target').Update("")

    lock_window.close()


def get_massgblock():  # Process and executes a mass global block

    data = []

    left = [
        [
            sg.Text(
                "IP to globally block",
                size=(20, 1)
            )
        ],
        [
            sg.InputText(
                key='target',
                size=(30, 1)
            )
        ],
        [
            sg.Button("Block All", key='_done_'),
            sg.Cancel(key='stop')

        ]
    ]

    center = [
        [
            sg.Button(">", key="_add_", bind_return_key=True)
        ],
        [
            sg.Button("<", key="_rmv_")
        ]
    ]

    right = [
        [
            sg.Listbox(
                data,
                size=(30, 10),
                key='thelist',
                enable_events=True
            )
        ],
        [
            sg.Text("Duration:"),
            sg.InputText(
                key='duration',
                size=(23, 1)
            )
        ],
        [
            sg.InputText(
                key='reason',
                default_text="Reason",
                size=(32, 1)
            )
        ]
    ]

    layout = [[
        sg.Column(left),
        sg.VerticalSeparator(),
        sg.Column(center),
        sg.VerticalSeparator(),
        sg.Column(right)
    ]]

    mass_window = sg.Window('Mass Global block', layout)

    while True:
        event, values = mass_window.read()

        if (
                event == "Exit" or
                event == sg.WIN_CLOSED or
                event == "stop"
        ):
            break

        elif event == "_add_":
            if values['target'] in data:
                sg.Popup(
                    "That is already in the list."
                )
                mass_window.FindElement('target').Update("")
            elif values['target'].strip() == "":
                mass_window.FindElement('target').Update("")
            else:
                data.append(values['target'])
                mass_window.FindElement('target').Update("")
                mass_window.FindElement('thelist').Update(data)

        elif event == "thelist":
            rmv_target = values['thelist'][0]

        elif event == "_rmv_":

            try:
                data.remove(rmv_target)
            except UnboundLocalError:
                continue
            except ValueError:
                continue
            finally:
                mass_window.FindElement('thelist').Update(data)

        elif event == "_done_":

            if (
                    values['reason'] == "" or
                    values['reason'] == "Reason" or
                    values['duration'] == "" or
                    values['duration'] == "Duration"
            ):
                sg.Popup(
                    "Please check your reason and duration...",
                    title="Error!"
                )
                continue
            elif len(data) == 0:
                sg.Popup(
                    "No accounts to block! Nothing to do...",
                    title="Error!"
                )
                continue

            targets = ", "

            if sg.popup_yes_no(
                    "Accounts to block: " + targets.join(data)
            ) == "Yes":

                for item in data:
                    values['target'] = item

                    resp = sam.testrun(SAM, values)

                    if resp['status'] == "Error":
                        sg.Popup(
                            resp['status'] + " " + resp['message'],
                            title="Error!"
                        )

                data = []
                mass_window.FindElement('thelist').Update(data)
                mass_window.FindElement('target').Update("")

                sg.Popup(
                    "Mass global block complete.",
                    title="Complete!"
                )

            else:
                if sg.popup_yes_no(
                        "Keep current list?"
                ) == "No":
                    data = []
                    mass_window.FindElement('thelist').Update(data)
                    mass_window.FindElement('target').Update("")

    mass_window.close()


def get_oauth():  # Adds new OAuth information to SAM.cfg
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

    start_sam()


def get_addapi():  # Adds an new project to the WIKIs file
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


def get_setup():

    s = sam.fetch_setup(SAM)

    is_gs = s['is_globalsysop']
    is_s = s['is_steward']

    layout = [
        [
            sg.Text("Account Name:"),
            sg.InputText(key='account', default_text=s['account_name'])
        ],
        [
            sg.Text("Home wiki:"),
            sg.InputText(key='wiki', default_text=s['homewiki'])
        ],
        [
            sg.Text("I am a Global sysop:"),
            sg.Radio("Yes", "gs", default=is_gs, key='gs'),
            sg.Radio("No", "gs", default=not is_gs)
        ],
        [
            sg.Text("I am a Steward:"),
            sg.Radio("Yes", "stew", default=is_s, key='stew'),
            sg.Radio("No", "stew", default=not is_s)
        ],
        [
            sg.Button("Save", key='save'),
            sg.Cancel()
        ]
    ]

    setup_window = sg.Window("Setup options", layout)

    while True:
        event, values = setup_window.Read()

        if (
            event == "Exit" or
            event == sg.WIN_CLOSED or
            event == "Cancel"
        ):
            break

        elif event == 'save':
            if sg.popup_yes_no(
                "Are you sure you want to save?",
                title="Confirm?"
            ) == "Yes":
                if values['gs'] is True:
                    SAM['Settings']['is_globalsysop'] = "Yes"
                else:
                    SAM['Settings']['is_globalsysop'] = "No"

                if values['stew'] is True:
                    SAM['Settings']['is_steward'] = "Yes"
                else:
                    SAM['Settings']['is_steward'] = "No"

                SAM['Settings']['homewiki'] = values['wiki']
                SAM['Settings']['account_name'] = values['account']

                with open('SAM.cfg', 'w') as f:
                    SAM.write(f)

                sg.Popup(
                    "Settings saved",
                    title="Saved!"
                )

                break

    setup_window.close()

    start_sam()

def get_modgblock():
    pass

if __name__ == "__main__":
    main()
