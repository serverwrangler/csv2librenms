#!/usr/bin/python
import config
import math
import requests
import ipaddress
from ipaddress import IPv4Address
import pandas as pd

# Setup Requests Headers
request_headers = {"Content-Type": "application/json",
                   "Accept-Language": "en-US,en;q=0.5",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "X-Auth-Token": config.librenms_apikey,
                   "Connection": "keep-alive"
                   }

def device_add(add_request):
    api_url = "https://{}/api/v0/devices".format(config.librenms_ipaddress)
    r = requests.post(api_url, json=add_request, headers=request_headers)
    print(r.text)

def device_update(hostname, update_request):
    api_url = "http://{}/api/v0/devices/{}".format(config.librenms_ipaddress, hostname)
    r = requests.patch(api_url, json=update_request, headers=request_headers)
    print(r.text)

# Read CSV file
try:
    df = pd.read_csv("data/bulkadd.csv")
except FileNotFoundError:
    print("ERROR: data/bulkadd.csv missing")
    quit()

for index, row in df.iterrows():
    try:
        #DEBUG
        #print(row)
        # Add Device to LibreNMS via SNMP
        desc = row["Name:String(32):Required"]
        hostname = row["IP Address:Subnets(a.b.c.d/m#....):Required"]
        size = len(hostname)
        ip = hostname[:size - 3]
        community = row["SNMP:RO Community:String(32)"]
        #DEBUG
        #print(hostname)
        #print(ip)
        #print(community)
        add_device = {
            "hostname":ip,
            "community":community,
            "version":"v2c"
            }
        print(f"Attempting to add device {desc}...")
        device_add(add_device)
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    except:
        print("shit went sideways... :-(")
quit()
