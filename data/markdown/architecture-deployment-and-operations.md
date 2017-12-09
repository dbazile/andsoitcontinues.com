---
date:    2017-12-09
subject: Architecture, Deployment and Operations
tags:
    - architecture
    - containers
    - deployments
    - development
    - CI/CD
    - GIS
    - geospatial
abstract: |
    A baseline application development and deployment model based on lessons
    learned from the last two years of building, extending and deploying apps
    in CI/CD in "enterprise" GIS.
---

## Background

Over the last two years I've started and contributed to a number of projects
at work.  In each of those projects, I've seen myriad approaches to solving the
same problems: provisioning local development environments, test/stage/prod
deployment infrastructure and __effectively__ managing the configurations
between all of those things.  I've made my own naïve attempts to solve these
problems on my own, often with little to zero visibility into the context of
upstream environments that the code will be deployed into.

While some of those approaches have been well thought-out, executed and
documented, most have been nightmarishly inconsistent and fraught with kludges
and hacks (occasionally for good reason).  This post is an attempt to
reconcile the lessons learned from all of that into a single document/design
specification that can serve as the basis for further discussion and
refinement with other devs and ops folk.

Much of my thinking on this is inspired by discussions with folks in
operations, quality assurance and other developers, from reading opinions on
Twitter, HN, from decomposing aspects of some popular PaaS platforms and from
poring over scores of `Jenkinsfile`s, `Dockerfile`s and `manifest.yml`s.

### What's the scope of the problem?

Here are some of the stickier issues I've seen that my proposed model aims to
solve:

#### Difficulty standing up a development environment on a developer's local machine

Installing and running the bits needed to run one or more components on a
developer's local machine ranges from cumbersome to impossible.

#### System-level incompatibilities between builders and runtime environments cause builds to pass but deployments to fail

We had a microservice that unit tested and packaged successfully in CI but
exploded at deployment time because we were vendoring dependencies at build
time (via `pip download -r requirements.txt`) and the build agent, running
RHEL, provides Python 2.7 compiled with narrow Unicode character width (UCS-2)
while the runtime environment, running Debian, provides Python 2.7 compiled
with wide Unicode character widths (UCS-4) ([ref](https://stackoverflow.com/questions/1446347/how-to-find-out-if-python-is-compiled-with-ucs-2-or-ucs-4)).

PSA: stuff like this is why you should be using Python 3, people. ;)

#### One-size-fits-all build infrastructure will inevitably lead to snowflake configurations

Most of the time, projects that are even written in the same language vary
wildly in configuration and OS requirements.  This leads to people adopting
"pet" build agents that can handle their project's needs by making (usually
undocumented) ad hoc changes to the build boxes themselves.  Eventually, that
pet stops functioning in a predictable way and gets decommissioned and replaced
with a more generic one that fixes some projects while hosing the others that
had come to rely on the nonstandard behavior, starting the cycle all over
again.

