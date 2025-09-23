#  SplitPe - Multiparty Split Payment System

A **microservices-based system** that automatically splits and settles payments among multiple parties.  
It enables **transparent revenue sharing** and **hassle-free payouts** through event-driven architecture.  

---

##  Project Description

This project is a **microservices architecture** built with **FastAPI**, **RabbitMQ**, and **MySQL** to handle payment splitting and settlements.

- Provides a **webhook integration** for platforms to log new orders.  
- Automatically **splits payments** based on predefined rules (percentage/fixed).  
- Manages **party balances** (credits, debits, refunds).  
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