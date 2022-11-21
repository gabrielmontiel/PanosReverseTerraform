
resource "panos_panorama_security_policy" "europe_pre-rulebase_Test_Shared-1-1" {
    device_group = "europe"
    rulebase = "pre-rulebase"
    rule {
        
        name = "Test Shared-1-1"
        source_zones = ["america","europe"]
        source_addresses = ["any"]
        source_users = ["any"]
        #hip_profiles = ["any"]
        destination_zones = ["america"]
        destination_addresses = ["any"]
        applications = ["1und1-mail","2ch","ssl","web-browsing"]
        services = ["service-http","service-https"]
        categories = ["abused-drugs","business-and-economy"]
        action = "drop"
        #uuid = "28937b7d-e8e4-4542-b6cd-0451c207c7b4"
    }

    lifecycle {
        create_before_destroy = true
    }
}

resource "panos_panorama_security_policy" "spain_pre-rulebase_Test_Shared-1-2" {
    device_group = "spain"
    rulebase = "pre-rulebase"
    rule {
        
        name = "Test Shared-1-2"
        source_zones = ["america","europe"]
        source_addresses = ["any"]
        source_users = ["any"]
        #hip_profiles = ["any"]
        destination_zones = ["america"]
        destination_addresses = ["any"]
        applications = ["1und1-mail","2ch","ssl","web-browsing"]
        services = ["service-http","service-https"]
        categories = ["abused-drugs","business-and-economy"]
        action = "drop"
        #uuid = "dee5158e-ce3b-45d9-a5d8-3ba6a127addf"
    }

    lifecycle {
        create_before_destroy = true
    }
}

resource "panos_panorama_security_policy" "america_pre-rulebase_Test_Shared-1-1" {
    device_group = "america"
    rulebase = "pre-rulebase"
    rule {
        
        name = "Test Shared-1-1"
        source_zones = ["america","europe"]
        source_addresses = ["any"]
        source_users = ["any"]
        #hip_profiles = ["any"]
        destination_zones = ["america"]
        destination_addresses = ["any"]
        applications = ["1und1-mail","2ch","ssl","web-browsing"]
        services = ["service-http","service-https"]
        categories = ["abused-drugs","business-and-economy"]
        action = "drop"
        #uuid = "80da6e25-d332-4912-9969-77696ea75233"
    }

    lifecycle {
        create_before_destroy = true
    }
}

resource "panos_panorama_security_policy" "usa_pre-rulebase_Test_Shared-1-2" {
    device_group = "usa"
    rulebase = "pre-rulebase"
    rule {
        
        name = "Test Shared-1-2"
        source_zones = ["america","europe"]
        source_addresses = ["any"]
        source_users = ["any"]
        #hip_profiles = ["any"]
        destination_zones = ["america"]
        destination_addresses = ["any"]
        applications = ["1und1-mail","2ch","ssl","web-browsing"]
        services = ["service-http","service-https"]
        categories = ["abused-drugs","business-and-economy"]
        action = "drop"
        #uuid = "e799add6-b165-4ae7-9129-5d4b408810db"
    }

    lifecycle {
        create_before_destroy = true
    }
}

resource "panos_panorama_security_policy" "shared_pre-rulebase_Test_Shared" {
    device_group = "shared"
    rulebase = "pre-rulebase"
    rule {
        
        name = "Test Shared"
        source_zones = ["america","europe"]
        source_addresses = ["any"]
        source_users = ["any"]
        #hip_profiles = ["any"]
        destination_zones = ["america"]
        destination_addresses = ["any"]
        applications = ["1und1-mail","2ch","ssl","web-browsing"]
        services = ["service-http","service-https"]
        categories = ["abused-drugs","business-and-economy"]
        action = "drop"
        #uuid = "20d2dd9d-3c4c-4615-b2c2-b3259e9835ef"
    }

    lifecycle {
        create_before_destroy = true
    }
}

resource "panos_panorama_security_policy" "shared_pre-rulebase_Test_Shared-1" {
    device_group = "shared"
    rulebase = "pre-rulebase"
    rule {
        
        name = "Test Shared-1"
        source_zones = ["america","europe"]
        source_addresses = ["any"]
        source_users = ["any"]
        #hip_profiles = ["any"]
        destination_zones = ["america"]
        destination_addresses = ["any"]
        applications = ["1und1-mail","2ch","ssl","web-browsing"]
        services = ["service-http","service-https"]
        categories = ["abused-drugs","business-and-economy"]
        action = "drop"
        #uuid = "e3b36053-73af-42e9-a217-42b6a0a8df51"
    }

    lifecycle {
        create_before_destroy = true
    }
}
