from time import sleep

1. create a function that get the names of the Vms and stores them in a list
2. create a function that recevied a ip ipaddress range of the Vms
3. create a fuction/ convert a list to a dict of vm name and ipaddress
4. create a function that reach for a vms that are not answar to a ping
5.create a function that execute a api command to shutdown vm that is active/up and wait with some hold timer
to insure that the VM is down or until some log is sent
6. create a function that store the shutdown vms in a list

faulty_mechines = []
powered_of_machines = []

def get_connention():
    aws_client = '#maginc to initlized the client'

def get_all_ip():
    """obtain list of all machines"""

    ip_list = ["1.1.1.1", '2.2.2.2']
    return ip_list

def is_machine_on(ip):
    try:

      return True
    except:
        #blabla

def power_off_machine(powerd_on_list):
    """shut down the machine"""
    ip = ' '

    counter = 0
    while is_machine_on(ip) or counter <5:
        sleep(5)
        counter += 1

    if counter == 5: # it means we stopped the loop due to timeout
        faulty_machines.append(machine_ip)
    else:
        power_off_machine.append(machine_ip)

def print_summary():
    print(f"The list of powered off machines {powered_of_machines}")
    print(f"The list of faulty machines {faulty_mechines}")

if __name__ == "__main__":
ips = get_all_ip()

for ip in ips:
    if is_machine_on(ip):
    power_off_machine(ip)