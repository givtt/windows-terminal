"====== Library No Need Install ======"
import os
import time
import sys
import ctypes
import datetime
import subprocess
import platform
import zipfile
import shutil

"====== Library Need Install ======"
import requests
from prettytable import *

"===================================="


v = "v1"
os.system('cls')

welcome_message = """
                 ,  ,
              #▄▓██████▀
            "▀███████████▄L
           ▄R████████████▄▄
            ▄▀█████████▓▀▀N
             ' ▀█▀███▀█ ▀
                ' ▀█▌"
                   ▐█
                   ██
                   ██
    ""▀▀▀██▄▄   ▄▄▄██▄a▄▄   ,▄▄██▀▀""
           "▀██▄⌠▀▀▀▀▀'¡▄██▀"
               ▀██▄  ▄██▀`
                  ████"
               ▄▄█▌▀╙██▄▄
          ██▄▄██▀█    █▀███▀█▌

            [ Made By GIVT ]
     
     
     [ + ] Telegram  : givtt
     [ + ] Instagram : we62
     
     [ ! ] You are not entitled to sell the Tool [ ! ]
"""
print(welcome_message)
time.sleep(3)

os.system("cls")


class Colors():
    def change_color_return(self, text, color):
        if color == "red":
            c = "\033[31m"
        elif color == "green":
            c = "\033[32m"
        elif color == "yellow":
            c = "\033[33m"
        elif color == "blue":
            c = "\033[34m"
        else:
            c = ""
        return c + text + "\033[0m"

    def change_color(self, text, color):
        if color == "red":
            c = "\033[31m"
        elif color == "green":
            c = "\033[32m"
        elif color == "yellow":
            c = "\033[33m"
        elif color == "blue":
            c = "\033[34m"
        else:
            c = ""

        print(c + text + "\033[0m")

class AppAata():
    def appdata_folder(self):
        try:
            if self.is_exists():
                return self.appdata_path() + "/givt-terminal"
            else:
                self.create()
                self.appdata_folder()
        except Exception as e:
            self.write(f"Trying get appdata folder [ GIVT ]\nError : {e}")

    def appdata_path(self):
        return os.getenv('APPDATA')

    def is_exists(self):
        path = self.appdata_path()
        folder_path = os.path.join(path, "givt-terminal")
        if os.path.exists(folder_path):
            return True
        else:
            return False

    def create(self):
        if self.is_exists() is not True:
            path = self.appdata_path()
            file_name = "/givt-terminal"
            try:
                os.mkdir(path + file_name)
                with open(path + file_name + "/log.txt", 'w') as f:
                    f.write(f'Created File in > {datetime.datetime.now()}\n')
                return True
            except Exception as e:
                print(e)
                return False

    def write(self, log):
        if self.is_exists():
            path = self.appdata_path() + "/givt-terminal/log.txt"
            with open(path, 'a') as F:
                F.write(log + "\n")
            F.close()
            return True
        else:
            self.create()
            self.write(log=log)

    def write_errors(self, error, line, why, by):
        error_message = f"""
        \n\n========================
        Error ! -> To Logs/
        Line       : {line}
        error      : {error}
        why?       : {why}
        error from : {by}
        Time       : {datetime.datetime.now()}
        ========================\n\n
        """
        if self.is_exists():
            path = self.appdata_path() + "/givt-terminal/log.txt"
            with open(path, 'a') as F:
                F.write(error_message + "\n")
            F.close()
            return True
        else:
            self.create()
            self.write_errors(error, line, why, by)

    def check_if_installed(self, name):
        if self.is_exists():
            path = self.appdata_folder() + "/" + name
            if os.path.exists(path):
                return True
            else:
                return False
        else:
            self.create()
            self.check_if_installed(name)

