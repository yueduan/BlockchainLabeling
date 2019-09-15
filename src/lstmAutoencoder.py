import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed


# node_txs_mapping[idx] = [list of txs]
node_txs_mapping = {}


def readFeatureVectors(filepath):
    max_tx = 0
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            line = line.strip()
            if ":" in line:
                idx_txnum = line.split(':') 
                idx = int(idx_txnum[0])
                txnum = int(idx_txnum[1])
                print(txnum)
                if max_tx < txnum:
                    max_tx = txnum
                
                txs = []
                for i in range(txnum):
                    line = fp.readline().strip()
                    tx = [int(s) for s in line.split(' ')]
                    txs.append(tx)
                
                node_txs_mapping[idx] = txs

            line = fp.readline()
    return max_tx


max_tx = readFeatureVectors("/home/yueduan/yueduan/feature")
print(len(node_txs_mapping))
print(max_tx)





def lstmAutoEncoder():
    timesteps = 10000
    n_features = 7
    X = np.random.rand(100000, timesteps, n_features)

    # define model
    model = Sequential()
    model.add(LSTM(128, activation='relu', input_shape=(timesteps,n_features), return_sequences=True))
    model.add(LSTM(64, activation='relu', return_sequences=False))
    model.add(RepeatVector(timesteps))
    model.add(LSTM(64, activation='relu', return_sequences=True))
    model.add(LSTM(128, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(n_features)))
    model.compile(optimizer='adam', loss='mse')
    model.summary()


    # fit model
    model.fit(X, X, epochs=300, batch_size=5, verbose=0)
    # demonstrate reconstruction
    yhat = model.predict(X, verbose=0)
    print('---Predicted---')
    print(np.round(yhat,3))
    print('---Actual---')
    print(np.round(X, 3))

