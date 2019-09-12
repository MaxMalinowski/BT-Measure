const mam = require('@iota/mam');
const converter = require('@iota/converter');
let rssi_file = require('./' + process.argv[2]);

let mamState = mam.init('https://nodes.devnet.thetangle.org:443');
const mamType = 'restricted';
const mamSecret = 'Bluetooth + BLE + Iota';

mamState = mam.changeMode(mamState, mamType, mamSecret);

const publish = async data => {
	// Convert the JSON to trytes and create a MAM message
	const trytes = converter.asciiToTrytes(data);
	const message = mam.create(mamState, trytes);

	// Update the MAM state to the state of this latest message
	// We need this so the next publish action knows it's state
	mamState = message.state;

	// Attach the message
	await mam.attach(message.payload, message.address, 3, 9);
	console.log('Sent message to private MAM stream');
	console.log('Address: ' + message.root)
};

publish(JSON.stringify(rssi_file));


