#!/usr/bin/env python3
import subprocess, time, platform, sys, re
import pyinputplus as pyip

# You can over-ride this list to change the default hosts mhping reaches out to.
default_hosts = ['8.8.8.8']
# Change this if you want to customize output if host doesnt respond (Keep to 3 characters)
no_response_str = '  '
# Can be adjusted if you want more results printed per row, default is 13
results_per_row = 13 

# Create list of hosts to ping, define regex to capture ms ping times, create dict used to display
# the aggregated results. 
if len(sys.argv) > 1:
    default_hosts = [ip for ip in sys.argv[1:]]
time_re = re.compile(r'time=(\d{1,3}).*ms')
ping_results = {ip: [] for ip in default_hosts}

# Detect platform, and set the terminal clearing function
os = platform.system()
if os == "Windows":
    def clear_window():
        subprocess.Popen("cls", shell=True).communicate()
else: #Linux and Mac
    def clear_window():
        print("\033c", end="")

def process_regex(text_to_process, default_output):
    if time_re.search(text_to_process):
        text = time_re.search(text_to_process).group(1)
    else:
        text = default_output
    return text

# Main loop
while True:
    # st = time.time() # for debugging time differences during run-time

    clear_window()
    print('If host responds to ping, result will be displayed in ms response time')
    print('Ctrl+C to stop at any time')
    print('    Hosts        |')
    print('____________________________________________________________________________________________________')
    
    # Calculate hosts column width, display it, then display ping results for that host.
    for ip in default_hosts:
        len_ip = len(ip)
        print(ip," "*(15-len_ip),'|',*ping_results[ip],'')

    # For every host you want to ping, try to ping it once, collect output, and store it 
    # in the ping_results dict for later printing to screen
    for ip in default_hosts:
        if os == "Windows":
            terminal = subprocess.Popen(f'ping {ip} -n 1 -w 1000', shell=True, 
            stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
        else:
            terminal = subprocess.Popen(f'ping {ip} -c 1 -w 1', shell=True,
            stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)

        terminal_output = terminal.stdout.read()
        response_time = str(process_regex(terminal_output, no_response_str))
        response_time = response_time+" "*(3-len(response_time)) + " | " # Centers text in column
        ping_results[ip].append(response_time)
    # time.sleep(1)

    # When display reaches threshold, clear results dict.
    if len(list(ping_results.values())[0]) == results_per_row: 
        ping_results = {ip: [] for ip in default_hosts}
    else:
        continue
    time.sleep(1)

