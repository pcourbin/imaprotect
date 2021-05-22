=====
Usage
=====
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