import api

def print_green(skk): print("\033[92m {}\033[00m" .format(skk))

print('Testing API')
print('indices: ', api.get_indices())
protocols=api.get_protocols()
print('protocols: ',protocols) 
#print('flows with the protocol ', protocols[0], ': ', api.get_flows(protocols[0]))
print_green('get_protocols_flows_count()')
print(api.get_protocols_flows_count())
print_green('get_protocols_total_bytes()')
print(api.get_protocols_total_bytes())

print_green('apps: ')
print(api.get_apps()) 
#print('flows with the app ', apps[0], ': ', api.get_flows(apps[0]))
print_green('get_apps_flows_count()')
print(api.get_apps_flows_count())
print_green('get_apps_total_bytes()')
print(api.get_apps_total_bytes())

