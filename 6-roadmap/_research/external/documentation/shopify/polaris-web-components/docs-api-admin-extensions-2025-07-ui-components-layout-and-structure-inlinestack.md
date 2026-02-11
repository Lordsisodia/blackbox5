---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack",
    "fetched_at": "2026-02-10T13:28:57.557859",
    "status": 200,
    "size_bytes": 277738
  },
  "metadata": {
    "title": "InlineStack",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "layout-and-structure",
    "component": "inlinestack"
  }
}
---

# InlineStack

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# InlineStackAsk assistantUse this to organize layout elements along the horizontal axis of the page. It's great for horizontal alignment.

## [Anchor to inlinestackprops](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops)InlineStackProps[Anchor to accessibilityLabel](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the element. When set, it will be announced to users using assistive technologies and will provide them with more context. When set, any children or `label` supplied will not be announced to screen readers.

[Anchor to accessibilityRole](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-accessibilityrole)accessibilityRole**accessibilityRole**AccessibilityRoleAccessibilityRole**AccessibilityRoleAccessibilityRole**Default: 'generic'**Default: 'generic'**Sets the semantic meaning of the component’s content. When set, the role will be used by assistive technologies to help users navigate the page.

[Anchor to blockAlignment](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-blockalignment)blockAlignment**blockAlignment**CrossAxisAlignmentCrossAxisAlignment**CrossAxisAlignmentCrossAxisAlignment**Default: 'start'**Default: 'start'**Position children along the cross axis

[Anchor to blockGap](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-blockgap)blockGap**blockGap**SpacingKeywordSpacingKeyword | boolean**SpacingKeywordSpacingKeyword | boolean**Adjust spacing between elements in the block axis.

Alias for `rowGap`

[Anchor to blockSize](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-blocksize)blockSize**blockSize**number | `${number}%`**number | `${number}%`**Adjust the block size.

- `number`: size in pixels.

- ``${number}%``: size in percentages of the available space.

[Anchor to columnGap](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-columngap)columnGap**columnGap**SpacingKeywordSpacingKeyword | boolean**SpacingKeywordSpacingKeyword | boolean**Adjust spacing between children in the inline axis

[Anchor to gap](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-gap)gap**gap**MaybeTwoBoxEdgesShorthandPropertyMaybeTwoBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**MaybeTwoBoxEdgesShorthandPropertyMaybeTwoBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**Adjust spacing between children

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to inlineAlignment](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-inlinealignment)inlineAlignment**inlineAlignment**MainAxisAlignmentMainAxisAlignment**MainAxisAlignmentMainAxisAlignment**Default: 'start'**Default: 'start'**Position children along the main axis

[Anchor to inlineGap](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-inlinegap)inlineGap**inlineGap**SpacingKeywordSpacingKeyword | boolean**SpacingKeywordSpacingKeyword | boolean**Adjust spacing between elements in the inline axis.

Alias for `columnGap`

[Anchor to inlineSize](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-inlinesize)inlineSize**inlineSize**number | `${number}%`**number | `${number}%`**Adjust the inline size.

- `number`: size in pixels.

- ``${number}%``: size in percentages of the available space.

[Anchor to maxBlockSize](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-maxblocksize)maxBlockSize**maxBlockSize**number | `${number}%`**number | `${number}%`**Adjust the maximum block size.

- `number`: size in pixels.

- ``${number}%``: size in percentages of the available space.

[Anchor to maxInlineSize](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-maxinlinesize)maxInlineSize**maxInlineSize**number | `${number}%`**number | `${number}%`**Adjust the maximum inline size.

- `number`: size in pixels.

- ``${number}%``: size in percentages of the available space.

[Anchor to minBlockSize](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-minblocksize)minBlockSize**minBlockSize**number | `${number}%`**number | `${number}%`**Adjust the minimum block size.

- `number`: size in pixels.

- ``${number}%``: size in percentages of the available space.

[Anchor to minInlineSize](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-mininlinesize)minInlineSize**minInlineSize**number | `${number}%`**number | `${number}%`**Adjust the minimum inline size.

- `number`: size in pixels.

- ``${number}%``: size in percentages of the available space.

[Anchor to padding](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-padding)padding**padding**MaybeAllBoxEdgesShorthandPropertyMaybeAllBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**MaybeAllBoxEdgesShorthandPropertyMaybeAllBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**Adjust the padding.

To shorten the code, it is possible to specify all the padding for all edges of the box in one property.

- `base` means block-start, inline-end, block-end and inline-start paddings are `base`.

