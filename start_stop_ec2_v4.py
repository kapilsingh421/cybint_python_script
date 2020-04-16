import sys
import os
import time
import argparse
import boto3.ec2
from botocore.exceptions import ClientError

VERSION = '1.5.0'
ec2 = boto3.client('ec2')
#client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
instance_id = 'i-0f6927a0eb7486107'


class Mem:
    """
    Global Class Pattern:
    Declare globals here.
    """
    instance_id = "i-0f6927a0eb7486107"


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
        instances = ec2_resource.create_instances(ImageId='ami-07ebfd5b3428b6f4d', MinCount=1, MaxCount=1, InstanceType = 't2.micro', KeyName = 'myvpc_api',                                  SubnetId = 'subnet-5c02b83b')         
        print("Success", "INSTANCE LAUNCHED", instances)
        instance = instances[0]
        instance.wait_until_running()
        instance.load()
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
        response = ec2.start_instances(InstanceIds=[Mem.instance_id], DryRun=False)
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
        print("Success","Terminate",response)
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


def main():
    """
    The entry point of this program.
    """
    args = parse_arguments()
    sys.stdout.write(str(evaluate(args)))
    print()


if __name__ == '__main__':
    main()
