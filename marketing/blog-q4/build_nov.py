"""Build the November blog drafts (posts 5-9) in the Q4 Blog Path format.

Writes <n>-<slug>.html (article body), .json (articleCreate input) and .md (review copy).
Source copy: the five PDFs supplied on Nov 9, 2026.
"""
import json, re, html

BLOG_ID = "gid://shopify/Blog/96175292654"
IMG_BASE = "https://raw.githubusercontent.com/GeekIsle/Funtosh---slack--dataspace/edb3ff5c80ced0588bd11d972d3142b663965f49/marketing/originals-assets/listing/"
TAGS = ["#SustainableLiving", "#LowWasteLiving", "#EcoSwaps", "#ConsciousConsumer", "#DailyEssentials"]
SITE = "https://www.mimro.com"
P = {
    "swe": f'<a href="{SITE}/products/mimro-swedish-dishcloth">Mimro Swedish Dishcloth</a>',
    "loof": f'<a href="{SITE}/products/mimro-natural-loofah-cellulose-sponge">Mimro Natural Loofah Cellulose Sponge</a>',
    "coco": f'<a href="{SITE}/products/mimro-coconut-cellulose-kitchen-sponge">Mimro Coconut Cellulose Kitchen Sponge</a>',
    "bath": f'<a href="{SITE}/products/mimro-natural-loofah-bath-set">Mimro Natural Loofah Bath Set</a>',
}
C = {
    "kitchen": ("Shop Kitchen Solutions", "/collections/kitchen-solutions"),
    "clean": ("Shop Cleaning Essentials", "/collections/home-cleaners"),
    "care": ("Shop Personal Care", "/collections/hygiene-essentials"),
    "self": ("Shop Self-Care", "/collections/self-care-goods"),
    "originals": ("Shop Mimro Originals", "/collections/mimro-originals"),
    "top": ("Shop Top Picks", "/collections/eco-pick"),
    "all": ("Explore All Collections", "/collections/all"),
}
PRI = 'display:inline-block;background:linear-gradient(to right,#007ae7,#2ad265);color:#fff;text-decoration:none;border-radius:40px;padding:12px 30px;font-weight:600;margin:4px 6px 4px 0'
SEC = 'display:inline-block;background:#fff;color:#007ae7;border:2px solid #007ae7;text-decoration:none;border-radius:40px;padding:10px 28px;font-weight:600;margin:4px 6px 4px 0'
ITEM = 'margin:0 0 14px'


def btns(*keys):
    out = []
    for k in keys:
        label, path = C[k]
        out.append(f'<a href="{SITE}{path}" style="{SEC if k == "all" else PRI}">{label}</a>')
    return "<p>\n" + "\n".join(out) + "\n</p>"


def render(blocks):
    """blocks: ('p', html) | ('h', text) | ('n', [(lead, text)...]) numbered | ('b', [(lead, text)]) bullets | ('btn', keys) | ('strong', html)"""
    out = []
    for kind, val in blocks:
        if kind == "p":
            out.append(f"<p>{val}</p>")
        elif kind == "strong":
            out.append(f"<p><strong>{val}</strong></p>")
        elif kind == "h":
            out.append(f"<h2>{val}</h2>")
        elif kind == "n":
            for i, (lead, text) in enumerate(val, 1):
                out.append(f'<p style="{ITEM}"><strong>{i}. {lead}</strong> {text}</p>')
        elif kind == "b":
            for lead, text in val:
                out.append(f'<p style="{ITEM}">• <strong>{lead}</strong> {text}</p>')
        elif kind == "btn":
            out.append(btns(*val))
    return "\n".join(out) + "\n"


