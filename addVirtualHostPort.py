######################################################################
# ScriptName addVirtualHostPort                                      #
# Usage      Add webserver port to virtualhost.                      #
# Create     2015-5-5                                                #
# Modify     2015-5-5                                                #
# Version    1.0                                                     #
#                                                                    #
######################################################################

import os
lineSep = os.linesep

portList=[]
cellName = AdminControl.getCell()
nodes=AdminTask.listNodes().split(lineSep)
for node in nodes:
 if(node.find('WEB')>=0):
  print node
  webId=AdminConfig.getid('/Cell:'+cellName+'/Node:'+node+'/')
  webs=AdminConfig.list('NamedEndPoint',webId).split(lineSep)
  for web in webs:
   oldPort=AdminConfig.showAttribute(AdminConfig.showAttribute(web,'endPoint'),'port')
   if(len(oldPort)<=3):
    if(len(oldPort)==2):
     newPort="10"+oldPort
    if(len(oldPort)==3):
     newPort="1"+oldPort
    if(portList.count(newPort)==0):
     portList.append(newPort)
    try:
     AdminConfig.modify(AdminConfig.showAttribute(web,'endPoint'),'[[port \"' + newPort + '\"]]')
     print oldPort +" modify to "+ newPort + " ok."
    except:
     print oldPort +" modify to "+ newPort + " failed."

for port in portList:
 try:
  AdminConfig.create('HostAlias',AdminConfig.getid('/Cell:'+cellName+'/VirtualHost:default_host/'),'[[hostname \"*\"][port \"'+port+'\"]]')
  print port + " has added to VirtaulHost."
 except:
  print port + " add to VirtualHost error."

print "Save the config." 
AdminConfig.save()