class Terminal():
    def __init__(self):
        self.username = os.getlogin()
        self.tool_path = os.getcwd()
        self.thired_part = AppAata().appdata_folder()
        self.output_beautiful = Colors()
        self.need_restart = False
        AppAata().create()
        while True:
            self.work()

    def restart_script(self):
        try:
            os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            AppAata().write_errors(e, "142", "", "user")
            self.output_beautiful.change_color("[-] Unable to restart, restart the tool manually", 'error')

    def show_restart_device(self, message, title):
        MB_YESNO = 0x4
        MB_ICONWARNING = 0x30

        popup = ctypes.windll.user32.MessageBoxW(0, message, title, MB_ICONWARNING | MB_YESNO)
        if popup == 6:
            os.system("shutdown /r /t 1")

    def is_admin(self) -> bool:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1

    def is_python_installed(self) -> bool:
        try:
            subprocess.run(['python', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False

    def remove_dir(self, path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
        return True

    def download_file(self, link, path, chunk_size=1024):
        try:
            r = requests.get(link, stream=True)
            total_size = int(r.headers.get('content-length', 0))
            block_size = chunk_size
            wrote = 0
            with open(path, 'wb') as f:
                for data in r.iter_content(chunk_size=block_size):
                    wrote += len(data)
                    f.write(data)
                    progress = min(50, int(50 * wrote / total_size))
                    sys.stdout.write('\r[{}{}] {}%'.format('#' * progress, '-' * (50 - progress), int(100 * wrote / total_size)))
                    sys.stdout.flush()
            f.close()
            print("\n")
            return True
        except KeyboardInterrupt:
            self.output_beautiful.change_color('\n[-] Canceling download ..', 'red')
            os.remove(link)
            return False

        except ConnectionError:
            self.output_beautiful.change_color('\n[-] Please Check Your Internet ..', 'red')
            self.output_beautiful.change_color('\n[-] Canceling download ..', 'red')
            os.remove(link)
        return False

    def work(self):
        if self.is_admin():
            ms = f'''┌──(\033[31mroot\033[0m@{self.username})-[{self.tool_path}]\n└─$ '''
            ctypes.windll.kernel32.SetConsoleTitleW(f"Windows terminal ( Full Root )")
        else:
            ctypes.windll.kernel32.SetConsoleTitleW("Windows terminal ( Not root )")
            ms = f'''┌──(user@{self.username})-[{self.tool_path}]\n└─$ '''
        print('\n')
        terminal_input = input(ms)
        if terminal_input == "sudo":
            if self.is_admin():
                self.output_beautiful.change_color('[+] You already Admin', 'yellow')
            else:
                try:
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                    exit() or quit()
                except PermissionError:
                    self.output_beautiful.change_color("[X] Error Permission Error", 'error')

        elif terminal_input == "help":
            self.output_beautiful.change_color("[+] Welcome To Windows Terminal V1", 'green')
            self.output_beautiful.change_color("[/] The best commands have been modified and added to the terminal :", 'green')
            print("""
install python : That Command Install python [[ 3.10.10 ]] And setup it with add path to env auto
burpsuit       : Run burpsuit without setup or install it on your windows system
wireshark      : Run wireshark without setup or install it on your windows system
aircrack-ng    : Run aircrack-ng without setup or install it on your windows
john           : Run john without setup or install it on your windows
nmap           : Run nmap without setup or install it on your windows
sqlmap         : Run sqlmap without setup or install it on your windows
clear_temp     : Remove all the files that the tool works on such as burpsuit files and everything you download it
""")
            self.output_beautiful.change_color("This All Commands For terminal :", 'yellow')
            print("""
clear   : For Clear windows terminal
exit    : For Close the windows terminal
ls      : For lists all files in the current directory
cd      : Change the current working directory in various operating systems
cd ..   : Back to the main command prompt
restart : Restart The script
sudo    : Run Script with admin
pwd     : Writes to standard output the full path name of your current directory
mkdir   : It creates each directory specifed on the command line in the order given. you can use -p
rm      : Auto Remove Files And directory
nano    : text viewer from any file
ps      : writes the status of active processes
kill    : kill some processes
arp     : displays the Internet-to-adapter address translation tables used by the Address in Networks and communication management
whoami  : displays a username associated with check if root or not
                    """)

        elif terminal_input == "burpsuit":
            try:
                subprocess.Popen([f"{self.thired_part}/burpsuit/BurpSuiteCommunity.exe"])
            except FileNotFoundError:
                self.output_beautiful.change_color('[-] You Run The Tool First Time\n[/] Please give me 30sec','yellow')
                self.output_beautiful.change_color("[!] Will Download burpsuit files .. ( 237MB )", "yellow")
                if input("[!] Press (Y) to continue: ").lower() == "y":
                    self.download_file("https://github.com/givtt/windows-terminal/raw/main/src/librarys/burpsuit.zip", path=self.thired_part + "/burpsuit.zip")
                    zip_file = zipfile.ZipFile(f"{self.thired_part}/burpsuit.zip", 'r')
                    zip_file.extractall(self.thired_part)
                    zip_file.close()
                    self.output_beautiful.change_color('[+] Done \nUse to run > burpsuit', 'green')
                else:
                    self.output_beautiful.change_color("[-] Cansel Download burpsuit ..", "red")
                    time.sleep(2)
                    os.system("cls")

        elif terminal_input == "wireshark":
            try:
                subprocess.Popen([f"{self.thired_part}/wireshark/Wireshark.exe"])
            except FileNotFoundError:
                self.output_beautiful.change_color('[-] You Run The Tool First Time\n[/] Please give me 30sec','yellow')
                self.output_beautiful.change_color("[!] Will Download wireshark files .. ( 61.4MB )", "yellow")
                if input("[!] Press (Y) to continue: ").lower() == "y":
                    self.download_file("https://github.com/givtt/windows-terminal/raw/main/src/librarys/wireshark.zip", path=self.thired_part + "/wireshark.zip")
                    zip_file = zipfile.ZipFile(f"{self.thired_part}/wireshark.zip", 'r')
                    zip_file.extractall(self.thired_part)
                    zip_file.close()
                    self.output_beautiful.change_color('[+] Done \nUse to run > wireshark', 'green')
                else:
                    self.output_beautiful.change_color("[-] Cansel Download wireshark ..", "red")
                    time.sleep(2)
                    os.system("cls")

        elif terminal_input[:11] == "aircrack-ng":
            try:
                command = terminal_input.split("aircrack-ng ")[1]
                self.output_beautiful.change_color("[+] Runing aircrack-ng ..", 'green')
                time.sleep(2)
                subprocess.run([self.thired_part + "/aircrack-ng/bin/aircrack-ng.exe", command])
            except IndexError:
                self.output_beautiful.change_color("[-] Please Add Some args like -> aircrack-ng --help", 'error')
            except FileNotFoundError:
                self.output_beautiful.change_color('[-] You Run The Tool First Time\n[/] Please give me 30sec','yellow')
                self.output_beautiful.change_color("[!] Will Download aircrack-ng files .. ( 12MB )", "yellow")
                if input("[!] Press (Y) to continue: ").lower() == "y":
                    self.download_file("https://github.com/givtt/windows-terminal/raw/main/src/librarys/aircrack-ng.zip", path=self.thired_part + "/aircrack-ng.zip")
                    zip_file = zipfile.ZipFile(f"{self.thired_part}/aircrack-ng.zip", 'r')
                    zip_file.extractall(self.thired_part)
                    zip_file.close()
                    self.output_beautiful.change_color('[+] Done \nUse to run > aircrack-ng --help', 'green')
                else:
                    self.output_beautiful.change_color("[-] Cansel Download aircrack-ng ..", "red")
                    time.sleep(2)
                    os.system("cls")

        elif terminal_input[:4] == "john":
            try:
                command = terminal_input.split("john ")[1]
                self.output_beautiful.change_color("[+] Runing john ..", 'green')
                time.sleep(2)
                subprocess.run([self.thired_part + "/john/run/john.exe", command])
            except IndexError:
                self.output_beautiful.change_color("[-] Please Add Some args like -> john -h", 'error')
            except FileNotFoundError:
                self.output_beautiful.change_color('[-] You Run The Tool First Time\n[/] Please give me 30sec', 'yellow')
                self.output_beautiful.change_color("[!] Will Download aircrack-ng files .. ( 63.3MB )", "yellow")
                if input("[!] Press (Y) to continue: ").lower() == "y":
                    self.download_file("https://github.com/givtt/windows-terminal/raw/main/src/librarys/john.zip", path=self.thired_part + "/john.zip")
                    zip_file = zipfile.ZipFile(f"{self.thired_part}/john.zip", 'r')
                    zip_file.extractall(self.thired_part)
                    zip_file.close()
                    self.output_beautiful.change_color('[+] Done \nUse to run > john -h', 'green')
                else:
                    self.output_beautiful.change_color("[-] Cansel Download john ..", "red")
                    time.sleep(2)
                    os.system("cls")

        elif terminal_input[:4] == "nmap":
            try:
                run = terminal_input.split('nmap ')[1]
                self.output_beautiful.change_color("[+] Runing Nmap Tool ..", 'green')
                time.sleep(2)
                subprocess.run(f'{self.thired_part}/Nmap/nmap.exe {run}')
            except IndexError:
                self.output_beautiful.change_color("[-] Please Add Some args like -> nmap -h", 'error')
            except FileNotFoundError:
                self.output_beautiful.change_color('[-] You Run The Tool First Time\n[/] Please give me 30sec', 'yellow')
                self.output_beautiful.change_color("[!] Will Download namp files .. ( 20MB )", "yellow")
                if input("[!] Press (Y) to continue: ").lower() == "y":
                    self.download_file("https://github.com/givtt/windows-terminal/raw/main/src/librarys/nmap.zip", path=self.thired_part + "/nmap.zip")
                    zip_file = zipfile.ZipFile(f"{self.thired_part}/nmap.zip", 'r')
                    zip_file.extractall(self.thired_part)
                    zip_file.close()
                    self.output_beautiful.change_color('[+] Done \nUse to run > nmap -h', 'green')
                else:
                    self.output_beautiful.change_color("[-] Cansel Download nmap ..", "red")
                    time.sleep(2)
                    os.system("cls")

        elif terminal_input[:6] == "sqlmap":
            try:
                run = terminal_input.split('sqlmap ')[1]
                self.output_beautiful.change_color("[+] Runing sqlmap Tool ..", "green")
                time.sleep(2)
                python_runner = self.thired_part + "/sqlmap/py-givt/python.exe"
                subprocess.run(f'{python_runner} {self.thired_part}/sqlmap/sqlmap.py {run}')
            except IndexError:
                self.output_beautiful.change_color("[-] Please Add Some args like -> sqlmap -h", "error")
            except FileNotFoundError:
                self.output_beautiful.change_color('[-] You Run The Tool First Time\n[/] Please give me 30sec', 'yellow')
                self.output_beautiful.change_color("[!] Will Download sqlmap files .. ( 50MB )", "yellow")
                if input("[!] Press (Y) to continue: ").lower() == "y":
                    self.download_file("https://github.com/givtt/windows-terminal/raw/main/src/librarys/sqlmap.zip", path=self.thired_part + "/sqlmap.zip")
                    zip_file = zipfile.ZipFile(f"{self.thired_part}/sqlmap.zip", 'r')
                    zip_file.extractall(self.thired_part)
                    zip_file.close()
                    self.output_beautiful.change_color('[+] Done \nUse to run > sqlmap -h', 'green')
                else:
                    self.output_beautiful.change_color("[-] Cansel Download sqlmap ..", "red")
                    time.sleep(2)
                    os.system("cls")

        elif terminal_input.lower() == "install python":
            if self.is_python_installed():
                self.output_beautiful.change_color("[-] Python Already installed", 'red')
            elif self.need_restart:
                self.show_restart_device("لقد تم تثبيت بايثون على جهازك بنجاح !\n يلزم اعادة تشغيل الجهاز \n هل تريد اعادة التشغيل الان ؟", "رائع !")
            else:
                self.output_beautiful.change_color("[+] Download Python.. [ 3.10.10 ]", 'yellow')
                if self.is_admin():
                    if platform.architecture()[0] == "64bit":
                        url = f"https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe"
                        app = "python-installer64.exe"
                    else:
                        url = f"https://www.python.org/ftp/python/3.10.10/python-3.10.10.exe"
                        app = "python-installer32.exe"
                    try:
                        if self.download_file(url, AppAata().appdata_folder() + "/" + app):
                            self.output_beautiful.change_color("[+] Done Download Python.. [ 3.10.10 ]", 'green')
                            self.output_beautiful.change_color("[+] Install The Python in system ..\n[/] Please wait..", 'yellow')
                            process = subprocess.Popen(f"{AppAata().appdata_folder() + '/' + app} /quiet InstallAllUsers=1 PrependPath=1 AppendPath=1",stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                            out, err = process.communicate()
                            return_code = process.returncode
                            while True:
                                if return_code == 0:
                                    self.output_beautiful.change_color("[+] Done Download And Setup The Python.. [ 3.10.10 ]", 'green')
                                    self.output_beautiful.change_color("[+] Done Setup pip..", 'green')
                                    self.output_beautiful.change_color("[+] Done Add python to env", 'green')
                                    self.need_restart = True
                                    os.remove(AppAata().appdata_folder() + '/' + app)
                                    break
                                elif err:
                                    self.output_beautiful.change_color(f"[-] Error Setup python\n Error -> {err}", 'red')
                                    AppAata().write_errors("python Cant setup", '390', 'Maybe The user may close the window without making sure that the installation is complete', 'user')
                                    break
                                else:
                                    for x in range(10 + 1):
                                        self.output_beautiful.change_color(f"[+] Working .. {x}", 'yellow')
                            self.show_restart_device("لقد تم تثبيت بايثون على جهازك بنجاح !\n يلزم اعادة تشغيل الجهاز \n هل تريد اعادة التشغيل الان ؟", "رائع !")
                        else:
                            pass
                    except Exception as e:
                        AppAata().write_errors(e, '387', 'Unknown', 'tool')
                        self.output_beautiful.change_color("[-] Error in Start Downloading python", 'red')
                        self.output_beautiful.change_color('[-] Please Reinstall the tool', 'error')
                else:
                    self.output_beautiful.change_color("[-] Error in Start Downloading python", 'red')
                    self.output_beautiful.change_color("[-] Please Run script use Permission admin", 'red')
                    self.output_beautiful.change_color("[-] To Get Permission admin use command [ sudo ]", 'red')

        elif terminal_input[:6].lower() == "whoami":
            if self.is_admin():
                print(f"[ {self.username} ] {self.output_beautiful.change_color_return('Root', 'red')}")
            else:
                print(f"[ {self.username} ] Not Root")

        elif terminal_input.lower() == "arp":
            devices = []
            arp_output = subprocess.check_output('arp -a', shell=True, text=True)
            for line in arp_output.splitlines():
                parts = line.split()
                if len(parts) == 3 and parts[0] != 'Interface:':
                    devices.append({'ip': parts[0], 'mac': parts[1]})
            for ip in devices:
                print(ip['ip'])

        elif terminal_input[:2].lower() == "ps":
            output = subprocess.check_output(['powershell', 'Get-Process'])
            print(output.decode('utf-8'))

        elif terminal_input[:4].lower() == "kill":
            try:
                command = terminal_input.lower()
                ID = command.split('kill ')[1]
                subprocess.call(['taskkill', '/F', '/PID', ID], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                self.output_beautiful.change_color(f"[+] The process with PID {ID} has been terminated.", 'green')
            except IndexError:
                self.output_beautiful.change_color('kill: For use [ kill ]  Command -> kill <ProcessId> ', 'red')
            except subprocess.CalledProcessError:
                self.output_beautiful.change_color(f'kill: ID not Found !', 'red')
            except PermissionError:
                self.output_beautiful.change_color('kill: Permission denied', 'red')
            except Exception as e:
                self.output_beautiful.change_color(f'kill: ID not Found !', 'red')
                AppAata().write_errors(e, '444', 'Unknown', 'tool')

        elif terminal_input[:4].lower() == "nano":
            try:
                file_name = terminal_input.split('nano ')[1]
                if os.path.isfile(file_name):
                    with open(file_name, 'r') as f:
                        contents = f.read()
                        f.close()
                    print(contents)
                else:
                    self.output_beautiful.change_color(f'nano: no such file or directory: haha', 'red')
            except IndexError:
                self.output_beautiful.change_color('For use [ nano ]  Command -> nano <FileName>', 'red')
            except FileNotFoundError:
                self.output_beautiful.change_color(f'nano: File ( {file_name} ) Not Found !', 'red')
            except PermissionError:
                self.output_beautiful.change_color('nano: Permission denied', 'red')
            except Exception as e:
                AppAata().write_errors(e, '460', 'Unknown', 'tool')

        elif terminal_input[:2].lower() == "rm":
            try:
                file_name = terminal_input.split('rm ')[1]
                if os.path.isdir(file_name):
                    self.remove_dir(file_name)
                else:
                    os.remove(file_name)
            except IndexError:
                self.output_beautiful.change_color('rm: For use [ rmdir ]  Command -> rmdir <FolderName>', 'red')
            except Exception as e:
                AppAata().write_errors(e, '479', 'Unknown', 'tool')

        elif terminal_input[:5].lower() == "mkdir":
            try:
                if '-p' in terminal_input:
                    file_name = terminal_input.split('mkdir -p ')[1]
                    os.makedirs(file_name)
                else:
                    file_name = terminal_input.split('mkdir ')[1]
                    os.mkdir(file_name)
            except IndexError:
                self.output_beautiful.change_color('mkdir: For use [ mkdir ]  Command -> mkdir <FolderName> or mkdir -p test/test2 ', 'red')
            except FileExistsError:
                self.output_beautiful.change_color(f'mkdir: Directory ( {file_name} ) already exist !', 'red')
            except PermissionError:
                self.output_beautiful.change_color(f"You don't have permissions to create dir", 'red')
            except Exception as e:
                AppAata().write_errors(e, '488', 'Unknown', 'tool')

        elif terminal_input.lower() == "pwd":
            print(os.getcwd())

        elif terminal_input.lower() == 'restart':
            self.restart_script()

        elif terminal_input[:2].lower() == "cd":
            try:
                path = terminal_input.split('cd ')[1]
                os.chdir(path)
                self.tool_path = os.getcwd()
            except IndexError:
                self.output_beautiful.change_color('cd: For use [ cd ]  Command -> cd YOUR_PATH', 'red')
            except FileNotFoundError:
                self.output_beautiful.change_color(f'cd: no such file or directory', 'red')
            except OSError:
                self.output_beautiful.change_color('cd: For use [ cd ]  Command -> cd YOUR_PATH OR FOLDER', 'red')

        elif terminal_input == "ls":
            try:
                x = PrettyTable()
                x.field_names = ['name', 'size', 'create at', 'modified at']
                x.set_style(style=MSWORD_FRIENDLY)
                x.border = True
                x.vertical_char = " "
                x.bottom_junction_char = " "
                for file in os.listdir(self.tool_path):
                    file_path = os.path.join(file)
                    if os.access(file_path, os.R_OK | os.W_OK | os.X_OK):
                        file_name = self.output_beautiful.change_color_return(file, 'blue')
                    else:
                        file_name = file
                    size = os.path.getsize(file_path)
                    created_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
                    modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
                    x.add_row([file_name, size, created_time, modified_time])
                print(x.get_string())
            except Exception as e:
                AppAata().write_errors(e, '552', 'Maybe with Line [ 533 to 522 ]', 'tool')

        elif terminal_input.lower()[:9] == "chmod 777":
            try:
                filename = terminal_input.split("chmod 777 ")[1]
                current_permissions = os.stat(filename).st_mode
                os.chmod(filename, current_permissions | 0o777)
            except FileNotFoundError:
                self.output_beautiful.change_color(f"chmod: No such file or directory", 'red')
            except IndexError:
                self.output_beautiful.change_color("chmod: For Use this command -> chmod 777 <filename>", 'red')
            except PermissionError:
                self.output_beautiful.change_color("chmod: Please Run this code with admin", 'red')
            except Exception as e:
                AppAata().write_errors(e, '546', 'Maybe with Line [ 546 ]', 'tool')

        elif terminal_input.lower() == "exit":
            exit() or quit()

        elif terminal_input.lower() == "clear_temp":
            if self.is_admin():
                response = ctypes.windll.user32.MessageBoxW(0, "هل انت متأكد من حذف جميع الملفات بالأداة ؟", "Confirmation", 4)
                if response == 6:
                    folder_path = self.thired_part + "/"
                    count = 0
                    for root, dirs, files in os.walk(folder_path, topdown=False):
                        for file_name in files:
                            file_path = os.path.join(root, file_name)
                            os.remove(file_path)
                            count +=1
                        for dir_name in dirs:
                            dir_path = os.path.join(root, dir_name)
                            shutil.rmtree(dir_path)
                            count +=1


                    shutil.rmtree(folder_path)
                    self.output_beautiful.change_color(f"[+] Done Remove {count} From your disk", "green")
                else:
                    self.output_beautiful.change_color("[/] Cancel Remove all temp files (:", "green")
            else:
                self.output_beautiful.change_color("[-] Please Run with admin rights > use : sudo", "red")



        elif terminal_input.lower() == 'clear':
            os.system('cls')
        else:
            if len(terminal_input.replace(" ", "")) == 0:
                pass
            else:
                self.output_beautiful.change_color('bash: command not found', 'red')



Terminal()