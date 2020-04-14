Java.perform(function() {
	Java.scheduleOnMainThread(function() {
		Toast = Java.use('android.widget.Toast')
		var context = Java.use('android.app.ActivityThread').currentApplication().getApplicationContext();
		var message = 'hi';

		Toast.makeText(context, message, Toast.LENGTH_SHORT.value).show();
	});
});

