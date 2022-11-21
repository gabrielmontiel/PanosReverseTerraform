# PanosReverseTerraform
Get Terraform files from  panorama configuration XML

## How to use

Run xml2terraform.py in the same directory as a Panorama running-config.xml file

Get main.tf with all the security Policies in the configuration in their respective Device Group and Rulebase

## NOTE: 
if you have dynamic object groups this program WONT work and WILL crash.
## Supports:

Security Policies
Address objects (All types)
Address groups (statics)
# Pending:

Address groups (dynamic)



### About terraformer

Ive seen that theres also this tool named terraformer (https://panos.pan.dev/docs/automation/terraformer_qs) that connect directly to the panorama/firewall to also do this kind of job, but it has let me down due to several limitations thats why im still working on tihis