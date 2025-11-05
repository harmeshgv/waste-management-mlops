mcqueen@mcqueen-Dell-G15-5511:~$ docker run -d \
  --name splunk \
  -p 8000:8000 \     # Web UI
  -p 8088:8088 \     # HTTP Event Collector (HEC)
  -p 8089:8089 \     # Management port (API)
  -e SPLUNK_START_ARGS="--accept-license" \
  -e SPLUNK_PASSWORD="admin12345" \
  splunk/splunk:latest
docker: invalid reference format

Run 'docker run --help' for more information
-p: command not found
-p: command not found
-e: command not found
mcqueen@mcqueen-Dell-G15-5511:~$ docker run -d \
  --name splunk \
  -p 8000:8000 \
  -p 8088:8088 \
  -p 8089:8089 \
  -e SPLUNK_START_ARGS="--accept-license" \
  -e SPLUNK_PASSWORD="admin12345" \
  splunk/splunk:latest
Unable to find image 'splunk/splunk:latest' locally
latest: Pulling from splunk/splunk
98b82e37c199: Pull complete
f5585752eb41: Pull complete
c3d0d4e43412: Pull complete
7bcfe765925e: Pull complete
3cf1bb3aa2af: Pull complete
ede3ffb0f67f: Downloading  179.3MB/1.146GB
4f4fb700ef54: Download complete
dcf0b775b7a2: Downloading  163.7MB/590.5MB
ede3ffb0f67f: Pull complete
4f4fb700ef54: Pull complete
dcf0b775b7a2: Pull complete
ea21c0c3ab53: Pull complete
da055c4f209e: Pull complete
4c1883d5c796: Pull complete
Digest: sha256:4a5ce5a7b4e84a87396f0664895095c6510a0f2bf52e8747a373c7357f3ee313
Status: Downloaded newer image for splunk/splunk:latest
af6fe571dbd5aa4791588688aa438b07615cfa63523feada9af3180643b52b29
mcqueen@mcqueen-Dell-G15-5511:~$
mcqueen@mcqueen-Dell-G15-5511:~$
mcqueen@mcqueen-Dell-G15-5511:~$
mcqueen@mcqueen-Dell-G15-5511:~$ docker run -d   --name splunk   -p 8000:8000   -p 8088:8088   -p 8089:8089   -e SPLUNK_START_ARGS="--accept-license"   -e SPLUNK_PASSWORD="admin12345"   splunk/splunk:latest
docker: Error response from daemon: Conflict. The container name "/splunk" is already in use by container "af6fe571dbd5aa4791588688aa438b07615cfa63523feada9af3180643b52b29". You have to remove (or rename) that container to be able to reuse that name.

Run 'docker run --help' for more information
mcqueen@mcqueen-Dell-G15-5511:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
mcqueen@mcqueen-Dell-G15-5511:~$ # Check all containers (including stopped ones)
docker ps -a

# Check container logs
docker logs splunk

# If the container exists but isn't running, start it
docker start splunk
CONTAINER ID   IMAGE                  COMMAND                  CREATED         STATUS                     PORTS     NAMES
af6fe571dbd5   splunk/splunk:latest   "/sbin/entrypoint.sh…"   6 minutes ago   Exited (1) 6 minutes ago             splunk
License not accepted, please adjust SPLUNK_GENERAL_TERMS and/or SPLUNK_START_ARGS to indicate you have accepted the current/latest version of the license.
The license you are accepting is the current/latest version of the Splunk General Terms, available here: https://www.splunk.com/en_us/legal/splunk-general-terms.html, as may be updated from time to time.
Unless you have jointly executed with Splunk a negotiated version of these General Terms that explicitly supersedes this agreement, by accessing or using Splunk software, you are agreeing to the Splunk General Terms posted at the time of your access and use and acknowledging its applicability to the Splunk software.
Please read and make sure you agree to the Splunk General Terms before you access or use this software.
Only after doing so should you include the '--accept-sgt-current-at-splunk-com' and '--accept-license' flags to indicate your acceptance of the Splunk General Terms and launch this software.
For example: docker run -e SPLUNK_GENERAL_TERMS=--accept-sgt-current-at-splunk-com -e SPLUNK_START_ARGS=--accept-license -e SPLUNK_PASSWORD splunk/splunk

For additional information and examples, see the help: docker run -it splunk/splunk help
splunk
mcqueen@mcqueen-Dell-G15-5511:~$ # Remove the failed container
docker rm splunk

# Run with proper license acceptance
docker run -d \
  --name splunk \
  -p 8000:8000 \
  -p 8088:8088 \
  -p 8089:8089 \
  -e SPLUNK_START_ARGS="--accept-license" \
  -e SPLUNK_GENERAL_TERMS="--accept-sgt-current-at-splunk-com" \
  -e SPLUNK_PASSWORD="admin12345" \
  splunk/splunk:latest
