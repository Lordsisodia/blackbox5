---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminblock",
    "fetched_at": "2026-02-10T13:29:05.613040",
    "status": 200,
    "size_bytes": 234233
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

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# AdminBlockAsk assistantThis component is similar to the AdminBlock, providing a deeper integration with the container your UI is rendered into. However, this only applies to Block Extensions which render inline on a resource page.

## [Anchor to adminblockprops](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminblock#adminblockprops)AdminBlockProps[Anchor to collapsedSummary](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminblock#adminblockprops-propertydetail-collapsedsummary)collapsedSummary**collapsedSummary**string**string**The summary to display when the app block is collapsed. Summary longer than 30 characters will be truncated.

[Anchor to title](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminblock#adminblockprops-propertydetail-title)title**title**string**string**The title to display at the top of the app block. If not provided, the name of the extension will be used. Titles longer than 40 characters will be truncated.

ExamplesSimple AdminBlock implementationReactJSCopy99123456789101112import React from 'react';import {reactExtension, AdminBlock} from '@shopify/ui-extensions-react/admin';function App() {  return (    <AdminBlock title="My App Block">      Block content    </AdminBlock>  );}export default reactExtension('Playground', () => <App />);## Preview### Examples- #### Simple AdminBlock implementationReact```

import React from 'react';

import {reactExtension, AdminBlock} from '@shopify/ui-extensions-react/admin';

function App() {

return (

<AdminBlock title="My App Block">

Block content

</AdminBlock>

);

}

export default reactExtension('Playground', () => <App />);

```JS```

import {extension, AdminBlock, Button} from '@shopify/ui-extensions/admin';

export default extension('Playground', (root) => {

const adminBlock = root.createComponent(AdminBlock, {

title: 'My App Block',

}, '5 items active');

root.appendChild(adminBlock);

root.mount();

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminblock#related)Related[AdminactionAdminaction](/docs/api/admin-extensions/components/other/adminaction)[ - Adminaction](/docs/api/admin-extensions/components/other/adminaction)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)