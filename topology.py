#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from comnetsemu.cli import CLI
from comnetsemu.net import Containernet
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller, Docker

if __name__ == "__main__":

    # Only used for auto-testing.
    AUTOTEST_MODE = os.environ.get("COMNETSEMU_AUTOTEST_MODE", 0)

    setLogLevel("info")

    net = Containernet(controller=Controller, link=TCLink, xterms=False)

    info("*** Add controller\n")
    net.addController("c0")

    info("*** Creating hosts\n")
    h1 = net.addDockerHost(
        "h1", dimage="dev_test", ip="10.0.0.1", docker_args={"hostname": "h1"}
    )
    h2 = net.addDockerHost(
        "h2", dimage="dev_test", ip="10.0.0.2", docker_args={"hostname": "h2"}
    )

    info("*** Adding switch and links\n")
    switch1 = net.addSwitch("s1")
    switch2 = net.addSwitch("s2")
    net.addLink(switch1, h1, bw=10, delay="10ms")
    net.addLink(switch1, switch2, bw=10, delay="10ms")
    net.addLink(switch2, h2, bw=10, delay="10ms")

    info("\n*** Starting network\n")
    net.start()

    # Add srv1 and srv2 as Docker containers
    srv1 = net.addDocker(
        "srv1", dimage="echo_server", ip="10.0.0.3", docker_args={"hostname": "srv1"}
    )
    srv2 = net.addDocker(
        "srv2", dimage="dev_test", ip="10.0.0.4", docker_args={"hostname": "srv2"}
    )

    # Connect srv1 and srv2 to switches
    net.addLink(srv1, switch1)
    net.addLink(srv2, switch2)

    # Perform ping test between srv1 and srv2
    ping_result = net.ping([srv1, srv2])

    # Print ping results
    info("\n*** Ping Results ***\n")
    for src, dest, result in ping_result:
        info(f"{src.name} -> {dest.name}: {result}\n")

    if not AUTOTEST_MODE:
        CLI(net)

    net.stop()