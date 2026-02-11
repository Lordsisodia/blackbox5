---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/layout-and-structure/grid",
    "fetched_at": "2026-02-10T13:30:29.380442",
    "status": 200,
    "size_bytes": 550025
  },
  "metadata": {
    "title": "Grid",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "layout-and-structure",
    "component": "grid"
  }
}
---

# Grid

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# GridAsk assistantUse `s-grid` to organize your content in a matrix of rows and columns and make responsive layouts for pages. Grid follows the same pattern as the [CSS grid layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout).

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties)Properties[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the element. When set, it will be announced to users using assistive technologies and will provide them with more context.

Only use this when the element's content is not enough context for users using assistive technologies.

[Anchor to accessibilityRole](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-accessibilityrole)accessibilityRole**accessibilityRole**AccessibilityRoleAccessibilityRole**AccessibilityRoleAccessibilityRole**Default: 'generic'**Default: 'generic'**Sets the semantic meaning of the component’s content. When set, the role will be used by assistive technologies to help users navigate the page.

[Anchor to accessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-accessibilityvisibility)accessibilityVisibility**accessibilityVisibility**"visible" | "hidden" | "exclusive"**"visible" | "hidden" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the element.

- `visible`: the element is visible to all users.

- `hidden`: the element is removed from the accessibility tree but remains visible.

- `exclusive`: the element is visually hidden but remains in the accessibility tree.

[Anchor to alignContent](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-aligncontent)alignContent**alignContent**"" | AlignContentKeywordAlignContentKeyword**"" | AlignContentKeywordAlignContentKeyword**Default: '' - meaning no override**Default: '' - meaning no override**Aligns the grid along the block axis.

This overrides the block value of `placeContent`.

[Anchor to alignItems](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-alignitems)alignItems**alignItems**"" | AlignItemsKeywordAlignItemsKeyword**"" | AlignItemsKeywordAlignItemsKeyword**Default: '' - meaning no override**Default: '' - meaning no override**Aligns the grid items along the block axis.

[Anchor to background](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-background)background**background**BackgroundColorKeywordBackgroundColorKeyword**BackgroundColorKeywordBackgroundColorKeyword**Default: 'transparent'**Default: 'transparent'**Adjust the background of the component.

[Anchor to blockSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-blocksize)blockSize**blockSize**SizeUnitsOrAutoSizeUnitsOrAuto**SizeUnitsOrAutoSizeUnitsOrAuto**Default: 'auto'**Default: 'auto'**Adjust the [block size](https://developer.mozilla.org/en-US/docs/Web/CSS/block-size).

[Anchor to border](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-border)border**border**BorderShorthandBorderShorthand**BorderShorthandBorderShorthand**Default: 'none' - equivalent to `none base auto`.**Default: 'none' - equivalent to `none base auto`.**Set the border via the shorthand property.

This can be a size, optionally followed by a color, optionally followed by a style.

If the color is not specified, it will be `base`.

If the style is not specified, it will be `auto`.

Values can be overridden by `borderWidth`, `borderStyle`, and `borderColor`.

[Anchor to borderColor](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-bordercolor)borderColor**borderColor**"" | ColorKeywordColorKeyword**"" | ColorKeywordColorKeyword**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the color of the border.

[Anchor to borderRadius](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-borderradius)borderRadius**borderRadius**MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderRadiiBoxBorderRadii>**MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderRadiiBoxBorderRadii>**Default: 'none'**Default: 'none'**Adjust the radius of the border.

[Anchor to borderStyle](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-borderstyle)borderStyle**borderStyle**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderStylesBoxBorderStyles>**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderStylesBoxBorderStyles>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the style of the border.

[Anchor to borderWidth](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-borderwidth)borderWidth**borderWidth**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<"small" | "small-100" | "base" | "large" | "large-100" | "none">**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<"small" | "small-100" | "base" | "large" | "large-100" | "none">**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the width of the border.

[Anchor to columnGap](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-columngap)columnGap**columnGap**MaybeResponsiveMaybeResponsive<"" | SpacingKeywordSpacingKeyword>**MaybeResponsiveMaybeResponsive<"" | SpacingKeywordSpacingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust spacing between elements in the inline axis.

This overrides the column value of `gap`. `columnGap` either accepts:

- a single [SpacingKeyword](/docs/api/app-home/using-polaris-components#scale) value (e.g. `large-100`)

- OR a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported SpacingKeyword as a query value.

[Anchor to display](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-display)display**display**MaybeResponsiveMaybeResponsive<"auto" | "none">**MaybeResponsiveMaybeResponsive<"auto" | "none">**Default: 'auto'**Default: 'auto'**Sets the outer [display](https://developer.mozilla.org/en-US/docs/Web/CSS/display) type of the component. The outer type sets a component's participation in [flow layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flow_layout).

- `auto` the component's initial value. The actual value depends on the component and context.

- `none` hides the component from display and removes it from the accessibility tree, making it invisible to screen readers.

[Anchor to gap](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-gap)gap**gap**MaybeResponsiveMaybeResponsive<MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<SpacingKeywordSpacingKeyword>>**MaybeResponsiveMaybeResponsive<MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<SpacingKeywordSpacingKeyword>>**Default: 'none'**Default: 'none'**Adjust spacing between elements.

`gap` can either accept:

- a single [SpacingKeyword](/docs/api/app-home/using-polaris-components#scale) value applied to both axes (e.g. `large-100`)

- OR a pair of values (eg `large-100 large-500`) can be used to set the inline and block axes respectively

- OR a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported SpacingKeyword as a query value.

[Anchor to gridTemplateColumns](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-gridtemplatecolumns)gridTemplateColumns**gridTemplateColumns**string**string**Default: 'none'**Default: 'none'**Define columns and specify their size. `gridTemplateColumns` either accepts:

- [track sizing values](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Basic_concepts_of_grid_layout#fixed_and_flexible_track_sizes) (e.g. `1fr auto`)

- OR [responsive values](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported track sizing values as a query value.

[Anchor to gridTemplateRows](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-gridtemplaterows)gridTemplateRows**gridTemplateRows**string**string**Default: 'none'**Default: 'none'**Define rows and specify their size. `gridTemplateRows` either accepts:

- [track sizing values](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Basic_concepts_of_grid_layout#fixed_and_flexible_track_sizes) (e.g. `1fr auto`)

- OR [responsive values](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported track sizing values as a query value.

[Anchor to inlineSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-inlinesize)inlineSize**inlineSize**SizeUnitsOrAutoSizeUnitsOrAuto**SizeUnitsOrAutoSizeUnitsOrAuto**Default: 'auto'**Default: 'auto'**Adjust the [inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/inline-size).

[Anchor to justifyContent](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-justifycontent)justifyContent**justifyContent**"" | JustifyContentKeywordJustifyContentKeyword**"" | JustifyContentKeywordJustifyContentKeyword**Default: '' - meaning no override**Default: '' - meaning no override**Aligns the grid along the inline axis.

This overrides the inline value of `placeContent`.

[Anchor to justifyItems](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-justifyitems)justifyItems**justifyItems**"" | JustifyItemsKeywordJustifyItemsKeyword**"" | JustifyItemsKeywordJustifyItemsKeyword**Default: '' - meaning no override**Default: '' - meaning no override**Aligns the grid items along the inline axis.

[Anchor to maxBlockSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-maxblocksize)maxBlockSize**maxBlockSize**SizeUnitsOrNoneSizeUnitsOrNone**SizeUnitsOrNoneSizeUnitsOrNone**Default: 'none'**Default: 'none'**Adjust the [maximum block size](https://developer.mozilla.org/en-US/docs/Web/CSS/max-block-size).

[Anchor to maxInlineSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-maxinlinesize)maxInlineSize**maxInlineSize**SizeUnitsOrNoneSizeUnitsOrNone**SizeUnitsOrNoneSizeUnitsOrNone**Default: 'none'**Default: 'none'**Adjust the [maximum inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/max-inline-size).

[Anchor to minBlockSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-minblocksize)minBlockSize**minBlockSize**SizeUnitsSizeUnits**SizeUnitsSizeUnits**Default: '0'**Default: '0'**Adjust the [minimum block size](https://developer.mozilla.org/en-US/docs/Web/CSS/min-block-size).

[Anchor to minInlineSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-mininlinesize)minInlineSize**minInlineSize**SizeUnitsSizeUnits**SizeUnitsSizeUnits**Default: '0'**Default: '0'**Adjust the [minimum inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/min-inline-size).

[Anchor to overflow](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-overflow)overflow**overflow**"visible" | "hidden"**"visible" | "hidden"**Default: 'visible'**Default: 'visible'**Sets the overflow behavior of the element.

- `hidden`: clips the content when it is larger than the element’s container. The element will not be scrollable and the users will not be able to access the clipped content by dragging or using a scroll wheel on a mouse.

- `visible`: the content that extends beyond the element’s container is visible.

[Anchor to padding](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-padding)padding**padding**MaybeResponsiveMaybeResponsive<MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: 'none'**Default: 'none'**Adjust the padding of all edges.

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

[Anchor to paddingBlock](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-paddingblock)paddingBlock**paddingBlock**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-padding.

- `large none` means block-start padding is `large`, block-end padding is `none`.

This overrides the block value of `padding`.

`paddingBlock` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingBlockEnd](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-paddingblockend)paddingBlockEnd**paddingBlockEnd**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-end padding.

This overrides the block-end value of `paddingBlock`.

`paddingBlockEnd` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingBlockStart](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-paddingblockstart)paddingBlockStart**paddingBlockStart**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-start padding.

This overrides the block-start value of `paddingBlock`.

`paddingBlockStart` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInline](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-paddinginline)paddingInline**paddingInline**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline padding.

- `large none` means inline-start padding is `large`, inline-end padding is `none`.

This overrides the inline value of `padding`.

`paddingInline` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInlineEnd](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-paddinginlineend)paddingInlineEnd**paddingInlineEnd**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline-end padding.

This overrides the inline-end value of `paddingInline`.

`paddingInlineEnd` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInlineStart](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-paddinginlinestart)paddingInlineStart**paddingInlineStart**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline-start padding.

This overrides the inline-start value of `paddingInline`.

`paddingInlineStart` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to placeContent](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-placecontent)placeContent**placeContent**"normal normal" | "normal stretch" | "normal start" | "normal end" | "normal center" | "normal unsafe start" | "normal unsafe end" | "normal unsafe center" | "normal safe start" | "normal safe end" | "normal safe center" | "stretch normal" | "stretch stretch" | "stretch start" | "stretch end" | "stretch center" | "stretch unsafe start" | "stretch unsafe end" | "stretch unsafe center" | "stretch safe start" | "stretch safe end" | "stretch safe center" | "baseline normal" | "baseline stretch" | "baseline start" | "baseline end" | "baseline center" | "baseline unsafe start" | "baseline unsafe end" | "baseline unsafe center" | "baseline safe start" | "baseline safe end" | "baseline safe center" | "first baseline normal" | "first baseline stretch" | "first baseline start" | "first baseline end" | "first baseline center" | "first baseline unsafe start" | "first baseline unsafe end" | "first baseline unsafe center" | "first baseline safe start" | "first baseline safe end" | "first baseline safe center" | "last baseline normal" | "last baseline stretch" | "last baseline start" | "last baseline end" | "last baseline center" | "last baseline unsafe start" | "last baseline unsafe end" | "last baseline unsafe center" | "last baseline safe start" | "last baseline safe end" | "last baseline safe center" | "start normal" | "start stretch" | "start start" | "start end" | "start center" | "start unsafe start" | "start unsafe end" | "start unsafe center" | "start safe start" | "start safe end" | "start safe center" | "end normal" | "end stretch" | "end start" | "end end" | "end center" | "end unsafe start" | "end unsafe end" | "end unsafe center" | "end safe start" | "end safe end" | "end safe center" | "center normal" | "center stretch" | "center start" | "center end" | "center center" | "center unsafe start" | "center unsafe end" | "center unsafe center" | "center safe start" | "center safe end" | "center safe center" | "unsafe start normal" | "unsafe start stretch" | "unsafe start start" | "unsafe start end" | "unsafe start center" | "unsafe start unsafe start" | "unsafe start unsafe end" | "unsafe start unsafe center" | "unsafe start safe start" | "unsafe start safe end" | "unsafe start safe center" | "unsafe end normal" | "unsafe end stretch" | "unsafe end start" | "unsafe end end" | "unsafe end center" | "unsafe end unsafe start" | "unsafe end unsafe end" | "unsafe end unsafe center" | "unsafe end safe start" | "unsafe end safe end" | "unsafe end safe center" | "unsafe center normal" | "unsafe center stretch" | "unsafe center start" | "unsafe center end" | "unsafe center center" | "unsafe center unsafe start" | "unsafe center unsafe end" | "unsafe center unsafe center" | "unsafe center safe start" | "unsafe center safe end" | "unsafe center safe center" | "safe start normal" | "safe start stretch" | "safe start start" | "safe start end" | "safe start center" | "safe start unsafe start" | "safe start unsafe end" | "safe start unsafe center" | "safe start safe start" | "safe start safe end" | "safe start safe center" | "safe end normal" | "safe end stretch" | "safe end start" | "safe end end" | "safe end center" | "safe end unsafe start" | "safe end unsafe end" | "safe end unsafe center" | "safe end safe start" | "safe end safe end" | "safe end safe center" | "safe center normal" | "safe center stretch" | "safe center start" | "safe center end" | "safe center center" | "safe center unsafe start" | "safe center unsafe end" | "safe center unsafe center" | "safe center safe start" | "safe center safe end" | "safe center safe center" | AlignContentKeywordAlignContentKeyword | "normal space-between" | "normal space-around" | "normal space-evenly" | "baseline space-between" | "baseline space-around" | "baseline space-evenly" | "first baseline space-between" | "first baseline space-around" | "first baseline space-evenly" | "last baseline space-between" | "last baseline space-around" | "last baseline space-evenly" | "start space-between" | "start space-around" | "start space-evenly" | "end space-between" | "end space-around" | "end space-evenly" | "center space-between" | "center space-around" | "center space-evenly" | "unsafe start space-between" | "unsafe start space-around" | "unsafe start space-evenly" | "unsafe end space-between" | "unsafe end space-around" | "unsafe end space-evenly" | "unsafe center space-between" | "unsafe center space-around" | "unsafe center space-evenly" | "safe start space-between" | "safe start space-around" | "safe start space-evenly" | "safe end space-between" | "safe end space-around" | "safe end space-evenly" | "safe center space-between" | "safe center space-around" | "safe center space-evenly" | "stretch space-between" | "stretch space-around" | "stretch space-evenly" | "space-between normal" | "space-between start" | "space-between end" | "space-between center" | "space-between unsafe start" | "space-between unsafe end" | "space-between unsafe center" | "space-between safe start" | "space-between safe end" | "space-between safe center" | "space-between stretch" | "space-between space-between" | "space-between space-around" | "space-between space-evenly" | "space-around normal" | "space-around start" | "space-around end" | "space-around center" | "space-around unsafe start" | "space-around unsafe end" | "space-around unsafe center" | "space-around safe start" | "space-around safe end" | "space-around safe center" | "space-around stretch" | "space-around space-between" | "space-around space-around" | "space-around space-evenly" | "space-evenly normal" | "space-evenly start" | "space-evenly end" | "space-evenly center" | "space-evenly unsafe start" | "space-evenly unsafe end" | "space-evenly unsafe center" | "space-evenly safe start" | "space-evenly safe end" | "space-evenly safe center" | "space-evenly stretch" | "space-evenly space-between" | "space-evenly space-around" | "space-evenly space-evenly"**"normal normal" | "normal stretch" | "normal start" | "normal end" | "normal center" | "normal unsafe start" | "normal unsafe end" | "normal unsafe center" | "normal safe start" | "normal safe end" | "normal safe center" | "stretch normal" | "stretch stretch" | "stretch start" | "stretch end" | "stretch center" | "stretch unsafe start" | "stretch unsafe end" | "stretch unsafe center" | "stretch safe start" | "stretch safe end" | "stretch safe center" | "baseline normal" | "baseline stretch" | "baseline start" | "baseline end" | "baseline center" | "baseline unsafe start" | "baseline unsafe end" | "baseline unsafe center" | "baseline safe start" | "baseline safe end" | "baseline safe center" | "first baseline normal" | "first baseline stretch" | "first baseline start" | "first baseline end" | "first baseline center" | "first baseline unsafe start" | "first baseline unsafe end" | "first baseline unsafe center" | "first baseline safe start" | "first baseline safe end" | "first baseline safe center" | "last baseline normal" | "last baseline stretch" | "last baseline start" | "last baseline end" | "last baseline center" | "last baseline unsafe start" | "last baseline unsafe end" | "last baseline unsafe center" | "last baseline safe start" | "last baseline safe end" | "last baseline safe center" | "start normal" | "start stretch" | "start start" | "start end" | "start center" | "start unsafe start" | "start unsafe end" | "start unsafe center" | "start safe start" | "start safe end" | "start safe center" | "end normal" | "end stretch" | "end start" | "end end" | "end center" | "end unsafe start" | "end unsafe end" | "end unsafe center" | "end safe start" | "end safe end" | "end safe center" | "center normal" | "center stretch" | "center start" | "center end" | "center center" | "center unsafe start" | "center unsafe end" | "center unsafe center" | "center safe start" | "center safe end" | "center safe center" | "unsafe start normal" | "unsafe start stretch" | "unsafe start start" | "unsafe start end" | "unsafe start center" | "unsafe start unsafe start" | "unsafe start unsafe end" | "unsafe start unsafe center" | "unsafe start safe start" | "unsafe start safe end" | "unsafe start safe center" | "unsafe end normal" | "unsafe end stretch" | "unsafe end start" | "unsafe end end" | "unsafe end center" | "unsafe end unsafe start" | "unsafe end unsafe end" | "unsafe end unsafe center" | "unsafe end safe start" | "unsafe end safe end" | "unsafe end safe center" | "unsafe center normal" | "unsafe center stretch" | "unsafe center start" | "unsafe center end" | "unsafe center center" | "unsafe center unsafe start" | "unsafe center unsafe end" | "unsafe center unsafe center" | "unsafe center safe start" | "unsafe center safe end" | "unsafe center safe center" | "safe start normal" | "safe start stretch" | "safe start start" | "safe start end" | "safe start center" | "safe start unsafe start" | "safe start unsafe end" | "safe start unsafe center" | "safe start safe start" | "safe start safe end" | "safe start safe center" | "safe end normal" | "safe end stretch" | "safe end start" | "safe end end" | "safe end center" | "safe end unsafe start" | "safe end unsafe end" | "safe end unsafe center" | "safe end safe start" | "safe end safe end" | "safe end safe center" | "safe center normal" | "safe center stretch" | "safe center start" | "safe center end" | "safe center center" | "safe center unsafe start" | "safe center unsafe end" | "safe center unsafe center" | "safe center safe start" | "safe center safe end" | "safe center safe center" | AlignContentKeywordAlignContentKeyword | "normal space-between" | "normal space-around" | "normal space-evenly" | "baseline space-between" | "baseline space-around" | "baseline space-evenly" | "first baseline space-between" | "first baseline space-around" | "first baseline space-evenly" | "last baseline space-between" | "last baseline space-around" | "last baseline space-evenly" | "start space-between" | "start space-around" | "start space-evenly" | "end space-between" | "end space-around" | "end space-evenly" | "center space-between" | "center space-around" | "center space-evenly" | "unsafe start space-between" | "unsafe start space-around" | "unsafe start space-evenly" | "unsafe end space-between" | "unsafe end space-around" | "unsafe end space-evenly" | "unsafe center space-between" | "unsafe center space-around" | "unsafe center space-evenly" | "safe start space-between" | "safe start space-around" | "safe start space-evenly" | "safe end space-between" | "safe end space-around" | "safe end space-evenly" | "safe center space-between" | "safe center space-around" | "safe center space-evenly" | "stretch space-between" | "stretch space-around" | "stretch space-evenly" | "space-between normal" | "space-between start" | "space-between end" | "space-between center" | "space-between unsafe start" | "space-between unsafe end" | "space-between unsafe center" | "space-between safe start" | "space-between safe end" | "space-between safe center" | "space-between stretch" | "space-between space-between" | "space-between space-around" | "space-between space-evenly" | "space-around normal" | "space-around start" | "space-around end" | "space-around center" | "space-around unsafe start" | "space-around unsafe end" | "space-around unsafe center" | "space-around safe start" | "space-around safe end" | "space-around safe center" | "space-around stretch" | "space-around space-between" | "space-around space-around" | "space-around space-evenly" | "space-evenly normal" | "space-evenly start" | "space-evenly end" | "space-evenly center" | "space-evenly unsafe start" | "space-evenly unsafe end" | "space-evenly unsafe center" | "space-evenly safe start" | "space-evenly safe end" | "space-evenly safe center" | "space-evenly stretch" | "space-evenly space-between" | "space-evenly space-around" | "space-evenly space-evenly"**Default: 'normal normal'**Default: 'normal normal'**A shorthand property for `justify-content` and `align-content`.

[Anchor to placeItems](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-placeitems)placeItems**placeItems**AlignItemsKeywordAlignItemsKeyword | "normal normal" | "normal stretch" | "normal baseline" | "normal first baseline" | "normal last baseline" | "normal start" | "normal end" | "normal center" | "normal unsafe start" | "normal unsafe end" | "normal unsafe center" | "normal safe start" | "normal safe end" | "normal safe center" | "stretch normal" | "stretch stretch" | "stretch baseline" | "stretch first baseline" | "stretch last baseline" | "stretch start" | "stretch end" | "stretch center" | "stretch unsafe start" | "stretch unsafe end" | "stretch unsafe center" | "stretch safe start" | "stretch safe end" | "stretch safe center" | "baseline normal" | "baseline stretch" | "baseline baseline" | "baseline first baseline" | "baseline last baseline" | "baseline start" | "baseline end" | "baseline center" | "baseline unsafe start" | "baseline unsafe end" | "baseline unsafe center" | "baseline safe start" | "baseline safe end" | "baseline safe center" | "first baseline normal" | "first baseline stretch" | "first baseline baseline" | "first baseline first baseline" | "first baseline last baseline" | "first baseline start" | "first baseline end" | "first baseline center" | "first baseline unsafe start" | "first baseline unsafe end" | "first baseline unsafe center" | "first baseline safe start" | "first baseline safe end" | "first baseline safe center" | "last baseline normal" | "last baseline stretch" | "last baseline baseline" | "last baseline first baseline" | "last baseline last baseline" | "last baseline start" | "last baseline end" | "last baseline center" | "last baseline unsafe start" | "last baseline unsafe end" | "last baseline unsafe center" | "last baseline safe start" | "last baseline safe end" | "last baseline safe center" | "start normal" | "start stretch" | "start baseline" | "start first baseline" | "start last baseline" | "start start" | "start end" | "start center" | "start unsafe start" | "start unsafe end" | "start unsafe center" | "start safe start" | "start safe end" | "start safe center" | "end normal" | "end stretch" | "end baseline" | "end first baseline" | "end last baseline" | "end start" | "end end" | "end center" | "end unsafe start" | "end unsafe end" | "end unsafe center" | "end safe start" | "end safe end" | "end safe center" | "center normal" | "center stretch" | "center baseline" | "center first baseline" | "center last baseline" | "center start" | "center end" | "center center" | "center unsafe start" | "center unsafe end" | "center unsafe center" | "center safe start" | "center safe end" | "center safe center" | "unsafe start normal" | "unsafe start stretch" | "unsafe start baseline" | "unsafe start first baseline" | "unsafe start last baseline" | "unsafe start start" | "unsafe start end" | "unsafe start center" | "unsafe start unsafe start" | "unsafe start unsafe end" | "unsafe start unsafe center" | "unsafe start safe start" | "unsafe start safe end" | "unsafe start safe center" | "unsafe end normal" | "unsafe end stretch" | "unsafe end baseline" | "unsafe end first baseline" | "unsafe end last baseline" | "unsafe end start" | "unsafe end end" | "unsafe end center" | "unsafe end unsafe start" | "unsafe end unsafe end" | "unsafe end unsafe center" | "unsafe end safe start" | "unsafe end safe end" | "unsafe end safe center" | "unsafe center normal" | "unsafe center stretch" | "unsafe center baseline" | "unsafe center first baseline" | "unsafe center last baseline" | "unsafe center start" | "unsafe center end" | "unsafe center center" | "unsafe center unsafe start" | "unsafe center unsafe end" | "unsafe center unsafe center" | "unsafe center safe start" | "unsafe center safe end" | "unsafe center safe center" | "safe start normal" | "safe start stretch" | "safe start baseline" | "safe start first baseline" | "safe start last baseline" | "safe start start" | "safe start end" | "safe start center" | "safe start unsafe start" | "safe start unsafe end" | "safe start unsafe center" | "safe start safe start" | "safe start safe end" | "safe start safe center" | "safe end normal" | "safe end stretch" | "safe end baseline" | "safe end first baseline" | "safe end last baseline" | "safe end start" | "safe end end" | "safe end center" | "safe end unsafe start" | "safe end unsafe end" | "safe end unsafe center" | "safe end safe start" | "safe end safe end" | "safe end safe center" | "safe center normal" | "safe center stretch" | "safe center baseline" | "safe center first baseline" | "safe center last baseline" | "safe center start" | "safe center end" | "safe center center" | "safe center unsafe start" | "safe center unsafe end" | "safe center unsafe center" | "safe center safe start" | "safe center safe end" | "safe center safe center"**AlignItemsKeywordAlignItemsKeyword | "normal normal" | "normal stretch" | "normal baseline" | "normal first baseline" | "normal last baseline" | "normal start" | "normal end" | "normal center" | "normal unsafe start" | "normal unsafe end" | "normal unsafe center" | "normal safe start" | "normal safe end" | "normal safe center" | "stretch normal" | "stretch stretch" | "stretch baseline" | "stretch first baseline" | "stretch last baseline" | "stretch start" | "stretch end" | "stretch center" | "stretch unsafe start" | "stretch unsafe end" | "stretch unsafe center" | "stretch safe start" | "stretch safe end" | "stretch safe center" | "baseline normal" | "baseline stretch" | "baseline baseline" | "baseline first baseline" | "baseline last baseline" | "baseline start" | "baseline end" | "baseline center" | "baseline unsafe start" | "baseline unsafe end" | "baseline unsafe center" | "baseline safe start" | "baseline safe end" | "baseline safe center" | "first baseline normal" | "first baseline stretch" | "first baseline baseline" | "first baseline first baseline" | "first baseline last baseline" | "first baseline start" | "first baseline end" | "first baseline center" | "first baseline unsafe start" | "first baseline unsafe end" | "first baseline unsafe center" | "first baseline safe start" | "first baseline safe end" | "first baseline safe center" | "last baseline normal" | "last baseline stretch" | "last baseline baseline" | "last baseline first baseline" | "last baseline last baseline" | "last baseline start" | "last baseline end" | "last baseline center" | "last baseline unsafe start" | "last baseline unsafe end" | "last baseline unsafe center" | "last baseline safe start" | "last baseline safe end" | "last baseline safe center" | "start normal" | "start stretch" | "start baseline" | "start first baseline" | "start last baseline" | "start start" | "start end" | "start center" | "start unsafe start" | "start unsafe end" | "start unsafe center" | "start safe start" | "start safe end" | "start safe center" | "end normal" | "end stretch" | "end baseline" | "end first baseline" | "end last baseline" | "end start" | "end end" | "end center" | "end unsafe start" | "end unsafe end" | "end unsafe center" | "end safe start" | "end safe end" | "end safe center" | "center normal" | "center stretch" | "center baseline" | "center first baseline" | "center last baseline" | "center start" | "center end" | "center center" | "center unsafe start" | "center unsafe end" | "center unsafe center" | "center safe start" | "center safe end" | "center safe center" | "unsafe start normal" | "unsafe start stretch" | "unsafe start baseline" | "unsafe start first baseline" | "unsafe start last baseline" | "unsafe start start" | "unsafe start end" | "unsafe start center" | "unsafe start unsafe start" | "unsafe start unsafe end" | "unsafe start unsafe center" | "unsafe start safe start" | "unsafe start safe end" | "unsafe start safe center" | "unsafe end normal" | "unsafe end stretch" | "unsafe end baseline" | "unsafe end first baseline" | "unsafe end last baseline" | "unsafe end start" | "unsafe end end" | "unsafe end center" | "unsafe end unsafe start" | "unsafe end unsafe end" | "unsafe end unsafe center" | "unsafe end safe start" | "unsafe end safe end" | "unsafe end safe center" | "unsafe center normal" | "unsafe center stretch" | "unsafe center baseline" | "unsafe center first baseline" | "unsafe center last baseline" | "unsafe center start" | "unsafe center end" | "unsafe center center" | "unsafe center unsafe start" | "unsafe center unsafe end" | "unsafe center unsafe center" | "unsafe center safe start" | "unsafe center safe end" | "unsafe center safe center" | "safe start normal" | "safe start stretch" | "safe start baseline" | "safe start first baseline" | "safe start last baseline" | "safe start start" | "safe start end" | "safe start center" | "safe start unsafe start" | "safe start unsafe end" | "safe start unsafe center" | "safe start safe start" | "safe start safe end" | "safe start safe center" | "safe end normal" | "safe end stretch" | "safe end baseline" | "safe end first baseline" | "safe end last baseline" | "safe end start" | "safe end end" | "safe end center" | "safe end unsafe start" | "safe end unsafe end" | "safe end unsafe center" | "safe end safe start" | "safe end safe end" | "safe end safe center" | "safe center normal" | "safe center stretch" | "safe center baseline" | "safe center first baseline" | "safe center last baseline" | "safe center start" | "safe center end" | "safe center center" | "safe center unsafe start" | "safe center unsafe end" | "safe center unsafe center" | "safe center safe start" | "safe center safe end" | "safe center safe center"**Default: 'normal normal'**Default: 'normal normal'**A shorthand property for `justify-items` and `align-items`.

[Anchor to rowGap](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#properties-propertydetail-rowgap)rowGap**rowGap**MaybeResponsiveMaybeResponsive<"" | SpacingKeywordSpacingKeyword>**MaybeResponsiveMaybeResponsive<"" | SpacingKeywordSpacingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust spacing between elements in the block axis.

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

```### JustifyItemsKeywordJustify items defines the default justify-self for all items of the box, giving them all a default way of justifying each box along the appropriate axis.```

'normal' | 'stretch' | BaselinePosition | OverflowPosition | ContentPosition

```### SizeUnitsOrNone```

SizeUnits | 'none'

```### PaddingKeyword```

SizeKeyword | 'none'

```## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Grid.

## [Anchor to griditem](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem)GridItemDisplay content within a single item of a grid layout.

[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the element. When set, it will be announced to users using assistive technologies and will provide them with more context.

Only use this when the element's content is not enough context for users using assistive technologies.

[Anchor to accessibilityRole](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-accessibilityrole)accessibilityRole**accessibilityRole**AccessibilityRoleAccessibilityRole**AccessibilityRoleAccessibilityRole**Default: 'generic'**Default: 'generic'**Sets the semantic meaning of the component’s content. When set, the role will be used by assistive technologies to help users navigate the page.

[Anchor to accessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-accessibilityvisibility)accessibilityVisibility**accessibilityVisibility**"visible" | "hidden" | "exclusive"**"visible" | "hidden" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the element.

- `visible`: the element is visible to all users.

- `hidden`: the element is removed from the accessibility tree but remains visible.

- `exclusive`: the element is visually hidden but remains in the accessibility tree.

[Anchor to background](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-background)background**background**BackgroundColorKeywordBackgroundColorKeyword**BackgroundColorKeywordBackgroundColorKeyword**Default: 'transparent'**Default: 'transparent'**Adjust the background of the component.

[Anchor to blockSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-blocksize)blockSize**blockSize**SizeUnitsOrAutoSizeUnitsOrAuto**SizeUnitsOrAutoSizeUnitsOrAuto**Default: 'auto'**Default: 'auto'**Adjust the [block size](https://developer.mozilla.org/en-US/docs/Web/CSS/block-size).

[Anchor to border](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-border)border**border**BorderShorthandBorderShorthand**BorderShorthandBorderShorthand**Default: 'none' - equivalent to `none base auto`.**Default: 'none' - equivalent to `none base auto`.**Set the border via the shorthand property.

This can be a size, optionally followed by a color, optionally followed by a style.

If the color is not specified, it will be `base`.

If the style is not specified, it will be `auto`.

Values can be overridden by `borderWidth`, `borderStyle`, and `borderColor`.

[Anchor to borderColor](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-bordercolor)borderColor**borderColor**"" | ColorKeywordColorKeyword**"" | ColorKeywordColorKeyword**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the color of the border.

[Anchor to borderRadius](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-borderradius)borderRadius**borderRadius**MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderRadiiBoxBorderRadii>**MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderRadiiBoxBorderRadii>**Default: 'none'**Default: 'none'**Adjust the radius of the border.

[Anchor to borderStyle](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-borderstyle)borderStyle**borderStyle**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderStylesBoxBorderStyles>**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderStylesBoxBorderStyles>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the style of the border.

[Anchor to borderWidth](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-borderwidth)borderWidth**borderWidth**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<"small" | "small-100" | "base" | "large" | "large-100" | "none">**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<"small" | "small-100" | "base" | "large" | "large-100" | "none">**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the width of the border.

[Anchor to display](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-display)display**display**MaybeResponsiveMaybeResponsive<"auto" | "none">**MaybeResponsiveMaybeResponsive<"auto" | "none">**Default: 'auto'**Default: 'auto'**Sets the outer [display](https://developer.mozilla.org/en-US/docs/Web/CSS/display) type of the component. The outer type sets a component's participation in [flow layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flow_layout).

- `auto` the component's initial value. The actual value depends on the component and context.

- `none` hides the component from display and removes it from the accessibility tree, making it invisible to screen readers.

[Anchor to gridColumn](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-gridcolumn)gridColumn**gridColumn**"auto" | `span ${number}`**"auto" | `span ${number}`**Default: 'auto'**Default: 'auto'**Number of columns the item will span across

[Anchor to gridRow](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-gridrow)gridRow**gridRow**"auto" | `span ${number}`**"auto" | `span ${number}`**Default: 'auto'**Default: 'auto'**Number of rows the item will span across

[Anchor to inlineSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-inlinesize)inlineSize**inlineSize**SizeUnitsOrAutoSizeUnitsOrAuto**SizeUnitsOrAutoSizeUnitsOrAuto**Default: 'auto'**Default: 'auto'**Adjust the [inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/inline-size).

[Anchor to maxBlockSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-maxblocksize)maxBlockSize**maxBlockSize**SizeUnitsOrNoneSizeUnitsOrNone**SizeUnitsOrNoneSizeUnitsOrNone**Default: 'none'**Default: 'none'**Adjust the [maximum block size](https://developer.mozilla.org/en-US/docs/Web/CSS/max-block-size).

[Anchor to maxInlineSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-maxinlinesize)maxInlineSize**maxInlineSize**SizeUnitsOrNoneSizeUnitsOrNone**SizeUnitsOrNoneSizeUnitsOrNone**Default: 'none'**Default: 'none'**Adjust the [maximum inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/max-inline-size).

[Anchor to minBlockSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-minblocksize)minBlockSize**minBlockSize**SizeUnitsSizeUnits**SizeUnitsSizeUnits**Default: '0'**Default: '0'**Adjust the [minimum block size](https://developer.mozilla.org/en-US/docs/Web/CSS/min-block-size).

[Anchor to minInlineSize](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-mininlinesize)minInlineSize**minInlineSize**SizeUnitsSizeUnits**SizeUnitsSizeUnits**Default: '0'**Default: '0'**Adjust the [minimum inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/min-inline-size).

[Anchor to overflow](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-overflow)overflow**overflow**"visible" | "hidden"**"visible" | "hidden"**Default: 'visible'**Default: 'visible'**Sets the overflow behavior of the element.

- `hidden`: clips the content when it is larger than the element’s container. The element will not be scrollable and the users will not be able to access the clipped content by dragging or using a scroll wheel on a mouse.

- `visible`: the content that extends beyond the element’s container is visible.

[Anchor to padding](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-padding)padding**padding**MaybeResponsiveMaybeResponsive<MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: 'none'**Default: 'none'**Adjust the padding of all edges.

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

[Anchor to paddingBlock](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-paddingblock)paddingBlock**paddingBlock**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-padding.

- `large none` means block-start padding is `large`, block-end padding is `none`.

This overrides the block value of `padding`.

`paddingBlock` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingBlockEnd](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-paddingblockend)paddingBlockEnd**paddingBlockEnd**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-end padding.

This overrides the block-end value of `paddingBlock`.

`paddingBlockEnd` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingBlockStart](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-paddingblockstart)paddingBlockStart**paddingBlockStart**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-start padding.

This overrides the block-start value of `paddingBlock`.

`paddingBlockStart` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInline](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-paddinginline)paddingInline**paddingInline**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline padding.

- `large none` means inline-start padding is `large`, inline-end padding is `none`.

This overrides the inline value of `padding`.

`paddingInline` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInlineEnd](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-paddinginlineend)paddingInlineEnd**paddingInlineEnd**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline-end padding.

This overrides the inline-end value of `paddingInline`.

`paddingInlineEnd` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInlineStart](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#griditem-propertydetail-paddinginlinestart)paddingInlineStart**paddingInlineStart**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline-start padding.

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

```## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the GridItem.

ExamplesCodejsxhtmlCopy99123456789101112131415<s-grid  gridTemplateColumns="repeat(2, 1fr)"  gap="small"  justifyContent="center">  <s-grid-item gridColumn="span 2" border="base" borderStyle="dashed">    Summary of sales  </s-grid-item>  <s-grid-item gridColumn="span 1" border="base" borderStyle="dashed">    Orders  </s-grid-item>  <s-grid-item gridColumn="auto" border="base" borderStyle="dashed">    Customers  </s-grid-item></s-grid>## Preview### Examples- #### Codejsx```

<s-grid

gridTemplateColumns="repeat(2, 1fr)"

gap="small"

justifyContent="center"

>

<s-grid-item gridColumn="span 2" border="base" borderStyle="dashed">

Summary of sales

</s-grid-item>

<s-grid-item gridColumn="span 1" border="base" borderStyle="dashed">

Orders

</s-grid-item>

<s-grid-item gridColumn="auto" border="base" borderStyle="dashed">

Customers

</s-grid-item>

</s-grid>

```html```

<s-grid

gridTemplateColumns="repeat(2, 1fr)"

gap="small"

justifyContent="center"

>

<s-grid-item gridColumn="span 2" border="base" borderStyle="dashed">

Summary of sales

</s-grid-item>

<s-grid-item gridColumn="span 1" border="base" borderStyle="dashed">

Orders

</s-grid-item>

<s-grid-item gridColumn="auto" border="base" borderStyle="dashed">

Customers

</s-grid-item>

</s-grid>

```- #### Basic two-column layoutDescriptionSimple 12-column grid system with equal-width left and right columns.jsx```

<s-grid gridTemplateColumns="repeat(12, 1fr)" gap="base">

<s-grid-item gridColumn="span 6" gridRow="span 1">

<s-section>

<s-text>Left column</s-text>

</s-section>

</s-grid-item>

<s-grid-item gridColumn="span 6" gridRow="span 1">

<s-section>

<s-text>Right column</s-text>

</s-section>

</s-grid-item>

</s-grid>

```html```

<s-grid gridTemplateColumns="repeat(12, 1fr)" gap="base">

<s-grid-item gridColumn="span 6" gridRow="span 1">

<s-section>

<s-text>Left column</s-text>

</s-section>

</s-grid-item>

<s-grid-item gridColumn="span 6" gridRow="span 1">

<s-section>

<s-text>Right column</s-text>

</s-section>

</s-grid-item>

</s-grid>

```- #### Layout with spansDescriptionGrid layout with full-width, half-width, and third-width column arrangements.jsx```

<s-stack gap="base">

<s-grid gridTemplateColumns="repeat(12, 1fr)" gap="base">

<s-grid-item gridColumn="span 12" gridRow="span 1">

<s-section>

<s-text>Full width field</s-text>

</s-section>

</s-grid-item>

<s-grid-item gridColumn="span 6" gridRow="span 2">

<s-section>

<s-text>Half width field</s-text>

</s-section>

</s-grid-item>

<s-grid-item gridColumn="span 6" gridRow="span 2">

<s-section>

<s-text>Half width field</s-text>

</s-section>

</s-grid-item>

<s-grid-item gridColumn="span 4" gridRow="span 3">

<s-section>

<s-text>Third width field</s-text>

</s-section>

</s-grid-item>

<s-grid-item gridColumn="span 4" gridRow="span 3">

<s-section>

<s-text>Third width field</s-text>

</s-section>

</s-grid-item>

<s-grid-item gridColumn="span 4" gridRow="span 3">

<s-section>

<s-text>Third width field</s-text>

</s-section>

</s-grid-item>

</s-grid>

</s-stack>

```html```

<s-stack gap="base">

<s-grid gridTemplateColumns="repeat(12, 1fr)" gap="base">

<s-grid-item gridColumn="span 12" gridRow="span 1">

<s-section>

<s-text>Full width field</s-text>

</s-section>

</s-grid-item>

<s-grid-item gridColumn="span 6" gridRow="span 2">

<s-section>

<s-text>Half width field</s-text>

</s-section>

</s-grid-item>

<s-grid-item gridColumn="span 6" gridRow="span 2">

<s-section>

<s-text>Half width field</s-text>

</s-section>

</s-grid-item>

<s-grid-item gridColumn="span 4" gridRow="span 3">

<s-section>

<s-text>Third width field</s-text>

</s-section>

</s-grid-item>

<s-grid-item gridColumn="span 4" gridRow="span 3">

<s-section>

<s-text>Third width field</s-text>

</s-section>

</s-grid-item>

<s-grid-item gridColumn="span 4" gridRow="span 3">

<s-section>

<s-text>Third width field</s-text>

</s-section>

</s-grid-item>

</s-grid>

</s-stack>

```- #### Responsive gridDescriptionAdaptive grid that automatically adjusts column count based on screen size.jsx```

<s-stack gap="base">

<s-text type="strong">Narrow container (375px)</s-text>

<s-box inlineSize="375px">

<s-query-container>

<s-grid

gridTemplateColumns="@container (inline-size > 400px) 1fr 1fr 1fr, 1fr"

gap="base"

>

<s-grid-item>

<s-box padding="small" background="subdued">

<s-text>Item 1</s-text>

</s-box>

</s-grid-item>

<s-grid-item>

<s-box padding="small" background="subdued">

<s-text>Item 2</s-text>

</s-box>

</s-grid-item>

<s-grid-item>

<s-box padding="small" background="subdued">

<s-text>Item 3</s-text>

</s-box>

</s-grid-item>

</s-grid>

</s-query-container>

</s-box>

<s-text type="strong">Wide container (450px)</s-text>

<s-box inlineSize="450px">

<s-query-container>

<s-grid

gridTemplateColumns="@container (inline-size > 400px) 1fr 1fr 1fr, 1fr"

gap="base"

>

<s-grid-item>

<s-box padding="small" background="subdued">

<s-text>Item 1</s-text>

</s-box>

</s-grid-item>

<s-grid-item>

<s-box padding="small" background="subdued">

<s-text>Item 2</s-text>

</s-box>

</s-grid-item>

<s-grid-item>

<s-box padding="small" background="subdued">

<s-text>Item 3</s-text>

</s-box>

</s-grid-item>

</s-grid>

</s-query-container>

</s-box>

</s-stack>

```html```

<s-stack gap="base">

<s-text type="strong">Narrow container (375px)</s-text>

<s-box inlineSize="375px">

<s-query-container>

<s-grid

gridTemplateColumns="@container (inline-size > 400px) 1fr 1fr 1fr, 1fr"

gap="base"

>

<s-grid-item>

<s-box padding="small" background="subdued">

<s-text>Item 1</s-text>

</s-box>

</s-grid-item>

<s-grid-item>

<s-box padding="small" background="subdued">

<s-text>Item 2</s-text>

</s-box>

</s-grid-item>

<s-grid-item>

<s-box padding="small" background="subdued">

<s-text>Item 3</s-text>

</s-box>

</s-grid-item>

</s-grid>

</s-query-container>

</s-box>

<s-text type="strong">Wide container (450px)</s-text>

<s-box inlineSize="450px">

<s-query-container>

<s-grid

gridTemplateColumns="@container (inline-size > 400px) 1fr 1fr 1fr, 1fr"

gap="base"

>

<s-grid-item>

<s-box padding="small" background="subdued">

<s-text>Item 1</s-text>

</s-box>

</s-grid-item>

<s-grid-item>

<s-box padding="small" background="subdued">

<s-text>Item 2</s-text>

</s-box>

</s-grid-item>

<s-grid-item>

<s-box padding="small" background="subdued">

<s-text>Item 3</s-text>

</s-box>

</s-grid-item>

</s-grid>

</s-query-container>

</s-box>

</s-stack>

```## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#best-practices)Best practices

- Always configure layout properties when using Grid. At minimum, set gridTemplateColumns to define your column structure (e.g., repeat(12, 1fr) for a 12-column grid)

- Use gap to add spacing between grid items rather than adding margins to individual items

- Combine gridTemplateColumns with gridColumn on GridItem components to control how items span across columns

## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#useful-for)Useful for

- Building form layouts where you want more than one field on the same row.

- Organizing content into a grid-like layout with columns and rows with consistent alignment and spacing.

- Creating responsive layouts with consistent spacing.

## [Anchor to considerations](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/grid#considerations)Considerations

- Grid doesn't include any padding by default. If you need padding around your grid, use `base` to apply the default padding.

- Grid will allow children to overflow unless template rows/columns are properly set.

- Grid will always wrap children to a new line. If you need to control the wrapping behavior, use `s-stack` or `s-box`.

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)