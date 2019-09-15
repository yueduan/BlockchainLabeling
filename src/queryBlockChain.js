const Web3 = require('web3')
const rpcURL = 'http://localhost:8545' // Your RPC URL goes here
const web3 = new Web3(rpcURL)

//const address = '0x8c5535afdbdeea80adedc955420f684931bf91e0' // Your account address goes here

/*
web3.eth.getBlockNumber().then((latest) => {
  for (let i = 0; i < 10; i++) {
    web3.eth.getBlock(latest - i).then(console.log)
  }
})
*/
async function printTransaction(txHash) {
  var tx = await web3.eth.getTransaction(txHash);
  if (tx != null) {
    console.log("  tx hash          : " + tx.hash + "\n"
      + "   nonce           : " + tx.nonce + "\n"
      + "   blockHash       : " + tx.blockHash + "\n"
      + "   blockNumber     : " + tx.blockNumber + "\n"
      + "   transactionIndex: " + tx.transactionIndex + "\n"
      + "   from            : " + tx.from + "\n" 
      + "   to              : " + tx.to + "\n"
      + "   value           : " + tx.value + "\n"
      + "   gasPrice        : " + tx.gasPrice + "\n"
      + "   gas             : " + tx.gas + "\n"
      + "   input           : " + tx.input);
  }
}


function printBlock(block) {
  console.log("Block number     : " + block.number + "\n"
    + " hash            : " + block.hash + "\n"
    + " parentHash      : " + block.parentHash + "\n"
    + " nonce           : " + block.nonce + "\n"
    + " sha3Uncles      : " + block.sha3Uncles + "\n"
    + " logsBloom       : " + block.logsBloom + "\n"
    + " transactionsRoot: " + block.transactionsRoot + "\n"
    + " stateRoot       : " + block.stateRoot + "\n"
    + " miner           : " + block.miner + "\n"
    + " difficulty      : " + block.difficulty + "\n"
    + " totalDifficulty : " + block.totalDifficulty + "\n"
    + " extraData       : " + block.extraData + "\n"
    + " size            : " + block.size + "\n"
    + " gasLimit        : " + block.gasLimit + "\n"
    + " gasUsed         : " + block.gasUsed + "\n"
    + " timestamp       : " + block.timestamp + "\n"
    + " transactions    : " + block.transactions + "\n"
    + " uncles          : " + block.uncles);
    /*
    if (block.transactions != null) {
      console.log("\n--- transactions ---");
      block.transactions.forEach( function(e) {
        printTransaction(e);
      })
      console.log("--- Done transactions ---\n");
    }
    */
}



function printUncle(block, uncleNumber, uncle) {
  console.log("\n\nBlock number     : " + block.number + " , uncle position: " + uncleNumber + "\n"
    + " Uncle number    : " + uncle.number + "\n"
    + " hash            : " + uncle.hash + "\n"
    + " parentHash      : " + uncle.parentHash + "\n"
    + " nonce           : " + uncle.nonce + "\n"
    + " sha3Uncles      : " + uncle.sha3Uncles + "\n"
    + " logsBloom       : " + uncle.logsBloom + "\n"
    + " transactionsRoot: " + uncle.transactionsRoot + "\n"
    + " stateRoot       : " + uncle.stateRoot + "\n"
    + " miner           : " + uncle.miner + "\n"
    + " difficulty      : " + uncle.difficulty + "\n"
    + " totalDifficulty : " + uncle.totalDifficulty + "\n"
    + " extraData       : " + uncle.extraData + "\n"
    + " size            : " + uncle.size + "\n"
    + " gasLimit        : " + uncle.gasLimit + "\n"
    + " gasUsed         : " + uncle.gasUsed + "\n"
    + " timestamp       : " + uncle.timestamp + "\n"
    + " transactions    : " + uncle.transactions + "\n\n\n");
}





async function getMinedBlocks(miner, startBlockNumber, endBlockNumber) {
  if (endBlockNumber == null) {
    endBlockNumber = web3.eth.blockNumber;
    console.log("Using endBlockNumber: " + endBlockNumber);
  }
  if (startBlockNumber == null) {
    startBlockNumber = endBlockNumber - 10000;
    console.log("Using startBlockNumber: " + startBlockNumber);
  }
  console.log("Searching for miner \"" + miner + "\" within blocks "  + startBlockNumber + " and " + endBlockNumber + "\"");

  for (var i = startBlockNumber; i <= endBlockNumber; i++) {
    //if (i % 1000 == 0) {
      console.log("Searching for block " + i);
    //}
    var block = await web3.eth.getBlock(i);
    if (block != null) {
      if (block.miner == miner || miner == "*") {
        console.log("Found block " + block.number);
        //await printBlock(block);
      }

      if (block.uncles.length != 0) {
        for (var j = 0; j < block.uncles.length; j++) {
          var uncle = await web3.eth.getUncle(i, j);
          if (uncle != null) {
            //if (uncle.miner == miner || miner == "*") {
              console.log("Found uncle for " + block.number + " with uncle position: " + j);
              printUncle(block, j, uncle);
            //}
          }          
        }
      }
    }
  }
}



