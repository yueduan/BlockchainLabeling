# BlockchainLabeling


This project is to perform unsupervised graph representation learning on top of blockchain graph, where:
	1. each vertex is an blockchain address (normal account or smart contract)
	2. each edge represents a transaction between two addresses

To collect data, we first setup a full node of the blockchain locally, and use web3js to query the data. Then, we perform pre-processing to buildup the graph and extract node and edge information. Finally, we feed information into graph reprensentation learning algorithms to generate embeddings for each node.

NOTE: we now use Ethereum classic blockchain for testing. The two attacker accounts are reported in: https://blog.coinbase.com/ethereum-classic-etc-is-currently-being-51-attacked-33be13ce32de

Steps:
1. maintain a full node

	a. download geth from https://github.com/etclabscore/go-ethereum

	b. build and start it with the option '--rpc'. This will enable the HTTP-RPC server at http://localhost:8545 for web3js.

	c. let it sync for a while (take hours)



2. web3js query for blockchain data

	a. install web3js https://github.com/ethereum/web3.js/

	b. execute queryBlockChain.js in the src directory

	c. store the results somewhere



3. graph generation

	a. modify the input and output file paths at the beginning of preprocessing.py in src directory

	b. execute the python code

	c. transtion information and graph in edgelist format should be generated



4. run LSTM Autoencoder to generate node features

	a. excute lstmAutoencoder.py for node feature generation



5. graph representation learning

	a. two inputs: graph (edgelist) and node feature

	b. run ANRL (https://github.com/cszhangzhen/ANRL) with the two inputs 
