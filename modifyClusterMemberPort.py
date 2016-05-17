######################################################################
# ScriptName modfiyClusterMemberConfig                               #
# Usage      Modify all Cluster member port configuattion.           #
# Create     2015-4-30                                               #
# Modify     2015-4-30                                               #
# Version    1.0                                                     #
#                                                                    #
######################################################################

import os
lineSep = os.linesep

targetCluster='LT_CBS_CLUSTER'


cellName = AdminControl.getCell()
clusterIDList=AdminConfig.list('ServerCluster', AdminConfig.getid( '/Cell:'+cellName+'/')).split(lineSep)
for clusterID in clusterIDList:
 clusterName=AdminConfig.showAttribute(clusterID,'name')
 print clusterName
 if(clusterName == targetCluster):
 clusterMemberIDList=AdminConfig.list('ClusterMember', AdminConfig.getid( '/Cell:'+cellName+'/ServerCluster:'+clusterName+'/')).split(lineSep)
 for clusterMemberID in clusterMemberIDList:
  servers=AdminConfig.showAttribute(clusterMemberID,'memberName')
  ports=AdminTask.listServerPorts(''+servers+'').split(lineSep)
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






 
 


 

 
 