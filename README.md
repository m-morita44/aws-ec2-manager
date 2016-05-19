# aws-ec2-manager

the tools is managing AWS EC2 instance by python3.

## Install

First, install the boto3 library and set a default region:

```
$ pip install boto3
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

Then, set up the script.

```
python setup.py install
```

## Usage

```
aws-ec2-manager.py <command> <instanceId>
```