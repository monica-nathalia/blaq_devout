ifconfig br0 down

brctl delbr br0
brctl addbr br0
brctl stp br0 off

# ifconfig br0 up

brctl addif br0 $1
brctl addif br0 $2

# ifconfig br0 down

ifconfig $1 0 0.0.0.0
ifconfig $2 0 0.0.0.0
ifconfig br0 10.0.0.2 netmask 255.255.255.0 up
# ifconfig br0 up