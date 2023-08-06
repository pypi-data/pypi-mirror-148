#from classes import *
import pprint as pp
import json
import copy


#Dictionary Structure
awsRegBase={
    'id':       '',
    'inst':     [],
    'rmprice':  '',
    'rhprice':  '',
    }


awsInstBase={
        'id'  :     '',
        'name':     '',
        'status':   '',
        'avzone':   '',
        'status':   '',
        'birthday': '',
        'type':     '',
        'ipv4priv': '',
        'ipv4pub':  '',
        'cpus':     '',
        'os':       '',
        'memory':   '',
        'image':    '',
        'vpc_id':   '',
        'priceh':   '',
        'imprice':  '',
        'ihprice':  '',
        
    }

pp.pprint(awsRegBase)
print('XXXX')
#pp.pprint(awsInstBase)





#awsReg=awsRegBase.deepcopy()
#awsInst=awsInstBase.deepcopy()

awsReg=copy.deepcopy(awsRegBase)
awsInst=copy.deepcopy(awsInstBase)



awsReg['id']='cuchuflito'
pp.pprint(awsRegBase)
pp.pprint(awsReg)

#pp.pprint(awsInst)


###
awsInst["id"]="x-12345"; awsInst['name']= 'MJ-01'
pp.pprint(awsInstBase)
#awsReg['inst'].append(awsInst)
print('XXXXXXXXXXXXXXXXXX')
#pp.pprint(awsRegBase)

print('XXXXXXXXXXXXXXXXXX')
"""
###
awsInst['id']='x-23456'; awsInst['name']= 'MJ-02'
awsRug['inst'].append(awsInst)

awsRug={}; awsRug.clear() 
pp.pprint(awsRug)
awsRug=awsRegBase
pp.pprint(awsRegBase)


###
awsInst['id']='x-34567'; awsInst['name']= 'MJ-03'
awsRug['inst'].append(awsInst)




#XXXXXXX
"""

"""
awsReg['id']='us-east-2'
awsReg['rhprice']= '0.02'
awsReg['rmprice']= '0.2'



#pp.pprint(awsReg)
#pp.pprint(awsInst)

print('XXXXXXXXXXXXXXXXXXXXX')

aws_json = json.dumps(awsReg,indent=2)
#pp.pprint(aws_json)
#print(aws_json)

# Directly from dictionary
#with open('pru01.json', 'w') as outfile:
#    json.dump(aws_json, outfile)

# Using a JSON string
with open('pru01.json', 'w') as outfile:
    outfile.write(aws_json)

"""



