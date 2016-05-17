import os
lineSep = os.linesep
sslConfigList=AdminTask.listSSLConfigs('[-all true -displayObjectName false]')
for sslConfigName in sslConfigList.split(lineSep):
 if(sslConfigName.find("SSLSettings")>=0):
  astartIndex=sslConfigName.find("alias")
  mstartIndex=sslConfigName.find("managementScope")  
  sslAlias=sslConfigName[astartIndex+7:mstartIndex-1]
  manageScope=sslConfigName[mstartIndex+17:-1]
  sslConfig=AdminTask.getSSLConfig('[-alias '+ sslAlias +' -scopeName '+ manageScope +']')
  print sslConfig