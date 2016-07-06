import os

lineSep = os.linesep

sslConfigList = AdminTask.listSSLConfigs('[-all true -displayObjectName false]')
separator = ' '
ciphersList = AdminTask.listSSLCiphers('[-securityLevel HIGH]').split(lineSep)
cipher = ""
removeCipherList= ['RC4_128_MD5','RC4_128_SHA','DH','DHE']
customCipherList = []

try:
    for cipher in ciphersList:
        for removeCipher in removeCipherList:
            if cipher.find(removeCipher) < 0:
                customCipherList.append(cipher)
                print "Reserve cipher %s." %cipher
            else:
                print "Remove cipher %s." %cipher
except:
    print "Cannot remove unsafe ciphers."

ciphers = separator.join(customCipherList)

for sslConfigName in sslConfigList.split(lineSep):
    if (sslConfigName.find("SSLSettings") >= 0):
        astartIndex = sslConfigName.find("alias")
        mstartIndex = sslConfigName.find("managementScope")
        sslAlias = sslConfigName[astartIndex + 7:mstartIndex - 1]
        manageScope = sslConfigName[mstartIndex + 17:-1]
        sslConfig = AdminTask.getSSLConfig('[-alias ' + sslAlias + ' -scopeName ' + manageScope + ']')
        startIndex = sslConfig.find("sslProtocol") + 12
        endIndex = sslConfig.find("]", startIndex)
        sslProtocol = sslConfig[startIndex:endIndex]
        try:
            AdminTask.modifySSLConfig(
                '[-alias ' + sslAlias + ' -scopeName ' + manageScope + ' -sslProtocol TLS -securityLevel CUSTOM -enabledCiphers "' + ciphers + '"]')
            AdminConfig.save()
            print sslAlias + " " + manageScope + " " + sslProtocol + " to TLS and remove RC4 ciphers."
        except:
            print sslAlias + " " + manageScope + " error."
