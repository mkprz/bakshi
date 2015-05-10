
def separate_network():
	s = """ # GUESTWIFI.separate_network
		uci add_list network.interface = "guestwifi"
		uci set network.interface.last.proto = 'static'
		uci set network.interface.last.ipaddr = '10.0.0.1'
		uci set network.interface.last.netmask = '255.255.255.0'

		uci add_list wirelss.wifi-iface
		uci set wirelss.wifi-iface.last.device = wirelss.wifi-iface.first.device
		uci set wirelss.wifi-iface.last.mode = 'ap'
		uci set wirelss.wifi-iface.last.network = 'guest'
		uci set wirelss.wifi-iface.last.ssid = 'guest'
		uci set wirelss.wifi-iface.last.encryption = 'none'

		uci add_list dhcp.dhcp = "guest"
		uci set dhcp.dhcp.last.interface = 'guest'
		uci set dhcp.dhcp.last.start = '50'
		uci set dhcp.dhcp.last.limit = '200'
		uci set dhcp.dhcp.last.leasetime = '1h'

		uci add_list firewall.zone
		uci set firewall.zone.last.name = 'guest'
		uci set firewall.zone.last.network = 'guest'
		uci set firewall.zone.last.input = 'REJECT'
		uci set firewall.zone.last.forward = 'REJECT'
		uci set firewall.zone.last.output = 'ACCEPT'

		uci add_list firewall.forwarding
		uci set firewall.forwarding.last.src = 'guest'
		uci set firewall.forwarding.last.dest = 'wan'

		uci add_list firewall.rule
		uci set firewall.rule.last.name = 'Allow DNS Queries'
		uci set firewall.rule.last.src = 'guest'
		uci set firewall.rule.last.dest_port = '53'
		uci set firewall.rule.last.proto = 'tcpudp'
		uci set firewall.rule.last.target = ACCEPT'

		uci add_list firewall.rule
		uci set firewall.rule.last.name = 'Allow DHCP request'
		uci set firewall.rule.last.src = 'guest'
		uci set firewall.rule.last.src_port = '67-68'
		uci set firewall.rule.last.dest_port = '67-68'
		uci set firewall.rule.last.proto = 'udp'
		uci set firewall.rule.last.target = ACCEPT'
		"""

	return s
