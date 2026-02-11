---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/typography-and-content/tooltip",
    "fetched_at": "2026-02-10T13:31:04.948898",
    "status": 200,
    "size_bytes": 246448
  },
  "metadata": {
    "title": "Tooltip",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "typography-and-content",
    "component": "tooltip"
  }
}
---

# Tooltip

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# TooltipAsk assistantDisplays helpful information in a small overlay when users hover or focus on an element. Use to provide additional context without cluttering the interface.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/tooltip#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/tooltip#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Tooltip.

Only accepts `Text`, `Paragraph` components, and raw `textContent`.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/tooltip#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/tooltip#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Tooltip.

Only accepts `Text`, `Paragraph` components, and raw `textContent`.

ExamplesCodejsxhtmlCopy9123456<>  <s-tooltip id="bold-tooltip">Bold</s-tooltip>  <s-button interestFor="bold-tooltip" accessibilityLabel="Bold">    B  </s-button></>## Preview### Examples- #### Codejsx```

<>

<s-tooltip id="bold-tooltip">Bold</s-tooltip>

<s-button interestFor="bold-tooltip" accessibilityLabel="Bold">

B

</s-button>

</>

```html```

<s-tooltip id="bold-tooltip">Bold</s-tooltip>

<s-button interestFor="bold-tooltip" accessibilityLabel="Bold">B</s-button>

```- #### Basic UsageDescriptionDemonstrates a simple tooltip that provides additional context for a text element when hovered or focused.jsx```

<>

<s-tooltip id="shipping-status-tooltip">

<s-text>This order has shipping labels.</s-text>

</s-tooltip>

<s-text interestFor="shipping-status-tooltip">Shipping status</s-text>

</>

```html```

<s-tooltip id="shipping-status-tooltip">

<s-text>This order has shipping labels.</s-text>

</s-tooltip>

<s-text interestFor="shipping-status-tooltip">Shipping status</s-text>

```- #### With Icon ButtonDescriptionShows how to add a tooltip to an icon button, providing a clear explanation of the button's action when hovered.jsx```

<>

<s-tooltip id="delete-button-tooltip">

<s-text>Delete item permanently</s-text>

</s-tooltip>

<s-button interestFor="delete-button-tooltip">

<s-icon tone="neutral" type="info" />

</s-button>

</>

```html```

<s-tooltip id="delete-button-tooltip">

<s-text>Delete item permanently</s-text>

</s-tooltip>

<s-button interestFor="delete-button-tooltip">

<s-icon tone="neutral" type="info"></s-icon>

</s-button>

```## [Anchor to usage](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/tooltip#usage)UsageTooltips only render on devices with a pointer and do not display on mobile devices.

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/typography-and-content/tooltip#best-practices)Best practices

- Use for additional, non-essential context only

- Provide for icon-only buttons or buttons with keyboard shortcuts

- Keep content concise and in sentence case

- Don't use for critical information, errors, or blocking messages

- Don't contain any links or buttons

- Use sparingly. If you need many tooltips, clarify the design and language instead

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)