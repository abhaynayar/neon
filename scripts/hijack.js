/*
 *  method hijack @abhaynayar
 *  15th April 2020
 */


console.log('[~] Starting method hijack');
console.log('[!] Won\'t work if method has already been called')

send('[!] Enter fully qualified method name: ');
var methodName = ''
recv('input', function onMessage(value) {
	methodName = value.payload;
	handleCallback(methodName);
});

function handleCallback(input) {

	var res = input.split(/\.(?=[^\.]+$)/);

	Java.perform(function(){
		Java.use(res[0])[res[1]].implementation = function() {
			console.log('[+] Hello from the other side!');
			/*[-] Error: onCreate(): argument count of 0 does not match any of:
					.overload('android.os.Bundle')*/
		}
	});
}



