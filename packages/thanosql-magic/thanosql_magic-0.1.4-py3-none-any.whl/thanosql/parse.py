import re
from types import ModuleType


def convert_local_ns(query_string, local_ns) -> str:
    # remove local_ns items with ModuleType
    local_ns = {
        key: val for key, val in local_ns.items() if not isinstance(val, ModuleType)
    }

    # variables need to be converted
    var_list = list(set(map(str.strip, re.findall(r"=( *?\w+)", query_string))))

    # modifying query_string
    for i in range(len(var_list)):
        var = local_ns.get(var_list[i])

        if var:
            query_string = query_string.replace(var_list[i], f"'{str(var)}'")

    return query_string


def is_url(s):
    p = re.compile(r"^\w*://\w*")
    m = p.match(s)

    if m:
        return True
    else:
        return False
