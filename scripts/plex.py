import requests
country = "mx"
m3u = f"https://i.mjh.nz/Plex/{country}.m3u8"
xml = f"https://i.mjh.nz/Plex/{country}.xml"
output_m3u = "plex.m3u"
output_xml = "plex.xml"

try:
    response = requests.get(m3u)
    if response.status_code == 200:
        print("GET request successful.")

        with open(output_m3u, "w") as f:
            f.write(response.text)
            print(f"Response saved to {output_m3u}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
    
    response = requests.get(xml)
    if response.status_code == 200:
        print("GET request successful.")

        with open(output_xml, "w") as f:
            f.write(response.text)
            print(f"Response saved to {output_xml}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print("Error making GET request:", e)