# LBS Velocity Handler
An enhanced velocity handler

## Basic Features

1. Allow MCDR to handle player chat, player chat log line format can be configured in config

2. Allow ignoring or replace chat message with specified prefixes


## Requirements

[`parse`](https://github.com/r1chardj0n3s/parse)

[`mcdreforged`](https://mcdreforged.com) >= 2.13.0-alpha.1

## Usage

1. Place this plugin in your MCDR plugin directory
2. Install some Velocity plugin to print player chat to Velocity console, such as [VelocityMCDRCommand](https://github.com/Lazy-Bing-Server/MCDRCommand-Velocity/)
3. Start MCDR

## Command

Default command prefix: `!!hvl` (Can be configured in config file)

`!!hvl reload` Reload handler config


## Config

Config file path: `config/lbs_velocity_handler/config.json`

1. `reload_config_prefix`

   Modify this plugin config prefix

   Default value: `!!hvl`


2. `admin_permission`

   Only players has this permission level or higher can run this plugin commands

   Default_value: `4`


3. `replace_prefixes_map`

   Replace the prefixes defined in these keys to their corresponding values

   Default value: `{"!!MCDR": "!!VMCDR", "!!VMCDR": "!!MCDR"}` 

   (Default value is set to avoid conflict of `!!MCDR` with MCDR on sub-servers)


4. `ignore_prefixes`

   Chat message which starts with these values will be ignored

   Default value: Empty list


5. `player_chat_log_format`

   Player chat log formats which not includes Velocity regular log prefixes

   Default value: `['[{server}] <{name}> {message}']`

   (Default format is the same as the player chat log format of [VelocityMCDRCommand](https://github.com/Lazy-Bing-Server/MCDRCommand-Velocity/))
