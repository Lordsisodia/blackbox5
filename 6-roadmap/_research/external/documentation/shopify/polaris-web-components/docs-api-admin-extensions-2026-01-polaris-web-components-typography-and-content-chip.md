---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/typography-and-content/chip",
    "fetched_at": "2026-02-10T13:30:57.588279",
    "status": 200,
    "size_bytes": 266590
  },
  "metadata": {
    "title": "Chip",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "typography-and-content",
    "component": "chip"
  }
}
---

# Chip

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# ChipAsk assistantRepresents a set of user-supplied keywords that help label, organize, and categorize objects. Used to categorize or highlight content attributes. They are often displayed near the content they classify, enhancing discoverability by allowing users to identify items with similar properties.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/chip#properties)Properties[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/chip#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the Chip. It will be read to users using assistive technologies such as screen readers.

[Anchor to color](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/chip#properties-propertydetail-color)color**color**ColorKeywordColorKeyword**ColorKeywordColorKeyword**Default: 'base'**Default: 'base'**Modify the color to be more or less intense.

### ColorKeyword```

'subdued' | 'base' | 'strong'

```## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/chip#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/chip#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Chip.

[Anchor to graphic](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/chip#slots-propertydetail-graphic)graphic**graphic**HTMLElement**HTMLElement**The graphic to display in the chip.

Only accepts `Icon` components.

ExamplesCodejsxhtmlCopy91<s-chip>Chip</s-chip>## Preview### Examples- #### Codejsx```

<s-chip>Chip</s-chip>

```html```

<s-chip>Chip</s-chip>

```- #### Basic usageDescriptionSimple chip displaying product status without an icon.jsx```

<s-chip color="base" accessibilityLabel="Product status indicator">

Active

</s-chip>

```html```

<s-chip color="base" accessibilityLabel="Product status indicator">

Active

</s-chip>

```- #### With icon graphicDescriptionChip enhanced with an icon to provide visual context for the category.jsx```

<s-chip color="strong" accessibilityLabel="Product category">

<s-icon slot="graphic" type="catalog-product" size="small" />

Electronics

</s-chip>

```html```

<s-chip color="strong" accessibilityLabel="Product category">

<s-icon slot="graphic" type="catalog-product" size="small"></s-icon>

Electronics

</s-chip>

```- #### Color variantsDescriptionDemonstrates all three color variants for different levels of visual emphasis.jsx```

<s-stack direction="inline" gap="base">

<s-chip color="subdued" accessibilityLabel="Secondary information">

Draft

</s-chip>

<s-chip color="base" accessibilityLabel="Standard information">

Published

</s-chip>

<s-chip color="strong" accessibilityLabel="Important status">

<s-icon slot="graphic" type="check" size="small" />

Verified

</s-chip>

</s-stack>

```html```

<s-stack direction="inline" gap="base">

<s-chip color="subdued" accessibilityLabel="Secondary information">

Draft

</s-chip>

<s-chip color="base" accessibilityLabel="Standard information">

Published

</s-chip>

<s-chip color="strong" accessibilityLabel="Important status">

<s-icon slot="graphic" type="check" size="small"></s-icon>

Verified

</s-chip>

</s-stack>

```- #### Product statusDescriptionCommon status indicators demonstrating chips in real-world product management scenarios.jsx```

<s-stack direction="inline" gap="base">

<s-chip color="base" accessibilityLabel="Product status">

Active

</s-chip>

<s-chip color="subdued" accessibilityLabel="Product status">

Draft

</s-chip>

<s-chip color="strong" accessibilityLabel="Product status">

<s-icon slot="graphic" type="check" size="small" />

Published

</s-chip>

</s-stack>

```html```

<s-stack direction="inline" gap="base">

<s-chip color="base" accessibilityLabel="Product status">Active</s-chip>

<s-chip color="subdued" accessibilityLabel="Product status">Draft</s-chip>

<s-chip color="strong" accessibilityLabel="Product status">

<s-icon slot="graphic" type="check" size="small"></s-icon>

Published

</s-chip>

</s-stack>

```- #### Text truncationDescriptionDemonstrates automatic text truncation for long content within a constrained width.jsx```

<s-box maxInlineSize="200px">

<s-stack gap="base">

<s-chip color="base" accessibilityLabel="Long product name">

This is a very long product name that will be truncated with ellipsis when

it exceeds the container width

</s-chip>

<s-chip color="strong" accessibilityLabel="Long category name">

<s-icon slot="graphic" type="catalog-product" size="small" />

Electronics and computer accessories category with extended description

</s-chip>

</s-stack>

</s-box>

```html```

<s-box maxInlineSize="200px">

<s-stack gap="base">

<s-chip color="base" accessibilityLabel="Long product name">

This is a very long product name that will be truncated with ellipsis when

it exceeds the container width

</s-chip>

<s-chip color="strong" accessibilityLabel="Long category name">

<s-icon slot="graphic" type="catalog-product" size="small"></s-icon>

Electronics and computer accessories category with extended description

</s-chip>

</s-stack>

</s-box>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/chip#useful-for)Useful for

- Labeling, organizing, and categorizing objects

- Highlighting content attributes

- Enhancing discoverability by identifying items with similar properties

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/chip#best-practices)Best practices

- `subdued`: use for secondary or less important information

- `base`: use as default color

- `strong`: use for important or verified status

- Text truncates automatically, keep labels short to avoid truncation

- Chips are static indicators, not interactive or dismissible. For interactive chips, use ClickableChip

- Add icons to `graphic` slot to provide visual context

- Display chips near the content they classify

## [Anchor to content-guidelines](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/chip#content-guidelines)Content guidelinesChip labels should:

- Be short and concise to avoid truncation

- Use `accessibilityLabel` to describe purpose for screen readers

- Common status labels: `Active`, `Draft`, `Published`, `Verified`

- Common category labels: `Product type`, `Collection`, `Tag name`

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)