---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront",
    "fetched_at": "2026-02-10T13:39:22.092655",
    "status": 200,
    "size_bytes": 715284
  },
  "metadata": {
    "title": "Storefront API reference",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "api",
    "component": "storefront"
  }
}
---

# Storefront API reference

# GraphQL Storefront APICreate unique customer experiences with the Storefront API on any platform, including the web, apps, and games. The API offers a full range of commerce options making it possible for customers to view [products](/custom-storefronts/products-collections/getting-started) and [collections](/custom-storefronts/products-collections/filter-products), add products to a [cart](/custom-storefronts/cart/manage), and [check out](/custom-storefronts/checkout).Explore [Hydrogen](/custom-storefronts/hydrogen), Shopify’s official React-based framework for building headless commerce at global scale.Ask assistant

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest

## [Anchor to Development frameworks and SDKs](/docs/api/storefront/latest#development-frameworks-and-sdks)Development frameworks and SDKsUse Shopify’s officially supported libraries to build fast, reliable apps with the programming languages and frameworks you already know.cURL

Use the [curl utility](https://curl.se/) to make API queries directly from the command line.Hydrogen

A React-based framework for building custom storefronts on Shopify, Hydrogen has everything you need to build fast, and deliver personalized shopping experiences.

- [Docs](https://github.com/Shopify/hydrogen#readme)

- [npm package](https://www.npmjs.com/package/@shopify/hydrogen)

- [GitHub repo](https://github.com/Shopify/hydrogen)

Storefront API Client

The official lightweight client for any Javascript project interfacing with Storefront API and our recommended client for building custom storefronts without Hydrogen.

- [Docs](https://github.com/Shopify/shopify-app-js/tree/main/packages/api-clients/storefront-api-client#readme)

- [npm package](https://www.npmjs.com/package/@shopify/storefront-api-client)

- [GitHub repo](https://github.com/Shopify/shopify-app-js/tree/main/packages/api-clients/storefront-api-client)

React Router Apps

The official package for React Router apps.

- [Docs](/docs/api/shopify-app-react-router)

- [npm package](https://www.npmjs.com/package/@shopify/shopify-app-react-router)

- [GitHub repo](https://github.com/Shopify/shopify-app-template-react-router#readme)

Node.js

The official client library for Node.js applications, with full TypeScript support. It has no framework dependencies, so it can be used by any Node.js app.

- [Docs](https://github.com/Shopify/shopify-app-js/tree/main/packages/apps/shopify-api#readme)

- [npm package](https://www.npmjs.com/package/@shopify/shopify-api)

- [GitHub repo](https://github.com/Shopify/shopify-app-js/tree/main/packages/apps/shopify-api)

Shopify API (Apps)

The full suite library for TypeScript/JavaScript Shopify apps to access the GraphQL and REST Admin APIs and the Storefront API.

- [npm package](https://www.npmjs.com/package/@shopify/shopify-api)

- [GitHub repo](https://github.com/Shopify/shopify-app-js/tree/main/packages/apps/shopify-api)

Ruby

The official client library for Ruby applications. It has no framework dependencies, so it can be used by any Ruby app. This API applies a rate limit based on the IP address making the request, which will be your server’s address for all requests made by the library. Learn more about [rate limits](/api/usage/limits#rate-limits).

- [Docs](https://shopify.github.io/shopify-api-ruby/)

- [Ruby gem](https://rubygems.org/gems/shopify_api)

- [GitHub repo](https://github.com/Shopify/shopify-api-ruby)

Android

The official client library for Android apps.

- [Docs](https://github.com/Shopify/mobile-buy-sdk-android#readme)

- [GitHub repo](https://github.com/Shopify/mobile-buy-sdk-android)

iOS

The official client library for iOS applications.

- [Docs](https://github.com/Shopify/mobile-buy-sdk-ios#readme)

- [GitHub repo](https://github.com/Shopify/mobile-buy-sdk-ios)

Other

Other libraries are available in addition to the ones listed here. Check the list of [developer tools for custom storefronts](/custom-storefronts/tools).Shopify Hydrogen storefront creationStorefront API client installationShopify app React Router package installationShopify API installationShopify Ruby library installationCopy91234567npm init @shopify/hydrogen// ornpx @shopify/create-hydrogen// orpnpm create @shopify/create-hydrogen// oryarn create @shopify/hydrogen9123npm install --save @shopify/storefront-api-client// oryarn add @shopify/storefront-api-client9123npm install --save @shopify/shopify-app-react-router// oryarn add @shopify/shopify-app-react-router9123npm install --save @shopify/shopify-api// oryarn add @shopify/shopify-api91bundle add shopify_apiShopify Hydrogen storefront creation```

npm init @shopify/hydrogen

// or

npx @shopify/create-hydrogen

// or

pnpm create @shopify/create-hydrogen

// or

yarn create @shopify/hydrogen

```Storefront API client installation```

npm install --save @shopify/storefront-api-client

// or

yarn add @shopify/storefront-api-client

```Shopify app React Router package installation```

npm install --save @shopify/shopify-app-react-router

// or

yarn add @shopify/shopify-app-react-router

```Shopify API installation```

npm install --save @shopify/shopify-api

// or

yarn add @shopify/shopify-api

```Shopify Ruby library installation```

bundle add shopify_api

```

## [Anchor to Authentication](/docs/api/storefront/latest#authentication)AuthenticationThe Storefront API supports both tokenless access and token-based authentication.### [Anchor to Tokenless access](/docs/api/storefront/latest#tokenless-access)Tokenless accessTokenless access allows API queries without an access token providing access to essential features such as:

- Products and Collections

- Selling Plans

- Search

- Pages, Blogs, and Articles

- Cart (read/write)

Tokenless access has a query complexity limit of 1,000. Query complexity is calculated based on the cost of each field in the query. For more information, see the [Cost calculation](#rate-limits) section.### [Anchor to Token-based authentication](/docs/api/storefront/latest#token-based-authentication)Token-based authenticationFor access to all Storefront API features, an access token is required. The following features require token-based authentication:

- Product Tags

- Metaobjects and Metafields

- Menu (Online Store navigation)

- Customers

The Storefront API has the following types of token-based access:

- **Public access**: Used to query the API from a browser or mobile app.

- **Private access**: Used to query the API from a server or other private context, like a Hydrogen backend.

Learn more about [access tokens for the Storefront API](/api/usage/authentication#access-tokens-for-the-storefront-api).Tokenless (cURL)Token-based (cURL)HydrogenStorefront API ClientReact RouterShopify APIRubyCopy99123456789101112131415curl -X POST \  https://{shop}.myshopify.com/api/2026-01/graphql.json \  -H 'Content-Type: application/json' \  -d '{    "query": "{      products(first: 3) {        edges {          node {            id            title          }        }      }    }"  }'91234567curl -X POST \  https://{shop}.myshopify.com/api/2026-01/graphql.json \  -H 'Content-Type: application/json' \  -H 'X-Shopify-Storefront-Access-Token: {storefront-access-token}' \  -d '{    "query": "{your_query}"  }'912345const storefront = createStorefrontClient({publicStorefrontToken: env.PUBLIC_STOREFRONT_API_TOKEN,storeDomain: `https://\${env.PUBLIC_STORE_DOMAIN}\`,storefrontApiVersion: env.PUBLIC_STOREFRONT_API_VERSION || '2023-01',});91234567import {createStorefrontApiClient} from '@shopify/storefront-api-client';const client = createStorefrontApiClient({  storeDomain: 'http://your-shop-name.myshopify.com',  apiVersion: '2026-01',  publicAccessToken: <your-storefront-public-access-token>,});91234567import { authenticate } from "../shopify.server";// Use private access token on requests that don't come from Shopifyconst { storefront } = await unauthenticated.storefront(shop);// OR// Use private access token for app proxy requestsconst { storefront } = await authenticate.public.appProxy(request);9912345678910111213const adminApiClient = new shopify.clients.Rest({session});const storefrontTokenResponse = await adminApiClient.post({  path: 'storefront_access_tokens',  type: DataType.JSON,  data: {    storefront_access_token: {      title: 'This is my test access token',    },  },});const storefrontAccessToken =  storefrontTokenResponse.body['storefront_access_token']['access_token'];9912345678910111213141516# Create a REST client from your offline sessionclient = ShopifyAPI::Clients::Rest::Admin.new(  session: session)# Create a new access tokenstorefront_token_response = client.post(  path: 'storefront_access_tokens',  body: {    storefront_access_token: {      title: "This is my test access token",    }  })storefront_access_token = storefront_token_response.body['storefront_access_token']['access_token']Tokenless (cURL)```

curl -X POST \

https://{shop}.myshopify.com/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

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

```Token-based (cURL)```

curl -X POST \

https://{shop}.myshopify.com/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

-H 'X-Shopify-Storefront-Access-Token: {storefront-access-token}' \

-d '{

"query": "{your_query}"

}'

```Hydrogen```

const storefront = createStorefrontClient({

publicStorefrontToken: env.PUBLIC_STOREFRONT_API_TOKEN,

storeDomain: `https://\${env.PUBLIC_STORE_DOMAIN}\`,

storefrontApiVersion: env.PUBLIC_STOREFRONT_API_VERSION || '2023-01',

});

```Storefront API Client```

import {createStorefrontApiClient} from '@shopify/storefront-api-client';

const client = createStorefrontApiClient({

storeDomain: 'http://your-shop-name.myshopify.com',

apiVersion: '2026-01',

publicAccessToken: <your-storefront-public-access-token>,

});

```React Router```

import { authenticate } from "../shopify.server";

// Use private access token on requests that don't come from Shopify

const { storefront } = await unauthenticated.storefront(shop);

// OR

// Use private access token for app proxy requests

const { storefront } = await authenticate.public.appProxy(request);

```Shopify API```

const adminApiClient = new shopify.clients.Rest({session});

const storefrontTokenResponse = await adminApiClient.post({

path: 'storefront_access_tokens',

type: DataType.JSON,

data: {

storefront_access_token: {

title: 'This is my test access token',

},

},

});

const storefrontAccessToken =

storefrontTokenResponse.body['storefront_access_token']['access_token'];

```Ruby```

# Create a REST client from your offline session

client = ShopifyAPI::Clients::Rest::Admin.new(

session: session

)

# Create a new access token

storefront_token_response = client.post(

path: 'storefront_access_tokens',

body: {

storefront_access_token: {

title: "This is my test access token",

}

}

)

storefront_access_token = storefront_token_response.body['storefront_access_token']['access_token']

```

## [Anchor to Endpoints and queries](/docs/api/storefront/latest#endpoints-and-queries)Endpoints and queriesThe Storefront API is available only in GraphQL. There's no REST API for storefronts.All Storefront API queries are made on a single GraphQL endpoint, which only accepts `POST` requests:`https://{store_name}.myshopify.com/api/2026-01/graphql.json`### [Anchor to Versioning](/docs/api/storefront/latest#versioning)VersioningThe Storefront API is [versioned](/api/usage/versioning), with new releases four times a year. To keep your app stable, make sure that you specify a supported version in the URL.### [Anchor to GraphiQL explorer](/docs/api/storefront/latest#graphiql-explorer)GraphiQL explorerExplore and learn Shopify's Storefront API using the [GraphiQL explorer](/custom-storefronts/tools/graphiql-storefront-api). To build queries and mutations with shop data, install [Shopify's GraphiQL app](https://shopify-graphiql-app.shopifycloud.com/).### [Anchor to Usage limitations](/docs/api/storefront/latest#usage-limitations)Usage limitations

- Shopify Plus [bot protection](https://help.shopify.com/en/manual/checkout-settings/bot-protection) is only available for the [Cart](/custom-storefronts/cart/manage) object. It isn't available for the [Checkout](/custom-storefronts/checkout) object.

- You can't use Storefront API to duplicate existing Shopify functionality—be sure to check the API terms of service before you start.

POST## https://{store_name}.myshopify.com/api/2026-01/graphql.jsonTokenless requestToken-based requestHydrogenStorefront API ClientReact RouterShopify APIRubyCopy9912345678910111213141516# Get the ID and title of the three most recently added productscurl -X POST \  https://{store_name}.myshopify.com/api/2026-01/graphql.json \  -H 'Content-Type: application/json' \  -d '{    "query": "{      products(first: 3) {        edges {          node {            id            title          }        }      }    }"  }'991234567891011121314151617# Get the ID and title of the three most recently added productscurl -X POST \  https://{store_name}.myshopify.com/api/2026-01/graphql.json \  -H 'Content-Type: application/json' \  -H 'X-Shopify-Storefront-Access-Token: {storefront_access_token}' \  -d '{    "query": "{      products(first: 3) {        edges {          node {            id            title          }        }      }    }"  }'99123456789101112131415161718import {json} from '@shopify/remix-oxygen';export async function loader({context}) {  const PRODUCTS_QUERY = `#graphql    query products {      products(first: 3) {        edges {          node {            id            title          }        }      }    }  `;  const {products} = await context.storefront.query(PRODUCTS_QUERY);  return json({products});}99123456789101112131415const productQuery = `  query ProductQuery($handle: String) {    product(handle: $handle) {      id      title      handle    }  }`;const {data, errors, extensions} = await client.request(productQuery, {  variables: {    handle: 'sample-product',  },});9912345678910111213141516171819const { storefront } = await unauthenticated.storefront(  'your-development-store.myshopify.com');const response = await storefront.graphql(  `#graphql  query products {    products(first: 3) {      edges {        node {          id          title        }      }    }  }`,);const data = await response.json();99123456789101112131415161718192021222324// Load the access token as per instructions aboveconst storefrontAccessToken = '<my token>';// Shop from which we're fetching dataconst shop = 'my-shop.myshopify.com';// StorefrontClient takes in the shop url and the Storefront Access Token for that shop.const storefrontClient = new shopify.clients.Storefront({  domain: shop,  storefrontAccessToken,});// Use client.query and pass your query as \`data\`const products = await storefrontClient.query({  data: `{    products (first: 3) {      edges {        node {          id          title        }      }    }  }`,});9912345678910111213141516171819202122232425# Load the access token as per instructions abovestore_front_access_token = '<my token>'# Shop from which we're fetching datashop = 'my-shop.myshopify.com'# The Storefront client takes in the shop url and the Storefront Access Token for that shop.storefront_client = ShopifyAPI::Clients::Graphql::Storefront.new(  shop,  storefront_access_token)# Call query and pass your query as `data`my_query = <<~QUERY  {    products (first: 3) {      edges {        node {          id          title        }      }    }  }QUERYproducts = storefront_client.query(query: my_query)Tokenless request```

# Get the ID and title of the three most recently added products

curl -X POST \

https://{store_name}.myshopify.com/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

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

```Token-based request```

# Get the ID and title of the three most recently added products

curl -X POST \

https://{store_name}.myshopify.com/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

-H 'X-Shopify-Storefront-Access-Token: {storefront_access_token}' \

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

```Hydrogen```

import {json} from '@shopify/remix-oxygen';

export async function loader({context}) {

const PRODUCTS_QUERY = `#graphql

query products {

products(first: 3) {

edges {

node {

id

title

}

}

}

}

`;

const {products} = await context.storefront.query(PRODUCTS_QUERY);

return json({products});

}

```Storefront API Client```

const productQuery = `

query ProductQuery($handle: String) {

product(handle: $handle) {

id

title

handle

}

}

`;

const {data, errors, extensions} = await client.request(productQuery, {

variables: {

handle: 'sample-product',

},

});

```React Router```

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query products {

products(first: 3) {

edges {

node {

id

title

}

}

}

}`,

);

const data = await response.json();

```Shopify API```

// Load the access token as per instructions above

const storefrontAccessToken = '<my token>';

// Shop from which we're fetching data

const shop = 'my-shop.myshopify.com';

// StorefrontClient takes in the shop url and the Storefront Access Token for that shop.

const storefrontClient = new shopify.clients.Storefront({

domain: shop,

storefrontAccessToken,

});

// Use client.query and pass your query as \`data\`

const products = await storefrontClient.query({

data: `{

products (first: 3) {

edges {

node {

id

title

}

}

}

}`,

});

```Ruby```

# Load the access token as per instructions above

store_front_access_token = '<my token>'

# Shop from which we're fetching data

shop = 'my-shop.myshopify.com'

# The Storefront client takes in the shop url and the Storefront Access Token for that shop.

storefront_client = ShopifyAPI::Clients::Graphql::Storefront.new(

shop,

storefront_access_token

)

# Call query and pass your query as `data`

my_query = <<~QUERY

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

QUERY

products = storefront_client.query(query: my_query)

```

## [Anchor to Directives](/docs/api/storefront/latest#directives)DirectivesA directive provides a way for apps to describe additional options to the GraphQL executor. It lets GraphQL change the result of the query or mutation based on the additional information provided by the directive.### [Anchor to Storefront Directives](/docs/api/storefront/latest#storefront-directives)Storefront Directives@inContext (Country Code)

In the Storefront API, the `@inContext` directive takes an optional [country code argument](/api/storefront/2026-01/enums/countrycode) and applies this to the query or mutation.This example shows how to retrieve a list of available countries and their corresponding currencies for a shop that's located in France `@inContext(country: FR)`.

- [Examples for localized pricing](/api/examples/international-pricing)

- [GQL directives spec](https://graphql.org/learn/queries/#directives)

@inContext (Language)

In the Storefront API, beyond version 2022-04, the `@inContext` directive can contextualize any query to one of a shop's available languages with an optional [language code argument](/api/storefront/2026-01/enums/LanguageCode).This example shows how to return a product's `title`, `description`, and `options` translated into Spanish `@inContext(language: ES)`.

- [Examples for supporting multiple languages](/api/examples/multiple-languages)

- [GQL directives spec](https://graphql.org/learn/queries/#directives)

@inContext (Buyer Identity)

In the Storefront API, beyond version 2024-04, the `@inContext` directive can contextualize any query to a logged in buyer of a shop with an optional [buyer argument](/api/storefront/2026-01/input-objects/BuyerInput).This example shows how to return a product's price `amount` contextualized for a business customer buyer `@inContext(buyer: {customerAccessToken: 'token', companyLocationId: 'gid://shopify/CompanyLocation/1'})`.

- [Example for supporting a contextualized buyer identity](/custom-storefronts/headless/b2b#step-3-contextualize-storefront-api-requests)

- [GraphQL directives spec](https://graphql.org/learn/queries/#directives)

@inContext (Visitor Consent)

In the Storefront API, beyond version 2025-10, the `@inContext` directive can contextualize any query or mutation with visitor consent information using an optional `visitorConsent` argument.This example shows how to create a cart with visitor consent preferences `@inContext(visitorConsent: {analytics: true, preferences: true, marketing: false, saleOfData: false})`.The consent information is automatically encoded and included in the resulting [`checkoutUrl`](/docs/api/storefront/latest/objects/Cart#field-Cart.fields.checkoutUrl) to ensure privacy compliance throughout the checkout process. All consent fields are optional.

- [Examples for collecting and passing visitor consent with Checkout Kit](/docs/storefronts/mobile/checkout-kit/privacy-compliance)

- [GraphQL directives spec](https://graphql.org/learn/queries/#directives)

@defer

The `@defer` directive allows clients to prioritize part of a GraphQL query without having to make more requests to fetch the remaining information. It does this through streaming, where the first response contains the data that isn't deferred.The directive accepts two optional arguments: `label` and `if`. The `label` is included in the fragment response if it's provided in the directive. When the `if` argument is `false`, the fragment isn't deferred.This example shows how to return a product's `title` and `description` immediately, and then return the `descriptionHtml` and `options` after a short delay.The `@defer` directive is available as a [developer preview](/docs/api/developer-previews#defer-directive-developer-preview) in `unstable`.

- [Examples for how to use `@defer`](/docs/custom-storefronts/building-with-the-storefront-api/defer)

## OperationCopy9912345678910111213query productDetails {  productByHandle(handle: "baseball-t-shirt") {    title    description    ... @defer(label: "Extra info") {      descriptionHtml      options {        name        values      }    }  }}## ResponseJSONCopy9912345678910111213141516171819202122232425262728293031323334353637383940--graphqlContent-Type: application/jsonContent-Length: 158{  "data": {    "productByHandle": {      "title": "Baseball t-shirt",      "description": "description":"3 strikes, you're... never out of style in this vintage-inspired tee."    }  },  "hasNext": true}--graphqlContent-Type: application/jsonContent-Length: 295{  "incremental": [{    "path": ["productByHandle"],    "label": "Extra info",    "data": {      "descriptionHtml": "<p>3 strikes, you're... never out of style in this vintage-inspired tee. </p>",      "options": [        {          "name": "Size",          "values": ["Small", "Medium", "Large"]        },        {          "name": "Color",          "values": ["White", "Red"]        }      ]    }  }],  "hasNext": false}--graphql--

## [Anchor to Rate limits](/docs/api/storefront/latest#rate-limits)Rate limitsThe Storefront API is designed to support businesses of all sizes. The Storefront API will scale to support surges in buyer traffic or your largest flash sale. There are no rate limits applied on the number of requests that can be made to the API.The Storefront API provides protection against malicious users, such as bots, from consuming a high level of capacity. If a request appears to be malicious, Shopify will respond with a `430 Shopify Security Rejection` [error code](/docs/api/usage/response-codes) to indicate potential security concerns. Ensure requests to the Storefront API include the correct [Buyer IP header](/docs/api/usage/authentication#optional-ip-header).[Learn more about rate limits](/docs/api/usage/limits#rate-limits).### [Anchor to Query complexity limit for tokenless access](/docs/api/storefront/latest#query-complexity-limit-for-tokenless-access)Query complexity limit for tokenless accessTokenless access has a query complexity limit of 1,000. This limit is calculated based on the cost of each field in the query in the same way as the GraphQL Admin API. For more information on how query costs are calculated, see the [Cost calculation](/docs/api/usage/limits#rate-limits#cost-calculation) section in the API rate limits documentation.When using tokenless access, query complexity that exceeds 1,000 will result in an error.{}## Query complexity exceeded error responseCopy99123456789101112{  "errors": [    {      "message": "Complexity exceeded",      "extensions": {        "code": "MAX_COMPLEXITY_EXCEEDED",        "cost": 1250,        "maxCost": 1000      }    }  ]}{}## ResponseCopy991234567891011{  "errors": [    {      "message": "Internal error. Looks like something went wrong on our end.        Request ID: 1b355a21-7117-44c5-8d8b-8948082f40a8 (include this in support requests).",      "extensions": {        "code": "INTERNAL_SERVER_ERROR"      }    }  ]}

## [Anchor to Status and error codes](/docs/api/storefront/latest#status-and-error-codes)Status and error codesAll API queries return HTTP status codes that contain more information about the response.### [Anchor to 200 OK](/docs/api/storefront/latest#200-ok)200 OKThe Storefront API can return a `200 OK` response code in cases that would typically produce 4xx errors in REST.### [Anchor to Error handling](/docs/api/storefront/latest#error-handling)Error handlingThe response for the errors object contains additional detail to help you debug your operation.The response for mutations contains additional detail to help debug your query. To access this, you must request `userErrors`.#### Propertieserrors•arrayA list of all errors returned

Show error item propertieserrors[n].message•stringContains details about the error(s).

errors[n].extensions•objectProvides more information about the error(s) including properties and metadata.

Show extensions propertiesextensions.code•stringShows error codes common to Shopify. Additional error codes may also be shown.

Show common error codesACCESS_DENIEDThe client doesn’t have correct [authentication](#authentication) credentials. Similar to 401 Unauthorized.

SHOP_INACTIVEThe shop is not active. This can happen when stores repeatedly exceed API rate limits or due to fraud risk.

INTERNAL_SERVER_ERRORShopify experienced an internal error while processing the request. This error is returned instead of 500 Internal Server Error in most circumstances.

{}## Sample 200 error responsesThrottledInternal9912345678910{  "errors": [    {      "message": "Throttled",      "extensions": {        "code": "THROTTLED"      }    }  ]}991234567891011{  "errors": [    {      "message": "Internal error. Looks like something went wrong on our end.        Request ID: 1b355a21-7117-44c5-8d8b-8948082f40a8 (include this in support requests).",      "extensions": {        "code": "INTERNAL_SERVER_ERROR"      }    }  ]}Throttled```

{

"errors": [

{

"message": "Throttled",

"extensions": {

"code": "THROTTLED"

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

"code": "INTERNAL_SERVER_ERROR"

}

}

]

}

```### [Anchor to 4xx and 5xx status codes](/docs/api/storefront/latest#4xx-and-5xx-status-codes)4xx and 5xx status codesThe 4xx and 5xx errors occur infrequently. They are often related to network communications, your account, or an issue with Shopify’s services.Many errors that would typically return a 4xx or 5xx status code, return an HTTP 200 errors response instead. Refer to the [200 OK section](#200-ok) above for details.#### [Anchor to [object Object]](/docs/api/storefront/latest#400-bad-request)400 Bad RequestThe server will not process the request.#### [Anchor to [object Object]](/docs/api/storefront/latest#402-payment-required)402 Payment RequiredThe shop is frozen. The shop owner will need to pay the outstanding balance to [unfreeze](https://help.shopify.com/en/manual/your-account/pause-close-store#unfreeze-your-shopify-store) the shop.#### [Anchor to [object Object]](/docs/api/storefront/latest#403-forbidden)403 ForbiddenThe shop is forbidden. Returned if the store has been marked as fraudulent.#### [Anchor to [object Object]](/docs/api/storefront/latest#404-not-found)404 Not FoundThe resource isn’t available. This is often caused by querying for something that’s been deleted.#### [Anchor to [object Object]](/docs/api/storefront/latest#423-locked)423 LockedThe shop isn’t available. This can happen when stores repeatedly exceed API rate limits or due to fraud risk.#### [Anchor to [object Object]](/docs/api/storefront/latest#5xx-errors)5xx ErrorsAn internal error occurred in Shopify. Check out the [Shopify status page](https://www.shopifystatus.com) for more information.InfoDidn’t find the status code you’re looking for? View the complete list of

[API status response and error codes](/api/usage/response-codes).**Info:** Didn’t find the status code you’re looking for? View the complete list of

[API status response and error codes](/api/usage/response-codes).{}## Sample error codes4004024034044235009123456HTTP/1.1 400 Bad Request{  "errors": {    "query": "Required parameter missing or invalid"  }}91234HTTP/1.1 402 Payment Required{  "errors": "This shop's plan does not have access to this feature"}91234HTTP/1.1 403 Forbidden{  "errors": "Unavailable Shop"}91234HTTP/1.1 404 Not Found{  "errors": "Not Found"}91234HTTP/1.1 423 Locked{  "errors": "This shop is unavailable"}91234HTTP/1.1 500 Internal Server Error{  "errors": "An unexpected error occurred"}400```

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

HTTP/1.1 403 Forbidden

{

"errors": "Unavailable Shop"

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

## [Anchor to Resources](/docs/api/storefront/latest#resources)Resources[Get startedLearn more about how the Storefront API works and how to get started with it.Get startedLearn more about how the Storefront API works and how to get started with it.](/docs/storefronts/headless/building-with-the-storefront-api)[Get startedLearn more about how the Storefront API works and how to get started with it.](/docs/storefronts/headless/building-with-the-storefront-api)[Storefront Learning KitExplore a downloadable package of sample GraphQL queries for the Storefront API.Storefront Learning KitExplore a downloadable package of sample GraphQL queries for the Storefront API.](https://github.com/Shopify/storefront-api-learning-kit)[Storefront Learning KitExplore a downloadable package of sample GraphQL queries for the Storefront API.](https://github.com/Shopify/storefront-api-learning-kit)[Developer changelogRead about the changes currently introduced in the latest version of the Storefront API.Developer changelogRead about the changes currently introduced in the latest version of the Storefront API.](/changelog)[Developer changelogRead about the changes currently introduced in the latest version of the Storefront API.](/changelog)

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)