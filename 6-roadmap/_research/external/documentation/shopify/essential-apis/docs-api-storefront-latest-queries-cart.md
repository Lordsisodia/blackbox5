---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront/latest/queries/cart",
    "fetched_at": "2026-02-10T13:41:29.855285",
    "status": 200,
    "size_bytes": 365799
  },
  "metadata": {
    "title": "cart - Storefront API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "queries",
    "component": "cart"
  }
}
---

# cart - Storefront API

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to cart](/docs/api/storefront/latest/queries/cart#top)# cartqueryAsk assistantRetrieve a cart by its ID. For more information, refer to

[Manage a cart with the Storefront API](https://shopify.dev/custom-storefronts/cart/manage).

[Anchor to Arguments](/docs/api/storefront/latest/queries/cart#arguments)## Arguments- id (ID!)[Anchor to id](/docs/api/storefront/latest/queries/cart#arguments-id)id•[ID!](/docs/api/storefront/latest/scalars/ID)requiredThe ID of the cart.

Was this section helpful?YesNo## [Anchor to Possible returns](/docs/api/storefront/latest/queries/cart#possible-returns)Possible returns- Cart (Cart)[Anchor to Cart](/docs/api/storefront/latest/queries/cart#returns-Cart)Cart•[Cart](/docs/api/storefront/latest/objects/Cart)A cart represents the merchandise that a buyer intends to purchase,

and the estimated cost associated with the cart. Learn how to

[interact with a cart](https://shopify.dev/custom-storefronts/internationalization/international-pricing)

during a customer's session.

Show fields[Anchor to appliedGiftCards](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.appliedGiftCards)appliedGiftCards•[[AppliedGiftCard!]!](/docs/api/storefront/latest/objects/AppliedGiftCard)non-nullThe gift cards that have been applied to the cart.

Show fields[Anchor to attribute](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.attribute)attribute•[Attribute](/docs/api/storefront/latest/objects/Attribute)An attribute associated with the cart.

Show fields### Arguments[Anchor to key](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.attribute.arguments.key)key•[String!](/docs/api/storefront/latest/scalars/String)requiredThe key of the attribute.

[Anchor to attributes](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.attributes)attributes•[[Attribute!]!](/docs/api/storefront/latest/objects/Attribute)non-nullThe attributes associated with the cart. Attributes are represented as key-value pairs.

Show fields[Anchor to buyerIdentity](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.buyerIdentity)buyerIdentity•[CartBuyerIdentity!](/docs/api/storefront/latest/objects/CartBuyerIdentity)non-nullInformation about the buyer that's interacting with the cart.

Show fields[Anchor to checkoutUrl](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.checkoutUrl)checkoutUrl•[URL!](/docs/api/storefront/latest/scalars/URL)non-nullThe URL of the checkout for the cart.

[Anchor to cost](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.cost)cost•[CartCost!](/docs/api/storefront/latest/objects/CartCost)non-nullThe estimated costs that the buyer will pay at checkout. The costs are subject to change and changes will be reflected at checkout. The `cost` field uses the `buyerIdentity` field to determine [international pricing](https://shopify.dev/custom-storefronts/internationalization/international-pricing).

Show fields[Anchor to createdAt](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.createdAt)createdAt•[DateTime!](/docs/api/storefront/latest/scalars/DateTime)non-nullThe date and time when the cart was created.

[Anchor to delivery](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.delivery)delivery•[CartDelivery!](/docs/api/storefront/latest/objects/CartDelivery)non-nullThe delivery properties of the cart.

Show fields[Anchor to deliveryGroups](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.deliveryGroups)deliveryGroups•[CartDeliveryGroupConnection!](/docs/api/storefront/latest/connections/CartDeliveryGroupConnection)non-nullThe delivery groups available for the cart, based on the buyer identity default

delivery address preference or the default address of the logged-in customer.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.deliveryGroups.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.deliveryGroups.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.deliveryGroups.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.deliveryGroups.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.deliveryGroups.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to withCarrierRates](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.deliveryGroups.arguments.withCarrierRates)withCarrierRates•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseWhether to include [carrier-calculated delivery rates](https://help.shopify.com/en/manual/shipping/setting-up-and-managing-your-shipping/enabling-shipping-carriers) in the response.

By default, only static shipping rates are returned. This argument requires mandatory usage of the [`@defer` directive](https://shopify.dev/docs/api/storefront#directives).

For more information, refer to [fetching carrier-calculated rates for the cart using `@defer`](https://shopify.dev/docs/storefronts/headless/building-with-the-storefront-api/defer#fetching-carrier-calculated-rates-for-the-cart-using-defer).

[Anchor to discountAllocations](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.discountAllocations)discountAllocations•[[CartDiscountAllocation!]!](/docs/api/storefront/latest/interfaces/CartDiscountAllocation)non-nullThe discounts that have been applied to the entire cart.

Show fields[Anchor to discountCodes](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.discountCodes)discountCodes•[[CartDiscountCode!]!](/docs/api/storefront/latest/objects/CartDiscountCode)non-nullThe case-insensitive discount codes that the customer added at checkout.

Show fields[Anchor to id](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.id)id•[ID!](/docs/api/storefront/latest/scalars/ID)non-nullA globally-unique ID.

[Anchor to lines](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.lines)lines•[BaseCartLineConnection!](/docs/api/storefront/latest/connections/BaseCartLineConnection)non-nullA list of lines containing information about the items the customer intends to purchase.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.lines.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.lines.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.lines.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.lines.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.lines.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to metafield](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.metafield)metafield•[Metafield](/docs/api/storefront/latest/objects/Metafield) Token access requiredA [custom field](https://shopify.dev/docs/apps/build/custom-data), including its `namespace` and `key`, that's associated with a Shopify resource for the purposes of adding and storing additional information.

Show fields### Arguments[Anchor to namespace](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.metafield.arguments.namespace)namespace•[String](/docs/api/storefront/latest/scalars/String)The container the metafield belongs to. If omitted, the app-reserved namespace will be used.

[Anchor to key](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.metafield.arguments.key)key•[String!](/docs/api/storefront/latest/scalars/String)requiredThe identifier for the metafield.

[Anchor to metafields](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.metafields)metafields•[[Metafield]!](/docs/api/storefront/latest/objects/Metafield)non-null Token access requiredA list of [custom fields](/docs/apps/build/custom-data) that a merchant associates with a Shopify resource.

Show fields### Arguments[Anchor to identifiers](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.metafields.arguments.identifiers)identifiers•[[HasMetafieldsIdentifier!]!](/docs/api/storefront/latest/input-objects/HasMetafieldsIdentifier)requiredThe list of metafields to retrieve by namespace and key.

The input must not contain more than `250` values.

Show input fields[Anchor to note](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.note)note•[String](/docs/api/storefront/latest/scalars/String)A note that's associated with the cart. For example, the note can be a personalized message to the buyer.

[Anchor to totalQuantity](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.totalQuantity)totalQuantity•[Int!](/docs/api/storefront/latest/scalars/Int)non-nullThe total number of items in the cart.

[Anchor to updatedAt](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.updatedAt)updatedAt•[DateTime!](/docs/api/storefront/latest/scalars/DateTime)non-nullThe date and time when the cart was updated.

[Anchor to estimatedCost](/docs/api/storefront/latest/queries/cart#returns-Cart.fields.estimatedCost)estimatedCost•[CartEstimatedCost!](/docs/api/storefront/latest/objects/CartEstimatedCost)non-nullDeprecatedShow fieldsWas this section helpful?YesNo## Examples- ### cart referenceHide content## Query Reference Copy912345›⌄⌄{  cart(id) {    # cart fields  }}### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)