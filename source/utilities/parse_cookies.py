import json

def run():
    print("Enter the cookies: ")
    cookies_raw = input()
    cookies = [c.strip() for c in cookies_raw.split(";")]
    cookies = {c.split('=')[0] :c.split('=')[1] for c in cookies}
    print(cookies)
    print(json.dumps(cookies, indent=4))


if __name__ == "__main__":
    run()
