async def handle_five_sim_order(service_id, country_id):
    country = 'country_id'  # Replace with actual mapping
    operator = 'any'
    product = 'telegram'  # Replace with actual mapping
    
    headers = {
        'Authorization': 'Bearer ' + five_sim_token,
        'Accept': 'application/json',
    }

    url = f'https://5sim.net/v1/user/buy/activation/{country}/{operator}/{product}'
    response = requests.get(url, headers=headers)
    return response.json()
