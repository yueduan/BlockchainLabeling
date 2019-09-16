import os

tx_file = "/home/yueduan/yueduan/txs_7179343_7281000"
graph_file = "/home/yueduan/yueduan/graph.edgelist"
node_index_mapping_file = "/home/yueduan/yueduan/node_idx_mapping"

feature_file = "/home/yueduan/yueduan/feature"

# store the mapping between address (hash) and its node index in the graph
addressToIndex = {}

# store the mapping between node index and the outgoing txs 
indexToTxs = {}

# One tx record now contains 11 elements: 
# 0: from_addr
# 1: to_addr
# 2: nonce
# 3: value
# 4: timestamp
# 5: gasPrice
# 6: gas
# 7: input content
# 8: status
# 9: contractAddress
# 10: gasUsed

# only return numeric values so far, including nonce, value, timestamp, gasPrice, gas, status, gasUsed
def returnTxStr(tx):
    return str(tx[2]) + " " + str(tx[3]) + " " + str(tx[4]) + " " + str(tx[5]) + " " + str(tx[6])  + " " + str(tx[8])  + " " + str(tx[10]) + "\n"
    #str(tx[0]) + " " + str(tx[1]) + " " + str(tx[2]) + " " + str(tx[3]) + " " + str(tx[4]) + " " + str(tx[5]) + " " + str(tx[6]) + " " + str(tx[7])  + " " + str(tx[8])  + " " + str(tx[9])  + " " + str(tx[10]) + "\n"



def generateGraphEdgelist(alltxs):
    curr_idx = 0
    with open(graph_file, 'w') as gf:
        for txhash in alltxs:
            tx = alltxs[txhash]

            if tx[0] not in addressToIndex:
                addressToIndex[tx[0]] = curr_idx
                curr_idx += 1
            if tx[1] not in addressToIndex:
                addressToIndex[tx[1]] = curr_idx
                curr_idx += 1

            gf.write(str(addressToIndex[tx[0]]) + " " + str(addressToIndex[tx[1]]) + "\n")

    with open(node_index_mapping_file, 'w') as nimf:
        for addr in addressToIndex:
            nimf.write(str(addressToIndex[addr]) + ":" + addr + "\n")


def generateFeatures(alltxs):
    with open(feature_file, 'w') as ff:
        #ff.write("from_addr\tto_addr\tnonce\tvalue\ttimestamp\tgasPrice\tgas\tic\tstatus\tcontractAddress\tgasUsed")

        for txhash in alltxs:
            tx = alltxs[txhash]

            from_addr_idx = addressToIndex[tx[0]]

            if from_addr_idx not in indexToTxs:
                txs = []
                txs.append(tx)
                indexToTxs[from_addr_idx] = txs
                #ff.write("new from_addr:" + str(tx[0]) + "\n")
                #ff.write("\ttx:" + returnTxStr(tx) + "\n")
            else:
                indexToTxs[from_addr_idx].append(tx)
                #ff.write("existing tx:" + returnTxStr(tx) + "\n")
        
        for idx in indexToTxs:
            txs = indexToTxs[idx]
            ff.write(str(idx) + ":" + str(len(txs)) + "\n")

            for tx in txs:
                ff.write(returnTxStr(tx))
            ff.write("\n")
    


def main():
    alltxs = {}

    with open(tx_file) as txf:
        line = txf.readline()
        while line:
            # each tx takes 12 lines
            for i in range(1, 16):
                linestr = line.strip()
                if i == 1:
                    hash_tx = linestr.split(": ")[1].lower()
                elif i == 2:
                    from_addr = linestr.split(": ")[1].lower()
                elif i == 3:
                    to_addr = linestr.split(": ")[1].lower()
                elif i == 4:
                    nonce = linestr.split(": ")[1].lower()
                # elif i == 5:
                #     blockHash = linestr.split(": ")[1].lower()
                # elif i == 6:
                #     blockNum = linestr.split(": ")[1].lower()
                # elif i == 7:
                #     txIdx = linestr.split(": ")[1].lower()
                elif i == 8:
                    value = linestr.split(": ")[1].lower()
                elif i == 9:
                    timestamp = linestr.split(": ")[1].lower()
                elif i == 10:
                    gasPrice = linestr.split(": ")[1].lower()
                elif i == 11:
                    gas = linestr.split(": ")[1].lower()
                elif i == 12:
                    ic = linestr.split(": ")[1].lower()
                elif i == 13:
                    status = linestr.split(": ")[1].lower()
                    if status == 'true':
                        status = 1
                    else:
                        status = 0
                elif i == 14:
                    contractAddress = linestr.split(": ")[1].lower()
                    if contractAddress == 'undefined':
                        contractAddress = 0
                elif i == 15:
                    gasUsed = linestr.split(": ")[1].lower()
                    if gasUsed == 'undefined':
                        gasUsed = 0
                line = txf.readline()

            # store tx info
            alltxs[hash_tx] = [from_addr, to_addr, nonce, value, timestamp, gasPrice, gas, ic, status, contractAddress, gasUsed]
            #line = txf.readline()

    generateGraphEdgelist(alltxs)
    generateFeatures(alltxs)


if __name__== "__main__":
    main()