splunk
ea76f4a161c933f91a0d34e13f1cb96c55859c7e594e8c62a8a8cd3cd8b30a33
mcqueen@mcqueen-Dell-G15-5511:~$ docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS                             PORTS                                                                                                                                                  NAMES
ea76f4a161c9   splunk/splunk:latest   "/sbin/entrypoint.sh…"   11 seconds ago   Up 10 seconds (health: starting)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp, 8065/tcp, 8191/tcp, 9887/tcp, 0.0.0.0:8088-8089->8088-8089/tcp, [::]:8088-8089->8088-8089/tcp, 9997/tcp   splunk
mcqueen@mcqueen-Dell-G15-5511:~$ docker exec -it splunk bash
[ansible@ea76f4a161c9 splunk]$ /opt/splunk/bin/splunk http-event-collector list

Warning: cannot create "/opt/splunk/var/log/splunk"

Warning: cannot create "/opt/splunk/var/log/introspection"

Warning: cannot create "/opt/splunk/var/log/watchdog"

Warning: cannot create "/opt/splunk/var/log/client_events"
Splunk server uri is missing
[ansible@ea76f4a161c9 splunk]$

aste_classifier.pth
2025-11-02 02:27:44,708 - waste_management_backend - INFO - main - <module> - Model instance initialized successfully.
INFO:     Started server process [35082]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
2025-11-02 02:29:14,571 - waste_management_backend - INFO - main - health_check - Health check requested.
INFO:     127.0.0.1:46726 - "GET / HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'backend/utils/logger.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [35082]
2025-11-02 02:32:21,508 - waste_management_backend - INFO - logger - <module> - Logger initialized successfully.
2025-11-02 02:32:21,509 - waste_management_backend - INFO - efficientnet_model - __init__ - Loaded 4 classes from model/class_labels.json
2025-11-02 02:32:21,621 - waste_management_backend - INFO - efficientnet_model - __init__ - Device selected: cuda
2025-11-02 02:32:21,905 - waste_management_backend - INFO - efficientnet_model - __init__ - Model loaded successfully from model/efficientnet_b0_waste_classifier.pth
2025-11-02 02:32:21,905 - waste_management_backend - INFO - main - <module> - Model instance initialized successfully.
INFO:     Started server process [43357]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
^CINFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [43357]
INFO:     Stopping reloader process [35077]
(venv) mcqueen@mcqueen-Dell-G15-5511:~/Documents/waste-management-ml$ uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
INFO:     Will watch for changes in these directories: ['/home/mcqueen/Documents/waste-management-ml']
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [44711] using StatReload
2025-11-02 02:32:37,177 - waste_management_backend - INFO - logger - <module> - Logger initialized successfully.
2025-11-02 02:32:37,178 - waste_management_backend - INFO - efficientnet_model - __init__ - Loaded 4 classes from model/class_labels.json
2025-11-02 02:32:37,285 - waste_management_backend - INFO - efficientnet_model - __init__ - Device selected: cuda
2025-11-02 02:32:37,589 - waste_management_backend - INFO - efficientnet_model - __init__ - Model loaded successfully from model/efficientnet_b0_waste_classifier.pth
2025-11-02 02:32:37,589 - waste_management_backend - INFO - main - <module> - Model instance initialized successfully.
INFO:     Started server process [44715]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
2025-11-02 02:32:46,844 - waste_management_backend - INFO - main - health_check - Health check requested.
INFO:     127.0.0.1:41484 - "GET / HTTP/1.1" 200 OK
2025-11-02 02:33:56,325 - waste_management_backend - INFO - main - health_check - Health check requested.
INFO:     127.0.0.1:38994 - "GET / HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'backend/utils/logger.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [44715]
2025-11-02 02:36:57,149 - waste_management_backend - INFO - logger - <module> - Logger initialized successfully.
2025-11-02 02:36:57,150 - waste_management_backend - INFO - efficientnet_model - __init__ - Loaded 4 classes from model/class_labels.json
2025-11-02 02:36:57,258 - waste_management_backend - INFO - efficientnet_model - __init__ - Device selected: cuda
2025-11-02 02:36:57,506 - waste_management_backend - INFO - efficientnet_model - __init__ - Model loaded successfully from model/efficientnet_b0_waste_classifier.pth
2025-11-02 02:36:57,507 - waste_management_backend - INFO - main - <module> - Model instance initialized successfully.
INFO:     Started server process [50293]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
^CINFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [50293]
INFO:     Stopping reloader process [44711]
(venv) mcqueen@mcqueen-Dell-G15-5511:~/Documents/waste-management-ml$ Skip Navigation >
Apps
Administrator
1Messages
Settings
Activity
Help
Find
Add Data
Select Source
Input Settings
Review
Done
 Back Next
