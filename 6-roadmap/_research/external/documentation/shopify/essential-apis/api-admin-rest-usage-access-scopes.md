---
{
  "fetch": {
    "url": "https://shopify.dev/api/admin-rest/usage/access-scopes",
    "fetched_at": "2026-02-10T13:39:42.868004",
    "status": 200,
    "size_bytes": 255229
  },
  "metadata": {
    "title": "Access scopes for the REST Admin API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "usage",
    "component": "access-scopes"
  }
}
---

# Access scopes for the REST Admin API

ExpandOn this page- [How it works](/docs/api/admin-rest/usage/access-scopes#how-it-works)- [Authenticated access scopes](/docs/api/admin-rest/usage/access-scopes#authenticated-access-scopes)- [Checking granted access scopes](/docs/api/admin-rest/usage/access-scopes#checking-granted-access-scopes)- [Limitations and considerations](/docs/api/admin-rest/usage/access-scopes#limitations-and-considerations)

# Access scopes for the REST Admin APIAsk assistantLegacyThe REST Admin API is a legacy API as of October 1, 2024. All apps and integrations should be built with the [GraphQL Admin API](/docs/api/admin-graphql). For details and migration steps, visit our [migration guide](/docs/apps/build/graphql/migrate).**Legacy:** The REST Admin API is a legacy API as of October 1, 2024. All apps and integrations should be built with the [GraphQL Admin API](/docs/api/admin-graphql). For details and migration steps, visit our [migration guide](/docs/apps/build/graphql/migrate).All apps need to request access to specific store data during the app authorization process. This guide provides a list of available access scopes for the REST Admin API.

## [Anchor to How it works](/docs/api/admin-rest/usage/access-scopes#how-it-works)How it worksTipFor more information on how to configure your access scopes, refer to [app configuration](/docs/apps/build/cli-for-apps/app-configuration).**Tip:** For more information on how to configure your access scopes, refer to [app configuration](/docs/apps/build/cli-for-apps/app-configuration).Authorization is the process of giving permissions to apps. Users can authorize Shopify apps to access data in a store. For example, an app might be authorized to access customer data in a store.For the REST Admin API, an app can request authenticated access scopes. Authenticated access is intended for interacting with a store on behalf of a user. For example, creating products and  managing discount codes.Shopify has additional access scope types for working with GraphQL APIs. [Learn more](/docs/api/usage/access-scopes).

## [Anchor to Authenticated access scopes](/docs/api/admin-rest/usage/access-scopes#authenticated-access-scopes)Authenticated access scopesYour app can request the following authenticated access scopes:Authenticated access scopes| Scope | Access || `read_assigned_fulfillment_orders`,`write_assigned_fulfillment_orders` | [FulfillmentOrder](/docs/api/admin-rest/latest/resources/assignedfulfillmentorder) resources assigned to a location managed by your [fulfillment service](/docs/api/admin-rest/latest/resources/fulfillmentservice) || `read_checkouts`,`write_checkouts` | [Checkouts](/docs/api/admin-rest/latest/resources/checkout) || `read_content`,- `write_content` | [Article](/docs/api/admin-rest/latest/resources/article), [Blog](/docs/api/admin-rest/latest/resources/blog), [Comment](/docs/api/admin-rest/latest/resources/comment), [Page](/docs/api/admin-rest/latest/resources/page), and [Redirects](/docs/api/admin-rest/latest/resources/redirect) || `read_customers`,`write_customers` | [Customer](/docs/api/admin-rest/latest/resources/customer) || `read_draft_orders`,`write_draft_orders` | [Draft Order](/docs/api/admin-rest/latest/resources/draftorder) || `read_fulfillments`,`write_fulfillments` | [Fulfillment Service](/docs/api/admin-rest/latest/resources/fulfillmentservice) || `read_gift_cards`,`write_gift_cards` | [Gift Card](/docs/api/admin-rest/latest/resources/gift-card) || `read_inventory`,`write_inventory` | [Inventory Level](/docs/api/admin-rest/latest/resources/inventorylevel) and [Inventory Item](/docs/api/admin-rest/latest/resources/inventoryitem) || `read_locations` | [Location](/docs/api/admin-rest/latest/resources/location) || `read_marketing_events`,`write_marketing_events` | [Marketing Event](/docs/api/admin-rest/latest/resources/marketingevent) || `read_merchant_managed_fulfillment_orders`,`write_merchant_managed_fulfillment_orders` | [FulfillmentOrder](/docs/api/admin-rest/latest/resources/fulfillmentorder) resources assigned to merchant-managed locations || `read_orders`,`write_orders` | [Abandoned checkouts](/docs/api/admin-rest/latest/resources/abandoned-checkouts), [Customer](/docs/api/admin-rest/latest/resources/customer), [Fulfillment](/docs/api/admin-rest/latest/resources/fulfillment), [Order](/docs/api/admin-rest/latest/resources/order), and [Transaction](/docs/api/admin-rest/latest/resources/transaction) resources || `read_price_rules`,`write_price_rules` | [Price Rules](/docs/api/admin-rest/latest/resources/pricerule) || `read_products`,`write_products` | [Product](/docs/api/admin-rest/latest/resources/product), [Product Variant](/docs/api/admin-rest/latest/resources/product-variant), [Product Image](/docs/api/admin-rest/latest/resources/product-image), [Collect](/docs/api/admin-rest/latest/resources/collect), [Custom Collection](/docs/api/admin-rest/latest/resources/customcollection), and [Smart Collection](/docs/api/admin-rest/latest/resources/smartcollection) || `read_product_listings` | [Product Listing](/docs/api/admin-rest/latest/resources/productlisting) and [Collection Listing](/docs/api/admin-rest/latest/resources/collectionlisting) || `read_reports`,`write_reports` | [Reports](/docs/api/admin-rest/latest/resources/report) || `read_resource_feedbacks`,`write_resource_feedbacks` | [ResourceFeedback](/docs/api/admin-rest/latest/resources/resourcefeedback) || `read_script_tags`,`write_script_tags` | [Script Tag](/docs/api/admin-rest/latest/resources/scripttag) || `read_shipping`,`write_shipping` | [Carrier Service](/docs/api/admin-rest/latest/resources/carrierservice), [Country](/docs/api/admin-rest/latest/resources/country), and [Province](/docs/api/admin-rest/latest/resources/province) || `read_shopify_payments_disputes` | Shopify Payments [Dispute](/docs/api/admin-rest/latest/resources/dispute) resource || `read_shopify_payments_dispute_evidences` | Shopify Payments [Dispute Evidence](/docs/api/admin-rest/latest/resources/dispute-evidence) resource || `read_shopify_payments_payouts` | Shopify Payments [Payouts](/docs/api/admin-rest/latest/resources/payouts), [Balance](/docs/api/admin-rest/latest/resources/balance), and [Transaction](/docs/api/admin-rest/latest/resources/transaction) resources || `read_themes`,`write_themes` | [Asset](/docs/api/admin-rest/latest/resources/asset) and [Theme](/docs/api/admin-rest/latest/resources/theme) || `read_third_party_fulfillment_orders`,`write_third_party_fulfillment_orders` | [FulfillmentOrder](/docs/api/admin-rest/latest/resources/fulfillmentorder) resources assigned to a location managed by any [fulfillment service](/docs/api/admin-rest/latest/resources/fulfillmentservice)As of API version 2024-10, fulfillment orders that are assigned to a fulfillment service can only be fulfilled by the [fulfillment service app](/docs/apps/build/orders-fulfillment/fulfillment-service-apps) that manages the location they are assigned to. || `read_users` | [User](/docs/api/admin-rest/latest/resources/user)shopify plus |

## [Anchor to Checking granted access scopes](/docs/api/admin-rest/usage/access-scopes#checking-granted-access-scopes)Checking granted access scopesYou can check your app’s granted access scopes. The following is an example request:REST requestJSON responseCopy91GET https://{store_name}.myshopify.com/admin/oauth/access_scopes.json9912345678910111213{  "access_scopes": [    {      "handle": "read_products"    },    {      "handle": "write_orders"    },    {      "handle": "read_orders"    }  ]}REST request```

GET https://{store_name}.myshopify.com/admin/oauth/access_scopes.json

```JSON response```

{

"access_scopes": [

{

"handle": "read_products"

},

{

"handle": "write_orders"

},

{

"handle": "read_orders"

}

]

}

```

## [Anchor to Limitations and considerations](/docs/api/admin-rest/usage/access-scopes#limitations-and-considerations)Limitations and considerations

Apps should request only the minimum amount of data that's necessary for an app to function when using a Shopify API. Shopify restricts access to scopes for apps that don't require legitimate use of the associated data.

- Only [public or custom apps](/docs/apps/launch/distribution) are granted access scopes. Legacy app types, such as private or unpublished, won't be granted new access scopes.

Was this page helpful?YesNo- [How it works](/docs/api/admin-rest/usage/access-scopes#how-it-works)- [Authenticated access scopes](/docs/api/admin-rest/usage/access-scopes#authenticated-access-scopes)- [Checking granted access scopes](/docs/api/admin-rest/usage/access-scopes#checking-granted-access-scopes)- [Limitations and considerations](/docs/api/admin-rest/usage/access-scopes#limitations-and-considerations)### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)