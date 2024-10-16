# Neurosurgeon
💻 Welcome to all students working in the field of cloud-edge collaboration to engage in discussions.

💻 If there are any bugs in the code, please raise an issue, and I will try my best to improve it.

🥳 This project is implemented based on the classic paper: "Neurosurgeon: Collaborative Intelligence Between the Cloud and Mobile Edge." After selecting partition points for DNN models, they are deployed on cloud and edge devices for collaborative inference.

Paper link🔗：https://github.com/Tjyy-1223/Neurosurgeon/blob/main/paper/Collaborative_Intelligence%20Between_the_Cloud_and_Mobile_Edge.pdf

![image-20230524094940267.png](https://github.com/Tjyy-1223/Neurosurgeon/blob/main/assets/image-20230524094940267.png?raw=true)

Specific work:

1) Initially build using four classic DNN models.

2) Study the characteristics of DNN model layers: Layer latency and size of output data.

3) Deployment Phase: Run DNN layers on a local machine to build prediction models and provide model parameters.

4) Runtime Phase: Implement collaborative inference for DNN models. Refer to the script commands described below.

**Model parameters are provided in the project and can be directly cloned and run locally.**

## Project structure

```python
Neurosurgeon
├── cloud_api.py # Simulate cloud device entry point
├── deployment.py # Deployment phase
├── edge_api.py # Simulate edge device entry point
├── models # DNN models used
│   ├── AlexNet.py
│   ├── LeNet.py
│   ├── MobileNet.py
│   └── VggNet.py
├── net # Network module
│   ├── net_utils.py # Network utility methods
│   ├── monitor_client.py # Bandwidth monitor client
│   └── monitor_server.py # Bandwidth monitor server
│   └── monitor_test.py # Bandwidth monitor test service
├── predictor # Predictor module
│   ├── config # Model parameters
│   │   ├── cloud
│   │   └── edge
│   ├── dataset # Collect dataset for six different DNN layers
│   │   ├── cloud
│   │   └── edge
│   ├── get_datasets_func.py # Process of reading datasets
│   ├── kernel_flops.py 
│   └── predictor_utils.py # Predictor utilities
└── utils # Other tools
    ├── excel_utils.py # Excel spreadsheet operations
    └── inference_utils.py # Collaborative inference functions

```

## Operating environment

```
python 3.9
torch==1.9.0.post2
torchvision==0.10.0
xlrd==2.0.1
apscheduler
```

## Project Execution 

### single task mode 

+ **Typically used to evaluate performance improvements in DNN inference latency: Each time, tasks need to be provided to the client through instructions.**
+ **Bandwidth data is monitored once before each inference**

Run on the cloud device: You can modify the server’s open IP and port; -d indicates whether the cloud uses CPU or GPU: input parameters are "cpu" or "cuda."

```
 python cloud_api.py -i 127.0.0.1 -p 9999 -d cpu
```

Run on the edge device: -i and -d represent the server's open IP and port; -d indicates whether the edge uses CPU or GPU: input parameters are "cpu" or "cuda."

```
# -t represents the model type. The input parameters can be "alex_net", "vgg_net", "le_net", "mobilenet"
python edge_api.py -i 127.0.0.1 -p 9999 -d cpu -t vgg_net
```

**The results of stand-alone operation are as follows:**

**Cloud device:** python cloud_api.py -i 127.0.0.1 -p 9999 -d cpu
```
successfully connection :<socket.socket fd=6, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 9999), raddr=('127.0.0.1', 64595)>
get model type successfully.
get partition point successfully.
get edge_output and transfer latency successfully.
short message , transfer latency has been sent successfully
short message , cloud latency has been sent successfully
================= DNN Collaborative Inference Finished. ===================
```

**Edge device:** python edge_api.py -i 127.0.0.1 -p 9999 -d cpu -t alex_net

```
(tjyy) tianjiangyu@tianjiangyudeMacBook-Pro Neurosurgeon % python edge_api.py -i 127.0.0.1 -p 9999 -d cpu -t alex_net
get bandwidth value : 3259.5787388244685 MB/s
best latency : 10.07 ms , best partition point : 0 - None
----------------------------------------------------------------------------------------------------------
short message , model type has been sent successfully
short message , partition strategy has been sent successfully
alex_net inference completed on the edge device - 0.072 ms
get yes , edge output has been sent successfully
alex_net transmission completed - 0.129 ms
alex_net inference completed on the cloud device - 34.621 ms
================= DNN Collaborative Inference Finished. ===================
```



