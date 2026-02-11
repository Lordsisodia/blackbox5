---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-graphql/latest/objects/Order",
    "fetched_at": "2026-02-10T13:40:58.893958",
    "status": 200,
    "size_bytes": 1030717
  },
  "metadata": {
    "title": "Order - GraphQL Admin",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "objects",
    "component": "Order"
  }
}
---

# Order - GraphQL Admin

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to Order](/docs/api/admin-graphql/latest/objects/Order#top)# OrderobjectAsk assistantRequires `read_orders` access scope, `read_marketplace_orders` access scope or `read_quick_sale` access scope.

The `Order` object represents a customer's request to purchase one or more products from a store. Use the `Order` object to handle the complete purchase lifecycle from checkout to fulfillment.

Use the `Order` object when you need to:

- Display order details on customer account pages or admin dashboards.

- Create orders for phone sales, wholesale customers, or subscription services.

- Update order information like shipping addresses, notes, or fulfillment status.

- Process returns, exchanges, and partial refunds.

- Generate invoices, receipts, and shipping labels.

The `Order` object serves as the central hub connecting customer information, product details, payment processing, and fulfillment data within the GraphQL Admin API schema.

NoteOnly the last 60 days' worth of orders from a store are accessible from the `Order` object by default. If you want to access older records,

then you need to [request access to all orders](https://shopify.dev/docs/api/usage/access-scopes#orders-permissions). If your app is granted

access, then you can add the `read_all_orders`, `read_orders`, and `write_orders` scopes.**Note:** Only the last 60 days' worth of orders from a store are accessible from the `Order` object by default. If you want to access older records,

then you need to [request access to all orders](https://shopify.dev/docs/api/usage/access-scopes#orders-permissions). If your app is granted

access, then you can add the `read_all_orders`, `read_orders`, and `write_orders` scopes.**Note:** Only the last 60 days&#39; worth of orders from a store are accessible from the <code>Order</code> object by default. If you want to access older records,

then you need to <a href="https://shopify.dev/docs/api/usage/access-scopes#orders-permissions">request access to all orders</a>. If your app is granted

access, then you can add the <code><span class="PreventFireFoxApplyingGapToWBR">read<wbr/>_all<wbr/>_orders</span></code>, <code><span class="PreventFireFoxApplyingGapToWBR">read<wbr/>_orders</span></code>, and <code><span class="PreventFireFoxApplyingGapToWBR">write<wbr/>_orders</span></code> scopes.CautionOnly use orders data if it's required for your app's functionality. Shopify will restrict [access to scopes](https://shopify.dev/docs/api/usage/access-scopes#requesting-specific-permissions) for apps that don't have a legitimate use for the associated data.**Caution:** Only use orders data if it's required for your app's functionality. Shopify will restrict [access to scopes](https://shopify.dev/docs/api/usage/access-scopes#requesting-specific-permissions) for apps that don't have a legitimate use for the associated data.**Caution:** Only use orders data if it&#39;s required for your app&#39;s functionality. Shopify will restrict <a href="https://shopify.dev/docs/api/usage/access-scopes#requesting-specific-permissions">access to scopes</a> for apps that don&#39;t have a legitimate use for the associated data.Learn more about [building apps for orders and fulfillment](https://shopify.dev/docs/apps/build/orders-fulfillment).

## [Anchor to Fields](/docs/api/admin-graphql/latest/objects/Order#fields)Fields- additionalFees ([AdditionalFee!]!)- agreements (SalesAgreementConnection!)- alerts ([ResourceAlert!]!)- app (OrderApp)- billingAddress (MailingAddress)- billingAddressMatchesShippingAddress (Boolean!)- cancellation (OrderCancellation)- cancelledAt (DateTime)- cancelReason (OrderCancelReason)- canMarkAsPaid (Boolean!)- canNotifyCustomer (Boolean!)- capturable (Boolean!)- cartDiscountAmountSet (MoneyBag)- channelInformation (ChannelInformation)- clientIp (String)- closed (Boolean!)- closedAt (DateTime)- confirmationNumber (String)- confirmed (Boolean!)- createdAt (DateTime!)- currencyCode (CurrencyCode!)- currentCartDiscountAmountSet (MoneyBag!)- currentShippingPriceSet (MoneyBag!)- currentSubtotalLineItemsQuantity (Int!)- currentSubtotalPriceSet (MoneyBag!)- currentTaxLines ([TaxLine!]!)- currentTotalAdditionalFeesSet (MoneyBag)- currentTotalDiscountsSet (MoneyBag!)- currentTotalDutiesSet (MoneyBag)- currentTotalPriceSet (MoneyBag!)- currentTotalTaxSet (MoneyBag!)- currentTotalWeight (UnsignedInt64!)- customAttributes ([Attribute!]!)- customer (Customer)- customerAcceptsMarketing (Boolean!)- customerJourneySummary (CustomerJourneySummary)- customerLocale (String)- discountApplications (DiscountApplicationConnection!)- discountCode (String)- discountCodes ([String!]!)- displayAddress (MailingAddress)- displayFinancialStatus (OrderDisplayFinancialStatus)- displayFulfillmentStatus (OrderDisplayFulfillmentStatus!)- disputes ([OrderDisputeSummary!]!)- dutiesIncluded (Boolean!)- edited (Boolean!)- email (String)- estimatedTaxes (Boolean!)- events (EventConnection!)- fulfillable (Boolean!)- fulfillmentOrders (FulfillmentOrderConnection!)- fulfillments ([Fulfillment!]!)- fulfillmentsCount (Count)- fullyPaid (Boolean!)- hasTimelineComment (Boolean!)- id (ID!)- legacyResourceId (UnsignedInt64!)- lineItems (LineItemConnection!)- localizedFields (LocalizedFieldConnection!)- merchantBusinessEntity (BusinessEntity!)- merchantEditable (Boolean!)- merchantEditableErrors ([String!]!)- merchantOfRecordApp (OrderApp)- metafield (Metafield)- metafields (MetafieldConnection!)- name (String!)- netPaymentSet (MoneyBag!)- nonFulfillableLineItems (LineItemConnection!)- note (String)- number (Int!)- originalTotalAdditionalFeesSet (MoneyBag)- originalTotalDutiesSet (MoneyBag)- originalTotalPriceSet (MoneyBag!)- paymentCollectionDetails (OrderPaymentCollectionDetails!)- paymentGatewayNames ([String!]!)- paymentTerms (PaymentTerms)- phone (String)- poNumber (String)- presentmentCurrencyCode (CurrencyCode!)- processedAt (DateTime!)- productNetwork (Boolean!)- publication (Publication)- purchasingEntity (PurchasingEntity)- refundable (Boolean!)- refundDiscrepancySet (MoneyBag!)- refunds ([Refund!]!)- registeredSourceUrl (URL)- requiresShipping (Boolean!)- restockable (Boolean!)- retailLocation (Location)- returns (ReturnConnection!)- returnStatus (OrderReturnStatus!)- risk (OrderRiskSummary!)- shippingAddress (MailingAddress)- shippingLine (ShippingLine)- shippingLines (ShippingLineConnection!)- shopifyProtect (ShopifyProtectOrderSummary)- sourceIdentifier (String)- sourceName (String)- staffMember (StaffMember)- statusPageUrl (URL!)- subtotalLineItemsQuantity (Int!)- subtotalPriceSet (MoneyBag)- suggestedRefund (SuggestedRefund)- tags ([String!]!)- taxesIncluded (Boolean!)- taxExempt (Boolean!)- taxLines ([TaxLine!]!)- test (Boolean!)- totalCapturableSet (MoneyBag!)- totalCashRoundingAdjustment (CashRoundingAdjustment!)- totalDiscountsSet (MoneyBag)- totalOutstandingSet (MoneyBag!)- totalPriceSet (MoneyBag!)- totalReceivedSet (MoneyBag!)- totalRefundedSet (MoneyBag!)- totalRefundedShippingSet (MoneyBag!)- totalShippingPriceSet (MoneyBag!)- totalTaxSet (MoneyBag)- totalTipReceivedSet (MoneyBag!)- totalWeight (UnsignedInt64)- transactions ([OrderTransaction!]!)- transactionsCount (Count)- unpaid (Boolean!)- updatedAt (DateTime!)[Anchor to additionalFees](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.additionalFees)additionalFees•[[AdditionalFee!]!](/docs/api/admin-graphql/latest/objects/AdditionalFee)non-nullA list of additional fees applied to an order, such as duties, import fees, or [tax lines](https://shopify.dev/docs/api/admin-graphql/latest/objects/order#field-Order.fields.additionalFees.taxLines).

Show fields[Anchor to agreements](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.agreements)agreements•[SalesAgreementConnection!](/docs/api/admin-graphql/latest/connections/SalesAgreementConnection)non-nullA list of sales agreements associated with the order, such as contracts defining payment terms, or delivery schedules between merchants and customers.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.agreements.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.agreements.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.agreements.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.agreements.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.agreements.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to query](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.agreements.arguments.query)query•[String](/docs/api/admin-graphql/latest/scalars/String)A filter made up of terms, connectives, modifiers, and comparators.

You can apply one or more filters to a query. Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-happened_at)happened_at•time[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-id)id•idFilter by `id` range.

Example:- `id:1234`- `id:>=1234`- `id:<=1234`[Anchor to alerts](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.alerts)alerts•[[ResourceAlert!]!](/docs/api/admin-graphql/latest/objects/ResourceAlert)non-nullA list of messages that appear on the **Orders** page in the Shopify admin. These alerts provide merchants with important information about an order's status or required actions.

Show fields[Anchor to app](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.app)app•[OrderApp](/docs/api/admin-graphql/latest/objects/OrderApp)The application that created the order. For example, "Online Store", "Point of Sale", or a custom app name.

Use this to identify the order source for attribution and fulfillment workflows.

Learn more about [building apps for orders and fulfillment](https://shopify.dev/docs/apps/build/orders-fulfillment).

Show fields[Anchor to billingAddress](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.billingAddress)billingAddress•[MailingAddress](/docs/api/admin-graphql/latest/objects/MailingAddress)The billing address associated with the payment method selected by the customer for an order.

Returns `null` if no billing address was provided during checkout.

Show fields[Anchor to billingAddressMatchesShippingAddress](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.billingAddressMatchesShippingAddress)billingAddressMatchesShippingAddress•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the billing address matches the [shipping address](https://shopify.dev/docs/api/admin-graphql/latest/objects/order#field-Order.fields.shippingAddress). Returns `true` if both addresses are the same, and `false` if they're different or if an address is missing.

[Anchor to cancellation](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.cancellation)cancellation•[OrderCancellation](/docs/api/admin-graphql/latest/objects/OrderCancellation)Details of an order's cancellation, if it has been canceled. This includes the reason, date, and any [staff notes](https://shopify.dev/api/admin-graphql/latest/objects/OrderCancellation#field-OrderCancellation.fields.staffNote).

Show fields[Anchor to cancelledAt](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.cancelledAt)cancelledAt•[DateTime](/docs/api/admin-graphql/latest/scalars/DateTime)The date and time in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601) when an order was canceled.

Returns `null` if the order hasn't been canceled.

[Anchor to cancelReason](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.cancelReason)cancelReason•[OrderCancelReason](/docs/api/admin-graphql/latest/enums/OrderCancelReason)The reason provided for an order cancellation. For example, a merchant might cancel an order if there's insufficient inventory. Returns `null` if the order hasn't been canceled.

Show enum values[Anchor to canMarkAsPaid](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.canMarkAsPaid)canMarkAsPaid•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether an order can be manually marked as paid. Returns `false` if the order is already paid, is canceled, has pending [Shopify Payments](https://help.shopify.com/en/manual/payments/shopify-payments/payouts) transactions, or has a negative payment amount.

[Anchor to canNotifyCustomer](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.canNotifyCustomer)canNotifyCustomer•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether order notifications can be sent to the customer.

Returns `true` if the customer has a valid [email address](https://shopify.dev/docs/api/admin-graphql/latest/objects/order#field-Order.fields.email).

[Anchor to capturable](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.capturable)capturable•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether an authorized payment for an order can be captured.

Returns `true` if an authorized payment exists that hasn't been fully captured yet. Learn more about [capturing payments](https://help.shopify.com/en/manual/fulfillment/managing-orders/payments/capturing-payments).

[Anchor to cartDiscountAmountSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.cartDiscountAmountSet)cartDiscountAmountSet•[MoneyBag](/docs/api/admin-graphql/latest/objects/MoneyBag)The total discount amount applied at the time the order was created, displayed in both shop and presentment currencies, before returns, refunds, order edits, and cancellations. This field only includes discounts applied to the entire order.

Show fields[Anchor to channelInformation](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.channelInformation)channelInformation•[ChannelInformation](/docs/api/admin-graphql/latest/objects/ChannelInformation)Details about the sales channel that created the order, such as the [channel app type](https://shopify.dev/docs/api/admin-graphql/latest/objects/channel#field-Channel.fields.channelType)

and [channel name](https://shopify.dev/docs/api/admin-graphql/latest/objects/ChannelDefinition#field-ChannelDefinition.fields.channelName), which helps to track order sources.

Show fields[Anchor to clientIp](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.clientIp)clientIp•[String](/docs/api/admin-graphql/latest/scalars/String)The IP address of the customer who placed the order. Useful for fraud detection and geographic analysis.

[Anchor to closed](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.closed)closed•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether an order is closed. An order is considered closed if all its line items have been fulfilled or canceled, and all financial transactions are complete.

[Anchor to closedAt](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.closedAt)closedAt•[DateTime](/docs/api/admin-graphql/latest/scalars/DateTime)The date and time [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601) when an order was closed. Shopify automatically records this timestamp when all items have been fulfilled or canceled, and all financial transactions are complete. Returns `null` if the order isn't closed.

[Anchor to confirmationNumber](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.confirmationNumber)confirmationNumber•[String](/docs/api/admin-graphql/latest/scalars/String)A customer-facing order identifier, often shown instead of the sequential order name.

It uses a random alphanumeric format (for example, `XPAV284CT`) and isn't guaranteed to be unique across orders.

[Anchor to confirmed](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.confirmed)confirmed•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether inventory has been reserved for an order. Returns `true` if inventory quantities for an order's [line items](https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem) have been reserved.

Learn more about [managing inventory quantities and states](https://shopify.dev/docs/apps/build/orders-fulfillment/inventory-management-apps/manage-quantities-states).

[Anchor to createdAt](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.createdAt)createdAt•[DateTime!](/docs/api/admin-graphql/latest/scalars/DateTime)non-nullThe date and time in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601) when an order was created. This timestamp is set when the customer completes checkout and remains unchanged throughout an order's lifecycle.

[Anchor to currencyCode](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.currencyCode)currencyCode•[CurrencyCode!](/docs/api/admin-graphql/latest/enums/CurrencyCode)non-nullThe shop currency when the order was placed. For example, "USD" or "CAD".

Show enum values[Anchor to currentCartDiscountAmountSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.currentCartDiscountAmountSet)currentCartDiscountAmountSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe current total of all discounts applied to the entire order, after returns, refunds, order edits, and cancellations. This includes discount codes, automatic discounts, and other promotions that affect the whole order rather than individual line items. To get the original discount amount at the time of order creation, use the [`cartDiscountAmountSet`](https://shopify.dev/docs/api/admin-graphql/latest/objects/order#field-Order.fields.cartDiscountAmountSet) field.

Show fields[Anchor to currentShippingPriceSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.currentShippingPriceSet)currentShippingPriceSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe current shipping price after applying refunds and discounts.

If the parent `order.taxesIncluded` field is true, then this price includes taxes. Otherwise, this field is the pre-tax price.

Show fields[Anchor to currentSubtotalLineItemsQuantity](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.currentSubtotalLineItemsQuantity)currentSubtotalLineItemsQuantity•[Int!](/docs/api/admin-graphql/latest/scalars/Int)non-nullThe current sum of the quantities for all line items that contribute to the order's subtotal price, after returns, refunds, order edits, and cancellations.

[Anchor to currentSubtotalPriceSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.currentSubtotalPriceSet)currentSubtotalPriceSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe total price of the order, after returns and refunds, in shop and presentment currencies.

This includes taxes and discounts.

Show fields[Anchor to currentTaxLines](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.currentTaxLines)currentTaxLines•[[TaxLine!]!](/docs/api/admin-graphql/latest/objects/TaxLine)non-nullA list of all tax lines applied to line items on the order, after returns.

Tax line prices represent the total price for all tax lines with the same `rate` and `title`.

Show fields[Anchor to currentTotalAdditionalFeesSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.currentTotalAdditionalFeesSet)currentTotalAdditionalFeesSet•[MoneyBag](/docs/api/admin-graphql/latest/objects/MoneyBag)The current total of all additional fees for an order, after any returns or modifications. Modifications include returns, refunds, order edits, and cancellations. Additional fees can include charges such as duties, import fees, and special handling.

Show fields[Anchor to currentTotalDiscountsSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.currentTotalDiscountsSet)currentTotalDiscountsSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe total amount discounted on the order after returns and refunds, in shop and presentment currencies.

This includes both order and line level discounts.

Show fields[Anchor to currentTotalDutiesSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.currentTotalDutiesSet)currentTotalDutiesSet•[MoneyBag](/docs/api/admin-graphql/latest/objects/MoneyBag)The current total duties amount for an order, after any returns or modifications. Modifications include returns, refunds, order edits, and cancellations.

Show fields[Anchor to currentTotalPriceSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.currentTotalPriceSet)currentTotalPriceSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe total price of the order, after returns, in shop and presentment currencies.

This includes taxes and discounts.

Show fields[Anchor to currentTotalTaxSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.currentTotalTaxSet)currentTotalTaxSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe sum of the prices of all tax lines applied to line items on the order, after returns and refunds, in shop and presentment currencies.

Show fields[Anchor to currentTotalWeight](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.currentTotalWeight)currentTotalWeight•[UnsignedInt64!](/docs/api/admin-graphql/latest/scalars/UnsignedInt64)non-nullThe total weight of the order after returns and refunds, in grams.

[Anchor to customAttributes](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.customAttributes)customAttributes•[[Attribute!]!](/docs/api/admin-graphql/latest/objects/Attribute)non-nullA list of additional information that has been attached to the order. For example, gift message, delivery instructions, or internal notes.

Show fields[Anchor to customer](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.customer)customer•[Customer](/docs/api/admin-graphql/latest/objects/Customer)The customer who placed an order. Returns `null` if an order was created through a checkout without customer authentication, such as a guest checkout.

Learn more about [customer accounts](https://help.shopify.com/manual/customers/customer-accounts).

Show fields[Anchor to customerAcceptsMarketing](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.customerAcceptsMarketing)customerAcceptsMarketing•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the customer agreed to receive marketing emails at the time of purchase.

Use this to ensure compliance with marketing consent laws and to segment customers for email campaigns.

Learn more about [building customer segments](https://shopify.dev/docs/apps/build/marketing-analytics/customer-segments).

[Anchor to customerJourneySummary](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.customerJourneySummary)customerJourneySummary•[CustomerJourneySummary](/docs/api/admin-graphql/latest/objects/CustomerJourneySummary)The customer's visits and interactions with the online store before placing the order.

Use this to understand customer behavior, attribution sources, and marketing effectiveness to optimize your sales funnel.

Show fields[Anchor to customerLocale](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.customerLocale)customerLocale•[String](/docs/api/admin-graphql/latest/scalars/String)The customer's language and region preference at the time of purchase. For example, "en" for English, "fr-CA" for French (Canada), or "es-MX" for Spanish (Mexico).

Use this to provide localized customer service and targeted marketing in the customer's preferred language.

[Anchor to discountApplications](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.discountApplications)discountApplications•[DiscountApplicationConnection!](/docs/api/admin-graphql/latest/connections/DiscountApplicationConnection)non-nullA list of discounts that are applied to the order, excluding order edits and refunds.

Includes discount codes, automatic discounts, and other promotions that reduce the order total.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.discountApplications.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.discountApplications.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.discountApplications.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.discountApplications.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.discountApplications.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to discountCode](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.discountCode)discountCode•[String](/docs/api/admin-graphql/latest/scalars/String)The discount code used for an order. Returns `null` if no discount code was applied.

[Anchor to discountCodes](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.discountCodes)discountCodes•[[String!]!](/docs/api/admin-graphql/latest/scalars/String)non-nullThe discount codes used for the order. Multiple codes can be applied to a single order.

[Anchor to displayAddress](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.displayAddress)displayAddress•[MailingAddress](/docs/api/admin-graphql/latest/objects/MailingAddress)The primary address of the customer, prioritizing shipping address over billing address when both are available.

Returns `null` if neither shipping address nor billing address was provided.

Show fields[Anchor to displayFinancialStatus](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.displayFinancialStatus)displayFinancialStatus•[OrderDisplayFinancialStatus](/docs/api/admin-graphql/latest/enums/OrderDisplayFinancialStatus)An order's financial status for display in the Shopify admin.

Show enum values[Anchor to displayFulfillmentStatus](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.displayFulfillmentStatus)displayFulfillmentStatus•[OrderDisplayFulfillmentStatus!](/docs/api/admin-graphql/latest/enums/OrderDisplayFulfillmentStatus)non-nullThe order's fulfillment status that displays in the Shopify admin to merchants. For example, an order might be unfulfilled or scheduled.

For detailed processing, use the [`FulfillmentOrder`](https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentOrder) object.

Show enum values[Anchor to disputes](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.disputes)disputes•[[OrderDisputeSummary!]!](/docs/api/admin-graphql/latest/objects/OrderDisputeSummary)non-nullA list of payment disputes associated with the order, such as chargebacks or payment inquiries.

Disputes occur when customers challenge transactions with their bank or payment provider.

Show fields[Anchor to dutiesIncluded](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.dutiesIncluded)dutiesIncluded•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether duties are included in the subtotal price of the order.

Duties are import taxes charged by customs authorities when goods cross international borders.

[Anchor to edited](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.edited)edited•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the order has had any edits applied. For example, adding or removing line items, updating quantities, or changing prices.

[Anchor to email](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.email)email•[String](/docs/api/admin-graphql/latest/scalars/String)The email address associated with the customer for this order.

Used for sending order confirmations, shipping notifications, and other order-related communications.

Returns `null` if no email address was provided during checkout.

[Anchor to estimatedTaxes](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.estimatedTaxes)estimatedTaxes•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether taxes on the order are estimated.

This field returns `false` when taxes on the order are finalized and aren't subject to any changes.

[Anchor to events](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.events)events•[EventConnection!](/docs/api/admin-graphql/latest/connections/EventConnection)non-nullA list of events associated with the order. Events track significant changes and activities related to the order, such as creation, payment, fulfillment, and cancellation.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.events.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.events.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.events.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.events.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.events.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.events.arguments.sortKey)sortKey•[EventSortKeys](/docs/api/admin-graphql/latest/enums/EventSortKeys)Default:IDSort the underlying list using a key. If your query is slow or returns an error, then [try specifying a sort key that matches the field used in the search](https://shopify.dev/api/usage/pagination-graphql#search-performance-considerations).

Show enum values[Anchor to query](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.events.arguments.query)query•[String](/docs/api/admin-graphql/latest/scalars/String)A filter made up of terms, connectives, modifiers, and comparators.

You can apply one or more filters to a query. Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-action)action•stringThe action that occured.

Example:- `action:create`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-comments)comments•booleanWhether or not to include [comment-events](https://shopify.dev/api/admin-graphql/latest/objects/CommentEvent) in your search, passing `false` will exclude comment-events, any other value will include comment-events.

Example:- `false`- `true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-created_at)created_at•timeFilter by the date and time when the event occurred. Event data is retained for 1 year.

Example:- `created_at:>2025-10-21`- `created_at:<now`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-id)id•idFilter by `id` range.

Example:- `id:1234`- `id:>=1234`- `id:<=1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-subject_type)subject_type•stringThe resource type affected by this event. See [EventSubjectType](https://shopify.dev/api/admin-graphql/latest/enums/EventSubjectType) for possible values.

Example:- `PRODUCT_VARIANT`- `PRODUCT`- `COLLECTION`[Anchor to fulfillable](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fulfillable)fulfillable•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether there are line items that can be fulfilled.

This field returns `false` when the order has no fulfillable line items.

For a more granular view of the fulfillment status, refer to the [FulfillmentOrder](https://shopify.dev/api/admin-graphql/latest/objects/FulfillmentOrder) object.

[Anchor to fulfillmentOrders](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fulfillmentOrders)fulfillmentOrders•[FulfillmentOrderConnection!](/docs/api/admin-graphql/latest/connections/FulfillmentOrderConnection)non-nullA list of [fulfillment orders](https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentOrder) for an order.

Each fulfillment order groups [line items](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.lineItems) that are fulfilled together,

allowing an order to be processed in parts if needed.

Show fields### Arguments[Anchor to displayable](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fulfillmentOrders.arguments.displayable)displayable•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseIf false, all fulfillment orders will be returned. If true, fulfillment orders that are normally hidden from the merchant will be excluded.

For example, fulfillment orders that were closed after being combined or moved are hidden.

[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fulfillmentOrders.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fulfillmentOrders.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fulfillmentOrders.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fulfillmentOrders.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fulfillmentOrders.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to query](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fulfillmentOrders.arguments.query)query•[String](/docs/api/admin-graphql/latest/scalars/String)A filter made up of terms, connectives, modifiers, and comparators.

You can apply one or more filters to a query. Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-default)default•stringFilter by a case-insensitive search of multiple fields in a document.

Example:- `query=Bob Norman`- `query=title:green hoodie`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-assigned_location_id)assigned_location_id•id[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-id)id•idFilter by `id` range.

Example:- `id:1234`- `id:>=1234`- `id:<=1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-status)status•string[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-updated_at)updated_at•time[Anchor to fulfillments](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fulfillments)fulfillments•[[Fulfillment!]!](/docs/api/admin-graphql/latest/objects/Fulfillment)non-nullA list of shipments for the order. Fulfillments represent the physical shipment of products to customers.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fulfillments.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)Truncate the array result to this size.

[Anchor to query](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fulfillments.arguments.query)query•[String](/docs/api/admin-graphql/latest/scalars/String)Optional query string to filter fulfillments by timestamps. Examples:

`created_at:>='2024-05-07T08:37:00Z' updated_at:<'2025-05-07T08:37:00Z'`,

`created_at:'2024-05-07T08:37:00Z'`

[Anchor to fulfillmentsCount](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fulfillmentsCount)fulfillmentsCount•[Count](/docs/api/admin-graphql/latest/objects/Count)The total number of fulfillments for the order, including canceled ones.

Show fields[Anchor to fullyPaid](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.fullyPaid)fullyPaid•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the order has been paid in full. This field returns `true` when the total amount received equals or exceeds the order total.

[Anchor to hasTimelineComment](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.hasTimelineComment)hasTimelineComment•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the merchant has added a timeline comment to the order.

[Anchor to id](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.id)id•[ID!](/docs/api/admin-graphql/latest/scalars/ID)non-nullA globally-unique ID.

[Anchor to legacyResourceId](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.legacyResourceId)legacyResourceId•[UnsignedInt64!](/docs/api/admin-graphql/latest/scalars/UnsignedInt64)non-nullThe ID of the corresponding resource in the REST Admin API.

[Anchor to lineItems](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.lineItems)lineItems•[LineItemConnection!](/docs/api/admin-graphql/latest/connections/LineItemConnection)non-nullA list of the order's line items. Line items represent the individual products and quantities that make up the order.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.lineItems.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.lineItems.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.lineItems.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.lineItems.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.lineItems.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to localizedFields](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizedFields)localizedFields•[LocalizedFieldConnection!](/docs/api/admin-graphql/latest/connections/LocalizedFieldConnection)non-nullList of localized fields for the resource.

Show fields### Arguments[Anchor to countryCodes](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizedFields.arguments.countryCodes)countryCodes•[[CountryCode!]](/docs/api/admin-graphql/latest/enums/CountryCode)The country codes of the extensions.

Show enum values[Anchor to purposes](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizedFields.arguments.purposes)purposes•[[LocalizedFieldPurpose!]](/docs/api/admin-graphql/latest/enums/LocalizedFieldPurpose)The purpose of the extensions.

Show enum values[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizedFields.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizedFields.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizedFields.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizedFields.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizedFields.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to merchantBusinessEntity](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.merchantBusinessEntity)merchantBusinessEntity•[BusinessEntity!](/docs/api/admin-graphql/latest/objects/BusinessEntity)non-nullThe legal business structure that the merchant operates under for this order, such as an LLC, corporation, or partnership.

Used for tax reporting, legal compliance, and determining which business entity is responsible for the order.

Show fields[Anchor to merchantEditable](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.merchantEditable)merchantEditable•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the order can be edited by the merchant. Returns `false` for orders that can't be modified, such as canceled orders or orders with specific payment statuses.

[Anchor to merchantEditableErrors](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.merchantEditableErrors)merchantEditableErrors•[[String!]!](/docs/api/admin-graphql/latest/scalars/String)non-nullA list of reasons why the order can't be edited. For example, canceled orders can't be edited.

[Anchor to merchantOfRecordApp](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.merchantOfRecordApp)merchantOfRecordApp•[OrderApp](/docs/api/admin-graphql/latest/objects/OrderApp)The application acting as the Merchant of Record for the order. The Merchant of Record is responsible for tax collection and remittance.

Show fields[Anchor to metafield](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafield)metafield•[Metafield](/docs/api/admin-graphql/latest/objects/Metafield)A [custom field](https://shopify.dev/docs/apps/build/custom-data),

including its `namespace` and `key`, that's associated with a Shopify resource

for the purposes of adding and storing additional information.

Show fields### Arguments[Anchor to namespace](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafield.arguments.namespace)namespace•[String](/docs/api/admin-graphql/latest/scalars/String)The container the metafield belongs to. If omitted, the app-reserved namespace will be used.

[Anchor to key](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafield.arguments.key)key•[String!](/docs/api/admin-graphql/latest/scalars/String)requiredThe key for the metafield.

[Anchor to metafields](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafields)metafields•[MetafieldConnection!](/docs/api/admin-graphql/latest/connections/MetafieldConnection)non-nullA list of [custom fields](https://shopify.dev/docs/apps/build/custom-data)

that a merchant associates with a Shopify resource.

Show fields### Arguments[Anchor to namespace](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafields.arguments.namespace)namespace•[String](/docs/api/admin-graphql/latest/scalars/String)The metafield namespace to filter by. If omitted, all metafields are returned.

[Anchor to keys](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafields.arguments.keys)keys•[[String!]](/docs/api/admin-graphql/latest/scalars/String)List of keys of metafields in the format `namespace.key`, will be returned in the same format.

[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafields.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafields.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafields.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafields.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafields.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to name](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.name)name•[String!](/docs/api/admin-graphql/latest/scalars/String)non-nullThe unique identifier for the order that appears on the order page in the Shopify admin and the **Order status** page.

For example, "#1001", "EN1001", or "1001-A".

This value isn't unique across multiple stores. Use this field to identify orders in the Shopify admin and for order tracking.

[Anchor to netPaymentSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.netPaymentSet)netPaymentSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe net payment for the order, based on the total amount received minus the total amount refunded, in shop and presentment currencies.

Show fields[Anchor to nonFulfillableLineItems](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.nonFulfillableLineItems)nonFulfillableLineItems•[LineItemConnection!](/docs/api/admin-graphql/latest/connections/LineItemConnection)non-nullA list of line items that can't be fulfilled.

For example, tips and fully refunded line items can't be fulfilled.

For a more granular view of the fulfillment status, refer to the [FulfillmentOrder](https://shopify.dev/api/admin-graphql/latest/objects/FulfillmentOrder) object.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.nonFulfillableLineItems.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.nonFulfillableLineItems.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.nonFulfillableLineItems.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.nonFulfillableLineItems.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.nonFulfillableLineItems.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to note](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.note)note•[String](/docs/api/admin-graphql/latest/scalars/String)The note associated with the order.

Contains additional information or instructions added by merchants or customers during the order process.

Commonly used for special delivery instructions, gift messages, or internal processing notes.

[Anchor to number](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.number)number•[Int!](/docs/api/admin-graphql/latest/scalars/Int)non-nullThe order number used to generate the name using the store's configured order number prefix/suffix. This number isn't guaranteed to follow a consecutive integer sequence (e.g. 1, 2, 3..), nor is it guaranteed to be unique across multiple stores, or even for a single store.

[Anchor to originalTotalAdditionalFeesSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.originalTotalAdditionalFeesSet)originalTotalAdditionalFeesSet•[MoneyBag](/docs/api/admin-graphql/latest/objects/MoneyBag)The total amount of all additional fees, such as import fees or taxes, that were applied when an order was created.

Returns `null` if additional fees aren't applicable.

Show fields[Anchor to originalTotalDutiesSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.originalTotalDutiesSet)originalTotalDutiesSet•[MoneyBag](/docs/api/admin-graphql/latest/objects/MoneyBag)The total amount of duties calculated when an order was created, before any modifications. Modifications include returns, refunds, order edits, and cancellations. Use [`currentTotalDutiesSet`](https://shopify.dev/docs/api/admin-graphql/latest/objects/order#field-Order.fields.currentTotalDutiesSet) to retrieve the current duties amount after adjustments.

Show fields[Anchor to originalTotalPriceSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.originalTotalPriceSet)originalTotalPriceSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe total price of the order at the time of order creation, in shop and presentment currencies.

Use this to compare the original order value against the current total after edits, returns, or refunds.

Show fields[Anchor to paymentCollectionDetails](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.paymentCollectionDetails)paymentCollectionDetails•[OrderPaymentCollectionDetails!](/docs/api/admin-graphql/latest/objects/OrderPaymentCollectionDetails)non-nullThe payment collection details for the order, including payment status, outstanding amounts, and collection information.

Use this to understand when and how payments should be collected, especially for orders with deferred or installment payment terms.

Show fields[Anchor to paymentGatewayNames](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.paymentGatewayNames)paymentGatewayNames•[[String!]!](/docs/api/admin-graphql/latest/scalars/String)non-nullA list of the names of all payment gateways used for the order.

For example, "Shopify Payments" and "Cash on Delivery (COD)".

[Anchor to paymentTerms](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.paymentTerms)paymentTerms•[PaymentTerms](/docs/api/admin-graphql/latest/objects/PaymentTerms)The payment terms associated with the order, such as net payment due dates or early payment discounts. Payment terms define when and how an order should be paid. Returns `null` if no specific payment terms were set for the order.

Show fields[Anchor to phone](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.phone)phone•[String](/docs/api/admin-graphql/latest/scalars/String)The phone number associated with the customer for this order.

Useful for contacting customers about shipping updates, delivery notifications, or order issues.

Returns `null` if no phone number was provided during checkout.

[Anchor to poNumber](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.poNumber)poNumber•[String](/docs/api/admin-graphql/latest/scalars/String)The purchase order (PO) number that's associated with an order.

This is typically provided by business customers who require a PO number for their procurement.

[Anchor to presentmentCurrencyCode](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.presentmentCurrencyCode)presentmentCurrencyCode•[CurrencyCode!](/docs/api/admin-graphql/latest/enums/CurrencyCode)non-nullThe currency used by the customer when placing the order. For example, "USD", "EUR", or "CAD".

This may differ from the shop's base currency when serving international customers or using multi-currency pricing.

Show enum values[Anchor to processedAt](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.processedAt)processedAt•[DateTime!](/docs/api/admin-graphql/latest/scalars/DateTime)non-nullThe date and time in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601) when the order was processed.

This date and time might not match the date and time when the order was created.

[Anchor to productNetwork](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.productNetwork)productNetwork•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the customer also purchased items from other stores in the network.

[Anchor to publication](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.publication)publication•[Publication](/docs/api/admin-graphql/latest/objects/Publication)The sales channel that the order was created from, such as the [Online Store](https://shopify.dev/docs/apps/build/app-surfaces#online-store) or [Shopify POS](https://shopify.dev/docs/apps/build/app-surfaces#point-of-sale).

Show fields[Anchor to purchasingEntity](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.purchasingEntity)purchasingEntity•[PurchasingEntity](/docs/api/admin-graphql/latest/unions/PurchasingEntity)The business entity that placed the order, including company details and purchasing relationships.

Used for B2B transactions to track which company or organization is responsible for the purchase and payment terms.

Show union types[Anchor to refundable](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.refundable)refundable•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the order can be refunded based on its payment transactions.

Returns `false` for orders with no eligible payment transactions, such as fully refunded orders or orders with non-refundable payment methods.

[Anchor to refundDiscrepancySet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.refundDiscrepancySet)refundDiscrepancySet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe difference between the suggested and actual refund amount of all refunds that have been applied to the order.

A positive value indicates a difference in the merchant's favor, and a negative value indicates a difference in the customer's favor.

Show fields[Anchor to refunds](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.refunds)refunds•[[Refund!]!](/docs/api/admin-graphql/latest/objects/Refund)non-nullA list of refunds that have been applied to the order.

Refunds represent money returned to customers for returned items, cancellations, or adjustments.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.refunds.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)Truncate the array result to this size.

[Anchor to registeredSourceUrl](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.registeredSourceUrl)registeredSourceUrl•[URL](/docs/api/admin-graphql/latest/scalars/URL)The URL of the source that the order originated from, if found in the domain registry. Returns `null` if the source URL isn't in the domain registry.

[Anchor to requiresShipping](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.requiresShipping)requiresShipping•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the order requires physical shipping to the customer.

Returns `false` for digital-only orders (such as gift cards or downloadable products) and `true` for orders with physical products that need delivery.

Use this to determine shipping workflows and logistics requirements.

[Anchor to restockable](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.restockable)restockable•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether any line items on the order can be restocked into inventory.

Returns `false` for digital products, custom items, or items that can't be resold.

[Anchor to retailLocation](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.retailLocation)retailLocation•[Location](/docs/api/admin-graphql/latest/objects/Location)The physical location where a retail order is created or completed, except for draft POS orders completed using the "mark as paid" flow in the Shopify admin, which return `null`. Transactions associated with the order might have been processed at a different location.

Show fields[Anchor to returns](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.returns)returns•[ReturnConnection!](/docs/api/admin-graphql/latest/connections/ReturnConnection)non-nullThe returns associated with the order.

Contains information about items that customers have requested to return, including return reasons, status, and refund details.

Use this to track and manage the return process for order items.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.returns.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.returns.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.returns.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.returns.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.returns.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to query](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.returns.arguments.query)query•[String](/docs/api/admin-graphql/latest/scalars/String)A filter made up of terms, connectives, modifiers, and comparators.

You can apply one or more filters to a query. Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-id)id•idFilter by `id` range.

Example:- `id:1234`- `id:>=1234`- `id:<=1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-status)status•string[Anchor to returnStatus](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.returnStatus)returnStatus•[OrderReturnStatus!](/docs/api/admin-graphql/latest/enums/OrderReturnStatus)non-nullThe order's aggregated return status for display purposes.

Indicates the overall state of returns for the order, helping merchants track and manage the return process.

Show enum values[Anchor to risk](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.risk)risk•[OrderRiskSummary!](/docs/api/admin-graphql/latest/objects/OrderRiskSummary)non-nullThe risk assessment summary for the order.

Provides fraud analysis and risk scoring to help you identify potentially fraudulent orders.

Use this to make informed decisions about order fulfillment and payment processing.

Show fields[Anchor to shippingAddress](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.shippingAddress)shippingAddress•[MailingAddress](/docs/api/admin-graphql/latest/objects/MailingAddress)The shipping address where the order will be delivered.

Contains the customer's delivery location for fulfillment and shipping label generation.

Returns `null` for digital orders or orders that don't require shipping.

Show fields[Anchor to shippingLine](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.shippingLine)shippingLine•[ShippingLine](/docs/api/admin-graphql/latest/objects/ShippingLine)A summary of all shipping costs on the order.

Aggregates shipping charges, discounts, and taxes to provide a single view of delivery costs.

Show fields[Anchor to shippingLines](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.shippingLines)shippingLines•[ShippingLineConnection!](/docs/api/admin-graphql/latest/connections/ShippingLineConnection)non-nullThe shipping methods applied to the order.

Each shipping line represents a shipping option chosen during checkout, including the carrier, service level, and cost.

Use this to understand shipping charges and delivery options for the order.

Show fields### Arguments[Anchor to includeRemovals](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.shippingLines.arguments.includeRemovals)includeRemovals•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseWhether results should contain removed shipping lines.

[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.shippingLines.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.shippingLines.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.shippingLines.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.shippingLines.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.shippingLines.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to shopifyProtect](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.shopifyProtect)shopifyProtect•[ShopifyProtectOrderSummary](/docs/api/admin-graphql/latest/objects/ShopifyProtectOrderSummary)The Shopify Protect details for the order, including fraud protection status and coverage information.

Shopify Protect helps protect eligible orders against fraudulent chargebacks.

Returns `null` if Shopify Protect is disabled for the shop or the order isn't eligible for protection.

Learn more about [Shopify Protect](https://www.shopify.com/protect).

Show fields[Anchor to sourceIdentifier](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.sourceIdentifier)sourceIdentifier•[String](/docs/api/admin-graphql/latest/scalars/String)A unique POS or third party order identifier.

For example, "1234-12-1000" or "111-98567-54". The [`receiptNumber`](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order#field-receiptNumber) field is derived from this value for POS orders.

[Anchor to sourceName](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.sourceName)sourceName•[String](/docs/api/admin-graphql/latest/scalars/String)The name of the source associated with the order, such as "web", "mobile_app", or "pos". Use this field to identify the platform where the order was placed.

[Anchor to staffMember](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.staffMember)staffMember•[StaffMember](/docs/api/admin-graphql/latest/objects/StaffMember)The staff member who created or is responsible for the order.

Useful for tracking which team member handled phone orders, manual orders, or order modifications.

Returns `null` for orders created directly by customers through the online store.

Show fields[Anchor to statusPageUrl](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.statusPageUrl)statusPageUrl•[URL!](/docs/api/admin-graphql/latest/scalars/URL)non-nullThe URL where customers can check their order's current status, including tracking information and delivery updates.

Provides order tracking links in emails, apps, or customer communications.

Show arguments### Arguments[Anchor to audience](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.statusPageUrl.arguments.audience)audience•[Audience](/docs/api/admin-graphql/latest/enums/Audience)Specifies the intended audience for the status page URL.

Show enum values[Anchor to notificationUsage](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.statusPageUrl.arguments.notificationUsage)notificationUsage•[NotificationUsage](/docs/api/admin-graphql/latest/enums/NotificationUsage)Specifies the intended notification usage for the status page URL.

Show enum values[Anchor to subtotalLineItemsQuantity](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.subtotalLineItemsQuantity)subtotalLineItemsQuantity•[Int!](/docs/api/admin-graphql/latest/scalars/Int)non-nullThe sum of quantities for all line items that contribute to the order's subtotal price.

This excludes quantities for items like tips, shipping costs, or gift cards that don't affect the subtotal.

Use this to quickly understand the total item count for pricing calculations.

[Anchor to subtotalPriceSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.subtotalPriceSet)subtotalPriceSet•[MoneyBag](/docs/api/admin-graphql/latest/objects/MoneyBag)The sum of the prices for all line items after discounts and before returns, in shop and presentment currencies.

If `taxesIncluded` is `true`, then the subtotal also includes tax.

Show fields[Anchor to suggestedRefund](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.suggestedRefund)suggestedRefund•[SuggestedRefund](/docs/api/admin-graphql/latest/objects/SuggestedRefund)A calculated refund suggestion for the order based on specified line items, shipping, and duties.

Use this to preview refund amounts, taxes, and processing fees before creating an actual refund.

Show fields### Arguments[Anchor to shippingAmount](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.suggestedRefund.arguments.shippingAmount)shippingAmount•[Money](/docs/api/admin-graphql/latest/scalars/Money)The amount to refund for shipping. Overrides the `refundShipping` argument.

[Anchor to refundShipping](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.suggestedRefund.arguments.refundShipping)refundShipping•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Whether to refund the full shipping amount.

[Anchor to refundLineItems](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.suggestedRefund.arguments.refundLineItems)refundLineItems•[[RefundLineItemInput!]](/docs/api/admin-graphql/latest/input-objects/RefundLineItemInput)The line items from the order to include in the refund.

Show input fields[Anchor to refundDuties](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.suggestedRefund.arguments.refundDuties)refundDuties•[[RefundDutyInput!]](/docs/api/admin-graphql/latest/input-objects/RefundDutyInput)The duties from the order to include in the refund.

Show input fields[Anchor to suggestFullRefund](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.suggestedRefund.arguments.suggestFullRefund)suggestFullRefund•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseWhether the suggested refund should be created from all refundable line items on the order.

If `true`, the `refundLineItems` argument will be ignored.

[Anchor to refundMethodAllocation](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.suggestedRefund.arguments.refundMethodAllocation)refundMethodAllocation•[RefundMethodAllocation](/docs/api/admin-graphql/latest/enums/RefundMethodAllocation)Default:ORIGINAL_PAYMENT_METHODSSpecifies which refund methods to allocate the suggested refund amount to.

Show enum values[Anchor to tags](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.tags)tags•[[String!]!](/docs/api/admin-graphql/latest/scalars/String)non-nullA comma separated list of tags associated with the order. Updating `tags` overwrites

any existing tags that were previously added to the order. To add new tags without overwriting

existing tags, use the [tagsAdd](https://shopify.dev/api/admin-graphql/latest/mutations/tagsadd)

mutation.

[Anchor to taxesIncluded](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.taxesIncluded)taxesIncluded•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether taxes are included in the subtotal price of the order.

When `true`, the subtotal and line item prices include tax amounts. When `false`, taxes are calculated and displayed separately.

[Anchor to taxExempt](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.taxExempt)taxExempt•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether taxes are exempt on the order.

Returns `true` for orders where the customer or business has a valid tax exemption, such as non-profit organizations or tax-free purchases.

Use this to understand if tax calculations were skipped during checkout.

[Anchor to taxLines](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.taxLines)taxLines•[[TaxLine!]!](/docs/api/admin-graphql/latest/objects/TaxLine)non-nullA list of all tax lines applied to line items on the order, before returns.

Tax line prices represent the total price for all tax lines with the same `rate` and `title`.

Show fields[Anchor to test](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.test)test•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the order is a test.

Test orders are made using the Shopify Bogus Gateway or a payment provider with test mode enabled.

A test order can't be converted into a real order and vice versa.

[Anchor to totalCapturableSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalCapturableSet)totalCapturableSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe authorized amount that's uncaptured or undercaptured, in shop and presentment currencies.

This amount isn't adjusted for returns.

Show fields[Anchor to totalCashRoundingAdjustment](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalCashRoundingAdjustment)totalCashRoundingAdjustment•[CashRoundingAdjustment!](/docs/api/admin-graphql/latest/objects/CashRoundingAdjustment)non-nullThe total rounding adjustment applied to payments or refunds for an order involving cash payments. Applies to some countries where cash transactions are rounded to the nearest currency denomination.

Show fields[Anchor to totalDiscountsSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalDiscountsSet)totalDiscountsSet•[MoneyBag](/docs/api/admin-graphql/latest/objects/MoneyBag)The total amount discounted on the order before returns, in shop and presentment currencies.

This includes both order and line level discounts.

Show fields[Anchor to totalOutstandingSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalOutstandingSet)totalOutstandingSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe total amount not yet transacted for the order, in shop and presentment currencies.

A positive value indicates a difference in the merchant's favor (payment from customer to merchant) and a negative value indicates a difference in the customer's favor (refund from merchant to customer).

Show fields[Anchor to totalPriceSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalPriceSet)totalPriceSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe total price of the order, before returns, in shop and presentment currencies.

This includes taxes and discounts.

Show fields[Anchor to totalReceivedSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalReceivedSet)totalReceivedSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe total amount received from the customer before returns, in shop and presentment currencies.

Show fields[Anchor to totalRefundedSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalRefundedSet)totalRefundedSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe total amount that was refunded, in shop and presentment currencies.

Show fields[Anchor to totalRefundedShippingSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalRefundedShippingSet)totalRefundedShippingSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe total amount of shipping that was refunded, in shop and presentment currencies.

Show fields[Anchor to totalShippingPriceSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalShippingPriceSet)totalShippingPriceSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe total shipping costs returned to the customer, in shop and presentment currencies. This includes fees and any related discounts that were refunded.

Show fields[Anchor to totalTaxSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalTaxSet)totalTaxSet•[MoneyBag](/docs/api/admin-graphql/latest/objects/MoneyBag)The total tax amount before returns, in shop and presentment currencies.

Show fields[Anchor to totalTipReceivedSet](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalTipReceivedSet)totalTipReceivedSet•[MoneyBag!](/docs/api/admin-graphql/latest/objects/MoneyBag)non-nullThe sum of all tip amounts for the order, in shop and presentment currencies.

Show fields[Anchor to totalWeight](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalWeight)totalWeight•[UnsignedInt64](/docs/api/admin-graphql/latest/scalars/UnsignedInt64)The total weight of the order before returns, in grams.

[Anchor to transactions](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.transactions)transactions•[[OrderTransaction!]!](/docs/api/admin-graphql/latest/objects/OrderTransaction)non-nullA list of transactions associated with the order.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.transactions.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)Truncate the array result to this size.

[Anchor to capturable](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.transactions.arguments.capturable)capturable•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Filter transactions by whether they are capturable.

[Anchor to manuallyResolvable](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.transactions.arguments.manuallyResolvable)manuallyResolvable•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Filter transactions by whether they can be resolved manually.

For example, fully captured or voided transactions aren't manually resolvable.

[Anchor to transactionsCount](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.transactionsCount)transactionsCount•[Count](/docs/api/admin-graphql/latest/objects/Count)The number of transactions associated with the order.

Show fields[Anchor to unpaid](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.unpaid)unpaid•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether no payments have been made for the order.

[Anchor to updatedAt](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.updatedAt)updatedAt•[DateTime!](/docs/api/admin-graphql/latest/scalars/DateTime)non-nullThe date and time in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601) when the order was last modified.

### Deprecated fields- cartDiscountAmount (Money): deprecated- channel (Channel): deprecated- customerJourney (CustomerJourney): deprecated- landingPageDisplayText (String): deprecated- landingPageUrl (URL): deprecated- localizationExtensions (LocalizationExtensionConnection!): deprecated- metafieldDefinitions (MetafieldDefinitionConnection!): deprecated- netPayment (Money!): deprecated- physicalLocation (Location): deprecated- referralCode (String): deprecated- referrerDisplayText (String): deprecated- referrerUrl (URL): deprecated- riskLevel (OrderRiskLevel!): deprecated- risks ([OrderRisk!]!): deprecated- subtotalPrice (Money): deprecated- totalCapturable (Money!): deprecated- totalDiscounts (Money): deprecated- totalPrice (Money!): deprecated- totalReceived (Money!): deprecated- totalRefunded (Money!): deprecated- totalShippingPrice (Money!): deprecated- totalTax (Money): deprecated- totalTipReceived (MoneyV2!): deprecated[Anchor to cartDiscountAmount](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.cartDiscountAmount)cartDiscountAmount•[Money](/docs/api/admin-graphql/latest/scalars/Money)Deprecated[Anchor to channel](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.channel)channel•[Channel](/docs/api/admin-graphql/latest/objects/Channel)DeprecatedShow fields[Anchor to customerJourney](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.customerJourney)customerJourney•[CustomerJourney](/docs/api/admin-graphql/latest/objects/CustomerJourney)DeprecatedShow fields[Anchor to landingPageDisplayText](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.landingPageDisplayText)landingPageDisplayText•[String](/docs/api/admin-graphql/latest/scalars/String)Deprecated[Anchor to landingPageUrl](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.landingPageUrl)landingPageUrl•[URL](/docs/api/admin-graphql/latest/scalars/URL)Deprecated[Anchor to localizationExtensions](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizationExtensions)localizationExtensions•[LocalizationExtensionConnection!](/docs/api/admin-graphql/latest/connections/LocalizationExtensionConnection)non-nullDeprecatedShow fields### Arguments[Anchor to countryCodes](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizationExtensions.arguments.countryCodes)countryCodes•[[CountryCode!]](/docs/api/admin-graphql/latest/enums/CountryCode)The country codes of the extensions.

Show enum values[Anchor to purposes](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizationExtensions.arguments.purposes)purposes•[[LocalizationExtensionPurpose!]](/docs/api/admin-graphql/latest/enums/LocalizationExtensionPurpose)The purpose of the extensions.

Show enum values[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizationExtensions.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizationExtensions.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizationExtensions.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizationExtensions.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.localizationExtensions.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to metafieldDefinitions](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafieldDefinitions)metafieldDefinitions•[MetafieldDefinitionConnection!](/docs/api/admin-graphql/latest/connections/MetafieldDefinitionConnection)non-nullDeprecatedShow fields### Arguments[Anchor to namespace](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafieldDefinitions.arguments.namespace)namespace•[String](/docs/api/admin-graphql/latest/scalars/String)Filter metafield definitions by namespace.

[Anchor to pinnedStatus](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafieldDefinitions.arguments.pinnedStatus)pinnedStatus•[MetafieldDefinitionPinnedStatus](/docs/api/admin-graphql/latest/enums/MetafieldDefinitionPinnedStatus)Default:ANYFilter by the definition's pinned status.

Show enum values[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafieldDefinitions.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafieldDefinitions.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafieldDefinitions.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafieldDefinitions.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafieldDefinitions.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafieldDefinitions.arguments.sortKey)sortKey•[MetafieldDefinitionSortKeys](/docs/api/admin-graphql/latest/enums/MetafieldDefinitionSortKeys)Default:IDSort the underlying list using a key. If your query is slow or returns an error, then [try specifying a sort key that matches the field used in the search](https://shopify.dev/api/usage/pagination-graphql#search-performance-considerations).

Show enum values[Anchor to query](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.metafieldDefinitions.arguments.query)query•[String](/docs/api/admin-graphql/latest/scalars/String)A filter made up of terms, connectives, modifiers, and comparators.

You can apply one or more filters to a query. Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-default)default•stringFilter by a case-insensitive search of multiple fields in a document.

Example:- `query=Bob Norman`- `query=title:green hoodie`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-created_at)created_at•timeFilter by the date and time when the metafield definition was created.

Example:- `created_at:>2020-10-21T23:39:20Z`- `created_at:<now`- `created_at:<=2024`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-id)id•idFilter by `id` range.

Example:- `id:1234`- `id:>=1234`- `id:<=1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-key)key•stringFilter by the metafield definition [`key`](https://shopify.dev/docs/api/admin-graphql/latest/objects/MetafieldDefinition#field-key) field.

Example:- `key:some-key`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-namespace)namespace•stringFilter by the metafield definition [`namespace`](https://shopify.dev/docs/api/admin-graphql/latest/objects/MetafieldDefinition#field-namespace) field.

Example:- `namespace:some-namespace`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-owner_type)owner_type•stringFilter by the metafield definition [`ownerType`](https://shopify.dev/docs/api/admin-graphql/latest/objects/MetafieldDefinition#field-ownertype) field.

Example:- `owner_type:PRODUCT`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-type)type•stringFilter by the metafield definition [`type`](https://shopify.dev/docs/api/admin-graphql/latest/objects/MetafieldDefinition#field-type) field.

Example:- `type:single_line_text_field`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-updated_at)updated_at•timeFilter by the date and time when the metafield definition was last updated.

Example:- `updated_at:>2020-10-21T23:39:20Z`- `updated_at:<now`- `updated_at:<=2024`[Anchor to netPayment](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.netPayment)netPayment•[Money!](/docs/api/admin-graphql/latest/scalars/Money)non-nullDeprecated[Anchor to physicalLocation](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.physicalLocation)physicalLocation•[Location](/docs/api/admin-graphql/latest/objects/Location)DeprecatedShow fields[Anchor to referralCode](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.referralCode)referralCode•[String](/docs/api/admin-graphql/latest/scalars/String)Deprecated[Anchor to referrerDisplayText](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.referrerDisplayText)referrerDisplayText•[String](/docs/api/admin-graphql/latest/scalars/String)Deprecated[Anchor to referrerUrl](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.referrerUrl)referrerUrl•[URL](/docs/api/admin-graphql/latest/scalars/URL)Deprecated[Anchor to riskLevel](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.riskLevel)riskLevel•[OrderRiskLevel!](/docs/api/admin-graphql/latest/enums/OrderRiskLevel)non-nullDeprecatedShow enum values[Anchor to risks](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.risks)risks•[[OrderRisk!]!](/docs/api/admin-graphql/latest/objects/OrderRisk)non-nullDeprecatedShow fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.risks.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)Truncate the array result to this size.

[Anchor to subtotalPrice](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.subtotalPrice)subtotalPrice•[Money](/docs/api/admin-graphql/latest/scalars/Money)Deprecated[Anchor to totalCapturable](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalCapturable)totalCapturable•[Money!](/docs/api/admin-graphql/latest/scalars/Money)non-nullDeprecated[Anchor to totalDiscounts](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalDiscounts)totalDiscounts•[Money](/docs/api/admin-graphql/latest/scalars/Money)Deprecated[Anchor to totalPrice](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalPrice)totalPrice•[Money!](/docs/api/admin-graphql/latest/scalars/Money)non-nullDeprecated[Anchor to totalReceived](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalReceived)totalReceived•[Money!](/docs/api/admin-graphql/latest/scalars/Money)non-nullDeprecated[Anchor to totalRefunded](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalRefunded)totalRefunded•[Money!](/docs/api/admin-graphql/latest/scalars/Money)non-nullDeprecated[Anchor to totalShippingPrice](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalShippingPrice)totalShippingPrice•[Money!](/docs/api/admin-graphql/latest/scalars/Money)non-nullDeprecated[Anchor to totalTax](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalTax)totalTax•[Money](/docs/api/admin-graphql/latest/scalars/Money)Deprecated[Anchor to totalTipReceived](/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.totalTipReceived)totalTipReceived•[MoneyV2!](/docs/api/admin-graphql/latest/objects/MoneyV2)non-nullDeprecatedShow fieldsWas this section helpful?YesNo## Map### Fields and connections with this object- {}[CalculatedOrder.originalOrder](/docs/api/admin-graphql/latest/objects/CalculatedOrder#field-CalculatedOrder.fields.originalOrder)- {}[Company.orders](/docs/api/admin-graphql/latest/objects/Company#field-Company.fields.orders)- {}[CompanyContact.orders](/docs/api/admin-graphql/latest/objects/CompanyContact#field-CompanyContact.fields.orders)- {}[CompanyLocation.orders](/docs/api/admin-graphql/latest/objects/CompanyLocation#field-CompanyLocation.fields.orders)- {}[Customer.lastOrder](/docs/api/admin-graphql/latest/objects/Customer#field-Customer.fields.lastOrder)- {}[Customer.orders](/docs/api/admin-graphql/latest/objects/Customer#field-Customer.fields.orders)- {}[CustomerMergePreviewDefaultFields.orders](/docs/api/admin-graphql/latest/objects/CustomerMergePreviewDefaultFields#field-CustomerMergePreviewDefaultFields.fields.orders)- {}[DraftOrder.order](/docs/api/admin-graphql/latest/objects/DraftOrder#field-DraftOrder.fields.order)- {}[Fulfillment.order](/docs/api/admin-graphql/latest/objects/Fulfillment#field-Fulfillment.fields.order)- {}[FulfillmentOrder.order](/docs/api/admin-graphql/latest/objects/FulfillmentOrder#field-FulfillmentOrder.fields.order)- {}[GiftCard.order](/docs/api/admin-graphql/latest/objects/GiftCard#field-GiftCard.fields.order)- {}[OrderAgreement.order](/docs/api/admin-graphql/latest/objects/OrderAgreement#field-OrderAgreement.fields.order)- <->[OrderConnection.nodes](/docs/api/admin-graphql/latest/connections/OrderConnection#returns-nodes)- {}[OrderEdge.node](/docs/api/admin-graphql/latest/objects/OrderEdge#field-OrderEdge.fields.node)- {}[OrderTransaction.order](/docs/api/admin-graphql/latest/objects/OrderTransaction#field-OrderTransaction.fields.order)- {}[PaymentTerms.order](/docs/api/admin-graphql/latest/objects/PaymentTerms#field-PaymentTerms.fields.order)- {}[Refund.order](/docs/api/admin-graphql/latest/objects/Refund#field-Refund.fields.order)- {}[Return.order](/docs/api/admin-graphql/latest/objects/Return#field-Return.fields.order)- {}[ReverseFulfillmentOrder.order](/docs/api/admin-graphql/latest/objects/ReverseFulfillmentOrder#field-ReverseFulfillmentOrder.fields.order)- {}[ShopPayPaymentRequestReceipt.order](/docs/api/admin-graphql/latest/objects/ShopPayPaymentRequestReceipt#field-ShopPayPaymentRequestReceipt.fields.order)- {}[ShopifyPaymentsDispute.order](/docs/api/admin-graphql/latest/objects/ShopifyPaymentsDispute#field-ShopifyPaymentsDispute.fields.order)- {}[SubscriptionBillingCycleEditedContract.orders](/docs/api/admin-graphql/latest/objects/SubscriptionBillingCycleEditedContract#field-SubscriptionBillingCycleEditedContract.fields.orders)- {}[SubscriptionContract.orders](/docs/api/admin-graphql/latest/objects/SubscriptionContract#field-SubscriptionContract.fields.orders)- {}[SubscriptionContract.originOrder](/docs/api/admin-graphql/latest/objects/SubscriptionContract#field-SubscriptionContract.fields.originOrder)- ||-[SubscriptionContractBase.orders](/docs/api/admin-graphql/latest/interfaces/SubscriptionContractBase#fields-orders)- {}[TenderTransaction.order](/docs/api/admin-graphql/latest/objects/TenderTransaction#field-TenderTransaction.fields.order)Show deprecations### Possible type in- [CommentEventEmbed](/docs/api/admin-graphql/latest/unions/CommentEventEmbed)- [MetafieldReference](/docs/api/admin-graphql/latest/unions/MetafieldReference)- [MetafieldReferencer](/docs/api/admin-graphql/latest/unions/MetafieldReferencer)## [Anchor to Queries](/docs/api/admin-graphql/latest/objects/Order#queries)Queries- order (Order)- orderByIdentifier (Order)- orders (OrderConnection!)[Anchor to order](/docs/api/admin-graphql/latest/objects/Order#query-order)[order](/docs/api/admin-graphql/latest/queries/order)•queryThe `order` query retrieves an [order](https://shopify.dev/docs/api/admin-graphql/latest/objects/order) by its ID. This query provides access to comprehensive order information such as customer details, line items, financial data, and fulfillment status.

Use the `order` query to retrieve information associated with the following processes:

- [Order management and fulfillment](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps)

- [Financial reporting](https://help.shopify.com/manual/finance)

- [Customer purchase history](https://help.shopify.com/manual/reports-and-analytics/shopify-reports/report-types/default-reports/customers-reports) and [transaction analysis](https://shopify.dev/docs/apps/launch/billing/view-charges-earnings#transaction-data-through-the-graphql-admin-api)

- [Shipping](https://shopify.dev/docs/apps/build/checkout/delivery-shipping) and [inventory management](https://shopify.dev/docs/apps/build/orders-fulfillment/inventory-management-apps)

You can only retrieve the last 60 days worth of orders from a store by default. If you want to access older orders, then you need to [request access to all orders](https://shopify.dev/docs/api/usage/access-scopes#orders-permissions).

For large order datasets, consider using [bulk operations](https://shopify.dev/docs/api/usage/bulk-operations/queries).

Bulk operations handle pagination automatically and allow you to retrieve data asynchronously without being constrained by API rate limits.

Learn more about [creating orders](https://shopify.dev/docs/api/admin-graphql/latest/mutations/ordercreate) and [building order management apps](https://shopify.dev/docs/apps/build/orders-fulfillment).

Show fields### Arguments[Anchor to id](/docs/api/admin-graphql/latest/objects/Order#query-order.arguments.id)id•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the `Order` to return.

[Anchor to orderByIdentifier](/docs/api/admin-graphql/latest/objects/Order#query-orderByIdentifier)[orderByIdentifier](/docs/api/admin-graphql/latest/queries/orderByIdentifier)•queryReturn an order by an identifier.

Show fields### Arguments[Anchor to identifier](/docs/api/admin-graphql/latest/objects/Order#query-orderByIdentifier.arguments.identifier)identifier•[OrderIdentifierInput!](/docs/api/admin-graphql/latest/input-objects/OrderIdentifierInput)requiredThe identifier of the order.

Show input fields[Anchor to orders](/docs/api/admin-graphql/latest/objects/Order#query-orders)[orders](/docs/api/admin-graphql/latest/queries/orders)•queryReturns a list of [orders](https://shopify.dev/api/admin-graphql/latest/objects/Order) placed in the store, including data such as order status, customer, and line item details.

Use the `orders` query to build reports, analyze sales performance, or automate fulfillment workflows. The `orders` query supports [pagination](https://shopify.dev/docs/api/usage/pagination-graphql),

[sorting](https://shopify.dev/docs/api/admin-graphql/latest/queries/orders#arguments-sortKey), and [filtering](https://shopify.dev/docs/api/admin-graphql/latest/queries/orders#arguments-query).

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Order#query-orders.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Order#query-orders.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Order#query-orders.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Order#query-orders.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Order#query-orders.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/admin-graphql/latest/objects/Order#query-orders.arguments.sortKey)sortKey•[OrderSortKeys](/docs/api/admin-graphql/latest/enums/OrderSortKeys)Default:PROCESSED_ATSort the underlying list using a key. If your query is slow or returns an error, then [try specifying a sort key that matches the field used in the search](https://shopify.dev/api/usage/pagination-graphql#search-performance-considerations).

Show enum values[Anchor to query](/docs/api/admin-graphql/latest/objects/Order#query-orders.arguments.query)query•[String](/docs/api/admin-graphql/latest/scalars/String)A filter made up of terms, connectives, modifiers, and comparators.

You can apply one or more filters to a query. Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-default)default•stringFilter by a case-insensitive search of multiple fields in a document.

Example:- `query=Bob Norman`- `query=title:green hoodie`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-cart_token)cart_token•stringFilter by the cart token's unique value to track abandoned cart conversions or troubleshoot checkout issues. The token references the cart that's associated with an order.

Example:- `cart_token:abc123`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-channel)channel•stringFilter by the channel information [`handle`](https://shopify.dev/api/admin-graphql/latest/objects/ChannelInformation#field-ChannelInformation.fields.channelDefinition.handle) (`ChannelInformation.channelDefinition.handle`) field.

Example:- `channel:web`- `channel:web,pos`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-channel_id)channel_id•idFilter by the channel [`id`](https://shopify.dev/api/admin-graphql/latest/objects/Channel#field-Channel.fields.id) field.

Example:- `channel_id:123`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-chargeback_status)chargeback_status•stringFilter by the order's chargeback status. A chargeback occurs when a customer questions the legitimacy of a charge with their financial institution.

Valid values:- `accepted` - `charge_refunded` - `lost` - `needs_response` - `under_review` - `won` Example:- `chargeback_status:accepted`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-checkout_token)checkout_token•stringFilter by the checkout token's unique value to analyze conversion funnels or resolve payment issues. The checkout token's value references the checkout that's associated with an order.

Example:- `checkout_token:abc123`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-confirmation_number)confirmation_number•stringFilter by the randomly generated alpha-numeric identifier for an order that can be displayed to the customer instead of the sequential order name. This value isn't guaranteed to be unique.

Example:- `confirmation_number:ABC123`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-created_at)created_at•timeFilter by the date and time when the order was created in Shopify's system.

Example:- `created_at:2020-10-21T23:39:20Z`- `created_at:<now`- `created_at:<=2024`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-credit_card_last4)credit_card_last4•stringFilter by the last four digits of the payment card that was used to pay for the order. This filter matches only the last four digits of the card for heightened security.

Example:- `credit_card_last4:1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-current_total_price)current_total_price•floatFilter by the current total price of the order in the shop currency, including any returns/refunds/removals. This filter supports both exact values and ranges.

Example:- `current_total_price:10`- `current_total_price:>=5.00 current_total_price:<=20.99`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-customer_id)customer_id•idFilter orders by the customer [`id`](https://shopify.dev/api/admin-graphql/latest/objects/Customer#field-Customer.fields.id) field.

Example:- `customer_id:123`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-delivery_method)delivery_method•stringFilter by the delivery [`methodType`](https://shopify.dev/api/admin-graphql/2024-07/objects/DeliveryMethod#field-DeliveryMethod.fields.methodType) field.

Valid values:- `shipping` - `pick-up` - `retail` - `local` - `pickup-point` - `none` Example:- `delivery_method:shipping`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-discount_code)discount_code•stringFilter by the case-insensitive discount code that was applied to the order at checkout. Limited to the first discount code used on an order. Maximum characters: 255.

Example:- `discount_code:ABC123`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-email)email•stringFilter by the email address that's associated with the order to provide customer support or analyze purchasing patterns.

Example:- `email:example@shopify.com`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-financial_status)financial_status•stringFilter by the order [`displayFinancialStatus`](https://shopify.dev/api/admin-graphql/latest/objects/Order#field-Order.fields.displayFinancialStatus) field.

Valid values:- `paid` - `pending` - `authorized` - `partially_paid` - `partially_refunded` - `refunded` - `voided` - `expired` Example:- `financial_status:authorized`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-fraud_protection_level)fraud_protection_level•stringFilter by the level of fraud protection that's applied to the order. Use this filter to manage risk or handle disputes.

Valid values:- `fully_protected` - `partially_protected` - `not_protected` - `pending` - `not_eligible` - `not_available` Example:- `fraud_protection_level:fully_protected`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-fulfillment_location_id)fulfillment_location_id•idFilter by the fulfillment location [`id`](https://shopify.dev/api/admin-graphql/latest/objects/Fulfillment#field-Fulfillment.fields.location.id) (`Fulfillment.location.id`) field.

Example:- `fulfillment_location_id:123`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-fulfillment_status)fulfillment_status•stringFilter by the [`displayFulfillmentStatus`](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.displayFulfillmentStatus) field to prioritize shipments or monitor order processing.

