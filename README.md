# cassandra-operator

## Description

This is the Cassandra charm for Kubernetes using the Python Operator Framework.

## Usage


### Deploying

```
$ git clone https://github.com/martinrusev/cassandra-operator
$ cd cassandra-operator

$ sudo snap install charmcraft --beta
$ charmcraft build
Created 'cassandra.charm'.


$ juju deploy ./cassandra.charm --resource cassandra-image=bitnami/cassandra:3.11.10

$ juju status
Model    Controller  Cloud/Region        Version  SLA          Timestamp
cassandra  pebble      microk8s/localhost  2.9-rc7  unsupported  16:36:06+01:00

App      Version  Status  Scale  Charm      Store  Channel  Rev  OS      Address  Message
cassandra         active      1  cassandra  local             1  ubuntu           cassandra started

Unit        Workload  Agent  Address       Ports  Message
cassandra/0*  active    idle   10.1.243.208         cassandra started
```

Visit that IP address at port 9042 in your browser and you should see the cassandra web UI. For example, http://10.1.243.208:9042/


## Developing

Create and activate a virtualenv with the development requirements:

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

```
./run_tests
```