async function getTransactionsByAccount(myaccount, startBlockNumber, endBlockNumber) {
  if (endBlockNumber == 0) {
    endBlockNumber = await web3.eth.blockNumber;
    console.log("Using endBlockNumber: " + endBlockNumber);
  }
  if (startBlockNumber == 0) {
    startBlockNumber = endBlockNumber - 1000;
    console.log("Using startBlockNumber: " + startBlockNumber);
  }
  console.log("Searching for transactions to/from account \"" + myaccount + "\" within blocks "  + startBlockNumber + " and " + endBlockNumber);

  for (var i = startBlockNumber; i <= endBlockNumber; i++) {

    var block = await web3.eth.getBlock(i, true);
    if (block != null && block.transactions != null) {

      var txs = block.transactions

      for (index = 0; index < txs.length; index++) { 
        e = txs[index] 
        if (myaccount == "*" || myaccount == e.from || myaccount == e.to) {
          console.log("  tx hash          : " + e.hash + "\n"
            + "   from            : " + e.from + "\n" 
            + "   to              : " + e.to + "\n"
            + "   nonce           : " + e.nonce + "\n"
            + "   blockHash       : " + e.blockHash + "\n"
            + "   blockNumber     : " + e.blockNumber + "\n"
            + "   transactionIndex: " + e.transactionIndex + "\n"
            + "   value           : " + e.value + "\n"
            + "   time            : " + block.timestamp + "\n"//" " + new Date(block.timestamp * 1000).toGMTString() + "\n"
            + "   gasPrice        : " + e.gasPrice + "\n"
            + "   gas             : " + e.gas + "\n"
            + "   input           : " + e.input);

          var rcpt = await web3.eth.getTransactionReceipt(e.hash)
          console.log("   status          : " + rcpt.status + "\n"
            + "   contractAddress : " + e.contractAddress + "\n" 
            + "   gasUsed         : " + e.gasUsed);
        }
      } 

      // block.transactions.forEach( async function(e) {
      //   if (myaccount == "*" || myaccount == e.from || myaccount == e.to) {
      //     console.log("  tx hash          : " + e.hash + "\n"
      //       + "   from            : " + e.from + "\n" 
      //       + "   to              : " + e.to + "\n"
      //       + "   nonce           : " + e.nonce + "\n"
      //       + "   blockHash       : " + e.blockHash + "\n"
      //       + "   blockNumber     : " + e.blockNumber + "\n"
      //       + "   transactionIndex: " + e.transactionIndex + "\n"
      //       + "   value           : " + e.value + "\n"
      //       + "   time            : " + block.timestamp + "\n"//" " + new Date(block.timestamp * 1000).toGMTString() + "\n"
      //       + "   gasPrice        : " + e.gasPrice + "\n"
      //       + "   gas             : " + e.gas + "\n"
      //       + "   input           : " + e.input);

      //     var rcpt = await web3.eth.getTransactionReceipt(e.hash)
      //     console.log("   status          : " + rcpt.status + "\n"
      //       + "   contractAddress:            : " + e.contractAddress + "\n" 
      //       + "   gasUsed:            : " + e.gasUsed);
      //   }
      // })
    }
  }
}



async function getBalanceAtSpecificBlock(account, blockNumber, fee, value) {
  wei_value = await web3.eth.getBalance(account, blockNumber)
  console.log("sender: ", account)
  console.log("blockNumber: ", blockNumber)
  console.log("balance: ", wei_value/1000000000000000000)
  console.log("tx fee: ", fee)
  console.log("value: ", value)
  console.log("\n\n")
  return (wei_value/1000000000000000000)
}


async function getAllBalanceInfo() {
  var lineReader = require('readline').createInterface({
    input: require('fs').createReadStream('../result_check_orphan_tx_unpicked')
  });

  var hash_tx = ''
  var sender_addr = ''
  var blockNum = ''
  var gas = ''
  var gasprice = ''
  var value = ''

  lineReader.on('line', function (line) {
    if (line.startsWith('hash_tx:  ')) {
      hash_tx = line.replace('hash_tx:  ', '')
    }
    if (line.startsWith('from:  ')) {
      sender_addr = line.replace('from:  ', '')
    }
    if (line.startsWith('gas:  ')) {
      gas = line.replace('gas:  ', '')
    }
    if (line.startsWith('gasprice:  ')) {
      gasprice = line.replace('gasprice:  ', '')
    }
    if (line.startsWith('value:  ')) {
      value = line.replace('value:  ', '')
    }
    if (line.startsWith('block:  ')) {
      blockNum = line.replace('block:  ', '').trim()
      fee = Number(gas) * Number(gasprice)
      // hash_tx and sender_addr are avaiable for this transaction already
      // console.log("\n\nblock: ", blockNum)
      // console.log(hash_tx, sender_addr, blockNum)
      getBalanceAtSpecificBlock(sender_addr, blockNum, fee, value)
    }
  });

}



//getAllBalanceInfo()

getTransactionsByAccount("*", 7179343, 7281000)