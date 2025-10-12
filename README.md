# Starling Home Hub Integration

[![ThomasLomas - ha-starlinghomehub](https://img.shields.io/static/v1?label=ThomasLomas&message=ha-starlinghomehub&color=blue&logo=github)](https://github.com/ThomasLomas/ha-starlinghomehub "Go to GitHub repo")
[![stars - ha-starlinghomehub](https://img.shields.io/github/stars/ThomasLomas/ha-starlinghomehub?style=social)](https://github.com/ThomasLomas/ha-starlinghomehub)
[![forks - ha-starlinghomehub](https://img.shields.io/github/forks/ThomasLomas/ha-starlinghomehub?style=social)](https://github.com/ThomasLomas/ha-starlinghomehub)

[![GitHub tag](https://img.shields.io/github/release/ThomasLomas/ha-starlinghomehub?include_prereleases=&sort=semver&style=flat-square)](https://github.com/ThomasLomas/ha-starlinghomehub/releases/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/ThomasLomas/ha-starlinghomehub/validate.yml?style=flat-square)](https://github.com/ThomasLomas/ha-starlinghomehub/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](#license)
[![HACS](https://img.shields.io/badge/HACS-default-orange.svg?style=flat-square)](https://hacs.xyz)
[![issues - ha-starlinghomehub](https://img.shields.io/github/issues/ThomasLomas/ha-starlinghomehub?style=flat-square)](https://github.com/ThomasLomas/ha-starlinghomehub/issues)

This is a custom integration for Home Assistant for accessing the [Starling Home Hub](https://www.starlinghome.io/) via the Starling Developer Connect API. My work is unaffiliated with Starling LLC. This is for use at your own risk. I don't provide any warranties whatsoever.

Since v2 of the Starling Home Hub API there is now more widespread support for devices, and as such this may now also include non-Nest devices. To turn devices on/off use your Starling Hub App, or disable in Home Asisstant if you want to keep access for HomeKit.

## Hub Setup

> Ensure you are using the latest firmware (2024.43 or above). You must provide a /v2/ URL for the API integration to work.
> If your cameras are not detecting certain things, such as vehicles, then make sure that vehicle notifications is turned on in your Google Home app. Without notifications the Starling Home Hub won't get updates and thereby Home Assistant won't either.

The SDC API is disabled by default. To enable the API, go to the Starling app, then:

1. Open the Starling Developer Connect section in the app.
2. If not already active, you will be prompted to enable Password Security to set an access password for your hub.
3. Select the Enable HTTP Access and/or Enable HTTPS Access checkboxes.

Access to the API requires creating an API key - one per app - with specific permissions that you set. To create an API key for your application:

1. In the My API Keys section, press Create New API Key.
2. Enter a name for your app/API key, and choose the permissions appropriate for your use case.
3. Press Create API Key. Your API key (a 12-character opaque alphanumeric string) will then appear under My API Keys.

To modify an existing API key's permissions or name, hover over the key in My API Keys, then press the edit button.

## Installation

### Install via HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ThomasLomas&repository=ha-starlinghomehub&category=integration)

### Install Manually

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `starling_home_hub`.
1. Download _all_ the files from the `custom_components/starling_home_hub/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Starling Home Hub Integration"

## Development

### Mock Server

To run a mock server for development purposes, you can use the provided `mockserver` script. This script sets up a virtual environment, installs the required dependencies, and starts the mock server.

```bash
./scripts/mockserver
```

#### Integration Properties

| Property     | Value                    |
|--------------|--------------------------|
| **Base URL** | `http://127.0.0.1:5000/` |
| **API Key**  | `test`                   |

## Contributions are welcome

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)
