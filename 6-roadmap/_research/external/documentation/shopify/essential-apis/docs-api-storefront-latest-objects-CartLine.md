---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront/latest/objects/CartLine",
    "fetched_at": "2026-02-10T13:41:09.330103",
    "status": 200,
    "size_bytes": 298549
  },
  "metadata": {
    "title": "CartLine - Storefront API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "objects",
    "component": "CartLine"
  }
}
---

# CartLine - Storefront API

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to CartLine](/docs/api/storefront/latest/objects/CartLine#top)# CartLineobjectAsk assistantRepresents information about the merchandise in the cart.

## [Anchor to Fields](/docs/api/storefront/latest/objects/CartLine#fields)Fields- attribute (Attribute)- attributes ([Attribute!]!)- cost (CartLineCost!)- discountAllocations ([CartDiscountAllocation!]!)- id (ID!)- instructions (CartLineInstructions!)- merchandise (Merchandise!)- parentRelationship (CartLineParentRelationship)- quantity (Int!)- sellingPlanAllocation (SellingPlanAllocation)- estimatedCost (CartLineEstimatedCost!): deprecated[Anchor to attribute](/docs/api/storefront/latest/objects/CartLine#field-CartLine.fields.attribute)attribute•[Attribute](/docs/api/storefront/latest/objects/Attribute)An attribute associated with the cart line.

Show fields### Arguments[Anchor to key](/docs/api/storefront/latest/objects/CartLine#field-CartLine.fields.attribute.arguments.key)key•[String!](/docs/api/storefront/latest/scalars/String)requiredThe key of the attribute.

[Anchor to attributes](/docs/api/storefront/latest/objects/CartLine#field-CartLine.fields.attributes)attributes•[[Attribute!]!](/docs/api/storefront/latest/objects/Attribute)non-nullThe attributes associated with the cart line. Attributes are represented as key-value pairs.

Show fields[Anchor to cost](/docs/api/storefront/latest/objects/CartLine#field-CartLine.fields.cost)cost•[CartLineCost!](/docs/api/storefront/latest/objects/CartLineCost)non-nullThe cost of the merchandise that the buyer will pay for at checkout. The costs are subject to change and changes will be reflected at checkout.

Show fields[Anchor to discountAllocations](/docs/api/storefront/latest/objects/CartLine#field-CartLine.fields.discountAllocations)discountAllocations•[[CartDiscountAllocation!]!](/docs/api/storefront/latest/interfaces/CartDiscountAllocation)non-nullThe discounts that have been applied to the cart line.

Show fields[Anchor to id](/docs/api/storefront/latest/objects/CartLine#field-CartLine.fields.id)id•[ID!](/docs/api/storefront/latest/scalars/ID)non-nullA globally-unique ID.

[Anchor to instructions](/docs/api/storefront/latest/objects/CartLine#field-CartLine.fields.instructions)instructions•[CartLineInstructions!](/docs/api/storefront/latest/objects/CartLineInstructions)non-nullThe instructions for the line item.

Show fields[Anchor to merchandise](/docs/api/storefront/latest/objects/CartLine#field-CartLine.fields.merchandise)merchandise•[Merchandise!](/docs/api/storefront/latest/unions/Merchandise)non-nullThe merchandise that the buyer intends to purchase.

Show union types[Anchor to parentRelationship](/docs/api/storefront/latest/objects/CartLine#field-CartLine.fields.parentRelationship)parentRelationship•[CartLineParentRelationship](/docs/api/storefront/latest/objects/CartLineParentRelationship)The parent of the line item.

Show fields[Anchor to quantity](/docs/api/storefront/latest/objects/CartLine#field-CartLine.fields.quantity)quantity•[Int!](/docs/api/storefront/latest/scalars/Int)non-nullThe quantity of the merchandise that the customer intends to purchase.

[Anchor to sellingPlanAllocation](/docs/api/storefront/latest/objects/CartLine#field-CartLine.fields.sellingPlanAllocation)sellingPlanAllocation•[SellingPlanAllocation](/docs/api/storefront/latest/objects/SellingPlanAllocation)The selling plan associated with the cart line and the effect that each selling plan has on variants when they're purchased.

Show fields[Anchor to estimatedCost](/docs/api/storefront/latest/objects/CartLine#field-CartLine.fields.estimatedCost)estimatedCost•[CartLineEstimatedCost!](/docs/api/storefront/latest/objects/CartLineEstimatedCost)non-nullDeprecatedShow fieldsWas this section helpful?YesNo## Map### Fields with this object- {}[CartLineParentRelationship.parent](/docs/api/storefront/latest/objects/CartLineParentRelationship#field-CartLineParentRelationship.fields.parent)- {}[ComponentizableCartLine.lineComponents](/docs/api/storefront/latest/objects/ComponentizableCartLine#field-ComponentizableCartLine.fields.lineComponents)## [Anchor to Interfaces](/docs/api/storefront/latest/objects/CartLine#interfaces)Interfaces- BaseCartLine- Node[Anchor to BaseCartLine](/docs/api/storefront/latest/objects/CartLine#interface-BaseCartLine)[BaseCartLine](/docs/api/storefront/latest/interfaces/BaseCartLine)•interface[Anchor to Node](/docs/api/storefront/latest/objects/CartLine#interface-Node)[Node](/docs/api/storefront/latest/interfaces/Node)•interfaceWas this section helpful?YesNo## ||-CartLine Implements### Implements- ||-[BaseCartLine](/docs/api/storefront/latest/interfaces/BaseCartLine)- ||-[Node](/docs/api/storefront/latest/interfaces/Node)### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)