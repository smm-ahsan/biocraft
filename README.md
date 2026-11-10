# BioCraft

A tiny open-source CLI that generates social media bio options for small businesses and creators - every option built to fit the platform's character limit, never truncated mid-word.

## Platform limits

| Platform  | Bio character limit |
|-----------|---------------------|
| Instagram | 150                 |
| TikTok    | 80                  |
| LinkedIn  | 220                 |

BioCraft composes each bio from short pieces - your name, what you do, a benefit line, a call to action, and your location when you give one. If a composed bio is too long for the platform, it drops the location first, then the call to action, then the benefit line, until it fits. Every printed option shows its exact character count so you can see it is within the limit.

## Requirements

- Python 3
- Standard library only - nothing to install

## Usage

```bash
python3 biocraft.py --name "Crumb and Craft" --what "handmade bakery" --niche bakery --location "Valletta" --platform instagram --count 3 --seed 4
python3 biocraft.py --name "Crumb and Craft" --what "handmade bakery" --niche bakery --location "Valletta" --platform tiktok --count 2 --seed 4
```

More examples, with real output, are in [examples.md](examples.md).

### Options

- `--name` (required): business or person name.
- `--what` (required): what they do, e.g. "handmade bakery".
- `--niche`: cafe, restaurant, bakery, salon, gym, realestate or general (default general). Chooses the benefit lines.
- `--location`: optional, shown as "📍 <location>".
- `--platform`: instagram (150 chars), tiktok (80) or linkedin (220). Default instagram.
- `--tone`: professional, friendly or bold (default friendly). Chooses the call to action style.
- `--count`: how many options to print (default 3).
- `--seed`: change for a different selection (default 1).

## License

MIT - see [LICENSE](LICENSE).
