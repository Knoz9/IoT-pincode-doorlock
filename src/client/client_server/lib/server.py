def heartbeat(apikey):
    import urequests as requests
    r = requests.get("https://pinlock.nor.nu/api/lock/beat?apikey=" + apikey)
    r.close()

def check(apikey, pin):
    import urequests as requests
    r = requests.get("https://pinlock.nor.nu/api/lock?pin=" + pin + "&apikey=" + apikey)
    response = r.json()
    r.close()
    return response