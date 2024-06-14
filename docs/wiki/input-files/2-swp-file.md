---
search:
  boost: 0.5
---

# .SWP

.swp file is the main configuration file for the SWAP model. It contains all the settings for the simulation and indicates which additional files should be created. In pySWAP, this file is represented by the main class `Model`. Upon calling `Model.run('./')` method on a model object, a .swp file is created in a temporary directory along with all other input files. So you do not even see the file anymore.

??? filetemplate "SWAP.template"

    ```txt
    {% include "./templates/SWAP.template" %}
    ```
