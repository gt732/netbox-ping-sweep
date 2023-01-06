# netbox-ping-sweep


This code is used to find live hosts on a network, retrieve information about those hosts using Napalm, and create a new device in the Netbox database with specified parameters.

How it works

1. Pinging a range of IP addresses to find live hosts and storing them in a CSV file.
2. Connecting to the live hosts, retrieving information using Napalm, and printing the result.
3. Sending requests to the Netbox API to retrieve lists of device types and roles, and prompting the user to select one of each.
4. Sending a request to the Netbox API to create a new device with the specified parameters.
