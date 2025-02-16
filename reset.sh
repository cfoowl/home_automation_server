#!/bin/bash
echo ""  > /var/lib/misc/dnsmasq.leases
systemctl restart hostapd.service
systemctl restart dnsmasq.service