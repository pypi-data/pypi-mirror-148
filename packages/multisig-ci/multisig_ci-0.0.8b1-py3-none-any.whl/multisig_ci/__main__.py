from multisig_ci.run_brownie import run_brownie
from multisig_ci.hydrate_ci_cache import hydrate_compiler_cache
import multisig_ci.telegram as telegram
import multisig_ci.shame as shame
import sys
import os

if __name__ == '__main__':
    if 'hydrate_compiler_cache' in sys.argv:
        hydrate_compiler_cache()
        sys.exit(0)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'send_and_pin_message':
        try:
            telegram.send_and_pin_message(sys.argv[2], sys.argv[3], os.getenv("TELEGRAM_MESSAGE"))
            exit(0)
        except:
            exit(1)
    elif len(sys.argv) > 1 and sys.argv[1] == 'shame':
        try:
            shame.shame_alert(sys.argv[2], sys.argv[3])
            exit(0)
        except:
            exit(1)


    run_brownie(sys.argv[1:])