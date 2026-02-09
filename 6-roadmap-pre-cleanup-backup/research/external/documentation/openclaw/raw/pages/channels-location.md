---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/channels/location",
    "fetched_at": "2026-02-07T10:12:59.800161",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 480251
  },
  "metadata": {
    "title": "Channel Location Parsing",
    "section": "location",
    "tier": 3,
    "type": "reference"
  }
}
---

- Channel Location Parsing - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationConfigurationChannel Location Parsing[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Chat Channels](/channels)Messaging platforms- [WhatsApp](/channels/whatsapp)- [Telegram](/channels/telegram)- [grammY](/channels/grammy)- [Discord](/channels/discord)- [Slack](/channels/slack)- [Feishu](/channels/feishu)- [Google Chat](/channels/googlechat)- [Mattermost](/channels/mattermost)- [Signal](/channels/signal)- [iMessage](/channels/imessage)- [Microsoft Teams](/channels/msteams)- [LINE](/channels/line)- [Matrix](/channels/matrix)- [Zalo](/channels/zalo)- [Zalo Personal](/channels/zalouser)Configuration- [Pairing](/start/pairing)- [Group Messages](/concepts/group-messages)- [Groups](/concepts/groups)- [Broadcast Groups](/broadcast-groups)- [Channel Routing](/concepts/channel-routing)- [Channel Location Parsing](/channels/location)- [Channel Troubleshooting](/channels/troubleshooting)On this page- [Channel location parsing](#channel-location-parsing)- [Text formatting](#text-formatting)- [Context fields](#context-fields)- [Channel notes](#channel-notes)Configuration# Channel Location Parsing# [​](#channel-location-parsing)Channel location parsing

OpenClaw normalizes shared locations from chat channels into:

- human-readable text appended to the inbound body, and

- structured fields in the auto-reply context payload.

Currently supported:

- **Telegram** (location pins + venues + live locations)

- **WhatsApp** (locationMessage + liveLocationMessage)

- **Matrix** (`m.location` with `geo_uri`)

## [​](#text-formatting)Text formatting

Locations are rendered as friendly lines without brackets:

- Pin:

`📍 48.858844, 2.294351 ±12m`

- Named place:

`📍 Eiffel Tower — Champ de Mars, Paris (48.858844, 2.294351 ±12m)`

- Live share:

`🛰 Live location: 48.858844, 2.294351 ±12m`

If the channel includes a caption/comment, it is appended on the next line:

Copy```

📍 48.858844, 2.294351 ±12m

Meet here

```

## [​](#context-fields)Context fields

When a location is present, these fields are added to `ctx`:

- `LocationLat` (number)

- `LocationLon` (number)

- `LocationAccuracy` (number, meters; optional)

- `LocationName` (string; optional)

- `LocationAddress` (string; optional)

- `LocationSource` (`pin | place | live`)

- `LocationIsLive` (boolean)

## [​](#channel-notes)Channel notes

- **Telegram**: venues map to `LocationName/LocationAddress`; live locations use `live_period`.

- **WhatsApp**: `locationMessage.comment` and `liveLocationMessage.caption` are appended as the caption line.

- **Matrix**: `geo_uri` is parsed as a pin location; altitude is ignored and `LocationIsLive` is always false.

[Channel Routing](/concepts/channel-routing)[Channel Troubleshooting](/channels/troubleshooting)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)