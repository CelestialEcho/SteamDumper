import requests
import json

class BackPackTF:
    def __init__(self, api_key: str, logs: bool = True, app_id: int = 440):
        self.api_key = api_key
        self.app_id = app_id
        self.logs = logs
        self.url = "https://backpack.tf/api/IGetPrices/v4"
        self.params = {
            "key": self.api_key,
            "appid": self.app_id,
            "compress": 0
        }

    def fetch_prices(self):
        try:
            response = requests.get(self.url, params=self.params, timeout=30)
            response.raise_for_status()
            data = response.json()

            processed_data = {}

            for item_name, item_data in data["response"]["items"].items():
                last_update = None
                value = None
                currency = None
                difference = None

                for quality in item_data["prices"].values():
                    for tradable in quality.values():
                        for craftable in tradable.values():
                            if isinstance(craftable, list):
                                for price_info in craftable:
                                    if isinstance(price_info, dict):
                                        if price_info.get("last_update") and (last_update is None or price_info["last_update"] > last_update):
                                            last_update = price_info["last_update"]
                                            value = price_info["value"]
                                            currency = price_info["currency"]
                                            difference = price_info["difference"]

                processed_data[item_name] = {"last_update": last_update, "value": value, "currency": currency, "difference": difference}
                if self.logs:
                    print(f"[+] {item_name} | time: {last_update} value: {value}")

            return processed_data

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    def save_processed_data(self, processed_data: dict, filename: str = "processed_response.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(processed_data, file, ensure_ascii=False, indent=4)
        if self.logs:
            print(f"Processed data saved to file '{filename}'")

    def run(self):
        processed_data = self.fetch_prices()
        if processed_data:
            self.save_processed_data(processed_data)

if __name__ == "__main__":
    api_key = ""
    fetcher = BackPackTF(api_key, logs=False)
    fetcher.run()
