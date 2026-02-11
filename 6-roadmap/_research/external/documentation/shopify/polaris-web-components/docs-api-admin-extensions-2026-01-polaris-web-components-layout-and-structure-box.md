---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/layout-and-structure/box",
    "fetched_at": "2026-02-10T13:30:25.822939",
    "status": 200,
    "size_bytes": 331469
  },
  "metadata": {
    "title": "Box",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "layout-and-structure",
    "component": "box"
  }
}
---

# Box

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# BoxAsk assistantA generic container that provides a flexible alternative for custom designs not achievable with existing components. Use it to apply styling such as backgrounds, padding, or borders, or to nest and group other components. The contents of Box always maintain their natural size, making it especially useful within layout components that would otherwise stretch their children.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties)Properties[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the element. When set, it will be announced to users using assistive technologies and will provide them with more context.

Only use this when the element's content is not enough context for users using assistive technologies.

[Anchor to accessibilityRole](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-accessibilityrole)accessibilityRole**accessibilityRole**AccessibilityRoleAccessibilityRole**AccessibilityRoleAccessibilityRole**Default: 'generic'**Default: 'generic'**Sets the semantic meaning of the component’s content. When set, the role will be used by assistive technologies to help users navigate the page.

[Anchor to accessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-accessibilityvisibility)accessibilityVisibility**accessibilityVisibility**"visible" | "hidden" | "exclusive"**"visible" | "hidden" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the element.

- `visible`: the element is visible to all users.

- `hidden`: the element is removed from the accessibility tree but remains visible.

- `exclusive`: the element is visually hidden but remains in the accessibility tree.

[Anchor to background](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-background)background**background**BackgroundColorKeywordBackgroundColorKeyword**BackgroundColorKeywordBackgroundColorKeyword**Default: 'transparent'**Default: 'transparent'**Adjust the background of the component.

