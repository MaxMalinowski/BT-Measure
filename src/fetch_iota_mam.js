// Fetch the message from private mam stream
const mam = require('@iota/mam');
const converter = require('@iota/converter');

// Enter the address from send_iota_mam.js!
const root = process.argv[2] ;
const mamType = 'restricted';
const mamSecret = 'Bluetooth + BLE + Iota';

mam.init('https://nodes.devnet.thetangle.org:443');
const showData = raw => console.log(JSON.parse(converter.trytesToAscii(raw)));

const get_data = async () => {
    const response = await mam.fetch(root, mamType, mamSecret, showData);
};

get_data();
