---
{
  "fetch": {
    "url": "https://shopify.dev/api/catalog-api/index",
    "fetched_at": "2026-02-10T13:39:59.200946",
    "status": 200,
    "size_bytes": 269760
  },
  "metadata": {
    "title": "Catalog API reference",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "catalog-api",
    "component": "index"
  }
}
---

# Catalog API reference

# Catalog API referenceThe Catalog API provides access to product data across all eligible Shopify merchants, enabling agentic commerce applications to search, discover, and retrieve detailed product information to render product details pages.Ask assistant

## [Anchor to Authentication](/docs/api/catalog-api/index#authentication)AuthenticationAll Catalog API requests require a valid bearer token.API keys created in the [Dev Dashboard](https://dev.shopify.com/dashboard/) provide a client ID and secret that can be used to generate a JWT token.POST## /auth/access_tokenCopy912345678curl --request POST \  --url https://api.shopify.com/auth/access_token \  --header 'Content-Type: application/json' \  --data '{    "client_id": "{your_client_id}",    "client_secret": "{your_client_secret}",    "grant_type": "client_credentials"  }'The response will contain:

- `access_token`: A JWT access token that can be used to interact with the Catalog API.

- `scope`: The list of access scopes that were granted to your API key.

- `expires_in`: The number of seconds until the access token expires.

## {} ResponseCopy912345{    "access_token": "f8563253df0bf277ec9ac6f649fc3f17",    "scope": "read_global_api_catalog_search",    "expires_in": 86399}Include your token as a `Authorization: Bearer {token}` header on all API queries.

JWT tokens created from Dev Dashboard credentials have a 60-minute TTL. You can use a JWT decoder tool like [`jwt.io`](https://www.jwt.io/) to investigate more details related to how Shopify issues this token.Learn more about [building agentic commerce experiences](/docs/agents/get-started/authentication).GET## /global/v2/searchCopy9123curl -X GET \  'https://discover.shopifyapps.com/global/v2/search?query=glossier%20lip%20balm' \  -H 'Authorization: Bearer {BEARER_TOKEN}'

## [Anchor to Endpoints and requests](/docs/api/catalog-api/index#endpoints-and-requests)Endpoints and requestsCatalog API endpoints are organized by resource type.

You'll need to use different endpoints depending on your agent's requirements.All Catalog API endpoints follow this pattern: `https://discover.shopifyapps.com/global//{resource}`.The Catalog API provides three main endpoints:

- **[Lookup](/docs/api/catalog-api/lookup):** Get detailed product information using a Universal Product ID (UPID).

- **[Lookup by variant](/docs/api/catalog-api/lookup-by-variant):** Get detailed product information using a Variant ID (VID).

- **[Search](/docs/api/catalog-api/search):** Search for products across the global Shopify Catalog.

The references and examples document `https://discover.shopifyapps.com/global/v2/search` as the endpoint, which assumes Search and Lookup against the entire Shopify catalog.

If you want your agents to make requests against a [saved catalog you've created in Dev Dashboard](/docs/api/catalog-api#saved-catalogs), update the endpoint URLs accordingly.For usage guidelines, see [About Catalog](/docs/api/catalog-api#usage-guidelines).

## [Anchor to Status and error codes](/docs/api/catalog-api/index#status-and-error-codes)Status and error codesAll API queries return HTTP status codes that can tell you more about the response.`200 OK`The request was successful.`400 Bad Request`The request contains invalid parameters. Check the `errors` object in the response for details.`401 Unauthorized`The bearer token is missing or invalid.`404 Not Found`The requested product (UPID) was not found.`429 Too Many Requests`Rate limit exceeded. Wait before retrying.## {} Sample error responses400401404Copy9123456789{  "errors": {    "limit": ["must be greater than or equal to 1"],    "max_price": ["must be greater than 0"],    "categories": {      "0": ["must be a Shopify Taxonomy category identifier"]    }  }}9123{  "error": "Unauthorized"}91234567{  "errors": {    "product": [      "Not found"    ]  }}400```

{

"errors": {

"limit": ["must be greater than or equal to 1"],

"max_price": ["must be greater than 0"],

"categories": {

"0": ["must be a Shopify Taxonomy category identifier"]

}

}

}

```401```

{

"error": "Unauthorized"

}

```404```

{

"errors": {

"product": [

"Not found"

]

}

}

```

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)