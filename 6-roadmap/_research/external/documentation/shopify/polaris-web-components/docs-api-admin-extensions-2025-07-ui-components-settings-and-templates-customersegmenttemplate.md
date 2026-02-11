---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/customersegmenttemplate",
    "fetched_at": "2026-02-10T13:29:08.126238",
    "status": 200,
    "size_bytes": 243239
  },
  "metadata": {
    "title": "CustomerSegmentTemplate",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "settings-and-templates",
    "component": "customersegmenttemplate"
  }
}
---

# CustomerSegmentTemplate

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# CustomerSegmentTemplateAsk assistantRequires use of the [admin.customers.segmentation-templates.render](/docs/api/admin-extensions/api/extension-targets#extensiontargets-propertydetail-admincustomerssegmentationtemplatesrender) target.**Requires use of the [admin.customers.segmentation-templates.render](/docs/api/admin-extensions/api/extension-targets#extensiontargets-propertydetail-admincustomerssegmentationtemplatesrender) target.:**CustomerSegmentTemplate is used to configure a template rendered in the **Customers** section of the Shopify admin. Templates can be applied in the [customer segment editor](https://help.shopify.com/en/manual/customers/customer-segmentation/customer-segments) and used to create segments.

## [Anchor to customersegmenttemplateprops](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/customersegmenttemplate#customersegmenttemplateprops)CustomerSegmentTemplateProps[Anchor to description](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/customersegmenttemplate#customersegmenttemplateprops-propertydetail-description)description**description**string | string[]**string | string[]**required**required**The localized description of the template. An array can be used for multiple paragraphs.

[Anchor to query](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/customersegmenttemplate#customersegmenttemplateprops-propertydetail-query)query**query**string**string**required**required**The code snippet to render in the template with syntax highlighting. The `query` is not validated in the template.

[Anchor to title](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/customersegmenttemplate#customersegmenttemplateprops-propertydetail-title)title**title**string**string**required**required**The localized title of the template.

[Anchor to createdOn](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/customersegmenttemplate#customersegmenttemplateprops-propertydetail-createdon)createdOn**createdOn**string**string**ISO 8601-encoded date and time string. A "New" badge will be rendered for templates introduced in the last month.

[Anchor to dependencies](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/customersegmenttemplate#customersegmenttemplateprops-propertydetail-dependencies)dependencies**dependencies**{ standardMetafields?: "facts.birth_date"[]; customMetafields?: string[]; }**{ standardMetafields?: "facts.birth_date"[]; customMetafields?: string[]; }**The list of customer standard metafields or custom metafields used in the template's query.

[Anchor to queryToInsert](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/customersegmenttemplate#customersegmenttemplateprops-propertydetail-querytoinsert)queryToInsert**queryToInsert**string**string**The code snippet to insert in the segment editor. If missing, `query` will be used. The `queryToInsert` is not validated in the template.

ExamplesSimple CustomerSegmentTemplate implementationReactJSCopy99123456789101112131415import React from 'react';import {reactExtension, CustomerSegmentTemplate} from '@shopify/ui-extensions/admin';function App() {  return (    <CustomerSegmentTemplate        title="My Customer Segment Template"        description="Description of the segment"        query="number_of_orders > 0"        createdOn={new Date('2023-01-15').toISOString()}    />  );}export default reactExtension('Playground', () => <App />);## Preview### Examples- #### Simple CustomerSegmentTemplate implementationReact```

import React from 'react';

import {reactExtension, CustomerSegmentTemplate} from '@shopify/ui-extensions/admin';

function App() {

return (

<CustomerSegmentTemplate

title="My Customer Segment Template"

description="Description of the segment"

query="number_of_orders > 0"

createdOn={new Date('2023-01-15').toISOString()}

/>

);

}

export default reactExtension('Playground', () => <App />);

```JS```

import {extension, CustomerSegmentTemplate} from '@shopify/ui-extensions/admin';

export default extension(

'admin.customers.segmentation-templates.render',

(root, {i18n}) => {

const template = root.createComponent(CustomerSegmentTemplate, {

title: i18n.translate('template.title'),

description: i18n.translate('template.description'),

query: "number_of_orders > 0'",

createdOn: new Date('2023-01-15').toISOString(),

});

root.appendChild(template);

root.mount();

},

);

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)