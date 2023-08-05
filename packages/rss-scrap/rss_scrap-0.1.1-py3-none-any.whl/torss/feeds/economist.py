import re
import urllib.parse
import asyncio

from torss.feed import Channel, Feed, Item
from torss.utils import fetch_bs, expect


async def fetch_urls(session):
    url = "https://www.economist.com/weeklyedition"

    soup = await fetch_bs(session, url)

    world_this_week = soup.find(re.compile(r"h\d"), string="The world this week")
    expect(world_this_week, "Couldn't get 'The world this week section'")
    section = world_this_week.find_parent("section")

    politics = section.find("a", string=re.compile(r"Politics.*"))
    business = section.find("a", string=re.compile(r"Business.*"))

    # KAL's uses a real typographic apostrophe (KAL’s cartoon) so to be safe,
    # let's skip it entirely with regular expression
    kal = section.find("a", string=re.compile(r"KAL.*cartoon"))

    urljoin = urllib.parse.urljoin

    ret = {}
    if politics:
        ret["politics"] = urljoin(url, politics["href"])
    if business:
        ret["business"] = urljoin(url, business["href"])
    if kal:
        ret["kal"] = urljoin(url, kal["href"])
    return ret


async def parse_article(session, url):
    def _body_filter(tag):
        if tag.name == "p":
            return any("article" in cls for cls in tag.get("class", []))
        if tag.name in ("h1", "h2", "h3"):
            return tag.text != "Listen on the go"
        if tag.name == "img":
            return True
        return False

    contents = []

    soup = await fetch_bs(session, url)
    main = soup.find("main", id="content")

    lead = main.find(class_="article__lead-image")
    if lead:
        contents.extend(lead.find_all("img"))

    body = main.find(class_="layout-article-body")
    contents.extend(body.find_all(_body_filter))

    return "\n".join(str(elem) for elem in contents)


async def politics(session, urls):
    expect("politics" in urls, "URL for Politics this week not found")
    url = urls["politics"]

    ch = Channel("The Economist: Politics this week", "https://www.economist.com")
    ch.items.append(
        Item(
            title="Politics this week",
            link=url,
            content=await parse_article(session, url),
        )
    )
    return Feed(ch, "politics.xml")


async def business(session, urls):
    expect("business" in urls, "URL for Business this week not found")
    url = urls["business"]

    ch = Channel("The Economist: Business this week", "https://www.economist.com")
    ch.items.append(
        Item(
            title="Business this week",
            link=url,
            content=await parse_article(session, url),
        )
    )
    return Feed(ch, "business.xml")


async def kal(session, urls):
    expect("kal" in urls, "URL for KAL's cartoon not found")
    url = urls["kal"]

    ch = Channel("The Economist: KAL's cartoon", "https://www.economist.com")
    ch.items.append(
        Item(
            title="KAL's cartoon",
            link=url,
            content=await parse_article(session, url),
        )
    )
    return Feed(ch, "kal.xml")


async def run(session, **kw):
    urls = await fetch_urls(session)
    feeds = await asyncio.gather(
        politics(session, urls), business(session, urls), kal(session, urls)
    )
    return feeds
