# netbox-ping-sweep


This code is used to find live hosts on a network, retrieve information about those hosts using Napalm, and create a new device in the Netbox database with specified parameters.

## This test was performed in a lab with a mix of Cisco vIOS and CSRV devices only.

How it works

1. Pinging a range of IP addresses to find live hosts and storing them in a CSV file.
2. Connecting to the live hosts, retrieving information using Napalm, and printing the result.
3. The hosts that respond to a PING but NAPALM is unable to connect to them are displayed on the screen.
4. Sending requests to the Netbox API to retrieve lists of device types and roles, and prompting the user to select one of each.
5. Sending a request to the Netbox API to create a new device with the specified parameters.

## Prerequisites IMPORTANT
You must create the following in Netbox before executing the script.
- Device Type
- Device Role
- Organization Site


## Example Script Run
![My Remote Image](https://i.imgur.com/sLixV5M.png)
## Netbox Devices
![My Remote Image](https://i.imgur.com/cdtiOl7.png)
