---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminprintaction",
    "fetched_at": "2026-02-10T13:29:06.928483",
    "status": 200,
    "size_bytes": 235511
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

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# AdminPrintActionAsk assistantAdminPrintAction is a component used by admin print action extensions to denote a URL to print. Admin print action extensions require the use of this component.

## [Anchor to adminprintactionprops](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminprintaction#adminprintactionprops)AdminPrintActionProps[Anchor to src](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminprintaction#adminprintactionprops-propertydetail-src)src**src**string**string**Sets the src URL of the preview and the document to print. If not provided, the preview will show an empty state and the print button will be disabled. HTML, PDFs and images are supported.

ExamplesSet the source URL of the print action extension.ReactJSCopy9912345678910111213141516171819import React from 'react';import {  reactExtension,  AdminPrintAction,  Text,} from '@shopify/ui-extensions-react/admin';function App() {  return (    <AdminPrintAction src="https://example.com">      <Text>Modal content</Text>    </AdminPrintAction>  );}export default reactExtension(  'Playground',  () => <App />,);## Preview### Examples- #### Set the source URL of the print action extension.React```

import React from 'react';

import {

reactExtension,

AdminPrintAction,

Text,

} from '@shopify/ui-extensions-react/admin';

function App() {

return (

<AdminPrintAction src="https://example.com">

<Text>Modal content</Text>

</AdminPrintAction>

);

}

export default reactExtension(

'Playground',

() => <App />,

);

```JS```

import {extension, AdminPrintAction, Text} from '@shopify/ui-extensions/admin';

export default extension('Playground', (root) => {

const adminPrintAction = root.createComponent(

AdminPrintAction,

{

src: 'https://example.com',

},

root.createComponent(Text, {fontWeight: 'bold'}, 'Modal content'),

);

root.append(adminPrintAction);

root.mount();

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminprintaction#related)Related[AdminActionAdminAction](/docs/api/admin-extensions/components/other/adminaction)[ - AdminAction](/docs/api/admin-extensions/components/other/adminaction)[AdminBlockAdminBlock](/docs/api/admin-extensions/components/other/adminblock)[ - AdminBlock](/docs/api/admin-extensions/components/other/adminblock)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)