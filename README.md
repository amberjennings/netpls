# netpls

A python script used to test network connectivity, and, if needed, reconnect to wifi and send an email.<br>
Written to deal with the lack of ethernet and spotty wifi in my dorm.<br>
Includes a systemd service and timer, currently configured to run every 30 minutes.<br>

## Prereqs:
- A systemd-based Linux/Unix system with Python installed<br>
- `python-yaml`, via pip or your systems package manager
- Root access<br>
- Access to a mail server from which to route your notifications<br>

## Setup:
- Update `rb.cfg.example` to be `rb.cfg`, within which all fields should be updated to have actual info<br>
- Update `netpls.service` to reflect the location of `netpls.py`
- Move `netpls.service` and `netpls.timer` into `/etc/systemd/system`, or wherever you keep your services
- As root, `systemctl enable netpls.service && systemctl enable netpls.timer`

## Notes:
- Please secure your .cfg file! This will have important passwords in it.
- If it doesn't work, please try to do some debugging or contact me before raising an issue.
