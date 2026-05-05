---
search:
  boost: 0.5
---

# .BBC

The .bbc file contains settings of the bottom boundary conditions. Normally it is included within the .swp file, but can also be excluded to a separate file.

!!! note

    For now, pySWAP does not include the option to create the .bbc file.

??? filetemplate "BBCFIL.template"

    ```txt
    {% include "./templates/BBCFIL.template" %}
    ```
