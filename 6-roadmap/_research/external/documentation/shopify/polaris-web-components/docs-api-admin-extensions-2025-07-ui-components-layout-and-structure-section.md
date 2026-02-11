---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/section",
    "fetched_at": "2026-02-10T13:28:58.767364",
    "status": 200,
    "size_bytes": 237716
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

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# SectionAsk assistant`Section` is a structural component that allows thematic grouping of content. Its visual style is contextual and controlled by Shopify, so a `Section` may look different depending on the component it is nested inside.

`Section` also automatically increases the heading level for its content to ensure a semantically correct heading structure in the document. To further increase the heading level inside the `Section`, consider nesting new `Section`s.

## [Anchor to sectionprops](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/section#sectionprops)SectionProps[Anchor to accessibilityLabel](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/section#sectionprops-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label used to describe the section that will be announced by assistive technologies.

When no `heading` property is provided or included as a children of the Section, you **must** provide an `accessibilityLabel` to describe the Section. This is important as it allows assistive technologies to provide the right context to users.

[Anchor to heading](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/section#sectionprops-propertydetail-heading)heading**heading**string**string**A title that describes the content of the section.

[Anchor to padding](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/section#sectionprops-propertydetail-padding)padding**padding**'base' | 'none'**'base' | 'none'**Default: "base"**Default: "base"**Adjust the padding of all edges.

`base`: applies padding that is appropriate for the element. Note that it may result in no padding if Shopify believes this is the right design decision in a particular context.

`none`: removes all padding from the element. This can be useful when elements inside the Section need to span to the edge of the Section. For example, a full-width image. In this case, rely on `Box` or any other layout element to bring back the desired padding for the rest of the content.

ExamplesSection to an app pageReactJSCopy9912345678910111213141516import React from 'react';import {  render,  Section,} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  return (    <Section heading="Section heading">      Section content    </Section>  );}## Preview### Examples- #### Section to an app pageReact```

import React from 'react';

import {

render,

Section,

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<Section heading="Section heading">

Section content

</Section>

);

}

```JS```

import {

extend,

Section,

} from '@shopify/ui-extensions/admin';

export default extend(

'Playground',

(root) => {

const section = root.createComponent(

Section,

{

heading: 'Section heading',

},

'Section content'

);

root.appendChild(section);

},

);

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)