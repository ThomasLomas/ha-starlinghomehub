# Starling Home Hub Integration

# NOTE: No longer supporting v1 of the Starling Home Hub API

[![ThomasLomas - ha-starlinghomehub](https://img.shields.io/static/v1?label=ThomasLomas&message=ha-starlinghomehub&color=blue&logo=github)](https://github.com/ThomasLomas/ha-starlinghomehub "Go to GitHub repo")
[![stars - ha-starlinghomehub](https://img.shields.io/github/stars/ThomasLomas/ha-starlinghomehub?style=social)](https://github.com/ThomasLomas/ha-starlinghomehub)
[![forks - ha-starlinghomehub](https://img.shields.io/github/forks/ThomasLomas/ha-starlinghomehub?style=social)](https://github.com/ThomasLomas/ha-starlinghomehub)

[![Validate](https://github.com/ThomasLomas/ha-starlinghomehub/workflows/Validate/badge.svg)](https://github.com/ThomasLomas/ha-starlinghomehub/actions?query=workflow:"Validate")
[![GitHub tag](https://img.shields.io/github/tag/ThomasLomas/ha-starlinghomehub?include_prereleases=&sort=semver&color=blue)](https://github.com/ThomasLomas/ha-starlinghomehub/releases/)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)
[![issues - ha-starlinghomehub](https://img.shields.io/github/issues/ThomasLomas/ha-starlinghomehub)](https://github.com/ThomasLomas/ha-starlinghomehub/issues)

This is a custom integration for Home Assistant for accessing the [Starling Home Hub](https://www.starlinghome.io/) via the Starling Developer Connect API. My work is unaffiliated with Starling LLC. This is for use at your own risk. I don't provide any warranties whatsoever.

## Current Support

- [x] Nest Protect
  - [x] Battery Status
  - [x] Carbon Monoxide Detection
  - [x] Smoke Detection
- [ ] Thermostat
- [ ] Temperature Sensor
- [ ] Camera (pre-2021 models)
- [ ] Camera (2021/22 models)
- [ ] Guard
- [ ] Detect
- [ ] Nest x Yale Lock
- [ ] Nest Weather Service

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `starling_home_hub`.
1. Download _all_ the files from the `custom_components/starling_home_hub/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Starling Home Hub Integration"

## Hub Setup

> Note: Ensure you are using the latest firmware (2024.43 or above)

The SDC API is disabled by default. To enable the API, go to the Starling app, then:

1. Open the Starling Developer Connect section in the app.
2. If not already active, you will be prompted to enable Password Security to set an access password for your hub.
3. Select the Enable HTTP Access and/or Enable HTTPS Access checkboxes.

Access to the API requires creating an API key - one per app - with specific permissions that you set. To create an API key for your application:
1. In the My API Keys section, press Create New API Key.
2. Enter a name for your app/API key, and choose the permissions appropriate for your use case.
3. Press Create API Key. Your API key (a 12-character opaque alphanumeric string) will then appear under My API Keys.

To modify an existing API key's permissions or name, hover over the key in My API Keys, then press the edit button.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)
