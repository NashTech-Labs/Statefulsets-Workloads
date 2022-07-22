### Install Kubernetes Python Client:

`git clone --recursive https://github.com/kubernetes-client/python.git cd`

`cd python`

`python setup.py install`

### Installation from pip:

`pip install kubernetes`

For Statefulsets, we use AppsV1Api class from client module.


### Authentication to the Kubernetes Python Client in other cluster is done by: 

`configuration.api_key = {"authorization": "Bearer" + bearer_token}`

We will use here the Bearer Token which enable requests to authenticate using an access key.

In update.py file there is a functions for updating Statefulset:

1. Create Statefulsets

In this we have to pass the namespace in which we will update Statefulsets:
namespace="default"

Give your cluster details:
```
cluster_details={
        "bearer_token":"Your_cluster_bearer_token",
        "api_server_endpoint":"Your_cluster_IP"
    }
```

### Running the File:
```
python3 create.py
```

### Check the Statefulset:
```
kubectl get statefulset
```

2. Update Statefulsets

In this we have to pass the namespace in which we will update Statefulsets:
namespace="default"

Give your cluster details:
```
cluster_details={
        "bearer_token":"Your_cluster_bearer_token",
        "api_server_endpoint":"Your_cluster_IP"
    }
```

### Running the File:
```
python3 update.py
```

### Check the Statefulsets:
```
kubectl get statefulset
```