from brownie import *
from ape_safe import ApeSafe
import requests
import os
import multisig_ci.telegram as telegram
import json

SIGNERS = os.getenv('SIGNERS')
if SIGNERS and SIGNERS != "":
    SIGNERS = json.loads(SIGNERS)

def shame_alert(bot_token, chat_id):
    alert_text = shame()
    telegram.send_and_pin_message(bot_token, chat_id, alert_text)

def shame():
    safe = ApeSafe(os.getenv('ETH_SAFE_ADDRESS'))
    url = f"https://safe-transaction.mainnet.gnosis.io/api/v1/safes/{safe}/transactions/"
    data = requests.get(url).json()
    nonce = safe.retrieve_nonce()
    pending = [tx for tx in data["results"][::-1] if not tx["isExecuted"] and tx["nonce"] >= nonce]

    safe_contract = Contract(os.getenv('ETH_SAFE_ADDRESS'))
    owners = set(safe_contract.getOwners())
    threshold = safe_contract.getThreshold()

    res = []
    if len(pending) > 4:
        res.append(
            "Okay, Okay, Okay. I need the signatures to go up. I can't take this anymore. Everyday I'm checking the signatures and it's dipping. Everyday I check the signatures, bad signatures. I can't take this anymore man. I have over-delegated, by A LOT. It is what it is but I need the signatures to go up. Can signers do something?\n"
        )

    res.append(f"pls sign/exec https://gnosis-safe.io/app/eth:{safe}/transactions/queue")
    for tx in pending:
        unsigned = owners - {x["owner"] for x in tx["confirmations"]}
        if SIGNERS and SIGNERS != "" and len(SIGNERS) > 0:
            users = " ".join(f"@{SIGNERS[x]}" for x in unsigned)
        else:
            users = " ".join(unsigned)

        num_signed = len(tx["confirmations"])
        if num_signed >= threshold:
            res.append(f'{tx["nonce"]} ({num_signed}/{threshold}): ready to exec')
        else:
            res.append(f'{tx["nonce"]} ({num_signed}/{threshold}): {users}')

    print('\n'.join(res))
    return '\n'.join(res)