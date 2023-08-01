import requests
import time
DISCORD_WEBHOOK_URL = 'buraya_Webhook'
GAMES = {
    'Ready Or Not': 1144200,
    'Pacify': 967050,
    "Garry's Mod": 4000,
    'Euro Truck Simulator 2': 227300,
    'Rust': 252490,
    'Sons Of The Forest': 1089790,
    'Phasmophobia': 739630,
    'Dying Light 2': 534380,
    'Devour': 1274570,
    'Call of Duty: Black Ops 3': 311210,
    'Mafia: Definitive Edition': 1030840,
    'Half-Life: Alyx': 546560,
    'Mount & Blade II: Bannerlord': 261550,
    'Cyberpunk 2077': 1091500,
    'God of War': 1593500,
    "Don't Starve Together": 322330,
    'Internet Cafe Simulator 2': 1563180,
    'Spider-Man': 1817070,
    'DayZ': 221100,
    'Outlast Trials': 1304930,
    'Fallout 4': 377160,
    'Assassin’s Creed Valhalla': 2208920,
    'Elden Ring': 1245620,
    'Mortal Kombat 11': 976310,
    'UNCHARTED: Legacy of Thieves Collection': 1659420,
    'Arma 3': 107410,
    'Resident Evil Village': 1196590,
    'DOOM Eternal': 782330,
    'A Way Out': 1222700,
    'Forza Motorsport 5': 1551360,
    'The Long Dark': 305620,
    'Devil May Cry': 601150,
    'Watch Dogs': 447040,
    'Left 4 Dead 2': 550,
    'Stranded Deep': 313120,
    'FIFA 23': 1811260,
    'Contraband Police': 756800,
    'Among Us': 945360
}
def get_game_info(app_id):
    url = f'https://store.steampowered.com/api/appdetails?appids={app_id}&cc=TR'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get(str(app_id)) and data[str(app_id)].get('success') and data[str(app_id)]['success']:
            game_data = data[str(app_id)]['data']
            return game_data
    return None

def create_embed(is_discounted):
    embed = {
        "title": f"{'İndirime Girmiş' if is_discounted else 'Henüz İndirime Girmemiş'} Oyunlar",
        "color": 16756736 if is_discounted else 65315,
        "fields": []
    }
    for game_name, app_id in GAMES.items():
        game_data = get_game_info(app_id)
        if game_data:
            price_overview = game_data.get('price_overview')
            if price_overview:
                if (price_overview.get('discount_percent', 0) > 0) == is_discounted:
                    if is_discounted:
                        embed["fields"].append({
                            "name": game_name,
                            "value": f"Normal Fiyat: {price_overview['initial_formatted']}\n"
                                     f"İndirimli Fiyat: {price_overview['final_formatted']}\n"
                                     f"İndirim Oranı: {price_overview['discount_percent']}%",
                            "inline": False
                        })
                    else:
                        embed["fields"].append({
                            "name": game_name,
                            "value": f"Fiyat: {price_overview['final_formatted']}",
                            "inline": False
                        })
            else:
                embed["fields"].append({
                    "name": game_name,
                    "value": "Fiyat bilgisi alınamadı.",
                    "inline": False
                })
        else:
            embed["fields"].append({
                "name": game_name,
                "value": "Oyun bilgisi alınamadı.",
                "inline": False
            })
    embed["footer"] = {"text": "Developed by quecy"}
    return embed

def send_discord_webhook(embed):
    data = {
        "embeds": [embed]
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Discord Webhook sent successfully.")
    else:
        print("Failed to send Discord Webhook.")

if __name__ == '__main__':
    try:
        while True:
            discounted_embed = create_embed(True)
            not_discounted_embed = create_embed(False)

            send_discord_webhook(discounted_embed)
            send_discord_webhook(not_discounted_embed)

            time.sleep(3600)
    except KeyboardInterrupt:
        print("Bot stopped.")
