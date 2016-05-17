import os
lineSep = os.linesep

initHeapSize='1024'
maxHeapSize='2048'

def configJVMSetting(serverName):
 serverID=AdminConfig.getid('/Server:'+serverName)
 JVM=AdminConfig.list('JavaVirtualMachine',serverID)
 jvmMaxHeapSize=AdminConfig.showAttribute(JVM,'maximumHeapSize')
 jvmInitHeapSize=AdminConfig.showAttribute(JVM,'initialHeapSize')
 AdminTask.setJVMInitialHeapSize('[-serverName ' + serverName + ' -initialHeapSize ' + initHeapSize + ']')
 AdminTask.setJVMMaxHeapSize('[-serverName ' + serverName + ' -maximumHeapSize ' + maxHeapSize + ']')
 print jvmInitHeapSize + " modified to " + initHeapSize
 print jvmMaxHeapSize  + " modified to " + maxHeapSize
 AdminConfig.save()
#enddef

cellName = AdminControl.getCell()

serverList=[]
nodeIDList=AdminConfig.list('Node').split(lineSep)
nodeNameList=AdminTask.listNodes().split(lineSep)

for nodeID in nodeIDList:
 nodeName=AdminConfig.showAttribute(nodeID,'name')
 serverEntryList=AdminConfig.list('ServerEntry',nodeID).split(lineSep)
 for serverEntry in serverEntryList:
  serverType=AdminConfig.showAttribute(serverEntry,'serverType')
  serverName=AdminConfig.showAttribute(serverEntry,'serverName')
  if(serverType == 'APPLICATION_SERVER'):
   serverList.append(serverName)

for serverName in serverList:
 print serverName
 configJVMSetting(serverName)