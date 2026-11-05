# Businesses Without a Website Finder

Find **local businesses that have no website** in any city, region or country, and sell them one.

Type a location ("Lyon, France", "Austin, Texas", "Bavaria, Germany"), pick categories (restaurants, hair salons, garages, plumbers, bakeries…) and get a clean list of places that have **no website listed**, with their phone, email, Facebook or Instagram page and address.

Data comes from **OpenStreetMap**, the open map maintained by millions of contributors. No Google scraping, no proxy, no login, so runs are fast and cheap.

## Why it is useful

- **Web agencies and freelancers**: every row is a business that needs a website.
- **Local marketing, POS, booking and delivery apps**: find businesses that are still offline.
- **Market research**: measure how many restaurants or salons in a city are without a website.

`onlySocialMedia: true` flags businesses that rely on a Facebook or Instagram page instead of a website: usually the warmest leads.

## Output

| Field | Example |
|---|---|
| `name`, `category` | Le Petit Zinc, amenity=restaurant |
| `phone`, `email` | +33 4 50 …, contact@… (when the business published them) |
| `facebook`, `instagram`, `onlySocialMedia` | page URL, true |
| `address`, `postcode`, `city` | 12 rue Royale, 74000, Annecy |
| `openingHours` | Mo-Sa 09:00-19:00 |
| `latitude`, `longitude`, `osmUrl` | GPS and the map link |

Export to CSV, Excel or JSON, or send to Google Sheets, HubSpot, Make or Zapier.

## Input example

```json
{
  "locations": ["Lyon, France", "Grenoble, France"],
  "categories": ["restaurants", "beauty"],
  "requireContact": "phone",
  "maxResults": 1000
}
```

## Tips

- Big areas (a whole country) can take a few minutes; split them into regions for speed.
- Coverage depends on the area: OpenStreetMap is very complete in Europe and big cities.
- Chains and franchises are skipped by default.

## Legal

Data © OpenStreetMap contributors, available under the Open Database License (ODbL). Contact details are the ones the businesses published publicly. You remain responsible for how you contact them (GDPR, CAN-SPAM, local rules on B2B prospecting): always include an opt-out.

## Pricing

Pay per result: you only pay for businesses saved to the dataset.

Made by [Frix Studio](https://frix-studio.vercel.app).
