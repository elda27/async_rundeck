import stringcase

special_case_property = {
    "serverNodeUUID": "server_node_uuid",
    "serverNodeUUIDFilter": "server_node_uuid_filter",
    "serverUUID": "server_uuid",
    "jobref": "job_ref",
    "os": "OS",
    "loglevel": "log_level",
    "jobID": "job_id",
    "executionID": "execution_id",
}

invert_special_case_property = {v: k for k, v in special_case_property.items()}


def format_property(name: str) -> str:
    if name in special_case_property:
        return special_case_property[name]
    else:
        return stringcase.snakecase(name)


def invert_property(name: str) -> str:
    if name in invert_special_case_property:
        return invert_special_case_property[name]
    else:
        return stringcase.camelcase(name)
