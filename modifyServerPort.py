######################################################################
# ScriptName modfiyServerConfig                                      #
# Usage      Modify target server port.                              #
# Create     2015-4-30                                               #
# Modify     2015-5-5                                                #
# Version    1.0                                                     #
#                                                                    #
######################################################################
import os
lineSep = os.linesep

serverList=['server1','server2']
for serverName in serverList:
 ports=AdminTask.listServerPorts(serverName).split(lineSep)
 for port in ports:
  hostSIdx=port.find('[host ')
  hostEIdx=port.find(']',hostSIdx)
  nodeSIdx=port.find('[node ')
  nodeEIdx=port.find(']',nodeSIdx)
  serverSIdx=port.find('[server ')
  serverEIdx=port.find(']',serverSIdx)
  portSIdx=port.find('[port ')
  portEIdx=port.find(']',portSIdx)
  endPointName=port[2:hostSIdx-3]
  hostName=port[hostSIdx+6:hostEIdx]
  nodeName=port[nodeSIdx+6:nodeEIdx]
  serverName=port[serverSIdx+8:serverEIdx]
  oldPort=port[portSIdx+6:portEIdx]
  if(len(oldPort)==4):
   newPort="1"+oldPort
  if(len(oldPort)==3):
   newPort="10"+oldPort    
  AdminTask.modifyServerPort(''+serverName+'', '[-nodeName '+nodeName+' -endPointName '+endPointName+' -host '+hostName+' -port '+newPort+' -modifyShared true]')
  print oldPort +" modify to "+ newPort + " ok."
       
print "Save the config." 
 
AdminConfig.save()


       