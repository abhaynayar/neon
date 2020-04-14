Java.scheduleOnMainThread(function() {
	Java.use("android.widget.Toast")
		.makeText(Java.use("android.app.ActivityThread")
		.currentApplication().getApplicationContext(), "Text to Toast here", 0)
		.show();
});

