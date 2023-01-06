from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir_csv.plugins.inventory import CsvInventory
from nornir.core.plugins.inventory import InventoryPluginRegister
from pypinger import pyping
import csv
import time
import requests
import pprint
from rich import print as rprint

your_dir = '/your/dir/path/inventory/'
netbox_endpoint = 'netbox-lab-demo.com'
api_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'


def find_live_host():
    print('*' * 100)
    rprint('[yellow]Running Ping Sweep.[/yellow]')
    print('*' * 100)
    live_hosts = pyping(count=3)
    print(live_hosts)
    print('*' * 100)
    rprint('[yellow]Creating Nornir Host CSV File.[/yellow]')
    print('*' * 100)
    with open(f'{your_dir}hosts.csv', 'w', encoding='UTF8', newline='') as f:
        header = ['name', 'hostname', 'platform']
        writer = csv.writer(f)
        writer.writerow(header)
    for i in live_hosts:
        data = [f'{i}', f'{i}', 'ios']
        with open(f'{your_dir}hosts.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
    time.sleep(3)


def run_nornir_napaml():
    InventoryPluginRegister.register("CsvInventoryPlugin", CsvInventory)
    nr = InitNornir(
        config_file=f"{your_dir}config.yaml"
    )

    with open(f'{your_dir}adding_these_host.csv', 'w', encoding='UTF8', newline='') as f:
        header = ['hostname']
        writer = csv.writer(f)
        writer.writerow(header)
    rprint('[yellow]Running NAPAML to each host in host file.[/yellow]')
    print('*' * 100)
    results = nr.run(task=napalm_get, getters=['get_facts'])
    for device, multi_result in results.items():
        if multi_result[0].failed == False:
            hostname = multi_result[0].result['get_facts']['hostname']
            data = [f'{hostname}']
            with open(f'{your_dir}adding_these_host.csv', 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
        else:
            rprint(
                f'[red]Received ICMP reply from {device} but NAPAML was unable to connect[/red]')
            print('*' * 100)
    time.sleep(3)
    rprint('[yellow]Created CSV file for sucessful NAPAML logins.[/yellow]')
    print('*' * 100)


def device_type_id():
    url = f"http://{netbox_endpoint}/api/dcim/device-types/"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Token {api_token}"}

    response = requests.get(url, headers=headers).json()
    print('*' * 100)
    for i in response['results']:
        pprint.pprint(i['manufacturer']['name'])
    print('*' * 100)
    user_input_device_type = input(
        'Enter the name of the manufacturer from the list above: ')
    matching_id = None
    for i in response['results']:
        if i['manufacturer']['name'] == user_input_device_type:
            matching_id = i['id']
            return matching_id


def device_role_id():
    url = f"http://{netbox_endpoint}/api/dcim/device-roles/"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Token {api_token}"}

    response = requests.get(url, headers=headers).json()
    print('*' * 100)
    for i in response['results']:
        pprint.pprint(i['display'])
    print('*' * 100)
    user_input_device_role = input(
        'Enter the device role from the list above: ')
    matching_id = None
    for i in response['results']:
        if i['name'] == user_input_device_role:
            matching_id = i['id']
            return matching_id


def device_site_id():
    url = f"http://{netbox_endpoint}/api/dcim/sites/"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Token {api_token}"}

    response = requests.get(url, headers=headers).json()
    print('*' * 100)
    for i in response['results']:
        pprint.pprint(i['display'])
    print('*' * 100)
    user_input_site_id = input(
        'Enter the site name from the list above: ')
    matching_id = None
    for i in response['results']:
        if i['display'] == user_input_site_id:
            matching_id = i['id']
            return matching_id


def netbox_api_request(device_id_type, device_role, device_site):
    url = f"http://{netbox_endpoint}/api/dcim/devices/"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Token {api_token}"}
    rprint('[yellow]Adding host to Netbox.[/yellow]')
    print('*' * 100)

    with open(f'{your_dir}adding_these_host.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            hostname = row[0]
            data = {
                "name": hostname,
                "device_type": device_id_type,
                "device_role": device_role,
                "site": device_site,
            }

            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                rprint(f'[green]{hostname} was successfully added.[/green]')
            else:
                rprint('[red]Failed to add: [/red]' + hostname)


if __name__ == '__main__':
    device_id_type = device_type_id()
    device_role = device_role_id()
    device_site = device_site_id()
    find_live_host()
    run_nornir_napaml()
    netbox_api_request(device_id_type=device_id_type,
                       device_role=device_role, device_site=device_site)
