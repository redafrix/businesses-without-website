"""Find local businesses that have no website, from OpenStreetMap (Overpass API)."""
import json, time, urllib.parse, urllib.request

UA = 'frix-studio-nosite-actor/1.0 (https://frix-studio.vercel.app)'
OVERPASS = ['https://overpass-api.de/api/interpreter', 'https://overpass.private.coffee/api/interpreter',
            'https://maps.mail.ru/osm/tools/overpass/api/interpreter', 'https://overpass.kumi.systems/api/interpreter']
CATEGORIES = {
    'restaurants': '["amenity"~"^(restaurant|cafe|fast_food|bar|pub|ice_cream)$"]',
    'beauty': '["shop"~"^(hairdresser|beauty|cosmetics|tattoo|massage)$"]',
    'food_shops': '["shop"~"^(bakery|pastry|butcher|deli|greengrocer|wine|alcohol|cheese|confectionery|seafood)$"]',
    'retail': '["shop"~"^(clothes|shoes|jewelry|gift|florist|optician|bicycle|furniture|books|toys|sports|electronics|mobile_phone|pet)$"]',
    'auto': '["shop"~"^(car_repair|car|tyres|motorcycle|car_parts)$"]',
    'trades': '["craft"]',
    'health': '["amenity"~"^(dentist|doctors|clinic|veterinary|pharmacy)$"]',
    'fitness': '["leisure"~"^(fitness_centre|sports_centre|dance)$"]',
    'lodging': '["tourism"~"^(hotel|guest_house|hostel|motel|apartment)$"]',
}


def get(url, data=None, tries=2, timeout=200):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers={'User-Agent': UA, 'Accept': '*/*'})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except Exception:
            if i == tries - 1: raise
            time.sleep(5 * (i + 1))


def area_id(location):
    """Geocode a place name ("Lyon", "Gironde, France", "Austin, TX") to an Overpass area id."""
    q = urllib.parse.urlencode({'q': location, 'format': 'json', 'limit': 5})
    for hit in get(f'https://nominatim.openstreetmap.org/search?{q}'):
        if hit.get('osm_type') == 'relation':
            return 3600000000 + int(hit['osm_id']), hit['display_name']
    return None, None


def build_query(area, cats, contact):
    must = {'email': '[~"^(email|contact:email)$"~"."]', 'phone': '[~"^(phone|contact:phone|contact:mobile)$"~"."]'}.get(contact, '')
    lines = [f'nwr(area.a){CATEGORIES[c]}["name"][!"website"][!"contact:website"][!"url"]{must};' for c in cats if c in CATEGORIES]
    return f'[out:json][timeout:180];area({area})->.a;(\n' + '\n'.join(lines) + '\n);out tags center;'


def overpass(query, log=print):
    data = urllib.parse.urlencode({'data': query}).encode()
    last = None
    for url in OVERPASS:
        try: return get(url, data, tries=1, timeout=150)
        except Exception as e:
            log(f'{url.split("/")[2]} failed ({e}), trying the next mirror'); last = e
    raise last


def category_of(t):
    for k in ('amenity', 'shop', 'craft', 'leisure', 'tourism'):
        if t.get(k): return f'{k}={t[k]}'
    return ''


def row(el):
    t = el.get('tags', {}); c = el.get('center') or el
    addr = ' '.join(x for x in (t.get('addr:housenumber'), t.get('addr:street')) if x)
    social = {k.split(':')[-1]: t[k] for k in ('contact:facebook', 'contact:instagram', 'facebook', 'instagram') if t.get(k)}
    return {
        'name': t.get('name'), 'category': category_of(t),
        'email': t.get('email') or t.get('contact:email'),
        'phone': t.get('phone') or t.get('contact:phone') or t.get('contact:mobile'),
        'address': addr or None, 'postcode': t.get('addr:postcode'), 'city': t.get('addr:city'),
        'openingHours': t.get('opening_hours'), 'facebook': social.get('facebook'), 'instagram': social.get('instagram'),
        'onlySocialMedia': bool(social), 'hasWebsite': False,
        'latitude': c.get('lat'), 'longitude': c.get('lon'),
        'osmUrl': f"https://www.openstreetmap.org/{el['type']}/{el['id']}",
    }
