import ctypes
import os
import subprocess
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Please enter your password here
    database=""  # Please enter your database name here

)
mycursor = mydb.cursor()

print(mydb)


def run_cmd(cmd):

    cmd_struct = subprocess.run(cmd, stdout=subprocess.PIPE, encoding='866')
    if cmd_struct.returncode == 0:
        mb.showinfo(title=None, message="Successfully")
        print("----------successful---------")
        print()
    else:
        mb.showerror(title=None, message="Error while executing")
        print("----------ERROR----------")
        print(cmd_struct.stdout.replace("\n", ""))
        print()


def is_admin():

    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


if not is_admin():  # checks if the script is running as administrator
    mb.showerror('Error', 'Run as administrator')


def get_ips(domenname):

    cmd = ["nslookup", domenname]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, encoding='866')
    try:
        starts = result.stdout.rindex("Addresses:") + 10
        ends = len(result.stdout)
        ip = result.stdout[starts + 1:ends]
        ip = ip.replace("\n", "")
        ip = ip.replace(" ", "")
        ip = ip.split("\t")
        return ip
    except ValueError:
        starts = result.stdout.rindex("Address:") + 8
        ends = len(result.stdout)
        ip = result.stdout[starts + 1:ends]
        ip = ip.replace("\n", "")
        ip = ip.replace(" ", "")
        ip = [ip]
        return ip


def enable_firewall():

    cmd = ["netsh", "advfirewall", "set", "allprofiles", "state", "on"]
    mycursor.execute(
        "INSERT INTO records(activity,time) VALUES('enabling firewall', CURRENT_TIMESTAMP());")
    mydb.commit()
    run_cmd(cmd)


def disable_firewall():

    cmd = ["netsh", "advfirewall", "set", "allprofiles", "state", "off"]
    run_cmd(cmd)
    mycursor.execute(
        "INSERT INTO records(activity,time) VALUES('Disabling firewall', CURRENT_TIMESTAMP());")
    mydb.commit()


def reset_firewall():

    cmd = ["netsh", "advfirewall", "reset"]
    run_cmd(cmd)
    print("ads")
    mycursor.execute(
        "INSERT INTO records(activity,time) VALUES('firewall resetted', CURRENT_TIMESTAMP());")
    mydb.commit()


def firewall_block_all():
    cmd = ["netsh", "advfirewall", "set", "allprofiles",
           "firewallpolicy", "blockinbound,blockoutbound"]
    run_cmd(cmd)
    mycursor.execute(
        "INSERT INTO records VALUES ('Blocking all incoming connections', CURRENT_TIMESTAMP());")
    mydb.commit()
    pass


def block_http_port():
    cmd = ["netsh", "advfirewall", "firewall", "add", "rule", 'name="HTTP-block"', "protocol=TCP", "remoteport=80",
           "action=block", "dir=OUT"]
    mycursor.execute(
        "INSERT INTO records VALUES ('Blocking incoming http traffic', CURRENT_TIMESTAMP());")
    mydb.commit()
    run_cmd(cmd)


def unblock_http_port():
    cmd = ["netsh", "advfirewall", "firewall",
           "delete", "rule", 'name="HTTP-block"']
    mycursor.execute(
        "INSERT INTO records VALUES ('unblocking http traffic', CURRENT_TIMESTAMP());")
    mydb.commit()
    run_cmd(cmd)


def block_https_port():
    cmd = ["netsh", "advfirewall", "firewall", "add", "rule", 'name=HTTPS-block', "protocol=TCP", "remoteport=443",
           "action=block", "dir=OUT"]
    run_cmd(cmd)
    mycursor.execute(
        "INSERT INTO records VALUES ('Blocking incoming https traffic', CURRENT_TIMESTAMP());")
    mydb.commit()


def unblock_https_port():
    cmd = ["netsh", "advfirewall", "firewall",
           "delete", "rule", 'name=HTTPS-block']
    run_cmd(cmd)
    mycursor.execute(
        "INSERT INTO records VALUES ('UNBlocking incoming http traffic', CURRENT_TIMESTAMP());")
    mydb.commit()


