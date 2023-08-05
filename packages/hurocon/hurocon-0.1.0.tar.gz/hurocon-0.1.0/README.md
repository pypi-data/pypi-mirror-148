# Hurocon
Hurocon *(**hu**awei **ro**uter **con**trol)* - command line interface tool for interacting with Huawei LTE routers


## Features
- Device Control
  - Reboot
- SMS Control
  - Send

> **Planned**:  
> *Device Control* - `Information/Stats`, `Signal Level`, `LED Control`;  
> *SMS Control* - `List`, `View`;  
> *Connection Control* - `WiFi Settings/Switches`, `Cellular Settings/Switches`;  


## Supported Devices
Full list of supported devices is available on [this link](https://github.com/Salamek/huawei-lte-api#tested-on).


## Installation
Currently this tool can only be installed with `pip` on `python` >= 3.7. You can install it from PyPi:

```bash
pip install hurocon
```

Or directly from this Github repo:

```bash
pip install git+https://github.com/maximilionus/hurocon.git
```

> Built executable mode *([pyinstaller](https://pyinstaller.org/)-based)* is planned but no ETA yet


## Quickstart
### Intro
After successful [installation](#installation) of this tool it can be accessed in shell using the following commands:

```bash
$ hurocon
# OR
$ python -m hurocon
```

You can also view a list of all root commands with:
```bash
$ hurocon --help
```

Each command in this tool has a special `--help` flag to display detailed information about it

### Authentification
First of all, you need to specify the authorization and connection data so that this tool can access the router in the future. You do it in two ways.

- In interactive mode:
  ``` bash
  $ hurocon auth login
  ```

- Manually, by running:
  ```bash
  # Initialize local configuration file
  $ hurocon config init

  # Show path to local configuration file
  $ hurocon config path
  ```

  And then manually editing the `json` file with any text editor. It has a human-readable structure, so every part of it is exactly what you think it is.

### Testing Connection
After auth details successfully specified you can test your connection with router by running

```bash
$ hurocon auth test

# Returns
# Success: Successful Authentification
# Failure: Auth failed, reason: "..."
```

### Conclusion
That's it, you're ready to go. And remember - no matter how deep you go, `--help` flag is always here to help 👍


## Special
Big thanks to [Adam Schubert](https://github.com/Salamek) for his amazing [`huawei-lte-api`](https://github.com/Salamek/huawei-lte-api) package, that made this whole thing possible.
