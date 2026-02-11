---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront/latest/queries/products",
    "fetched_at": "2026-02-10T13:41:25.513331",
    "status": 200,
    "size_bytes": 364149
  },
  "metadata": {
    "title": "products - Storefront API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "queries",
    "component": "products"
  }
}
---

# products - Storefront API

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to products](/docs/api/storefront/latest/queries/products#top)# productsqueryAsk assistantReturns a list of the shop's products. For storefront search, use the [`search`](https://shopify.dev/docs/api/storefront/latest/queries/search) query.

[Anchor to Arguments](/docs/api/storefront/latest/queries/products#arguments)## ProductConnection arguments•[ProductConnection!](/docs/api/storefront/latest/connections/ProductConnection)- after (String)- before (String)- first (Int)- last (Int)- query (String)- reverse (Boolean)- sortKey (ProductSortKeys)[Anchor to after](/docs/api/storefront/latest/queries/products#arguments-after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to before](/docs/api/storefront/latest/queries/products#arguments-before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to first](/docs/api/storefront/latest/queries/products#arguments-first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to last](/docs/api/storefront/latest/queries/products#arguments-last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to query](/docs/api/storefront/latest/queries/products#arguments-query)query•[String](/docs/api/storefront/latest/scalars/String)You can apply one or multiple filters to a query.

Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/storefront/latest/queries/products#argument-query-filter-available_for_sale)available_for_sale•Filter by products that have at least one product variant available for sale.

[Anchor to ](/docs/api/storefront/latest/queries/products#argument-query-filter-created_at)created_at•Filter by the date and time when the product was created.

Example:- `created_at:>'2020-10-21T23:39:20Z'`- `created_at:<now`- `created_at:<=2024`[Anchor to ](/docs/api/storefront/latest/queries/products#argument-query-filter-product_type)product_type•Filter by a comma-separated list of [product types](https://help.shopify.com/en/manual/products/details/product-type).

Example:- `product_type:snowboard`[Anchor to ](/docs/api/storefront/latest/queries/products#argument-query-filter-tag)tag•Filter products by the product [`tags`](https://shopify.dev/docs/api/storefront/latest/objects/Product#field-tags) field.

Example:- `tag:my_tag`[Anchor to ](/docs/api/storefront/latest/queries/products#argument-query-filter-tag_not)tag_not•Filter by products that don't have the specified product [tags](https://shopify.dev/docs/api/storefront/latest/objects/Product#field-tags).

Example:- `tag_not:my_tag`[Anchor to ](/docs/api/storefront/latest/queries/products#argument-query-filter-title)title•Filter by the product [`title`](https://shopify.dev/docs/api/storefront/latest/objects/Product#field-title) field.

Example:- `title:The Minimal Snowboard`[Anchor to ](/docs/api/storefront/latest/queries/products#argument-query-filter-updated_at)updated_at•Filter by the date and time when the product was last updated.

Example:- `updated_at:>'2020-10-21T23:39:20Z'`- `updated_at:<now`- `updated_at:<=2024`[Anchor to ](/docs/api/storefront/latest/queries/products#argument-query-filter-variants.price)variants.price•Filter by the price of the product's variants.

[Anchor to ](/docs/api/storefront/latest/queries/products#argument-query-filter-vendor)vendor•Filter by the product [`vendor`](https://shopify.dev/docs/api/storefront/latest/objects/Product#field-vendor) field.

Example:- `vendor:Snowdevil`- `vendor:Snowdevil OR vendor:Icedevil`[Anchor to reverse](/docs/api/storefront/latest/queries/products#arguments-reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/storefront/latest/queries/products#arguments-sortKey)sortKey•[ProductSortKeys](/docs/api/storefront/latest/enums/ProductSortKeys)Default:IDSort the underlying list by the given key.

Show enum valuesWas this section helpful?YesNo## [Anchor to Possible returns](/docs/api/storefront/latest/queries/products#possible-returns)Possible returns- edges ([ProductEdge!]!)- filters ([Filter!]!)- nodes ([Product!]!)- pageInfo (PageInfo!)[Anchor to edges](/docs/api/storefront/latest/queries/products#returns-edges)edges•[[ProductEdge!]!](/docs/api/storefront/latest/objects/ProductEdge)non-nullA list of edges.

Show fields[Anchor to filters](/docs/api/storefront/latest/queries/products#returns-filters)filters•[[Filter!]!](/docs/api/storefront/latest/objects/Filter)non-nullA list of available filters.

Show fields[Anchor to nodes](/docs/api/storefront/latest/queries/products#returns-nodes)nodes•[[Product!]!](/docs/api/storefront/latest/objects/Product)non-nullA list of the nodes contained in ProductEdge.

Show fields[Anchor to pageInfo](/docs/api/storefront/latest/queries/products#returns-pageInfo)pageInfo•[PageInfo!](/docs/api/storefront/latest/objects/PageInfo)non-nullInformation to aid in pagination.

Show fieldsWas this section helpful?YesNo## Examples- ### Retrieve first three products#### DescriptionThe following example shows how to query for first three products.

#### Query```

query getProducts($first: Int) {

products(first: $first) {

edges {

cursor

node {

title

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

"query": "query getProducts($first: Int) { products(first: $first) { edges { cursor node { title } } } }"

}'

```#### React Router```

import { unauthenticated } from "../shopify.server";

export const loader = async () => {

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query getProducts($first: Int) {

products(first: $first) {

edges {

cursor

node {

title

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

data: `query getProducts($first: Int) {

products(first: $first) {

edges {

cursor

node {

title

}

}

}

}`,

});

```#### Response```

{

"products": {

"edges": [

{

"cursor": "eyJsYXN0X2lkIjo2NTcyMTE2NSwibGFzdF92YWx1ZSI6IjY1NzIxMTY1In0=",

"node": {

"title": "Storefront Spoon"

}

},

{

"cursor": "eyJsYXN0X2lkIjoyNjMwNzE4NTYsImxhc3RfdmFsdWUiOiIyNjMwNzE4NTYifQ==",

"node": {

"title": "Storefront Shoes"

}

},

{

"cursor": "eyJsYXN0X2lkIjo1Mzg4MjUyNjEsImxhc3RfdmFsdWUiOiI1Mzg4MjUyNjEifQ==",

"node": {

"title": "Guitar"

}

}

]

}

}

```- ### Retrieve first three products in reverse order#### DescriptionThe following example shows how to query for first three products in reverse order.

#### Query```

query getProducts($first: Int, $reverse: Boolean) {

products(first: $first, reverse: $reverse) {

edges {

cursor

node {

title

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

"query": "query getProducts($first: Int, $reverse: Boolean) { products(first: $first, reverse: $reverse) { edges { cursor node { title } } } }"

}'

```#### React Router```

import { unauthenticated } from "../shopify.server";

export const loader = async () => {

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query getProducts($first: Int, $reverse: Boolean) {

products(first: $first, reverse: $reverse) {

edges {

cursor

node {

title

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

data: `query getProducts($first: Int, $reverse: Boolean) {

products(first: $first, reverse: $reverse) {

edges {

cursor

node {

title

}

}

}

}`,

});

```#### Response```

{

"products": {

"edges": [

{

"cursor": "eyJsYXN0X2lkIjo5Mjk4OTg0NjUsImxhc3RfdmFsdWUiOiI5Mjk4OTg0NjUifQ==",

"node": {

"title": "Camper Van"

}

},

{

"cursor": "eyJsYXN0X2lkIjo1Mzg4MjUyNjEsImxhc3RfdmFsdWUiOiI1Mzg4MjUyNjEifQ==",

"node": {

"title": "Guitar"

}

},

{

"cursor": "eyJsYXN0X2lkIjoyNjMwNzE4NTYsImxhc3RfdmFsdWUiOiIyNjMwNzE4NTYifQ==",

"node": {

"title": "Storefront Shoes"

}

}

]

}

}

```- ### Retrieve first two products after cursor#### DescriptionThe following example shows how to query for first two products after cursor.

#### Query```

query getProducts($first: Int, $after: String) {

products(first: $first, after: $after) {

edges {

cursor

node {

title

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

"query": "query getProducts($first: Int, $after: String) { products(first: $first, after: $after) { edges { cursor node { title } } } }"

}'

```#### React Router```

import { unauthenticated } from "../shopify.server";

export const loader = async () => {

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query getProducts($first: Int, $after: String) {

products(first: $first, after: $after) {

edges {

cursor

node {

title

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

data: `query getProducts($first: Int, $after: String) {

products(first: $first, after: $after) {

edges {

cursor

node {

title

}

}

}

}`,

});

```#### Response```

{

"products": {

"edges": [

{

"cursor": "eyJsYXN0X2lkIjoyNjMwNzE4NTYsImxhc3RfdmFsdWUiOiIyNjMwNzE4NTYifQ==",

"node": {

"title": "Storefront Shoes"

}

},

{

"cursor": "eyJsYXN0X2lkIjo1Mzg4MjUyNjEsImxhc3RfdmFsdWUiOiI1Mzg4MjUyNjEifQ==",

"node": {

"title": "Guitar"

}

}

]

}

}

```- ### Retrieve last two products before cursor#### DescriptionThe following example shows how to query for last two products before cursor.

#### Query```

query getProducts($last: Int, $before: String) {

products(last: $last, before: $before) {

edges {

cursor

node {

title

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

"query": "query getProducts($last: Int, $before: String) { products(last: $last, before: $before) { edges { cursor node { title } } } }"

}'

```#### React Router```

import { unauthenticated } from "../shopify.server";

export const loader = async () => {

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query getProducts($last: Int, $before: String) {

products(last: $last, before: $before) {

edges {

cursor

node {

title

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

data: `query getProducts($last: Int, $before: String) {

products(last: $last, before: $before) {

edges {

cursor

node {

title

}

}

}

}`,

});

```#### Response```

{

"products": {

"edges": [

{

"cursor": "eyJsYXN0X2lkIjo2NTcyMTE2NSwibGFzdF92YWx1ZSI6IjY1NzIxMTY1In0=",

"node": {

"title": "Storefront Spoon"

}

},

{

"cursor": "eyJsYXN0X2lkIjoyNjMwNzE4NTYsImxhc3RfdmFsdWUiOiIyNjMwNzE4NTYifQ==",

"node": {

"title": "Storefront Shoes"

}

}

]

}

}

```- ### Retrieve product that matches the query#### DescriptionThe following example shows how to query product that matches the query.

#### Query```

query getProducts($first: Int, $query: String) {

products(first: $first, query: $query) {

edges {

cursor

node {

title

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

"query": "query getProducts($first: Int, $query: String) { products(first: $first, query: $query) { edges { cursor node { title } } } }"

}'

```#### React Router```

import { unauthenticated } from "../shopify.server";

export const loader = async () => {

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query getProducts($first: Int, $query: String) {

products(first: $first, query: $query) {

edges {

cursor

node {

title

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

data: `query getProducts($first: Int, $query: String) {

products(first: $first, query: $query) {

edges {

cursor

node {

title

}

}

}

}`,

});

```#### Response```

{

"products": {

"edges": [

{

"cursor": "eyJsYXN0X2lkIjo1Mzg4MjUyNjEsImxhc3RfdmFsdWUiOiI1Mzg4MjUyNjEifQ==",

"node": {

"title": "Guitar"

}

}

]

}

}

```- ### Retrieve products after sorting by a key#### DescriptionThe following example shows how to query products after sorting by a key.

#### Query```

query getProducts($first: Int, $sortKey: ProductSortKeys) {

products(first: $first, sortKey: $sortKey) {

edges {

cursor

node {

title

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

"query": "query getProducts($first: Int, $sortKey: ProductSortKeys) { products(first: $first, sortKey: $sortKey) { edges { cursor node { title } } } }"

}'

```#### React Router```

import { unauthenticated } from "../shopify.server";

export const loader = async () => {

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query getProducts($first: Int, $sortKey: ProductSortKeys) {

products(first: $first, sortKey: $sortKey) {

edges {

cursor

node {

title

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

data: `query getProducts($first: Int, $sortKey: ProductSortKeys) {

products(first: $first, sortKey: $sortKey) {

edges {

cursor

node {

title

}

}

}

}`,

});

```#### Response```

{

"products": {

"edges": [

{

"cursor": "eyJsYXN0X2lkIjo5Mjk4OTg0NjUsImxhc3RfdmFsdWUiOiJDYW1wZXIgVmFuIn0=",

"node": {

"title": "Camper Van"

}

},

{

"cursor": "eyJsYXN0X2lkIjo1Mzg4MjUyNjEsImxhc3RfdmFsdWUiOiJHdWl0YXIifQ==",

"node": {

"title": "Guitar"

}

},

{

"cursor": "eyJsYXN0X2lkIjoyNjMwNzE4NTYsImxhc3RfdmFsdWUiOiJTdG9yZWZyb250IFNob2VzIn0=",

"node": {

"title": "Storefront Shoes"

}

},

{

"cursor": "eyJsYXN0X2lkIjo2NTcyMTE2NSwibGFzdF92YWx1ZSI6IlN0b3JlZnJvbnQgU3Bvb24ifQ==",

"node": {

"title": "Storefront Spoon"

}

}

]

}

}

```## ExamplesRetrieve first three productsHide contentGQLcURLReact RouterNode.jsShow description[Open in GraphiQL](http://localhost:3457/graphiql?query=query%20getProducts(%24first%3A%20Int)%20%7B%0A%20%20products(first%3A%20%24first)%20%7B%0A%20%20%20%20edges%20%7B%0A%20%20%20%20%20%20cursor%0A%20%20%20%20%20%20node%20%7B%0A%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D)Copy9912345678910111213141516171819202122›⌄import { unauthenticated } from "../shopify.server";export const loader = async () => {  const { storefront } = await unauthenticated.storefront(    'your-development-store.myshopify.com'  );  const response = await storefront.graphql(    `#graphql  query getProducts($first: Int) {    products(first: $first) {      edges {        cursor        node {          title        }      }    }  }`,  );  const json = await response.json();  return json.data;}GQL```

query getProducts($first: Int) {

products(first: $first) {

edges {

cursor

node {

title

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

"query": "query getProducts($first: Int) { products(first: $first) { edges { cursor node { title } } } }"

}'

```React Router```

import { unauthenticated } from "../shopify.server";

export const loader = async () => {

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query getProducts($first: Int) {

products(first: $first) {

edges {

cursor

node {

title

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

data: `query getProducts($first: Int) {

products(first: $first) {

edges {

cursor

node {

title

}

}

}

}`,

});

```Hide content## ResponseJSON99123456789101112131415161718192021222324›⌄⌄⌄⌄⌄⌄⌄⌄⌄{  "products": {    "edges": [      {        "cursor": "eyJsYXN0X2lkIjo2NTcyMTE2NSwibGFzdF92YWx1ZSI6IjY1NzIxMTY1In0=",        "node": {          "title": "Storefront Spoon"        }      },      {        "cursor": "eyJsYXN0X2lkIjoyNjMwNzE4NTYsImxhc3RfdmFsdWUiOiIyNjMwNzE4NTYifQ==",        "node": {          "title": "Storefront Shoes"        }      },      {        "cursor": "eyJsYXN0X2lkIjo1Mzg4MjUyNjEsImxhc3RfdmFsdWUiOiI1Mzg4MjUyNjEifQ==",        "node": {          "title": "Guitar"        }      }    ]  }}### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)