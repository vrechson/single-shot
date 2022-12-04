# single-shot
A tool designed to generate all possible payloads that can lead to RCE in blind SSRF scenarios.

### Usage
```sh
python3 single-shot.py --help
```

This command will show every option supported by the tool. The supported options are:

```console
usage: single-shot [-h] [-v] (-t [TARGET] | -l [TARGET_FILE]) [-c [COMMAND]] [-e [ENCODE_LEVEL]] [-p [PROTOCOL]] [-cn [CANARY_ADDRESS]] [-m [MODE]] [-f [FILTER ...]] [-V]

Generate possible RCE payloads to use in with blind SSRF scenarios

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -t [TARGET], --target [TARGET]
                        Set the target internal domain name or IP address
  -l [TARGET_FILE], --target-list [TARGET_FILE]
                        Set the target list containing internal domain names or IP addresses
  -c [COMMAND], --command [COMMAND]
                        Set the command to be executed
  -e [ENCODE_LEVEL], --encode [ENCODE_LEVEL]
                        Set the payload's URLencode level,ex: -e 0 will not encode the payload -e 2 will double URLencode the output
  -p [PROTOCOL], --protocol [PROTOCOL]
                        Set the internal address protocol. default is http://
  -cn [CANARY_ADDRESS], --canary [CANARY_ADDRESS]
                        Set canary address to confirm internal services
  -m [MODE], --mode [MODE]
                        There are currently three supported modes: canary (deafult mode: generate canary payloads) rce (generate payloads that can lead to RCE) all (generates RCE and Canary payloads)
  -f [FILTER ...], --filter [FILTER ...]
                        Filter category, framework or a specific payload from the results default: exclude Shellshock payloads
  -V, --verbose         Show name of the exploited service and vulnerability for each payload

After all, we are all alike
```

### Running

Generating payloads to look for SSRF canaries:
```sh
python3 single-shot.py -t 127.0.0.1 -cn subdomain.collaborator.net -m canary
```

Generating double encoded payloads to look for SSRF canaries:
```sh
python3 single-shot.py -l addresses.txt -cn https://subdomain.collaborator.net -m canary -e 2
```

Payloads to look for RCE ignoring the framwork Jira:
```sh
python3 single-shot.py -l addresses.txt -c 'touch vrechson' -m rce -f Jira
```

Displaying details about every payload considering the internal framweorks use HTTPS:
```sh
python3 single-shot.py -l addresses.txt -c 'touch vrechson' -m rce -p https -V
```

### Credits
All current payloads were taken from this [assetnote blogpost](https://blog.assetnote.io/2021/01/13/blind-ssrf-chains/).

### Contributing
You can contribute openning isses, submitting pull requests or through [!["Buying a coffee for me"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/vrechson)