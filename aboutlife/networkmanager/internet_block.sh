#!/usr/bin/env bash

TAG="ABOUTLIFE_TEMP_RULE"
ADD_TAG="-m comment --comment '$TAG'"
IPTABLES="sudo /usr/bin/env iptables"
IP6TABLES="sudo /usr/bin/env ip6tables"

block_internet_interface ()
{
route_result=$(ip route get 8.8.8.8)

if [[ $route_result == *"unreachable"* ]]; then
    exit 0
fi

interface=$(sed -n 's/.*dev \([^\ ]*\).*/\1/p' <<< "$route_result")

$IPTABLES -I OUTPUT -o "$interface" -j DROP $ADD_TAG
$IP6TABLES -I OUTPUT -o "$interface" -j DROP $ADD_TAG
}

block_internet_interface
block_internet_interface
block_internet_interface

$IPTABLES -I INPUT -i lo -j ACCEPT $ADD_TAG
$IPTABLES -I OUTPUT -o lo -j ACCEPT $ADD_TAG
$IP6TABLES -I INPUT -i lo -j ACCEPT $ADD_TAG
$IP6TABLES -I OUTPUT -o lo -j ACCEPT $ADD_TAG

# TODO don't hardcode this ip, extract it from somewhere
$IPTABLES -I INPUT -s 192.168.1.0/24 -j ACCEPT $ADD_TAG
$IPTABLES -I OUTPUT -d 192.168.1.0/24 -j ACCEPT $ADD_TAG
$IPTABLES -I INPUT -s 192.168.18.0/24 -j ACCEPT $ADD_TAG
$IPTABLES -I OUTPUT -d 192.168.18.0/24 -j ACCEPT $ADD_TAG
