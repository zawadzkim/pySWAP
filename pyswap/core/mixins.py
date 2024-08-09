import chardet

from .basemodel import PySWAPBaseModel


class FileMixin:
    """Saving and readin files.

    Not all classes require to be saved or have read functionality. Therefore,
    it makes sense to move this functionality from the main PySWAPBaseModel
    class to a mixin and use it only on classes that need it.

    Functions:
        save_file: Saves a string to a file.
        read_file: Reads a file from a string.

    """

    @staticmethod
    def save_file(
        string: str,
        fname: str,
        path: str,
        mode: str = "w",
        extension: str | None = None,
        encoding: str = "ascii",
    ) -> str:
        """Saves a string to a file.

        Arguments:
            string: The string to be saved to a file.
            extension: The extension that the file should have (e.g. 'txt',
                'csv', etc.).
            fname: The name of the file.
            path: The path where the file should be saved.
            mode: The mode in which the file should be opened (e.g. 'w' for
                write, 'a' for append, etc.).
            encoding: The encoding to use for the file (default is 'ascii').

        Returns:
            Success message.
        """

        if extension is not None:
            fname = f"{fname}.{extension}"

        with open(f"{path}/{fname}", f"{mode}", encoding=f"{encoding}") as f:
            f.write(string)

        return f"{fname}.{extension} saved successfully."

    @staticmethod
    def read_file(file_path: str) -> str:
        """Open file and detect encoding with chardet.

        Arguments:
            file_path (str): Path to the file to be opened.
        """
        with open(file_path, "rb") as f:
            raw_data = f.read()
        encoding = chardet.detect(raw_data)["encoding"]

        return raw_data.decode(encoding)


class SerializableMixin:
    """Converting a model to a SWAP-formatted string.

    This mixin is supposed to be used on classes that should
    directly serialize to a file and do not contain nested classes.
    Each class that has nested classes inheriting from this mixin
    should have a method utilizing this the functionality here to
    concatenate the files.
    """

    @staticmethod
    def format(attr, value) -> str:
        if attr.startswith("table_") or attr.startswith("list_"):
            fstring = f"{value}"
        else:
            fstring = f"{attr} = {value}\n"
        return fstring

    def concat_attributes(self) -> list[str | None]:
        """Concatenate the attributes of a PySWAPBaseModel class into a string.

        The object it's used on should be an instance of a PySWAPBaseModel
        with maximum 1 depth level. This is checked in
        the issubclass() conditional."""

        if not issubclass(type(self), PySWAPBaseModel):
            raise TypeError("Can only be used on a PySWAPBaseModel instance!")
        string = []
        for attr, value in self.model_dump(mode="json", exclude_none=True).items():
            if isinstance(value, dict):
                for k, v in value.items():
                    string.append(self.format(k, v))
            else:
                string.append(self.format(attr, value))

        return string


class ComplexSerializableMixin(SerializableMixin):
    """Serialize a class composed of nested models."""
    @staticmethod
    def concat_nested_models(file):
        string_list = []

        for section in dict(file).values():
            if section is None or isinstance(section, str):
                continue
            string_list.extend(section.concat_attributes())
        return "".join(string_list)
