---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/layout-and-structure/divider",
    "fetched_at": "2026-02-10T13:30:27.492433",
    "status": 200,
    "size_bytes": 263534
  },
  "metadata": {
    "title": "Divider",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "layout-and-structure",
    "component": "divider"
  }
}
---

# Divider

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# DividerAsk assistantCreate clear visual separation between elements in your user interface.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/divider#properties)Properties[Anchor to color](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/divider#properties-propertydetail-color)color**color**"base" | "strong"**"base" | "strong"**Default: 'base'**Default: 'base'**Modify the color to be more or less intense.

[Anchor to direction](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/divider#properties-propertydetail-direction)direction**direction**"inline" | "block"**"inline" | "block"**Default: 'inline'**Default: 'inline'**Specify the direction of the divider. This uses [logical properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values).

ExamplesCodejsxhtmlCopy91<s-divider />## Preview### Examples- #### Codejsx```

<s-divider />

```html```

<s-divider></s-divider>

```- #### Basic usageDescriptionDemonstrates the default divider with standard base color and inline direction.jsx```

<s-divider />

```html```

<s-divider></s-divider>

```- #### Custom colorDescriptionShows a divider with a strong color variant for increased visual emphasis.jsx```

<s-divider color="strong" />

```html```

<s-divider color="strong"></s-divider>

```- #### Custom directionDescriptionIllustrates using a block-direction divider within an inline stack to create vertical separation between items.jsx```

<s-stack direction="inline" gap="base">

<s-text>Item 1</s-text>

<s-divider direction="block" />

<s-text>Item 2</s-text>

</s-stack>

```html```

<s-stack direction="inline" gap="base">

<s-text>Item 1</s-text>

<s-divider direction="block"></s-divider>

<s-text>Item 2</s-text>

</s-stack>

```- #### Separating form sectionsDescriptionUses a divider to visually group and separate different sections of a form, improving readability and user comprehension.jsx```

<s-stack gap="base">

<s-text-field label="Store name" />

<s-text-field label="Description" />

<s-divider />

<s-text-field label="Email address" />

<s-text-field label="Phone number" />

</s-stack>

```html```

<s-stack gap="base">

<s-text-field label="Store name"></s-text-field>

<s-text-field label="Description"></s-text-field>

<s-divider></s-divider>

<s-text-field label="Email address"></s-text-field>

<s-text-field label="Phone number"></s-text-field>

</s-stack>

```- #### Organizing settings panelsDescriptionDemonstrates using a divider to logically separate basic and advanced settings in a configuration panel.jsx```

<s-box padding="base">

<s-stack gap="base">

<s-switch label="Email notifications" />

<s-switch label="Auto-save" />

<s-divider />

<s-switch label="Advanced settings" />

<s-switch label="Developer tools" />

</s-stack>

</s-box>

```html```

<s-box padding="base">

<s-stack gap="base">

<s-switch label="Email notifications"></s-switch>

<s-switch label="Auto-save"></s-switch>

<s-divider></s-divider>

<s-switch label="Advanced settings"></s-switch>

<s-switch label="Developer tools"></s-switch>

</s-stack>

</s-box>

```- #### Visual breaks in section layoutsDescriptionShows how dividers can be used to create clean, segmented sections within a section, improving information hierarchy.jsx```

<s-box padding="large-400" background="base">

<s-stack gap="base">

<s-heading>Order summary</s-heading>

<s-text>3 items</s-text>

<s-divider />

<s-heading>Shipping address</s-heading>

<s-text>123 Main Street, Toronto ON</s-text>

<s-divider />

<s-heading>Payment method</s-heading>

<s-text>•••• 4242</s-text>

</s-stack>

</s-box>

```html```

<s-box padding="large-400" background="base">

<s-stack gap="base">

<s-heading>Order summary</s-heading>

<s-text>3 items</s-text>

<s-divider></s-divider>

<s-heading>Shipping address</s-heading>

<s-text>123 Main Street, Toronto ON</s-text>

<s-divider></s-divider>

<s-heading>Payment method</s-heading>

<s-text>•••• 4242</s-text>

</s-stack>

</s-box>

```- #### Separating content sectionsDescriptionIllustrates using dividers to create clear, visually distinct sections for different metrics or content blocks.jsx```

<s-stack gap="base">

<s-box padding="base">

<s-text>150 orders</s-text>

</s-box>

<s-divider />

<s-box padding="base">

<s-text>$2,400 revenue</s-text>

</s-box>

<s-divider />

<s-box padding="base">

<s-text>89 customers</s-text>

</s-box>

</s-stack>

```html```

<s-stack gap="base">

<s-box padding="base">

<s-text>150 orders</s-text>

</s-box>

<s-divider></s-divider>

<s-box padding="base">

<s-text>$2,400 revenue</s-text>

</s-box>

<s-divider></s-divider>

<s-box padding="base">

<s-text>89 customers</s-text>

</s-box>

</s-stack>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/divider#useful-for)Useful for

- Separating elements inside sections.

- Visually grouping related content in forms and lists.

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)