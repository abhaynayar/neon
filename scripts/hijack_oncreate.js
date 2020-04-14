console.log('[~] Starting method hijack');
console.log('[!] Won\'t work if method has already been called')
send('[!] Enter class name: ');

var className = ''
recv('input', function onMessage(value) {
	className = value.payload;
	handleCallback(className);
});

function handleCallback() {
	Java.perform(function(){
		//t = Java.use('java.lang.Boolean').$new(true);
		Java.use(className)['onCreate'].implementation = function() {
			console.log('[+] hello from the other side');
			this.onCreate();
			/*[-] Error: onCreate(): argument count of 0 does not match any of:
					.overload('android.os.Bundle')*/
			//return t;
		}
	});
}