Token has been created successfully.
Configure your inputs by going to Settings > Data Inputs

Token Value
eb6ba566-abfb-4640-bbe6-8d8c183e5132
Start Searching Search your data now or see examples and tutorials.
Add More Data Add more data inputs now or see examples and tutorials.
Download Apps Apps help you do more with your data. Learn more.
Build Dashboards Visualize your searches. Learn more.^C
(venv) mcqueen@mcqueen-Dell-G15-5511:~/Documents/waste-management-ml$ uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
INFO:     Will watch for changes in these directories: ['/home/mcqueen/Documents/waste-management-ml']
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [50842] using StatReload
2025-11-02 02:37:28,625 - waste_management_backend - INFO - logger - <module> - Logger initialized successfully.
2025-11-02 02:37:28,626 - waste_management_backend - INFO - efficientnet_model - __init__ - Loaded 4 classes from model/class_labels.json
2025-11-02 02:37:30,071 - waste_management_backend - INFO - efficientnet_model - __init__ - Device selected: cuda
2025-11-02 02:37:30,318 - waste_management_backend - INFO - efficientnet_model - __init__ - Model loaded successfully from model/efficientnet_b0_waste_classifier.pth
2025-11-02 02:37:30,318 - waste_management_backend - INFO - main - <module> - Model instance initialized successfully.
INFO:     Started server process [50844]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
2025-11-02 02:37:37,843 - waste_management_backend - INFO - main - health_check - Health check requested.
INFO:     127.0.0.1:39884 - "GET / HTTP/1.1" 200 OK
2025-11-02 02:37:40,677 - waste_management_backend - INFO - main - health_check - Health check requested.
INFO:     127.0.0.1:39900 - "GET / HTTP/1.1" 200 OK
2025-11-02 02:37:41,364 - waste_management_backend - INFO - main - health_check - Health check requested.
INFO:     127.0.0.1:39916 - "GET / HTTP/1.1" 200 OK
        ^CINFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [50844]
INFO:     Stopping reloader process [50842]
(venv) mcqueen@mcqueen-Dell-G15-5511:~/Documents/waste-management-ml$
 *  History restored

mcqueen@mcqueen-Dell-G15-5511:~/Documents/waste-management-ml$
 *  History restored

