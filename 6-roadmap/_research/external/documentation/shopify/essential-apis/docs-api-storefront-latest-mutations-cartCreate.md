---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront/latest/mutations/cartCreate",
    "fetched_at": "2026-02-10T13:41:15.211781",
    "status": 200,
    "size_bytes": 315870
  },
  "metadata": {
    "title": "cartCreate - Storefront API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "mutations",
    "component": "cartCreate"
  }
}
---

# cartCreate - Storefront API

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to cartCreate](/docs/api/storefront/latest/mutations/cartCreate#top)# cartCreatemutationAsk assistantCreates a new cart.

[Anchor to Arguments](/docs/api/storefront/latest/mutations/cartCreate#arguments)## Arguments- input (CartInput)[Anchor to input](/docs/api/storefront/latest/mutations/cartCreate#arguments-input)input•[CartInput](/docs/api/storefront/latest/input-objects/CartInput)The fields used to create a cart.

Show input fieldsWas this section helpful?YesNo## [Anchor to CartCreatePayload returns](/docs/api/storefront/latest/mutations/cartCreate#returns)CartCreatePayload returns- cart (Cart)- userErrors ([CartUserError!]!)- warnings ([CartWarning!]!)[Anchor to cart](/docs/api/storefront/latest/mutations/cartCreate#returns-cart)cart•[Cart](/docs/api/storefront/latest/objects/Cart)The new cart.

Show fields[Anchor to userErrors](/docs/api/storefront/latest/mutations/cartCreate#returns-userErrors)userErrors•[[CartUserError!]!](/docs/api/storefront/latest/objects/CartUserError)non-nullThe list of errors that occurred from executing the mutation.

Show fields[Anchor to warnings](/docs/api/storefront/latest/mutations/cartCreate#returns-warnings)warnings•[[CartWarning!]!](/docs/api/storefront/latest/objects/CartWarning)non-nullA list of warnings that occurred during the mutation.

Show fieldsWas this section helpful?YesNo## Examples- ### cartCreate referenceHide content## Mutation ReferenceCopy991234567891011121314›⌄⌄⌄⌄⌄mutation cartCreate($input: CartInput) {  cartCreate(input: $input) {    cart {      # Cart fields    }    userErrors {      field      message    }    warnings {      # CartWarning fields    }  }}Hide content## InputVariablesSchemaCopy99123456789101112131415161718192021222324252627282930313233343536373839404142434445464748›⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄{  "input": {    "attributes": [      {        "key": "<your-key>",        "value": "<your-value>"      }    ],    "lines": [      {        "attributes": [          {}        ],        "quantity": 1,        "merchandiseId": "gid://shopify/<objectName>/10079785100",        "sellingPlanId": "gid://shopify/<objectName>/10079785100",        "parent": {}      }    ],    "discountCodes": [      "<your-discountCodes>"    ],    "giftCardCodes": [      "<your-giftCardCodes>"    ],    "note": "<your-note>",    "buyerIdentity": {      "email": "<your-email>",      "phone": "<your-phone>",      "companyLocationId": "gid://shopify/<objectName>/10079785100",      "countryCode": "AF",      "customerAccessToken": "<your-customerAccessToken>",      "preferences": {}    },    "delivery": {      "addresses": [        {}      ]    },    "metafields": [      {        "key": "<your-key>",        "value": "<your-value>",        "type": "<your-type>"      }    ]  }}Variables```

{

"input": {

"attributes": [

{

"key": "<your-key>",

"value": "<your-value>"

}

],

"lines": [

{

"attributes": [

{}

],

"quantity": 1,

"merchandiseId": "gid://shopify/<objectName>/10079785100",

"sellingPlanId": "gid://shopify/<objectName>/10079785100",

"parent": {}

}

],

"discountCodes": [

"<your-discountCodes>"

],

"giftCardCodes": [

"<your-giftCardCodes>"

],

"note": "<your-note>",

"buyerIdentity": {

"email": "<your-email>",

"phone": "<your-phone>",

"companyLocationId": "gid://shopify/<objectName>/10079785100",

"countryCode": "AF",

"customerAccessToken": "<your-customerAccessToken>",

"preferences": {}

},

"delivery": {

"addresses": [

{}

]

},

"metafields": [

{

"key": "<your-key>",

"value": "<your-value>",

"type": "<your-type>"

}

]

}

}

```Schema```

input CartInput {

attributes: [AttributeInput!]

lines: [CartLineInput!]

discountCodes: [String!]

giftCardCodes: [String!]

note: String

buyerIdentity: CartBuyerIdentityInput

delivery: CartDeliveryInput

metafields: [CartInputMetafieldInput!]

}

input AttributeInput {

key: String!

value: String!

}

input CartLineInput {

attributes: [AttributeInput!]

quantity: Int

merchandiseId: ID!

sellingPlanId: ID

parent: CartLineParentInput

}

input CartBuyerIdentityInput {

email: String

phone: String

companyLocationId: ID

countryCode: CountryCode

customerAccessToken: String

preferences: CartPreferencesInput

}

input CartDeliveryInput {

addresses: [CartSelectableAddressInput!]

}

input CartInputMetafieldInput {

key: String!

value: String!

type: String!

}

```### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)