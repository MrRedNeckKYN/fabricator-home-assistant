# Grass (ARM64, manual login)

Unofficial replacement for the old Grass add-on. It follows the ARM64 recipe
from [MRColorR/get-grass](https://github.com/MRColorR/get-grass) and uses a
noVNC Chromium session for **manual** Grass login. No Grass credentials are
stored in Home Assistant options.

Set a unique `VNC_PASSWORD`, start the add-on, then visit
`http://HOME_ASSISTANT_IP:6080` from your trusted LAN. Use the displayed
browser to log in to Grass. The Chromium profile persists in `/data/grass`.

This is ARM64-only and unofficial; Grass does not officially support Raspberry
Pi/ARM Linux. It sends traffic through your public IP, so read Grass's terms,
privacy policy, and your ISP's rules before using it. Keep port 6080 off the
public internet.
