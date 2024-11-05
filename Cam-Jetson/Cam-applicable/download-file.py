import requests

url = "https://ultralytics.com/images/bus.jpg"
response = requests.get(url, stream=True)
response.raise_for_status()  # Check if the request was successful

with open('bus.jpg', 'wb') as file:
    for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)

