#!/bin/bash

ip_address=$1 

sudo nmap -F "$ip_address" -oN /dev/stdout