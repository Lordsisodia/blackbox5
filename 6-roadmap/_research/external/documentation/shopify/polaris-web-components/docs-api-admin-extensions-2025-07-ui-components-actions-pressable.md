---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/actions/pressable",
    "fetched_at": "2026-02-10T13:28:27.130132",
    "status": 200,
    "size_bytes": 279066
  },
  "metadata": {
    "title": "Pressable",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "actions",
    "component": "pressable"
  }
}
---

# Pressable

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# PressableAsk assistantUse this component when you need to capture click or press events on its child elements without adding any additional visual styling. It subtly enhances user interaction by changing the cursor when hovering over the child elements, providing a clear indication of interactivity.

## [Anchor to pressableprops](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops)PressableProps[Anchor to accessibilityLabel](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the element. When set, it will be announced to users using assistive technologies and will provide them with more context. When set, any children or `label` supplied will not be announced to screen readers.

[Anchor to accessibilityRole](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-accessibilityrole)accessibilityRole**accessibilityRole**AccessibilityRoleAccessibilityRole**AccessibilityRoleAccessibilityRole**Default: 'generic'**Default: 'generic'**Sets the semantic meaning of the component’s content. When set, the role will be used by assistive technologies to help users navigate the page.

[Anchor to blockSize](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-blocksize)blockSize**blockSize**number | `${number}%`**number | `${number}%`**Adjust the block size.

- `number`: size in pixels.

- ``${number}%``: size in percentages of the available space.

[Anchor to display](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-display)display**display**'auto' | 'none'**'auto' | 'none'**Default: 'auto'**Default: 'auto'**The display property sets the display behavior of an element.

[Anchor to href](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-href)href**href**string**string**The URL to link to. If set, it will navigate to the location specified by `href` after executing the `onClick` callback.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-id)id**id**string**string**A unique identifier for the link.

[Anchor to inlineSize](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-inlinesize)inlineSize**inlineSize**number | `${number}%`**number | `${number}%`**Adjust the inline size.

- `number`: size in pixels.

- ``${number}%``: size in percentages of the available space.

[Anchor to lang](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-lang)lang**lang**string**string**Alias for `language`

[Anchor to language](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-language)language**language**string**string**Indicate the text language. Useful when the text is in a different language than the rest of the page. It will allow assistive technologies such as screen readers to invoke the correct pronunciation. [Reference of values](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) ("subtag" label)

[Anchor to maxBlockSize](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-maxblocksize)maxBlockSize**maxBlockSize**number | `${number}%`**number | `${number}%`**Adjust the maximum block size.

- `number`: size in pixels.

- ``${number}%``: size in percentages of the available space.

[Anchor to maxInlineSize](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-maxinlinesize)maxInlineSize**maxInlineSize**number | `${number}%`**number | `${number}%`**Adjust the maximum inline size.

- `number`: size in pixels.

- ``${number}%``: size in percentages of the available space.

[Anchor to minBlockSize](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-minblocksize)minBlockSize**minBlockSize**number | `${number}%`**number | `${number}%`**Adjust the minimum block size.

- `number`: size in pixels.

- ``${number}%``: size in percentages of the available space.

[Anchor to minInlineSize](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-mininlinesize)minInlineSize**minInlineSize**number | `${number}%`**number | `${number}%`**Adjust the minimum inline size.

- `number`: size in pixels.

- ``${number}%``: size in percentages of the available space.

[Anchor to onClick](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-onclick)onClick**onClick**() => void**() => void**Callback when a link is pressed. If `href` is set, it will execute the callback and then navigate to the location specified by `href`.

[Anchor to onPress](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-onpress)onPress**onPress**() => void**() => void**Alias for `onClick` Callback when a link is pressed. If `href` is set, it will execute the callback and then navigate to the location specified by `href`.

[Anchor to padding](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-padding)padding**padding**MaybeAllBoxEdgesShorthandPropertyMaybeAllBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**MaybeAllBoxEdgesShorthandPropertyMaybeAllBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**Adjust the padding.

To shorten the code, it is possible to specify all the padding for all edges of the box in one property.

- `base` means block-start, inline-end, block-end and inline-start paddings are `base`.

- `base none` means block-start and block-end paddings are `base`, inline-start and inline-end paddings are `none`.

- `base none large` means block-start padding is `base`, inline-end padding is `none`, block-end padding is `large` and inline-start padding is `none`.

- `base none large small` means block-start padding is `base`, inline-end padding is `none`, block-end padding is `large` and inline-start padding is `small`.

- `true` applies a default padding that is appropriate for the component.

