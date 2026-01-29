import inspect
import json
from fastapi import File, Form, UploadFile
from pydantic import BaseModel

# Used to wrap the pydantic model as a decorator.
# When needed, the decorated pydantic model can be called <modelName>.as_form
# During which the decorator wrapper is called at runtime, replacing all fields and its 
# default values with Form() fields
# Basically hijacks the model at runtime and reorganize it to be interpreted as a form
# before going through TSA
def as_form(cls: type[BaseModel]):
    new_parameters = []

    # For every required field, translate that field's default value into default Form value
    for field_name, field_info in cls.model_fields.items():
        if field_info.annotation == UploadFile:
            continue

        if field_info.is_required():
            default_value = Form(...)
        else:
            default_value = Form(field_info.default)

        parameter = inspect.Parameter(
            field_name,  # Param name
            inspect.Parameter.POSITIONAL_ONLY,  # Type of param (as in positional param or keyword param, etc..)
            default=default_value,  # Default value assigned for the param
            annotation=field_info.annotation,  # Type hint of the param
        )
        new_parameters.append(parameter)  # Add newly constructed param to list

    for field_name, field_info in cls.model_fields.items():
        if field_info.annotation == UploadFile:
            parameter = inspect.Parameter(
                field_name,
                inspect.Parameter.POSITIONAL_ONLY,
                default=File(None) if not field_info.is_required() else File(...),
                annotation=UploadFile,
            )
            new_parameters.append(parameter)

    async def as_form_func(**data):
        processed_data = {}
        fields_in_request = set()

        # Remember, in Pydantic models, their fields can be type None which means the request
        # body can just not contain the field.
        # This is a set of ONLY fields specified in the request
        for field_name, field_info in cls.model_fields.items():
            if field_name in data and data[field_name] is not None:
                fields_in_request.add(field_name)

        # processed_data is a dictionary of ALL fields specified by the Pydantic model
        # That means even though peepeepoopoo isn't specified, it will still add it into
        # processed_data with its value being None
        for field_name, field_info in cls.model_fields.items():
            if field_name not in data or data[field_name] is None:
                processed_data[field_name] = data.get(field_name)
                continue
            
            # In the case the field was specified in the request body
            value = data[field_name]

            # In the case the value is detected as string but the field type specified isn't 
            # str
            # This is here because of Pydantic's tendency to treat fields that it doesn't
            # recognize as just string
            if isinstance(value, str) and field_info.annotation is not str:
                try:
                    if (
                        hasattr(field_info.annotation, "__origin__")
                        and field_info.annotation.__origin__ is dict
                    ):
                        processed_data[field_name] = json.loads(value)
                    elif isinstance(field_info.annotation, type) and issubclass(
                        field_info.annotation, BaseModel
                    ):
                        json_data = json.loads(value)
                        processed_data[field_name] = (
                            field_info.annotation.model_validate(json_data)
                        )
                    else:
                        processed_data[field_name] = json.loads(value)
                except (json.JSONDecodeError, ValueError):
                    processed_data[field_name] = value
            else:
                processed_data[field_name] = value
        instance = cls(**processed_data)
        setattr(instance, "_fields_in_request", fields_in_request)
        return instance

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig
    setattr(cls, "as_form", as_form_func)
    return cls
