---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/paragraph",
    "fetched_at": "2026-02-10T13:29:11.858546",
    "status": 200,
    "size_bytes": 241690
  },
  "metadata": {
    "title": "Paragraph",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "typography-and-content",
    "component": "paragraph"
  }
}
---

# Paragraph

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# ParagraphAsk assistantUse this to display a block of text similar to the `<p>` tag in HTML.

## [Anchor to paragraphprops](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/paragraph#paragraphprops)ParagraphProps[Anchor to children](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/paragraph#paragraphprops-propertydetail-children)children**children**any**any**[Anchor to fontSize](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/paragraph#paragraphprops-propertydetail-fontsize)fontSize**fontSize**SizeScaleSizeScale**SizeScaleSizeScale**Size of the typography's font.

[Anchor to fontStyle](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/paragraph#paragraphprops-propertydetail-fontstyle)fontStyle**fontStyle**FontStyleFontStyle**FontStyleFontStyle**Use to emphasize a word or a group of words.

[Anchor to fontWeight](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/paragraph#paragraphprops-propertydetail-fontweight)fontWeight**fontWeight**FontWeightFontWeight**FontWeightFontWeight**Sets the weight of the font.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/paragraph#paragraphprops-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to textOverflow](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/paragraph#paragraphprops-propertydetail-textoverflow)textOverflow**textOverflow**TextOverflowTextOverflow**TextOverflowTextOverflow**Set how hidden overflow content is signaled to users.

### SizeScale```

'small-300' | 'small-200' | 'small-100' | 'base' | 'large-100' | 'large-200' | 'large-300'

```### FontStyle```

'italic' | 'normal'

```### FontWeight```

'light-300' | 'light-200' | 'light-100' | 'light' | 'base' | 'normal' | 'bold' | 'bold-100' | 'bold-200' | 'bold-300'

```### TextOverflow```

'ellipsis'

```ExamplesSimple Paragraph exampleReactJSCopy9912345678910111213141516import {    render,    BlockStack,    Paragraph,} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {    return (        <BlockStack inlineAlignment='center' gap>            <Paragraph fontWeight='bold'>Name:</Paragraph>            <Paragraph>Jane Doe</Paragraph>        </BlockStack>    )}## Preview### Examples- #### Simple Paragraph exampleReact```

import {

render,

BlockStack,

Paragraph,

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<BlockStack inlineAlignment='center' gap>

<Paragraph fontWeight='bold'>Name:</Paragraph>

<Paragraph>Jane Doe</Paragraph>

</BlockStack>

)

}

```JS```

import {extend, Paragraph, BlockStack} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const paragraph = root.createComponent(BlockStack, {inlineAlignment: 'center', gap: true}, [

root.createComponent(Paragraph, {fontWeight: 'bold'}, 'Name:'),

root.createComponent(Paragraph, {}, 'Jane Doe'),

]);

root.appendChild(paragraph);

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/paragraph#related)Related[HeadingHeading](/docs/api/admin-extensions/components/titles-and-text/heading)[ - Heading](/docs/api/admin-extensions/components/titles-and-text/heading)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)