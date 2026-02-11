---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/network-features",
    "fetched_at": "2026-02-10T13:29:16.996321",
    "status": 200,
    "size_bytes": 428904
  },
  "metadata": {
    "title": "Network Features",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "2026-01",
    "component": "network-features"
  }
}
---

# Network Features

# Network FeaturesAdmin UI extensions make it possible to surface contextual app functionality within the Shopify Admin interface.Ask assistant

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest

## [Anchor to Overview](/docs/api/admin-extensions/latest/network-features#overview)OverviewExtend the Shopify Admin with UI Extensions.[App authenticationMake authenticated requests to your app's backendApp authenticationMake authenticated requests to your app's backend](/docs/api/admin-extensions/latest/#app-authentication)[App authentication - Make authenticated requests to your app's backend](#app-authentication)[Direct API accessAccess the Shopify GraphQL API directlyDirect API accessAccess the Shopify GraphQL API directly](/docs/api/admin-extensions/latest/#direct-api-access)[Direct API access - Access the Shopify GraphQL API directly](#direct-api-access)[Custom protocolsEasily construct URLs to navigate to common locationsCustom protocolsEasily construct URLs to navigate to common locations](/docs/api/admin-extensions/latest/#custom-protocols)[Custom protocols - Easily construct URLs to navigate to common locations](#custom-protocols)

## [Anchor to App Authentication](/docs/api/admin-extensions/latest/network-features#app-authentication)App AuthenticationAdmin UI extensions can also make authenticated calls to your app's backend. When you use `fetch()` to make a request to your app's configured auth domain or any of its subdomains, an `Authorization` header is automatically added with a Shopify [OpenID Connect ID Token](/docs/api/app-home/apis/id-token). There's no need to manually manage ID tokens.Relative URLs passed to `fetch()` are resolved against your app's `app_url`. This means if your app's backend is on the same domain as your `app_url`, you can make requests to it using `fetch('/path')`.If you need to make requests to a different domain, you can use the [`auth.idToken()` method](/docs/api/admin-extensions/api/standard-api#standardapi-propertydetail-auth) to retrieve the ID token and manually add it to your request headers.## Make requests to your app's backendGet Product DataGet Data from a different domainCopy991234567891011121314151617181920212223242526272829import {render} from 'preact';import {useEffect, useState} from 'preact/hooks';export default async () => {  render(<Extension />, document.body);}// Get product info from app backendasync function getProductInfo(id) {  const res = await fetch(`/api/products/${id}`);  return res.json();}function Extension() {  // Contextual "input" data passed to this extension:  const {data} = shopify;  const productId = data.selected?.[0]?.id;  const [productInfo, setProductInfo] = useState();  useEffect(() => {    getProductInfo(productId).then(setProductInfo);  }, [productId]);  return (    <s-admin-block title="Product Info">      <s-text>Info: {productInfo?.title}</s-text>    </s-admin-block>  );}9912345678910111213141516171819202122232425262728293031323334import {render} from 'preact';import {useEffect, useState} from 'preact/hooks';export default async () => {  render(<Extension />, document.body);}// Get product info from a different app backendasync function getProductInfo(id, auth) {  const token = await auth.idToken();  const res = await fetch(`https://app.example.com/api/products/${id}`, {    headers: {      Authorization: `Bearer ${token}`,    },  });  return res.json();}function Extension() {  // Contextual "input" data passed to this extension:  const {data, auth} = shopify;  const productId = data.selected?.[0]?.id;  const [productInfo, setProductInfo] = useState();  useEffect(() => {    getProductInfo(productId, auth).then(setProductInfo);  }, [productId, auth]);  return (    <s-admin-block title="Product Info">      <s-text>Info: {productInfo?.title}</s-text>    </s-admin-block>  );}Get Product Data```

import {render} from 'preact';

import {useEffect, useState} from 'preact/hooks';

export default async () => {

render(<Extension />, document.body);

}

// Get product info from app backend

async function getProductInfo(id) {

const res = await fetch(`/api/products/${id}`);

return res.json();

}

function Extension() {

// Contextual "input" data passed to this extension:

const {data} = shopify;

const productId = data.selected?.[0]?.id;

const [productInfo, setProductInfo] = useState();

useEffect(() => {

getProductInfo(productId).then(setProductInfo);

}, [productId]);

return (

<s-admin-block title="Product Info">

<s-text>Info: {productInfo?.title}</s-text>

</s-admin-block>

);

}

```Get Data from a different domain```

import {render} from 'preact';

import {useEffect, useState} from 'preact/hooks';

export default async () => {

render(<Extension />, document.body);

}

// Get product info from a different app backend

async function getProductInfo(id, auth) {

const token = await auth.idToken();

const res = await fetch(`https://app.example.com/api/products/${id}`, {

headers: {

Authorization: `Bearer ${token}`,

},

});

return res.json();

}

function Extension() {

// Contextual "input" data passed to this extension:

const {data, auth} = shopify;

const productId = data.selected?.[0]?.id;

const [productInfo, setProductInfo] = useState();

useEffect(() => {

getProductInfo(productId, auth).then(setProductInfo);

}, [productId, auth]);

return (

<s-admin-block title="Product Info">

<s-text>Info: {productInfo?.title}</s-text>

</s-admin-block>

);

}

```

## [Anchor to Direct API access](/docs/api/admin-extensions/latest/network-features#direct-api-access)Direct API accessYou can make Shopify Admin API requests directly from your extension using the [query API](/docs/api/admin-extensions/api/standard-api#standardapi-propertydetail-query) or the standard [web fetch API](https://developer.mozilla.org/en-US/docs/Web/API/fetch)!Any `fetch()` calls from your extension to Shopify's Admin GraphQL API are automatically authenticated by default. These calls are fast too, because Shopify handles requests directly.Direct API requests use [online access](/docs/apps/build/authentication-authorization/access-token-types/online-access-tokens) mode by default. If you want to use [offline access](/docs/apps/build/authentication-authorization/access-token-types/offline-access-tokens) mode, you can set the `direct_api_mode` property to `offline` in your [app TOML file](/docs/apps/tools/cli/configuration#admin).Note: Direct API can't be used to manage storefront access tokens.[NoteDirect API can't be used to manage storefront access tokens.NoteDirect API can't be used to manage storefront access tokens.](/docs/api/admin-extensions#direct-api-access)[Note - Direct API can't be used to manage storefront access tokens.](/docs/api/admin-extensions#direct-api-access)[Developer guideLearn more about access scopesDeveloper guideLearn more about access scopes](/docs/api/usage/access-scopes)[Developer guide - Learn more about access scopes](/docs/api/usage/access-scopes)## Query Shopify dataFetch Product dataQuery Product dataCopy99123456789101112131415161718192021222324252627282930313233import {render} from 'preact';export default async () => {  const productId = shopify.data.selected?.[0]?.id;  const product = await getProduct(productId);  render(<Extension product={product} />, document.body);};async function getProduct(id) {  const res = await fetch('shopify:admin/api/graphql.json', {    method: 'POST',    body: JSON.stringify({      query: `        query GetProduct($id: ID!) {          product(id: $id) {            title          }        }      `,      variables: {id},    }),  });  const {data} = await res.json();  return data.product;}function Extension({product}) {  return (    <s-admin-block heading="Product Info">      <s-text>The selected product title is {product.title}</s-text>    </s-admin-block>  );}991234567891011121314151617181920212223242526import {render} from 'preact';export default async () => {  const productId = shopify.data.selected?.[0]?.id;  const {    data: {product},  } = await shopify.query(    `    query GetProduct($id: ID!) {      product(id: $id) {        title      }    }  `,    {variables: {id: productId}},  );  render(<Extension product={product} />, document.body);};function Extension({product}) {  return (    <s-admin-block heading="Product Info">      <s-text>The selected product title is {product.title}</s-text>    </s-admin-block>  );}Fetch Product data```

import {render} from 'preact';

export default async () => {

const productId = shopify.data.selected?.[0]?.id;

const product = await getProduct(productId);

render(<Extension product={product} />, document.body);

};

async function getProduct(id) {

const res = await fetch('shopify:admin/api/graphql.json', {

method: 'POST',

body: JSON.stringify({

query: `

query GetProduct($id: ID!) {

product(id: $id) {

title

}

}

`,

variables: {id},

}),

});

const {data} = await res.json();

return data.product;

}

function Extension({product}) {

return (

<s-admin-block heading="Product Info">

<s-text>The selected product title is {product.title}</s-text>

</s-admin-block>

);

}

```Query Product data```

import {render} from 'preact';

export default async () => {

const productId = shopify.data.selected?.[0]?.id;

const {

data: {product},

} = await shopify.query(

`

query GetProduct($id: ID!) {

product(id: $id) {

title

}

}

`,

{variables: {id: productId}},

);

render(<Extension product={product} />, document.body);

};

function Extension({product}) {

return (

<s-admin-block heading="Product Info">

<s-text>The selected product title is {product.title}</s-text>

</s-admin-block>

);

}

```

## [Anchor to Custom Protocols](/docs/api/admin-extensions/latest/network-features#custom-protocols)Custom ProtocolsCustom protocols make it easier to navigate to common locations, and construct URLs.Shopify Protocol

Use the `shopify:admin` protocol when you want to construct a URL with a root of the Shopify Admin.App Protocol

Use the `app:` protocol to construct a URL for your app. Shopify will handle constructing the base URL for your app. This works for both embedded and non-embedded apps.Extension Protocol

Triggers an action extension from a block extension using the `extension:` protocol. The `extensionTarget` is the target of the action extension. The handle is the handle of the action extension that will be opened.Relative Urls

Relative urls are relative to your app and are useful when you want to link to a route within your app. This works for both embedded and non-embedded apps.## shopify:adminLink to Product PageFetch dataCopy91<s-link href="shopify:admin/products/1234567890">Link to Product Page</s-link>;91234fetch('shopify:admin/api/graphql.json', {  method: 'POST',  body: JSON.stringify(simpleProductQuery),});Link to Product Page```

<s-link href="shopify:admin/products/1234567890">Link to Product Page</s-link>;

```Fetch data```

fetch('shopify:admin/api/graphql.json', {

method: 'POST',

body: JSON.stringify(simpleProductQuery),

});

```## app:Copy## Link to Settings91<Link to="app:settings/advanced" />;## extension:Copy## Trigger Action Extension from a Block extension91<Link to={`extension:${extension.handle}/${extensionTarget}`} />;## /relative/urlsCopy## Link to route in your app91<Link to={`/reviews/${product.id}`} />;

## [Anchor to Security](/docs/api/admin-extensions/latest/network-features#security)SecurityUI Extensions run on a different origin than the Shopify Admin. For network calls to succeed, your server must support [cross-origin resource sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) for the origin `https://extensions.shopifycdn.com`.If you have a custom [`Access-Control-Allow-Origin` header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin) set, you must include `https://extensions.shopifycdn.com` in the list of allowed origins.If you are using the [Shopify App Remix Template](https://github.com/Shopify/shopify-app-template-remix), this is done automatically for you.

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)