---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/typography-and-content/text",
    "fetched_at": "2026-02-10T13:31:02.950433",
    "status": 200,
    "size_bytes": 277295
  },
  "metadata": {
    "title": "Text",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "typography-and-content",
    "component": "text"
  }
}
---

# Text

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# TextAsk assistantDisplays inline text with specific visual styles or tones. Use to emphasize or differentiate words or phrases within a Paragraph or other block-level components.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/text#properties)Properties[Anchor to accessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/text#properties-propertydetail-accessibilityvisibility)accessibilityVisibility**accessibilityVisibility**"visible" | "hidden" | "exclusive"**"visible" | "hidden" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the element.

- `visible`: the element is visible to all users.

- `hidden`: the element is removed from the accessibility tree but remains visible.

- `exclusive`: the element is visually hidden but remains in the accessibility tree.

[Anchor to color](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/text#properties-propertydetail-color)color**color**"base" | "subdued"**"base" | "subdued"**Default: 'base'**Default: 'base'**Modify the color to be more or less intense.

[Anchor to dir](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/text#properties-propertydetail-dir)dir**dir**"" | "auto" | "ltr" | "rtl"**"" | "auto" | "ltr" | "rtl"**Default: ''**Default: ''**Indicates the directionality of the element’s text.

- `ltr`: languages written from left to right (e.g. English)

- `rtl`: languages written from right to left (e.g. Arabic)

- `auto`: the user agent determines the direction based on the content

- `''`: direction is inherited from parent elements (equivalent to not setting the attribute)

[Anchor to fontVariantNumeric](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/text#properties-propertydetail-fontvariantnumeric)fontVariantNumeric**fontVariantNumeric**"auto" | "normal" | "tabular-nums"**"auto" | "normal" | "tabular-nums"**Default: 'auto' - inherit from the parent element**Default: 'auto' - inherit from the parent element**Set the numeric properties of the font.

[Anchor to interestFor](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/text#properties-propertydetail-interestfor)interestFor**interestFor**string**string**ID of a component that should respond to interest (e.g. hover and focus) on this component.

[Anchor to tone](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/text#properties-propertydetail-tone)tone**tone**"info" | "success" | "warning" | "critical" | "auto" | "neutral" | "caution"**"info" | "success" | "warning" | "critical" | "auto" | "neutral" | "caution"**Default: 'auto'**Default: 'auto'**Sets the tone of the component, based on the intention of the information being conveyed.

[Anchor to type](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/text#properties-propertydetail-type)type**type**"strong" | "generic" | "address" | "redundant"**"strong" | "generic" | "address" | "redundant"**Default: 'generic'**Default: 'generic'**Provide semantic meaning and default styling to the text.

Other presentation properties on Text override the default styling.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/text#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/text#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Text.

ExamplesCodejsxhtmlCopy91234<s-paragraph>  <s-text type="strong">Name: </s-text>  <s-text>Jane Doe</s-text></s-paragraph>## Preview### Examples- #### Codejsx```

<s-paragraph>

<s-text type="strong">Name: </s-text>

<s-text>Jane Doe</s-text>

</s-paragraph>

```html```

<s-paragraph>

<s-text type="strong">Name: </s-text>

<s-text>Jane Doe</s-text>

</s-paragraph>

```- #### Basic UsageDescriptionStandard text content for general interface messaging and descriptions.jsx```

<s-text>

Manage your products and inventory from one dashboard.

</s-text>

```html```

<s-text>

Manage your products and inventory from one dashboard.

</s-text>

```- #### Strong TextDescriptionEmphasized text for important messages and call-to-actions.jsx```

<s-text type="strong">

Free shipping on orders over $50

</s-text>

```html```

<s-text type="strong">

Free shipping on orders over $50

</s-text>

```- #### Semantic AddressDescriptionStructured address text with proper semantic meaning for screen readers.jsx```

<s-text type="address">

123 Commerce Street, Toronto, ON M5V 2H1

</s-text>

```html```

<s-text type="address">

123 Commerce Street, Toronto, ON M5V 2H1

</s-text>

```- #### Tabular NumbersDescriptionMonospace number formatting for consistent alignment in tables and financial data.jsx```

<s-text fontVariantNumeric="tabular-nums">

$1,234.56

</s-text>

```html```

<s-text fontVariantNumeric="tabular-nums">

$1,234.56

</s-text>

```- #### Status TonesDescriptionColor-coded text indicating different status states and semantic meanings.jsx```

<s-stack gap="small">

<s-text tone="success">Order fulfilled</s-text>

<s-text tone="critical">Payment failed</s-text>

<s-text tone="warning">Low inventory</s-text>

</s-stack>

```html```

<s-stack gap="small">

<s-text tone="success">Order fulfilled</s-text>

<s-text tone="critical">Payment failed</s-text>

<s-text tone="warning">Low inventory</s-text>

</s-stack>

```- #### Accessibility Hidden TextDescriptionText visible only to screen readers for providing additional context.jsx```

<s-text accessibilityVisibility="exclusive">

Product prices include tax

</s-text>

```html```

<s-text accessibilityVisibility="exclusive">

Product prices include tax

</s-text>

```- #### Right-to-Left TextDescriptionText direction support for RTL languages like Arabic and Hebrew.jsx```

<s-text dir="rtl">

محتوى النص باللغة العربية

</s-text>

```html```

<s-text dir="rtl">

محتوى النص باللغة العربية

</s-text>

```- #### Subdued ColorDescriptionLower contrast text for secondary information and timestamps.jsx```

<s-text color="subdued">

Last updated 2 hours ago

</s-text>

```html```

<s-text color="subdued">

Last updated 2 hours ago

</s-text>

```- #### Interest For AssociationDescriptionText element associated with tooltips using the `interestFor` attribute to show additional information on hover or focus.jsx```

<>

<s-tooltip id="sku-tooltip">

SKU must be unique across all products and cannot be changed after creation

</s-tooltip>

<s-text color="subdued" interestFor="sku-tooltip">

What is a product SKU?

</s-text>

</>

```html```

<s-tooltip id="sku-tooltip">

SKU must be unique across all products and cannot be changed after creation

</s-tooltip>

<s-text color="subdued" interestFor="sku-tooltip">

What is a product SKU?

</s-text>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/text#useful-for)Useful for

- Adding inline text elements such as labels or line errors.

- Applying different visual tones and text styles to specific words or phrases within a `s-paragraph`, such as a `strong` type or `critical` tone.

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/text#best-practices)Best practices

- Text elements display inline and will flow on the same line when placed next to each other. To stack multiple text elements vertically, wrap them in a Stack container or use multiple `s-paragraph` components.

- Use plain and clear terms.

- Don't use jargon or technical language.

- Don't use different terms to describe the same thing.

- Don't duplicate content.

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)