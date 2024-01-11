from web3 import Web3
import json
import os
import datetime

# ABI for ERC20 token
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

# Function to get balances
async def get_balance():
    try:
        # Providers
        HARMProvider = Web3(Web3.HTTPProvider('https://api.harmony.one/'))
        DFKCProvider = Web3(Web3.HTTPProvider('https://subnets.avax.network/defi-kingdoms/dfk-chain/rpc'))
        KLAYProvider = Web3(Web3.HTTPProvider('https://klaytn.rpc.defikingdoms.com/'))

        # Contract instances
        HARMJEWEL = HARMProvider.eth.contract(address="0x72Cb10C6bfA5624dD07Ef608027E366bd690048F", abi=ERC20_ABI)
        KLAYJEWEL = KLAYProvider.eth.contract(address="0x30C103f8f5A3A732DFe2dCE1Cc9446f545527b43", abi=ERC20_ABI)

        # Total burn amounts
        tokenomicsBurn = 375328483.070918749502816906

        # Get and convert balances
        balanceHARM = HARMJEWEL.functions.balanceOf('0x000000000000000000000000000000000000dEaD').call()
        formattedHARM = balanceHARM / 1e18

        DFKCJEWEL = DFKCProvider.eth.get_balance('0x000000000000000000000000000000000000dEaD') / 1e18
        DFKCValJEWEL = DFKCProvider.eth.get_balance('0x0000000000000000000000000000000000000000') / 1e18
        totalDFKJ = DFKCJEWEL + DFKCValJEWEL - tokenomicsBurn

        balanceKLAY = KLAYJEWEL.functions.balanceOf('0x000000000000000000000000000000000000dEaD').call()
        formattedKLAY = balanceKLAY / 1e18

        totalBurn = totalDFKJ + formattedKLAY + formattedHARM

        # Create query object
        query = {
            "day": str(datetime.date.today()),
            "time": str(datetime.datetime.now().time()),
            "totalBurn": f"{totalBurn} JEWEL",
            "difference": None
        }

        # Read previous queries from JSON file
        previousQueries = []
        if os.path.exists('queries.json'):
            with open('queries.json', 'r') as file:
                previousQueries = json.load(file)

        # Calculate difference from previous query
        if previousQueries:
            previousTotalBurn = float(previousQueries[-1]["totalBurn"].split()[0])
            query["difference"] = f"{totalBurn - previousTotalBurn} JEWEL"

        # Add current query to previous queries
        previousQueries.append(query)

        # Write updated queries to JSON file
        with open('queries.json', 'w') as file:
            json.dump(previousQueries, file, indent=2)

        # Display query information
        print(f"Harmony Burn: {formattedHARM}")
        print(f"DFKC Burn: {totalDFKJ}")
        print(f"Klaytn Burn: {formattedKLAY}")
        print(f"\nTotal Burn: {totalBurn} JEWEL")
        print(f"Difference from previous query: {query['difference']}")

    except Exception as e:
        print(f"Error: {e}")

# Run the function
import asyncio
asyncio.run(get_balance())
