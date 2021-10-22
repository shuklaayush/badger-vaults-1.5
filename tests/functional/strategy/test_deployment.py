import brownie
from brownie import (
    Vault,
    DemoStrategy
)

from helpers.constants import AddressZero

performanceFeeGovernance = 1000
performanceFeeStrategist = 1000
withdrawalFee = 50
managementFee = 50

# Test's strategy's deployment
def test_strategy_deployment(deployer, governance, keeper, guardian, strategist, token):
    
    want = token

    vault = Vault.deploy({"from": deployer})
    vault.initialize(
      token, governance, keeper, guardian, strategist, False, "", "", [performanceFeeGovernance, performanceFeeStrategist, withdrawalFee, managementFee]
    )
    vault.setStrategist(strategist, {"from": governance})
    # NOTE: Vault starts unpaused

    strategy = DemoStrategy.deploy({"from": deployer})
    strategy.initialize(
      vault, [token]
    )
    # NOTE: Strategy starts unpaused

    # Addresses
    assert strategy.want() == want
    assert strategy.governance() == governance
    assert strategy.keeper() == keeper
    assert strategy.vault() == vault
    assert strategy.guardian() == guardian

    # Params

    assert strategy.withdrawalMaxDeviationThreshold() == 50
    assert strategy.MAX() == 10_000
