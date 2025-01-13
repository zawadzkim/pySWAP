"""Core functionality for pySWAP.

Core package containing the main classes and functions for the SWAP model. It is
used mostly internally by the package. None of the functionality is directly
exposed to the user.

Modules:
    basemodel: Base models inherited by all pySWAP models.
    defaults: Variables shared across the package.
    fields: Custom field types for pySWAP serialization and deserialization.
    mixins: Reusable mixins enhancing functionality of specific PySWAPBaseModel.
    parsers: Functions to parse SWAP formatted ascii files into pySWAP objects.
    serializers: Functions to fine tune the serializatino of pySWAP objects to
        SWAP formatted ASCII.
    valueranges: Value ranges for pydantic Field objects used in pyswap
        validation.

Subpackages:
    cli: Command line interface for pySWAP (PROTOTYPE FEATURE).
    io: Input/output functionality for pySWAP.
    db: Database integrations for pySWAP.

Resources:
    validation.yaml: YAML file containing the validation schema for pySWAP
        models
"""
