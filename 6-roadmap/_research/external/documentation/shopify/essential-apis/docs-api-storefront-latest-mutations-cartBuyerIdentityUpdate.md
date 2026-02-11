---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront/latest/mutations/cartBuyerIdentityUpdate",
    "fetched_at": "2026-02-10T13:41:20.333561",
    "status": 200,
    "size_bytes": 310459
  },
  "metadata": {
    "title": "cartBuyerIdentityUpdate - Storefront API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "mutations",
    "component": "cartBuyerIdentityUpdate"
  }
}
---

# cartBuyerIdentityUpdate - Storefront API

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to cartBuyerIdentityUpdate](/docs/api/storefront/latest/mutations/cartBuyerIdentityUpdate#top)# cartBuyerIdentityUpdatemutationAsk assistantUpdates customer information associated with a cart.

Buyer identity is used to determine

[international pricing](https://shopify.dev/custom-storefronts/internationalization/international-pricing)

and should match the customer's shipping address.

[Anchor to Arguments](/docs/api/storefront/latest/mutations/cartBuyerIdentityUpdate#arguments)## Arguments- buyerIdentity (CartBuyerIdentityInput!)- cartId (ID!)[Anchor to buyerIdentity](/docs/api/storefront/latest/mutations/cartBuyerIdentityUpdate#arguments-buyerIdentity)buyerIdentity•[CartBuyerIdentityInput!](/docs/api/storefront/latest/input-objects/CartBuyerIdentityInput)requiredThe customer associated with the cart. Used to determine

[international pricing](https://shopify.dev/custom-storefronts/internationalization/international-pricing).

Buyer identity should match the customer's shipping address.

Show input fields[Anchor to cartId](/docs/api/storefront/latest/mutations/cartBuyerIdentityUpdate#arguments-cartId)cartId•[ID!](/docs/api/storefront/latest/scalars/ID)requiredThe ID of the cart.

Was this section helpful?YesNo## [Anchor to CartBuyerIdentityUpdatePayload returns](/docs/api/storefront/latest/mutations/cartBuyerIdentityUpdate#returns)CartBuyerIdentityUpdatePayload returns- cart (Cart)- userErrors ([CartUserError!]!)- warnings ([CartWarning!]!)[Anchor to cart](/docs/api/storefront/latest/mutations/cartBuyerIdentityUpdate#returns-cart)cart•[Cart](/docs/api/storefront/latest/objects/Cart)The updated cart.

Show fields[Anchor to userErrors](/docs/api/storefront/latest/mutations/cartBuyerIdentityUpdate#returns-userErrors)userErrors•[[CartUserError!]!](/docs/api/storefront/latest/objects/CartUserError)non-nullThe list of errors that occurred from executing the mutation.

Show fields[Anchor to warnings](/docs/api/storefront/latest/mutations/cartBuyerIdentityUpdate#returns-warnings)warnings•[[CartWarning!]!](/docs/api/storefront/latest/objects/CartWarning)non-nullA list of warnings that occurred during the mutation.

Show fieldsWas this section helpful?YesNo## Examples- ### cartBuyerIdentityUpdate referenceHide content## Mutation ReferenceCopy991234567891011121314›⌄⌄⌄⌄⌄mutation cartBuyerIdentityUpdate($cartId: ID!, $buyerIdentity: CartBuyerIdentityInput!) {  cartBuyerIdentityUpdate(cartId: $cartId, buyerIdentity: $buyerIdentity) {    cart {      # Cart fields    }    userErrors {      field      message    }    warnings {      # CartWarning fields    }  }}Hide content## InputVariablesSchemaCopy9912345678910111213141516›⌄⌄⌄⌄{  "cartId": "gid://shopify/<objectName>/10079785100",  "buyerIdentity": {    "email": "<your-email>",    "phone": "<your-phone>",    "companyLocationId": "gid://shopify/<objectName>/10079785100",    "countryCode": "AF",    "customerAccessToken": "<your-customerAccessToken>",    "preferences": {      "delivery": {},      "wallet": [        "<your-wallet>"      ]    }  }}Variables```

{

"cartId": "gid://shopify/<objectName>/10079785100",

"buyerIdentity": {

"email": "<your-email>",

"phone": "<your-phone>",

"companyLocationId": "gid://shopify/<objectName>/10079785100",

"countryCode": "AF",

"customerAccessToken": "<your-customerAccessToken>",

"preferences": {

"delivery": {},

"wallet": [

"<your-wallet>"

]

}

}

}

```Schema```

input CartBuyerIdentityInput {

email: String

phone: String

companyLocationId: ID

countryCode: CountryCode

customerAccessToken: String

preferences: CartPreferencesInput

}

input CartPreferencesInput {

delivery: CartDeliveryPreferenceInput

wallet: [String!]

}

```### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)