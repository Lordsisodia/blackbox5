---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/layout-and-structure/orderedlist",
    "fetched_at": "2026-02-10T13:30:31.049578",
    "status": 200,
    "size_bytes": 259612
  },
  "metadata": {
    "title": "OrderedList",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "layout-and-structure",
    "component": "orderedlist"
  }
}
---

# OrderedList

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# OrderedListAsk assistantDisplays a numbered list of related items in a specific sequence. Use to present step-by-step instructions, ranked items, or procedures where order matters.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/orderedlist#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/orderedlist#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The items of the OrderedList.

Only ListItems are accepted.

## [Anchor to listitem](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/orderedlist#listitem)ListItemRepresents a single item within an unordered or ordered list. Use only as a child of `s-unordered-list` or `s-ordered-list` components.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/orderedlist#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/orderedlist#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the ListItem.

ExamplesCodejsxhtmlCopy912345<s-ordered-list>  <s-list-item>Red shirt</s-list-item>  <s-list-item>Green shirt</s-list-item>  <s-list-item>Blue shirt</s-list-item></s-ordered-list>## Preview### Examples- #### Codejsx```

<s-ordered-list>

<s-list-item>Red shirt</s-list-item>

<s-list-item>Green shirt</s-list-item>

<s-list-item>Blue shirt</s-list-item>

</s-ordered-list>

```html```

<s-ordered-list>

<s-list-item>Red shirt</s-list-item>

<s-list-item>Green shirt</s-list-item>

<s-list-item>Blue shirt</s-list-item>

</s-ordered-list>

```- #### Basic usageDescriptionDemonstrates a simple ordered list with three sequential steps.jsx```

<s-ordered-list>

<s-list-item>Add products to your catalog</s-list-item>

<s-list-item>Set up payment methods</s-list-item>

<s-list-item>Configure shipping zones</s-list-item>

</s-ordered-list>

```html```

<s-ordered-list>

<s-list-item>Add products to your catalog</s-list-item>

<s-list-item>Set up payment methods</s-list-item>

<s-list-item>Configure shipping zones</s-list-item>

</s-ordered-list>

```- #### Order processing stepsDescriptionShows an ordered list with multiple steps in a workflow process.jsx```

<s-ordered-list>

<s-list-item>Review order details and customer information</s-list-item>

<s-list-item>Verify payment and billing address</s-list-item>

<s-list-item>Check inventory availability for all items</s-list-item>

<s-list-item>Generate fulfillment labels and packing slip</s-list-item>

<s-list-item>Package items and update tracking information</s-list-item>

<s-list-item>Send shipment confirmation to customer</s-list-item>

</s-ordered-list>

```html```

<s-ordered-list>

<s-list-item>Review order details and customer information</s-list-item>

<s-list-item>Verify payment and billing address</s-list-item>

<s-list-item>Check inventory availability for all items</s-list-item>

<s-list-item>Generate fulfillment labels and packing slip</s-list-item>

<s-list-item>Package items and update tracking information</s-list-item>

<s-list-item>Send shipment confirmation to customer</s-list-item>

</s-ordered-list>

```- #### Product setup instructionsDescriptionIllustrates a nested ordered list with sub-steps within main steps.jsx```

<s-ordered-list>

<s-list-item>

Create product listing with title and description

<s-ordered-list>

<s-list-item>Add high-quality product images</s-list-item>

<s-list-item>Set SEO title and meta description</s-list-item>

</s-ordered-list>

</s-list-item>

<s-list-item>Configure pricing and inventory tracking</s-list-item>

<s-list-item>Set up product variants (size, color, material)</s-list-item>

<s-list-item>Enable inventory tracking and set stock levels</s-list-item>

<s-list-item>Review and publish product to storefront</s-list-item>

</s-ordered-list>

```html```

<s-ordered-list>

<s-list-item>

Create product listing with title and description

<s-ordered-list>

<s-list-item>Add high-quality product images</s-list-item>

<s-list-item>Set SEO title and meta description</s-list-item>

</s-ordered-list>

</s-list-item>

<s-list-item>Configure pricing and inventory tracking</s-list-item>

<s-list-item>Set up product variants (size, color, material)</s-list-item>

<s-list-item>Enable inventory tracking and set stock levels</s-list-item>

<s-list-item>Review and publish product to storefront</s-list-item>

</s-ordered-list>

```- #### Fulfillment processDescriptionDisplays a complex nested list with multiple levels of sub-steps.jsx```

<s-ordered-list>

<s-list-item>

Process payment

<s-ordered-list>

<s-list-item>Verify card details</s-list-item>

<s-list-item>Apply discount codes</s-list-item>

<s-list-item>Calculate taxes</s-list-item>

</s-ordered-list>

</s-list-item>

<s-list-item>

Prepare shipment

<s-ordered-list>

<s-list-item>Print shipping label</s-list-item>

<s-list-item>Pack items securely</s-list-item>

</s-ordered-list>

</s-list-item>

<s-list-item>Update customer with tracking info</s-list-item>

</s-ordered-list>

```html```

<s-ordered-list>

<s-list-item>

Process payment

<s-ordered-list>

<s-list-item>Verify card details</s-list-item>

<s-list-item>Apply discount codes</s-list-item>

<s-list-item>Calculate taxes</s-list-item>

</s-ordered-list>

</s-list-item>

<s-list-item>

Prepare shipment

<s-ordered-list>

<s-list-item>Print shipping label</s-list-item>

<s-list-item>Pack items securely</s-list-item>

</s-ordered-list>

</s-list-item>

<s-list-item>Update customer with tracking info</s-list-item>

</s-ordered-list>

```## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/orderedlist#best-practices)Best practices

- Use to break up related content and improve scannability

- Phrase items consistently (start each with a noun or verb)

- Start each item with a capital letter

- Don't use commas or semicolons at the end of lines

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)