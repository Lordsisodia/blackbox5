---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/typography-and-content/heading",
    "fetched_at": "2026-02-10T13:30:59.301892",
    "status": 200,
    "size_bytes": 259537
  },
  "metadata": {
    "title": "Heading",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "typography-and-content",
    "component": "heading"
  }
}
---

# Heading

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# HeadingAsk assistantRenders hierarchical titles to communicate the structure and organization of page content. Heading levels adjust automatically based on nesting within parent Section components, ensuring a meaningful and accessible page outline.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/heading#properties)Properties[Anchor to accessibilityRole](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/heading#properties-propertydetail-accessibilityrole)accessibilityRole**accessibilityRole**"none" | "presentation" | "heading"**"none" | "presentation" | "heading"**Default: 'heading'**Default: 'heading'**Sets the semantic meaning of the component’s content. When set, the role will be used by assistive technologies to help users navigate the page.

- `heading`: defines the element as a heading to a page or section.

- `presentation`: the heading level will be stripped, and will prevent the element’s implicit ARIA semantics from being exposed to the accessibility tree.

- `none`: a synonym for the `presentation` role.

[Anchor to accessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/heading#properties-propertydetail-accessibilityvisibility)accessibilityVisibility**accessibilityVisibility**"visible" | "hidden" | "exclusive"**"visible" | "hidden" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the element.

- `visible`: the element is visible to all users.

- `hidden`: the element is removed from the accessibility tree but remains visible.

- `exclusive`: the element is visually hidden but remains in the accessibility tree.

[Anchor to lineClamp](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/heading#properties-propertydetail-lineclamp)lineClamp**lineClamp**number**number**Default: Infinity - no truncation is applied**Default: Infinity - no truncation is applied**Truncates the text content to the specified number of lines.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/heading#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/heading#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Heading.

ExamplesCodejsxhtmlCopy91<s-heading>Online store dashboard</s-heading>## Preview### Examples- #### Codejsx```

<s-heading>Online store dashboard</s-heading>

```html```

<s-heading>Online store dashboard</s-heading>

```- #### Basic headingDescriptionStandard heading for section titles and page content organization that creates a simple, clean title for a content section.jsx```

<s-heading>Product details</s-heading>

```html```

<s-heading>Product details</s-heading>

```- #### Heading with line clampingDescriptionTruncated heading that limits text to a specified number of lines, using ellipsis to indicate additional content for long product names or constrained layouts.jsx```

<s-box inlineSize="200px">

<s-heading lineClamp={2}>

Premium organic cotton t-shirt with sustainable manufacturing practices

</s-heading>

</s-box>

```html```

<s-box inlineSize="200px">

<s-heading lineClamp="2">

Premium organic cotton t-shirt with sustainable manufacturing practices

</s-heading>

</s-box>

```- #### Heading with custom accessibilityDescriptionHeading configured with custom ARIA roles and visibility settings to meet specific accessibility requirements or design constraints.jsx```

<s-heading accessibilityRole="presentation" accessibilityVisibility="hidden">

Sale badge

</s-heading>

```html```

<s-heading accessibilityRole="presentation" accessibilityVisibility="hidden">

Sale badge

</s-heading>

```- #### Heading within section hierarchyDescriptionDemonstrates nested heading structure that automatically adjusts heading levels (h2, h3, h4) based on the current section depth, ensuring proper semantic document structure.jsx```

<s-section>

<s-heading>Order information</s-heading>

{/* Renders as h2 */}

<s-section>

<s-heading>Shipping details</s-heading>

{/* Renders as h3 */}

<s-section>

<s-heading>Tracking updates</s-heading>

{/* Renders as h4 */}

</s-section>

</s-section>

</s-section>

```html```

<s-section>

<s-heading>Order information</s-heading>

<!-- Renders as h2 -->

<s-section>

<s-heading>Shipping details</s-heading>

<!-- Renders as h3 -->

<s-section>

<s-heading>Tracking updates</s-heading>

<!-- Renders as h4 -->

</s-section>

</s-section>

</s-section>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/heading#useful-for)Useful for

- Creating titles and subtitles for your content that are consistent across your app.

- Helping users with visual impairments navigate through content effectively using assistive technologies like screen readers.

## [Anchor to considerations](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/heading#considerations)Considerations

- The level of the heading is automatically determined by how deeply it's nested inside other components, starting from h2.

- Default to using the `heading` property in `s-section`. The `s-heading` component should only be used if you need to implement a custom layout for your heading in the UI.

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/heading#best-practices)Best practices

- Use short headings to make your content scannable.

- Use plain and clear terms.

- Don't use jargon or technical language.

- Don't use different terms to describe the same thing.

- Don't duplicate content.

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)