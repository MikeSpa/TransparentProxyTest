# Transparent Proxy

Test the Transparent Proxy pattern for upgrading smart contracts.


1. Deploy a `Box` implementation contract
2. Deploy a `ProxyAdmin` contract to be the admin of the proxy
3. Deploy a `TransparentUpgradeableProxy` to be the proxy for the implementations
   
Then, the upgrade script will:

4. Deploy a new Box implementation `BoxV2`
5. Upgrade the proxy to point to the new implementation contract, essentially upgrading your infrastructure. 
6. Then it will call a function only `BoxV2` can call


