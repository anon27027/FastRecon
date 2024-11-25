#!/bin/bash

ip_address=$1

# Correct the command by removing the -oN flag and specifying a file for output
naabu -host "$ip_address" -o /dev/stdout
