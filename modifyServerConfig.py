######################################################################
# ScriptName modfiyServerConfig                                      #
# Usage      Modify all target server configuattion.                 #
# Create     2015-4-30                                               #
# Modify     2015-4-30                                               #
# Version    1.0                                                     #
#                                                                    #
######################################################################
import os
lineSep = os.linesep

targetServerList=['server1','server2']
initHeapSize='1024'
maxHeapSize='2048'
jvmGCPolicyArgs=' -Xgcpolicy:gencon'
jvmGCLogArgs=' -Xverbosegclog:${SERVER_LOG_ROOT}/native_stderr.log,10,10000'
envPath='/wasdump/heapdump'
rolloverType='SIZE'
rolloverSize='20'
maxNumberOfBackupFiles='10'
webContainerMax='100'
webContainerMin='20'


def configEnvironment(serverName):
 serverID=AdminConfig.getid('/Server:'+serverName)
 javaProcDef = AdminConfig.list('JavaProcessDef',serverID)
 javacorePath=envPath+'/'+serverName
 heapdumpPath=envPath+'/'+serverName
 coredumpPath=envPath+'/'+serverName
 varName=['name','IBM_JAVACOREDIR']
 varValue=['value',javacorePath]
 env=[varName,varValue]
 AdminConfig.create('Property',javaProcDef,env)
 varName=['name','IBM_HEAPDUMPDIR']
 varValue=['value',heapdumpPath]
 env=[varName,varValue]
 AdminConfig.create('Property',javaProcDef,env)
 varName=['name','IBM_COREDIR']
 varValue=['value',coredumpPath]
 env=[varName,varValue]
 AdminConfig.create('Property',javaProcDef,env)
 AdminConfig.save()
 print "configEnvironment finished."
#enddef

def configJVMSetting(serverName):
 AdminTask.setJVMInitialHeapSize('[-serverName ' + serverName + ' -initialHeapSize ' + initHeapSize + ']')
 AdminTask.setJVMMaxHeapSize('[-serverName ' + serverName + ' -maximumHeapSize ' + maxHeapSize + ']')
 serverID=AdminConfig.getid('/Server:'+serverName)
 jvm=AdminConfig.list('JavaVirtualMachine',serverID)
 jvmGenericArgs=AdminConfig.showAttribute(JVM,'genericJvmArguments')
 if(jvmGenericArgs.find('Xgcpolicy')<0):
  if(jvmGenericArgs.find('Xverbosegclog')<0):
   jvmNewArgs=jvmGenericArgs + jvmGCPolicyArgs + jvmGCLogArgs
  else:
   jvmNewArgs=jvmGenericArgs + jvmGCPolicyArgs
 else:
  if(jvmGenericArgs.find('Xverbosegclog')<0):
   jvmNewArgs=jvmGenericArgs + jvmGCLogArgs
  else:
   jvmNewArgs=jvmGenericArgs
 jvmAttribue=[['genericJvmArguments', jvmNewArgs],['verboseModeGarbageCollection','true']]
 AdminConfig.modify(jvm,jvmAttribue)
 AdminConfig.save()
 print "configJVMSetting finished."
#enddef

def configSystemLog(serverName):
 serverID=AdminConfig.getid('/Server:'+serverName)
 systemOut=AdminConfig.showAttribute(serverID,'outputStreamRedirect')
 systemErr=AdminConfig.showAttribute(serverID,'errorStreamRedirect')
 systemOutAttr=[['rolloverType',rolloverType],['maxNumberOfBackupFiles',maxNumberOfBackupFiles],['rolloverSize',rolloverSize]]
 systemErrAttr=[['rolloverType',rolloverType],['maxNumberOfBackupFiles',maxNumberOfBackupFiles],['rolloverSize',rolloverSize]]
 AdminConfig.modify(systemOut,systemOutAttr)
 AdminConfig.modify(systemErr,systemErrAttr)
 AdminConfig.save()
 print "configSystemLog finished."
#enddef

def configWebContainer(serverName):
 serverID=AdminConfig.getid('/Server:'+serverName)
 threadPoolList=AdminConfig.list('ThreadPool',serverID).split(lineSep)
 for threadPool in threadPoolList:
  if(threadPool.find('WebContainer')>=0):
   webContainer=threadPool
 if(webContainer!=''):
  webContainerAttr=[['maximumSize',webContainerMax],['minimumSize',webContainerMin]]
  AdminConfig.modify(webContainer,webContainerAttr)
  AdminConfig.save()
  print "configWebContainer finished."
#enddef


for serverName in targetServerList:
 print serverName
 configJVMSetting(serverName)
 configEnvironment(serverName)
 configSystemLog(serverName)
 configWebContainer(serverName)