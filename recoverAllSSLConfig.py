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
  startIndex=sslConfig.find("sslProtocol")+12
  endIndex=sslConfig.find("]",startIndex)
  sslProtocol=sslConfig[startIndex:endIndex]
  try:
   AdminTask.modifySSLConfig('[-alias ' + sslAlias + ' -scopeName ' + manageScope + ' -sslProtocol SSL_TLS -securityLevel HIGH -enabledCiphers ""]')
   AdminConfig.save()
   print sslAlias + " " + manageScope + " " + sslProtocol + " to SSL_TLS and recover RC4 ciphers."
  except:
   print "Error"