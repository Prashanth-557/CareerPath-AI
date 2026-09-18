import requests

print("Attempting to connect to the AI server...")

# The URL where your Flask server is running
url = "http://127.0.0.1:5000/analyze"

# We will just upload this python script itself as a "fake" PDF to test the connection
with open(__file__, 'rb') as f:
    files = {'file': ('dummy_resume.pdf', f, 'application/pdf')}
    data = {'role': 'Data Scientist'}
    
    try:
        response = requests.post(url, files=files, data=data)
        
        print("\n--- SERVER RESPONSE ---")
        print(f"Status Code: {response.status_code}")
        print("Data:")
        print(response.json())
        print("-----------------------")
        print("If you see this data, app.py is 100% PERFECT!")
        
    except Exception as e:
        print("\nCRASH: The server failed to respond.")
        print(e)