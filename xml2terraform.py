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
                f.write(policy_block(rule, dg["@name"], rulebase))

    try:
        os.remove("main.tf")
    except OSError:
        pass

    with open(PANORAMA_CONFIG_FILENAME) as f:
        doc = xmltodict.parse(f.read())
        device_groups = doc["config"]["devices"]["entry"]["device-group"]["entry"]
        device_groups = single_list(device_groups)

        for dg in device_groups:
            try:
                pre_rules = dg["pre-rulebase"]["security"]["rules"]["entry"]
                pre_rules = single_list(pre_rules)
                writeblock(pre_rules, "pre-rulebase")
            except KeyError:
                pass
            try:
                post_rules = dg["post-rulebase"]["security"]["rules"]["entry"]
                post_rules = single_list(post_rules)
                writeblock(post_rules, "post-rulebase")
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
