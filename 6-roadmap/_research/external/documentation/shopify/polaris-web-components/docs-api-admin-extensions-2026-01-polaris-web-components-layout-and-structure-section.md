---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/layout-and-structure/section",
    "fetched_at": "2026-02-10T13:30:34.502255",
    "status": 200,
    "size_bytes": 270179
  },
  "metadata": {
    "title": "Section",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "layout-and-structure",
    "component": "section"
  }
}
---

# Section

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# SectionAsk assistantGroups related content into clearly-defined thematic areas. Sections have contextual styling that automatically adapts based on nesting depth. They also adjust heading levels to maintain a meaningful and accessible page structure.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/section#properties)Properties[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/section#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label used to describe the section that will be announced by assistive technologies.

When no `heading` property is provided or included as a children of the Section, you **must** provide an `accessibilityLabel` to describe the Section. This is important as it allows assistive technologies to provide the right context to users.

[Anchor to heading](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/section#properties-propertydetail-heading)heading**heading**string**string**A title that describes the content of the section.

[Anchor to padding](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/section#properties-propertydetail-padding)padding**padding**"base" | "none"**"base" | "none"**Default: 'base'**Default: 'base'**Adjust the padding of all edges.

- `base`: applies padding that is appropriate for the element. Note that it may result in no padding if this is the right design decision in a particular context.

- `none`: removes all padding from the element. This can be useful when elements inside the Section need to span to the edge of the Section. For example, a full-width image. In this case, rely on `s-box` with a padding of 'base' to bring back the desired padding for the rest of the content.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/section#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/section#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Section.

ExamplesCodejsxhtmlCopy9123<s-section heading="Online store dashboard">  <s-paragraph>View a summary of your online store’s performance.</s-paragraph></s-section>## Preview### Examples- #### Codejsx```

<s-section heading="Online store dashboard">

<s-paragraph>View a summary of your online store’s performance.</s-paragraph>

</s-section>

```html```

<s-section heading="Online store dashboard">

<s-paragraph>View a summary of your online store’s performance.</s-paragraph>

</s-section>

```- #### Top-Level Section with Form ElementsDescriptionDemonstrates a level 1 section with a heading and multiple form fields. This example shows how sections provide visual hierarchy and structure for input elements.jsx```

<s-section heading="Customer information">

<s-text-field label="First name" value="John" />

<s-text-field label="Last name" value="Doe" />

<s-email-field label="Email" value="john@example.com" />

</s-section>

```html```

<!-- Level 1 section - elevated with shadow on desktop -->

<s-section heading="Customer information">

<s-text-field label="First name" value="John"></s-text-field>

<s-text-field label="Last name" value="Doe"></s-text-field>

<s-email-field label="Email" value="john@example.com"></s-email-field>

</s-section>

```- #### Nested Sections with Visual Level DifferencesDescriptionIllustrates how sections can be nested to create a hierarchical layout, with each nested section automatically adjusting its visual style. This example demonstrates the automatic visual leveling of nested sections.jsx```

<s-stack gap="base">

{/* Level 1 section */}

<s-section heading="Order details">

<s-paragraph>Order #1234 placed on January 15, 2024</s-paragraph>

{/* Level 2 section - nested with different visual treatment */}

<s-section heading="Customer">

<s-text-field label="Name" value="Jane Smith" />

<s-text-field label="Email" value="jane@example.com" />

{/* Level 3 section - further nested */}

<s-section heading="Billing address">

<s-text-field label="Street" value="123 Main St" />

<s-text-field label="City" value="Toronto" />

</s-section>

</s-section>

{/* Another Level 2 section */}

<s-section heading="Items">

<s-paragraph>2 items totaling $49.99</s-paragraph>

</s-section>

</s-section>

</s-stack>

```html```

<s-stack gap="base">

<!-- Level 1 section -->

<s-section heading="Order details">

<s-paragraph>Order #1234 placed on January 15, 2024</s-paragraph>

<!-- Level 2 section - nested with different visual treatment -->

<s-section heading="Customer">

<s-text-field label="Name" value="Jane Smith"></s-text-field>

<s-text-field label="Email" value="jane@example.com"></s-text-field>

<!-- Level 3 section - further nested -->

<s-section heading="Billing address">

<s-text-field label="Street" value="123 Main St"></s-text-field>

<s-text-field label="City" value="Toronto"></s-text-field>

</s-section>

</s-section>

<!-- Another Level 2 section -->

<s-section heading="Items">

<s-paragraph>2 items totaling $49.99</s-paragraph>

</s-section>

</s-section>

</s-stack>

```- #### Section with Accessibility LabelDescriptionShows how to add an accessibility label to a section, providing an additional hidden heading for screen readers while maintaining a visible heading.jsx```

<s-section

heading="Payment summary"

accessibilityLabel="Order payment breakdown and totals"

>

<s-stack>

<s-paragraph>Subtotal: $42.99</s-paragraph>

<s-paragraph>Tax: $5.59</s-paragraph>

<s-paragraph>Shipping: $1.41</s-paragraph>

<s-paragraph>

<s-text type="strong">Total: $49.99</s-text>

</s-paragraph>

</s-stack>

</s-section>

```html```

<s-section

heading="Payment summary"

accessibilityLabel="Order payment breakdown and totals"

>

<s-stack gap="base">

<s-paragraph>Subtotal: $42.99</s-paragraph>

<s-paragraph>Tax: $5.59</s-paragraph>

<s-paragraph>Shipping: $1.41</s-paragraph>

<s-paragraph>

<s-text type="strong">Total: $49.99</s-text>

</s-paragraph>

</s-stack>

</s-section>

```- #### Full-width Content LayoutDescriptionDemonstrates using a section with `padding="none"` to create a full-width layout, ideal for displaying tables or other content that requires edge-to-edge rendering.jsx```

<s-section padding="none">

<s-table>

<s-table-header-row>

<s-table-header listSlot="primary">Product</s-table-header>

<s-table-header listSlot="labeled">Price</s-table-header>

<s-table-header listSlot="inline">Status</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>Cotton t-shirt</s-table-cell>

<s-table-cell>$29.99</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```html```

<s-section padding="none">

<s-table>

<s-table-header-row>

<s-table-header listSlot="primary">Product</s-table-header>

<s-table-header listSlot="labeled">Price</s-table-header>

<s-table-header listSlot="inline">Status</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>Cotton t-shirt</s-table-cell>

<s-table-cell>$29.99</s-table-cell>

<s-table-cell><s-badge tone="success">Active</s-badge></s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/section#useful-for)Useful for

- Organizing your page in a logical structure based on nesting levels.

- Creating consistency across pages.

## [Anchor to considerations](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/section#considerations)Considerations

- When adding headings inside sections they automatically use a specific style, which helps keep the content organized and clear.

- Built-in spacing is added between nested sections, as well as between heading and content.

- **Level 1:** Display as responsive cards with background color, rounded corners, and shadow effects. Includes outer padding that can be removed when content like `s-table` needs to expand to the full width of the section.

- **Nested sections:** Don't have any background color or effects by default.

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)