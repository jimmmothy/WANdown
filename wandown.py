#!/usr/bin/python3

'''
## WANDOWN

Uses paramiko to log into my home IOS router and do basic stuff that I can automate if needed

https://docs.paramiko.org/en/stable/api/client.html
https://docs.paramiko.org/en/stable/api/channel.html#paramiko.channel.Channel.send
'''

import paramiko
import sys
import time

class wandown:
    def __init__(self, ip: str, un: str, pw: str):
        self.cpe_ip = ip
        self.cpe_un = un
        self.cpe_pw = pw
        self.time = 1

        self.stdin = ""
        self.stdout = ""
        self.stderr = ""
        self.recent_failure = False
        self.recent_output = []

        #self.connected = False
        self.ssh = paramiko.SSHClient()
        self.max_attempts = 1

        self.default_route = ""
        self.default_error = "??? Does not compute ???"
        self.expected_arguments = {"shut_noshut":1,"reset":1,"default_route":0,"direct":1}


    ''' Usage '''
    def usage(self):
        print("wandown.py {command}\nor\nwandown.py {command} {argument}")


    ''' check if command is valid and return expected arugment count '''    
    def valid_command(self, command) -> int:

        if command in self.expected_arguments:
            return self.expected_arguments[command]
        return -1

    
    ''' Connect to router '''
    def connect(self) -> bool:

        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self.ssh.connect(self.cpe_ip, username=self.cpe_un, password=self.cpe_pw, look_for_keys=False)
            self.connected = True
            return True

        except Exception as error:
            print(f"{self.default_error}\n{error}")
            return False


    ''' Disconnect from router '''
    def disconnect(self):

        self.ssh.close()
        self.connected = False
    

    ''' Do a command, keep track of things '''
    def execute_command(self, command) -> bool:

        if self.recent_failure == True:
            return False

        try:
            self.stdin, self.stdout, self.stderr = self.ssh.exec_command(command)
            self.recent_output = self.stdout.readlines()
            return True

        except Exception as error:
            print(f"{self.default_error}\n{error}")
            return False


    ''' Control commands being executed '''
    def action_command(self, command: str, argument: str) -> bool:

        print(f"{command},{argument}")
        if command == "direct":
            self.execute_command(argument)
            self.print_output()

        elif command == "shut_noshut" or command == "reset":
            self.shut_noshut(argument)

        elif command == "default_route":
            self.find_default_route()


    ''' Self explantory here '''
    def print_output(self):
        for x in self.recent_output:
            print(x)


    ''' Find default route '''
    def find_default_route(self) -> bool:

        if self.execute_command("show ip route") == False:
            self.recent_failure = True
        
        else:
            for line in self.recent_output:
                if "0.0.0.0/0" in line:
                    print(f"Default route located:\n{line}")
                    self.default_route = line
                    return True
            return False


    ''' shut and unshut an interface 
        used for shut_noshut or reset command '''
    def shut_noshut(self, interface: str) -> bool:

        try:
            connection = self.ssh.invoke_shell()
            connection.send("conf t\n")
            time.sleep(self.time)
            connection.send("int " + interface + "\n")
            time.sleep(self.time)
            connection.send("shut\n")
            time.sleep(self.time * 3)
            connection.send("no shut\n")
            time.sleep(self.time * 3)
            connection.send("exit\n")
            time.sleep(self.time)
            connection.send("exit\n")
            #print(connection.recv(65535))
            return True

        except Exception as error:
            print(f"{self.default_error}\n{error}")
            return False


def main():

    cpe_ip = "192.168.0.1"
    cpe_un = "root"
    cpe_pw = "hunter2"
    mikobot = wandown(cpe_ip, cpe_un, cpe_pw)

    if len(sys.argv) >= 1:

        command = sys.argv[1]
        vc = mikobot.valid_command(command)

        if vc == -1:
            mikobot.usage()
        
        else:
            if vc == 0:
                argument = ""
            else:
                argument = sys.argv[2]

            print(f"Running wandown.py {command} {argument}")

            mikobot.connect()
            mikobot.action_command(command, argument)
            mikobot.disconnect()

            print("Completed\n")

    else:
        mikobot.usage()

if __name__ == "__main__":
    main()