###################################################
# ScriptName serverInfo.py                        #
# Usage      Show all server configuation         #
# Create     2015-4-30                            #
# Modify     2016-4-28                            #
# Version    1. 1                                 #
# Modify History                                  #
# 1.1 Add rolloverType for SystemOut,SystemErr    #
###################################################

import os
lineSep = os.linesep

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

for server in serverList:
 print server
 try:
  serverID=AdminConfig.getid('/Server:'+server)
  threadPoolList=AdminConfig.list('ThreadPool',serverID).split(lineSep)
  for threadPool in threadPoolList:
   if(threadPool.find('WebContainer')>=0):
    webContainer=threadPool
    webContainerMax = AdminConfig.showAttribute(webContainer,'maximumSize')
    webContainerMin = AdminConfig.showAttribute(webContainer,'minimumSize')
  print 'webContainerMin ' + webContainerMin
  print 'webContainerMax ' + webContainerMax
  systemErr                 = AdminConfig.showAttribute(serverID,'errorStreamRedirect')
  systemOut                 = AdminConfig.showAttribute(serverID,'outputStreamRedirect')
  errMaxNumberOfBackupFiles = AdminConfig.showAttribute(systemErr,'maxNumberOfBackupFiles')
  errRolloverType           = AdminConfig.showAttribute(systemErr,'rolloverType')
  errRolloverSize           = AdminConfig.showAttribute(systemErr,'rolloverSize')
  outMaxNumberOfBackupFiles = AdminConfig.showAttribute(systemOut,'maxNumberOfBackupFiles')
  outRolloverType           = AdminConfig.showAttribute(systemOut,'rolloverType')
  outRolloverSize           = AdminConfig.showAttribute(systemOut,'rolloverSize')
  print 'SystemErr Files ' + errMaxNumberOfBackupFiles + ' rolloverType ' + errRolloverType + ' rolloverSize ' + errRolloverSize
  print 'SystemOut Files ' + outMaxNumberOfBackupFiles + ' rolloverType ' + outRolloverType + ' rolloverSize ' + outRolloverSize
  javaProcDef = AdminConfig.list('JavaProcessDef',serverID)
  envs=AdminConfig.showAttribute(javaProcDef,'environment').replace('[','')
  envs=envs.replace(']','')
  if(envs != ''):
   for env in envs.split(' '):
    print AdminConfig.showAttribute(env,'name') + " " + AdminConfig.showAttribute(env,'value')
  JVM=AdminConfig.list('JavaVirtualMachine',serverID)
  jvmMaxHeapSize=AdminConfig.showAttribute(JVM,'maximumHeapSize')
  jvmInitHeapSize=AdminConfig.showAttribute(JVM,'initialHeapSize')
  jvmVerboseGC=AdminConfig.showAttribute(JVM,'verboseModeGarbageCollection')
  jvmGenericArgs=AdminConfig.showAttribute(JVM,'genericJvmArguments')
  print 'MaxHeapSize ' + jvmMaxHeapSize
  print 'InitHeapSize ' + jvmInitHeapSize
  print 'VerboseGC ' + jvmVerboseGC
  print 'JVMGenericArgs ' + jvmGenericArgs
 except:
  e = str(sys.exc_info()[1])
  print 'Error : %s' %(e)
