Set interface to DHCP

netsh interface ip set address "Local Area Connection" dhcp

schedule reboot 2

shutdown -r -f -c "Chase scheduled reboot for testing"

set ip for interface

netsh interface ip set address "Local Area Connection" static 10.1.1.3 255.255.255.0 10.1.1.2 1

set ip info from file

netsh -f c:\setteamip.txt

setteamip.txt

#========================
# Interface configuration
#========================
pushd interface

reset all


popd
# End of interface configuration

#========================
# Interface configuration
#========================
pushd interface ipv6

uninstall


popd
# End of interface configuration



# ----------------------------------
# ISATAP Configuration
# ----------------------------------
pushd interface ipv6 isatap



popd
# End of ISATAP configuration



# ----------------------------------
# 6to4 Configuration
# ----------------------------------
pushd interface ipv6 6to4

reset



popd
# End of 6to4 configuration

#========================
# Port Proxy configuration
#========================
pushd interface portproxy

reset


popd
# End of Port Proxy configuration



# ---------------------------------- 
# Interface IP Configuration         
# ---------------------------------- 
pushd interface ip


# Interface IP Configuration for "Network Team 1"

set address name="Network Team 1" source=static addr=10.1.1.1 mask=255.255.255.0
set address name="Network Team 1" gateway=10.1.1.2 gwmetric=0
set dns name="Network Team 1" source=static addr=127.0.0.1 register=PRIMARY
set wins name="Network Team 1" source=static addr=none


popd
# End of interface IP configuration

# end of set team ip
