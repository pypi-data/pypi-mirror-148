##### Logs-in and extract all instances data grouped by regions #####
#it needs complete credentials on cred01.py on same folder



from itertools import count
from datetime import date
import copy
import pprint as pp
import boto3
from botocore.config import Config
from collections import defaultdict
from cred01 import *
from classes import *
from prices00 import *
#from resource00 import *


# load all regions in list regions
def available_regions(service):
    regions = []
    client = boto3.client(service)
    response = client.describe_regions()

    for item in response["Regions"]:
        #print(item["RegionName"])
        regions.append(item["RegionName"])
    return regions

# Scan all available regions 
def main():
    print("Scan all available regions")
    regions = available_regions("ec2")
    # Scan all of EC2 in each region
    cnt = 0
    my_ids=[];my_instsold=[]; insts={}

    aws_rep=copy.deepcopy(awsRepBase)     
    for region in regions:
        #get_res_data(region)
        #try:
        #print('Region:',region)
        ec2_res = boto3.resource('ec2',            
            region_name= region,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY)

        instances = ec2_res.instances.all()
        #print('Region:',region,instances)        
        aws_reg=copy.deepcopy(awsRegBase)
        aws_reg['id']= region
        region_has_inst=False      
        
        for instance in instances:
            region_has_inst=True
            print('__________________________________________')            
            #Instantiate instance
            i1=Inst()
            i1.region = region
            #Initiate Reg and Inst dictios
            #awsInst={}; awsInst.clear(); awsInst=awsInstBase
            aws_inst=copy.deepcopy(awsInstBase)          

            for tag in instance.tags:
                if 'Name'in tag['Key']:
                    ##i1.name = tag['Value']
                    aws_inst['name']=tag['Value']
                
            ##i1.id= instance.id  
            aws_inst['id']= instance.id            

            #print(i1.id,i1.name,'VPC:', instance.vpc )
            #i1.vpc=instance.vpc #not clean output
            
            ##i1.status= instance.state['Name']
            aws_inst['status']= instance.state['Name'] 
            ##i1.birthday= instance.launch_time            
            aws_inst['birthday']=str(instance.launch_time)             
            ##i1.ipv4priv= instance.private_ip_address
            aws_inst['ipv4priv']=instance.private_ip_address            
            ##i1.ipv4pub= instance.public_ip_address  
            aws_inst['ipv4pub']= instance.public_ip_address        
            ##i1.type = instance.instance_type
            aws_inst['type']= instance.instance_type

            #i1.cpus= instance.cpu_options.core_count
            i1.cpus= instance.cpu_options.get(u'CoreCount','1')
            aws_inst['cpus']=instance.cpu_options.get(u'CoreCount','1')
            i1.image= instance.image_id
            aws_inst['image']=instance.image_id           
            
            i1.os= 'Linux' if 'Linux' in instance.platform_details else 'Windows'
            aws_inst['os']='Linux' if 'Linux' in instance.platform_details else 'Windows'
            
            # Get Name, Memory, avzone, vps (need client)
            ec2_cli = boto3.client('ec2',    
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY,
                region_name= region)              

            #r_inst = ec2_cli.describe_instances(InstanceIds=[i1.id])["Reservations"][0]
            r_inst = ec2_cli.describe_instances(InstanceIds=[aws_inst['id']])["Reservations"][0]

            #r_inst=response["Reservations"][0]
            ##i1.avzone = r_inst["Instances"][0]["Placement"]["AvailabilityZone"] 
            aws_inst['avzone']=r_inst["Instances"][0]["Placement"]["AvailabilityZone"]
            ##i1.vpc_id = r_inst["Instances"][0]["VpcId"]
            aws_inst['vpc_id']=r_inst["Instances"][0]["VpcId"]

            #pp.pprint(r_inst["Instances"][0]["Placement"]["AvailabilityZone"])
            #pp.pprint(r_inst["Instances"])

            #Get memory size from _types
            #r_typ =ec2_cli.describe_instance_types(InstanceTypes=[i1.type])
            r_typ =ec2_cli.describe_instance_types(InstanceTypes=[aws_inst['type']])
            
            ##i1.memory= r_typ["InstanceTypes"][0]["MemoryInfo"]["SizeInMiB"]
            aws_inst['memory']=r_typ["InstanceTypes"][0]["MemoryInfo"]["SizeInMiB"]

            #i1.server= r_typ["ResponseMetadata"]["HTTPHeaders"]["server"]

            #Get nominal hourly price from AWS Pricing (call prices)
            ##region_code = i1.region
            ##instance_type = i1.type
            ##operating_system = i1.os
            region_code = aws_reg['id']
            instance_type = aws_inst['type']
            operating_system = aws_inst['os']

            ##i1.priceh = get_ec2_instance_hourly_price(
            ##    region_code=region_code, 
            ##    instance_type=instance_type, 
            ##    operating_system=operating_system,
            ##)


            aws_inst['ihprice']=get_ec2_instance_hourly_price(
                region_code=region_code, 
                instance_type=instance_type, 
                operating_system=operating_system,
            )



            #i1.pricem='disabled for not to charge costs'            
            ce_enable=False
            if ce_enable:
                #Get Monthly price (need cost explorer client)
                #(I have to modify this part in order to have automatic time period from date)
                ce_cli = boto3.client('ce',
                    aws_access_key_id=AWS_ACCESS_KEY,
                    aws_secret_access_key=AWS_SECRET_KEY,
                    region_name= region)

                period_start=str(date.today().replace(day=1))
                period_end=str(date.today())

                response = ce_cli.get_cost_and_usage(
                    TimePeriod={
                        'Start': period_start,
                        'End': period_end

                        #'Start': '2022-04-01',
                        #'End': '2022-04-10'
                    },
                    Metrics=['UnblendedCost'],
                    Granularity='MONTHLY',
                )
                #awsInst['imprice']=response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
                aws_rep['totalmprice']=response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
                i1.pricem=(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
                i1.priceu=(response['ResultsByTime'][0]['Total']['UnblendedCost']['Unit'])
                

            #Store the instance id and data in lists 
            #my_ids.append(i1.id); my_instsold.append(i1)
            my_ids.append(aws_inst['id'])
            aws_reg['inst'].append(aws_inst)
            
        ### After scanning each region
        if region_has_inst:
            aws_rep['regions'].append(aws_reg)


    pp.pprint(aws_rep)
    print('__________________________________________')
    if len(my_ids) == 1:
        print(f"You have {len(my_ids)} instance here M.J!",'\n')
    elif len(my_ids) > 1:
        print(f"You have {len(my_ids)} instances here M.J.!",'\n')
    else:
        print(f"You have no instances here M.J.!",'\n')    
    

    #Generate report json file
    aws_json = json.dumps(aws_rep,indent=2)
    with open('report01.json', 'w') as outfile:
        outfile.write(aws_json)


# call function
if __name__ == "__main__":
    main()