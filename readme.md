#  SplitPe - Multiparty Split Payment System

A **microservices-based system** that automatically splits and settles payments among multiple parties.  
It enables **transparent revenue sharing** and **hassle-free payouts** through event-driven architecture.  

---

##  Project Description

This project is a **microservices architecture** built with **FastAPI**, **RabbitMQ**, and **MySQL** to handle payment splitting and settlements.

- Provides a **webhook integration** for platforms to log new orders.  
- Automatically **splits payments** based on predefined rules (percentage/fixed).  
- Manages **party balances** in their wallet (credits, debits).  
- Tracks a **history of splits** and marks orders as fully settled.  

---

##  System Architecture

The system consists of **three independent services**:

###  Payment Logger Service
- API endpoint to log **new orders**.  
- Stores orders in **MySQL**.  
- Publishes **`order.recorded`** events to RabbitMQ.  

###  Rule Splitter Service
- Listens for **`order.recorded`** events.  
- Fetches parties and their **split rules** from the database.  
- Splits payments into multiple party allocations.  
- Publishes **`wallet.credit.requested`** events for each party.  

###  Wallet Credit Service
- Listens for **`wallet.credit.requested`** events.  
- Updates **party balances** in the database.  
- Marks the order as **split complete** (`split_status = true`).  
- Logs each split into a dedicated **splits history table**.  

---

##  Tech Stack

- **Backend Framework**: FastAPI (Python)  
- **Message Broker**: RabbitMQ  
- **Database**: MySQL  
- **ORM**: SQLAlchemy  

---


##  Project Demo
[Screencast from 2025-09-23 01-09-37.webm](https://github.com/user-attachments/assets/f3ab9a6b-1589-469d-b17f-fe6109d24f42)

## RabbitMQ Pub/Sub Pattern Between Services
<img width="1920" height="588" alt="Screenshot from 2025-09-23 00-27-34" src="https://github.com/user-attachments/assets/9c61de8b-de3b-48e1-9794-65ea1399f09c" />

##  Setup Locally

### Clone the repo
```bash
https://github.com/kanishkaag/SplitPe.git
cd SplitPe
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Start RabbitMQ & MySQL server with docker compose
```bash
docker-compose up --build
```

### Start all the services by running a script
```bash
python start_services.py
```

### To run the frontend
```bash
cd frontend
npm install
npm run dev
```
### Initial Configuration (Required)
```bash
 Login to the frontend as Admin
 Navigate to "Manage Parties"
 Create required parties
 Define revenue-sharing rules (percentage / fixed amount)
```

### For Testing

```bash
Hit the webhook endpoint in Postman for intializing split for an order.
method- POST
url - http://localhost:8001/orders
body -
{
  "idempotency_key": "test56d1455adnmfsd43",
  "order_id": "ORD-2001",
  "total_amount": 55763.99
}
```
---
### Built with ❤️ by Kanishka.  