POSTS = [
 dict(n=5, slug="after-the-last-use", img="L_loof_lifestyle.jpg",
  title="After the Last Use: Knowing What to Do with Everyday Products",
  blocks=[
   ("p", "Most of us try to do the “right thing” after we’re done with something. We rinse the container. We save the box. We stare at the recycling bin and hesitate. Is this recyclable or trash? Does it need to be clean? Is it compostable, or only in certain places?"),
   ("p", "That uncertainty is exhausting, and it’s one reason sustainable living can feel harder than it needs to be. When end-of-life rules are unclear, we either guess, or we give up and throw it away. Not because we don’t care, but because the instructions are inconsistent and the systems around us vary."),
   ("p", "The truth is, disposal isn’t one universal rule. It depends on the material, your local waste services, and how a product is made. Mimro exists to make eco-conscious choices feel realistic and repeatable, and that includes what happens after the last use, not just what you buy."),
   ("h", "The habit: the End-of-Life Ladder"),
   ("p", "If you want a simple way to handle disposal without overthinking it, use an End-of-Life Ladder. Start at the top and move down only if you need to."),
   ("n", [
     ("Reuse (best default).", "Before you toss something, ask: can it do one more job? A jar becomes storage. A pouch becomes a travel kit. A cloth becomes a cleaning rag. Reuse buys time and reduces demand for new stuff."),
     ("Repair (if it’s meant to last).", "If something is designed for repeat use, treat it like a tool, not a disposable. Tighten it, patch it, replace a part if you can. Repair keeps your low-waste choices from turning into low-waste purchases that still end up in the bin."),
     ("Recycle (only if your local system accepts it).", "Recycling isn’t a magic fix. It’s a local service with specific rules. Some places accept certain plastics, some don’t. Some require labels removed, and many require items to be clean and dry. If you’re unsure, check your local waste guidelines. “Recyclable” on a label doesn’t mean recyclable where you live."),
     ("Compost (only if the conditions match).", "Compostable items often need specific conditions. Some are home-compostable, some only industrial-compostable. If your area doesn’t have industrial composting, “compostable” may not be practical. Look for clear instructions and certifications, and match them to what you can actually access."),
     ("Trash (sometimes the most honest option).", "It sounds harsh, but it’s real: putting the wrong item in recycling can contaminate a whole batch. If you can’t verify it’s accepted, trash may be better than wish-cycling. The long-term goal is to land here less often by choosing repeat-use and refill-friendly options first."),
   ]),
   ("p", "Try it for one week: every time you finish a product, run it through the ladder. You’ll start noticing which materials and formats cause the most confusion, and that’s your clue for what to upgrade next."),
   ("h", "Choose products that make “after” easier"),
   ("p", "One of the easiest ways to reduce disposal stress is to buy fewer things that need complicated end-of-life decisions."),
   ("b", [
     ("Sustainable cleaning essentials:", f"reusable tools that replace paper towels and disposable wipes, like the {P['swe']} or the plant-based {P['loof']}. Less trash, and fewer “can I recycle this?” moments."),
     ("Low-waste home essentials:", "practical items that support refill-first routines and cut constant packaging waste."),
     ("Natural personal care:", "simpler routines and lower-packaging options that reduce bathroom-bin overflow."),
     ("Eco-friendly daily swaps:", "repeat-use upgrades that shrink the volume of single-use items you have to deal with in the first place."),
     ("Food and drink basics:", "reusables that cut snack and drink packaging, one of the biggest sources of daily waste."),
   ]),
   ("btn", ["clean", "kitchen", "care"]),
   ("p", "The goal isn’t perfection. It’s choosing categories that make your end-of-life decisions simpler and more consistent."),
   ("h", "Build better defaults, not more disposal"),
   ("p", "The easiest way to make “after the last use” simpler is to create fewer last uses. Pick one repeat-use item you’ll reach for every week, and let that one default replace dozens of disposable decisions over time."),
   ("btn", ["top", "all"]),
   ("h", "Mimro AI: help choosing what fits your routine"),
   ("p", "Not sure what to buy first, what will actually last, or what makes the biggest difference? Tell Mimro AI, our eco-shopping assistant, what you’re trying to reduce (packaging, disposables, confusing materials), what your routine looks like, and your comfort level. It helps you narrow down options from Mimro’s collections without guilt or information overload."),
   ("h", "Sustainable living doesn’t end at checkout"),
   ("p", "When you know what to do with what you already have, you waste less, stress less, and make smarter choices next time."),
   ("strong", "Use the End-of-Life Ladder, follow your local disposal rules, and build repeat-use defaults that make everyday living, and everyday disposal, feel simpler."),
  ]),
 dict(n=6, slug="the-things-we-dont-think-about", img="L_swe_lifestyle.jpg",
  title="The Things We Don’t Think About: Everyday Waste That Happens on Autopilot",
  blocks=[
   ("p", "Waste doesn’t always look like an overflowing bin. Sometimes it looks like running the tap a little longer than necessary, buying another bottle of cleaner before finishing the last one, forgetting leftovers at the back of the fridge, or ordering something online without a thought for its packaging."),
   ("p", "These habits seem too small to matter. But when they become part of our daily routines, they quietly add up."),
   ("p", "The problem isn’t that we don’t care about the environment. It’s that many everyday decisions happen without much thought. We repeat what feels convenient, familiar, or automatic, and rarely stop to consider what those choices leave behind."),
   ("p", "The good news? You don’t need to change your entire lifestyle to make a difference. You just need to start noticing what happens on autopilot."),
   ("h", "Notice the habits hiding in plain sight"),
   ("b", [
     ("The products we overuse.", "A little extra laundry detergent, too much dish soap, or more cleaning spray than needed means products run out faster than expected. Following usage instructions and measuring carefully helps supplies last longer."),
     ("The food we forget.", "Leftovers pushed behind newer groceries, vegetables forgotten in a drawer, and ingredients bought without a meal in mind can all end up wasted. A quick fridge check before shopping helps you use what you already have."),
     ("The things we replace too soon.", "A worn cleaning cloth, a container with plenty of life left, or a product that just needs proper care may not need replacing yet. Check whether cleaning, repairing, or reusing it is a reasonable option first."),
     ("The packaging we barely notice.", "Individual purchases, repeated deliveries, and extra outer packaging create waste beyond the item itself. Combining orders when practical and choosing products with less packaging can help."),
     ("The resources we leave running.", "Water flowing while we brush our teeth, lights left on in empty rooms, and electronics running when they’re not needed are easy to overlook. Small reminders make mindful use feel natural."),
   ]),
   ("p", "None of these habits makes you careless. They simply show how easily convenience becomes automatic."),
   ("h", "The habit: a one-week Autopilot Check"),
   ("p", "The first step isn’t buying something new. It’s paying attention. For one week, notice what you throw away, use up quickly, or keep replacing. No complicated tracking system needed. Just ask yourself:"),
   ("n", [
     ("What am I wasting?", ""),
     ("Why does it keep happening?", ""),
     ("What small change would prevent it next time?", ""),
   ]),
   ("p", "Then attach that change to a habit you already have. Check the fridge before writing your grocery list. Measure cleaning products before using them. Keep reusable items where you can easily reach them. Finish opened products before starting new ones."),
   ("p", "These small adjustments work because they address why waste happens in the first place: repetition without reflection."),
   ("h", "Choose products that support better habits"),
   ("p", "Once you know where waste happens, the right products make better choices easier to keep."),
   ("b", [
     ("In the kitchen:", f"the {P['swe']} is a reusable option for wiping surfaces, handling spills, and cleaning dishes. It’s washable and dries fast, so it’s practical for repeated use."),
     ("For cleaning:", f"the {P['loof']} is a plant-based alternative for everyday dishwashing and surface cleaning. Pair good tools with careful product measuring to avoid unnecessary consumption."),
     ("In personal care:", "shampoo bars, conditioner bars, and toothpaste tablets offer alternatives to some conventional bottled formats, and Mimro’s refill options help you reduce packaging where it suits you."),
   ]),
   ("p", "The goal isn’t to replace everything you own. Use what you have first, then choose a better alternative when something genuinely needs replacing."),
   ("btn", ["kitchen", "clean", "care"]),
   ("h", "Shop with your habits in mind"),
   ("p", "Before adding anything to your cart, think about the problem you want to solve. Throwing away cleaning materials constantly? Forgetting food? Buying the same essentials too often? Start with that need."),
   ("btn", ["top", "all"]),
   ("h", "Let Mimro AI help you choose thoughtfully"),
   ("p", "Not sure which options suit your needs? Instead of shopping for whatever looks sustainable, start with a specific question for Mimro AI, our eco-shopping assistant: What could help me reduce packaging? Which reusable option suits my kitchen? What fits my current routine? A focused search helps you choose well without turning sustainability into more clutter or spending."),
   ("h", "Small things count when we start noticing"),
   ("p", "Everyday waste often begins with something we barely notice. But once you recognize a pattern, you can change it. You don’t need a perfect routine or a waste-free home, just a few better decisions that become habits over time."),
   ("strong", "Use what you have. Pay attention to what you consume. Make things last, and replace them thoughtfully when the time comes."),
  ]),
 dict(n=7, slug="sustainable-by-season", img="L_bath_lifestyle.jpg",
  title="Sustainable by Season: How Your Everyday Habits Change Throughout the Year",
  blocks=[
   ("p", "Sustainable living often gets framed like a personality trait. Either you “are” low-waste, or you’re not. But real life doesn’t work like that. Your routines change constantly, and your habits change with them."),
   ("p", "In summer, you’re out more. You buy more drinks on the go and need hydration, sunscreen, quick cleanups, and travel-friendly basics. In the school season, mornings speed up and convenience wins. In winter, laundry piles up, indoor messes increase, and you restock home and personal care more often. Add holidays, hosting, and weekend trips, and your “simple” routine becomes a rotating set of needs."),
   ("p", "That’s why many eco habits don’t stick. It’s not that you failed. It’s that your system didn’t adapt. If your low-waste options only work for one version of your life, you’ll fall back into single-use shortcuts the moment the season changes."),
   ("p", "Mimro exists to make low-waste living feel normal and repeatable, even when your routine shifts. The goal isn’t to do everything all year. It’s to build seasonal defaults you can reuse."),
   ("h", "The habit: the Seasonal Reset"),
   ("p", "Instead of trying to be perfectly sustainable, do one seasonal reset, one routine at a time. At the start of each season, ask:"),
   ("n", [
     ("What routine is about to change?", "Hydration, laundry, travel, hosting, school mornings."),
     ("What disposable shortcut shows up when I’m busy?", "Paper towels, wipes, bottled drinks, snack packaging, “emergency” buys."),
     ("What reusable or refill-friendly default can replace it?", ""),
     ("Where will I keep it so I actually use it?", "This is the difference between a good intention and a habit. The better option has to be the closest option."),
   ]),
   ("p", "Keep it simple: choose one seasonal routine to upgrade for the next 30 days. Not your whole life. Just one repeat moment."),
   ("h", "Match your swaps to the season you’re in"),
   ("p", "Once you know the routine you’re upgrading, shopping gets easier. You’re not buying random eco stuff. You’re building a seasonal kit that supports your real habits."),
   ("b", [
     ("Food and drink basics:", "for summer hydration, school lunches, road trips, and busy days when packaging adds up fast."),
     ("Sustainable cleaning essentials:", f"quick, reusable tools for seasonal messes, from summer spills to winter indoor cleanup, like the {P['swe']} and {P['coco']}, without burning through paper towels."),
     ("Low-waste home essentials:", "practical items that reduce restocking and keep routines smooth when schedules get hectic."),
     ("Natural personal care:", f"for seasonal self-care, travel, and basics that run out faster than you expect, like the {P['bath']}."),
     ("Eco-friendly daily swaps:", "small upgrades that cut single-use habits across the year, one routine at a time."),
   ]),
   ("btn", ["kitchen", "clean", "self"]),
   ("p", "The goal isn’t to switch everything each season. It’s to choose the category that removes the most friction in your current routine."),
   ("h", "Start with one seasonal default"),
   ("p", "The simplest path: pick one item you’ll use weekly (or daily) in the season you’re entering, and build one seasonal default kit, a small set of reusables that stays ready so you don’t have to re-decide every time your routine shifts."),
   ("btn", ["top", "all"]),
   ("h", "Mimro AI: a smarter way to shop for your season"),
   ("p", "Not sure what fits your current season? Tell Mimro AI, our eco-shopping assistant, what’s changing (school mornings, travel, hosting, laundry, on-the-go days), what you want to avoid (single-use plastics, clutter, complicated care), and your comfort level. It helps you narrow down options from Mimro’s collections so your seasonal routine is easy to repeat."),
   ("h", "A system that adapts"),
   ("p", "Sustainable living isn’t one routine. It’s a set of routines that change throughout the year. You don’t need to be perfect in every season. You just need a system that adapts."),
   ("strong", "Start with one Seasonal Reset, upgrade one repeat habit, and keep the better option where you naturally reach."),
  ]),
 dict(n=8, slug="new-chapter-lighter-footprint", img="L_coco_lifestyle.jpg",
  title="New Chapter, Lighter Footprint: Making More Thoughtful Choices During Life Changes",
  blocks=[
   ("p", "Every new chapter brings a to-do list. A new home needs setting up, university calls for supplies, a new job changes your routine, and welcoming a baby brings new responsibilities. Suddenly, shopping feels like the easiest way to get ready."),
   ("p", "Between endless checklists, recommendations, and perfectly organized spaces on social media, preparation can turn into pressure. You start wondering whether you need new furniture, clothes, matching containers, cleaning supplies, and products you’ve never used before."),
   ("p", "But a fresh start doesn’t require a completely new set of belongings. It’s a chance to decide what you genuinely need, what you already have, and which habits you want to carry into your next chapter."),
   ("h", "The fresh-start trap: when preparing means buying more"),
   ("p", "Life transitions can make familiar belongings feel outdated. A new apartment may inspire an entirely new kitchen setup. Starting university can make it feel like everyone else has better supplies. Becoming a parent brings endless recommendations for products that promise to make life easier."),
   ("p", "The result? Unnecessary spending, clutter, and waste before your new routine has even settled. Usable items get discarded because they don’t match a new space, while unopened purchases sit in cupboards waiting for a purpose."),
   ("p", "Before adding anything to your cart, ask: <em>Am I buying this because I need it, or because I feel a new beginning should look different?</em>"),
   ("h", "The habit: build better habits before a shopping list"),
   ("n", [
     ("Take inventory before shopping.", "Kitchen towels, storage containers, toiletries, cleaning tools, and everyday bags may still be perfectly useful. Reorganize or reuse them before deciding they need replacing."),
     ("Separate essentials from nice-to-haves.", "Make two lists: what you need now and what can wait. A student may prioritize basic cleaning supplies and a reusable water bottle over decor. A new parent may focus on practical essentials over every recommended baby product."),
     ("Let your routine reveal your needs.", "You don’t have to anticipate every challenge in advance. Spend a few weeks in your new space or schedule, then notice what you use, what creates waste, and where a better alternative would genuinely help."),
     ("Choose items that do more.", "Prioritize durable, reusable, refillable, or versatile products. A washable cloth can replace disposable alternatives, and refillable cleaning products let you reuse containers."),
     ("Give unwanted items another life.", "Sell, donate, share, or responsibly recycle usable belongings instead of throwing them away. A new chapter for you doesn’t have to mean the end of an item’s useful life."),
   ]),
   ("h", "Shop thoughtfully: essentials for your next chapter"),
   ("b", [
     ("Kitchen and household essentials:", f"the {P['swe']} is a washable, fast-drying alternative to paper towels, and the {P['loof']} is a plant-based option for dishwashing."),
     ("Home cleaning:", "refillable formats and practical tools that suit your space and reduce dependence on disposable supplies. Choose what fits your existing habits rather than replacing everything at once."),
     ("Personal care and hygiene:", "shampoo bars, toothpaste tablets, and reusable personal-care essentials simplify bathroom routines, whether you’re moving into shared accommodation or starting a new job."),
     ("Reusable everyday essentials:", "food wraps, shopping bags, and reusable containers for university, work, or home. The best choice is the one you’ll remember to use."),
   ]),
   ("btn", ["kitchen", "clean", "care"]),
   ("h", "Ready for your next chapter? Shop with purpose"),
   ("p", "Your shopping list should reflect your needs, not someone else’s idea of the perfect fresh start. Start with one category, identify what genuinely needs replacing, and choose products that fit your budget, space, and routine. A few well-chosen swaps beat a complete lifestyle overhaul."),
   ("btn", ["top", "all"]),
   ("h", "Not sure what you need? Ask Mimro AI"),
   ("p", "Sometimes the hardest part is knowing where to begin. Whether you’re cutting plastic in a new apartment, building a university essentials list, or simplifying a new household routine, describe your situation to Mimro AI, our eco-shopping assistant: what you already own and the problem you want to solve. It helps you narrow your choices instead of growing an already overwhelming list."),
   ("h", "A new beginning doesn’t need more stuff"),
   ("p", "Moving, studying, starting a family, or beginning a new job already brings enough change. You don’t need to replace everything to make your next chapter meaningful."),
   ("strong", "Use what you have. Buy what you need. Choose better alternatives when something genuinely needs replacing, and start your next chapter with less clutter and a lighter footprint."),
  ]),
 dict(n=9, slug="the-sustainable-workday", img="L_swe_packshot.jpg",
  title="The Sustainable Workday: Small Environmental Choices Beyond Your Front Door",
  blocks=[
   ("p", "Between morning commutes, back-to-back meetings, lunch breaks, and the rush to finish the day, sustainability can slip down the priority list. Coffee comes in a disposable cup, lunch arrives in layers of packaging, and forgotten chargers or printed documents become part of the daily routine."),
   ("p", "Whether you work from an office, a coworking space, or your kitchen table, your workday involves choices that affect how much you consume and throw away."),
   ("p", "The challenge isn’t finding time for an entirely new lifestyle. It’s recognizing where small adjustments fit into the workday you already have."),
   ("h", "The habit: rethink what follows you to work"),
   ("b", [
     ("Rethink your commute.", "When practical, walk, cycle, take public transit, or share a ride. If you can work remotely, combining errands or coordinating office days also cuts unnecessary trips. The best choice depends on your location, schedule, accessibility, and safety."),
     ("Make lunch less wasteful.", "Buying lunch every day means repeated takeaway containers, cutlery, napkins, and packaging. Prep meals when convenient, carry a reusable container, or keep cutlery at your desk. If you order food, request only the extras you actually need."),
     ("Make meetings more intentional.", "Before printing an agenda or handouts, consider whether digital will work. For in-person meetings, reusable cups and shared supplies reduce disposables."),
     ("Treat shared resources with care.", "Lights, air conditioning, printers, and equipment are easy to overlook because everyone uses them. Switch off what you’re responsible for when it’s safe and appropriate, avoid unnecessary printing, and follow your workplace’s policies."),
     ("Build a better end-of-day habit.", "Before logging off, check that your lunch container is ready for tomorrow, devices are charging appropriately, and unneeded equipment is switched off. A two-minute check makes tomorrow easier."),
   ]),
   ("p", "None of this requires perfection. It simply makes thoughtful choices easier to repeat."),
   ("h", "Choose essentials that work beyond home"),
   ("p", "Start with what you already use regularly rather than buying a new collection of products."),
   ("b", [
     ("Lunch and hydration:", "reusable food containers, snack bags, and water bottles reduce dependence on disposable packaging. Explore Mimro’s Kitchen Solutions collection for food-storage and on-the-go options."),
     ("Reusable cleaning tools:", f"a cloth in your work bag or home office handles everyday spills and surfaces. The {P['swe']} is made from 70% cellulose wood pulp and 30% cotton, is machine washable, dries fast, and is designed for 100+ washes."),
     ("Personal care on the go:", "long workdays and commutes make portable formats useful. Shampoo and conditioner bars and toothpaste and mouthwash tablets offer alternatives to some bottled formats. Choose what suits your routine, storage, and travel needs."),
   ]),
   ("p", "The goal isn’t to carry every sustainable product to work. It’s to keep a few useful essentials within reach so better choices are practical, not inconvenient."),
   ("btn", ["kitchen", "clean", "care"]),
   ("h", "Shop for the workday you actually have"),
   ("p", "Your needs depend on how you work. An office commuter may benefit most from reusable lunch containers, while someone working from home might prioritize washable cloths or kitchen essentials. Start by identifying one recurring source of waste, then find the product that fits that specific need."),
   ("btn", ["top", "all"]),
   ("h", "Let Mimro AI help you find the right fit"),
   ("p", "Not sure what makes sense for your working routine? Ask Mimro AI, our eco-shopping assistant, a simple question: What reusable essentials would make my commute easier? How can I cut lunch packaging? What fits my home-office routine? Starting with a real need helps you avoid products that end up unused in a drawer."),
   ("h", "Take better habits beyond the clock"),
   ("p", "Sustainable living doesn’t stop at your front door, and it doesn’t need to interrupt your productivity. It can start with the container you bring to lunch, the journey you choose when practical, or the equipment you switch off."),
   ("strong", "Choose one change this week. Make it easy to repeat, then build from there. Small decisions matter when they’re part of how you work every day."),
  ]),
]


