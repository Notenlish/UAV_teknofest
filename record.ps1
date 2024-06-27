Start-Process -FilePath py streaming/server.py

# Start the second Python script
Start-Process -FilePath py streaming/client.py
