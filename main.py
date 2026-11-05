import asyncio
from apify import Actor
from core import CATEGORIES, area_id, build_query, overpass, row


async def main():
    async with Actor:
        inp = await Actor.get_input() or {}
        locations = [l.strip() for l in inp.get('locations') or [] if l.strip()]
        if not locations:
            await Actor.fail(status_message='Add at least one location, e.g. "Lyon, France".'); return
        cats = inp.get('categories') or list(CATEGORIES)
        contact = inp.get('requireContact', 'any')
        limit = max(1, min(int(inp.get('maxResults') or 500), 50000))
        seen, pushed = set(), 0
        for loc in locations:
            area, label = await asyncio.to_thread(area_id, loc)
            await asyncio.sleep(1.1)  # Nominatim fair-use: 1 request/second
            if not area:
                Actor.log.warning(f'Location not found: {loc}'); continue
            Actor.log.info(f'Searching {label}')
            data = await asyncio.to_thread(overpass, build_query(area, cats, contact))
            for el in data.get('elements', []):
                r = row(el)
                key = r['osmUrl']
                if key in seen or (inp.get('skipChains', True) and el.get('tags', {}).get('brand')): continue
                seen.add(key); r['searchLocation'] = loc
                res = await Actor.push_data(r, charged_event_name='lead')
                pushed += 1
                if (res and res.event_charge_limit_reached) or pushed >= limit: break
            if pushed >= limit: break
        await Actor.set_status_message(f'{pushed} businesses without a website saved')

if __name__ == '__main__':
    asyncio.run(main())
