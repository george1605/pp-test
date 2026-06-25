import requests
import time
import os
import json
from abc import ABC, abstractmethod

class NetworkClient(ABC):
    @abstractmethod
    def get(self, url: str) -> str:
        pass

class RealNetworkClient(NetworkClient):
    def get(self, url: str) -> str:
        """Efectuează cererea GET reală către URL-ul specificat."""
        try:
            response = requests.get(url, timeout=5)
            return response.text
        except requests.RequestException as e:
            return f"Eroare la realizarea cererii: {e}"

class CacheProxy(NetworkClient):
    def __init__(self, real_client: NetworkClient, cache_file: str = "cache.txt"):
        self._real_client = real_client
        self._cache_file = cache_file
        self._cache_duration = 3600  # 1 oră în secunde

    def _load_cache(self) -> dict:
        """Încarcă datele din fișierul text (format JSON)."""
        if not os.path.exists(self._cache_file):
            return {}
        try:
            with open(self._cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _save_cache(self, cache_data: dict):
        """Salvează datele în fișierul text."""
        with open(self._cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=4)

    def get(self, url: str) -> str:
        cache_data = self._load_cache()
        current_time = time.time()

        if url in cache_data:
            entry = cache_data[url]
            saved_time = entry.get("timestamp", 0)
            response_content = entry.get("response", "")

            if current_time - saved_time < self._cache_duration:
                print(f"[CACHE] Raspunsul a fost preluat din cache ({int(current_time - saved_time)} secunde).")
                return response_content
            else:
                print(f"[CACHE] Intrarea a expirat pentru {url}. Se efectuează cererea nouă.")
        else:
            print(f"[CACHE] URL-ul {url} nu a fost găsit în cache. Se efectuează cererea.")

        new_response = self._real_client.get(url)

        cache_data[url] = {
            "timestamp": current_time,
            "response": new_response
        }
        self._save_cache(cache_data)

        return new_response

if __name__ == "__main__":
    real_client = RealNetworkClient()
    proxy = CacheProxy(real_client, cache_file="url_cache.txt")

    test_url = "https://httpbin.org/get"

    print("--- Prima Cerere ---")
    response_1 = proxy.get(test_url)
    print(f"Lungime răspuns: {len(response_1)} caractere.\n")

    print("--- A Doua Cerere ---")
    response_2 = proxy.get(test_url)
    print(f"Lungime răspuns: {len(response_2)} caractere.\n")

    print("--- Simulare expirare cache ---")
    if os.path.exists("url_cache.txt"):
        with open("url_cache.txt", "r", encoding="utf-8") as f:
            cache_data = json.load(f)
        
        if test_url in cache_data:
            cache_data[test_url]["timestamp"] = time.time() - 7200 # 2h (mai mult decat 1h)
            with open("url_cache.txt", "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=4)

    print("--- A Treia Cerere (Cache expirat) ---")
    response_3 = proxy.get(test_url)
    print(f"Lungime raspuns: {len(response_3)} caractere.\n")