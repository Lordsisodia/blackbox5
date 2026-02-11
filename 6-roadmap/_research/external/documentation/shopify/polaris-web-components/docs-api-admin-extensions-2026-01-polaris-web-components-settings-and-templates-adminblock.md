---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/settings-and-templates/adminblock",
    "fetched_at": "2026-02-10T13:30:54.164360",
    "status": 200,
    "size_bytes": 230441
  },
  "metadata": {
    "title": "AdminBlock",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "settings-and-templates",
    "component": "adminblock"
  }
}
---

# AdminBlock

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# AdminBlockAsk assistant`s-admin-block` provides a deeper integration with the container your UI is rendered into. This component should only be used in Block Extensions, which render inline on a resource page.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/settings-and-templates/adminblock#properties)Properties[Anchor to collapsedSummary](/docs/api/admin-extensions/latest/polaris-web-components/settings-and-templates/adminblock#properties-propertydetail-collapsedsummary)collapsedSummary**collapsedSummary**string**string**The summary to display when the app block is collapsed. Summary longer than 30 characters will be truncated.

[Anchor to heading](/docs/api/admin-extensions/latest/polaris-web-components/settings-and-templates/adminblock#properties-propertydetail-heading)heading**heading**string**string**The text to use as the Block title in the block header. If not provided, the name of the extension will be used.

ExamplesExample## jsx Copy91<s-admin-block title="My App Block">5 items active</s-admin-block>;## Preview### Examples- #### jsx```

<s-admin-block title="My App Block">5 items active</s-admin-block>;

```## [Anchor to considerations](/docs/api/admin-extensions/latest/polaris-web-components/settings-and-templates/adminblock#considerations)Considerations

- Initial height is limited to 300px.

- When content exceeds the height limit, a "Show more" button appears.

- In development, the following warning also displays: "Warning! This Block is too tall."

- After expanding to the max height, content that exceeds the limit is cut off, and the merchant must navigate to the extension's app via the provided link.

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)