def strip_tags(s):
    s = re.sub(r'<a href="([^"]+)">([^<]+)</a>', r"[\2](\1)", s)
    s = re.sub(r"</?em>", "*", s)
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def to_md(post):
    lines = [f"**Status:** Draft (unpublished) on Shopify",
             f"**Title:** {post['title']}",
             f"**Handle:** /blogs/news/{post['slug']}",
             f"**Tags:** {', '.join(TAGS)}",
             f"![{post['title']}]({IMG_BASE}{post['img']})", "---"]
    for kind, val in post["blocks"]:
        if kind == "p":
            lines.append(strip_tags(val))
        elif kind == "strong":
            lines.append(f"**{strip_tags(val)}**")
        elif kind == "h":
            lines.append(f"## {val}")
        elif kind == "n":
            lines += [f"{i}. **{a}** {strip_tags(b)}".rstrip() for i, (a, b) in enumerate(val, 1)]
        elif kind == "b":
            lines += [f"- **{a}** {strip_tags(b)}" for a, b in val]
        elif kind == "btn":
            lines += [f"**[{C[k][0]} →]({SITE}{C[k][1]})**" for k in val]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    for post in POSTS:
        base = os.path.join(here, f"{post['n']}-{post['slug']}")
        body = render(post["blocks"])
        first = next(v for k, v in post["blocks"] if k == "p")
        art = {"article": {"blogId": BLOG_ID, "title": post["title"], "handle": post["slug"],
                           "author": {"name": "Mimro"}, "body": body, "summary": f"<p>{first}</p>",
                           "tags": TAGS, "isPublished": False, "templateSuffix": "article",
                           "image": {"url": IMG_BASE + post["img"], "altText": post["title"]}}}
        open(base + ".html", "w").write(body)
        open(base + ".json", "w").write(json.dumps(art, ensure_ascii=False))
        open(base + ".md", "w").write(to_md(post))
        print(post["n"], post["slug"], len(strip_tags(body).split()), "words")
