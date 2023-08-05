#!/usr/bin/env python

import paramiko
import time


"""
A generic and agnostic module to establish SSH connection to any devices that supports SSH.
"""


conf_terminal_setup = f"configure terminal"

def ssh_connector(hostname, username, password, key=False, timeout=10, port=22):
    """ Connect to remote device and return a channel to use for sending cmds.
        return the returned value is the channel object that will be used to send command to remote device
    """
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username,
                    password=password, look_for_keys=key, timeout=timeout)
        print("Connected to {0}\n".format(hostname))
    except:
        print("Could not connect to {0}".format(hostname))
        ssh.close()
        return None
    else:
        channel = ssh.invoke_shell()
        return channel


def send_cmd(cmd, channel, incoming_sleep_time=2, out_going_sleep_time=2):
    """Send a cmd in 'global configuration mode' via the channel if channel object is not None
        return: the return value is the result or the executed cmd
    """

    if not cmd:
        print(f"Not command to send\n")
        return None
    if not channel:
        print(f"No channel available\n")
        return None

    banner = channel.recv(99999).decode("utf-8")
    time.sleep(incoming_sleep_time)
    print(f"{banner}\n\n")

    channel.send(cmd + "\n")
    time.sleep(out_going_sleep_time)

    output = channel.recv(99999).decode("utf-8")
    time.sleep(incoming_sleep_time)
    return output


def send_config_cmd(cmd, channel, incoming_sleep_time=2, out_going_sleep_time=2):
    """Send a cmd in 'configuration mode' via the channel if channel object is not None
        return: the return value is the result or the executed cmd
    """

    if not cmd:
        print(f"Not command to send\n")
        return None
    if not channel:
        print(f"No channel available\n")
        return None

    banner = channel.recv(99999).decode("utf-8")
    time.sleep(incoming_sleep_time)
    print(f"{banner}\n\n")

    # Set the config terminal
    channel.send(conf_terminal_setup + "\n")
    time.sleep(out_going_sleep_time)
    tmp_output = channel.recv(99999).decode("utf-8")
    time.sleep(incoming_sleep_time)
    print(tmp_output)

    channel.send(cmd + "\n")
    time.sleep(out_going_sleep_time)

    output = channel.recv(99999).decode("utf-8")
    time.sleep(incoming_sleep_time)
    return output


def send_cmds(list_of_commands, channel, incoming_sleep_time=2, out_going_sleep_time=2):
    """Send multiple cmds in 'global configuration mode' via the channel if channel object is not None
        return: the return value is the result or the executed cmds
    """
    list_of_commands = list(list_of_commands)

    if not list_of_commands:
        print(f"Not commands to send\n")
        return None
    if not channel:
        print(f"No channel available\n")
        return None

    banner = channel.recv(99999).decode("utf-8")
    time.sleep(incoming_sleep_time)
    print(f"{banner}\n\n")

    all_outputs = ""
    for cmd in list_of_commands:
        channel.send(cmd + "\n")
        time.sleep(out_going_sleep_time)

        output = channel.recv(99999).decode("utf-8")
        time.sleep(incoming_sleep_time)
        all_outputs += f"{output}\n"

    #channel.close()
    return all_outputs


def send_config_cmds(list_of_commands, channel, incoming_sleep_time=2, out_going_sleep_time=2):
    """Send multiple cmds in 'configuration mode' via the channel if channel object is not None
        return: the return value is the result or the executed cmds
    """
    list_of_commands = list(list_of_commands)

    if not list_of_commands:
        print(f"Not commands to send\n")
        return None
    if not channel:
        print(f"No channel available\n")
        return None

    banner = channel.recv(99999).decode("utf-8")
    time.sleep(incoming_sleep_time)
    print(f"{banner}\n\n")

    # Set the config terminal
    channel.send(conf_terminal_setup + "\n")
    time.sleep(out_going_sleep_time)
    tmp_output = channel.recv(99999).decode("utf-8")
    time.sleep(incoming_sleep_time)
    print(tmp_output)

    all_outputs = ""
    for cmd in list_of_commands:
        channel.send(cmd + "\n")
        time.sleep(out_going_sleep_time)

        output = channel.recv(99999).decode("utf-8")
        time.sleep(incoming_sleep_time)
        all_outputs += f"{output}\n"

    #channel.close()
    return all_outputs


# This function is not yet tested, I am working on it.

# def send_commands_return_dictionary(list_of_commands, list_of_hosts, username,
#                                     password, incoming_sleep_time=1, out_going_sleep_time=1):
#     """connect to each device and execute all commands per device and record the results per device in a dict"""
#     output_dict = {}
#     if not list_of_commands:
#         print(f"Not commands to send\n")
#         return None
#     if not list_of_hosts:
#         print(f"Not hosts in the list of hosts\n")
#         return None
#
#     for host in list_of_hosts:
#         new_channel = ssh_connector(hostname=host, username=username, password=password)
#
#         all_outputs = ""
#         for cmd in list_of_commands:
#             new_channel.send(cmd + "\n")
#             time.sleep(out_going_sleep_time)
#
#             output = new_channel.recv(99999).decode("utf-8")
#             time.sleep(incoming_sleep_time)
#             all_outputs += f"{output}\n"
#
#         output_dict[host] = all_outputs
#         all_outputs = ""
#         new_channel.close()
#
#     return output_dict





















