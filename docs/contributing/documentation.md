# Documentation is __critical__

Documentation is one of the most important part of the codebase; afterall, why bother writing and publishing software if no one else but the author knows how to use it.

Quite a few times after picking up development of a project after some time I realised that I do not remember myself how to use certain parts of the code. This becomes even more tricky once the codebase and contributors group grows.

I need to acknowledge however, that writing the documentation takes as long as coding. And it is not easy to keep up with changes nor it is easy, for the developer, to reaslise what has been explained poorly or not at all. Therefore, user experience and contribution is crutial.

Contributing to documentation is very easy, and takes the same step as contributing to code, but you can hardly break things. Moreover, it's a kind gesture, more than 90% of users will ever do.

If you'd like to support the project, but you are not quite familiar with Python, please look at the docs and find mistakes and areas to improve. If you have no time to make the fork, edit and submit a PR, please at least create an issue with `#docs` tag. It will help a lot!.

# Where can you contribute

pySWAP documentation can be split in two parts: API reference, which is generate automatically from docstrings in the code, user guide.

## User guide and Wiki

In this documentation I also placed a lot of information I thought was important from the perspective of a SWAP user. Even if you do not use pySWAP, you can go to the wiki and check what a particular variable does in the model.

That is mostly taken from the sample files provided with SWAP version 4.2.

## API reference
Contributing to the API reference can take a bit more skill. Over all throughout the project we use Google style documentation. Each component is documented with docstrings.

### Module documentation
At the top of each module, there is a docstring which describes what that particular module does and what elements are defined in it. Here is an example:

```Python
"""
Irrigation settings for the SWAP simuluation.

Classes:
    IrgFile: The irrigation file.
    FixedIrrigation: Fixed irrigation settings.
    ScheduledIrrigation: Irrigation scheduling settings.
    IRRIGATION: Information for each fixed irrigation event.

Functions:
    irg_from_csv: Load the irrigation file from a CSV file.
"""
```

By reading this, we immediatelly know what can we import from this module. This also works in your code editor; when you do `from pyswap import irrigation` and you hoover over the `irrigation`, you will see that docstring in a popup window.

### Classes and functions
Docstrings are defined directly under the class or function definition. They follow the standard Google pattern like so:

```Python
class Irrigation:
    """Holds the crop settings of the simulation.

    Attributes:
        swcrop (int): Switch for crop:

            * 0 - Bare soil.
            * 1 - Simulate crop.

        rds (Optional[float]): Rooting depth of the crop [cm].
        table_croprotation (Optional[Table]): Table with crop rotation data.
        cropfiles (Optional[List[CropFile]]): List of crop files.

    Methods:
        write_crop: Write the crop files.
"""
    # Definition of the class; attributes, etc.
```

There are a few twists, though.

#### Describe switch options
To make sure the switch options are displayed as a list, you have to add a new line before and after, write the list in 1 tab indentation and start each line with `*`.

### Other reusable elements
For instance if tyou define a new type of field, the docstring for that goes directly under the definition of the varialbe like so:

```Python
Arrays = Annotated[
    DataFrame,
    PlainSerializer(serialize_arrays, return_type=str, when_used="json")
]
"""Serialize pd.DataFrame without headers to a string with leading variable name."""
```

That docstring is then used by inpecting tools in code editors, helping users understand what it does and is automatically pulled by mkdocs to generate online documentation.