mcqueen@mcqueen-Dell-G15-5511:~/Documents/waste-management-ml$ source .venv/bin/a
activate  ___.csh   ___.fish  ___.ps1
mcqueen@mcqueen-Dell-G15-5511:~/Documents/waste-management-ml$ source .venv/bin/activate
(.venv) mcqueen@mcqueen-Dell-G15-5511:~/Documents/waste-management-ml$ uvicorn backend.main:app --reload
INFO:     Will watch for changes in these directories: ['/home/mcqueen/Documents/waste-management-ml']
ERROR:    [Errno 98] Address already in use
(.venv) mcqueen@mcqueen-Dell-G15-5511:~/Documents/waste-management-ml$ uvicorn backend.main:app --reload --port 8001
INFO:     Will watch for changes in these directories: ['/home/mcqueen/Documents/waste-management-ml']
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [72535] using StatReload
2025-11-03 14:33:43,002 | INFO | WasteManagementBackend | logger | <module> | ✅ Splunk logging enabled.
2025-11-03 14:33:43,002 | INFO | WasteManagementBackend | logger | <module> | Logger initialized successfully.
2025-11-03 14:33:43,004 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Loaded 4 classes from model/class_labels.json
2025-11-03 14:33:44,475 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Using device: cuda
2025-11-03 14:33:44,827 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Model loaded successfully from model/efficientnet_b0_waste_classifier.pth
2025-11-03 14:33:44,827 | INFO | WasteManagementBackend | main | <module> | ✅ Model initialized successfully.
INFO:     Started server process [72543]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
2025-11-03 14:33:46,611 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:47350 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:47350 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:47350 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:47350 - "GET /openapi.json HTTP/1.1" 200 OK
2025-11-03 14:35:11,846 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38328 - "GET / HTTP/1.1" 200 OK
2025-11-03 14:35:12,992 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38328 - "GET / HTTP/1.1" 200 OK
2025-11-03 14:35:13,695 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38328 - "GET / HTTP/1.1" 200 OK
2025-11-03 14:35:14,031 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38328 - "GET / HTTP/1.1" 200 OK
2025-11-03 14:35:14,198 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38328 - "GET / HTTP/1.1" 200 OK
2025-11-03 14:35:14,339 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38328 - "GET / HTTP/1.1" 200 OK
2025-11-03 14:35:14,496 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38328 - "GET / HTTP/1.1" 200 OK
2025-11-03 14:35:14,675 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38328 - "GET / HTTP/1.1" 200 OK
WARNING:  StatReload detected changes in 'backend/utils/logger.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [72543]
2025-11-03 14:38:55,588 | INFO | WasteManagementBackend | logger | <module> | ✅ Splunk logging enabled.
2025-11-03 14:38:55,588 | INFO | WasteManagementBackend | logger | <module> | Logger initialized successfully.
2025-11-03 14:38:55,589 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Loaded 4 classes from model/class_labels.json
2025-11-03 14:38:55,703 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Using device: cuda
2025-11-03 14:38:56,013 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Model loaded successfully from model/efficientnet_b0_waste_classifier.pth
2025-11-03 14:38:56,013 | INFO | WasteManagementBackend | main | <module> | ✅ Model initialized successfully.
INFO:     Started server process [78210]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/utils/logger.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [78210]
2025-11-03 14:39:14,861 | WARNING | WasteManagementBackend | logger | <module> | ⚠️ Failed to initialize Splunk handler: SplunkHandler.__init__() missing 1 required positional argument: 'index'
2025-11-03 14:39:14,861 | INFO | WasteManagementBackend | logger | <module> | Logger initialized successfully.
2025-11-03 14:39:14,862 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Loaded 4 classes from model/class_labels.json
2025-11-03 14:39:14,977 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Using device: cuda
2025-11-03 14:39:15,285 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Model loaded successfully from model/efficientnet_b0_waste_classifier.pth
2025-11-03 14:39:15,286 | INFO | WasteManagementBackend | main | <module> | ✅ Model initialized successfully.
INFO:     Started server process [78593]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/utils/logger.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [78593]
2025-11-03 14:40:54,446 | WARNING | WasteManagementBackend | logger | <module> | ⚠️ Failed to initialize Splunk handler: SplunkHandler.__init__() missing 3 required positional arguments: 'host', 'port', and 'index'
2025-11-03 14:40:54,446 | INFO | WasteManagementBackend | logger | <module> | Logger initialized successfully.
2025-11-03 14:40:54,446 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Loaded 4 classes from model/class_labels.json
2025-11-03 14:40:54,558 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Using device: cuda
2025-11-03 14:40:54,857 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Model loaded successfully from model/efficientnet_b0_waste_classifier.pth
2025-11-03 14:40:54,857 | INFO | WasteManagementBackend | main | <module> | ✅ Model initialized successfully.
INFO:     Started server process [79938]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  StatReload detected changes in 'backend/utils/logger.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [79938]
2025-11-03 14:41:40,528 | INFO | WasteManagementBackend | logger | <module> | ✅ Splunk logging enabled (HEC connected).
2025-11-03 14:41:40,528 | INFO | WasteManagementBackend | logger | <module> | Logger initialized successfully.
2025-11-03 14:41:40,529 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Loaded 4 classes from model/class_labels.json
2025-11-03 14:41:40,661 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Using device: cuda
2025-11-03 14:41:40,968 | INFO | WasteManagementBackend | efficientnet_model | __init__ | Model loaded successfully from model/efficientnet_b0_waste_classifier.pth
2025-11-03 14:41:40,968 | INFO | WasteManagementBackend | main | <module> | ✅ Model initialized successfully.
INFO:     Started server process [80558]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:38840 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:38840 - "GET /openapi.json HTTP/1.1" 200 OK
2025-11-03 14:41:54,272 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38840 - "GET / HTTP/1.1" 200 OK
2025-11-03 14:41:55,341 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38840 - "GET / HTTP/1.1" 200 OK
2025-11-03 14:41:56,218 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38840 - "GET / HTTP/1.1" 200 OK
2025-11-03 14:41:56,406 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38840 - "GET / HTTP/1.1" 200 OK
2025-11-03 14:41:56,560 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38840 - "GET / HTTP/1.1" 200 OK
2025-11-03 14:41:56,733 | INFO | WasteManagementBackend | main | health_check | Health check called.
INFO:     127.0.0.1:38840 - "GET / HTTP/1.1" 200 OK

 eval $(minikube docker-env)

 docker build -t waste-backend:latest .

 kubectl apply -f k8s/backend-deployment.yaml

 ✅ Fix Options
Option 1 — Use Minikube’s gateway IP (Recommended for Linux)

Run on your host:

minikube ssh


Then inside that VM:

ip route | grep default


You’ll see something like:

default via 192.168.49.1 dev eth0


That 192.168.49.1 is the host IP from Minikube’s perspective.
So your backend pod should talk to Splunk using that.

Your Python code already defaults to:

SPLUNK_HEC_HOST = "192.168.49.1"


So simply change the env in your Deployment YAML back to:

- name: SPLUNK_HEC_HOST
  value: "192.168.49.1"


Then apply:

kubectl apply -f backend-deployment.yaml