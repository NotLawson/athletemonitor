# ADP Athlete Monitor
A custom built Athlete Monitor for WestMAC's ADP Program.

This repository will contain the backend server code.

## Server Architecture


## Versioning

To ensure compatibility between the client and the server, there will be three main versions:
- The Client Version: This is the used by the clinet device to manage updates, etc. This changes with every update to the client, in the format of major.minor.patch.
- The Server Version: This is used by the server to make sure that it is up to date with the latest changes. This changes with every update to the server, in the format of major.minor.patch
- The API Version: This is check on a connection initalisation between the client and the server to make sure the two versions are compatible. This changes with every change to the API, with the format of major.minor.

The major version number must be updated when a breaking change/and or major feature is being introduced. The minor version number must be updated when releasing a minor feature. For the API, it must be changed every revision. A patch version number must be changed on every revision.