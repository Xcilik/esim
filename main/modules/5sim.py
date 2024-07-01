async def handle_five_sim_order(service_id, country_id):
    country = 'russia'  # Replace with actual mapping
    operator = 'any'
    product = 'amazon'  # Replace with actual mapping
    
    headers = {
        'Authorization': 'Bearer ' + five_sim_token,
        'Accept': 'application/json',
    }

    url = f'https://5sim.net/v1/user/buy/activation/{country}/{operator}/{product}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        json_data = response.json()
        return {
            "id": json_data.get("id"),
            "phone": json_data.get("phone"),
            "product": json_data.get("product"),
            "expires": json_data.get("expires"),
            "country": json_data.get("country")
        }
    else:
        response.raise_for_status()
