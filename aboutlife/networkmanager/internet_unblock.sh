#!/usr/bin/env bash

TAG="ABOUTLIFE_TEMP_RULE"
IPTABLES="sudo /usr/bin/env iptables"
IP6TABLES="sudo /usr/bin/env ip6tables"

delete_tagged_rules ()
{
IPTABLES_CMD="$1"
CHAIN="$2"

# list all our tagged rules in reverse order

$IPTABLES_CMD -L $CHAIN --line-numbers | grep "$TAG" | awk '{ print $1 }' | tac | while read -r RULE_NUM; do
    echo "Deleting rule $RULE_NUM for chain $CHAIN"
    $IPTABLES_CMD -D $CHAIN $RULE_NUM
done
}

delete_tagged_rules "$IPTABLES" "INPUT"
delete_tagged_rules "$IPTABLES" "OUTPUT"
delete_tagged_rules "$IP6TABLES" "INPUT"
delete_tagged_rules "$IP6TABLES" "OUTPUT"
