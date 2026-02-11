---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-graphql",
    "fetched_at": "2026-02-10T13:39:41.119730",
    "status": 200,
    "size_bytes": 502778
  },
  "metadata": {
    "title": "GraphQL Admin API reference",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "api",
    "component": "admin-graphql"
  }
}
---

# GraphQL Admin API reference

# GraphQL Admin API referenceThe Admin API lets you build apps and integrations that extend and enhance the Shopify admin.This page will help you get up and running with Shopify’s GraphQL API.Ask assistant

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest

## [Anchor to Client libraries](/docs/api/admin-graphql/latest#client-libraries)Client librariesUse Shopify’s officially supported libraries to build fast, reliable apps with the programming languages and frameworks you already know.React Router

The official package for React Router applications.

- [Docs](/docs/api/shopify-app-react-router)

- [npm package](https://www.npmjs.com/package/@shopify/shopify-app-react-router)

- [GitHub repo](https://github.com/Shopify/shopify-app-js/tree/main/packages/apps/shopify-app-react-router#readme)

Node.js

The official client library for Node.js apps. No framework dependencies—works with any Node.js app.

- [Docs](https://github.com/Shopify/shopify-app-js/tree/main/packages/apps/shopify-api#readme)

- [npm package](https://www.npmjs.com/package/@shopify/shopify-api)

- [GitHub repo](https://github.com/Shopify/shopify-app-js/tree/main/packages/apps/shopify-api)

Ruby

The official client library for Ruby apps.

-

[Docs](https://shopify.github.io/shopify-api-ruby/)

-

[Ruby gem](https://rubygems.org/gems/shopify_api)

-

[GitHub repo](https://github.com/Shopify/shopify-api-ruby)

cURL

Use the [curl utility](https://curl.se/) to make API queries directly from the command line.Other

Need a different language? Check the list of [community-supported libraries](/apps/tools/api-libraries#third-party-admin-api-libraries).React RouterNode.jsRubycURLCopy912npm install -g @shopify/cli@latestshopify app init9123npm install --save @shopify/shopify-api# oryarn add @shopify/shopify-api91bundle add shopify_api912# cURL is often available by default on macOS and Linux.# See http://curl.se/docs/install.html for more details.React Router```

npm install -g @shopify/cli@latest

shopify app init

```Node.js```

npm install --save @shopify/shopify-api

# or

yarn add @shopify/shopify-api

```Ruby```

bundle add shopify_api

```cURL```

# cURL is often available by default on macOS and Linux.

# See http://curl.se/docs/install.html for more details.

```

## [Anchor to Authentication](/docs/api/admin-graphql/latest#authentication)AuthenticationAll GraphQL Admin API requests require a valid Shopify access token. If you use Shopify’s [client libraries](/apps/tools/api-libraries), then this will be done for you. Otherwise, you should include your token as a `X-Shopify-Access-Token` header on all GraphQL requests.Public and custom apps created in the Dev Dashboard generate tokens using [OAuth](/apps/auth/oauth), and custom apps made in the Shopify admin are [authenticated in the Shopify admin](/apps/auth/admin-app-access-tokens).To keep the platform secure, apps need to request specific [access scopes](/api/usage/access-scopes) during the install process. Only request as much data access as your app needs to work.Learn more about [getting started with authentication](/apps/auth) and [building apps](/apps/getting-started).React RouterNode.jsRubycURLCopy912345678import { authenticate } from "../shopify.server";export async function loader({request}) {  const { admin } = await authenticate.admin(request);  const response = await admin.graphql(    `query { shop { name } }`,  );}912const client = new shopify.clients.Graphql({session});const response = await client.query({data: 'query { shop { name } }'});912345678session = ShopifyAPI::Auth::Session.new(  shop: 'your-development-store.myshopify.com',  access_token: access_token,)client = ShopifyAPI::Clients::Graphql::Admin.new(  session: session,)response = client.query(query: 'query { shop { name } }')912345678# Replace {SHOPIFY_ACCESS_TOKEN} with your actual access token  curl -X POST \  https://{shop}.myshopify.com/admin/api/2026-01/graphql.json \  -H 'Content-Type: application/json' \  -H 'X-Shopify-Access-Token: {SHOPIFY_ACCESS_TOKEN}' \  -d '{  "query": "query { shop { name } }"  }'React Router```

import { authenticate } from "../shopify.server";

export async function loader({request}) {

const { admin } = await authenticate.admin(request);

const response = await admin.graphql(

`query { shop { name } }`,

);

}

```Node.js```

const client = new shopify.clients.Graphql({session});

const response = await client.query({data: 'query { shop { name } }'});

```Ruby```

session = ShopifyAPI::Auth::Session.new(

shop: 'your-development-store.myshopify.com',

access_token: access_token,

)

client = ShopifyAPI::Clients::Graphql::Admin.new(

session: session,

)

response = client.query(query: 'query { shop { name } }')

```cURL```

# Replace {SHOPIFY_ACCESS_TOKEN} with your actual access token

curl -X POST \

https://{shop}.myshopify.com/admin/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

-H 'X-Shopify-Access-Token: {SHOPIFY_ACCESS_TOKEN}' \

-d '{

"query": "query { shop { name } }"

}'

```

## [Anchor to Endpoints and queries](/docs/api/admin-graphql/latest#endpoints-and-queries)Endpoints and queriesGraphQL queries are executed by sending `POST` HTTP requests to the endpoint:`https://{store_name}.myshopify.com/admin/api/2026-01/graphql.json`Queries begin with one of the objects listed under [QueryRoot](/api/admin-graphql/2026-01/objects/queryroot). The QueryRoot is the schema’s entry-point for queries.Queries are equivalent to making a `GET` request in REST. The example shown is a query to get the ID and title of the first three products.Learn more about [API usage](/api/usage).NoteExplore and learn Shopify's Admin API using [GraphiQL Explorer](/apps/tools/graphiql-admin-api). To build queries and mutations with shop data, install [Shopify’s GraphiQL app](https://shopify-graphiql-app.shopifycloud.com/).**Note:** Explore and learn Shopify's Admin API using [GraphiQL Explorer](/apps/tools/graphiql-admin-api). To build queries and mutations with shop data, install [Shopify’s GraphiQL app](https://shopify-graphiql-app.shopifycloud.com/).POST## https://{store_name}.myshopify.com/admin/api/2026-01/graphql.jsonReact RouterNode.jsRubycURLCopy991234567891011121314151617181920import { authenticate } from "../shopify.server";export async function loader({request}) {  const { admin } = await authenticate.admin(request);  const response = await admin.graphql(    `#graphql    query getProducts {      products (first: 3) {        edges {          node {            id            title          }        }      }    }`,  );  const json = await response.json();  return { products: json?.data?.products?.edges };}9912345678910111213141516const queryString = `{  products (first: 3) {    edges {      node {        id        title      }    }  }}`// `session` is built as part of the OAuth processconst client = new shopify.clients.Graphql({session});const products = await client.query({  data: queryString,});991234567891011121314151617181920query = <<~GQL  {    products (first: 3) {      edges {        node {          id          title        }      }    }  }GQL# session is built as part of the OAuth processclient = ShopifyAPI::Clients::Graphql::Admin.new(  session: session)products = client.query(  query: query,)9912345678910111213141516# Get the ID and title of the three most recently added productscurl -X POST   https://{store_name}.myshopify.com/admin/api/2026-01/graphql.json \  -H 'Content-Type: application/json' \  -H 'X-Shopify-Access-Token: {access_token}' \  -d '{  "query": "{    products(first: 3) {      edges {        node {          id          title        }      }    }  }"}'React Router```

import { authenticate } from "../shopify.server";

export async function loader({request}) {

const { admin } = await authenticate.admin(request);

const response = await admin.graphql(

`#graphql

query getProducts {

products (first: 3) {

edges {

node {

id

title

}

}

}

}`,

);

const json = await response.json();

return { products: json?.data?.products?.edges };

}

```Node.js```

const queryString = `{

products (first: 3) {

edges {

node {

id

title

}

}

}

}`

// `session` is built as part of the OAuth process

const client = new shopify.clients.Graphql({session});

const products = await client.query({

data: queryString,

});

```Ruby```

query = <<~GQL

{

products (first: 3) {

edges {

node {

id

title

}

}

}

}

GQL

# session is built as part of the OAuth process

client = ShopifyAPI::Clients::Graphql::Admin.new(

session: session

)

products = client.query(

query: query,

)

```cURL```

# Get the ID and title of the three most recently added products

curl -X POST   https://{store_name}.myshopify.com/admin/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

-H 'X-Shopify-Access-Token: {access_token}' \

-d '{

"query": "{

products(first: 3) {

edges {

node {

id

title

}

}

}

}"

}'

```

## [Anchor to Rate limits](/docs/api/admin-graphql/latest#rate-limits)Rate limitsThe GraphQL Admin API is rate-limited using calculated query costs, measured in cost points. Each field returned by a query costs a set number of points. The total cost of a query is the maximum of possible fields selected, so more complex queries cost more to run.Learn more about [rate limits](/api/usage/limits#graphql-admin-api-rate-limits).{}## RequestCopy9123456789{  products(first: 1) {    edges {      node {        title      }    }  }}{}## ResponseCopy99123456789101112131415161718192021222324{  "data": {    "products": {      "edges": [        {          "node": {            "title": "Hiking backpack"          }        }      ]    }  },  "extensions": {    "cost": {      "requestedQueryCost": 3,      "actualQueryCost": 3,      "throttleStatus": {        "maximumAvailable": 1000.0,        "currentlyAvailable": 997,        "restoreRate": 50.0      }    }  }}

## [Anchor to Status and error codes](/docs/api/admin-graphql/latest#status-and-error-codes)Status and error codesAll API queries return HTTP status codes that contain more information about the response.### [Anchor to 200 OK](/docs/api/admin-graphql/latest#200-ok)200 OKGraphQL HTTP status codes are different from REST API status codes. Most importantly, the GraphQL API can return a `200 OK` response code in cases that would typically produce 4xx or 5xx errors in REST.### [Anchor to Error handling](/docs/api/admin-graphql/latest#error-handling)Error handlingThe response for the errors object contains additional detail to help you debug your operation.The response for mutations contains additional detail to help debug your query. To access this, you must request `userErrors`.#### Propertieserrors•arrayA list of all errors returned

Show error item propertieserrors[n].message•stringContains details about the error(s).

errors[n].extensions•objectProvides more information about the error(s) including properties and metadata.

Show extensions propertieserrors[n].extensions.code•stringShows error codes common to Shopify. Additional error codes may also be shown.

Show common error codesTHROTTLEDThe client has exceeded the [rate limit](#rate-limits). Similar to 429 Too Many Requests.

ACCESS_DENIEDThe client doesn’t have correct [authentication](#authentication) credentials. Similar to 401 Unauthorized.

SHOP_INACTIVEThe shop is not active. This can happen when stores repeatedly exceed API rate limits or due to fraud risk.

INTERNAL_SERVER_ERRORShopify experienced an internal error while processing the request. This error is returned instead of 500 Internal Server Error in most circumstances.

### [Anchor to 4xx and 5xx status codes](/docs/api/admin-graphql/latest#4xx-and-5xx-status-codes)4xx and 5xx status codesThe 4xx and 5xx errors occur infrequently. They are often related to network communications, your account, or an issue with Shopify’s services.Many errors that would typically return a 4xx or 5xx status code, return an HTTP 200 errors response instead. Refer to the [200 OK section](#200-ok) above for details.{}## Sample 200 error responsesThrottledInternal991234567891011121314151617181920{"errors": [  {    "message": "Query cost is 2003, which exceeds the single query max cost limit (1000).See https://shopify.dev/concepts/about-apis/rate-limits for more information on how thecost of a query is calculated.To query larger amounts of data with fewer limits, bulk operations should be used instead.See https://shopify.dev/tutorials/perform-bulk-operations-with-admin-api for usage details.",    "extensions": {      "code": "MAX_COST_EXCEEDED",      "cost": 2003,      "maxCost": 1000,      "documentation": "https://shopify.dev/api/usage/limits#rate-limits"    }  }]}99123456789101112{"errors": [  {    "message": "Internal error. Looks like something went wrong on our end.Request ID: 1b355a21-7117-44c5-8d8b-8948082f40a8 (include this in support requests).",    "extensions": {      "code": "INTERNAL_SERVER_ERROR",      "requestId": "1b355a21-7117-44c5-8d8b-8948082f40a8"    }  }]}Throttled```

{

"errors": [

{

"message": "Query cost is 2003, which exceeds the single query max cost limit (1000).

See https://shopify.dev/concepts/about-apis/rate-limits for more information on how the

cost of a query is calculated.

To query larger amounts of data with fewer limits, bulk operations should be used instead.

See https://shopify.dev/tutorials/perform-bulk-operations-with-admin-api for usage details.

",

"extensions": {

"code": "MAX_COST_EXCEEDED",

"cost": 2003,

"maxCost": 1000,

"documentation": "https://shopify.dev/api/usage/limits#rate-limits"

}

}

]

}

```Internal```

{

"errors": [

{

"message": "Internal error. Looks like something went wrong on our end.

Request ID: 1b355a21-7117-44c5-8d8b-8948082f40a8 (include this in support requests).",

"extensions": {

"code": "INTERNAL_SERVER_ERROR",

"requestId": "1b355a21-7117-44c5-8d8b-8948082f40a8"

}

}

]

}

```### [Anchor to 4xx and 5xx status codes](/docs/api/admin-graphql/latest#4xx-and-5xx-status-codes)4xx and 5xx status codesThe 4xx and 5xx errors occur infrequently. They are often related to network communications, your account, or an issue with Shopify’s services.Many errors that would typically return a 4xx or 5xx status code, return an HTTP 200 errors response instead. Refer to the [200 OK section](#200-ok) above for details.#### [Anchor to [object Object]](/docs/api/admin-graphql/latest#400-bad-request)400 Bad RequestThe server will not process the request.#### [Anchor to [object Object]](/docs/api/admin-graphql/latest#402-payment-required)402 Payment RequiredThe shop is frozen. The shop owner will need to pay the outstanding balance to [unfreeze](https://help.shopify.com/en/manual/your-account/pause-close-store#unfreeze-your-shopify-store) the shop.#### [Anchor to [object Object]](/docs/api/admin-graphql/latest#403-forbidden)403 ForbiddenThe shop is forbidden. Returned if the store has been marked as fraudulent.#### [Anchor to [object Object]](/docs/api/admin-graphql/latest#404-not-found)404 Not FoundThe resource isn’t available. This is often caused by querying for something that’s been deleted.#### [Anchor to [object Object]](/docs/api/admin-graphql/latest#423-locked)423 LockedThe shop isn’t available. This can happen when stores repeatedly exceed API rate limits or due to fraud risk.#### [Anchor to [object Object]](/docs/api/admin-graphql/latest#5xx-errors)5xx ErrorsAn internal error occurred in Shopify. Check out the [Shopify status page](https://www.shopifystatus.com) for more information.InfoDidn’t find the status code you’re looking for? View the complete list of

[API status response and error codes](/api/usage/response-codes).**Info:** Didn’t find the status code you’re looking for? View the complete list of

[API status response and error codes](/api/usage/response-codes).{}## Sample error codes4004024034044235009123456HTTP/1.1 400 Bad Request{  "errors": {    "query": "Required parameter missing or invalid"  }}91234HTTP/1.1 402 Payment Required{  "errors": "This shop's plan does not have access to this feature"}91234HTTP/1.1 403 Access Denied{  "errors": "User does not have access"}91234HTTP/1.1 404 Not Found{  "errors": "Not Found"}91234HTTP/1.1 423 Locked{  "errors": "This shop is unavailable"}91234HTTP/1.1 500 Internal Server Error{  "errors": "An unexpected error occurred"}400```

HTTP/1.1 400 Bad Request

{

"errors": {

"query": "Required parameter missing or invalid"

}

}

```402```

HTTP/1.1 402 Payment Required

{

"errors": "This shop's plan does not have access to this feature"

}

```403```

HTTP/1.1 403 Access Denied

{

"errors": "User does not have access"

}

```404```

HTTP/1.1 404 Not Found

{

"errors": "Not Found"

}

```423```

HTTP/1.1 423 Locked

{

"errors": "This shop is unavailable"

}

```500```

HTTP/1.1 500 Internal Server Error

{

"errors": "An unexpected error occurred"

}

```

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)