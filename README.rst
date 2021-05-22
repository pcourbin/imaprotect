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

This is a *custom component* for `Home Assistant`_.
The *imaprotect* integration allows you to get information from your `IMA Protect Alarm`_.
It uses python package `pyimaprotect`_ to call the IMA Protect API, based on the work of of `lplancke`_ and `chris94440`_ for `Jeedom`_.


`Documentation`_
----------------
See https://pcourbin.github.io/imaprotect

Full Example
------------

To add imaprotect to your installation, go to Configuration >> Integrations in the UI, click the button with + sign and from the list of integrations select *IMA Protect Alarm*.
It will add a single sensor with the state of your alarm:

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

Alternatively, you need to add the following to your configuration.yaml file:

.. code-block:: yaml

  # Example configuration.yaml entry
  sensor:
    - platform: imaprotect
      name: "My IMA Protect"
      username: "myusername"
      password: "mypassword"



Credits
-------

| This repo structure was inspired by `oncleben31/cookiecutter-homeassistant-custom-component`_ project template created with Cookiecutter_.

.. _`IMA Protect Alarm`: https://www.imaprotect.com/1483-domotique-ethernet-webserver-ipx800-v4-3760309690001.html
.. _`Home Assistant`: https://www.home-assistant.io/
.. _`pyimaprotect`: https://github.com/pcourbin/pyimaprotect
.. _`lplancke`: https://github.com/lplancke/jeedom_alarme_IMA
.. _`Jeedom`: https://www.jeedom.com
.. _`chris94440`: https://github.com/chris94440

.. _`Documentation`: https://pcourbin.github.io/imaprotect

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`oncleben31/cookiecutter-homeassistant-custom-component`: https://github.com/oncleben31/cookiecutter-homeassistant-custom-component

.. _`hacs`: https://hacs.xyz
.. _`forum`: https://community.home-assistant.io/
.. _`pre-commit`: https://github.com/pre-commit/pre-commit
.. _`black`: https://github.com/psf/black
.. _`user_profile`: https://github.com/pcourbin
.. _`buymecoffee`: https://www.buymeacoffee.com/pcourbin