[![A Vicious Cycle](/writing/attachments/vicious-cycle.png)](http://www.smbc-comics.com/comic/a-vicious-cycle)

#### Installing "sciency" dependencies (e.g., GDAL, scipy, numpy, etc) can be hard to get right and harder to repeat

While they work, some of these libraries require some serious configuration
gymnastics to compile, install and make portable.  At the risk of
overgeneralizing, scientists (rightfully) are often more interested in proving
theorem and correctness at the expense of code convention, readability and
(most importantly) portability.  Some of the messiest/scariest code I've seen
has been from peeking at source code of widely-used geospatial libraries and
tools (e.g., `gdal_merge.py`, OSM's `generate_tiles.py`, and pretty much _any_
implementation of decimal-degree-to-UTM/MGRS coordinate conversion, etc).

Or, as one commenter at [The Daily WTF](https://thedailywtf.com/articles/comments/an-academic-consideration#comment-489696) put it:

> As a sysadmin for a research computing facility, "scientists write
> code. It’s often not very good code" is the biggest understatement I've
> seen on this site. And yes, I've been reading this site for several years.
> Scientific code is, generally speaking, horrific.

I still have nightmares about the time I tried to install GDAL with Python
bindings on bare metal on macOS.  I'd never used Homebrew because I'd been
actively trying to avoid it. I'll spare you the gory details and just say that
I now use Homebrew...

#### Managed PaaS components being arbitrarily removed/downgraded without notice

We were plagued by a random "rolling back" of CloudFoundry buildpack versions
that would happen every couple of weeks or so and I'd have to bug the same guy
every single time to have him fix it.  I'm sure he got tired of me after the
third or fourth time I raised the issue, but apparently not tired enough to
automate the whole thing. ¯\\\_(ツ)\_/¯

Mind you, I don't attribute this occurrence to malice, but likely some AMI or
EBS snapshot that kept falling back to baseline because changes were never
persisted.




## Proposed Model

If you'd like to critique some aspect of this model, please post a comment on
[the GitHub gist I wrote to collect my notes](https://gist.github.com/dbazile/5320772d9c739ea9b797c92a8194f0d6).

This model depends on containers to bridge the gaps between developer laptops,
CI servers and production servers.  If the deployment environments (e.g.,
stage, production, qa, etc) can't run containers for whatever reason, __at
minimum, containers should be used in CI to build and stage `.rpms` or `.debs`
that can be installed into whatever raw VM/box comprises the running system__.

This model also assumes partial or full adherence to
[12-Factor](https://12factor.net/) principles, __at minimum, externalized
configuration in the form of environment variables (preferably) or
configuration files (if you've just _gots_ to have you some crazy-convoluted
configs)__.

Finally, the model uses AWS concepts (e.g., EC2, RDS, CloudFormation, etc) for
the purpose of illustration, but can work in other vendors' cloud offerings.



### Local Development Environment

Developers run Docker on their laptops to run and test individual application
components along with any backing services (e.g., PostgreSQL, RabbitMQ,
GeoServer, etc).  Optionally, the requests to those collaborating services can
instead be proxied to the `dev` or `stage` deployment environment instances.

All configurations to the runtime environment occur inside the `Dockerfile`,
`docker-compose.yml` or some other configuration file that is checked into
version control.  Secrets are fed in via environment variables at runtime at
the command prompt, e.g.,:

```
docker-compose build

docker-compose run -e SECRET=secret myproj-component-a
```

...or by whatever mechanism the developer's IDE allows them to define and pass
environment variables into Docker.

If the component needs some dependency that's crazy-hard to install or compile,
__that process should be extracted into its own `Dockerfile`__ which is used to
create a base image.  Once the base image is built, the actual application
component's `Dockerfile` should extend via `FROM myproj/crazy-dep:v1.2.3`.



### CI/CD Pipeline

This is an abstract pipeline design that optimizes for
[blue/green deployments](https://martinfowler.com/bliki/BlueGreenDeployment.html),
[repeatable builds](https://martinfowler.com/bliki/ReproducibleBuild.html) and
bakes in the ability to rapidly deploy a hotfix in emergencies.

The unit being tested, built and deployed here is some application component
such as a microservice.

#### Parameters

| Parameter            | Default | Description                                                              |
|----------------------|---------|--------------------------------------------------------------------------|
| `version`            | `HEAD`  | Git tag or commit SHA to be built and deployed.                          |
| `target`             | `stage` | Enumeration: `{ dev | stage | prod }`                                    |
| `skip_slow_scans`    | `false` | Enable builds to optionally complete faster by skipping some slow scans. |

#### Stages

- **Prepare Workspace**
    - Clean workspace
    - Check out `$version`
- **Unit Tests**
    - Executes unit tests inside Docker container
- **Build**
    - Builds artifacts inside Docker container (e.g., `.tgz`, `.rpm`, `.deb`,
    `.jar`, etc)
- **Push artifacts to Nexus/S3**
- **Deploy (initial)**
    - Pull artifact from Nexus/S3
    - Push to `$target` with version-suffixed domain/route
- **Integration Tests**
    - If `$skip_slow_scans`, skip X, Y and/or Z
- **Deploy (cutover)**
    - Point unsuffixed domain/route to newly deployed instance
    - Terminate previous instance



### Deployment Infrastructure

#### Build Artifacts

Build artifacts would ideally be pushed to some central repository that the CI
server has read/write access to.  This example just uses some S3 bucket, e.g.:

```
myproj-build-artifacts/<component_name>/myproj-<component_name>-<version>-<commit_sha>.tar.gz
```

#### Domains/Routing

To accomplish the blue/green deployment, each project component requires
__at least__ two DNS entries:

##### 1. Fully-qualified application hostname

```
<component_name>-<commit_sha>.<target>.myproj.somehost.com
```

This entry enables us to run integration tests on the incoming instance
to make sure it actually works before tearing down the previous instance.

The CI server updates this DNS record during each build.

##### 2. Short "alias" to the fully-qualified hostname

```
<component_name>.<target>.myproj.somehost.com
```

This entry is effectively a pointer to the latest deployed instance of a
component (identified by its commit SHA-suffixed hostname), allowing for
"zero downtime" deployments (in theory).  It will always point to a
running instance (either the previous instance just before it gets torn down)
or the incoming instance (once the alias record gets updated to point to it).

The CI server updates this DNS record during each build __if and only if__
the integration tests for the incoming instance all pass.



### Releases

Given some project _myproj_ that is to be deployed directly onto one or more
EC2 instances:

| Repository/Pipeline Name | Params                      | Description |
|--------------------------|-----------------------------|-------------|
| `myproj-infrastructure`  | <ul><li>`$target`</li></ul> | <p>Creates a deployment target environment (e.g., `dev`, `qa`, `stage`, `prod`) and provisions all of the raw resources needed to run the system (e.g., VPC, Route53, S3, EC2, RDS, etc)</p><p>All infrastructure should be tagged for push-button wholesale teardown of **everything** inside the deployment target environment.</p> |
| `myproj-api`             | <ul><li>`$target`</li><li>`$version`</li></ul> | |
| `myproj-ui`              | <ul><li>`$target`</li><li>`$version`</li></ul> | |
| `myproj-microservice-a`  | <ul><li>`$target`</li><li>`$version`</li></ul> | |
| `myproj-microservice-b`  | <ul><li>`$target`</li><li>`$version`</li></ul> | |
| __`myproj-release`__     | <ul><li>`$target`</li><li>`$api_version`</li><li>`$ui_version`</li><li>`$msa_version`</li><li>`$msb_version`</li></ul> | <p>Triggers and waits for each of the above builds and optionally flip some arbitrary switch at the end of it all (maybe set and push some git tags to the repos?).</p><p>**Given the same set of parameters, the build system should be capable of deploying an exact replica each .**</p> |




## What's the next step?

To support the lowest common denominator, this model assumes the deployment
target __is not__ a PaaS, but a collection of EC2 instances that we're
directly installing `.deb`s or `.rpms` onto.  But with things like
[EKS](https://aws.amazon.com/about-aws/whats-new/2017/11/introducing-amazon-elastic-container-service-for-kubernetes/) and
[Fargate](https://aws.amazon.com/blogs/aws/aws-fargate/) on the horizon, the
up-front complexity of deploying containers to production should drop
significantly in the future.  As such, my next area of research is use cases
and design considerations for using Kubernetes, Mesos or some other container
orchestration platform in production.
