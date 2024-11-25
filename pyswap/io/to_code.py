from ..core import PySWAPBaseModel

def to_code(obj, filename='generated_model.py'):
    def _object_to_code(obj):
        code = []
        class_name = obj.__class__.__name__
        code.append(f"ps.{class_name}(")
        
        for attr, value in obj.__dict__.items():
            if isinstance(value, PySWAPBaseModel):
                code.append(f"    {attr}={_object_to_code(value)},")
            elif isinstance(value, (list, tuple)):
                code.append(f"    {attr}={_list_to_code(value)},")
            else:
                code.append(f"    {attr}={repr(value)},")
        
        code.append(")")
        return "\n".join(code)

    def _list_to_code(lst):
        if all(isinstance(item, PySWAPBaseModel) for item in lst):
            return "[" + ", ".join(_object_to_code(item) for item in lst) + "]"
        else:
            return repr(lst)
        
    code = []
    code.append("import pyswap as ps")
    code.append("from datetime import date as dt")
    code.append("")

    for attr, value in obj.__dict__.items():
        from pyswap.core.basemodel import PySWAPBaseModel
        if isinstance(value, PySWAPBaseModel):
            code.append(f"{attr} = {_object_to_code(value)}")
            code.append("")

    code.append("model = ps.Model(")
    for attr, value in obj.__dict__.items():
        if isinstance(value, PySWAPBaseModel):
            code.append(f"    {attr}={attr},")
    code.append(")")

    with open(filename, 'w') as f:
        f.write("\n".join(code))