Learn more about the 1-to-4-value syntax at [https://developer.mozilla.org/en-US/docs/Web/CSS/Shorthand_properties#edges_of_a_box](https://developer.mozilla.org/en-US/docs/Web/CSS/Shorthand_properties#edges_of_a_box)

[Anchor to paddingBlock](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-paddingblock)paddingBlock**paddingBlock**MaybeTwoBoxEdgesShorthandPropertyMaybeTwoBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**MaybeTwoBoxEdgesShorthandPropertyMaybeTwoBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**Adjust the block-padding.

- `base none` means block-start padding is `base`, block-end padding is `none`.

[Anchor to paddingBlockEnd](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-paddingblockend)paddingBlockEnd**paddingBlockEnd**SpacingKeywordSpacingKeyword | boolean**SpacingKeywordSpacingKeyword | boolean**Adjust the block-end padding.

[Anchor to paddingBlockStart](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-paddingblockstart)paddingBlockStart**paddingBlockStart**SpacingKeywordSpacingKeyword | boolean**SpacingKeywordSpacingKeyword | boolean**Adjust the block-start padding.

[Anchor to paddingInline](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-paddinginline)paddingInline**paddingInline**MaybeTwoBoxEdgesShorthandPropertyMaybeTwoBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**MaybeTwoBoxEdgesShorthandPropertyMaybeTwoBoxEdgesShorthandProperty<SpacingKeywordSpacingKeyword | boolean>**Adjust the inline padding.

- `base none` means inline-start padding is `base`, inline-end padding is `none`.

[Anchor to paddingInlineEnd](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-paddinginlineend)paddingInlineEnd**paddingInlineEnd**SpacingKeywordSpacingKeyword | boolean**SpacingKeywordSpacingKeyword | boolean**Adjust the inline-end padding.

[Anchor to paddingInlineStart](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-paddinginlinestart)paddingInlineStart**paddingInlineStart**SpacingKeywordSpacingKeyword | boolean**SpacingKeywordSpacingKeyword | boolean**Adjust the inline-start padding.

[Anchor to target](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-target)target**target**'_blank' | '_self'**'_blank' | '_self'**Default: '_self'**Default: '_self'**Specifies where to display the linked URL

[Anchor to to](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-to)to**to**string**string**Alias for `href` If set, it will navigate to the location specified by `to` after executing the `onClick` callback.

[Anchor to tone](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#pressableprops-propertydetail-tone)tone**tone**'default' | 'inherit' | 'critical'**'default' | 'inherit' | 'critical'**Sets the link color.

- `inherit` will take the color value from its parent, giving the link a monochrome appearance. In some cases, its important to pair this property with another stylistic treatment, like an underline, to differentiate the link from a normal text.

### AccessibilityRole```

'main' | 'header' | 'footer' | 'section' | 'aside' | 'navigation' | 'ordered-list' | 'list-item' | 'list-item-separator' | 'unordered-list' | 'separator' | 'status' | 'alert' | 'generic'

```### MaybeAllBoxEdgesShorthandProperty```

T | `${T} ${T}` | `${T} ${T} ${T}` | `${T} ${T} ${T} ${T}`

```### SpacingKeyword```

'none' | 'small' | 'base' | 'large'

```### MaybeTwoBoxEdgesShorthandProperty```

T | `${T} ${T}`

```ExamplesSimple pressable exampleReactJSCopy991234567891011121314151617181920import {  reactExtension,  Icon,  InlineStack,  Pressable,  Text,} from '@shopify/ui-extensions-react/admin';reactExtension('Playground', () => <Extension />);function Extension() {  return (    <Pressable padding="base">      <InlineStack>        <Text>Go to Apps Dashboard</Text>        <Icon name="AppsMajor" />      </InlineStack>    </Pressable>  );}## Preview### Examples- #### Simple pressable exampleReact```

import {

reactExtension,

Icon,

InlineStack,

Pressable,

Text,

} from '@shopify/ui-extensions-react/admin';

reactExtension('Playground', () => <Extension />);

function Extension() {

return (

<Pressable padding="base">

<InlineStack>

<Text>Go to Apps Dashboard</Text>

<Icon name="AppsMajor" />

</InlineStack>

</Pressable>

);

}

```JS```

import {

extension,

Icon,

InlineStack,

Pressable,

Text,

} from '@shopify/ui-extensions/admin';

extension('Playground', (root) => {

const pressable = root.createComponent(

Pressable,

{

padding: 'base',

onPress: () => console.log('onPress event'),

},

[

root.createComponent(InlineStack, {}, [

root.createComponent(Text, {}, 'Go to App Dashboard'),

root.createComponent(Icon, {name: 'AppsMajor'}),

]),

],

);

root.appendChild(pressable);

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/actions/pressable#related)Related[ButtonButton](/docs/api/admin-extensions/components/actions/button)[ - Button](/docs/api/admin-extensions/components/actions/button)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)