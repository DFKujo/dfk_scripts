import requests

url = 'https://api.defikingdoms.com/graphql'
limit = 1000  # Assuming the limit per request is 1000

def fetch_data(skip):
    query = f"""
    {{
      bloater_suit: armors(skip: {skip}, where: {{displayId: 50000}}) {{
        id
        displayId
      }}
      karate_gi: armors(skip: {skip}, where: {{displayId: 50001}}) {{
        id
        displayId
      }}
      bloater_head: accessories(skip: {skip}, where: {{displayId: 50000}}) {{
        id
        displayId
      }}
    }}
    """
    result = requests.post(url, json={'query': query})
    return result.json()

total_bloater_suit = 0
total_karate_gi = 0
total_bloater_head = 0
skip = 0

while True:
    data = fetch_data(skip)
    bloater_suit_count = len(data['data']['bloater_suit'])
    karate_gi_count = len(data['data']['karate_gi'])
    bloater_head_count = len(data['data']['bloater_head'])

    total_bloater_suit += bloater_suit_count
    total_karate_gi += karate_gi_count
    total_bloater_head += bloater_head_count

    if bloater_suit_count < limit and karate_gi_count < limit and bloater_head_count < limit:
        break

    skip += limit

print(f"Total Bloater Suit: {total_bloater_suit}")
print(f"Total Karate Gi: {total_karate_gi}")
print(f"Total Bloater Head: {total_bloater_head}")
