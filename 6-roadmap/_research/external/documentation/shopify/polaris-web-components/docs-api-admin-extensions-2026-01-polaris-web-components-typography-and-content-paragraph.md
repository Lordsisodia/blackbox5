---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/typography-and-content/paragraph",
    "fetched_at": "2026-02-10T13:31:01.035874",
    "status": 200,
    "size_bytes": 276355
  },
  "metadata": {
    "title": "Paragraph",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "typography-and-content",
    "component": "paragraph"
  }
}
---

# Paragraph

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# ParagraphAsk assistantDisplays a block of text and can contain inline elements such as buttons, links, or emphasized text. Use to present standalone blocks of content as opposed to inline text.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/paragraph#properties)Properties[Anchor to accessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/paragraph#properties-propertydetail-accessibilityvisibility)accessibilityVisibility**accessibilityVisibility**"visible" | "hidden" | "exclusive"**"visible" | "hidden" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the element.

- `visible`: the element is visible to all users.

- `hidden`: the element is removed from the accessibility tree but remains visible.

- `exclusive`: the element is visually hidden but remains in the accessibility tree.

[Anchor to color](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/paragraph#properties-propertydetail-color)color**color**"base" | "subdued"**"base" | "subdued"**Default: 'base'**Default: 'base'**Modify the color to be more or less intense.

[Anchor to dir](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/paragraph#properties-propertydetail-dir)dir**dir**"" | "auto" | "ltr" | "rtl"**"" | "auto" | "ltr" | "rtl"**Default: ''**Default: ''**Indicates the directionality of the element’s text.

- `ltr`: languages written from left to right (e.g. English)

- `rtl`: languages written from right to left (e.g. Arabic)

- `auto`: the user agent determines the direction based on the content

- `''`: direction is inherited from parent elements (equivalent to not setting the attribute)

[Anchor to fontVariantNumeric](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/paragraph#properties-propertydetail-fontvariantnumeric)fontVariantNumeric**fontVariantNumeric**"auto" | "normal" | "tabular-nums"**"auto" | "normal" | "tabular-nums"**Default: 'auto' - inherit from the parent element**Default: 'auto' - inherit from the parent element**Set the numeric properties of the font.

[Anchor to lineClamp](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/paragraph#properties-propertydetail-lineclamp)lineClamp**lineClamp**number**number**Default: Infinity - no truncation is applied**Default: Infinity - no truncation is applied**Truncates the text content to the specified number of lines.

[Anchor to tone](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/paragraph#properties-propertydetail-tone)tone**tone**"info" | "success" | "warning" | "critical" | "auto" | "neutral" | "caution"**"info" | "success" | "warning" | "critical" | "auto" | "neutral" | "caution"**Default: 'auto'**Default: 'auto'**Sets the tone of the component, based on the intention of the information being conveyed.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/paragraph#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/paragraph#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Paragraph.

ExamplesCodejsxhtmlCopy91234<s-paragraph>  Shopify POS is the easiest way to sell your products in person. Available for  iPad, iPhone, and Android.</s-paragraph>## Preview### Examples- #### Codejsx```

<s-paragraph>

Shopify POS is the easiest way to sell your products in person. Available for

iPad, iPhone, and Android.

</s-paragraph>

```html```

<s-paragraph>

Shopify POS is the easiest way to sell your products in person. Available for

iPad, iPhone, and Android.

</s-paragraph>

```- #### Basic UsageDescriptionDemonstrates a simple paragraph with default styling, showing how to use the paragraph component for standard text content.jsx```

<s-paragraph>

Track inventory across all your retail locations in real-time.

</s-paragraph>

```html```

<s-paragraph>

Track inventory across all your retail locations in real-time.

</s-paragraph>

```- #### With Tone and ColorDescriptionIllustrates how to apply different tones and color variations to convey different types of information, such as informational and success messages.jsx```

<s-section>

<s-paragraph tone="info" color="base">

Your order will be processed within 2-3 business days.

</s-paragraph>

<s-paragraph tone="success" color="subdued">

Payment successfully processed.

</s-paragraph>

</s-section>

```html```

<s-section>

<s-paragraph tone="info" color="base">

Your order will be processed within 2-3 business days.

</s-paragraph>

<s-paragraph tone="success" color="subdued">

Payment successfully processed.

</s-paragraph>

</s-section>

```- #### Line ClampingDescriptionShows how to limit the number of lines displayed using the lineClamp prop, which truncates long text with an ellipsis after the specified number of lines.jsx```

<s-box inlineSize="300px">

<s-paragraph lineClamp={1}>

Premium organic cotton t-shirt featuring sustainable manufacturing

processes, ethically sourced materials, and carbon-neutral shipping.

Available in multiple colors and sizes with customization options for your

brand.

</s-paragraph>

</s-box>

```html```

<s-box inlineSize="300px">

<s-paragraph lineClamp="1">

Premium organic cotton t-shirt featuring sustainable manufacturing

processes, ethically sourced materials, and carbon-neutral shipping.

Available in multiple colors and sizes with customization options for your

brand.

</s-paragraph>

</s-box>

```- #### Tabular NumbersDescriptionDemonstrates the use of tabular numbers with fontVariantNumeric, ensuring consistent alignment and readability for numerical data.jsx```

<s-paragraph fontVariantNumeric="tabular-nums">

Orders: 1,234 Revenue: $45,678.90 Customers: 890

</s-paragraph>

```html```

<s-paragraph fontVariantNumeric="tabular-nums">

Orders: 1,234 Revenue: $45,678.90 Customers: 890

</s-paragraph>

```- #### RTL SupportDescriptionIllustrates right-to-left (RTL) text rendering, showing how the paragraph component supports internationalization and different text directions.jsx```

<s-paragraph dir="rtl">

محتوى النص باللغة العربية

</s-paragraph>

```html```

<s-paragraph dir="rtl">

محتوى النص باللغة العربية

</s-paragraph>

```- #### Screen Reader TextDescriptionShows how to use the accessibilityVisibility prop to create text that is exclusively available to screen readers, improving accessibility for assistive technologies.jsx```

<s-paragraph accessibilityVisibility="exclusive">

Table sorted by date, newest first.

</s-paragraph>

```html```

<s-paragraph accessibilityVisibility="exclusive">

Table sorted by date, newest first.

</s-paragraph>

```- #### Admin UI PatternsDescriptionShowcases various tone and color combinations for different administrative messages, illustrating how paragraph can communicate different types of information in a user interface.jsx```

<s-section>

<s-paragraph tone="success" color="base">

Payment successfully processed and order confirmed.

</s-paragraph>

<s-paragraph tone="warning" color="base">

Inventory levels are running low for this product.

</s-paragraph>

<s-paragraph tone="critical" color="base">

This order requires immediate attention due to shipping delays.

</s-paragraph>

<s-paragraph tone="info" color="base">

Customer requested gift wrapping for this order.

</s-paragraph>

<s-paragraph tone="caution" color="base">

Review shipping address before processing.

</s-paragraph>

</s-section>

```html```

<s-section>

<s-paragraph tone="success" color="base">

Payment successfully processed and order confirmed.

</s-paragraph>

<s-paragraph tone="warning" color="base">

Inventory levels are running low for this product.

</s-paragraph>

<s-paragraph tone="critical" color="base">

This order requires immediate attention due to shipping delays.

</s-paragraph>

<s-paragraph tone="info" color="base">

Customer requested gift wrapping for this order.

</s-paragraph>

<s-paragraph tone="caution" color="base">

Review shipping address before processing.

</s-paragraph>

</s-section>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/paragraph#useful-for)Useful for

- Displaying text content in a paragraph format.

- Grouping elements with the same style. For instance, icons inside a paragraph will automatically adopt the paragraph's tone.

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/paragraph#best-practices)Best practices

- Use short paragraphs to make your content scannable.

- Use plain and clear terms.

- Don't use jargon or technical language.

- Don't use different terms to describe the same thing.

- Don't duplicate content.

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)