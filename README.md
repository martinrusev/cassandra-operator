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


$ juju deploy ./cassandra.charm --resource cassandra-image=cassandra:3.11.10

$ juju status
Model    Controller  Cloud/Region        Version  SLA          Timestamp
cassandra  pebble      microk8s/localhost  2.9-rc7  unsupported  16:36:06+01:00

App      Version  Status  Scale  Charm      Store  Channel  Rev  OS      Address  Message
cassandra         active      1  cassandra  local             1  ubuntu           cassandra started

Unit        Workload  Agent  Address       Ports  Message
cassandra/0*  active    idle   10.1.243.208         cassandra started
```

To access Cassandra, download `cqlsh` from https://downloads.datastax.com/#cqlsh

Create a config file that includes the connection details:

```
$ touch config

# config
[connection]
hostname = 10.1.243.208
port = 9042
```

Access the cluster with:

```
$ cqlsh-astra/bin ❯ ./cqlsh --cqlshrc config                                                                                                                                                                      12m 37s 
Connected to charm-cluster at 10.1.243.223:9042.
[cqlsh 6.8.0 | Cassandra 3.11.10 | CQL spec 3.4.4 | Native protocol v4]
Use HELP for help.
cqlsh>
```


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
