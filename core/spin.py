import requests
import time

from hokireceh_claimer import base
from core.headers import headers
from core.info import get_info


def spin_info(data, proxies=None):
    url = "https://api.tabibot.com/api/spin/v1/info"

    try:
        response = requests.post(
            url=url, headers=headers(data=data), proxies=proxies, timeout=20
        )
        data = response.json()
        energy = data["data"]["energy"]["energy"]
        return energy
    except:
        return None


def play_spin(data, multiplier, proxies=None):
    url = "https://api.tabibot.com/api/spin/v1/play"
    payload = {"multiplier": multiplier}

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        prize = data["data"]["prize"]
        return prize
    except:
        return None


def process_spin(data, multiplier, proxies=None):
    while True:
        energy = spin_info(data=data, proxies=proxies)
        if energy is not None:
            if energy > 0:
                final_multiplier = min(multiplier, energy)
                prize = play_spin(
                    data=data, multiplier=final_multiplier, proxies=proxies
                )
                if prize:
                    prize_type = prize["prize_type"]
                    amount = prize["amount"]
                    multiplier = prize["multiplier"]
                    if amount > 0:
                        base.log(
                            f"{base.white}Auto Spin: {base.green}Success | Added {amount*multiplier} {prize_type}"
                        )
                    else:
                        base.log(
                            f"{base.white}Auto Spin: {base.green}Success | {base.red}{amount*multiplier} {prize_type}"
                        )
                    get_info(data=data, proxies=proxies)
                    time.sleep(1)
                else:
                    base.log(f"{base.white}Auto Spin: {base.red}Fail")
                    break
            else:
                base.log(f"{base.white}Auto Spin: {base.red}No energy to spin")
                break
        else:
            base.log(f"{base.white}Auto Spin: {base.red}Energy data not found")
            break
