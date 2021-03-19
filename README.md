# Mid-altitude Balloon Launch (multiple years)
KML network link, sample data, and Python tool for accessing APRS balloon data. 

Python minimally parses KML but uses oldschool scrapping techniques to get at data.  Python converts to CSV (in buffer) and writes to target ArcGIS Onlinne feature service.  Ideally python script run on a daily scheduler.  Version one does not check for redundant data, although if run at 24 hour increments, it shouldn't matter much.

This is an experimental script only and needs further work.
