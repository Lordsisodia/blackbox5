---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront/latest/mutations/cartLinesRemove",
    "fetched_at": "2026-02-10T13:41:18.975215",
    "status": 200,
    "size_bytes": 304231
  },
  "metadata": {
    "title": "cartLinesRemove - Storefront API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "mutations",
    "component": "cartLinesRemove"
  }
}
---

# cartLinesRemove - Storefront API

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to cartLinesRemove](/docs/api/storefront/latest/mutations/cartLinesRemove#top)# cartLinesRemovemutationAsk assistantRemoves one or more merchandise lines from the cart.

[Anchor to Arguments](/docs/api/storefront/latest/mutations/cartLinesRemove#arguments)## Arguments- cartId (ID!)- lineIds ([ID!]!)[Anchor to cartId](/docs/api/storefront/latest/mutations/cartLinesRemove#arguments-cartId)cartId•[ID!](/docs/api/storefront/latest/scalars/ID)requiredThe ID of the cart.

[Anchor to lineIds](/docs/api/storefront/latest/mutations/cartLinesRemove#arguments-lineIds)lineIds•[[ID!]!](/docs/api/storefront/latest/scalars/ID)requiredThe merchandise line IDs to remove.

The input must not contain more than `250` values.

Was this section helpful?YesNo## [Anchor to CartLinesRemovePayload returns](/docs/api/storefront/latest/mutations/cartLinesRemove#returns)CartLinesRemovePayload returns- cart (Cart)- userErrors ([CartUserError!]!)- warnings ([CartWarning!]!)[Anchor to cart](/docs/api/storefront/latest/mutations/cartLinesRemove#returns-cart)cart•[Cart](/docs/api/storefront/latest/objects/Cart)The updated cart.

Show fields[Anchor to userErrors](/docs/api/storefront/latest/mutations/cartLinesRemove#returns-userErrors)userErrors•[[CartUserError!]!](/docs/api/storefront/latest/objects/CartUserError)non-nullThe list of errors that occurred from executing the mutation.

Show fields[Anchor to warnings](/docs/api/storefront/latest/mutations/cartLinesRemove#returns-warnings)warnings•[[CartWarning!]!](/docs/api/storefront/latest/objects/CartWarning)non-nullA list of warnings that occurred during the mutation.

Show fieldsWas this section helpful?YesNo## Examples- ### cartLinesRemove referenceHide content## Mutation ReferenceCopy991234567891011121314›⌄⌄⌄⌄⌄mutation cartLinesRemove($cartId: ID!, $lineIds: [ID!]!) {  cartLinesRemove(cartId: $cartId, lineIds: $lineIds) {    cart {      # Cart fields    }    userErrors {      field      message    }    warnings {      # CartWarning fields    }  }}Hide content## InputVariablesCopy9123456›⌄⌄{  "cartId": "gid://shopify/<objectName>/10079785100",  "lineIds": [    "gid://shopify/<objectName>/10079785100"  ]}Variables```

{

"cartId": "gid://shopify/<objectName>/10079785100",

"lineIds": [

"gid://shopify/<objectName>/10079785100"

]

}

```### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)