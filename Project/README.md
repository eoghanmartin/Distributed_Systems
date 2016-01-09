# A Basic Distributed File System

#### Requirements
* Python 2.7

## Features
1. Transparent Distributed File System
2. Locking on Writes
3. Replication

### 1. Transparent Distributed File System
The **ClientProxy.py** file is used to implement an interface to the **client.py** file. **open(fileName)**, **delete(fileName)**, **write(fileName, data)** and **create(fileName)** functions are exposed to the client.
The files are written to a file server and the directory of files to file servers is maintained by the **dir_server.py**.

### 2. Locking on Writes
Locking is impolemented in the **dir_server.py** file. A lock is associated with a file directory entry while writes are being performed.

### 3. Replication
Upon any write operation, all files are replicated across the system.

### System Architecture
![alt tag](https://raw.githubusercontent.com/eoghanmartin/Distributed_Systems/master/Project/components.png)

#### Limitations
* Replicated files are not locked or deleted.
* Currently: All new file are created on a single server. A file server election algorithm has to be implemented here.
* Currently: The system is not available to use on a distributed system across multiple machines.
