=====================================================
`IMA Protect Alarm`_ component for `Home Assistant`_
=====================================================


.. image:: https://img.shields.io/github/license/pcourbin/imaprotect.svg
        :target: (LICENSE)
        :alt: License

.. image:: https://img.shields.io/badge/HACS-Default-orange.svg
        :target: `hacs`_
        :alt: HACS

.. image:: https://img.shields.io/badge/community-forum-brightgreen.svg
        :target: `forum`_
        :alt: Community Forum

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen
        :target: `pre-commit`_
        :alt: pre-commit

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: `black`_
        :alt: Black

.. image:: https://img.shields.io/badge/maintainer-%40pcourbin-blue.svg
        :target: `user_profile`_
        :alt: Project Maintenance

.. image:: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg
        :target: `buymecoffee`_
        :alt: BuyMeCoffee


| This is a *custom component* for `Home Assistant`_.
| The *imaprotect* integration allows you to get information from your `IMA Protect Alarm`_.
|
| This work is inspired by on the work on `Verisure Alarm`_ by `@frenck`_ for `Home Assistant`_.
| It uses python package `pyimaprotect`_ to call the IMA Protect API, based on the work of of `lplancke`_ and `chris94440`_ for `Jeedom`_.

`Documentation`_
----------------
See https://pcourbin.github.io/imaprotect

Installation
------------
This integration requires a running Selenium server to retrieve images. Deploy the Selenium standalone Firefox Docker container below, and when creating the IMAProtect client set the remote_webdriver parameter to the correct WebDriver URL reachable from your Home Assistant instance (for example: ``http://localhost:4444`` or ``http://selenium_firefox:4444``).

.. note:: Make sure the WebDriver URL you provide in ``remote_webdriver`` is accessible from the environment where Home Assistant runs.

.. code-block:: yaml

  services:
    firefox:
      container_name: selenium_firefox
      image: selenium/standalone-firefox:143.0-20251020
      shm_size: 2g
      ports:
        - "4444:4444"
        - "7900:7900"

Usage:
# 1. Save this as docker-compose.yml in the project folder.
# 2. Start with: docker-compose up -d
# 3. When creating IMAProtect, provide the WebDriver URL, for example:
#    remote_webdriver='http://localhost:4444'  (adjust host/port to match your deployment)

Configuration
-------------

To add imaprotect to your installation:

* go to Configuration >> Integrations in the UI,
* click the button with + sign and from the list of integrations
* select *IMA Protect Alarm*.

It will add a *alarm_control_panel* with the state of your alarm:

.. list-table:: List of Alarm status values
   :widths: auto
   :header-rows: 1

   * - Alarm Value
     - IMA State
   * - `disarmed`
     - `OFF`
   * - `armed_home`
     - `PARTIAL`
   * - `armed_away`
     - `ON`

Then, **you can define a code** (number or digit) in the configuration of the integration. By default, no code is needed.

If your IMA Protect account lists security cameras, they will be added as *camera* entities. These entities do not currently refresh automatically, and only display the last picture taken.

Credits
-------
| This work is inspired by the work of `Verisure Alarm`_ by `@frenck`_ for `Home Assistant`_.
| This repo structure was inspired by `oncleben31/cookiecutter-homeassistant-custom-component`_ project template created with Cookiecutter_.

.. _`IMA Protect Alarm`: https://www.imaprotect.com/1483-domotique-ethernet-webserver-ipx800-v4-3760309690001.html
.. _`Home Assistant`: https://www.home-assistant.io/
.. _`pyimaprotect`: https://github.com/pcourbin/pyimaprotect
.. _`lplancke`: https://github.com/lplancke/jeedom_alarme_IMA
.. _`Jeedom`: https://www.jeedom.com
.. _`chris94440`: https://github.com/chris94440
.. _`Verisure Alarm`: https://github.com/home-assistant/core/tree/dev/homeassistant/components/verisure
.. _`@frenck`: https://github.com/frenck

.. _`Documentation`: https://pcourbin.github.io/imaprotect

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`oncleben31/cookiecutter-homeassistant-custom-component`: https://github.com/oncleben31/cookiecutter-homeassistant-custom-component

.. _`hacs`: https://hacs.xyz
.. _`forum`: https://community.home-assistant.io/
.. _`pre-commit`: https://github.com/pre-commit/pre-commit
.. _`black`: https://github.com/psf/black
.. _`user_profile`: https://github.com/pcourbin
.. _`buymecoffee`: https://www.buymeacoffee.com/pcourbin
