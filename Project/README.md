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

1. Directory server initialised and requests all of the files on file servers. Updates a directory with respective files and locations.
2. Client makes a request to directory server. Directory server finds the location of the file in question and returns. If a lock is required the corresponding file is locked in the **dir_server.py** directory (declining request if the file is locked).
3. Client sends a request to the file server that the directory server informed it about with a message containing the operation required. File server operates this function and returns an 'OK' message.
4. If operation was executed as expected, the client now informs the directory server that the updates have been performed correctly (unless a simple READ was performed).
5. The directory server may unlock the corresponding file and/or message all other file servers to inform them of a new write/update.
6. This message contains the address of the primary file server and the name of the file in question. Each slave file server will hence use this information to ask the primary file server for the contents of the updated file. They will then either create the file on their server or update a file that's already on their server (replication). Next time that the directory server request all files on the file servers the replications will be added to the directory.

#### Limitations
* Replicated files are not locked or deleted.
* Currently: All new file are created on a single server. A file server election algorithm has to be implemented here.
* Currently: The system is not available to use on a distributed system across multiple machines.
* Currently: Code functionality is not extrapolated out into structured modular components.
* Currently: Text files are used to maintain the directory of files in the system in a plain text format. As a result, these text files have to be manually parsed out everytime a maintenance job is to be excecuted. This is messy and not consistent. **TODO:** Use a lightweight database and JSON markup to format messages.
