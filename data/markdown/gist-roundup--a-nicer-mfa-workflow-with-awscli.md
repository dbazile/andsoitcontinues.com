---
date:    2018-05-20
subject: A Nicer MFA Workflow with awscli
tags:
    - awscli
    - mfa
    - python
abstract: |
    This utility tries to make the multifactor authentication (MFA) login
    workflow with awscli a little more user-friendly.
---

## Usage

In `~/.aws/credentials`, add a profile for the account you need to authenticate
into that looks like the following:

```
[someaccount]
__mfa__ = arn:aws:iam:123456789:987654321:mfa/bob
aws_access_key_id = ZZZZZ
aws_secret_access_key ZZZZZ
```

So here, `__mfa__` should be your MFA serial number, and
`aws_access_key_id` / `aws_secret_access_key` are your standard-issue access keys
that you made in the IAM.

Then from the terminal, execute:

```
$ ./aws-login.py someaccount
Enter MFA token: ••••••••
Session started; expires in 2 hours
```

This will put the session token in your default AWS credential profile so you
can use `aws` as you would normally without having to remember to put `--profile
someaccount` on _every single subsequent command_.

___Note:__ This implementation depends on [`arrow`](http://arrow.readthedocs.io/en/latest/)
for the time parsing and math, but it's not critical to the operation.  If you
don't have arrow installed you can always just comment those lines out._

## Source

<div class="codeblockname">aws-login.py</div>

```python
#!/usr/bin/env python3

import argparse
import configparser
import json
import subprocess
import os

import arrow


CREDENTIALS_FILEPATH = os.path.expanduser('~/.aws/credentials')


ap = argparse.ArgumentParser()
ap.add_argument('profile')
opts = ap.parse_args()

profile = opts.profile

credentials = configparser.ConfigParser()
credentials.read(CREDENTIALS_FILEPATH)

try:
    mfa_serial = credentials[profile]['__mfa__']
except KeyError:
    print(f"error: could not read '{profile}.__mfa__' (file={CREDENTIALS_FILEPATH})")
    exit(1)

try:
    response = subprocess.check_output([
        'aws',
        'sts',
        'get-session-token',
        '--profile',
        profile,
        '--serial-number',
        mfa_serial,
        '--token-code',
        input('\nEnter MFA token: ').strip(),
    ])
except subprocess.CalledProcessError as err:
    print('error: auth failed: {}'.format(err))
    exit(1)
except KeyboardInterrupt:
    print()
    exit(1)


try:
    parsed = json.loads(response)
except json.JSONDecodeError as err:
    print('error: could not decode auth response: {}'.format(err))
    print('---\n{}\n---'.format(response))
    exit(1)


session_start = arrow.now().to('US/Eastern')
session_expiration = arrow.get(parsed['Credentials']['Expiration']).to('US/Eastern')

credentials.remove_section('default')
credentials.add_section('default')

credentials.set('default', '__profile__', profile)
credentials.set('default', '__started__', session_start.format())
credentials.set('default', '__expires__', session_expiration.format())
credentials.set('default', 'aws_access_key_id', parsed['Credentials']['AccessKeyId'])
credentials.set('default', 'aws_secret_access_key', parsed['Credentials']['SecretAccessKey'])
credentials.set('default', 'aws_session_token', parsed['Credentials']['SessionToken'])

with open(CREDENTIALS_FILEPATH, 'w') as f:
    credentials.write(f)

print('Session started; expires {}'.format(session_expiration.humanize()))
```


## Background

I'm assuming my google-fu just wasn't strong enough to find the less clunky way
of MFA sessions than execute some arcane command and copy/paste a bunch of
tokens around files manually and then include repetitive flags on every command
because honestly, I find it hard to believe that [this is _all_ Amazon has to
say on the matter](https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/).


## A little extra something-something (added 2019-12-12)

I found myself needing snippets of the actual IAM pieces to enforce MFA in the
first place, so I'm adding this bit in case I'm on the hook for implementing it
again.

*Note: Change the contents of `Action` to whichever API permissions you need or
just use `"*"` if you want to live dangerously. 🤖*

```bash
aws iam create-policy \
    --policy-name 'CliAccess-RequireMFA' \
    --policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "cloudformation:*",
                    "ec2:*",
                    "s3:*"
                ],
                "Resource": "*",
                "Condition": {
                    "Bool": {
                        "aws:MultiFactorAuthPresent": "true"
                    }
                }
            }
        ]
    }'

aws iam create-group \
    --group-name CliAccess-RequireMFA

aws iam attach-group-policy \
    --group-name CliAccess-RequireMFA \
    --policy-arn POLICY_ARN
```

Create a new user, add them to **CliAccess-RequireMFA**, then generate an
access key.  To test that MFA is enforced, use `aws s3 ls` use that user's
access key _without_ an STS token which should give you an *Access Denied*
error.


## Comments?

Is there an out-of-the-box way to do this already?  Leave a comment on [the
gist](https://gist.github.com/dbazile/87110f80de086726f50ac2ca0e75e409) where I
was originally keeping this.
