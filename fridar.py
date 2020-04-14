from __future__ import print_function 
import argparse
from colors import *
from cmd import Cmd

import frida
import os,sys
import random
import subprocess

# check python version
if sys.version_info < (3,5):
    print(bad + ' Sorry, fridar requires Python 3.5 or higher.')
    exit()
 
print('''%s
         ____     _     __          
        / __/____(_)___/ /___ ______
       / /_/ ___/ / __  / __ `/ ___/
      / __/ /  / / /_/ / /_/ / /    
     /_/ /_/  /_/\__,_/\__,_/_/ (v0.2.0)%s
   
         a simple frida wrapper
''' % (yellow,end))

hints = ['Usual workflow: package > script {classes > methods > hijack}'
        # 'Use command line option -f to set package beforehand.',
        # 'Use `fridar> refresh` to refresh device and processes.'
        ]
print('%s(Hint) %s' % (yellow,end) + random.choice(hints) + '\n')

class Preferences:
    def __init__(self):
        self.package_name = ''
        self.script_name = ''
        self.current_script = ''
        self.device_init()

    def device_init(self):
        print(run + ' Attempting USB connection')
        try:
            self.device = frida.get_usb_device()
            print(good + ' Connected to USB device')
        except:
            print(bad + ' No USB devices found')
            exit()

prefs = Preferences()
 
# parsing command line arguments
parser = argparse.ArgumentParser(description='...')
parser.add_argument('-f', '--file',
        help='package name of app (adb shell ps|grep {{keyword}})')
parser.add_argument('-l', '--load',
        help='frida script to load (./scripts - don\'t add extension)')
args = parser.parse_args()

if args.file: prefs.package_name = args.file
if args.load: prefs.script_name = args.load

class AutoComplete:
    def __init__(self):
        self.packages = self.list_packages()
        self.scripts = [f.split('.')[0] for f in os.listdir('scripts')]

    def list_packages(self):

        print(run + ' Loading processes')
        p1 = subprocess.check_output(['frida-ps', '-Ua'])

        plist = str(p1).split('\\n')
        result = []
        
        for item in plist[2:-1]:
            result.append(item.split()[-1])
        
        print(good + ' Process list loaded')
        return(result)

auto_complete = AutoComplete()

class FridarPrompt(Cmd):

    prompt = '%sfridar>%s ' % (red,end)
       
    def do_package(self, inp):
        if inp in auto_complete.packages:
            print(good + ' Package set to ' + inp)
            prefs.package_name = inp
        else: print(bad + ' Package should be currently running')

    def complete_package(self, text, line, begidx, endidx):
        if text:
            return [cmd for cmd in auto_complete.packages
                    if cmd.startswith(text)]
        else: return auto_complete.packages

    def help_package(self):
        print('Usage: package com.example.app')

    def do_refresh(self,inp):
        prefs.device_init() # re-connect with usb device
        auto_complete.packages = auto_complete.list_packages()

    def help_refresh(self,inp):
        print('Refreshes loaded process list')

    def do_script(self, inp):
        if inp in auto_complete.scripts:
            print(good + ' Script set to ' + inp)
            prefs.script_name = inp
        else: print(bad + ' Choose an existing script')

    def complete_script(self, text, line, begidx, endidx):
        if text: return [cmd for cmd in auto_complete.scripts
                if cmd.startswith(text)]
        else: return auto_complete.scripts

    def help_script(self):
        print('Usage: script frida_script_name')

    def do_view(self, inp):
        print('package: ' + prefs.package_name + ' ' +
              '\nscript: ' + prefs.script_name)
    def help_view(self):
        print('Displays preferences')

    def do_run(self, inp):
        if not prefs.script_name or not prefs.package_name:
            print(bad + ' Please choose package and script')
            return

        frida_code = ''
        print(run + ' Running supplied script')
        path = os.path.dirname(os.path.realpath(__file__)) \
                    + '/scripts/' + prefs.script_name + '.js'
        with open(path) as f: frida_code = f.read()
    
        pid = prefs.device.get_process(prefs.package_name).pid
        process = prefs.device.attach(pid)
        prefs.current_script = process.create_script(frida_code)
        
        prefs.current_script.on('message', on_message)
        prefs.current_script.load()
    
        sys.stdin.read()
        # device.resume(pid)
        # time.sleep(1)

    def help_run(self):
        print('Runs supplied frida script')

    do_r = do_run
    def help_r(): pass

    def do_exit(self, inp):
        return True

    def help_exit(self):
        print('Press Ctrl-D to exit')
   
    # using ctrl-d to exit
    do_EOF = do_exit
    def help_EOF(self): pass
    
    def default(self, line):
        # cmd, arg, line = self.parseline(line)
        # func = [getattr(self, n) for n in self.get_names() if n.startswith('do_' + cmd)]
        # if len(func) == 1: func[0](arg)
        # else:
        print('Type ? to see list of available commands')

# defining message callback
def on_message(message, data):
    try:
        if message['type'] != 'error':
            print(message['payload'], end='')
            send_message()
        else:
            print(bad + ' ' + message['description'])
    except Exception:
        exit()

# sending back to the frida script
def send_message():
    method = input()
    prefs.current_script.post({'type': 'input', 'payload': method})

def main():
    
    try: FridarPrompt().cmdloop()
    except KeyboardInterrupt:
        print()
        main()
    
if __name__ == '__main__':
    main()

