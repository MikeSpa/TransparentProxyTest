#!/usr/bin/python3
from brownie import (
    Box,
    TransparentUpgradeableProxy,
    ProxyAdmin,
    config,
    network,
    Contract,
)
from scripts.helpful_scripts import get_account, encode_function_data


def deploy_box():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    # Optional, deploy the ProxyAdmin and use that as the admin contract
    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
    )

    # If we want an intializer function we can add
    # `initializer=box.store, 1`
    # to simulate the initializer being the `store` function
    # with a `newValue` of 1
    box_encoded_initializer_function = encode_function_data()
    # box_encoded_initializer_function = encode_function_data(initializer=box.store, 1)
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,  # or account address
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1_000_000},  # proxies often need the gas limit
    )
    print(f"Proxy deployed to {proxy} ! You can now upgrade it to BoxV2!")
    # usually we would do box.retrieve()
    # but now we want to call these function on the proxy
    # since that address will not change unlike the logic contract address
    # We assign the abi of box contract to proxy_box
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    print(f"Here is the initial value in the Box: {proxy_box.retrieve()}")
    store_tx = proxy_box.store(8, {"from": account})
    store_tx.wait(1)
    print(f"The value in the Boxis now: {proxy_box.retrieve()}")


def main():
    deploy_box()
