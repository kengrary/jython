import os
lineSep = os.linesep

sslConfigList=AdminTask.listSSLConfigs('[-all true -displayObjectName false]')
separator=' '
ciphersList=AdminTask.listSSLCiphers('[-securityLevel HIGH]').split(lineSep)
try:
 ciphersList.remove('SSL_RSA_WITH_RC4_128_MD5')
 ciphersList.remove('SSL_RSA_WITH_RC4_128_SHA')
except:
 print "Cannot remove RC4_MD5 and RC4_SHA ciphers."
finally:
 ciphers=separator.join(ciphersList)

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
   AdminTask.modifySSLConfig('[-alias ' + sslAlias + ' -scopeName ' + manageScope + ' -sslProtocol TLS -securityLevel CUSTOM -enabledCiphers "' + ciphers + '"]')
   AdminConfig.save()
   print sslAlias + " " + manageScope + " " + sslProtocol + " to TLS and remove RC4 ciphers."
  except:
   print sslAlias + " " + manageScope + " error."
