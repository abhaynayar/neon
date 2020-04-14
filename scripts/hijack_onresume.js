/*
 * onResume method hijack by @abhaynayar
 * 11th April 2020
 * overrides onresume implementation
*/

console.log('[~] Starting onResume method hijack.');
send('[!] Enter class name (example: com.package.class): ');
console.log('[!] Now open the activity on your device')

var methodName = '';
recv('input', function onMessage(value) {
	methodName = value.payload;
	handleCallback(methodName);
});

function handleCallback(input) {
	Java.perform(function() {
		var Activity = Java.use(input);
		Activity.onResume.implementation = function() {
			console.log('[+] ' + input + '.onResume has been hijacked!');

			// enter your own code here ...
			console.log('[~] Returning to the original implementation');
			this.onResume();
		}
	});
}