### Multi-task Mode


+ After tasks_cloud_api.py starts: Two processes are launched (on two different ports), one to wait for tasks sent from the edge device, and the other to periodically collect bandwidth data.
+ After tasks_edge_api.py starts: Responsible for fetching different DNN inference tasks from the queue one by one and performing inference using cloud-edge collaborative computing.


**Design Details:**

+ Uses BackgroundScheduler for asynchronous scheduling, which does not block the main process. It schedules tasks in the background and monitors the bandwidth every 1 second.
+ The edge device continuously fetches tasks from the queue and performs edge-side inference based on the current bandwidth conditions.
+ The cloud device completes the remaining half of the inference tasks.


Edge device runs：python tasks_edge_api.py -i 127.0.0.1 -p 9999 -d cpu

```
tasks list info : ['le_net', 'mobile_net', 'le_net', 'alex_net', 'vgg_net', 'vgg_net', 'vgg_net', 'le_net', 'mobile_net', 'mobile_net', 'alex_net', 'vgg_net', 'mobile_net', 'vgg_net', 'alex_net', 'alex_net', 'alex_net', 'le_net', 'alex_net', 'vgg_net', 'mobile_net', 'vgg_net', 'alex_net', 'le_net', 'vgg_net', 'vgg_net', 'le_net', 'alex_net', 'vgg_net', 'mobile_net', 'mobile_net', 'alex_net', 'alex_net', 'vgg_net', 'vgg_net', 'le_net', 'le_net', 'le_net', 'vgg_net', 'mobile_net']
===================== start inference tasks ===================== 
get bandwidth value : 7152.80666553514 MB/s
get model type: le_net 
best latency : 88.77 ms , best partition point : 0 - None
----------------------------------------------------------------------------------------------------------
short message, model type has been sent successfully
short message, partition strategy has been sent successfully
le_net inference completed on the edge device - 0.001 ms
get yes, edge output has been sent successfully
le_net transmission completed - 0.098 ms
le_net inference completed on the cloud device - 17.468 ms
================= DNN Collaborative Inference Finished. ===================
get bandwidth value: 7152.80666553514 MB/s
get model type: mobile_net
best latency: 115.15 ms, best partition point: 0 - None
----------------------------------------------------------------------------------------------------------
short message, model type has been sent successfully
short message, partition strategy has been sent successfully
mobile_net inference completed on the edge device - 0.001 ms
get yes, edge output has been sent successfully
mobile_net transmission completed - 0.254 ms
mobile_net inference completed on the cloud device - 103.763 ms
================= DNN Collaborative Inference Finished. ===================
.....
```

Cloud device runs：python tasks_cloud_api.py -i 127.0.0.1 -p 9999 -d cpu

```
successfully connection :<socket.socket fd=6, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 9999), raddr=('127.0.0.1', 50656)>
get model type successfully.
get partition point successfully.
get edge_output and transfer latency successfully.
short message , transfer latency has been sent successfully
short message , cloud latency has been sent successfully
================= DNN Collaborative Inference Finished. ===================
successfully connection :<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 9999), raddr=('127.0.0.1', 50661)>
get model type successfully.
get partition point successfully.
get edge_output and transfer latency successfully.
short message , transfer latency has been sent successfully
short message , cloud latency has been sent successfully
================= DNN Collaborative Inference Finished. ===================
...
```



## Conclusion

Neurosurgeon is an excellent framework for cloud-edge collaborative inference, being the first to implement the deployment of DNN models across cloud and edge devices for collaborative inference.

However, it has certain limitations:

+ It is only applicable to chain topologies.
+ It does not consider multi-level structures of models or various DAG topologies — see how DADS solves this; the DADS framework will be reproduced later.
+ It only considers partitioning under static network conditions — see the CAS paper for how to address dynamic network conditions.
+ Optimizing task scheduling under high-load tasks is also a key consideration.

Potential Improvements:

+ Linear regression is not very accurate — how to improve the predictor’s performance to precisely predict the inference latency of DNN layers ✅ (due to limited data collection).
+ Multi-process mode is already used: before the main inference task, a new process is started to send data and obtain network bandwidth ✅.
+ Pay attention to the packet sticking problem during communication ✅ (there are minimal bugs).

## Discussion

If you have better ideas or want to discuss this project, feel free to raise an issue on GitHub.