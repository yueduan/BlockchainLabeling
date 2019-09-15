from bq_helper import BigQueryHelper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
#%matplotlib inline
plt.style.use('ggplot')
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})

query = """
SELECT 
  block_timestamp,
  from_address,
  to_address,
  value,
  receipt_contract_address,
  receipt_status,
  block_number
FROM
  `bigquery-public-data.ethereum_blockchain.transactions` AS transactions
WHERE TRUE
  AND block_timestamp < '2017-01-01 00:00:00'
"""
# This establishes an authenticated session and prepares a reference to the dataset that lives in BigQuery.
bq_assistant = BigQueryHelper("bigquery-public-data", "ethereum_blockchain")
print("estimated query data size: " + str(bq_assistant.estimate_query_size(query)))


df = bq_assistant.query_to_pandas_safe(query, max_gb_scanned=60)


df.to_csv("/home/yueduan/yueduan/postdoc_study/ether_transactions_before2017.csv")


# # Import dataset from big query
# from google.cloud import bigquery
# from bq_helper import BigQueryHelper
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
# #%matplotlib inline
# plt.style.use('ggplot')
# sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})

# # This establishes an authenticated session and prepares a reference to the dataset that lives in BigQuery.
# bq_assistant = BigQueryHelper("bigquery-public-data", "ethereum_blockchain")


# query = """
# SELECT 
#   value,
#   timestamp
# FROM
#   `bigquery-public-data.ethereum_blockchain.transactions` AS transactions,
#   `bigquery-public-data.ethereum_blockchain.blocks` AS blocks
# WHERE TRUE
#   AND transactions.block_number = blocks.number
#   AND receipt_status = 1
#   AND value > 0
#   AND timestamp >= '2016-01-01 00:00:00'
#   AND timestamp < '2018-01-10 00:00:00'
# """

# print("estimated query data size: " + str(bq_assistant.estimate_query_size(query)))

# df = bq_assistant.query_to_pandas_safe(query, max_gb_scanned=15)
# df.to_csv("etc.csv")
# # f, g = plt.subplots(figsize=(12, 9))
# # g = sns.lineplot(x="timestamp", y="value", data=df, palette="Blues_d")
# # plt.title("transaction value over time")
# # plt.show(g)