Valid values:- `unshipped` - `shipped` - `fulfilled` - `partial` - `scheduled` - `on_hold` - `unfulfilled` - `request_declined` Example:- `fulfillment_status:fulfilled`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-gateway)gateway•stringFilter by the [`paymentGatewayNames`](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.paymentGatewayNames) field. Use this filter to find orders that were processed through specific payment providers like Shopify Payments, PayPal, or other custom payment gateways.

Example:- `gateway:shopify_payments`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-id)id•idFilter by `id` range.

Example:- `id:1234`- `id:>=1234`- `id:<=1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-location_id)location_id•idFilter by the location [`id`](https://shopify.dev/docs/api/admin-graphql/latest/objects/Location#field-Location.fields.id) that's associated with the order to view and manage orders for specific locations. For POS orders, locations must be defined in the Shopify admin under **Settings** > **Locations**. If no ID is provided, then the primary location of the shop is returned.

Example:- `location_id:123`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-metafields.{namespace}.{key})metafields.{namespace}.{key}•mixedFilters resources by metafield value. Format: `metafields.{namespace}.{key}:{value}`. Learn more about [querying by metafield value](https://shopify.dev/apps/build/custom-data/metafields/query-by-metafield-value).

Example:- `metafields.custom.on_sale:true`- `metafields.product.material:"gid://shopify/Metaobject/43458085"`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-name)name•stringFilter by the order [`name`](https://shopify.dev/api/admin-graphql/latest/objects/Order#field-name) field.

Example:- `name:1001-A`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-payment_id)payment_id•stringFilter by the payment ID that's associated with the order to reconcile financial records or troubleshoot payment issues.

Example:- `payment_id:abc123`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-payment_provider_id)payment_provider_id•idFilter by the ID of the payment provider that's associated with the order to manage payment methods or troubleshoot transactions.

Example:- `payment_provider_id:123`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-po_number)po_number•stringFilter by the order [`poNumber`](https://shopify.dev/api/admin-graphql/latest/objects/order#field-Order.fields.poNumber) field.

Example:- `po_number:P01001`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-processed_at)processed_at•timeFilter by the order [`processedAt`](https://shopify.dev/api/admin-graphql/latest/objects/order#field-Order.fields.processedAt) field.

Example:- `processed_at:2021-01-01T00:00:00Z`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-reference_location_id)reference_location_id•idFilter by the ID of a location that's associated with the order, such as locations from fulfillments, refunds, or the shop's primary location.

Example:- `reference_location_id:123`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-return_status)return_status•stringFilter by the order's [`returnStatus`](https://shopify.dev/api/admin-graphql/latest/objects/Order#field-Order.fields.returnStatus) to monitor returns processing and track which orders have active returns.

Valid values:- `return_requested` - `in_progress` - `inspection_complete` - `returned` - `return_failed` - `no_return` Example:- `return_status:in_progress`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-risk_level)risk_level•stringFilter by the order risk assessment [`riskLevel`](https://shopify.dev/api/admin-graphql/latest/objects/OrderRiskAssessment#field-OrderRiskAssessment.fields.riskLevel) field.

Valid values:- `high` - `medium` - `low` - `none` - `pending` Example:- `risk_level:high`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-sales_channel)sales_channel•stringFilter by the [sales channel](https://shopify.dev/docs/apps/build/sales-channels) where the order was made to analyze performance or manage fulfillment processes.

Example:- `sales_channel: some_sales_channel`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-sku)sku•stringFilter by the product variant [`sku`](https://shopify.dev/api/admin-graphql/latest/objects/ProductVariant#field-ProductVariant.fields.sku) field. [Learn more about SKUs](https://help.shopify.com/manual/products/details/sku).

Example:- `sku:ABC123`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-source_identifier)source_identifier•stringFilter by the ID of the order placed on the originating platform, such as a unique POS or third-party identifier. This value doesn't correspond to the Shopify ID that's generated from a completed draft order.

Example:- `source_identifier:1234-12-1000`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-source_name)source_name•stringFilter by the platform where the order was placed to distinguish between web orders, POS sales, draft orders, or third-party channels. Use this filter to analyze sales performance across different ordering methods.

Example:- `source_name:web`- `source_name:shopify_draft_order`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-status)status•stringFilter by the order's status to manage workflows or analyze the order lifecycle.

Valid values:- `open` - `closed` - `cancelled` - `not_closed` Example:- `status:open`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-subtotal_line_items_quantity)subtotal_line_items_quantity•stringFilter by the total number of items across all line items in an order. This filter supports both exact values and ranges, and is useful for identifying bulk orders or analyzing purchase volume patterns.

Example:- `subtotal_line_items_quantity:10`- `subtotal_line_items_quantity:5..20`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-tag)tag•stringFilter objects by the `tag` field.

Example:- `tag:my_tag`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-tag_not)tag_not•stringFilter by objects that don’t have the specified tag.

Example:- `tag_not:my_tag`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-test)test•booleanFilter by test orders. Test orders are made using the [Shopify Bogus Gateway](https://help.shopify.com/manual/checkout-settings/test-orders/payments-test-mode#bogus-gateway) or a payment provider with test mode enabled.

Example:- `test:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-total_weight)total_weight•stringFilter by the order weight. This filter supports both exact values and ranges, and is to be used to filter orders by the total weight of all items (excluding packaging). It takes a unit of measurement as a suffix. It accepts the following units: g, kg, lb, oz.

