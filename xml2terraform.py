import xmltodict
import os
import glob

PANORAMA_CONFIG_FILENAME = "running-config.xml"


def main():

    fileList = glob.glob("*.tf")
    for file in fileList:
        os.remove(file) if os.path.exists(file) else None

    with open(PANORAMA_CONFIG_FILENAME) as f:
        doc = xmltodict.parse(f.read())
        # Select device groups entries
        device_groups = doc["config"]["devices"]["entry"]["device-group"]["entry"]
        # Create a list with a single element if theres only one device group
        # To generalize the code
        device_groups = single_list(device_groups)

        # Select Shared DG and create a single elem list
        shared_dg = doc["config"]["shared"]
        shared_dg = single_list(shared_dg)

        # Append shared as a DG
        device_groups += shared_dg

        for dg in device_groups:
            # Get rules per rulebase
            for rulebase in ["pre-rulebase", "post-rulebase"]:
                write_policy_block(dg, rulebase)

            ###Get Addresses from DG
            addresses = dg.get("address", [])
            if addresses:
                addresses = single_list(addresses["entry"])
                dg_name = dg.get("@name", "shared")
            for address in addresses:
                address["dg_name"] = dg_name
                write_object_block(address)
                pass
            # Get address groups
            address_groups = dg.get("address-group", None)
            if address_groups:
                address_groups = address_groups["entry"]
                for address_group in address_groups:
                    write_group_object_block(address_group)
                    pass


def single_list(item):
    if not (isinstance(item, list)):
        item = [item]
    return item


def name_parser(name: str):
    return name.replace(" ", "_")


def write_policy_block(dg, rulebase):
    try:
        rules = dg[rulebase]["security"]["rules"]["entry"]
    except KeyError:
        return
    except TypeError:
        return
    rules = single_list(rules)
    multiples = [
        "category",
        "service",
        "from",
        "to",
        "destination",
        "source",
        "source-user",
        "source-hip",
        "application",
    ]
    for rule in rules:
        for key in rule.keys():
            if key in multiples:
                rule[key]["member"] = parseMultiples(rule[key]["member"])

        dg_name = dg.get("@name", "shared")
        with open(f"security_policies_{dg_name}.tf", "a") as f:
            f.write(policy_block(rule, dg_name, rulebase))


def write_object_block(address):
    with open(f"addresses.tf", "a") as f:
        f.write(object_block(address))


def write_group_object_block(group):
    with open(f"address_groups.tf", "a") as f:
        f.write(group_object_block(group))
    pass


def parseMultiples(value):
    if isinstance(value, list):
        return '","'.join(value)
    else:
        return value


def policy_block(rule, dg, rb):
    name = f"{dg}_{rb}_{rule['@name']}"
    name = name_parser(name)
    terraform_string = f"""
resource "panos_panorama_security_policy" "{name}" {{
    device_group = "{dg}"
    rulebase = "{rb}"
    rule {{
        name = "{rule["@name"]}"
        source_zones = ["{rule["from"]["member"]}"]
        source_addresses = ["{rule["source"]["member"]}"]
        source_users = {smartGet(rule, "null",["source-user","member"])}
        destination_zones = ["{rule["to"]["member"]}"]
        destination_addresses = ["{rule["destination"]["member"]}"]
        applications = ["{rule["application"]["member"]}"]
        services = ["{rule["service"]["member"]}"]
        categories = {smartGet(rule, "null",["category","member"])}
        action = "{rule["action"]}"
        

        description = "{rule.get("description","null")}"
        negate_source = {"true" if rule.get("negate-source", False) else "false"}
        negate_destination = {"true" if rule.get("negate-destination", False) else "false"}
        log_setting = "{rule.get("log-setting", "null")}"
        disabled = {"true" if rule.get("disabled", False) else "false"}
        group = "{deepGet(rule,"null", ["profile-setting","group","member"])}"

        #uuid = "{rule["@uuid"]}"

    }}

    lifecycle {{
        create_before_destroy = true
    }}
}}
"""
    return terraform_string


def deepGet(t: dict, default, keys: list):
    for key in keys:
        result = t.get(key, default)
        if result == default:
            return default
    return result


def smartGet(t: dict, default: str, keys: list):
    for key in keys:
        result = t.get(key, default)
        if result == default:
            return default
        else:
            t = result
    return f'["{t}"]'


def object_block(address):
    address_type = list(address.keys())[1]
    terraform_string = f"""
resource "panos_panorama_address_object" "{name_parser(address["@name"])}" {{

    device_group = "{address["dg_name"]}"
    name = "{address["@name"]}"
    value = "{address[address_type]}"
    type = "{address_type}"
    #description = ""

    lifecycle {{
        create_before_destroy = true
    }}
}}
"""
    return terraform_string


def parse_group_members(members):
    if isinstance(members, list):
        string = str(members).replace("'", '"')
    else:
        string = f'["{members}"]'
    return string


def group_object_block(group):
    terraform_string = f"""
# Static group
resource "panos_panorama_address_group" "example" {{
    name = "{group["@name"]}"
    description = null
    static_addresses = {parse_group_members(group["static"]["member"])}

    lifecycle {{
        create_before_destroy = true
    }}
}}
"""
    return terraform_string


main()
