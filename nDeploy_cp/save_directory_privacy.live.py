#!/usr/bin/python
import os
import socket
import yaml
import cgi
import cgitb
import re
import sys


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()


close_cpanel_liveapisock()
form = cgi.FieldStorage()


print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>XtendWeb</title>')
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<a href="xtendweb.live.py"><img border="0" src="xtendweb.png" alt="nDeploy"></a>')
print('<HR>')
if form.getvalue('domain') and form.getvalue('action') and form.getvalue('protectedurl'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    action = form.getvalue('action')
    protectedurl = form.getvalue('protectedurl')
    if not protectedurl.startswith('/'):
        protectedurl = '/'+protectedurl
    if protectedurl != '/' and protectedurl.endswith('/'):
        protectedurl = protectedurl[:-1]
    if not re.match("^[a-zA-Z/_-]*$", protectedurl):
        print("Error: Invalid char in sub-directory name")
        sys.exit(0)
    profileyaml = installation_path + "/domain-data/" + mydomain
    if os.path.isfile(profileyaml):
        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        protected_dir_list = yaml_parsed_profileyaml.get('protected_dir')
        if action == 'add':
            if protectedurl not in protected_dir_list:
                protected_dir_list.append(protectedurl)
        elif action == 'del':
            if protectedurl in protected_dir_list:
                protected_dir_list.remove(protectedurl)
        yaml_parsed_profileyaml['protected_dir'] = protected_dir_list
        print(('<p style="background-color:LightGrey">CONFIGURING PASSWORD PROTECTED URL FOR:  '+mydomain+'</p>'))
        print('<HR>')
        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
        print('<div class="boxedyellow">')
        print('password protected URL list modified for '+mydomain)
        print('</div>')
        print('</form>')
    else:
        print('ERROR : domain-data file i/o error')
else:
    print('ERROR : Forbidden')
print('</body>')
print('</html>')
