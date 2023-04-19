"""
This module provides a function to assign subnets to requested networks
based on a base CIDR network.
"""

import ipaddress
import json
import os
import argparse
from pprint import pprint
import csv


def get_cidr(network: dict) -> str:
    """Get the CIDR prefix length from a network dictionary.

    Args:
        network: A dictionary representing a network, with keys 'name', 'cidr', and 'vid'.

    Returns:
        The CIDR prefix length as a string.

    """
    return network["cidr"]


def assign_subnets(
    base_cidr: ipaddress.IPv4Network,
    networks: list,
    location_code: str,
    company_name: str,
) -> list:
    """
    Assigns subnets to the requested networks based on a base CIDR network.

    Args:
        base_cidr (ipaddress.IPv4Network): The base CIDR network to use.
        networks (list): A list of dictionaries containing network definitions.

    Returns:
        A list of dictionaries containing the network definitions, with the `network`,
        `subnetmask`, and `cidr` keys added.
    """

    # Keep track of used subnets
    used_networks = []

    # Iterate through the networks to assign subnets
    for network in sorted(networks, key=get_cidr):
        subnet_size = network["cidr"]
        available_subnets = list(base_cidr.subnets(new_prefix=subnet_size))

        # Find the first available subnet that does not overlap
        # with any previously allocated subnets
        for subnet in available_subnets:
            if not any(
                subnet.overlaps(ipaddress.IPv4Network(used_subnet))
                for used_subnet in used_networks
            ):
                used_networks.append(str(subnet))
                break

        # Assign the subnet to the network
        subnet_str = str(subnet)
        network["network"] = subnet_str
        network["subnetmask"] = str(subnet.netmask)
        network["cidr"] = str(subnet.prefixlen)
        network["company_description"] = f"{company_name} {network['name']}"
        network["location_description"] = f"{location_code} {network['name']}"

    return networks


def output_csv(
        network_list: list,
        path: str
):
    """
    Saves the results to a csv file.

    Args:
        network_list (list): A list of dictionaries containing network definitions.
        path: The file path of the csv.
    
    """
    
    # Get field names
    keys = network_list[0].keys()

    # Write data to file
    with open(path, 'w', newline='') as file:
        w = csv.DictWriter(file, keys)
        w.writeheader()
        w.writerows(network_list)


def main():
    """
    Assign subnets to requested networks based on a base CIDR network.

    This script takes in a JSON file containing network definitions
    and assigns subnets to each network based on a given base CIDR network.
    The resulting network definitions are printed to the console, sorted by CIDR prefix
    length.

    Required arguments:
    -s/--base-cidr: The base CIDR network to use.
    -j/--json-file: The JSON file containing the network definitions.
    -l/--location-code: The location code to use.
    -c/--company-name: The company name to use.

    Optional arguments:
    -o/--output-csv: save the output as csv.

    Returns:
    None
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Assign subnets to requested networks based on a base CIDR network."
    )
    parser.add_argument(
        "-s",
        "--base-cidr",
        metavar="BASE_CIDR",
        type=str,
        required=True,
        help="the base CIDR network to use",
    )
    parser.add_argument(
        "-j",
        "--json-file",
        metavar="JSON_FILE",
        type=str,
        required=True,
        help="the JSON file containing the network definitions",
    )
    parser.add_argument(
        "-l",
        "--location-code",
        metavar="LOCATION_CODE",
        type=str,
        required=True,
        help="the location code to use",
    )
    parser.add_argument(
        "-c",
        "--company-name",
        metavar="COMPANY_NAME",
        type=str,
        required=True,
        help="the company name to use",
    )
    parser.add_argument(
        "-o",
        "--output-csv",
        metavar="OUTPUT_CSV",
        type=str,
        required=False,
        help="the file path for csv output"
    )
    args = parser.parse_args()

    # Check that the base CIDR network has a valid format
    try:
        base_cidr = ipaddress.IPv4Network(args.base_cidr)
    except ValueError:
        print("Error: invalid base CIDR network format")
        return

    # Check that the JSON file exists
    if not os.path.isfile(args.json_file):
        print("Error: JSON file does not exist")
        return

    # Validate location code format
    if len(args.location_code) != 3:
        print("Error: location code must be exactly 3 characters")
        return

    # Convert the base CIDR network to an IPv4Network object
    base_cidr = ipaddress.IPv4Network(args.base_cidr)

    # Load the network definitions from the JSON file
    with open(args.json_file, "r", encoding="utf-8") as loaded_file:
        networks = json.load(loaded_file)

    # Assign subnets to the networks
    networks = assign_subnets(
        base_cidr, networks, args.location_code, args.company_name
    )

    # Print the networks and their descriptions
    for network in sorted(networks, key=get_cidr):
        pprint(
            f"{network['network']}, {network['company_description']}, {network['location_description']}"
        )

    # Save the output as csv
    if args.output_csv:
        output_csv(networks, args.output_csv)


if __name__ == "__main__":
    main()
