# [IMA Protect Alarm](https://www.imaprotect.com/) component for [Home Assistant](https://www.home-assistant.io/)

This is a *custom component* for [Home Assistant](https://www.home-assistant.io/). 
The `imaprotect` integration allows you to get information from your [IMA Protect Alarm](https://www.imaprotect.com/).
It uses python package [pyimaprotect](https://github.com/pcourbin/pyimaprotect) to call the IMA Protect API, based on the work of [lplancke](https://github.com/lplancke/jeedom_alarme_IMA) for [Jeedom](https://www.jeedom.com).

## Installation

Copy the `custom_components/imaprotect` folder into the config folder.

## Configuration

To add imaprotect to your installation, go to Configuration >> Integrations in the UI, click the button with + sign and from the list of integrations select `IMA Protect Alarm`.
It will add a single sensor with the state of your alarm:

| Alarm Value | State |
|:----:|:----:|
| `0` | `ON` |
| `1` | `PARTIAL` |
| `2` | `OFF` |
| `-1` | `UNKNOWN` |

Alternatively, you need to add the following to your configuration.yaml file:
```yaml
# Example configuration.yaml entry
sensor:
  - platform: imaprotect
    name: "My IMA Protect"
    username: "myusername"
    password: "mypassword"
```