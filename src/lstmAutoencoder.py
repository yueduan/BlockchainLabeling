import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed


# node_txs_mapping[idx] = [list of txs]
# idx starts from 0
node_txs_mapping = {}

# max limit of tx numbers of one address
max_tx = 10000

# feature_size
feature_size = 7


# if tx_number exceeds max_tx, slice the list. But if tx_number is less than max_tx, we fill the list using [0] * feature_size
def adjust_tx_num(tx_list):
    return tx_list[:max_tx] + [[0] * feature_size] * (max_tx - len(tx_list))


def readFeatureVectors(filepath, max_tx):
    curr_max_tx = 0
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            line = line.strip()
            if ":" in line:
                idx_txnum = line.split(':') 
                idx = int(idx_txnum[0])
                txnum = int(idx_txnum[1])

                if curr_max_tx < txnum:
                    curr_max_tx = txnum
                
                txs = []
                for _ in range(txnum):
                    line = fp.readline().strip()
                    tx = [int(s) for s in line.split(' ')]
                    txs.append(tx)
                
                node_txs_mapping[idx] = txs

            line = fp.readline()
    
    if curr_max_tx < max_tx:
        return curr_max_tx
    else:
        return max_tx



# This function adjusts the length of tx list for each address in the blockchain
def adjust_length():
    for key in node_txs_mapping:
        txs = node_txs_mapping[key]
        txs = adjust_tx_num(txs)
        node_txs_mapping[key] = txs


# generate np.array for lstmAutoencoder
def reshape_to_nparray():
    adjust_length()
    array = [] #np.array(len(node_txs_mapping), max_tx, feature_size)
    for i in range(len(node_txs_mapping)):
        if i in node_txs_mapping:
            array.append(node_txs_mapping[i])
    return np.asarray(array)





def lstmAutoEncoder(input_array):
    # define model
    model = Sequential()
    model.add(LSTM(128, activation='relu', input_shape=(max_tx,feature_size), return_sequences=True))
    model.add(LSTM(64, activation='relu', return_sequences=False))
    model.add(RepeatVector(max_tx))
    model.add(LSTM(64, activation='relu', return_sequences=True))
    model.add(LSTM(128, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(feature_size)))
    model.compile(optimizer='adam', loss='mse')
    model.summary()


    # fit model
    model.fit(input_array, input_array, epochs=300, batch_size=5, verbose=0)
    # demonstrate reconstruction
    yhat = model.predict(input_array, verbose=0)



max_tx = readFeatureVectors("/home/yueduan/yueduan/feature", max_tx)
input_array = reshape_to_nparray()
print(input_array.shape())
lstmAutoEncoder(input_array)