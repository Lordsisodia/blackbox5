---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/layout-and-structure/unorderedlist",
    "fetched_at": "2026-02-10T13:30:40.910235",
    "status": 200,
    "size_bytes": 250244
  },
  "metadata": {
    "title": "UnorderedList",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "layout-and-structure",
    "component": "unorderedlist"
  }
}
---

# UnorderedList

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# UnorderedListAsk assistantDisplays a bulleted list of related items. Use to present collections of items or options where the sequence isn’t critical.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/unorderedlist#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/unorderedlist#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The items of the UnorderedList.

Only ListItems are accepted.

## [Anchor to listitem](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/unorderedlist#listitem)ListItemRepresents a single item within an unordered or ordered list. Use only as a child of `s-unordered-list` or `s-ordered-list` components.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/unorderedlist#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/unorderedlist#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the ListItem.

ExamplesCodejsxhtmlCopy912345<s-unordered-list>  <s-list-item>Red shirt</s-list-item>  <s-list-item>Green shirt</s-list-item>  <s-list-item>Blue shirt</s-list-item></s-unordered-list>## Preview### Examples- #### Codejsx```

<s-unordered-list>

<s-list-item>Red shirt</s-list-item>

<s-list-item>Green shirt</s-list-item>

<s-list-item>Blue shirt</s-list-item>

</s-unordered-list>

```html```

<s-unordered-list>

<s-list-item>Red shirt</s-list-item>

<s-list-item>Green shirt</s-list-item>

<s-list-item>Blue shirt</s-list-item>

</s-unordered-list>

```- #### Unordered list with nested itemsDescriptionA standard unordered list with nested items demonstrating hierarchical content structure.jsx```

<s-stack gap="base">

<s-box borderWidth="small-100" borderRadius="base" padding="base">

<s-unordered-list>

<s-list-item>Configure payment settings</s-list-item>

<s-list-item>

Set up shipping options

<s-unordered-list>

<s-list-item>Domestic shipping rates</s-list-item>

<s-list-item>International shipping zones</s-list-item>

</s-unordered-list>

</s-list-item>

<s-list-item>Add product descriptions</s-list-item>

</s-unordered-list>

</s-box>

<s-box borderWidth="small-100" borderRadius="base" padding="base">

<s-unordered-list>

<s-list-item>Enable online payments</s-list-item>

<s-list-item>Set up shipping rates</s-list-item>

<s-list-item>Configure tax settings</s-list-item>

<s-list-item>Add product descriptions</s-list-item>

</s-unordered-list>

</s-box>

</s-stack>

```html```

<s-stack gap="base">

<s-box borderWidth="small-100" borderRadius="base" padding="base">

<s-unordered-list>

<s-list-item>Configure payment settings</s-list-item>

<s-list-item>

Set up shipping options

<s-unordered-list>

<s-list-item>Domestic shipping rates</s-list-item>

<s-list-item>International shipping zones</s-list-item>

</s-unordered-list>

</s-list-item>

<s-list-item>Add product descriptions</s-list-item>

</s-unordered-list>

</s-box>

<s-box borderWidth="small-100" borderRadius="base" padding="base">

<s-unordered-list>

<s-list-item>Enable online payments</s-list-item>

<s-list-item>Set up shipping rates</s-list-item>

<s-list-item>Configure tax settings</s-list-item>

<s-list-item>Add product descriptions</s-list-item>

</s-unordered-list>

</s-box>

</s-stack>

```## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/unorderedlist#best-practices)Best practices

- Use to break up related content and improve scannability

- Phrase items consistently (start each with a noun or verb)

- Start each item with a capital letter

- Don't use commas or semicolons at the end of lines

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)