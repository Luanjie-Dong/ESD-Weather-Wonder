import requests

def check_location_exists(supabase_url, supabase_table, headers, data):
    response = requests.get(
        f"{supabase_url}/rest/v1/{supabase_table}?latitude=eq.{data['latitude']}&longitude=eq.{data['longitude']}",
        headers=headers
    )
    
    if response.status_code == 200:
        locations = response.json()
        return locations[0] if locations else None
    else:
        return None


def insert_location(supabase_url, supabase_table, headers, payload):
    response = requests.post(
        f"{supabase_url}/rest/v1/{supabase_table}",
        headers=headers,
        json=payload
    )
    
    if response.status_code in [200, 201]:
        return {"success": True}
    
    return {"error": response.json()}
