cellName = AdminControl.getCell()
nodes=AdminTask.listNodes().split('\n')
for node in nodes:
 if(node.find('WEB')<0):
  Sync1 = AdminControl.completeObjectName('type=NodeSync,process=nodeagent,node='+node+',*')
  try:
   print AdminControl.invoke(Sync1, 'sync')
   print node+" sync ok."
  except:
   print node+" sync error, maybe is DMGR."