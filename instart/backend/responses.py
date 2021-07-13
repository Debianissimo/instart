from copy import copy


def validateJSON(config):
    errors = []
    if "username" in config:
        if not "password" in config:
            errors.append("Username specified but no password specified.")

    return errors


async def getResponse(app, config, data):
    response = "done"
    errors = validateJSON(data)

    if not errors:
        for key, value in data.items():
            config[key] = value
    else:
        response = "error"

    return {"result": response, "errors": errors}
