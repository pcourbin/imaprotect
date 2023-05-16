=======
History
=======

1.0.4 (2023-05-16)
------------------

* Correction of depreciated code (since 2023.5) by a PR of `@fslef`_, on a proposition of `@bcze91`_.

1.0.3 (2021-12-31)
------------------

* Update login procedure according to new IMAProtect "API", thanks to `@Thesola10`_
* Initial cameras support, thanks to `@Thesola10`_


1.0.2 (2021-12-31)
------------------

* Update imports to remove references to `HTTP_CODES` from `homeassistant.const`

1.0.0 (2021-05-22)
------------------

* Full rewrite using a alarm_control_panel based on work for `Verisure Alarm`_ by `@frenck`_.
* Able to get the status and change the status of the alarm using a alarm_control_panel
* Option to define/change a code (number or digit) in configuration of the integration. By default, no code is needed.
* Remove the configuration using YAML, only possible using the UI.

.. _`Verisure Alarm`: https://github.com/home-assistant/core/tree/dev/homeassistant/components/verisure
.. _`@frenck`: https://github.com/frenck

0.4.0 (2021-05-13)
------------------

* Full rewrite using platform/devices
* Allow adding devices/entities without knowing the API: counter, digitalinput, enocean, post, relay, supplierindex, toroid, virtualoutput, x4fp, xthl
* Allow selecting different components (e.g. for `enocean`, you can select `sensor`, `switch` or `light`)

0.3.0 (2021-05-09)
------------------

* Update pyimaprotect, using new IMAProtect "API"
* Older versions are not working anymore


0.1.0 (2021-04-08)
------------------

* First version



.. _`@Thesola10`: https://github.com/Thesola10
.. _`@bcze91`: https://github.com/bcze91
.. _`@fslef`: https://github.com/fslef
