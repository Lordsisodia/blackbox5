---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/layout-and-structure/stack",
    "fetched_at": "2026-02-10T13:30:36.562604",
    "status": 200,
    "size_bytes": 352713
  },
  "metadata": {
    "title": "Stack",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "layout-and-structure",
    "component": "stack"
  }
}
---

# Stack

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# StackAsk assistantOrganizes elements horizontally or vertically along the block or inline axis. Use to structure layouts, group related components, or control spacing between elements.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties)Properties[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the element. When set, it will be announced to users using assistive technologies and will provide them with more context.

Only use this when the element's content is not enough context for users using assistive technologies.

[Anchor to accessibilityRole](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-accessibilityrole)accessibilityRole**accessibilityRole**AccessibilityRoleAccessibilityRole**AccessibilityRoleAccessibilityRole**Default: 'generic'**Default: 'generic'**Sets the semantic meaning of the component’s content. When set, the role will be used by assistive technologies to help users navigate the page.

[Anchor to accessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-accessibilityvisibility)accessibilityVisibility**accessibilityVisibility**"visible" | "hidden" | "exclusive"**"visible" | "hidden" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the element.

- `visible`: the element is visible to all users.

- `hidden`: the element is removed from the accessibility tree but remains visible.

- `exclusive`: the element is visually hidden but remains in the accessibility tree.

[Anchor to alignContent](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-aligncontent)alignContent**alignContent**AlignContentKeywordAlignContentKeyword**AlignContentKeywordAlignContentKeyword**Default: 'normal'**Default: 'normal'**Aligns the Stack's children along the block axis.

This overrides the block value of `alignContent`.

[Anchor to alignItems](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-alignitems)alignItems**alignItems**AlignItemsKeywordAlignItemsKeyword**AlignItemsKeywordAlignItemsKeyword**Default: 'normal'**Default: 'normal'**Aligns the Stack's children along the block axis.

[Anchor to background](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-background)background**background**BackgroundColorKeywordBackgroundColorKeyword**BackgroundColorKeywordBackgroundColorKeyword**Default: 'transparent'**Default: 'transparent'**Adjust the background of the component.

