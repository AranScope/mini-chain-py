# mini-chain-py
Mini chain is a basic blockchain project, without proof of work.
Currently there is a single peer node that exposes a flask REST api
for interacting with the blockchain.

Support for multiple peers and chain replacement will be added shortly.

## Running without docker
```Bash
pip3 install -r requirements.txt
python3 run.py
```

## Running with docker
```Docker
docker build -f Dockerfile -t mini-chain-py:latest .
docker run --rm -ti -p 8000:8000 mini-chain-py:latest
```

## Querying the chain
```Bash
# get the latest full chain
curl http://localhost:8000/chain

# get a block by it's index in the chain
# in this case, the genesis block
curl http://localhost:8000/block/0

# add a new block to the chain
curl -H "Content-Type: application/json" -X POST -d '{"data":"look Im in the chain"}' http://localhost:8000/chain/add
```