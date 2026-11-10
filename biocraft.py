#!/usr/bin/env python3
"""BioCraft - generate social media bio options that respect platform character limits.

Builds each bio from short template pieces (name, what you do, a benefit
line, a call to action, an optional location). If a composed bio exceeds
the platform limit, optional pieces are dropped - location first, then
the call to action, then the benefit line - until it fits. Text is never
truncated mid-word.
"""

import argparse
import random
import sys

LIMITS = {
    "instagram": 150,
    "tiktok": 80,
    "linkedin": 220,
}

BENEFITS = {
    "cafe": [
        "Fresh brews and slow mornings",
        "Specialty coffee, honest food",
        "Your daily coffee ritual, upgraded",
    ],
    "restaurant": [
        "Seasonal menus, cooked with care",
        "Real food, made from scratch",
        "Dinner done properly",
    ],
    "bakery": [
        "Baked fresh every morning",
        "Small batch, real ingredients",
        "Warm bread, happy days",
    ],
    "salon": [
        "Hair that turns heads",
        "Book in, glow out",
        "Your hair, but better",
    ],
    "gym": [
        "Stronger every week",
        "Real coaching, real results",
        "Train hard, stay humble",
    ],
    "realestate": [
        "Homes matched to your life",
        "Local knowledge, honest advice",
        "Keys to your next chapter",
    ],
    "general": [
        "Quality you can feel",
        "Small team, big care",
        "Done properly, every time",
    ],
}

CTAS = {
    "professional": [
        "Book your visit",
        "Get in touch to order",
        "Enquiries welcome",
    ],
    "friendly": [
        "DM to order",
        "Follow for daily tips",
        "Come say hi",
    ],
    "bold": [
        "DM to order now",
        "Book your visit today",
        "Follow for daily tips",
    ],
}

# Drop order for optional pieces when a bio is too long:
# location first, then the call to action, then the benefit line.
DROP_ORDER = (1, 2, 3)


def compose(segments, separator, limit):
    """Join segments, dropping optional ones until the text fits the limit.

    segments is a list of (text, rank) pairs. rank None means essential;
    ranks follow DROP_ORDER (1 = location, 2 = call to action, 3 = benefit).
    Returns the composed string, or None if even the essential pieces
    alone exceed the limit.
    """
    segs = [[text, rank] for text, rank in segments if text]

    def render():
        return separator.join(text for text, _rank in segs if text)

    while len(render()) > limit:
        dropped = False
        for rank in DROP_ORDER:
            for seg in segs:
                if seg[1] == rank and seg[0]:
                    seg[0] = ""
                    dropped = True
                    break
            if dropped:
                break
        if not dropped:
            return None
    return render()


def shapes(p):
    """Template shapes. Each returns (segments, separator) for compose()."""
    name = p["name"]
    what = p["what"]
    what_cap = what[:1].upper() + what[1:]
    benefit = p["benefit"]
    cta = p["cta"]
    loc = p["loc"]
    return [
        # 1. Classic pipe list.
        ([(name, None), (what, None), (benefit, 3), (cta, 2), (loc, 1)], " | "),
        # 2. Sentence style.
        ([(f"{name} - {what}.", None), (benefit + ".", 3), (cta + ".", 2), (loc, 1)], " "),
        # 3. What-first.
        ([(f"{what_cap} by {name}.", None), (benefit + ".", 3), (loc, 1), (cta + ".", 2)], " "),
        # 4. Short and direct, no benefit line.
        ([(f"{name}: {what}.", None), (cta + ".", 2), (loc, 1)], " "),
        # 5. Benefit first.
        ([(benefit, 3), (name, None), (what, None), (loc, 1), (cta, 2)], " | "),
        # 6. Dotted list.
        ([(name, None), (what, None), (loc, 1), (benefit, 3), (cta, 2)], " · "),
        # 7. At-style.
        ([(f"{what_cap} at {name}.", None), (cta + ".", 2), (loc, 1), (benefit + ".", 3)], " "),
    ]


def build_options(args):
    limit = LIMITS[args.platform]
    rng = random.Random(args.seed)
    options = []
    seen = set()
    for _round in range(10):
        if len(options) >= args.count:
            break
        pieces = {
            "name": args.name,
            "what": args.what,
            "benefit": rng.choice(BENEFITS[args.niche]),
            "cta": rng.choice(CTAS[args.tone]),
            "loc": f"📍 {args.location}" if args.location else "",
        }
        order = shapes(pieces)
        rng.shuffle(order)
        for segments, separator in order:
            if len(options) >= args.count:
                break
            text = compose(segments, separator, limit)
            if text and text not in seen:
                seen.add(text)
                options.append(text)
    return options


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate social media bio options that fit each platform's character limit."
    )
    parser.add_argument("--name", required=True, help="Business or person name.")
    parser.add_argument("--what", required=True, help='What they do, e.g. "handmade bakery".')
    parser.add_argument(
        "--niche",
        choices=["cafe", "restaurant", "bakery", "salon", "gym", "realestate", "general"],
        default="general",
    )
    parser.add_argument("--location", default=None, help="Optional location, shown with a pin.")
    parser.add_argument(
        "--platform",
        choices=["instagram", "linkedin", "tiktok"],
        default="instagram",
    )
    parser.add_argument(
        "--tone",
        choices=["professional", "friendly", "bold"],
        default="friendly",
    )
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args(argv)

    if args.count < 1:
        parser.error("--count must be at least 1")

    options = build_options(args)
    if not options:
        print(
            "error: name and description alone exceed the "
            f"{args.platform} limit of {LIMITS[args.platform]} characters; "
            "try shorter inputs or a platform with a higher limit.",
            file=sys.stderr,
        )
        return 2

    for i, text in enumerate(options, 1):
        if args.count > 1:
            print(f"--- Option {i} ---")
        print(text)
        print(f"({len(text)} chars)")
        if i < len(options):
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
