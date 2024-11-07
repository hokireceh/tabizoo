import requests

from hokireceh_claimer import base
from core.headers import headers


def get_info(data, proxies=None):
    url = "https://api.tabibot.com/api/user/v1/profile"

    try:
        response = requests.get(
            url=url, headers=headers(data=data), proxies=proxies, timeout=20
        )
        data = response.json()
        coins = data["data"]["user"]["coins"]
        zoo_coins = data["data"]["user"]["zoo_coins"]
        crystal_coins = data["data"]["user"]["crystal_coins"]
        level = data["data"]["user"]["level"]
        streak = data["data"]["user"]["streak"]

        base.log(
            f"{base.green}Coins: {base.white}{coins:,} - {base.green}Zoo Coins: {base.white}{zoo_coins:,} - {base.green}Crystal Coins: {base.white}{crystal_coins:,} - {base.green}Level: {base.white}{level} - {base.green}Streak: {base.white}{streak}"
        )
        return data
    except:
        return None
