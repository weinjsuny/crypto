# Multiprocessing Crypto Recorder & Data Replay
As of November 1st, 2018.

## 1. Purpose
The purpose of this application is to record full limit order book and trade tick data 
from **Coinbase Pro** and **Bitfinex** into an Arctic Tickstore database (i.e., MongoDB) 
to perform reinforcement learning research.

There are multiple branches of this project, each with a different implementation pattern for persisting data:
 - **FULL** branch is intended to be the foundation for a fully automated trading system (i.e., implementation of
 design patterns that are ideal for a trading system that requires parallel processing) and  persists streaming 
 tick data into an **Arctic Tick Store**
 
 **Note:** the branches below (i.e., lightweight, order book snapshot, mongo integration) are no longer actively maintained as of October 2018, 
 and are here for reference.
 - **LIGHT WEIGHT** branch is intended to record streaming data more efficiently than the __full__ branch (i.e., 
 all websocket connections are made from a single process __and__ the limit order book is not maintained) and
 persists streaming tick data into an **Arctic tick store**
 - **ORDER BOOK SNAPSHOT** branch has the same design pattern as the __full__ branch, but instead of recording 
 streaming ticks, snapshots of the limit order book are taken every **N** seconds and persisted 
 into an **Arctic tick store**
 - **MONGO INTEGRATION** branch is the same implementation as **ORDER BOOK SNAPSHOT**, with the difference being 
 a standard MongoDB is used, rather than Arctic. This branch was originally used to benchmark Arctic's 
 performance and is not up to date with the **FULL** branch.

## 2. Scope
Application is intended to be used to record and simulate limit order book data 
for reinforcement learning modeling. Currently, there is no functionality 
developed to place an order or automate trading.

## 3. Dependencies
- abc
- [arctic](https://github.com/manahl/arctic)
- asyncio
- datetime
- json
- multiprocessing
- numpy
- os
- pandas
- pytz
- requests
- SortedDict
- threading
- time
- websockets

## 4. Design Pattern
The design pattern is intended to serve as a foundation for implementing a trading strategy.
### 4.1 Architecture
- Each crypto pair (e.g., Bitcoin-USD) runs on its own `Process`
  - Each exchange data feed is processed in its own `Thread` within the parent crypto pair `Process`
  - A timer for periodic polling (or order book snapshots--see `mongo-integration` or `arctic-book-snapshot` 
  branch) runs on a separate thread

![Design Pattern](images/design-pattern.png)

### 4.2 Arctic Schema
**Arctic tick store** is the database implementation of choice for this project for the 
following reasons:
 - Open sourced reliability
 - Superior performance metrics (e.g., 10x data compression)

The **Arctic Tick Store** data model is essentially a `list` of `dict`s, where 
each `dict` is an incoming **tick** from the exchanges.
- Each `list` consists of `./configurations/BATCH_SIZE` ticks (e.g., 100,000 ticks)
- Per the Arctic Tick Store design, all currency pairs are stored in the **same** MongoDB collection

### 4.3 Limit Order Book
**SortedDict** pure python class is used for the limit order book
for the following reasons:
- Sorted Price **Insertions** within the limit order book
 can be performed with **O(log n)**
- Price **Deletions** within the limit order book can be performed with **O(log n)**
- **Getting / setting** values are performed with **O(1)**
- **SortedDict** interface is intuitive, thus making implementation easier

## 5. Examples and Usage
### 5.1 Recorder.py
This class is the entry point for recording tick data. 
To start the application, type `python recorder.py` into your command prompt.

### 5.2 Simulator.py
This class is used for retrieving historical tick data which was stored in the `Arctic Tick Store`
for the purpose of data replays. 

To run the simulation, type `python simulator.py` into your command prompt.

**Note** at the moment, there is only the functionality to create the dataset for
reinforcement learning. The OpenAI.Gym styled environment is still work in progress
and will be pushed after completion and thorough testing.

**Also**, make sure to adjust the query parameters within the `simulator.py` file
before running the script, to make sure you're retrieving data you have aggregated
in your `Arctic Tick Store`. 
```
    // simulator.py
    
    query = {
        'ccy': ['BCH-USD', 'tBCHUSD'],
        'start_date': 20181105,
        'end_date': 20181106
    }
```


## 6. Appendix
### 6.1 Assumptions
- You know how to start up a MongoDB database and have mongoDB installed already
- You know how to use Git tools
- You are familiar with python3

### 6.2 To-dos:
1. Create a back testing simulation environment using GYM
2. Create agent architecture using Tensorflow an equivalent (e.g., Tensorforce, Keras, etc.)
3. Create DockerFile so that simulations can be rapidly deployed in the cloud (e.g., AWS Fargate)
