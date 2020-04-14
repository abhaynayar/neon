# fridar

👾 a simple fᴙida wrapper

### Setup

Requirements:

- frida
- python3

Clone this repository `git clone https://github.com/abhaynayar/fridar`

### Usage

Use the `-h` flag to see the required arguments.

```bash
$ python3 fridar.py -p com.tinder -s onresume

       __      _     _            
      / _|_ __(_) __| | __ _ _ __ 
     | |_| '__| |/ _` |/ _` | '__|
     |  _| |  | | (_| | (_| | |   
     |_| |_|  |_|\__,_|\__,_|_| v0.1.0

        *a simple frida wrapper*
    http://github.com/abhaynayar/fridar


[+] Starting onResume method hijack.
[.] Enter method name (example: com.package.class.method): com.tinder.settings.activity.SettingsActivity
[.] Now open the activity on your device.
[+] com.tinder.settings.activity.SettingsActivity.onResume has been hijacked!
```

