import json

def run():
    print("Enter the cookies: ")
    cookies_raw = input()
    cookies_list = [c.strip() for c in cookies_raw.split(";")]
    cookies = {}

    for cookie in cookies_list:
        twodotid = cookie.index('=')
        key = cookie[:twodotid]
        val = cookie[twodotid+1:]
        cookies[key] = val
    print(json.dumps(cookies, indent=4))


if __name__ == "__main__":
    run()