[Anchor to blockSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-blocksize)blockSize**blockSize**SizeUnitsOrAutoSizeUnitsOrAuto**SizeUnitsOrAutoSizeUnitsOrAuto**Default: 'auto'**Default: 'auto'**Adjust the [block size](https://developer.mozilla.org/en-US/docs/Web/CSS/block-size).

[Anchor to border](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-border)border**border**BorderShorthandBorderShorthand**BorderShorthandBorderShorthand**Default: 'none' - equivalent to `none base auto`.**Default: 'none' - equivalent to `none base auto`.**Set the border via the shorthand property.

This can be a size, optionally followed by a color, optionally followed by a style.

If the color is not specified, it will be `base`.

If the style is not specified, it will be `auto`.

Values can be overridden by `borderWidth`, `borderStyle`, and `borderColor`.

[Anchor to borderColor](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-bordercolor)borderColor**borderColor**"" | ColorKeywordColorKeyword**"" | ColorKeywordColorKeyword**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the color of the border.

[Anchor to borderRadius](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-borderradius)borderRadius**borderRadius**MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderRadiiBoxBorderRadii>**MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderRadiiBoxBorderRadii>**Default: 'none'**Default: 'none'**Adjust the radius of the border.

[Anchor to borderStyle](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-borderstyle)borderStyle**borderStyle**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderStylesBoxBorderStyles>**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderStylesBoxBorderStyles>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the style of the border.

[Anchor to borderWidth](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-borderwidth)borderWidth**borderWidth**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<"small" | "small-100" | "base" | "large" | "large-100" | "none">**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<"small" | "small-100" | "base" | "large" | "large-100" | "none">**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the width of the border.

[Anchor to display](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-display)display**display**MaybeResponsiveMaybeResponsive<"auto" | "none">**MaybeResponsiveMaybeResponsive<"auto" | "none">**Default: 'auto'**Default: 'auto'**Sets the outer [display](https://developer.mozilla.org/en-US/docs/Web/CSS/display) type of the component. The outer type sets a component's participation in [flow layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flow_layout).

- `auto` the component's initial value. The actual value depends on the component and context.

- `none` hides the component from display and removes it from the accessibility tree, making it invisible to screen readers.

[Anchor to inlineSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-inlinesize)inlineSize**inlineSize**SizeUnitsOrAutoSizeUnitsOrAuto**SizeUnitsOrAutoSizeUnitsOrAuto**Default: 'auto'**Default: 'auto'**Adjust the [inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/inline-size).

[Anchor to maxBlockSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-maxblocksize)maxBlockSize**maxBlockSize**SizeUnitsOrNoneSizeUnitsOrNone**SizeUnitsOrNoneSizeUnitsOrNone**Default: 'none'**Default: 'none'**Adjust the [maximum block size](https://developer.mozilla.org/en-US/docs/Web/CSS/max-block-size).

[Anchor to maxInlineSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-maxinlinesize)maxInlineSize**maxInlineSize**SizeUnitsOrNoneSizeUnitsOrNone**SizeUnitsOrNoneSizeUnitsOrNone**Default: 'none'**Default: 'none'**Adjust the [maximum inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/max-inline-size).

[Anchor to minBlockSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-minblocksize)minBlockSize**minBlockSize**SizeUnitsSizeUnits**SizeUnitsSizeUnits**Default: '0'**Default: '0'**Adjust the [minimum block size](https://developer.mozilla.org/en-US/docs/Web/CSS/min-block-size).

[Anchor to minInlineSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-mininlinesize)minInlineSize**minInlineSize**SizeUnitsSizeUnits**SizeUnitsSizeUnits**Default: '0'**Default: '0'**Adjust the [minimum inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/min-inline-size).

[Anchor to overflow](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-overflow)overflow**overflow**"visible" | "hidden"**"visible" | "hidden"**Default: 'visible'**Default: 'visible'**Sets the overflow behavior of the element.

- `hidden`: clips the content when it is larger than the element’s container. The element will not be scrollable and the users will not be able to access the clipped content by dragging or using a scroll wheel on a mouse.

- `visible`: the content that extends beyond the element’s container is visible.

[Anchor to padding](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-padding)padding**padding**MaybeResponsiveMaybeResponsive<MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: 'none'**Default: 'none'**Adjust the padding of all edges.

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

[Anchor to paddingBlock](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-paddingblock)paddingBlock**paddingBlock**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-padding.

- `large none` means block-start padding is `large`, block-end padding is `none`.

This overrides the block value of `padding`.

`paddingBlock` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingBlockEnd](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-paddingblockend)paddingBlockEnd**paddingBlockEnd**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-end padding.

This overrides the block-end value of `paddingBlock`.

`paddingBlockEnd` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingBlockStart](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-paddingblockstart)paddingBlockStart**paddingBlockStart**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-start padding.

This overrides the block-start value of `paddingBlock`.

`paddingBlockStart` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInline](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-paddinginline)paddingInline**paddingInline**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline padding.

- `large none` means inline-start padding is `large`, inline-end padding is `none`.

This overrides the inline value of `padding`.

`paddingInline` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInlineEnd](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-paddinginlineend)paddingInlineEnd**paddingInlineEnd**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline-end padding.

This overrides the inline-end value of `paddingInline`.

