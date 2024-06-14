---
search:
  boost: 0.5
---

# .CRP

In swap there are three implementation of a crop module: simple (fixed) crop, WOFOST implementation and a dynamic grass growth. Each requires slightly different set of variables. Below are the templates of the .crp files.

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
