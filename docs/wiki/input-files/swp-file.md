---
search:
  boost: 0.5
---

# .SWP

The `.swp` file is the main configuration file for the SWAP model. It contains essential settings for the simulation and specifies which output information should be returned. In pySWAP, this file is managed by the `Model` class. When you call the `Model.run('./')` method, a `.swp` file is automatically created in a temporary directory along with all other input files, so you don't have to worry about handling it manually.

??? filetemplate "SWAP.template"

    ```txt
    {% include "./templates/SWAP.template" %}
    ```
