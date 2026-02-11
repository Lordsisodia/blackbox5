---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/heading",
    "fetched_at": "2026-02-10T13:29:09.603577",
    "status": 200,
    "size_bytes": 233676
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

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# HeadingAsk assistantUse this to display a title. It's similar to the h1-h6 tags in HTML

## [Anchor to headingprops](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/heading#headingprops)HeadingProps[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/heading#headingprops-propertydetail-id)id**id**string**string**A unique identifier for the field.

[Anchor to size](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/heading#headingprops-propertydetail-size)size**size**LevelLevel**LevelLevel**The visual size of the heading.

There are no guarantee that the level set will render the same level in the HTML `<h*>` element. The heading level that gets rendered is determined by the parent `HeadingGroup` or `Section` component.

### Level```

1 | 2 | 3 | 4 | 5 | 6

```ExamplesSimple Heading exampleReactJSCopy91234567import {render, Heading} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  return <Heading>Store name</Heading>;}## Preview### Examples- #### Simple Heading exampleReact```

import {render, Heading} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return <Heading>Store name</Heading>;

}

```JS```

import {extend, Heading} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const heading = root.createComponent(Heading, undefined, 'Headings are cool');

root.appendChild(heading);

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/heading#related)Related[TextText](/docs/api/admin-extensions/components/titles-and-text/text)[ - Text](/docs/api/admin-extensions/components/titles-and-text/text)[HeadingGroupHeadingGroup](/docs/api/admin-extensions/components/titles-and-text/headinggroup)[ - HeadingGroup](/docs/api/admin-extensions/components/titles-and-text/headinggroup)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)