[Anchor to blockSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-blocksize)blockSize**blockSize**SizeUnitsOrAutoSizeUnitsOrAuto**SizeUnitsOrAutoSizeUnitsOrAuto**Default: 'auto'**Default: 'auto'**Adjust the [block size](https://developer.mozilla.org/en-US/docs/Web/CSS/block-size).

[Anchor to border](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-border)border**border**BorderShorthandBorderShorthand**BorderShorthandBorderShorthand**Default: 'none' - equivalent to `none base auto`.**Default: 'none' - equivalent to `none base auto`.**Set the border via the shorthand property.

This can be a size, optionally followed by a color, optionally followed by a style.

If the color is not specified, it will be `base`.

If the style is not specified, it will be `auto`.

Values can be overridden by `borderWidth`, `borderStyle`, and `borderColor`.

[Anchor to borderColor](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-bordercolor)borderColor**borderColor**"" | ColorKeywordColorKeyword**"" | ColorKeywordColorKeyword**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the color of the border.

[Anchor to borderRadius](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-borderradius)borderRadius**borderRadius**MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderRadiiBoxBorderRadii>**MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderRadiiBoxBorderRadii>**Default: 'none'**Default: 'none'**Adjust the radius of the border.

[Anchor to borderStyle](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-borderstyle)borderStyle**borderStyle**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderStylesBoxBorderStyles>**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderStylesBoxBorderStyles>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the style of the border.

[Anchor to borderWidth](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-borderwidth)borderWidth**borderWidth**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<"small" | "small-100" | "base" | "large" | "large-100" | "none">**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<"small" | "small-100" | "base" | "large" | "large-100" | "none">**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the width of the border.

[Anchor to columnGap](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-columngap)columnGap**columnGap**MaybeResponsiveMaybeResponsive<"" | SpacingKeywordSpacingKeyword>**MaybeResponsiveMaybeResponsive<"" | SpacingKeywordSpacingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust spacing between elements in the inline axis.

This overrides the column value of `gap`. `columnGap` either accepts:

- a single [SpacingKeyword](/docs/api/app-home/using-polaris-components#scale) value (e.g. `large-100`)

- OR a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported SpacingKeyword as a query value.

[Anchor to direction](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-direction)direction**direction**MaybeResponsiveMaybeResponsive<"inline" | "block">**MaybeResponsiveMaybeResponsive<"inline" | "block">**Default: 'block'**Default: 'block'**Sets how the Stack's children are placed within the Stack.

`direction` either accepts:

- a single value either `inline` or `block`

- OR a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported SpacingKeyword as a query value.

[Anchor to display](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-display)display**display**MaybeResponsiveMaybeResponsive<"auto" | "none">**MaybeResponsiveMaybeResponsive<"auto" | "none">**Default: 'auto'**Default: 'auto'**Sets the outer [display](https://developer.mozilla.org/en-US/docs/Web/CSS/display) type of the component. The outer type sets a component's participation in [flow layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flow_layout).

- `auto` the component's initial value. The actual value depends on the component and context.

- `none` hides the component from display and removes it from the accessibility tree, making it invisible to screen readers.

[Anchor to gap](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-gap)gap**gap**MaybeResponsiveMaybeResponsive<MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<SpacingKeywordSpacingKeyword>>**MaybeResponsiveMaybeResponsive<MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<SpacingKeywordSpacingKeyword>>**Default: 'none'**Default: 'none'**Adjust spacing between elements.

`gap` can either accept:

- a single [SpacingKeyword](/docs/api/app-home/using-polaris-components#scale) value applied to both axes (e.g. `large-100`)

- OR a pair of values (eg `large-100 large-500`) can be used to set the inline and block axes respectively

- OR a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported SpacingKeyword as a query value.

[Anchor to inlineSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-inlinesize)inlineSize**inlineSize**SizeUnitsOrAutoSizeUnitsOrAuto**SizeUnitsOrAutoSizeUnitsOrAuto**Default: 'auto'**Default: 'auto'**Adjust the [inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/inline-size).

[Anchor to justifyContent](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-justifycontent)justifyContent**justifyContent**JustifyContentKeywordJustifyContentKeyword**JustifyContentKeywordJustifyContentKeyword**Default: 'normal'**Default: 'normal'**Aligns the Stack's children along the inline axis.

[Anchor to maxBlockSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-maxblocksize)maxBlockSize**maxBlockSize**SizeUnitsOrNoneSizeUnitsOrNone**SizeUnitsOrNoneSizeUnitsOrNone**Default: 'none'**Default: 'none'**Adjust the [maximum block size](https://developer.mozilla.org/en-US/docs/Web/CSS/max-block-size).

[Anchor to maxInlineSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-maxinlinesize)maxInlineSize**maxInlineSize**SizeUnitsOrNoneSizeUnitsOrNone**SizeUnitsOrNoneSizeUnitsOrNone**Default: 'none'**Default: 'none'**Adjust the [maximum inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/max-inline-size).

[Anchor to minBlockSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-minblocksize)minBlockSize**minBlockSize**SizeUnitsSizeUnits**SizeUnitsSizeUnits**Default: '0'**Default: '0'**Adjust the [minimum block size](https://developer.mozilla.org/en-US/docs/Web/CSS/min-block-size).

[Anchor to minInlineSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-mininlinesize)minInlineSize**minInlineSize**SizeUnitsSizeUnits**SizeUnitsSizeUnits**Default: '0'**Default: '0'**Adjust the [minimum inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/min-inline-size).

[Anchor to overflow](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-overflow)overflow**overflow**"visible" | "hidden"**"visible" | "hidden"**Default: 'visible'**Default: 'visible'**Sets the overflow behavior of the element.

- `hidden`: clips the content when it is larger than the element’s container. The element will not be scrollable and the users will not be able to access the clipped content by dragging or using a scroll wheel on a mouse.

- `visible`: the content that extends beyond the element’s container is visible.

[Anchor to padding](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-padding)padding**padding**MaybeResponsiveMaybeResponsive<MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: 'none'**Default: 'none'**Adjust the padding of all edges.

[1-to-4-value syntax](https://developer.mozilla.org/en-US/docs/Web/CSS/Shorthand_properties#edges_of_a_box) is supported. Note that, contrary to the CSS, it uses flow-relative values and the order is:

- 4 values: `block-start inline-end block-end inline-start`

- 3 values: `block-start inline block-end`

- 2 values: `block inline`

For example:

- `large` means block-start, inline-end, block-end and inline-start paddings are `large`.

- `large none` means block-start and block-end paddings are `large`, inline-start and inline-end paddings are `none`.

- `large none large` means block-start padding is `large`, inline-end padding is `none`, block-end padding is `large` and inline-start padding is `none`.

- `large none large small` means block-start padding is `large`, inline-end padding is `none`, block-end padding is `large` and inline-start padding is `small`.

A padding value of `auto` will use the default padding for the closest container that has had its usual padding removed.

`padding` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingBlock](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-paddingblock)paddingBlock**paddingBlock**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-padding.

- `large none` means block-start padding is `large`, block-end padding is `none`.

This overrides the block value of `padding`.

`paddingBlock` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingBlockEnd](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-paddingblockend)paddingBlockEnd**paddingBlockEnd**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-end padding.

This overrides the block-end value of `paddingBlock`.

`paddingBlockEnd` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingBlockStart](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-paddingblockstart)paddingBlockStart**paddingBlockStart**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-start padding.

This overrides the block-start value of `paddingBlock`.

`paddingBlockStart` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInline](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-paddinginline)paddingInline**paddingInline**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline padding.

- `large none` means inline-start padding is `large`, inline-end padding is `none`.

This overrides the inline value of `padding`.

`paddingInline` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInlineEnd](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-paddinginlineend)paddingInlineEnd**paddingInlineEnd**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline-end padding.

This overrides the inline-end value of `paddingInline`.

`paddingInlineEnd` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInlineStart](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-paddinginlinestart)paddingInlineStart**paddingInlineStart**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline-start padding.

This overrides the inline-start value of `paddingInline`.

`paddingInlineStart` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to rowGap](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#properties-propertydetail-rowgap)rowGap**rowGap**MaybeResponsiveMaybeResponsive<"" | SpacingKeywordSpacingKeyword>**MaybeResponsiveMaybeResponsive<"" | SpacingKeywordSpacingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust spacing between elements in the block axis.

This overrides the row value of `gap`. `rowGap` either accepts:

- a single [SpacingKeyword](/docs/api/app-home/using-polaris-components#scale) value (e.g. `large-100`)

- OR a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported SpacingKeyword as a query value.

### AccessibilityRole```

'main' | 'header' | 'footer' | 'section' | 'region' | 'aside' | 'navigation' | 'ordered-list' | 'list-item' | 'list-item-separator' | 'unordered-list' | 'separator' | 'status' | 'alert' | 'generic' | 'presentation' | 'none'

```### AlignContentKeywordAlign content sets the distribution of space between and around content items along a flexbox's cross axis, or a grid or block-level element's block axis.```

'normal' | BaselinePosition | ContentDistribution | OverflowPosition | ContentPosition

```### BaselinePosition```

'baseline' | 'first baseline' | 'last baseline'

```### ContentDistribution```

'space-between' | 'space-around' | 'space-evenly' | 'stretch'

```### OverflowPosition```

`unsafe ${ContentPosition}` | `safe ${ContentPosition}`

```### ContentPosition```

'center' | 'start' | 'end'

```### AlignItemsKeywordAlign items sets the align-self value on all direct children as a group.```

'normal' | 'stretch' | BaselinePosition | OverflowPosition | ContentPosition

```### BackgroundColorKeyword```

'transparent' | ColorKeyword

```### ColorKeyword```

'subdued' | 'base' | 'strong'

```### SizeUnitsOrAuto```

SizeUnits | 'auto'

```### SizeUnits```

`${number}px` | `${number}%` | `0`

```### BorderShorthandRepresents a shorthand for defining a border. It can be a combination of size, optionally followed by color, optionally followed by style.```

BorderSizeKeyword | `${BorderSizeKeyword} ${ColorKeyword}` | `${BorderSizeKeyword} ${ColorKeyword} ${BorderStyleKeyword}`

```### BorderSizeKeyword```

SizeKeyword | 'none'

```### SizeKeyword```

'small-500' | 'small-400' | 'small-300' | 'small-200' | 'small-100' | 'small' | 'base' | 'large' | 'large-100' | 'large-200' | 'large-300' | 'large-400' | 'large-500'

```### BorderStyleKeyword```

'none' | 'solid' | 'dashed' | 'dotted' | 'auto'

```### MaybeAllValuesShorthandProperty```

T | `${T} ${T}` | `${T} ${T} ${T}` | `${T} ${T} ${T} ${T}`

```### BoxBorderRadii```

'small' | 'small-200' | 'small-100' | 'base' | 'large' | 'large-100' | 'large-200' | 'none'

```### BoxBorderStyles```

'auto' | 'none' | 'solid' | 'dashed'

```### MaybeResponsive```

T | `@container${string}`

```### SpacingKeyword```

SizeKeyword | 'none'

```### MaybeTwoValuesShorthandProperty```

T | `${T} ${T}`

```### JustifyContentKeywordJustify content defines how the browser distributes space between and around content items along the main-axis of a flex container, and the inline axis of a grid container.```

'normal' | ContentDistribution | OverflowPosition | ContentPosition

```### SizeUnitsOrNone```

SizeUnits | 'none'

```### PaddingKeyword```

SizeKeyword | 'none'

```## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Stack.

ExamplesCodejsxhtmlCopy9123456<s-stack gap="base">  <s-badge>Paid</s-badge>  <s-badge>Processing</s-badge>  <s-badge>Filled</s-badge>  <s-badge>Completed</s-badge></s-stack>## Preview### Examples- #### Codejsx```

<s-stack gap="base">

<s-badge>Paid</s-badge>

<s-badge>Processing</s-badge>

<s-badge>Filled</s-badge>

<s-badge>Completed</s-badge>

</s-stack>

```html```

<s-stack gap="base">

<s-badge>Paid</s-badge>

<s-badge>Processing</s-badge>

<s-badge>Filled</s-badge>

<s-badge>Completed</s-badge>

</s-stack>

```- #### Basic block stack (vertical)DescriptionDefault vertical stacking layout with consistent spacing between text elements.jsx```

<s-stack gap="base">

<s-text>First item</s-text>

<s-text>Second item</s-text>

<s-text>Third item</s-text>

</s-stack>

```html```

<s-stack gap="base">

<s-text>First item</s-text>

<s-text>Second item</s-text>

<s-text>Third item</s-text>

</s-stack>

```- #### Inline stack (horizontal)DescriptionHorizontal layout for arranging badges or similar elements side by side.jsx```

<s-stack direction="inline" gap="large-100">

<s-badge>Item 1</s-badge>

<s-badge>Item 2</s-badge>

<s-badge>Item 3</s-badge>

</s-stack>

```html```

<s-stack direction="inline" gap="large-100">

<s-badge>Item 1</s-badge>

<s-badge>Item 2</s-badge>

<s-badge>Item 3</s-badge>

</s-stack>

```- #### Responsive stack with container queriesDescriptionAdvanced responsive layout that changes direction and spacing based on container size.jsx```

<s-query-container>

<s-stack

direction="@container (inline-size > 500px) inline, block"

gap="@container (inline-size > 500px) base, small-300"

>

<s-box

padding="large-100"

borderColor="base"

borderWidth="small"

borderRadius="large-100"

>

Content 1

</s-box>

<s-box

padding="large-100"

borderColor="base"

borderWidth="small"

borderRadius="large-100"

>

Content 2

</s-box>

</s-stack>

</s-query-container>

```html```

<s-query-container>

<s-stack

direction="@container (inline-size > 500px) inline, block"

gap="@container (inline-size > 500px) base, small-300"

>

<s-box

padding="large-100"

borderColor="base"

borderWidth="small"

borderRadius="large-100"

>

Content 1

</s-box>

<s-box

padding="large-100"

borderColor="base"

borderWidth="small"

borderRadius="large-100"

>

Content 2

</s-box>

</s-stack>

</s-query-container>

```- #### Custom alignmentDescriptionHorizontal stack with space-between justification and center alignment for balanced layouts.jsx```

<s-stack direction="inline" justifyContent="space-between" alignItems="center">

<s-text>Left aligned</s-text>

<s-text>Centered text</s-text>

<s-text>Right aligned</s-text>

</s-stack>

```html```

<s-stack direction="inline" justifyContent="space-between" alignItems="center">

<s-text>Left aligned</s-text>

<s-text>Centered text</s-text>

<s-text>Right aligned</s-text>

</s-stack>

```- #### Custom spacingDescriptionStack with custom gap values and separate row/column gap controls for precise spacing.jsx```

<s-stack gap="large-100 large-500" rowGap="large-300" columnGap="large-200">

<s-box

padding="large-100"

borderColor="base"

borderWidth="small"

borderRadius="large-100"

>

Box with custom spacing

</s-box>

<s-box

padding="large-100"

borderColor="base"

borderWidth="small"

borderRadius="large-100"

>

Another box

</s-box>

</s-stack>

```html```

<s-stack gap="large-100 large-500" rowGap="large-300" columnGap="large-200">

<s-box

padding="large-100"

borderColor="base"

borderWidth="small"

borderRadius="large-100"

>

Box with custom spacing

</s-box>

<s-box

padding="large-100"

borderColor="base"

borderWidth="small"

borderRadius="large-100"

>

Another box

</s-box>

</s-stack>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#useful-for)Useful for

- Placing non-form items in rows or columns when sections don't work for your layout.

- Controlling the spacing between elements.

- For form layouts where you need multiple input fields on the same row, use `s-grid` instead.

## [Anchor to considerations](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#considerations)Considerations

- Stack doesn't add any padding by default. If you want padding around your stacked elements, use `base` to apply the default padding.

- When spacing becomes limited, Stack will always wrap children to a new line.

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/stack#best-practices)Best practices

- Use smaller gaps between small elements and larger gaps between big ones.

- Maintain consistent spacing in stacks across all pages of your app.

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)