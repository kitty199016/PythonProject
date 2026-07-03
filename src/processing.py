def filter_by_state(cards:list[dict], state = 'EXECUTED') -> list[dict]:
     result = [i for i in cards if i['state'] == state]
     return result

