from .api import Api


def get_cli_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", type=str, default="http://192.168.0.1")
    parser.add_argument("-u", "--user", type=str, default="admin")
    parser.add_argument("password", type=str)
    return parser.parse_args()


def get_router():
    args = get_cli_args()
    router = Api(args.address, args.user, args.password)
    router.login()
    return router


def disable_firewall():
    router = get_router()
    old_state = router.get_firewall()
    router.set_firewall(False)
    new_state = router.get_firewall()
    if old_state != new_state:
        print(f"Firewall state changed: {old_state} -> {new_state}")
    else:
        print(f"Firewall state did not change ({old_state})")
    router.logout()


def recent_calls():
    router = get_router()
    print(router.get_calls())
    router.logout()
