# // Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# // SPDX-License-Identifier: Apache-2.0
import json
import boto3
import botocore
import argparse

def delete_iam_policy_and_role(iam_role_arn):
    role_name = iam_role_arn.split('/')[-1]
    iam = boto3.client('iam')
    try:
        response = iam.list_role_policies(RoleName=role_name)
    except botocore.exceptions.ClientError as e:
        print(e)
        return
    for policy in response.get('PolicyNames',[]):
        print(f"Deleting policy {policy}")
        try:
            resp = iam.delete_role_policy(RoleName=role_name, PolicyName=policy)
        except botocore.exceptions.ClientError as e:
            print(e)
            continue
    print(f"Deleting role {role_name}")
    try:
        resp = iam.delete_role(RoleName=role_name)
    except botocore.exceptions.ClientError as e:
        print(e)
    return

def create_iam_role(iam_policy_file, role_name):
    role_arn = ""
    lambda_trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
    iam = boto3.client('iam')
    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(lambda_trust_policy)
        )
    except botocore.exceptions.ClientError as e:
        print(e)
        return role_arn
    with open(iam_policy_file) as f:
        iam_policy = json.load(f)
        for policy_name, value in iam_policy.items():
            print(f"Creating policy {policy_name}")
            try:
                resp = iam.put_role_policy(
                    RoleName=role_name,
                    PolicyName=policy_name,
                    PolicyDocument=json.dumps(value)
                )
            except botocore.exceptions.ClientError as e:
                print(e)
                continue
    role_arn = response.get('Role',{}).get('Arn',"")
    print(f"Created role {role_arn}")
    return role_arn

# create the main function and call create or delete based on arguments
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--iam_policy_file', required=True)
    parser.add_argument('--role_name', required=True)
    parser.add_argument('--delete', action='store_true')
    args = parser.parse_args()
    if args.delete:
        delete_iam_policy_and_role(args.role_name)
    else:
        create_iam_role(args.iam_policy_file, args.role_name)

if __name__ == "__main__":
    main()
