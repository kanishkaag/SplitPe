import subprocess
import time

services = [
    {
        "name": "Order Service",
        "module": "payment_logger_service.main:app",  # path to your main.py:app
        "port": 8001
    },
    {
        "name": "Rule Split Service",
        "module": "rule_split_service.main:app",
        "port": 8002
    },
    {
        "name": "Wallet Credit Service",
        "module": "wallet_service.main:app",
        "port": 8003
    }
]

processes = []

try:
    for svc in services:
        print(f"Starting {svc['name']} on port {svc['port']}...")
        p = subprocess.Popen([
            "uvicorn",
            svc["module"],
            "--host", "0.0.0.0",
            "--port", str(svc["port"]),
            "--reload"
        ])
        processes.append(p)
        time.sleep(1)  # small delay so logs don't overlap

    print("All services are running! Press Ctrl+C to stop.")

    # Keep the script alive
    for p in processes:
        p.wait()

except KeyboardInterrupt:
    print("\n Shutting down services...")
    for p in processes:
        p.terminate()