`paddingInlineEnd` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInlineStart](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#properties-propertydetail-paddinginlinestart)paddingInlineStart**paddingInlineStart**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline-start padding.

This overrides the inline-start value of `paddingInline`.

`paddingInlineStart` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

### AccessibilityRole```

'main' | 'header' | 'footer' | 'section' | 'region' | 'aside' | 'navigation' | 'ordered-list' | 'list-item' | 'list-item-separator' | 'unordered-list' | 'separator' | 'status' | 'alert' | 'generic' | 'presentation' | 'none'

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

```### SizeUnitsOrNone```

SizeUnits | 'none'

```### PaddingKeyword```

SizeKeyword | 'none'

```### MaybeTwoValuesShorthandProperty```

T | `${T} ${T}`

```## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Box.

ExamplesCodejsxhtmlCopy91234567<>  <s-box padding="base">Available for iPad, iPhone, and Android.</s-box>  <s-box padding="base" background="subdued" border="base" borderRadius="base">    Available for iPad, iPhone, and Android.  </s-box></>## Preview### Examples- #### Codejsx```

<>

<s-box padding="base">Available for iPad, iPhone, and Android.</s-box>

<s-box padding="base" background="subdued" border="base" borderRadius="base">

Available for iPad, iPhone, and Android.

</s-box>

</>

```html```

<s-box padding="base">Available for iPad, iPhone, and Android.</s-box>

<s-box padding="base" background="subdued" border="base" borderRadius="base">

Available for iPad, iPhone, and Android.

</s-box>

```- #### Basic containerDescriptionDemonstrates creating a simple container with padding, base background, border, and rounded corners to group and highlight product information.jsx```

<s-box

padding="base"

background="base"

borderWidth="base"

borderColor="base"

borderRadius="base"

>

<s-paragraph>Product information</s-paragraph>

</s-box>

```html```

<s-box

padding="base"

background="base"

borderWidth="base"

borderColor="base"

borderRadius="base"

>

<s-paragraph>Product information</s-paragraph>

</s-box>

```- #### Responsive shipping noticeDescriptionIllustrates using a box with responsive padding to create an adaptable container for shipping information that can adjust to different screen or container sizes.jsx```

<s-query-container>

<s-box

padding="@container (inline-size > 400px) base, large-200"

background="base"

borderWidth="base"

borderColor="base"

>

<s-text>Your order will be processed within 2-3 business days</s-text>

</s-box>

</s-query-container>

```html```

<s-query-container>

<s-box

padding="@container (inline-size > 400px) base, large-200"

background="base"

borderWidth="base"

borderColor="base"

>

<s-paragraph>Your order will be processed within 2-3 business days</s-paragraph>

</s-box>

</s-query-container>

```- #### Accessible status messagesDescriptionShows how to use boxes with ARIA roles and visibility controls to create semantic, screen-reader-friendly status and informational messages.jsx```

<s-stack gap="base">

<s-box

accessibilityRole="status"

padding="base"

background="strong"

borderRadius="base"

>

<s-paragraph>Payment failed</s-paragraph>

</s-box>

<s-box accessibilityVisibility="exclusive">

<s-paragraph>Price includes tax and shipping</s-paragraph>

</s-box>

</s-stack>

```html```

<s-stack gap="base">

<s-box

accessibilityRole="status"

padding="base"

background="strong"

borderRadius="base"

>

<s-paragraph>Payment failed</s-paragraph>

</s-box>

<s-box accessibilityVisibility="exclusive">

<s-paragraph>Price includes tax and shipping</s-paragraph>

</s-box>

</s-stack>

```- #### Nested hierarchical containersDescriptionDemonstrates creating nested, hierarchical layouts using multiple boxes, showing how boxes can be combined to organize related content sections with different styling.jsx```

<s-stack gap="base">

{/* Inventory status section */}

<s-box

padding="base"

background="base"

borderRadius="base"

borderWidth="base"

borderColor="base"

>

<s-stack gap="base">

<s-box padding="small-100" background="subdued" borderRadius="small">

<s-paragraph>In stock: 45 units</s-paragraph>

</s-box>

<s-box padding="small-100" background="subdued" borderRadius="small">

<s-paragraph>Low stock alert: 5 units</s-paragraph>

</s-box>

</s-stack>

</s-box>

{/* Product information section */}

<s-box

padding="base"

background="base"

borderRadius="base"

borderWidth="base"

borderColor="base"

>

<s-stack gap="base">

<s-heading>Product sales</s-heading>

<s-paragraph color="subdued">No recent sales of this product</s-paragraph>

<s-link>View details</s-link>

</s-stack>

</s-box>

</s-stack>

```html```

<s-stack gap="base">

<!-- Inventory status section -->

<s-box

padding="base"

background="base"

borderRadius="base"

borderWidth="base"

borderColor="base"

>

<s-stack gap="base">

<s-box padding="small-100" background="subdued" borderRadius="small">

<s-paragraph>In stock: 45 units</s-paragraph>

</s-box>

<s-box padding="small-100" background="subdued" borderRadius="small">

<s-paragraph>Low stock alert: 5 units</s-paragraph>

</s-box>

</s-stack>

</s-box>

<!-- Product information section -->

<s-box

padding="base"

background="base"

borderRadius="base"

borderWidth="base"

borderColor="base"

>

<s-stack gap="base">

<s-heading>Product sales</s-heading>

<s-paragraph color="subdued">No recent sales of this product</s-paragraph>

<s-link>View details</s-link>

</s-stack>

</s-box>

</s-stack>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#useful-for)Useful for

- Creating custom designs when you can't build what you need with the existing components.

- Setting up specific stylings such as background colors, paddings, and borders.

- Nesting with other components.

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/box#best-practices)Best practices

- Use for structural layouts with consistent spacing patterns

- Avoid adding too many borders that may visually fragment the interface

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)