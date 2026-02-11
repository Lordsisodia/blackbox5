---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/feedback-and-status-indicators/spinner",
    "fetched_at": "2026-02-10T13:29:35.302331",
    "status": 200,
    "size_bytes": 247878
  },
  "metadata": {
    "title": "Spinner",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "feedback-and-status-indicators",
    "component": "spinner"
  }
}
---

# Spinner

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# SpinnerAsk assistantDisplays an animated indicator showing users that content or actions are loading. Use to communicate ongoing processes, such as fetching data from a server. For loading states on buttons, use the “loading” property on the Button component instead.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/spinner#properties)Properties[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/spinner#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose of the progress. When set, it will be announced to users using assistive technologies and will provide them with more context. Providing an `accessibilityLabel` is recommended if there is no accompanying text describing that something is loading.

[Anchor to size](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/spinner#properties-propertydetail-size)size**size**"base" | "large" | "large-100"**"base" | "large" | "large-100"**Default: 'base'**Default: 'base'**ExamplesCodejsxhtmlCopy91<s-spinner accessibilityLabel="Loading" size="large-100" />## Preview### Examples- #### Codejsx```

<s-spinner accessibilityLabel="Loading" size="large-100" />

```html```

<s-spinner accessibilityLabel="Loading" size="large-100"></s-spinner>

```- #### Basic usageDescriptionStandard loading spinner with accessibility label for screen readers.jsx```

<s-spinner accessibilityLabel="Loading content" />

```html```

<s-spinner accessibilityLabel="Loading content"></s-spinner>

```- #### Loading state in sectionDescriptionCentered loading indicator with text in a section layout for content loading states.jsx```

<s-stack alignItems="center" gap="base" padding="large">

<s-spinner accessibilityLabel="Loading products" size="large" />

<s-text>Loading products...</s-text>

</s-stack>

```html```

<s-stack alignItems="center" gap="base" padding="large">

<s-spinner accessibilityLabel="Loading products" size="large"></s-spinner>

<s-text>Loading products...</s-text>

</s-stack>

```- #### Inline loading with textDescriptionCompact inline loading indicator for form submissions and quick actions.jsx```

<s-stack direction="inline" alignItems="center" gap="small">

<s-spinner accessibilityLabel="Saving" />

<s-text>Saving...</s-text>

</s-stack>

```html```

<s-stack direction="inline" alignItems="center" gap="small">

<s-spinner accessibilityLabel="Saving"></s-spinner>

<s-text>Saving...</s-text>

</s-stack>

```## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/feedback-and-status-indicators/spinner#best-practices)Best practices

- Use to notify merchants that their action is being processed

- Don't use for entire page loads

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)