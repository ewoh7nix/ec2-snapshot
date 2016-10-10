#!/usr/bin/python
# @author: Nasrullah <ewoh7nix@gmail.com>
# @version: 0.1
# @description:
#   Create a backup snapshot from every volumes attached to running instances
#   and delete the old one if age > 2 weeks.

import boto3
import datetime

ec2 = boto3.resource('ec2')

def create_snapshot():
    for instance in ec2.instances.all():
        # Create snapshot from running instances only
        if instance.state['Name'] != 'running':
            continue
        # Create snapshot from every volumes attached to instances
        for device in instance.block_device_mappings:
            volume_id = device['Ebs']['VolumeId']
            device_name = device['DeviceName']
            snapshot_desc = 'EBS Snapshot from Volume ' + volume_id + ', instance ' + instance.id
            snapshot_tags = [{'Key': 'Name', 'Value': snapshot_desc}]

            print 'Creating snapshot from', volume_id, '(',instance.id,')'
            snapshot = ec2.create_snapshot(VolumeId=volume_id, Description=snapshot_desc)
            snapshot.create_tags(Tags=snapshot_tags)
def delete_snapshot():
    today = datetime.date.today()
    for snapshot in ec2.snapshots.filter(Filters=[{ 'Name': 'description', 'Values': ['EBS*'] }]):
        age = today - snapshot.start_time.date()
        # Skip if snapshot age less than 2 weeks
        if age <= datetime.timedelta(days=14):
            continue
        print 'Deleting snapshot', snapshot.snapshot_id
        snapshot.delete()

if __name__ == '__main__':
    create_snapshot()
    delete_snapshot()
