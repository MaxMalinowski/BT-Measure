const iotaLib = require('@iota/core');
const converter = require('@iota/converter');
const iota = iotaLib.composeAPI({provider: 'http://node05.iotatoken.nl:16265'});

let rssi_file = require('./' + process.argv[2]);

const seed = 'ENTER-YOUR-CREDENTIALS-HERE!!!';
const add = 'ENTER-YOUR-CREDENTIALS-HERE!!!';

const main = async () => {
    // Generate new address
    const receivingAdd = await iota.getNewAddress(seed, {index: 1, total: 1});

    // construct a tx to our new address
    // const transfer = [{value: 0, address: receivingAdd[0], message: 'HI'}];
    let msg = JSON.stringify(rssi_file);
    let trytemsg = converter.asciiToTrytes(msg);
    const transfer = [{value: 0, address: add, message: trytemsg}];
    console.log('Sending results to ' + add);

    try {
        // construnct bundle and convert to trytes
        const trytes = await iota.prepareTransfers(seed, transfer);
        // send bundle to node
        const response = await iota.sendTrytes(trytes, 3, 14);
        // transaction done
        console.log('Completed transaction');
        response.map(tx => console.log(tx));
    } catch (e) {
        console.error(e);
    }
};

// run main
main();
