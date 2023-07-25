#!/usr/bin/env python3
import subprocess, time, platform, sys, re
import pyinputplus as pyip

default_hosts = ['8.8.8.8']

# 
if len(sys.argv) > 1:
    default_hosts = [ip for ip in sys.argv[1:]]
time_re = re.compile(r'time=(\d{1,3}).*ms')
display_dict = {ip: [] for ip in default_hosts}
os = platform.system()

def process_regex(text_to_process, default_output):

    if time_re.search(text_to_process):
        text = time_re.search(text_to_process).group(1)
    else:
        text = default_output

    return text

while True:

    # st = time.time() # for debugging time differences during run-time

    # set up terminal display
    if platform.system()=="Windows":
        subprocess.Popen("cls", shell=True).communicate() #I like to use this instead of subprocess.call since for multi-word commands you can just type it out, granted this is just cls and subprocess.call should work fine 
    else: #Linux and Mac
        print("\033c", end="")
    print('\nIf IP responds to ping, result will be displayed in ms response time')
    print(f'    IP ADDRESS   |')
    print('____________________________________________________________________________________________________')
    
    #Format + display first column
    for ip in default_hosts:

        len_ip = len(ip)
        print(ip," "*(15-len_ip),'|',*display_dict[ip],'')

    #for every ip you want to ping, try to ping it once, collect output, and store it in the display_dict for printing
    for ip in default_hosts:
        
        if os == "Windows":
            terminal = subprocess.Popen(f'ping {ip} -n 1 -w 1000', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
        else:
            terminal = subprocess.Popen(f'ping {ip} -c 1 -w 1000', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)

        terminal_output = terminal.stdout.read()
        terminal_time = process_regex(terminal_output, '   ')
        terminal_time = str(terminal_time)
        terminal_time = terminal_time+" "*(3-len(terminal_time)) + " | "
        display_dict[ip].append(terminal_time)
    time.sleep(1)
    
    if len(list(display_dict.values())[0]) == 13: #can be adjusted if you want more results printed per row, default is 13
        display_dict = {ip: [] for ip in default_hosts}
    else:
        continue
    time.sleep(1)