Example:- `total_weight:10.5kg`- `total_weight:>=5g total_weight:<=20g`- `total_weight:.5 lb`[Anchor to ](/docs/api/admin-graphql/latest/objects/Order#argument-query-filter-updated_at)updated_at•timeFilter by the date and time when the order was last updated in Shopify's system.

Example:- `updated_at:2020-10-21T23:39:20Z`- `updated_at:<now`- `updated_at:<=2024`[Anchor to savedSearchId](/docs/api/admin-graphql/latest/objects/Order#query-orders.arguments.savedSearchId)savedSearchId•[ID](/docs/api/admin-graphql/latest/scalars/ID)The ID of a [saved search](https://shopify.dev/api/admin-graphql/latest/objects/savedsearch#field-id).

The search’s query string is used as the query argument.

Was this section helpful?YesNo## <?>Order Queries### Queried by- <?>[order](/docs/api/admin-graphql/latest/queries/order)- <?>[orderByIdentifier](/docs/api/admin-graphql/latest/queries/orderByIdentifier)- <?>[orders](/docs/api/admin-graphql/latest/queries/orders)## [Anchor to Mutations](/docs/api/admin-graphql/latest/objects/Order#mutations)Mutations- orderClose (OrderClosePayload)- orderCreate (OrderCreatePayload)- orderCreateManualPayment (OrderCreateManualPaymentPayload)- orderCustomerRemove (OrderCustomerRemovePayload)- orderCustomerSet (OrderCustomerSetPayload)- orderEditCommit (OrderEditCommitPayload)- orderInvoiceSend (OrderInvoiceSendPayload)- orderMarkAsPaid (OrderMarkAsPaidPayload)- orderOpen (OrderOpenPayload)- orderUpdate (OrderUpdatePayload)- refundCreate (RefundCreatePayload)- taxSummaryCreate (TaxSummaryCreatePayload)[Anchor to orderClose](/docs/api/admin-graphql/latest/objects/Order#mutation-orderClose)[orderClose](/docs/api/admin-graphql/latest/mutations/orderClose)•mutationMarks an open [`Order`](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order) as closed. A closed order is one where merchants fulfill or cancel all [`LineItem`](https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem) objects and complete all financial transactions.

Once closed, the order indicates that no further work is required. The order's [`closedAt`](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order#field-closedAt) timestamp is set when this mutation completes successfully.

Show payload### Arguments[Anchor to input](/docs/api/admin-graphql/latest/objects/Order#mutation-orderClose.arguments.input)input•[OrderCloseInput!](/docs/api/admin-graphql/latest/input-objects/OrderCloseInput)requiredThe input for the mutation.

Show input fields[Anchor to orderCreate](/docs/api/admin-graphql/latest/objects/Order#mutation-orderCreate)[orderCreate](/docs/api/admin-graphql/latest/mutations/orderCreate)•mutationCreates an order with attributes such as customer information, line items, and shipping and billing addresses.

Use the `orderCreate` mutation to programmatically generate orders in scenarios where

orders aren't created through the standard checkout process, such as when importing orders from an external

system or creating orders for wholesale customers.

The `orderCreate` mutation doesn't support applying multiple discounts, such as discounts on line items.

Automatic discounts won't be applied unless you replicate the logic of those discounts in your custom

implementation. You can [apply a discount code](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/OrderCreateDiscountCodeInput),

but only one discount code can be set for each order.

NoteIf you're using the `orderCreate` mutation with a

[trial](https://help.shopify.com/manual/intro-to-shopify/pricing-plans/free-trial) or

[development store](https://shopify.dev/docs/api/development-stores), then you can create a

maximum of five new orders per minute.**Note:** If you're using the `orderCreate` mutation with a

[trial](https://help.shopify.com/manual/intro-to-shopify/pricing-plans/free-trial) or

[development store](https://shopify.dev/docs/api/development-stores), then you can create a

maximum of five new orders per minute.**Note:** If you&#39;re using the <code><span class="PreventFireFoxApplyingGapToWBR">order<wbr/>Create</span></code> mutation with a

<a href="https://help.shopify.com/manual/intro-to-shopify/pricing-plans/free-trial">trial</a> or

<a href="https://shopify.dev/docs/api/development-stores">development store</a>, then you can create a

maximum of five new orders per minute.After you create an order, you can make subsequent edits to the order using one of the following mutations:

- [`orderUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderUpdate):

Used for simple updates to an order, such as changing the order's note, tags, or customer information.

- [`orderEditBegin`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderEditBegin):

Used when you need to make significant updates to an order, such as adding or removing line items, changing

quantities, or modifying discounts. The `orderEditBegin` mutation initiates an order editing session,

allowing you to make multiple changes before finalizing them. Learn more about using the `orderEditBegin`

mutation to [edit existing orders](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps/edit-orders).

Learn how to build apps that integrate with

[order management and fulfillment processes](https://shopify.dev/docs/apps/build/orders-fulfillment).

Show payload### Arguments[Anchor to order](/docs/api/admin-graphql/latest/objects/Order#mutation-orderCreate.arguments.order)order•[OrderCreateOrderInput!](/docs/api/admin-graphql/latest/input-objects/OrderCreateOrderInput)requiredThe attributes of the new order.

Show input fields[Anchor to options](/docs/api/admin-graphql/latest/objects/Order#mutation-orderCreate.arguments.options)options•[OrderCreateOptionsInput](/docs/api/admin-graphql/latest/input-objects/OrderCreateOptionsInput)The strategies for updating inventory and whether to send shipping and order confirmations to customers.

Show input fields[Anchor to orderCreateManualPayment](/docs/api/admin-graphql/latest/objects/Order#mutation-orderCreateManualPayment)[orderCreateManualPayment](/docs/api/admin-graphql/latest/mutations/orderCreateManualPayment)•mutationRecords a manual payment for an [`Order`](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order) that isn't fully paid. Use this mutation to track payments received outside the standard checkout process, such as cash, check, bank transfer, or other offline payment methods.

You can specify the payment [amount](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderCreateManualPayment#arguments-amount), [method name](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderCreateManualPayment#arguments-paymentMethodName), and [when it was processed](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderCreateManualPayment#arguments-processedAt).

Show payload### Arguments[Anchor to id](/docs/api/admin-graphql/latest/objects/Order#mutation-orderCreateManualPayment.arguments.id)id•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the order to create a manual payment for.

[Anchor to amount](/docs/api/admin-graphql/latest/objects/Order#mutation-orderCreateManualPayment.arguments.amount)amount•[MoneyInput](/docs/api/admin-graphql/latest/input-objects/MoneyInput)The manual payment amount to be created.

Show input fields[Anchor to paymentMethodName](/docs/api/admin-graphql/latest/objects/Order#mutation-orderCreateManualPayment.arguments.paymentMethodName)paymentMethodName•[String](/docs/api/admin-graphql/latest/scalars/String)The name of the payment method used for creating the payment. If none is provided, then the default manual payment method ('Other') will be used.

[Anchor to processedAt](/docs/api/admin-graphql/latest/objects/Order#mutation-orderCreateManualPayment.arguments.processedAt)processedAt•[DateTime](/docs/api/admin-graphql/latest/scalars/DateTime)The date and time ([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format) when a manual payment was processed. If you're importing transactions from an app or another platform, then you can set processedAt to a date and time in the past to match when the original transaction was created.

[Anchor to orderCustomerRemove](/docs/api/admin-graphql/latest/objects/Order#mutation-orderCustomerRemove)[orderCustomerRemove](/docs/api/admin-graphql/latest/mutations/orderCustomerRemove)•mutationRemoves customer from an order.

Show payload### Arguments[Anchor to orderId](/docs/api/admin-graphql/latest/objects/Order#mutation-orderCustomerRemove.arguments.orderId)orderId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the order having its customer removed.

[Anchor to orderCustomerSet](/docs/api/admin-graphql/latest/objects/Order#mutation-orderCustomerSet)[orderCustomerSet](/docs/api/admin-graphql/latest/mutations/orderCustomerSet)•mutationSets a customer on an order.

Show payload### Arguments[Anchor to orderId](/docs/api/admin-graphql/latest/objects/Order#mutation-orderCustomerSet.arguments.orderId)orderId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the order having a customer set.

[Anchor to customerId](/docs/api/admin-graphql/latest/objects/Order#mutation-orderCustomerSet.arguments.customerId)customerId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the customer being set on the order.

[Anchor to orderEditCommit](/docs/api/admin-graphql/latest/objects/Order#mutation-orderEditCommit)[orderEditCommit](/docs/api/admin-graphql/latest/mutations/orderEditCommit)•mutationApplies staged changes from an order editing session to the original order. This finalizes all modifications made during the edit session, including changes to line items, quantities, discounts, and shipping lines.

Order editing follows a three-step workflow: start with [`orderEditBegin`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderEditBegin) to create an editing session, apply changes using various orderEdit mutations, and then save the changes with the [`orderEditCommit`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderEditCommit) mutation. The mutation can optionally notify the customer of changes and add staff notes for internal tracking.

You can only edit unfulfilled line items. If an edit changes the total order value, then the customer might need to pay a balance or receive a refund.

Learn more about [editing existing orders](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps/edit-orders).

Show payload### Arguments[Anchor to id](/docs/api/admin-graphql/latest/objects/Order#mutation-orderEditCommit.arguments.id)id•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the [calculated order](https://shopify.dev/api/admin-graphql/latest/objects/calculatedorder)

or the order edit session that will have its changes applied to the order.

[Anchor to notifyCustomer](/docs/api/admin-graphql/latest/objects/Order#mutation-orderEditCommit.arguments.notifyCustomer)notifyCustomer•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Whether to notify the customer or not.

[Anchor to staffNote](/docs/api/admin-graphql/latest/objects/Order#mutation-orderEditCommit.arguments.staffNote)staffNote•[String](/docs/api/admin-graphql/latest/scalars/String)Note for staff members.

[Anchor to orderInvoiceSend](/docs/api/admin-graphql/latest/objects/Order#mutation-orderInvoiceSend)[orderInvoiceSend](/docs/api/admin-graphql/latest/mutations/orderInvoiceSend)•mutationSends an email invoice for an [`Order`](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order).

You can customize the email recipient, sender, and subject line using the [`email`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderInvoiceSend#arguments-email) argument.

NoteUse store or staff account email addresses for the [`from`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderInvoiceSend#arguments-email.fields.from) and [`bcc`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderInvoiceSend#arguments-email.fields.bcc) input fields.**Note:** Use store or staff account email addresses for the [`from`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderInvoiceSend#arguments-email.fields.from) and [`bcc`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderInvoiceSend#arguments-email.fields.bcc) input fields.**Note:** Use store or staff account email addresses for the <a href="https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderInvoiceSend#arguments-email.fields.from"><code>from</code></a> and <a href="https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderInvoiceSend#arguments-email.fields.bcc"><code>bcc</code></a> input fields.Show payload### Arguments[Anchor to id](/docs/api/admin-graphql/latest/objects/Order#mutation-orderInvoiceSend.arguments.id)id•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe order associated with the invoice.

[Anchor to email](/docs/api/admin-graphql/latest/objects/Order#mutation-orderInvoiceSend.arguments.email)email•[EmailInput](/docs/api/admin-graphql/latest/input-objects/EmailInput)The email input fields for the order invoice. The `bcc` and `from` fields should be store or staff account emails.

Show input fields[Anchor to orderMarkAsPaid](/docs/api/admin-graphql/latest/objects/Order#mutation-orderMarkAsPaid)[orderMarkAsPaid](/docs/api/admin-graphql/latest/mutations/orderMarkAsPaid)•mutationMarks an order as paid by recording a payment transaction for the outstanding amount.

Use the `orderMarkAsPaid` mutation to record payments received outside the standard checkout

process. The `orderMarkAsPaid` mutation is particularly useful in scenarios where:

- Orders were created with manual payment methods (cash on delivery, bank deposit, money order)

- Payments were received offline and need to be recorded in the system

- Previously authorized payments need to be captured manually

- Orders require manual payment reconciliation due to external payment processing

The mutation validates that the order can be marked as paid before processing.

An order can be marked as paid only if it has a positive outstanding balance and its

[financial status](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.displayFinancialStatus)

isn't already `PAID`. The mutation will either create a new sale transaction for the full

outstanding amount or capture an existing authorized transaction, depending on the order's current payment state.

After successfully marking an order as paid, the order's financial status is updated to

reflect the payment, and payment events are logged for tracking and analytics

purposes.

Learn more about [managing orders](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps)

in apps.

Show payload### Arguments[Anchor to input](/docs/api/admin-graphql/latest/objects/Order#mutation-orderMarkAsPaid.arguments.input)input•[OrderMarkAsPaidInput!](/docs/api/admin-graphql/latest/input-objects/OrderMarkAsPaidInput)requiredThe input for the mutation.

Show input fields[Anchor to orderOpen](/docs/api/admin-graphql/latest/objects/Order#mutation-orderOpen)[orderOpen](/docs/api/admin-graphql/latest/mutations/orderOpen)•mutationOpens a closed order.

Show payload### Arguments[Anchor to input](/docs/api/admin-graphql/latest/objects/Order#mutation-orderOpen.arguments.input)input•[OrderOpenInput!](/docs/api/admin-graphql/latest/input-objects/OrderOpenInput)requiredThe input for the mutation.

Show input fields[Anchor to orderUpdate](/docs/api/admin-graphql/latest/objects/Order#mutation-orderUpdate)[orderUpdate](/docs/api/admin-graphql/latest/mutations/orderUpdate)•mutationUpdates the attributes of an order, such as the customer's email, the shipping address for the order,

tags, and [metafields](https://shopify.dev/docs/apps/build/custom-data) associated with the order.

If you need to make significant updates to an order, such as adding or removing line items, changing

quantities, or modifying discounts, then use

the [`orderEditBegin`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderEditBegin)

mutation instead. The `orderEditBegin` mutation initiates an order editing session,

allowing you to make multiple changes before finalizing them. Learn more about using the `orderEditBegin`

mutation to [edit existing orders](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps/edit-orders).

If you need to remove a customer from an order, then use the [`orderCustomerRemove`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderCustomerRemove)

mutation instead.

Learn how to build apps that integrate with

[order management and fulfillment processes](https://shopify.dev/docs/apps/build/orders-fulfillment).

Show payload### Arguments[Anchor to input](/docs/api/admin-graphql/latest/objects/Order#mutation-orderUpdate.arguments.input)input•[OrderInput!](/docs/api/admin-graphql/latest/input-objects/OrderInput)requiredThe attributes of the updated order.

Show input fields[Anchor to refundCreate](/docs/api/admin-graphql/latest/objects/Order#mutation-refundCreate)[refundCreate](/docs/api/admin-graphql/latest/mutations/refundCreate)•mutationCreates a refund for an order, allowing you to process returns and issue payments back to customers.

Use the `refundCreate` mutation to programmatically process refunds in scenarios where you need to

return money to customers, such as when handling returns, processing chargebacks, or correcting

order errors.

The `refundCreate` mutation supports various refund scenarios:

- Refunding line items with optional restocking

- Refunding shipping costs

- Refunding duties and import taxes

- Refunding additional fees

- Processing refunds through different payment methods

- Issuing store credit refunds (when enabled)

You can create both full and partial refunds, and optionally allow over-refunding in specific

cases.

After creating a refund, you can track its status and details through the order's

[`refunds`](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order#field-Order.fields.refunds)

field. The refund is associated with the order and can be used for reporting and reconciliation purposes.

Learn more about

[managing returns](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-return-management)

and [refunding duties](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/view-and-refund-duties).

NoteThe refunding behavior of the `refundCreate` mutation is similar to the

[`refundReturn`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/returnRefund)

mutation. The key difference is that the `refundCreate` mutation lets you to specify restocking behavior

for line items, whereas the `returnRefund` mutation focuses solely on handling the financial refund without

any restocking input.**Note:** The refunding behavior of the `refundCreate` mutation is similar to the

[`refundReturn`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/returnRefund)

mutation. The key difference is that the `refundCreate` mutation lets you to specify restocking behavior

for line items, whereas the `returnRefund` mutation focuses solely on handling the financial refund without

any restocking input.**Note:** The refunding behavior of the <code><span class="PreventFireFoxApplyingGapToWBR">refund<wbr/>Create</span></code> mutation is similar to the

<a href="https://shopify.dev/docs/api/admin-graphql/latest/mutations/returnRefund"><code><span class="PreventFireFoxApplyingGapToWBR">refund<wbr/>Return</span></code></a>

mutation. The key difference is that the <code><span class="PreventFireFoxApplyingGapToWBR">refund<wbr/>Create</span></code> mutation lets you to specify restocking behavior

for line items, whereas the <code><span class="PreventFireFoxApplyingGapToWBR">return<wbr/>Refund</span></code> mutation focuses solely on handling the financial refund without

any restocking input.CautionAs of 2026-01, this mutation supports an optional idempotency key using the `@idempotent` directive.

As of 2026-04, the idempotency key is required and must be provided using the `@idempotent` directive.

For more information, see the [idempotency documentation](https://shopify.dev/docs/api/usage/idempotent-requests).**Caution:** As of 2026-01, this mutation supports an optional idempotency key using the `@idempotent` directive.

As of 2026-04, the idempotency key is required and must be provided using the `@idempotent` directive.

For more information, see the [idempotency documentation](https://shopify.dev/docs/api/usage/idempotent-requests).**Caution:** As of 2026-01, this mutation supports an optional idempotency key using the <code>@idempotent</code> directive.

As of 2026-04, the idempotency key is required and must be provided using the <code>@idempotent</code> directive.

For more information, see the <a href="https://shopify.dev/docs/api/usage/idempotent-requests">idempotency documentation</a>.Show payload### Arguments[Anchor to input](/docs/api/admin-graphql/latest/objects/Order#mutation-refundCreate.arguments.input)input•[RefundInput!](/docs/api/admin-graphql/latest/input-objects/RefundInput)requiredThe input fields that are used in the mutation for creating a refund.

Show input fields[Anchor to taxSummaryCreate](/docs/api/admin-graphql/latest/objects/Order#mutation-taxSummaryCreate)[taxSummaryCreate](/docs/api/admin-graphql/latest/mutations/taxSummaryCreate)•mutationCreates a tax summary for a given order.

If both an order ID and a start and end time are provided, the order ID will be used.

Show payload### Arguments[Anchor to orderId](/docs/api/admin-graphql/latest/objects/Order#mutation-taxSummaryCreate.arguments.orderId)orderId•[ID](/docs/api/admin-graphql/latest/scalars/ID)The ID of the order to create the tax summary for.

[Anchor to startTime](/docs/api/admin-graphql/latest/objects/Order#mutation-taxSummaryCreate.arguments.startTime)startTime•[DateTime](/docs/api/admin-graphql/latest/scalars/DateTime)The start time of the range of orders to create the tax summary for.

[Anchor to endTime](/docs/api/admin-graphql/latest/objects/Order#mutation-taxSummaryCreate.arguments.endTime)endTime•[DateTime](/docs/api/admin-graphql/latest/scalars/DateTime)The end time of the range of orders to create the tax summary for.

Was this section helpful?YesNo## <~> Order Mutations### Mutated by- <~>[orderClose](/docs/api/admin-graphql/latest/mutations/orderClose)- <~>[orderCreate](/docs/api/admin-graphql/latest/mutations/orderCreate)- <~>[orderCreateManualPayment](/docs/api/admin-graphql/latest/mutations/orderCreateManualPayment)- <~>[orderCustomerRemove](/docs/api/admin-graphql/latest/mutations/orderCustomerRemove)- <~>[orderCustomerSet](/docs/api/admin-graphql/latest/mutations/orderCustomerSet)- <~>[orderEditCommit](/docs/api/admin-graphql/latest/mutations/orderEditCommit)- <~>[orderInvoiceSend](/docs/api/admin-graphql/latest/mutations/orderInvoiceSend)- <~>[orderMarkAsPaid](/docs/api/admin-graphql/latest/mutations/orderMarkAsPaid)- <~>[orderOpen](/docs/api/admin-graphql/latest/mutations/orderOpen)- <~>[orderUpdate](/docs/api/admin-graphql/latest/mutations/orderUpdate)- <~>[refundCreate](/docs/api/admin-graphql/latest/mutations/refundCreate)- <~>[taxSummaryCreate](/docs/api/admin-graphql/latest/mutations/taxSummaryCreate)## [Anchor to Interfaces](/docs/api/admin-graphql/latest/objects/Order#interfaces)Interfaces- CommentEventSubject- HasEvents- HasLocalizationExtensions- HasLocalizedFields- HasMetafieldDefinitions- HasMetafields- LegacyInteroperability- Node[Anchor to CommentEventSubject](/docs/api/admin-graphql/latest/objects/Order#interface-CommentEventSubject)[CommentEventSubject](/docs/api/admin-graphql/latest/interfaces/CommentEventSubject)•interface[Anchor to HasEvents](/docs/api/admin-graphql/latest/objects/Order#interface-HasEvents)[HasEvents](/docs/api/admin-graphql/latest/interfaces/HasEvents)•interface[Anchor to HasLocalizationExtensions](/docs/api/admin-graphql/latest/objects/Order#interface-HasLocalizationExtensions)[HasLocalizationExtensions](/docs/api/admin-graphql/latest/interfaces/HasLocalizationExtensions)•interface[Anchor to HasLocalizedFields](/docs/api/admin-graphql/latest/objects/Order#interface-HasLocalizedFields)[HasLocalizedFields](/docs/api/admin-graphql/latest/interfaces/HasLocalizedFields)•interface[Anchor to HasMetafieldDefinitions](/docs/api/admin-graphql/latest/objects/Order#interface-HasMetafieldDefinitions)[HasMetafieldDefinitions](/docs/api/admin-graphql/latest/interfaces/HasMetafieldDefinitions)•interface[Anchor to HasMetafields](/docs/api/admin-graphql/latest/objects/Order#interface-HasMetafields)[HasMetafields](/docs/api/admin-graphql/latest/interfaces/HasMetafields)•interface[Anchor to LegacyInteroperability](/docs/api/admin-graphql/latest/objects/Order#interface-LegacyInteroperability)[LegacyInteroperability](/docs/api/admin-graphql/latest/interfaces/LegacyInteroperability)•interface[Anchor to Node](/docs/api/admin-graphql/latest/objects/Order#interface-Node)[Node](/docs/api/admin-graphql/latest/interfaces/Node)•interfaceWas this section helpful?YesNo## ||-Order Implements### Implements- ||-[CommentEventSubject](/docs/api/admin-graphql/latest/interfaces/CommentEventSubject)- ||-[HasEvents](/docs/api/admin-graphql/latest/interfaces/HasEvents)- ||-[HasLocalizationExtensions](/docs/api/admin-graphql/latest/interfaces/HasLocalizationExtensions)- ||-[HasLocalizedFields](/docs/api/admin-graphql/latest/interfaces/HasLocalizedFields)- ||-[HasMetafieldDefinitions](/docs/api/admin-graphql/latest/interfaces/HasMetafieldDefinitions)- ||-[HasMetafields](/docs/api/admin-graphql/latest/interfaces/HasMetafields)- ||-[LegacyInteroperability](/docs/api/admin-graphql/latest/interfaces/LegacyInteroperability)- ||-[Node](/docs/api/admin-graphql/latest/interfaces/Node)### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)