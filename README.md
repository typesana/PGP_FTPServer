# GPG_FTPServer
FTP Server & Clients with PGP. (Python 3)

## Quick Start
### Server
1. requirements
    ```shell script
    cd server
    # Maybe you should use pip
    pip3 install -r requirements.txt
    ```
2. run quick_start.py
    ```shell
    python3 quick_start.py
    ```
    This script will create basic file folders and move some files.

3. ftpServer.py
    ```shell script
    python3 ftpServer.py 127.0.0.1 2121
    ```
    Start FTPS Service on localhost:2121
### Client
1. requirements
    ```shell script
    cd client
    # Maybe you should use pip
    pip3 install -r requirements.txt
    ```
2. ftpClient.py
    ```shell script
    python3 ftpClient.py
    ```
    You should adjust some args if you want to use Unit Test.
    
## GUI
You can use GUI by run
```
python3 ftpClientGUI.py
```
