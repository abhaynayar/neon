// only displays classes that HAVE been opened before.

console.log('[~] Starting class enumeration')
console.log('[!] You need to open corresponding activities on your')
console.log('[!] ... device first, for the classes to appear here')

/*send('[!] Enter package name: ');

var className = ''
recv('input', function onMessage(value) {
	className = value.payload;
	handleCallback(className);
});*/

function handleCallback() {
	Java.perform(function(){
		Java.enumerateLoadedClasses({
	
			'onMatch': function(c) {
				if(c.includes('b3nac'))
					console.log(c);
			},
	
			'onComplete': function() {}
		});
	});

	console.log('[!] Finished script');
}

handleCallback();
