import requests
import random
import string
import concurrent.futures
import time

def generate_random_string(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def check_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.url != "https://zrr.ddu.kr/?zrr=404"
    except requests.RequestException:
        return False

def check_and_save_url(base_url):
    while True:
        random_string = generate_random_string()
        full_url = base_url + random_string
        if check_url(full_url):
            with open("link.log", "a") as file:
                file.write(full_url + "\n")
            print(f"URL saved: {full_url}")


def main():
    base_url = "https://zrr.kr/"
    num_workers = 5 

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(check_and_save_url, base_url) for _ in range(num_workers)]
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()