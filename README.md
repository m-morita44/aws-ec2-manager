# aws-ec2-manager

the tools is managing AWS EC2 instance by python3.

## Install

First, install the aws-ec2-manager library:

```
$ pip install git+https://github.com/mmorita44/aws-ec2-manager.git@master#egg=aws-ec2-manager
```

Next, set up credentials (in e.g. `~/.aws/credentials`):

```
[default]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YOUR_SECRET
```

Then, set up a default region (in e.g. `~/.aws/config`):

```
[default]
region = us-east-1
```

## Usage

```
aws-ec2-manager <command> <instanceId>
```
