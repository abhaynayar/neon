// only displays classes that HAVE been opened before.

console.log('[~] Starting class enumeration')
console.log('[!] You need to open corresponding activities first ...')
console.log('[!] ... on your device for the classes to appear here')

Java.perform(function(){
	Java.enumerateLoadedClasses({

		'onMatch':function(c) {
			if(c.includes('b3nac'))
				console.log(c);
		},

		'onComplete':function() {}
	});
});

console.log('[!] Finished script');

// a.includes(b)
