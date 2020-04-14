/*
 * enumerate static methods of a class 
 * https://github.com/frida/frida-java-bridge/issues/44
 * 13th April 2020
 * lists all methods in a class
 */

console.log('[~] Starting static method enumeration:w');
send('[!] Enter class name: ');

var className = ''
recv('input', function onMessage(value) {
	className = value.payload;
	handleCallback(className);
});

function handleCallback(input) {
	Java.perform(function() {
		var db1 = Java.use(className);
		var methodArr = db1.class.getDeclaredMethods();
		for(var m in methodArr)
			//if(methodArr[m].toString().includes(className))
				console.log(methodArr[m]);
	});
}


/* not used right now */

function describeJavaClass(className) {
  var jClass = Java.use(className);
  console.log(JSON.stringify({
    _name: className,
    _methods: Object.getOwnPropertyNames(jClass.__proto__) /*.filter(function(m) {
      return !m.startsWith('$') // filter out Frida related special properties
        || m == 'class' || m == 'constructor' // optional
    })*/, 
    _fields: jClass.class.getFields().map(function(f) {
      return f.toString()
    })  
  }, null, 2));
}

