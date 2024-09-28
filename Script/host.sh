#!/bin/bash

ip_address=$1

nmap -sn -oN /dev/stdout "$ip_address"