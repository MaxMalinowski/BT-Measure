const mam = require('@iota/mam');
const converter = require('@iota/converter');

let mamState = mam.init('https://nodes.devnet.thetangle.org:443');
mamState = mam.changeMode(mamState, 'public');

const publish = async (data) => {
	// Convert data to trytes and create mam message
	const trytes = converter.asciiToTrytes(data);
	const msg = mam.create(mamState, trytes);

	// Update mam state to lastest message
	mamstate = msg.state;

	// Attach message
	await mam.attach(msg.payload, msg.address, 3, 9);
	console.log('Sent message to the Tangle! ' + 'Message: ' + data);
	console.log('Address: ' + msg.root);
}

publish('1. Super fancy message on the tangle!');
publish('2. Another super fancy message on the tangle!');

