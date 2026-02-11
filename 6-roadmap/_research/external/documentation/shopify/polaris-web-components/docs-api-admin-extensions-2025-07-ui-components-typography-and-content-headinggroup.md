---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/headinggroup",
    "fetched_at": "2026-02-10T13:29:10.733411",
    "status": 200,
    "size_bytes": 232806
  },
  "metadata": {
    "title": "HeadingGroup",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "typography-and-content",
    "component": "headinggroup"
  }
}
---

# HeadingGroup

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# HeadingGroupAsk assistantThis groups headings together, much like the hgroup element in HTML.

ExamplesSimple HeadingGroup exampleReactJSCopy991234567891011121314151617181920212223import {    render,    HeadingGroup,    Heading,  } from '@shopify/ui-extensions-react/admin';  render('Playground', () => <App />);  function App() {    return (      <>        <Heading>Heading <h1></Heading>        <HeadingGroup>          <Heading>Heading <h2></Heading>          <HeadingGroup>            <Heading>Heading <h3></Heading>          </HeadingGroup>        </HeadingGroup>      </>    );  }## Preview### Examples- #### Simple HeadingGroup exampleReact```

import {

render,

HeadingGroup,

Heading,

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<>

<Heading>Heading <h1></Heading>

<HeadingGroup>

<Heading>Heading <h2></Heading>

<HeadingGroup>

<Heading>Heading <h3></Heading>

</HeadingGroup>

</HeadingGroup>

</>

);

}

```JS```

import {

extend,

HeadingGroup,

Heading,

BlockStack,

} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const headingGroup = root.createComponent(BlockStack, undefined, [

root.createComponent(Heading, undefined, 'Heading <h1>'),

root.createComponent(HeadingGroup, undefined, [

root.createComponent(Heading, undefined, 'Heading <h2>'),

root.createComponent(HeadingGroup, undefined, [

root.createComponent(Heading, undefined, 'Heading <h3>'),

]),

]),

]);

root.appendChild(headingGroup);

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/headinggroup#related)Related[HeadingHeading](/docs/api/admin-extensions/components/titles-and-text/heading)[ - Heading](/docs/api/admin-extensions/components/titles-and-text/heading)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)