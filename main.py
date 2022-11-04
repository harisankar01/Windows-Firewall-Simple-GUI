from handlers import *
from sniffer import capture


def block_site():

    domen = domen_string.get()
    ips = get_ips(domen)

    cmd = ["netsh", "advfirewall", "firewall", "add", "rule", 'name="{site_name}"', "protocol=TCP", "remoteport=80",
           "action=block", "dir=OUT", "remoteip={site_ip}"]

    if len(ips) > 1:
        for ip_address in ips:
            cmd[5] = "name=block " + domen
            cmd[10] = "remoteip=" + ip_address
            run_cmd(cmd)
            cmd[7] = "remoteport=443"
            run_cmd(cmd)
            cmd[7] = "remoteport=80"

        mb.showinfo(title=None, message="Successfully")
    elif len(ips) == 1:
        cmd[5] = "name=block " + domen
        cmd[10] = "remoteip=" + ips[0]
        run_cmd(cmd)
        cmd[7] = "remoteport=443"
        run_cmd(cmd)
        mb.showinfo(title=None, message="Successfully")
    else:
        mb.showerror("Error", "Error while blocking " + domen)


def unblock_site():

    name = 'name=block ' + domen_string.get()
    cmd = ["netsh", "advfirewall", "firewall", "delete", "rule", name]
    run_cmd(cmd)


def get_pack():
    print("GETIING packets")
    text = capture()
    text_area.insert(tk.END, str(text), "Asd")


window = tk.Tk()

window.title("Firewall")
window.minsize(600, 600)

# set maximum window size value
window.maxsize(1280, 800)
window.config(bg="#d6fff6")
# master.configure(background='SteelBlue1')
window.iconbitmap('favicon.ico')

w = window.winfo_screenwidth()
h = window.winfo_screenheight()

# w = w // 2
# h = h // 2
# w = w - 200
# h = h - 200
#
#
# window.geometry('290x403+{}+{}'.format(w, h))

# window.resizable(False, False)

mainmenu = tk.Menu(window)
window.config(menu=mainmenu)


configmenu = tk.Menu(mainmenu, tearoff=0)
configmenu.add_command(label="Save configuration", command=save_config)
configmenu.add_command(label="Import Configuration", command=import_config)
configmenu.add_separator()
configmenu.add_command(label="Exit", command=exit)


helpmenu = tk.Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="About the program", command=about)

main_frame = tk.Frame(window)
main_frame.grid(row=0, column=0, sticky="nswe")
main_frame.columnconfigure(0, weight=3)
main_frame.columnconfigure(1, weight=4)
left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky="nswe")
right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=1, sticky="nswe")
Firewall_label = tk.Label(left_frame,
                          text="Firewall",
                          background="white",
                          foreground="black",
                          font=("Times", "15", "bold")
                          ).grid(row=0, column=0, columnspan=3)

button_firewall_on = tk.Button(
    left_frame,
    background="black",
    foreground="white",
    text="On",
    width=29,
    height=2,
    command=enable_firewall
).grid(row=1, column=0, sticky="nswe")

button_firewall_off = tk.Button(
    left_frame,
    background="black",
    foreground="white",
    text="Off",
    width=29,
    height=2,
    command=disable_firewall
).grid(row=1, column=1, sticky="nswe")

button_firewall_reset = tk.Button(
    left_frame,
    background="black",
    foreground="white",
    text="Reset",
    width=29,
    height=2,
    command=reset_firewall
).grid(row=2, column=0, sticky="nswe")

button_firewall_block = tk.Button(
    left_frame,
    background="black",
    foreground="white",
    text="Block all",
    width=29,
    height=2,
    command=firewall_block_all
).grid(row=2, column=1, sticky="nswe")


block_http_label = tk.Label(
    left_frame, text="HTTP traffic",
    background="#e8b97b",
    foreground="black",
    font=("Times", "12", "bold")
).grid(row=3, column=0, columnspan=2, sticky="nswe")

button_http_on = tk.Button(
    left_frame,
    background="black",
    foreground="white",
    text="block",
    width=50,
    height=2,
    command=block_http_port
).grid(row=4, column=0, columnspan=2, sticky="nswe")

button_http_off = tk.Button(
    left_frame,
    background="black",
    foreground="white",
    text="Unlock",
    width=50,
    height=2,
    command=unblock_http_port
).grid(row=5, column=0, columnspan=2, sticky="nswe")


block_https_label = tk.Label(left_frame, text="HTTPS traffic",
                             background="white",
                             highlightcolor="black",
                             highlightthickness=1,
                             bg="#e8b97b",
                             foreground="black",
                             font=("Times", "12", "bold")
                             ).grid(row=6, column=0, columnspan=2, sticky="nswe")

button_https_on = tk.Button(
    left_frame,
    background="black",
    foreground="white",
    text="block",
    width=50,
    height=2,
    command=block_https_port
).grid(row=7, column=0, columnspan=2, sticky="nswe")

button_https_off = tk.Button(
    left_frame,
    background="black",
    foreground="white",
    text="Unlock",
    width=50,
    height=2,
    command=unblock_https_port
).grid(row=8, column=0, columnspan=2, sticky="nswe")


block_app_lbl = tk.Label(left_frame, text="Application",
                         background="white",
                         foreground="black",
                         bg="#e8b97b",
                         font=("Times", "12", "bold")
                         ).grid(row=9, column=0, columnspan=2, sticky="nswe")

app_app_btn = tk.Button(
    left_frame,
    background="black",
    foreground="white",
    text="Select application",
    width=50,
    height=2,
    command=app_access
).grid(row=10, column=0, columnspan=2, sticky="nswe")

block_domen_lbl = tk.Label(left_frame, text="Domain",
                           background="white",
                           foreground="black",
                           bg="#e8b97b",
                           font=("Times", "12", "bold")
                           ).grid(row=11, column=0, columnspan=2, sticky="nswe")

domen_string = tk.StringVar(window)


domen_txt = tk.Entry(left_frame,
                     width=80,
                     bg="pink",
                     fg="black",
                     justify="center",
                     textvariable=domen_string
                     ).grid(row=12, column=0, columnspan=2, sticky="nswe")

domen_block_btn = tk.Button(
    left_frame,
    background="black",
    foreground="white",
    text="block",
    width=50,
    height=2,
    command=block_site
).grid(row=13, column=0, columnspan=2, sticky="nswe")

domen_unblock_btn = tk.Button(
    left_frame,
    background="black",
    foreground="white",
    text="Unlock",
    width=50,
    height=2,
    command=unblock_site
).grid(row=14, column=0, columnspan=2, sticky="nswe")

printButton = tk.Button(left_frame,
                        background="black",
                        foreground="white",
                        text="GET_PACKETS",
                        justify="center",
                        command=get_pack).grid(row=16, column=0, columnspan=2, sticky="nswe")

text_area = tk.Text(
    right_frame,
    height=70,
    width=100,
    background="#e8b97b",
    foreground="black",
    font=("Times", "12", "bold")
)
text_area.grid(row=0, column=2, sticky="ns")


window.mainloop()
