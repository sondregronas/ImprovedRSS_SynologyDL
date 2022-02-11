# Improved RSS - Synology DL Station
This Flask application addresses some gripes with the current Synology RSS feed implementation in the Download Station package.
<br>
When queried the application outputs an RSS feed.

## What it does
- Optionally makes use of [RSSMerge](https://github.com/mgaulton/RssMerge) when queried a JSON path (relative to app.py's location)
- Automatically retries loading RSS upon failure
- Truncates some unnecessary data that would cause issues with results duplicating

## Setup
- `pip3 install -R requirements.txt`
- Adjust the variables in app.py (`host-ip`, `host-port`, `searchURL`) to your liking
- Run with `python3 app.py` (This can be added to cron; `@reboot python3 app.py`)
- In DL Station, simply add a new RSS feed; `http://<host-ip>:5000/?search="mysearch"` or `http://<host-ip>:5000/?j="myfeeds.json"`
- Optional flags are `&active=no`, `&limit=50` and `&category=41`

## JSON File
See videos.json for an example of how to setup a JSON file. `prefix=` can be omitted.<br>
Optional flags inside feeds, per RssMerge documentation:
```
"type": "normal",
"regex": {
	"pattern": None,
	"replace": None
},
"filter": None
```
