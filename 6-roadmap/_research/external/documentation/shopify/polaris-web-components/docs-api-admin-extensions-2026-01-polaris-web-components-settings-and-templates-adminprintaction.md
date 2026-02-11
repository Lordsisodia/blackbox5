---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/settings-and-templates/adminprintaction",
    "fetched_at": "2026-02-10T13:30:55.839276",
    "status": 200,
    "size_bytes": 229582
  },
  "metadata": {
    "title": "AdminPrintAction",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "settings-and-templates",
    "component": "adminprintaction"
  }
}
---

# AdminPrintAction

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# AdminPrintActionAsk assistant`s-admin-print-action` is a component used by admin print action extensions to denote a URL to print. Admin print action extensions require the use of this component.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/settings-and-templates/adminprintaction#properties)Properties[Anchor to src](/docs/api/admin-extensions/latest/polaris-web-components/settings-and-templates/adminprintaction#properties-propertydetail-src)src**src**string**string**Sets the src URL of the preview and the document to print. If not provided, the preview will show an empty state and the print button will be disabled. HTML, PDFs and images are supported.

ExamplesExample## jsx Copy9123456789import '@shopify/ui-extensions/preact';import {render} from 'preact';export default async () => {  render(    <s-admin-print-action src="https://example.com"></s-admin-print-action>,    document.body,  );}## Preview### Examples- #### jsx```

import '@shopify/ui-extensions/preact';

import {render} from 'preact';

export default async () => {

render(

<s-admin-print-action src="https://example.com"></s-admin-print-action>,

document.body,

);

}

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)