def save_config():
    try:
        file_path = fd.asksaveasfilename(
            filetypes=[("Windows firewall", "*.wfw")])
        cmd = ["netsh", "advfirewall", "export", file_path]
        run_cmd(cmd)
    except:
        mb.showerror("Error", "An error occurred while saving")


def import_config():

    try:
        filepath = fd.askopenfilename(
            filetypes=[("All files", "*.*"), ("Windows firewall", "*.wfw")]
        )

        if not filepath:
            mb.showerror("ERROR", "ERROR IN CONF")
            return

        cmd = ["netsh", "advfirewall", "import", filepath]
        run_cmd(cmd)
    except:
        mb.showerror()("Error", "An error occurred while importing the configuration")


def about():

    about_window = tk.Tk()
    about_window.config(bg="white")
    about_window.iconbitmap('favicon.ico')

    w = about_window.winfo_screenwidth()
    h = about_window.winfo_screenheight()
    w = w // 2
    h = h // 2
    w = w - 200
    h = h - 300
    about_window.geometry('290x60+{}+{}'.format(w, h))

    about_window.resizable(False, False)
    about_window.title("About the program")

    label2 = tk.Label(text="The program configures the firewall",
                      master=about_window,
                      background="white",
                      foreground="black",
                      )
    label2.pack()
    about_window.mainloop()


def app_access():
    file_str = ""

    def block_app():
        nonlocal file_str

        cmd = ["netsh", "advfirewall", "firewall", "add", "rule",
               'name="App block"', "dir=out", 'program=""',
               "action=block"]
        cmd[5] = 'name="{}"'.format(file_str[file_str.rfind('\\') + 1:])
        cmd[7] = 'program="{}"'.format(file_str)
        os.system(' '.join(cmd))
        cmd[6] = "dir=in"
        os.system(' '.join(cmd))
        mycursor.execute(
            "INSERT INTO records VALUES ('Blocking"+file_str+"', CURRENT_TIMESTAMP());")
        mydb.commit()
        mb.showinfo(title=None, message="ОК")

    def unblock_app():
        cmd = ["netsh", "advfirewall", "firewall", "delete", "rule", 'name={}']
        cmd[5] = 'name="{}"'.format(file_str[file_str.rfind('\\') + 1:])
        mycursor.execute(
            "INSERT INTO records VALUES ('UnBlocking "+file_str+"', CURRENT_TIMESTAMP());")
        mydb.commit()
        run_cmd(cmd)

    def get_file_path():
        nonlocal file_str
        file_str = fd.askopenfilename(
            filetypes=[("Executable", "*.exe")]
        )

        file_str = file_str.replace("/", "\\")

    app_access_window = tk.Tk()
    app_access_window.config(bg="white")
    w = app_access_window.winfo_screenwidth()
    h = app_access_window.winfo_screenheight()
    w = w // 2
    h = h // 2
    w = w + 100
    h = h - 200
    app_access_window.geometry('273x78+{}+{}'.format(w, h))
    app_access_window.iconbitmap('favicon.ico')
    app_access_window.resizable(False, False)
    app_access_window.title("Access to Internet programs")

    file_path_btn = tk.Button(
        app_access_window,
        background="black",
        foreground="white",
        text="Select .exe",
        width=38,
        height=1,
        command=get_file_path
    ).grid(row=0, column=0)

    button_app_on = tk.Button(
        app_access_window,
        background="black",
        foreground="white",
        text="Block internet access",
        width=38,
        height=1,
        command=block_app
    ).grid(row=1, column=0)

    button_app_off = tk.Button(
        app_access_window,
        background="black",
        foreground="white",
        text="Unblock internet access",
        width=38,
        height=1,
        command=unblock_app
    ).grid(row=2, column=0)

    app_access_window.mainloop()


def help_page():

    # TODO
    pass
