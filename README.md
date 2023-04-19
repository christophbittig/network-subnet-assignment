# Network Subnet Assignment

This script assigns subnets to requested networks based on a base CIDR network. The assigned subnets are non-overlapping and cover the entire base CIDR network.

## Requirements

* Python 3.6 or higher
* `ipaddress` module (included in Python 3)
* `json` module (included in Python 3)
* `argparse` module (included in Python 3)

## Usage

```python
python subnetting.py -s BASE_CIDR -j JSON_FILE -l LOCATION_CODE -c COMPANY_NAME
```

* `-s`, `--base-cidr`: the base CIDR network to use (required)
* `-j`, `--json-file`: the JSON file containing the network definitions (required)
* `-l`, `--location-code`: a 3-character location code to use in network descriptions (required)
* `-c`, `--company-name`: the company name to use in network descriptions (required)
* `-o`, `--output-csv`: save the output as csv (optional)

## JSON File Format

The JSON file should be an array of network objects, where each object has the following properties:

* `name`: the name of the network
* `cidr`: the size of the network in CIDR notation (e.g. `22`)
* `vid`: the VLAN ID to use for the network

Example JSON file:

```json
[
    {
        "name": "server",
        "cidr": 22,
        "vid": 2000
    },
    {
        "name": "clients",
        "cidr": 22,
        "vid": 2010
    },
    {
        "name": "guest-wifi",
        "cidr": 22,
        "vid": 2021
    }
]
```

## Output

The script outputs the assigned subnets for each network in the following format:

```text
192.0.1.0/24 clients (My Company - FMC)
192.0.2.0/24 server (My Company - LMC)
192.0.3.0/24 guest (My Company - GUEST)
```

The network description includes the company name and location code.

If provided, the output is saved to a csv file.

## License

This project is licensed under the terms of the MIT license.
