---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront/latest/queries/collections",
    "fetched_at": "2026-02-10T13:41:28.285131",
    "status": 200,
    "size_bytes": 334838
  },
  "metadata": {
    "title": "collections - Storefront API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "queries",
    "component": "collections"
  }
}
---

# collections - Storefront API

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to collections](/docs/api/storefront/latest/queries/collections#top)# collectionsqueryAsk assistantList of the shop’s collections.

[Anchor to Arguments](/docs/api/storefront/latest/queries/collections#arguments)## CollectionConnection arguments•[CollectionConnection!](/docs/api/storefront/latest/connections/CollectionConnection)- after (String)- before (String)- first (Int)- last (Int)- query (String)- reverse (Boolean)- sortKey (CollectionSortKeys)[Anchor to after](/docs/api/storefront/latest/queries/collections#arguments-after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to before](/docs/api/storefront/latest/queries/collections#arguments-before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to first](/docs/api/storefront/latest/queries/collections#arguments-first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to last](/docs/api/storefront/latest/queries/collections#arguments-last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to query](/docs/api/storefront/latest/queries/collections#arguments-query)query•[String](/docs/api/storefront/latest/scalars/String)Apply one or multiple filters to the query.

Refer to the detailed [search syntax](https://shopify.dev/api/usage/search-syntax) for more information about using filters.

Show filters[Anchor to ](/docs/api/storefront/latest/queries/collections#argument-query-filter-collection_type)collection_type•[Anchor to ](/docs/api/storefront/latest/queries/collections#argument-query-filter-title)title•[Anchor to ](/docs/api/storefront/latest/queries/collections#argument-query-filter-updated_at)updated_at•[Anchor to reverse](/docs/api/storefront/latest/queries/collections#arguments-reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/storefront/latest/queries/collections#arguments-sortKey)sortKey•[CollectionSortKeys](/docs/api/storefront/latest/enums/CollectionSortKeys)Default:IDSort the underlying list by the given key.

Show enum valuesWas this section helpful?YesNo## [Anchor to Possible returns](/docs/api/storefront/latest/queries/collections#possible-returns)Possible returns- edges ([CollectionEdge!]!)- nodes ([Collection!]!)- pageInfo (PageInfo!)- totalCount (UnsignedInt64!)[Anchor to edges](/docs/api/storefront/latest/queries/collections#returns-edges)edges•[[CollectionEdge!]!](/docs/api/storefront/latest/objects/CollectionEdge)non-nullA list of edges.

Show fields[Anchor to nodes](/docs/api/storefront/latest/queries/collections#returns-nodes)nodes•[[Collection!]!](/docs/api/storefront/latest/objects/Collection)non-nullA list of the nodes contained in CollectionEdge.

Show fields[Anchor to pageInfo](/docs/api/storefront/latest/queries/collections#returns-pageInfo)pageInfo•[PageInfo!](/docs/api/storefront/latest/objects/PageInfo)non-nullInformation to aid in pagination.

Show fields[Anchor to totalCount](/docs/api/storefront/latest/queries/collections#returns-totalCount)totalCount•[UnsignedInt64!](/docs/api/storefront/latest/scalars/UnsignedInt64)non-nullThe total count of Collections.

Was this section helpful?YesNo## Examples- ### Retrieve collections#### DescriptionA collection represents a group of products that a store owner can create. The store owner can organize these product groups to make their stores easier to browse. For example, a merchant might create a collection for a specific type of product that they sell, such as footwear.

Merchants can create collections by selecting products individually or by defining rules that automatically determine whether products are included.

The following example shows how to query for collections and the products that belong to those collections.

#### Query```

query {

collections(first: 2) {

edges {

node {

id

products(first: 5) {

edges {

node {

id

}

}

}

}

}

}

}

```#### cURL```

curl -X POST \

https://your-development-store.myshopify.com/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

-H 'X-Shopify-Storefront-Access-Token: {storefront_access_token}' \

-d '{

"query": "query { collections(first: 2) { edges { node { id products(first: 5) { edges { node { id } } } } } } }"

}'

```#### React Router```

import { unauthenticated } from "../shopify.server";

export const loader = async () => {

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query {

collections(first: 2) {

edges {

node {

id

products(first: 5) {

edges {

node {

id

}

}

}

}

}

}

}`,

);

const json = await response.json();

return json.data;

}

```#### Node.js```

const client = new shopify.clients.Storefront({

domain: 'your-development-store.myshopify.com',

storefrontAccessToken,

});

const data = await client.query({

data: `query {

collections(first: 2) {

edges {

node {

id

products(first: 5) {

edges {

node {

id

}

}

}

}

}

}

}`,

});

```#### Response```

{

"collections": {

"edges": [

{

"node": {

"id": "gid://shopify/Collection/547751128",

"products": {

"edges": [

{

"node": {

"id": "gid://shopify/Product/929898465"

}

},

{

"node": {

"id": "gid://shopify/Product/538825261"

}

}

]

}

}

},

{

"node": {

"id": "gid://shopify/Collection/585546552",

"products": {

"edges": []

}

}

}

]

}

}

```## Retrieve collectionsHide contentGQLcURLReact RouterNode.jsShow description[Open in GraphiQL](http://localhost:3457/graphiql?query=query%20%7B%0A%20%20collections(first%3A%202)%20%7B%0A%20%20%20%20edges%20%7B%0A%20%20%20%20%20%20node%20%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20products(first%3A%205)%20%7B%0A%20%20%20%20%20%20%20%20%20%20edges%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20node%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D)Copy9912345678910111213141516171819202122232425262728›⌄import { unauthenticated } from "../shopify.server";export const loader = async () => {  const { storefront } = await unauthenticated.storefront(    'your-development-store.myshopify.com'  );  const response = await storefront.graphql(    `#graphql  query {    collections(first: 2) {      edges {        node {          id          products(first: 5) {            edges {              node {                id              }            }          }        }      }    }  }`,  );  const json = await response.json();  return json.data;}GQL```

query {

collections(first: 2) {

edges {

node {

id

products(first: 5) {

edges {

node {

id

}

}

}

}

}

}

}

```cURL```

curl -X POST \

https://your-development-store.myshopify.com/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

-H 'X-Shopify-Storefront-Access-Token: {storefront_access_token}' \

-d '{

"query": "query { collections(first: 2) { edges { node { id products(first: 5) { edges { node { id } } } } } } }"

}'

```React Router```

import { unauthenticated } from "../shopify.server";

export const loader = async () => {

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query {

collections(first: 2) {

edges {

node {

id

products(first: 5) {

edges {

node {

id

}

}

}

}

}

}

}`,

);

const json = await response.json();

return json.data;

}

```Node.js```

const client = new shopify.clients.Storefront({

domain: 'your-development-store.myshopify.com',

storefrontAccessToken,

});

const data = await client.query({

data: `query {

collections(first: 2) {

edges {

node {

id

products(first: 5) {

edges {

node {

id

}

}

}

}

}

}

}`,

});

```Hide content## ResponseJSON99123456789101112131415161718192021222324252627282930313233›⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄{  "collections": {    "edges": [      {        "node": {          "id": "gid://shopify/Collection/547751128",          "products": {            "edges": [              {                "node": {                  "id": "gid://shopify/Product/929898465"                }              },              {                "node": {                  "id": "gid://shopify/Product/538825261"                }              }            ]          }        }      },      {        "node": {          "id": "gid://shopify/Collection/585546552",          "products": {            "edges": []          }        }      }    ]  }}### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)