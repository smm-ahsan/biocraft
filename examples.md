# Examples

Real output from BioCraft, captured from actual runs.

## Bakery bio for Instagram (limit 150)

Command:

```bash
python3 biocraft.py --name "Crumb and Craft" --what "handmade bakery" --niche bakery --location "Valletta" --platform instagram --count 3 --seed 4
```

Output:

```
--- Option 1 ---
Crumb and Craft - handmade bakery. Baked fresh every morning. Follow for daily tips. 📍 Valletta
(95 chars)

--- Option 2 ---
Handmade bakery by Crumb and Craft. Baked fresh every morning. 📍 Valletta Follow for daily tips.
(96 chars)

--- Option 3 ---
Handmade bakery at Crumb and Craft. Follow for daily tips. 📍 Valletta Baked fresh every morning.
(96 chars)
```

## Same bakery for TikTok (limit 80)

Command:

```bash
python3 biocraft.py --name "Crumb and Craft" --what "handmade bakery" --niche bakery --location "Valletta" --platform tiktok --count 2 --seed 4
```

Output:

```
--- Option 1 ---
Crumb and Craft - handmade bakery. Baked fresh every morning.
(61 chars)

--- Option 2 ---
Handmade bakery by Crumb and Craft. Baked fresh every morning.
(62 chars)
```

Notice what changed: to fit TikTok's 80-character limit, BioCraft dropped the location and the call to action instead of cutting words in half. The name, the description and the benefit line survive intact.