- `base none` means block-start and block-end paddings are `base`, inline-start and inline-end paddings are `none`.

- `base none large` means block-start padding is `base`, inline-end padding is `none`, block-end padding is `large` and inline-start padding is `none`.

- `base none large small` means block-start padding is `base`, inline-end padding is `none`, block-end padding is `large` and inline-start padding is `small`.

- `true` applies a default padding that is appropriate for the component.

Learn more about the 1-to-4-value syntax at [https://developer.mozilla.org/en-US/docs/Web/CSS/Shorthand_properties#edges_of_a_box](https://developer.mozilla.org/en-US/docs/Web/CSS/Shorthand_properties#edges_of_a_box)

[Anchor to paddingBlock](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-paddingblock)paddingBlock**paddingBlock**MaybeTwoBoxEdgesShorthandPropertyMaybeTwoBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**MaybeTwoBoxEdgesShorthandPropertyMaybeTwoBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**Adjust the block-padding.

- `base none` means block-start padding is `base`, block-end padding is `none`.

[Anchor to paddingBlockEnd](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-paddingblockend)paddingBlockEnd**paddingBlockEnd**SpacingKeywordSpacingKeyword | boolean**SpacingKeywordSpacingKeyword | boolean**Adjust the block-end padding.

[Anchor to paddingBlockStart](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-paddingblockstart)paddingBlockStart**paddingBlockStart**SpacingKeywordSpacingKeyword | boolean**SpacingKeywordSpacingKeyword | boolean**Adjust the block-start padding.

[Anchor to paddingInline](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-paddinginline)paddingInline**paddingInline**MaybeTwoBoxEdgesShorthandPropertyMaybeTwoBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**MaybeTwoBoxEdgesShorthandPropertyMaybeTwoBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**Adjust the inline padding.

- `base none` means inline-start padding is `base`, inline-end padding is `none`.

[Anchor to paddingInlineEnd](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-paddinginlineend)paddingInlineEnd**paddingInlineEnd**SpacingKeywordSpacingKeyword | boolean**SpacingKeywordSpacingKeyword | boolean**Adjust the inline-end padding.

[Anchor to paddingInlineStart](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-paddinginlinestart)paddingInlineStart**paddingInlineStart**SpacingKeywordSpacingKeyword | boolean**SpacingKeywordSpacingKeyword | boolean**Adjust the inline-start padding.

[Anchor to rowGap](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#inlinestackprops-propertydetail-rowgap)rowGap**rowGap**SpacingKeywordSpacingKeyword | boolean**SpacingKeywordSpacingKeyword | boolean**Adjust spacing between children in the block axis

### AccessibilityRole```

'main' | 'header' | 'footer' | 'section' | 'aside' | 'navigation' | 'ordered-list' | 'list-item' | 'list-item-separator' | 'unordered-list' | 'separator' | 'status' | 'alert' | 'generic'

```### CrossAxisAlignment```

'start' | 'center' | 'end' | 'baseline'

```### SpacingKeyword```

'none' | 'small' | 'base' | 'large'

```### MaybeTwoBoxEdgesShorthandProperty```

T | `${T} ${T}`

```### MainAxisAlignment```

'start' | 'center' | 'end' | 'space-between' | 'space-around' | 'space-evenly'

```### MaybeAllBoxEdgesShorthandProperty```

T | `${T} ${T}` | `${T} ${T} ${T}` | `${T} ${T} ${T} ${T}`

```ExamplesLaying out elements in a rowReactJSCopy99123456789101112131415161718import React from 'react';import {  render,  InlineStack,} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  return (    <InlineStack gap>      <>Child 1</>      <>Child 2</>      <>Child 3</>      <>Child 4</>    </InlineStack>  );}## Preview### Examples- #### Laying out elements in a rowReact```

import React from 'react';

import {

render,

InlineStack,

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<InlineStack gap>

<>Child 1</>

<>Child 2</>

<>Child 3</>

<>Child 4</>

</InlineStack>

);

}

```JS```

import {extension, InlineStack} from '@shopify/ui-extensions/admin';

export default extension('Playground', (root) => {

const inlineStack = root.createComponent(

InlineStack,

{

gap: true,

},

[

root.createText('Child 1'),

root.createText('Child 2'),

root.createText('Child 3'),

root.createText('Child 4'),

],

);

root.appendChild(inlineStack);

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/layout-and-structure/inlinestack#related)Related[BlockStackBlockStack](/docs/api/admin-extensions/components/structure/BlockStack)[ - BlockStack](/docs/api/admin-extensions/components/structure/BlockStack)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)