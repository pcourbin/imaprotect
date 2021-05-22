.. highlight:: shell

============
Installation
============

From `HACS`_
------------

1. Search "IMAProtect Alarm" in `integrations` of `HACS`_ store.
2. Click install.
3. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "IMAProtect Alarm".

From sources
------------

The sources for imaprotect can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/pcourbin/imaprotect

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/pcourbin/imaprotect/tarball/master

Once you have a copy of the source, you can install it with in your `Home Assistant`_ installation:


1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `imaprotect`.
4. Download _all_ the files from the `custom_components/imaprotect/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "IMAProtect Alarm"

.. _Github repo: https://github.com/pcourbin/imaprotect
.. _tarball: https://github.com/pcourbin/imaprotect/tarball/master
.. _`Home Assistant`: https://www.home-assistant.io/
.. _`HACS`: https://hacs.xyz
