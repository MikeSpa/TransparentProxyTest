#!/usr/bin/python3
from brownie import (
    BoxV2,
    TransparentUpgradeableProxy,
    ProxyAdmin,
    config,
    network,
    Contract,
)
from scripts.helpful_scripts import get_account, upgrade
from scripts.deploy_box import deploy_box


def upgrade_box():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box_v2 = BoxV2.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    proxy = TransparentUpgradeableProxy[-1]
    proxy_admin = ProxyAdmin[-1]
    # now to interact with boxV2 through the proxy
    # we need to call upgradeTo in TUP.sol
    # we will do that from a upgrade fct in python
    upgrade_tx = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )
    upgrade_tx.wait(1)
    print("Proxy has been upgraded!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    print(f"Starting value {proxy_box.retrieve()}")
    proxy_box.increment({"from": account})
    print(f"Ending value {proxy_box.retrieve()}")


def main():
    deploy_box()
    upgrade_box()
