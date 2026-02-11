---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront/latest/objects/Order",
    "fetched_at": "2026-02-10T13:41:05.459421",
    "status": 200,
    "size_bytes": 401616
  },
  "metadata": {
    "title": "Order - Storefront API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "objects",
    "component": "Order"
  }
}
---

# Order - Storefront API

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to Order](/docs/api/storefront/latest/objects/Order#top)# OrderobjectAsk assistantRequires `unauthenticated_read_customers` access scope.

An order is a customer’s completed request to purchase one or more products from a shop. An order is created when a customer completes the checkout process, during which time they provides an email address, billing address and payment information.

## [Anchor to Fields](/docs/api/storefront/latest/objects/Order#fields)Fields- billingAddress (MailingAddress)- canceledAt (DateTime)- cancelReason (OrderCancelReason)- currencyCode (CurrencyCode!)- currentSubtotalPrice (MoneyV2!)- currentTotalDuties (MoneyV2)- currentTotalPrice (MoneyV2!)- currentTotalShippingPrice (MoneyV2!)- currentTotalTax (MoneyV2!)- customAttributes ([Attribute!]!)- customerLocale (String)- customerUrl (URL)- discountApplications (DiscountApplicationConnection!)- edited (Boolean!)- email (String)- financialStatus (OrderFinancialStatus)- fulfillmentStatus (OrderFulfillmentStatus!)- id (ID!)- lineItems (OrderLineItemConnection!)- metafield (Metafield)- metafields ([Metafield]!)- name (String!)- orderNumber (Int!)- originalTotalDuties (MoneyV2)- originalTotalPrice (MoneyV2!)- phone (String)- processedAt (DateTime!)- shippingAddress (MailingAddress)- shippingDiscountAllocations ([DiscountAllocation!]!)- statusUrl (URL!)- subtotalPrice (MoneyV2)- successfulFulfillments ([Fulfillment!])- totalPrice (MoneyV2!)- totalRefunded (MoneyV2!)- totalShippingPrice (MoneyV2!)- totalTax (MoneyV2)[Anchor to billingAddress](/docs/api/storefront/latest/objects/Order#field-Order.fields.billingAddress)billingAddress•[MailingAddress](/docs/api/storefront/latest/objects/MailingAddress) Token access requiredThe address associated with the payment method.

Show fields[Anchor to canceledAt](/docs/api/storefront/latest/objects/Order#field-Order.fields.canceledAt)canceledAt•[DateTime](/docs/api/storefront/latest/scalars/DateTime) Token access requiredThe date and time when the order was canceled. Returns null if the order wasn't canceled.

[Anchor to cancelReason](/docs/api/storefront/latest/objects/Order#field-Order.fields.cancelReason)cancelReason•[OrderCancelReason](/docs/api/storefront/latest/enums/OrderCancelReason) Token access requiredThe reason for the order's cancellation. Returns `null` if the order wasn't canceled.

Show enum values[Anchor to currencyCode](/docs/api/storefront/latest/objects/Order#field-Order.fields.currencyCode)currencyCode•[CurrencyCode!](/docs/api/storefront/latest/enums/CurrencyCode)non-null Token access requiredThe code of the currency used for the payment.

Show enum values[Anchor to currentSubtotalPrice](/docs/api/storefront/latest/objects/Order#field-Order.fields.currentSubtotalPrice)currentSubtotalPrice•[MoneyV2!](/docs/api/storefront/latest/objects/MoneyV2)non-null Token access requiredThe subtotal of line items and their discounts, excluding line items that have been removed. Does not contain order-level discounts, duties, shipping costs, or shipping discounts. Taxes aren't included unless the order is a taxes-included order.

Show fields[Anchor to currentTotalDuties](/docs/api/storefront/latest/objects/Order#field-Order.fields.currentTotalDuties)currentTotalDuties•[MoneyV2](/docs/api/storefront/latest/objects/MoneyV2) Token access requiredThe total cost of duties for the order, including refunds.

Show fields[Anchor to currentTotalPrice](/docs/api/storefront/latest/objects/Order#field-Order.fields.currentTotalPrice)currentTotalPrice•[MoneyV2!](/docs/api/storefront/latest/objects/MoneyV2)non-null Token access requiredThe total amount of the order, including duties, taxes and discounts, minus amounts for line items that have been removed.

Show fields[Anchor to currentTotalShippingPrice](/docs/api/storefront/latest/objects/Order#field-Order.fields.currentTotalShippingPrice)currentTotalShippingPrice•[MoneyV2!](/docs/api/storefront/latest/objects/MoneyV2)non-null Token access requiredThe total cost of shipping, excluding shipping lines that have been refunded or removed. Taxes aren't included unless the order is a taxes-included order.

Show fields[Anchor to currentTotalTax](/docs/api/storefront/latest/objects/Order#field-Order.fields.currentTotalTax)currentTotalTax•[MoneyV2!](/docs/api/storefront/latest/objects/MoneyV2)non-null Token access requiredThe total of all taxes applied to the order, excluding taxes for returned line items.

Show fields[Anchor to customAttributes](/docs/api/storefront/latest/objects/Order#field-Order.fields.customAttributes)customAttributes•[[Attribute!]!](/docs/api/storefront/latest/objects/Attribute)non-null Token access requiredA list of the custom attributes added to the order. For example, whether an order is a customer's first.

Show fields[Anchor to customerLocale](/docs/api/storefront/latest/objects/Order#field-Order.fields.customerLocale)customerLocale•[String](/docs/api/storefront/latest/scalars/String) Token access requiredThe locale code in which this specific order happened.

[Anchor to customerUrl](/docs/api/storefront/latest/objects/Order#field-Order.fields.customerUrl)customerUrl•[URL](/docs/api/storefront/latest/scalars/URL) Token access requiredThe unique URL that the customer can use to access the order.

[Anchor to discountApplications](/docs/api/storefront/latest/objects/Order#field-Order.fields.discountApplications)discountApplications•[DiscountApplicationConnection!](/docs/api/storefront/latest/connections/DiscountApplicationConnection)non-null Token access requiredDiscounts that have been applied on the order.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/objects/Order#field-Order.fields.discountApplications.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/objects/Order#field-Order.fields.discountApplications.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/objects/Order#field-Order.fields.discountApplications.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/objects/Order#field-Order.fields.discountApplications.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/objects/Order#field-Order.fields.discountApplications.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to edited](/docs/api/storefront/latest/objects/Order#field-Order.fields.edited)edited•[Boolean!](/docs/api/storefront/latest/scalars/Boolean)non-null Token access requiredWhether the order has had any edits applied or not.

[Anchor to email](/docs/api/storefront/latest/objects/Order#field-Order.fields.email)email•[String](/docs/api/storefront/latest/scalars/String) Token access requiredThe customer's email address.

[Anchor to financialStatus](/docs/api/storefront/latest/objects/Order#field-Order.fields.financialStatus)financialStatus•[OrderFinancialStatus](/docs/api/storefront/latest/enums/OrderFinancialStatus) Token access requiredThe financial status of the order.

Show enum values[Anchor to fulfillmentStatus](/docs/api/storefront/latest/objects/Order#field-Order.fields.fulfillmentStatus)fulfillmentStatus•[OrderFulfillmentStatus!](/docs/api/storefront/latest/enums/OrderFulfillmentStatus)non-null Token access requiredThe fulfillment status for the order.

Show enum values[Anchor to id](/docs/api/storefront/latest/objects/Order#field-Order.fields.id)id•[ID!](/docs/api/storefront/latest/scalars/ID)non-null Token access requiredA globally-unique ID.

[Anchor to lineItems](/docs/api/storefront/latest/objects/Order#field-Order.fields.lineItems)lineItems•[OrderLineItemConnection!](/docs/api/storefront/latest/connections/OrderLineItemConnection)non-null Token access requiredList of the order’s line items.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/objects/Order#field-Order.fields.lineItems.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/objects/Order#field-Order.fields.lineItems.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/objects/Order#field-Order.fields.lineItems.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/objects/Order#field-Order.fields.lineItems.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/objects/Order#field-Order.fields.lineItems.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to metafield](/docs/api/storefront/latest/objects/Order#field-Order.fields.metafield)metafield•[Metafield](/docs/api/storefront/latest/objects/Metafield) Token access requiredA [custom field](https://shopify.dev/docs/apps/build/custom-data), including its `namespace` and `key`, that's associated with a Shopify resource for the purposes of adding and storing additional information.

Show fields### Arguments[Anchor to namespace](/docs/api/storefront/latest/objects/Order#field-Order.fields.metafield.arguments.namespace)namespace•[String](/docs/api/storefront/latest/scalars/String)The container the metafield belongs to. If omitted, the app-reserved namespace will be used.

[Anchor to key](/docs/api/storefront/latest/objects/Order#field-Order.fields.metafield.arguments.key)key•[String!](/docs/api/storefront/latest/scalars/String)requiredThe identifier for the metafield.

[Anchor to metafields](/docs/api/storefront/latest/objects/Order#field-Order.fields.metafields)metafields•[[Metafield]!](/docs/api/storefront/latest/objects/Metafield)non-null Token access requiredA list of [custom fields](/docs/apps/build/custom-data) that a merchant associates with a Shopify resource.

Show fields### Arguments[Anchor to identifiers](/docs/api/storefront/latest/objects/Order#field-Order.fields.metafields.arguments.identifiers)identifiers•[[HasMetafieldsIdentifier!]!](/docs/api/storefront/latest/input-objects/HasMetafieldsIdentifier)requiredThe list of metafields to retrieve by namespace and key.

The input must not contain more than `250` values.

Show input fields[Anchor to name](/docs/api/storefront/latest/objects/Order#field-Order.fields.name)name•[String!](/docs/api/storefront/latest/scalars/String)non-null Token access requiredUnique identifier for the order that appears on the order.

For example, *#1000* or _Store1001.

[Anchor to orderNumber](/docs/api/storefront/latest/objects/Order#field-Order.fields.orderNumber)orderNumber•[Int!](/docs/api/storefront/latest/scalars/Int)non-null Token access requiredA unique numeric identifier for the order for use by shop owner and customer.

[Anchor to originalTotalDuties](/docs/api/storefront/latest/objects/Order#field-Order.fields.originalTotalDuties)originalTotalDuties•[MoneyV2](/docs/api/storefront/latest/objects/MoneyV2) Token access requiredThe total cost of duties charged at checkout.

Show fields[Anchor to originalTotalPrice](/docs/api/storefront/latest/objects/Order#field-Order.fields.originalTotalPrice)originalTotalPrice•[MoneyV2!](/docs/api/storefront/latest/objects/MoneyV2)non-null Token access requiredThe total price of the order before any applied edits.

Show fields[Anchor to phone](/docs/api/storefront/latest/objects/Order#field-Order.fields.phone)phone•[String](/docs/api/storefront/latest/scalars/String) Token access requiredThe customer's phone number for receiving SMS notifications.

[Anchor to processedAt](/docs/api/storefront/latest/objects/Order#field-Order.fields.processedAt)processedAt•[DateTime!](/docs/api/storefront/latest/scalars/DateTime)non-null Token access requiredThe date and time when the order was imported.

This value can be set to dates in the past when importing from other systems.

If no value is provided, it will be auto-generated based on current date and time.

[Anchor to shippingAddress](/docs/api/storefront/latest/objects/Order#field-Order.fields.shippingAddress)shippingAddress•[MailingAddress](/docs/api/storefront/latest/objects/MailingAddress) Token access requiredThe address to where the order will be shipped.

Show fields[Anchor to shippingDiscountAllocations](/docs/api/storefront/latest/objects/Order#field-Order.fields.shippingDiscountAllocations)shippingDiscountAllocations•[[DiscountAllocation!]!](/docs/api/storefront/latest/objects/DiscountAllocation)non-null Token access requiredThe discounts that have been allocated onto the shipping line by discount applications.

Show fields[Anchor to statusUrl](/docs/api/storefront/latest/objects/Order#field-Order.fields.statusUrl)statusUrl•[URL!](/docs/api/storefront/latest/scalars/URL)non-null Token access requiredThe unique URL for the order's status page.

[Anchor to subtotalPrice](/docs/api/storefront/latest/objects/Order#field-Order.fields.subtotalPrice)subtotalPrice•[MoneyV2](/docs/api/storefront/latest/objects/MoneyV2) Token access requiredPrice of the order before shipping and taxes.

Show fields[Anchor to successfulFulfillments](/docs/api/storefront/latest/objects/Order#field-Order.fields.successfulFulfillments)successfulFulfillments•[[Fulfillment!]](/docs/api/storefront/latest/objects/Fulfillment) Token access requiredList of the order’s successful fulfillments.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/objects/Order#field-Order.fields.successfulFulfillments.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Truncate the array result to this size.

[Anchor to totalPrice](/docs/api/storefront/latest/objects/Order#field-Order.fields.totalPrice)totalPrice•[MoneyV2!](/docs/api/storefront/latest/objects/MoneyV2)non-null Token access requiredThe sum of all the prices of all the items in the order, duties, taxes and discounts included (must be positive).

Show fields[Anchor to totalRefunded](/docs/api/storefront/latest/objects/Order#field-Order.fields.totalRefunded)totalRefunded•[MoneyV2!](/docs/api/storefront/latest/objects/MoneyV2)non-null Token access requiredThe total amount that has been refunded.

Show fields[Anchor to totalShippingPrice](/docs/api/storefront/latest/objects/Order#field-Order.fields.totalShippingPrice)totalShippingPrice•[MoneyV2!](/docs/api/storefront/latest/objects/MoneyV2)non-null Token access requiredThe total cost of shipping.

Show fields[Anchor to totalTax](/docs/api/storefront/latest/objects/Order#field-Order.fields.totalTax)totalTax•[MoneyV2](/docs/api/storefront/latest/objects/MoneyV2) Token access requiredThe total cost of taxes.

Show fields### Deprecated fields- subtotalPriceV2 (MoneyV2): deprecated- totalPriceV2 (MoneyV2!): deprecated- totalRefundedV2 (MoneyV2!): deprecated- totalShippingPriceV2 (MoneyV2!): deprecated- totalTaxV2 (MoneyV2): deprecated[Anchor to subtotalPriceV2](/docs/api/storefront/latest/objects/Order#field-Order.fields.subtotalPriceV2)subtotalPriceV2•[MoneyV2](/docs/api/storefront/latest/objects/MoneyV2)Deprecated Token access requiredShow fields[Anchor to totalPriceV2](/docs/api/storefront/latest/objects/Order#field-Order.fields.totalPriceV2)totalPriceV2•[MoneyV2!](/docs/api/storefront/latest/objects/MoneyV2)non-nullDeprecated Token access requiredShow fields[Anchor to totalRefundedV2](/docs/api/storefront/latest/objects/Order#field-Order.fields.totalRefundedV2)totalRefundedV2•[MoneyV2!](/docs/api/storefront/latest/objects/MoneyV2)non-nullDeprecated Token access requiredShow fields[Anchor to totalShippingPriceV2](/docs/api/storefront/latest/objects/Order#field-Order.fields.totalShippingPriceV2)totalShippingPriceV2•[MoneyV2!](/docs/api/storefront/latest/objects/MoneyV2)non-nullDeprecated Token access requiredShow fields[Anchor to totalTaxV2](/docs/api/storefront/latest/objects/Order#field-Order.fields.totalTaxV2)totalTaxV2•[MoneyV2](/docs/api/storefront/latest/objects/MoneyV2)Deprecated Token access requiredShow fieldsWas this section helpful?YesNo## Map### Fields and connections with this object- {}[Customer.orders](/docs/api/storefront/latest/objects/Customer#field-Customer.fields.orders)- <->[OrderConnection.nodes](/docs/api/storefront/latest/connections/OrderConnection#returns-nodes)- {}[OrderEdge.node](/docs/api/storefront/latest/objects/OrderEdge#field-OrderEdge.fields.node)### Possible type in- [MetafieldParentResource](/docs/api/storefront/latest/unions/MetafieldParentResource)## [Anchor to Interfaces](/docs/api/storefront/latest/objects/Order#interfaces)Interfaces- HasMetafields- Node[Anchor to HasMetafields](/docs/api/storefront/latest/objects/Order#interface-HasMetafields)[HasMetafields](/docs/api/storefront/latest/interfaces/HasMetafields)•interface[Anchor to Node](/docs/api/storefront/latest/objects/Order#interface-Node)[Node](/docs/api/storefront/latest/interfaces/Node)•interfaceWas this section helpful?YesNo## ||-Order Implements### Implements- ||-[HasMetafields](/docs/api/storefront/latest/interfaces/HasMetafields)- ||-[Node](/docs/api/storefront/latest/interfaces/Node)### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)