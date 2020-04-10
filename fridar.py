import frida
import os,sys
import random
import argparse


print('''
       __      _     _            
      / _|_ __(_) __| | __ _ _ __ 
     | |_| '__| |/ _` |/ _` | '__|
     |  _| |  | | (_| | (_| | |   
     |_| |_|  |_|\__,_|\__,_|_| v0.1.0

        *a simple frida wrapper*
    http://github.com/abhaynayar/fridar

''')


# parsing command line arguments
parser = argparse.ArgumentParser(description='...')
parser.add_argument('-p', '--package', help='package name of app', required=True)
parser.add_argument('-s', '--script', help='frida script to load', required=True)
args = parser.parse_args()

package_name = args.package
frida_script = args.script

# reading script file
frida_code = None
with open(os.path.dirname(os.path.realpath(__file__)) + '/scripts/' + frida_script + '.js') as f:
    frida_code = f.read()

# connect to usb device
device = frida.get_usb_device()

# defining message callback
def on_message(message, data):
    try:
        print(message['payload'], end='')
    except Exception:
        print('[!] ' + message['description'])
        exit()
    send_message()

def send_message():
    method = input() #com.tinder.settings.activity.SettingsActivity
    script.post({'type': 'input', 'payload': method})

try:
    if device:

        pid = device.get_process(package_name).pid
        process = device.attach(pid)
        script = process.create_script(frida_code)
        
        script.on('message', on_message)
        script.load()
        sys.stdin.read()

        device.resume(pid)
        time.sleep(1)

    else:
        print('[!] No USB devices found.')

except KeyboardInterrupt:
    exit() 

