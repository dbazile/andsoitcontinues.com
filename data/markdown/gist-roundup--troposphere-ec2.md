---
date:    2018-05-19
subject: Bootstrapping EC2 instances with user-data "resource bundles"
tags:
    - ec2
    - python
    - script
    - troposphere
abstract: |
    This utility lets you maintain config files and scripts as actual files
    that get bundled up into the userdata instead of trying to interweave
    everything in hundreds of lines of brittle `cat <<-EOT ... EOT` blocks or
    take on the overhead of pre-staging files in S3 then pulling them in from
    the instance.
---

## Usage

- Create a directory called `resources` that lives alongside your troposphere
  script and put files you need in there (e.g., scripts, configs, etc).
- Add the output from `create_resource_bundle()` to the user data text.
- Start referencing files from `./resources`.


## Source

<div class="codeblockname">resources/main.sh</div>

```bash
#!/bin/bash -ex

echo 'pretend this is actually a complicated script...'
```

<div class="codeblockname">mystack.py</div>

```python
import base64
import io
import os
import tarfile
import textwrap

from troposphere import Base64, Parameter, Sub, Template
from troposphere import ec2


RESOURCE_DIR = 'resources'


def main():
    t = Template()

    t.add_parameter(Parameter('someParameter', Type='String'))

    t.add_resource(create_instance())

    print(t.to_yaml())


def create_instance():
    return ec2.Instance(
        'myinstance',
        ImageId='ami-0123456',
        InstanceType='t2.medium',
        KeyName='my-keypair',
        UserData=Base64(Sub(textwrap.dedent(rf'''
            #!/bin/bash -ex
            exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
            echo BEGIN
            date '+%Y-%m-%d %H:%M:%S'

            export SOME_PARAMETER='${{someParameter}}'

            cd ~
            {create_resource_bundle()}

            ./resources/main.sh

            echo END
            date '+%Y-%m-%d %H:%M:%S'
        ''').lstrip())),
    )


def create_resource_bundle():
    buf = io.BytesIO()

    with tarfile.open(fileobj=buf, mode='w:gz') as f:
        f.add(RESOURCE_DIR, os.path.basename(RESOURCE_DIR))

    buf.seek(0)
    return "echo '{}' | base64 -d | tar zx".format(base64.b64encode(buf.read()).decode())


if __name__ == '__main__':
    main()
```


## Shortcomings

One thing that comes to mind is secrets.  You probably don't want anything
sensitive in there.  __If you've got secrets in your configs, you probably do
want to stash them in S3 as that will be much more secure__.  Anyone with
shell access can get the entirety of the user-data at any time just by running
`curl 169.254.169.254/latest/user-data/`.


## Comments?

Maybe there's a better way, but this works for my use cases... `¯\_(ツ)_/¯`

Is there an out-of-the-box way to do this already?  Leave a comment on [the
gist](https://gist.github.com/dbazile/40ba0b689736a3f87f26050d00f4b526) where I
was originally keeping this.
