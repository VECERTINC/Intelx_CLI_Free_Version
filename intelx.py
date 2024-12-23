import requests
import json
import os
from colorama import init, Fore, Style
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

# File where the API key is stored
API_FILE = "API.txt"

def get_api_key():
    if os.path.exists(API_FILE):
        with open(API_FILE, 'r') as file:
            return file.read().strip()
    else:
        api_key = input(f"{Fore.YELLOW}Enter your API Key: {Style.RESET_ALL}")
        with open(API_FILE, 'w') as file:
            file.write(api_key)
        return api_key

API_KEY = get_api_key()

BASE_URL = "https://2.intelx.io"
HEADERS = {
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Accept-Language": "es-ES,es;q=0.9",
    "Sec-Ch-Ua": "\"Not?A_Brand\";v=\"99\", \"Chromium\";v=\"130\"",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36",
    "X-Key": API_KEY,
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://intelx.io"
}

def search(term):
    search_endpoint = f"{BASE_URL}/intelligent/search"
    data = {
        "term": term,
        "buckets": ["leaks.public.wikileaks", "leaks.public.general", "dumpster", "documents.public.scihub"],
        "lookuplevel": 0,
        "maxresults": 1000,
        "timeout": None,
        "datefrom": "",
        "dateto": "",
        "sort": 2,
        "media": 0,
        "terminate": []
    }
    
    response = requests.post(search_endpoint, headers=HEADERS, data=json.dumps(data))
    
    # Check response status and content
    if response.status_code != 200:
        print(f"{Fore.RED}✘ Error: Received status code {response.status_code}")
        print(f"Response content: {response.text}")
        return None
    
    try:
        response_data = response.json()
        return response_data.get("id")
    except json.JSONDecodeError:
        print(f"{Fore.RED}✘ Error: Unable to parse JSON response")
        print(f"Response content: {response.text}")
        return None

def get_results(search_id):
    results_endpoint = f"{BASE_URL}/intelligent/search/result"
    params = {
        "id": search_id,
        "limit": 90,
        "statistics": 1,
        "previewlines": 8
    }
    
    response = requests.get(results_endpoint, headers=HEADERS, params=params)
    
    if response.status_code != 200:
        print(f"{Fore.RED}✘ Error: Received status code {response.status_code}")
        print(f"Response content: {response.text}")
        return []

    try:
        response_data = response.json()
        return response_data.get('records', [])
    except json.JSONDecodeError:
        print(f"{Fore.RED}✘ Error: Unable to parse JSON response")
        print(f"Response content: {response.text}")
        return []

def preview_file(storage_id, api_key):
    preview_endpoint = f"{BASE_URL}/file/preview"
    params = {
        "sid": storage_id,
        "f": 0,
        "l": 8,
        "c": 1,
        "m": 24,
        "b": "leaks.public.general",
        "k": api_key
    }
    
    response = requests.get(preview_endpoint, headers=HEADERS, params=params)
    return response.content

def download_full_file(system_id):
    download_endpoint = f"{BASE_URL}/file/read?type=1&systemid={system_id}&bucket=leaks.public.general"
    response = requests.get(download_endpoint, headers=HEADERS, stream=True)
    
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        filename = f"{system_id}.bin"
        
        with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                bar.update(len(chunk))
        
        print(f"{Fore.GREEN}✔ File downloaded as {filename}")
    else:
        print(f"{Fore.RED}✘ Could not download the file.")

def main():
    while True:
        # ASCII Art
        ascii_art = f"""
{Fore.CYAN}



 ______              __                __           
/      |            /  |              /  |          
$$$$$$/  _______   _$$ |_     ______  $$ | __    __ 
  $$ |  /       \ / $$   |   /      \ $$ |/  \  /  |
  $$ |  $$$$$$$  |$$$$$$/   /$$$$$$  |$$ |$$  \/$$/ 
  $$ |  $$ |  $$ |  $$ | __ $$    $$ |$$ | $$  $$<  
 _$$ |_ $$ |  $$ |  $$ |/  |$$$$$$$$/ $$ | /$$$$  \ 
/ $$   |$$ |  $$ |  $$  $$/ $$       |$$ |/$$/ $$  |
$$$$$$/ $$/   $$/    $$$$/   $$$$$$$/ $$/ $$/   $$/ 
                                                    
                                                    

                      
vecert.io  Intelx Free Lookup


{Style.RESET_ALL}
"""
        print(ascii_art)
        
        term = input(f"{Fore.YELLOW}Enter an IP address, email, or domain: {Style.RESET_ALL}")
        search_id = search(term)

        if not search_id:
            print(f"{Fore.RED}✘ No results found.")
            continue

        results = get_results(search_id)
        
        if not results:
            print(f"{Fore.RED}✘ No results found for the provided ID.")
            continue

        # Display results
        print(f"{Fore.CYAN}Results:")
        for index, result in enumerate(results):
            if isinstance(result, dict):
                print(f"{Fore.GREEN}{index + 1}. {Fore.BLUE}System ID: {result.get('systemid', 'N/A')} {Fore.WHITE}- Name: {result.get('name', 'N/A')}")
            else:
                print(f"{Fore.RED}{index + 1}. Unexpected result format: {result}")

        choice = int(input(f"{Fore.YELLOW}Enter the number of the result you wish to view: {Style.RESET_ALL}")) - 1

        if 0 <= choice < len(results):
            selected_result = results[choice]
            storage_id = selected_result.get('storageid')
            system_id = selected_result.get('systemid')
            
            if storage_id and system_id:
                preview_content = preview_file(storage_id, API_KEY)
                print(f"{Fore.CYAN}Preview content:")
                print(preview_content.decode('utf-8'))

                download_choice = input(f"{Fore.YELLOW}Do you want to download the full file? (y/n): {Style.RESET_ALL}").strip().lower()
                if download_choice == 'y':
                    download_full_file(system_id)
                    
                    # Ask if the user wants to exit or return to the menu
                    exit_choice = input(f"{Fore.YELLOW}Do you want to exit the script? (y/n): {Style.RESET_ALL}").strip().lower()
                    if exit_choice == 'y':
                        break
            else:
                print(f"{Fore.RED}✘ Storage ID or System ID not found in the selected result.")
        else:
            print(f"{Fore.RED}✘ Invalid selection.")

if __name__ == "__main__":
    main()
