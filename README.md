[![License][license-shield]][license]
[![hacs][hacsbadge]][hacs]

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]
[![Community Forum][forum-shield]][forum]

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
| `0` | `OFF` |
| `1` | `PARTIAL` |
| `2` | `ON` |
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

[license-shield]: https://img.shields.io/github/license/pcourbin/imaprotect.svg?style=for-the-badge
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/

[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge

[maintenance-shield]: https://img.shields.io/badge/maintainer-%40pcourbin-blue.svg?style=for-the-badge
[buymecoffee]: https://www.buymeacoffee.com/pcourbin
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
