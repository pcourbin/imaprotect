[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
[![Community Forum][forum-shield]][forum]
[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

# [IMA Protect Alarm](https://www.imaprotect.com/) component for [Home Assistant](https://www.home-assistant.io/)

This is a _custom component_ for [Home Assistant](https://www.home-assistant.io/).
The `imaprotect` integration allows you to get and set the status of your [IMA Protect Alarm](https://www.imaprotect.com/).
This work is inspired by the work on [Verisure Alarm](https://github.com/home-assistant/core/tree/dev/homeassistant/components/verisure) by [@frenck](https://github.com/frenck).

{% if not installed %}

### Installation

1. Click install.
2. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "IMA Protect Alarm".

{% endif %}

### [Docs (installation, config, and issues)](https://pcourbin.github.io/imaprotect)

### Quick start

To add imaprotect to your installation:

- go to Configuration >> Integrations in the UI,
- click the button with + sign and from the list of integrations
- select `IMA Protect Alarm`.

It will add a _alarm_control_panel_ with the state of your alarm:

| Alarm Value  | IMA State |
| :----------: | :-------: |
|  `disarmed`  |   `OFF`   |
| `armed_home` | `PARTIAL` |
| `armed_away` |   `ON`    |

#### Define a code

Then, you can define a code (number or digit) in the configuration of the integration. By default, no code is needed.

[license-shield]: https://img.shields.io/github/license/pcourbin/imaprotect.svg
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg
[forum]: https://community.home-assistant.io/
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40pcourbin-blue.svg
[buymecoffee]: https://www.buymeacoffee.com/pcourbin
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg
[user_profile]: https://github.com/pcourbin
