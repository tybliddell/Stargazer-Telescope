Old repo: https://github.com/MRHT-SRProject/FlutterApp.git

Ideas for modes:
-Star trail from pointing at north pole - should make concentric circles from north pole going out.
-Queue of celestial bodies you would like pictures of. Could add specific settings for each request

Stretch goals:
-Privilege system to allow admins to add, remove and reorder entire queue. Non privileged mode that can only add, remove stars that you added yourself. Would require sending 'password' in the init from flutter to python, and python will respond in the init if they are a privileged user. Will also requier sending the client id of who added each star to allow flutter to display if star can be removed. 
-'Timeshare' mode. Allows people to share their telescopes across the web/app. 

TODO: 
-Add shutdown/periodic method to write data to disk
