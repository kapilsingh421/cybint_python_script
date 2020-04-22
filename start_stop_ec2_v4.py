import sys
import os
import time
import argparse
import boto3.ec2
import rsa,boto, base64
from botocore.exceptions import ClientError

VERSION = '1.5.0'
ec2 = boto3.client('ec2')
#client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
#echo -e "linuxpassword\nlinuxpassword" | passwd ubuntu'''
user_data = '''#!/bin/bash
echo -e "linuxpassword\nlinuxpassword" | passwd ubuntu'''
instance_id = 'i-0acc3acb246c19354'
tags = [
        {'Key':'Name','Value': 'cybint'},
        {'Key':'Env', 'Value': 'staging'},
       ]
tag_specification = [{'ResourceType': 'instance', 'Tags': tags},]

class Mem:
    """
    Global Class Pattern:
    Declare globals here.
    """
    instance_id = "i-0f6927a0eb7486107"
    ami_id= "ami-088dc85c8883d4298"


def parse_arguments():
    """
    The options the user can choose (up, down, version)
    :return: The chosen option.
    """
    parser = argparse.ArgumentParser("start_stop_ec2.py: \
    Start and stop your EC2 instance.\n")
    parser.add_argument(
        '-u', '--up', help="Start the EC2 instance", action='store_true')
    parser.add_argument('-d', '--down',
                        help="Stop the EC2 instance", action='store_true')
    parser.add_argument(
           '-r', '--run' , help ="Launch the Ec2 instance", action='store_true')
    parser.add_argument(
           '-t', '--terminate' , help ="Terminate the Ec2 instance", action='store_true')
    parser.add_argument(
           '-p', '--password' , help ="password of the Ec2 windows instance", action='store_true')
    parser.add_argument(
           '-a', '--ami' , help ="Decsribe the  Ami", action='store_true')
    parser.add_argument(
        '-v', '--version', help="Display the current version", action='store_true')
    args = parser.parse_args()
    return args


def evaluate(args):
    """
    Evaluate the given arguments.
    :param args: The user's input.
    """
    if args.run:
        create_instances()
    elif args.up:
        start_ec2()
    elif args.down:
        stop_ec2()
    elif args.terminate:
         terminate_ec2()
    elif args.ami:
         get_image()
    elif args.password:
         get_password()     
    elif args.version:
        print()
        print('This is version {0}.'.format(VERSION))
    else:
        print("Missing argument! Type '-h' for available arguments.")

def create_instances():
    """
    This code is from Amazon's EC2 example.
    Do a dryrun first to verify permissions.
    Try to start the EC2 instance.
    """
    print("------------------------------")
    print("Try to Launch the EC2 instance.")
    print("------------------------------")

    # Dry run succeeded, run start_instances without dryrun
    try:
        print("Launch instance ...")
        instances = ec2_resource.create_instances(ImageId='ami-0473608a4fdd2ce7a', MinCount=1, MaxCount=1, InstanceType = 't2.micro', KeyName = 'cybint_staging',                                     SubnetId = 'subnet-0c6d065ada4820c5f' ,TagSpecifications=tag_specification ,UserData=user_data)     
        print("Success", "INSTANCE LAUNCHED", instances)
        instance = instances[0]
        while instance.state['Name'] not in ('running','stopped'):
            time.sleep(2)
            state = instance.state
            instance.load()
            print ("state:", state)
        for instance in instances:
            for tag in instance.tags:
               if tag['Key'] == 'Name':
                   print (tag['Value'])
        print(instance.id)
        print(instance.public_ip_address)      
    except ClientError as e:
        print(e)


def start_ec2():
    """
    This code is from Amazon's EC2 example.
    Do a dryrun first to verify permissions.
    Try to start the EC2 instance.
    """
    print("------------------------------")
    print("Try to start the EC2 instance.")
    print("------------------------------")

    try:
        print("Start dry run...")
        ec2.start_instances(InstanceIds=[Mem.instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        print("Start instance without dry run...")
        instances = ec2.start_instances(InstanceIds=[Mem.instance_id], DryRun=False)
        instance = instances[0]
        print("Success","Started",response)
        fetch_public_ip()
    except ClientError as e:
        print(e)


def stop_ec2():
    """
    This code is from Amazon's EC2 example.
    Do a dryrun first to verify permissions.
    Try to stop the EC2 instance.
    """
    print("------------------------------")
    print("Try to stop the EC2 instance.")
    print("------------------------------")

    try:
        ec2.stop_instances(InstanceIds=[Mem.instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[Mem.instance_id], DryRun=False)
        print("Success","Stopped",response)
    except ClientError as e:
        print(e)


def terminate_ec2():
    """
    This code is from Amazon's EC2 example.
    Do a dryrun first to verify permissions.
    Try to Terminate the EC2 instance.
    """
    print("------------------------------")
    print("Try to Terminate the EC2 instance.")
    print("------------------------------")

    try:
        ec2.terminate_instances(InstanceIds=[Mem.instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call terminate_instances without dryrun
    try:
        response = ec2.terminate_instances(InstanceIds=[Mem.instance_id], DryRun=False)
        print("Success","Terminate")
    except ClientError as e:
        print(e)


def get_image():
    """
    This code is from Amazon's EC2 Boto3
    Do a dryrun first to verify permissions.
    Try to Describe  the EC2 AMI.
    """
    print("------------------------------")
    print("Try to Describe the EC2 Image.")
    print("------------------------------")

    try:
        ec2.describe_images(ImageIds=[Mem.ami_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call Describes_Ami without dryrun
    try:
        image = ec2.describe_images(ImageIds=[Mem.ami_id], DryRun=False)
        print("API Success")
        print(image)
    except ClientError as e:
        print(e)


def fetch_public_ip():
    """
    Fetch the public IP that has been assigned to the EC2 instance.
    :return: Print the public IP to the console.
    """
     
    """
    Fetch the public IP that has been assigned to the EC2 instance.
    :return: Print the public IP to the console.
    """
    print()
    print("Waiting for public IPv4 address...")
    print()
    time.sleep(16)
    response = ec2.describe_instances(InstanceIds=[instance_id])
    first_array = response["Reservations"]
    first_index = first_array[0]
    instances_dict = first_index["Instances"]
    instances_array = instances_dict[0]
    ip_address = instances_array["PublicIpAddress"]
    print()
    print("Public IPv4 address of the EC2 instance: {0}".format(ip_address)) 

    
   # print ("instance.ip_address")
   # print("Public IPv4 address of the EC2 instance: {0}".format(ip_address))

def get_password():
    """
    This code is from Amazon's EC2 Boto
    Do a dryrun first to verify permissions.
    Try  to fetch the windows data and password.
    """ 
    key_path = '/Users/kapil/Downloads/cybint_staging.pem'
    ec2_pass = boto.connect_ec2() #access_key,secret_key
    passwd = base64.b64decode(ec2_pass.get_password_data(instance_id))
    if (passwd):
        with open (key_path,'r') as privkeyfile:
            priv = rsa.PrivateKey.load_pkcs1(privkeyfile.read())
        key = rsa.decrypt(passwd,priv)
    else:
        key = 'Wait at least 4 minutes after creation before the admin password is available'
 
    print(key)


def main():
    """
    The entry point of this program.
    """
    args = parse_arguments()
    sys.stdout.write(str(evaluate(args)))
    print()


if __name__ == '__main__':
    main()
