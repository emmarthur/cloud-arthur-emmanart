# How to Run the Retail Intelligence Platform

## Quick Start (Manual Method)

### Step 1: Activate Virtual Environment

```bash
# In WSL/Linux
source venv/bin/activate

# Or on Windows PowerShell
venv\Scripts\Activate.ps1
```

### Step 2: Start the Server

Open **Terminal 1** (or run in background):

```bash
cd server
python server.py
```

The server will start on `http://localhost:8080`. You should see output indicating it's running.

**Keep this terminal open!**

### Step 3: Run the Client

Open **Terminal 2** (or new terminal window):

```bash
cd client
python client.py
```

The client will connect to the server and prompt you for a project description.

## Alternative: Using the Script

```bash
# Make sure you're in the project root directory
chmod +x run_application.sh
./run_application.sh
```

## Troubleshooting

### Server Won't Start

1. **Check if dependencies are installed:**
   ```bash
   pip install -r server/requirements.txt
   ```

2. **Check if port 8080 is already in use:**
   ```bash
   # Linux/WSL
   lsof -i :8080
   # or
   netstat -tulpn | grep 8080
   ```

3. **Try a different port:**
   ```bash
   PORT=8081 python server/server.py
   ```
   Then set `MCP_URL=http://localhost:8081/mcp` in your `.env` file

### Client Can't Connect to Server

1. **Make sure server is running** (check Terminal 1)

2. **Check MCP_URL in .env file:**
   ```bash
   # Should be:
   MCP_URL=http://localhost:8080/mcp
   ```

3. **Test server connection:**
   ```bash
   curl http://localhost:8080/
   ```

### Common Errors

**"Module not found" errors:**
```bash
# Install all requirements
pip install -r client/requirements.txt
pip install -r server/requirements.txt
```

**"Port already in use":**
```bash
# Kill process on port 8080
# Linux/WSL
kill $(lsof -t -i:8080)
```

**"Virtual environment not activated":**
```bash
source venv/bin/activate  # Linux/WSL
# or
venv\Scripts\activate  # Windows
```

## Running in Background

### Server in Background:
```bash
cd server
nohup python server.py > ../server.log 2>&1 &
```

### Check if server is running:
```bash
ps aux | grep server.py
# or
curl http://localhost:8080/
```

### Stop background server:
```bash
pkill -f server.py
# or find PID and kill it
ps aux | grep server.py
kill <PID>
```

