---
{
  "fetch": {
    "url": "https://shopify.dev/api/ajax/index",
    "fetched_at": "2026-02-10T13:39:31.577038",
    "status": 200,
    "size_bytes": 225610
  },
  "metadata": {
    "title": "About the Shopify Ajax API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "ajax",
    "component": "index"
  }
}
---

# About the Shopify Ajax API

ExpandOn this page- [Use cases](/docs/api/ajax/index#use-cases)- [Making requests to the API](/docs/api/ajax/index#making-requests-to-the-api)- [Locale-aware URLs](/docs/api/ajax/index#locale-aware-urls)- [Requirements and limitations](/docs/api/ajax/index#requirements-and-limitations)- [Tutorials](/docs/api/ajax/index#tutorials)

# About the Shopify Ajax APIAsk assistantThe Ajax API provides a suite of lightweight REST API endpoints for development of [Shopify themes](/docs/storefronts/themes). The Ajax API can only be used by themes that are hosted by Shopify. You can't use the Ajax API on a Shopify custom storefront.TipTo request the HTML markup for theme sections using an AJAX request, use the [Section Rendering API](/docs/api/ajax/section-rendering).**Tip:** To request the HTML markup for theme sections using an AJAX request, use the [Section Rendering API](/docs/api/ajax/section-rendering).

## [Anchor to Use cases](/docs/api/ajax/index#use-cases)Use casesPossible uses of the Ajax API include:

- Add products to the cart and update the cart item counter.

- Display related product recommendations.

- Suggest products and collections to visitors as they type in a search field.

Refer to the [Ajax API reference](/docs/api/ajax/reference/) for a full list of available API endpoints.

## [Anchor to Making requests to the API](/docs/api/ajax/index#making-requests-to-the-api)Making requests to the APIThe Ajax API accepts two types of HTTP requests:

- `GET` requests to read cart and some product data

- `POST` requests to update the cart for the current session

For instance, to fetch the current contents of the cart, send a client-side request to the store's `/cart.js` endpoint.Copy9123var cartContents = fetch(window.Shopify.routes.root + 'cart.js').then(response => response.json()).then(data => { return data });

## [Anchor to Locale-aware URLs](/docs/api/ajax/index#locale-aware-urls)Locale-aware URLsStores can have [dynamic URLs](/docs/storefronts/themes/markets/multiple-currencies-languages#locale-aware-urls) generated for them when they sell internationally or in multiple languages. When using the Ajax API, it's important to use dynamic, locale-aware URLs so that you can give visitors a consistent experience for the language and country that they've chosen.The global value `window.Shopify.routes.root` is available to use as a base when building locale-aware URLs in JavaScript. The global value will always end in a `/` character, so you can safely use simple string concatenation to build the full URLs.

## [Anchor to Requirements and limitations](/docs/api/ajax/index#requirements-and-limitations)Requirements and limitations

- This is an [unauthenticated](/docs/apps/build/authentication-authorization) API. It doesn't require access tokens or a client ID to access.

- There are no hard [rate limits](/docs/api/usage/limits#rate-limits) on the Ajax API. It's still subject to Shopify's standard API abuse-prevention measures.

- All API responses return JSON-formatted data.

- Product JSON responses are limited to a maximum of 250 variants.

- The Ajax API can't be used to read any customer or order data, or update any store data. If you need more extensive access, check the [GraphQL Admin API](/docs/api/admin-graphql).

## [Anchor to Tutorials](/docs/api/ajax/index#tutorials)Tutorials

- [Show product recommendations on product pages using the Ajax API](/docs/storefronts/themes/product-merchandising/recommendations)

Was this page helpful?YesNo- [Use cases](/docs/api/ajax/index#use-cases)- [Making requests to the API](/docs/api/ajax/index#making-requests-to-the-api)- [Locale-aware URLs](/docs/api/ajax/index#locale-aware-urls)- [Requirements and limitations](/docs/api/ajax/index#requirements-and-limitations)- [Tutorials](/docs/api/ajax/index#tutorials)### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)