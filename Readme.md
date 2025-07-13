# Easy DRPC

Easy DRPC is a simple and user-friendly tool for integrating Discord Rich Presence (DRPC) into your applications. This project allows you to easily configure and run DRPC either by building from source or using the provided executable.

## Features

- Effortless Discord Rich Presence integration
- Customizable configuration via a config file
- Lightweight and easy to use

## Getting Started

### Cloning the Repository

```bash
git clone https://github.com/iayushanand/Easy-DRPC.git
cd Easy-DRPC
```

## Configuration

Easy DRPC uses a `config.txt` file for setup. You can find a sample config in the repository.

### Example `config.txt`

```
CLIENT_ID=
LARGE_IMAGE=
LARGE_TEXT=
STATE=
DETAILS=
ENABLE_TIMESTAMP=
TIMESTAMP=
```

### How to Get Config Values

- **CLIENT_ID**: Create a new application on the [Discord Developer Portal](https://discord.com/developers/applications) and copy the Client ID.
- **LARGE_IMAGE**: Upload images in your Discord application’s Rich Presence assets and use their keys.
- **Details/State**: Customize these fields to display your status.
- **Timestamp**: Unix Timestamp. Use a [convertor](https://www.epochconverter.com/) to get the desired value


## Running the Executable

1. Download the latest release from the [Releases](https://github.com/iayushanand/Easy-DRPC/releases) page.
2. Extract the contents to your desired location.
3. Set up your config file
4. Double-click `EasyDRPC.exe` to start the application.

## License

This project is licensed under the MIT License.

---

For questions or support, open an issue on GitHub.
