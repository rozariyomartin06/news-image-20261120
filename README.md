# Sum up 20 November's world news in one image

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/rozariyomartin06/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/rozariyomartin06/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A newspaper front page image summing up 20 November 2026's world news.

Entry for the [make.fun](https://make.fun/bounty/news-image-20261120) bounty `news-image-20261120` — $250, 50 places paid.
Deadline: Sun 22 Nov 2026, 00:00 UTC.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## What it is

A newspaper front page for **Friday 20 November 2026**, drawn
programmatically (flat vector style, no photos, no faces) and stored
as `entry.png` (1024×1024, ~178 KB). `main.ts` (Node 22, stdlib only)
copies it to `/output/entry.png`. The grader runs it twice with no
network; copying a fixed file means both runs write identical bytes.

## The 33 stories

Three illustrated leads, ten grid stories, a world map and twenty
indexed briefs — every continent, all first reported on Friday
20 November 2026.

1. **Antalya — COP31 ends with no deal as fossil fuels vanish.**
   Talks run past Friday's deadline; the draft drops the $120bn aid
   goal and admits 1.5°C will be breached.
2. **Odisha — Cyclone Akvan hits the coast, spares lives.** Landfall
   at Gopalpur at 70–80 km/h; no major damage after 300,000 evacuated.
3. **Kyiv — Russia's overnight strikes kill 8.** Bridges hit; 28
   hurt across nine regions.
4. **Warsaw — Russia breaches Polish airspace.** 5. **Tallinn —
   Estonia shuts Russia border.** 6. **Brussels — UK and EU seal food
   and youth deals.** 7. **Washington — Kushner floated NATO-for-
   Donbas swap.** 8. **Baghdad — Iraq moves on Iran-backed militia.**
   9. **New York — AMD crashes 13% on China bombshell.**
   10. **Tehran — Iran rejects US bioweapon claims.** 11. **Mexico
   City — Sheinbaum's economy flight goes viral.** 12. **Sydney —
   man charged over car-bomb research.** 13. **London — RAF Fairford
   suspects face 2027 trial.**
14. **Khartoum — Sudan suspends all imports from Kenya.**
15. **Darfur — Darfur women demand protection, war-crimes trials.**
16. **Nairobi — Chief Justice vows purge of corrupt judges.**
17. **Kenema — teen gets 100 years for teacher's murder.**
18. **Mogadishu — Gulf bloc condemns Somalia's UAE remarks.**
19. **Nairobi — Kenya opposition seeks election law changes.**
20. **Kampala — Uganda curbs gatherings near Ebola-risk border.**
21. **Dar es Salaam — Tanzania re-elected to UN telecom council.**
22. **Dhaka — Tarique Rahman blames India for Bangladesh violence.**
23. **Islamabad — Pakistan army says 22 militants killed in raids.**
24. **New Delhi — IAF's active Rafale jets down to 32.**
25. **Taipei — TSMC tightens China AI chip curbs.** 26. **Washington
   — US to put $1,000 in retirement accounts from 2027.**
27. **Washington — Trump says Vance erred on Iran war critique.**
28. **Washington — Trump and Xi want moderate AI rules.**
29. **Brussels — EU confirms first AI-assisted cyberattack.**
30. **Cincinnati — P&G targets $10bn in productivity savings.**
31. **Wellington — India hit back on day two of NZ Test.**
32. **Niue — Niue wins Earthshot 2026 prize.** 33. **Wellington —
   NZ rejects becoming Australia's 7th state.**

A DATE CHECK at the foot names what was left out for being another
day's news (19 Nov: the Shenzhen summit, the ICJ genocide ruling,
GTA VI, Anthropic's IPO, Somalia expelling the UAE envoy, the Haiti
raid, the JPMorgan/Visa/Mastercard data leak, US–Venezuela military
ties).

Wording is kept to what was reported on 20 Nov 2026, with attribution
where the claim is one party's (Tehran: "Iran rejects…", WSJ: the
Kushner proposal). No outcome is invented for COP31, which was still
in overtime when this page was drawn.

## How it was built

`generate.py` draws the image with Pillow (DejaVu fonts, local only —
the entry itself needs no Pillow, the grader only runs `main.ts`):

```bash
python3 generate.py          # regenerates entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
python3 -c "from PIL import Image; im=Image.open('out/entry.png'); print(im.size)"
```

## Verify

- `entry.png`: 1024×1024 PNG, under 1 MiB.
- `main.ts` run twice produces byte-identical output (checked with sha256).
- Headlines stay legible when the image is shown ~300 px across.

## Sources (20 Nov 2026)

COP31: Reuters / UN News / Tribune. Cyclone Akvan: IMD / The Hindu /
NDTV. Kyiv strikes, Poland airspace, Estonia border, Iraq deployment,
RAF Fairford: Just Security / AP. EU–UK summit: Reuters / Al Jazeera.
Kushner NATO proposal, Vance: WSJ. AMD, P&G, TSMC, AI rules, Iran
claims, retirement accounts: Economic Times. Sheinbaum flight:
Bloomberg. Sydney terror charge: NZ Herald. Sudan/Kenya, Darfur,
Kenya CJ, Sierra Leone, Somalia/GCC, Uganda, Tanzania:
BBC / Radio Dabanga / The Standard / Calabash / AllAfrica /
AfricaFrontPage. Pakistan raids, Rafale count: The Hindu / FlightGlobal.
Rahman: Economic Times. EU cyberattack: Economic Times. NZ Test: EIN.
Niue Earthshot, NZ–Australia debate: Science Media Centre / The Post.

---

Entered on [make.fun](https://make.fun/?ref=cwecrfep&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards
