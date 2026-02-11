---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront/latest/queries/customer",
    "fetched_at": "2026-02-10T13:41:30.648539",
    "status": 200,
    "size_bytes": 386485
  },
  "metadata": {
    "title": "customer - Storefront API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "queries",
    "component": "customer"
  }
}
---

# customer - Storefront API

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to customer](/docs/api/storefront/latest/queries/customer#top)# customerqueryAsk assistantThe customer associated with the given access token. Tokens are obtained by using the

[`customerAccessTokenCreate` mutation](https://shopify.dev/docs/api/storefront/latest/mutations/customerAccessTokenCreate).

[Anchor to Arguments](/docs/api/storefront/latest/queries/customer#arguments)## Arguments- customerAccessToken (String!)[Anchor to customerAccessToken](/docs/api/storefront/latest/queries/customer#arguments-customerAccessToken)customerAccessToken•[String!](/docs/api/storefront/latest/scalars/String)requiredThe customer access token.

Was this section helpful?YesNo## [Anchor to Possible returns](/docs/api/storefront/latest/queries/customer#possible-returns)Possible returns- Customer (Customer)[Anchor to Customer](/docs/api/storefront/latest/queries/customer#returns-Customer)Customer•[Customer](/docs/api/storefront/latest/objects/Customer)A customer represents a customer account with the shop. Customer accounts store contact information for the customer, saving logged-in customers the trouble of having to provide it at every checkout.

Show fields[Anchor to acceptsMarketing](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.acceptsMarketing)acceptsMarketing•[Boolean!](/docs/api/storefront/latest/scalars/Boolean)non-null Token access requiredIndicates whether the customer has consented to be sent marketing material via email.

[Anchor to addresses](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.addresses)addresses•[MailingAddressConnection!](/docs/api/storefront/latest/connections/MailingAddressConnection)non-null Token access requiredA list of addresses for the customer.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.addresses.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.addresses.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.addresses.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.addresses.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.addresses.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to avatarUrl](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.avatarUrl)avatarUrl•[String](/docs/api/storefront/latest/scalars/String) Token access requiredThe URL of the customer's avatar image.

[Anchor to createdAt](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.createdAt)createdAt•[DateTime!](/docs/api/storefront/latest/scalars/DateTime)non-null Token access requiredThe date and time when the customer was created.

[Anchor to defaultAddress](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.defaultAddress)defaultAddress•[MailingAddress](/docs/api/storefront/latest/objects/MailingAddress) Token access requiredThe customer’s default address.

Show fields[Anchor to displayName](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.displayName)displayName•[String!](/docs/api/storefront/latest/scalars/String)non-null Token access requiredThe customer’s name, email or phone number.

[Anchor to email](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.email)email•[String](/docs/api/storefront/latest/scalars/String) Token access requiredThe customer’s email address.

[Anchor to firstName](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.firstName)firstName•[String](/docs/api/storefront/latest/scalars/String) Token access requiredThe customer’s first name.

[Anchor to id](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.id)id•[ID!](/docs/api/storefront/latest/scalars/ID)non-null Token access requiredA unique ID for the customer.

[Anchor to lastName](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.lastName)lastName•[String](/docs/api/storefront/latest/scalars/String) Token access requiredThe customer’s last name.

[Anchor to metafield](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.metafield)metafield•[Metafield](/docs/api/storefront/latest/objects/Metafield) Token access requiredA [custom field](https://shopify.dev/docs/apps/build/custom-data), including its `namespace` and `key`, that's associated with a Shopify resource for the purposes of adding and storing additional information.

Show fields### Arguments[Anchor to namespace](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.metafield.arguments.namespace)namespace•[String](/docs/api/storefront/latest/scalars/String)The container the metafield belongs to. If omitted, the app-reserved namespace will be used.

[Anchor to key](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.metafield.arguments.key)key•[String!](/docs/api/storefront/latest/scalars/String)requiredThe identifier for the metafield.

[Anchor to metafields](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.metafields)metafields•[[Metafield]!](/docs/api/storefront/latest/objects/Metafield)non-null Token access requiredA list of [custom fields](/docs/apps/build/custom-data) that a merchant associates with a Shopify resource.

Show fields### Arguments[Anchor to identifiers](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.metafields.arguments.identifiers)identifiers•[[HasMetafieldsIdentifier!]!](/docs/api/storefront/latest/input-objects/HasMetafieldsIdentifier)requiredThe list of metafields to retrieve by namespace and key.

The input must not contain more than `250` values.

Show input fields[Anchor to numberOfOrders](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.numberOfOrders)numberOfOrders•[UnsignedInt64!](/docs/api/storefront/latest/scalars/UnsignedInt64)non-null Token access requiredThe number of orders that the customer has made at the store in their lifetime.

[Anchor to orders](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.orders)orders•[OrderConnection!](/docs/api/storefront/latest/connections/OrderConnection)non-null Token access requiredThe orders associated with the customer.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.orders.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.orders.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.orders.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.orders.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.orders.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.orders.arguments.sortKey)sortKey•[OrderSortKeys](/docs/api/storefront/latest/enums/OrderSortKeys)Default:IDSort the underlying list by the given key.

Show enum values[Anchor to query](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.orders.arguments.query)query•[String](/docs/api/storefront/latest/scalars/String)Apply one or multiple filters to the query.

Refer to the detailed [search syntax](https://shopify.dev/api/usage/search-syntax) for more information about using filters.

Show filters[Anchor to ](/docs/api/storefront/latest/queries/customer#argument-query-filter-processed_at)processed_at•[Anchor to phone](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.phone)phone•[String](/docs/api/storefront/latest/scalars/String) Token access requiredThe customer’s phone number.

[Anchor to socialLoginProvider](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.socialLoginProvider)socialLoginProvider•[SocialLoginProvider](/docs/api/storefront/latest/objects/SocialLoginProvider) Token access requiredThe social login provider associated with the customer.

Show fields[Anchor to tags](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.tags)tags•[[String!]!](/docs/api/storefront/latest/scalars/String)non-null Token access requiredA comma separated list of tags that have been added to the customer.

Additional access scope required: unauthenticated_read_customer_tags.

[Anchor to updatedAt](/docs/api/storefront/latest/queries/customer#returns-Customer.fields.updatedAt)updatedAt•[DateTime!](/docs/api/storefront/latest/scalars/DateTime)non-null Token access requiredThe date and time when the customer information was updated.

Was this section helpful?YesNo## Examples- ### Get a customer by access token#### DescriptionThe following query retrieves the customer with the associated access token. It returns the customer fields specified in the query.

#### Query```

query {

customer(customerAccessToken: "bobs_token") {

id

firstName

lastName

acceptsMarketing

email

phone

}

}

```#### cURL```

curl -X POST \

https://your-development-store.myshopify.com/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

-H 'X-Shopify-Storefront-Access-Token: {storefront_access_token}' \

-d '{

"query": "query { customer(customerAccessToken: \"bobs_token\") { id firstName lastName acceptsMarketing email phone } }"

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

customer(customerAccessToken: "bobs_token") {

id

firstName

lastName

acceptsMarketing

email

phone

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

customer(customerAccessToken: "bobs_token") {

id

firstName

lastName

acceptsMarketing

email

phone

}

}`,

});

```#### Response```

{

"customer": {

"id": "gid://shopify/Customer/410535040",

"firstName": "John",

"lastName": "Smith",

"acceptsMarketing": false,

"email": "johnsmith@example.com",

"phone": "+16134504533"

}

}

```## Get a customer by access tokenHide contentGQLcURLReact RouterNode.jsShow description[Open in GraphiQL](http://localhost:3457/graphiql?query=query%20%7B%0A%20%20customer(customerAccessToken%3A%20%22bobs_token%22)%20%7B%0A%20%20%20%20id%0A%20%20%20%20firstName%0A%20%20%20%20lastName%0A%20%20%20%20acceptsMarketing%0A%20%20%20%20email%0A%20%20%20%20phone%0A%20%20%7D%0A%7D)Copy9912345678910111213141516171819202122›⌄import { unauthenticated } from "../shopify.server";export const loader = async () => {  const { storefront } = await unauthenticated.storefront(    'your-development-store.myshopify.com'  );  const response = await storefront.graphql(    `#graphql  query {    customer(customerAccessToken: "bobs_token") {      id      firstName      lastName      acceptsMarketing      email      phone    }  }`,  );  const json = await response.json();  return json.data;}GQL```

query {

customer(customerAccessToken: "bobs_token") {

id

firstName

lastName

acceptsMarketing

email

phone

}

}

```cURL```

curl -X POST \

https://your-development-store.myshopify.com/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

-H 'X-Shopify-Storefront-Access-Token: {storefront_access_token}' \

-d '{

"query": "query { customer(customerAccessToken: \"bobs_token\") { id firstName lastName acceptsMarketing email phone } }"

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

customer(customerAccessToken: "bobs_token") {

id

firstName

lastName

acceptsMarketing

email

phone

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

customer(customerAccessToken: "bobs_token") {

id

firstName

lastName

acceptsMarketing

email

phone

}

}`,

});

```Hide content## ResponseJSON9912345678910›⌄⌄{  "customer": {    "id": "gid://shopify/Customer/410535040",    "firstName": "John",    "lastName": "Smith",    "acceptsMarketing": false,    "email": "johnsmith@example.com",    "phone": "+16134504533"  }}### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)