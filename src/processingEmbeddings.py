import numpy as np
from scipy.spatial import distance

embedding_file = "/home/yueduan/yduan005@ucr.edu/Postdoc_study/BlockChainLabeling/G_0101_0110_embed.embeddings"

# read the embedding file
def ebd_file_to_dic(embedding_file):
    ebd_list = np.loadtxt(embedding_file)
    ebd_dic = {}
    feature_dim = len(ebd_list[0]) - 1
    for ebd in ebd_list:
        ebd_dic[int(ebd[0])] = ebd[1:]
    return ebd_dic, feature_dim


# similarity function cosine as default
def similarity(vec, ebd_dic):
    results = []
    for i in range(len(ebd_dic)):
        result = 1 - distance.cosine(vec, ebd_dic[i])
        #print(result)
        results.append(result)
    return results



ebd_dic, feature_dim = ebd_file_to_dic(embedding_file)
print(feature_dim)

ebd_mat = []
node_map = {}
#func_map = {}
for idx, line in ebd_dic.items():
    ebd_mat.append(line)
    node_map[str(idx)] = len(ebd_mat) - 1



ebd_array = np.array(ebd_mat)
print(ebd_dic[15571])
sim_result = similarity(ebd_dic[15571], ebd_dic)

sim_array = np.array(sim_result)
print(np.argsort(sim_array))