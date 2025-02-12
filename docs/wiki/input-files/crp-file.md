---
search:
  boost: 0.5
---

# .CRP

A .crp file defines crop parameters for different crop models. There are three types of crop modules in SWAP: simple (fixed) crop, WOFOST implementation, and dynamic grass growth. Each module requires a specific set of variables, which are outlined in their respective .crp file templates.

- Simple (fixed) crop - This module uses a fixed set of parameters for crop growth.
- WOFOST crop - This module follows the WOFOST model, which is more detailed.
- Dynamic grass growth - This module simulates the growth of grass dynamically over time.

## Simple (fixed) crop

??? filetemplate "CROPFIL_FIXED.template"

    ```txt
    {% include "./templates/CROPFIL_FIXED.template" %}
    ```

## WOFOST crop

??? filetemplate "CROPFIL_WOFOST.template"

    ```txt
    {% include "./templates/CROPFIL_WOFOST.template" %}
    ```

## Grass

To be added soon.
