import xmltodict
import os

PANORAMA_CONFIG_FILENAME = "running-config.xml"


def main():
    def writeblock(rules, rulebase):
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
            for prop in multiples:
                if isinstance(rule[prop]["member"], list):
                    rule[prop]["member"] = '","'.join(rule[prop]["member"])
            with open("main.tf", "a") as f:
                dg_name = dg.get("@name", "shared")
                f.write(policy_block(rule, dg_name, rulebase))

    try:
        os.remove("main.tf")
    except OSError:
        pass

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
            for rulebase in ["pre-rulebase", "post-rulebase"]:
                try:
                    rules = dg[rulebase]["security"]["rules"]["entry"]
                    rules = single_list(rules)
                    writeblock(rules, rulebase)
                except KeyError:
                    pass


def single_list(item):
    if not (isinstance(item, list)):
        item = [item]
    return item


def policy_block(rule, dg, rb):
    def name_parser(name: str):
        return name.replace(" ", "_")

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
        source_users = ["{rule["source-user"]["member"]}"]
        #hip_profiles = ["{rule["source-hip"]["member"]}"]
        destination_zones = ["{rule["to"]["member"]}"]
        destination_addresses = ["{rule["destination"]["member"]}"]
        applications = ["{rule["application"]["member"]}"]
        services = ["{rule["service"]["member"]}"]
        categories = ["{rule["category"]["member"]}"]
        action = "{rule["action"]}"
        #uuid = "{rule["@uuid"]}"
    }}

    lifecycle {{
        create_before_destroy = true
    }}
}}
"""
    return terraform_string


main()
