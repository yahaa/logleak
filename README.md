# Logleak
Use ansible script to check whether the container stdout log is written too fast on the kubernetes cluster.

### Before you begin
* You need to have a Kubernetes cluster and you can access it as an admin.
* You need to have a central control node with ansible installed and it can access the node of your Kubernetes cluster without password.

### Usage
```bash
$ git clone github.com/yahaa/logleak

$ cd log_leak

$ pip install -r requirements.txt

$ ansible -i inventory.txt all -m script -a 'logleak.py' | grep -v stdout| grep  "leak container" | sed 's/\"//g;s/leak container: //g;s/,//g' | awk '{print $1}'| python central.py
```

### Explain
* `logleak.py` Use to run as agent script on each node of the Kubernetes cluster.
* `central.py` Use to run in central node.