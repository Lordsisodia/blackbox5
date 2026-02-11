---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/text",
    "fetched_at": "2026-02-10T13:29:13.006035",
    "status": 200,
    "size_bytes": 243250
  },
  "metadata": {
    "title": "Text",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "typography-and-content",
    "component": "text"
  }
}
---

# Text

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# TextAsk assistantThis component renders text. Remember, you can also add your own styling.

## [Anchor to textprops](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/text#textprops)TextProps[Anchor to accessibilityRole](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/text#textprops-propertydetail-accessibilityrole)accessibilityRole**accessibilityRole**TextAccessibilityRoleTextAccessibilityRole**TextAccessibilityRoleTextAccessibilityRole**Provide semantic meaning to content and improve support for assistive technologies.

[Anchor to fontStyle](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/text#textprops-propertydetail-fontstyle)fontStyle**fontStyle**FontStyleFontStyle**FontStyleFontStyle**Use to emphasize a word or a group of words.

[Anchor to fontVariant](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/text#textprops-propertydetail-fontvariant)fontVariant**fontVariant**FontVariantOptionsFontVariantOptions | FontVariantOptionsFontVariantOptions[]**FontVariantOptionsFontVariantOptions | FontVariantOptionsFontVariantOptions[]**Set all the variants for a font with a shorthand property.

[Anchor to fontWeight](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/text#textprops-propertydetail-fontweight)fontWeight**fontWeight**FontWeightFontWeight**FontWeightFontWeight**Sets the weight (or boldness) of the font.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/text#textprops-propertydetail-id)id**id**string**string**A unique identifier for the field.

[Anchor to textOverflow](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/text#textprops-propertydetail-textoverflow)textOverflow**textOverflow**TextOverflowTextOverflow**TextOverflowTextOverflow**Set how hidden overflow content is signaled to users.

### TextAccessibilityRole```

'address' | 'deletion' | 'mark' | 'emphasis' | 'offset' | 'strong'

```### FontStyle```

'italic' | 'normal'

```### FontVariantOptions```

'numeric' | 'all-small-caps' | 'none'

```### FontWeight```

'light-300' | 'light-200' | 'light-100' | 'light' | 'base' | 'normal' | 'bold' | 'bold-100' | 'bold-200' | 'bold-300'

```### TextOverflow```

'ellipsis'

```ExamplesSimple Text exampleReactJSCopy99123456789101112import {render, Text, BlockStack} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  return (    <BlockStack inlineAlignment="center" gap>      <Text fontWeight="bold">Name:</Text>      <Text>Jane Doe</Text>    </BlockStack>  );}## Preview### Examples- #### Simple Text exampleReact```

import {render, Text, BlockStack} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<BlockStack inlineAlignment="center" gap>

<Text fontWeight="bold">Name:</Text>

<Text>Jane Doe</Text>

</BlockStack>

);

}

```JS```

import {extend, Text, BlockStack} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const text = root.createComponent(BlockStack, {inlineAlignment: 'center', gap: true}, [

root.createComponent(Text, {fontWeight: 'bold'}, 'Name:'),

root.createComponent(Text, {}, 'Jane Doe'),

]);

root.appendChild(text);

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/typography-and-content/text#related)Related[HeadingHeading](/docs/api/admin-extensions/components/titles-and-text/heading)[ - Heading](/docs/api/admin-extensions/components/titles-and-text/heading)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)