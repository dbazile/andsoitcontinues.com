Date:     2014-07-16
Subject:  CentOS 7 and Me
Tags:     linux, centos 7, iptables, system administration, systemd
Abstract: Not every day do I get to use the word *discombobulation*, but when I do, it's epic.

A few weeks ago, there was a small quiet celebration at my workstation when I read the headlines on HN that [CentOS 7 had been released](http://wiki.centos.org/Manuals/ReleaseNotes/CentOS7).  I dunno why, but whenever there's a new major release of a Linux distro, I get all excited to see what's included.


## An excuse to upgrade

This week, I needed to build a brand new virtual machine, so I decided to take this opportunity to start with 7.  Using the updated, *very* well-designed installation interface, I performed the minimal install.  After booting up and attempting to install packages and configure services, I discovered that my cheese had been moved!

> People don't like it when you move their cheese. They are just trying to get through the maze, they have it all under control and then, poof, someone moved their cheese. Now it's a huge hassle to find it again. Change a hotkey or the case of the menus and all heck breaks loose.<span class="quoth">[Scott Hanselman](http://www.hanselman.com/blog/Windows8ProductivityWhoMovedMyCheeseOhThereItIs.aspx)</span>


## Impressions


### Lightning-fast startup

The progress bar is visible for a grand total of 1.5 seconds&mdash;which is a shame because it's a very pretty shade of purple&mdash;just before it vanishes and you're greeted by the login screen.


### Where's mysql?

I can't find any official word on it (translation: *I'm too lazy to look below the fold of the first page of Google results*), but according to [this thread on DigitalOcean](https://www.digitalocean.com/community/questions/can-t-install-mysql-on-centos-7), it looks like CentOS 7 has replaced MySQL with [MariaDB](https://mariadb.org).

I installed the `mariadb` and `mariadb-server` packages on my sandbox VM and it looked like most things are pretty much the same with a bit of rebranding&mdash;the `mysql` command still works.


### Introduction to systemd

As a level 14 Senior Apprentice of the Init.d Dark Arts, I know where all of the components live, how to string things together manually and generally where to look when something's jacked up.  systemd is a completely unknown quantity.  I've never used it or seen it used before.

Imagine my surprise when I get this cryptic response from `/sbin/service`:

    $ service httpd
    The service command supports only basic LSB actions (start, stop, restart,
    try-restart, reload, force-reload, status). For other actions, please try
    to use systemctl.

    $ service httpd status
    Redirecting to /bin/systemctl status httpd.service
    httpd.service
       Loaded: not-found (Reason: No such file or directory)
       Active: inactive (dead)

It took a good amount of Google-fu to get enough info on systemd to proceed with what I wanted to do, but ultimately I have chosen to embrace this opportunity to "explore the frontier".  I very much like the status data it provides for running services, such as listing the hierarchy of process IDs and the log tail (thus proving yet again that I'm a sucker for anything with fancy text formatting):

<img src="/writing/attachments/systemd_status.png" class="figure center" />

One thing I don't like is the very cumbersome command name `systemctl`.  Typing that leads to a ton of time-wasting typos, so I set the following alias in my .profile:

    $ alias sc=systemctl


### Impenetrable iptables (and not in a good way)

Out of the box, running `iptables -L` will show you that there are now almost 2 entire screens worth of firewall rules on a fresh install.  I don't personally have need for super complex firewall and NAT rules since I'm not configuring servers sitting directly on the Internet&mdash;I'm used to having a handful of ports open running on a (relatively) friendly network and blocking everything else.

A quick `yum remove firewalld` and I'm back in my comfort zone.  Of course, on the way out, this uninvited dinner guest decides to take all of the silverware with it: `iptables -L` is completely empty.  I documented the process I took to configure iptables below.

I know at some point I'll have to actually face the music and look into firewalld, but today ain't it.


### Okay, well let's take a look at the network interface

#### Speaking of networks, where is `ifconfig`?

The `/sbin/ifconfig` command comes in the `net-tools` package, which is not installed by default.  So, do that.


#### Where'd all these extra characters on my network interface come from?

After installing ifconfig, it's time to look at the machine's assigned IP.  The interface name has a completely different naming convention:

<img src="/writing/attachments/ifconfig_interface_name.png" class="figure center" />

As for the reason why the interface names have lost their brevity, [CentOS has posted the following reason in their FAQ](http://wiki.centos.org/FAQ/CentOS7#head-62d45421abea0220e3038796e3dd5315906fa493), emphasis mine:

> As to "breaking expectations": The foregoing example uses a 'traditionally' named network device of: eth0.  Other device names are also possible, including for example: em1 or p3p1 and such. *Like it or not, this change in approach in interface naming is the future path for Linux.*



## Some helpful stuff

During my tooling around over the last few days, I've amassed some information that might be useful to a future Dave (or even a real live actual other person).

### Removing firewalld and using simple iptables

    $ yum remove firewalld

    $ cat << EOF > /usr/lib/system.d/system/iptables.service

    [Unit]
    Description=iptables Firewall
    DefaultDependencies=false

    [Service]
    type=oneshot
    RemainAfterExit=yes
    ExecStart=/sbin/iptables-restore /etc/sysconfig/iptables
    EOF

    $ iptables -L

    Chain INPUT (policy ACCEPT)
    target     prot opt source               destination
    ACCEPT     tcp  --  anywhere             anywhere            tcp dpt:ssh
    ACCEPT     all  --  anywhere             anywhere            state RELATED,ESTABLISHED
    REJECT     all  --  anywhere             anywhere            reject-with icmp-port-unreachable

    Chain FORWARD (policy ACCEPT)
    target     prot opt source               destination
    REJECT     all  --  anywhere             anywhere            reject-with icmp-port-unreachable

    Chain OUTPUT (policy ACCEPT)
    target     prot opt source               destination

    $ iptables-save | tee /etc/sysconfig/iptables
    # Generated by iptables-save v1.4.21 on Tue Jul 15 19:16:48 2014
    *filter
    :INPUT ACCEPT [0:0]
    :FORWARD ACCEPT [0:0]
    :OUTPUT ACCEPT [0:0]
    -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
    -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    -A INPUT -j REJECT
    -A FORWARD -j REJECT
    COMMIT
    # Completed on Tue Jul 15 19:16:48 2014
    EOF

Please don't consider this to be a universal network protection solution.  This config works for me because my boxes are hosted on mostly internal development networks, not the Internet at large.


### How to convert a .VDI to a .VMDK that vSphere won't choke on

When it comes time to actually deploy a VM to vSphere, the following command also helped me tons:

    C:\> VBoxManage.exe clonehd thefile.vdi output.vmdk --format VMDK

Bear in mind that if there are snapshots, this is likely to get the wrong version of the image you want.


## References:

1. [10 iptables rules to help secure your Linux box: (Tech Republic)](http://www.techrepublic.com/blog/10-things/10-iptables-rules-to-help-secure-your-linux-box/)
2. [Example iptables systemd service written by Jan Scholz (Github)](https://github.com/vonSchlotzkow/systemd-gentoo-units/blob/master/sys-apps/systemd-units/files/services-desktop/iptables.service)
3. [CentOS 7 FAQ (CentOS Wiki)](http://wiki.centos.org/FAQ/CentOS7#head-62d45421abea0220e3038796e3dd5315906fa493)
4. [Windows 8 productivity: Who moved my cheese? Oh, there it is (Scott Hanselman)](http://www.hanselman.com/blog/Windows8ProductivityWhoMovedMyCheeseOhThereItIs.aspx)
5. [VBoxManage: clonehd Command (VirtualBox Manual)](https://www.virtualbox.org/manual/ch08.html#vboxmanage-clonevdi)
