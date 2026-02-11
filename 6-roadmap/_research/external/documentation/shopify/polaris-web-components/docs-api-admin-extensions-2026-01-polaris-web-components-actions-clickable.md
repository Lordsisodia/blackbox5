---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/actions/clickable",
    "fetched_at": "2026-02-10T13:29:24.327228",
    "status": 200,
    "size_bytes": 352797
  },
  "metadata": {
    "title": "Clickable",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "actions",
    "component": "clickable"
  }
}
---

# Clickable

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# ClickableAsk assistantA generic interactive container component that provides a flexible alternative for custom interactive elements not achievable with existing components like Button or Link. Use it to apply specific styling such as backgrounds, padding, or borders.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties)Properties[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the element. When set, it will be announced to users using assistive technologies and will provide them with more context.

Only use this when the element's content is not enough context for users using assistive technologies.

[Anchor to accessibilityRole](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-accessibilityrole)accessibilityRole**accessibilityRole**AccessibilityRoleAccessibilityRole**AccessibilityRoleAccessibilityRole**Default: 'generic'**Default: 'generic'**Sets the semantic meaning of the component’s content. When set, the role will be used by assistive technologies to help users navigate the page.

[Anchor to accessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-accessibilityvisibility)accessibilityVisibility**accessibilityVisibility**"visible" | "hidden" | "exclusive"**"visible" | "hidden" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the element.

- `visible`: the element is visible to all users.

- `hidden`: the element is removed from the accessibility tree but remains visible.

- `exclusive`: the element is visually hidden but remains in the accessibility tree.

[Anchor to background](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-background)background**background**BackgroundColorKeywordBackgroundColorKeyword**BackgroundColorKeywordBackgroundColorKeyword**Default: 'transparent'**Default: 'transparent'**Adjust the background of the component.

[Anchor to blockSize](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-blocksize)blockSize**blockSize**SizeUnitsOrAutoSizeUnitsOrAuto**SizeUnitsOrAutoSizeUnitsOrAuto**Default: 'auto'**Default: 'auto'**Adjust the [block size](https://developer.mozilla.org/en-US/docs/Web/CSS/block-size).

[Anchor to border](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-border)border**border**BorderShorthandBorderShorthand**BorderShorthandBorderShorthand**Default: 'none' - equivalent to `none base auto`.**Default: 'none' - equivalent to `none base auto`.**Set the border via the shorthand property.

This can be a size, optionally followed by a color, optionally followed by a style.

If the color is not specified, it will be `base`.

If the style is not specified, it will be `auto`.

Values can be overridden by `borderWidth`, `borderStyle`, and `borderColor`.

[Anchor to borderColor](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-bordercolor)borderColor**borderColor**"" | ColorKeywordColorKeyword**"" | ColorKeywordColorKeyword**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the color of the border.

[Anchor to borderRadius](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-borderradius)borderRadius**borderRadius**MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderRadiiBoxBorderRadii>**MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderRadiiBoxBorderRadii>**Default: 'none'**Default: 'none'**Adjust the radius of the border.

[Anchor to borderStyle](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-borderstyle)borderStyle**borderStyle**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderStylesBoxBorderStyles>**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderStylesBoxBorderStyles>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the style of the border.

[Anchor to borderWidth](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-borderwidth)borderWidth**borderWidth**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<"small" | "small-100" | "base" | "large" | "large-100" | "none">**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<"small" | "small-100" | "base" | "large" | "large-100" | "none">**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the width of the border.

[Anchor to command](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-command)command**command**'--auto' | '--show' | '--hide' | '--toggle'**'--auto' | '--show' | '--hide' | '--toggle'**Default: '--auto'**Default: '--auto'**Sets the action the [command](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#command) should take when this clickable is activated.

See the documentation of particular components for the actions they support.

- `--auto`: a default action for the target component.

- `--show`: shows the target component.

- `--hide`: hides the target component.

- `--toggle`: toggles the target component.

[Anchor to commandFor](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-commandfor)commandFor**commandFor**string**string**Sets the element the [commandFor](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#commandfor) should act on when this clickable is activated.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-disabled)disabled**disabled**boolean**boolean**Disables the clickable, meaning it cannot be clicked or receive focus.

In this state, onClick will not fire. If the click event originates from a child element, the event will immediately stop propagating from this element.

However, items within the clickable can still receive focus and be interacted with.

This has no impact on the visual state by default, but developers are encouraged to style the clickable accordingly.

[Anchor to display](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-display)display**display**MaybeResponsiveMaybeResponsive<"auto" | "none">**MaybeResponsiveMaybeResponsive<"auto" | "none">**Default: 'auto'**Default: 'auto'**Sets the outer [display](https://developer.mozilla.org/en-US/docs/Web/CSS/display) type of the component. The outer type sets a component's participation in [flow layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flow_layout).

- `auto` the component's initial value. The actual value depends on the component and context.

- `none` hides the component from display and removes it from the accessibility tree, making it invisible to screen readers.

[Anchor to download](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-download)download**download**string**string**Causes the browser to treat the linked URL as a download with the string being the file name. Download only works for same-origin URLs or the `blob:` and `data:` schemes.

[Anchor to href](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-href)href**href**string**string**The URL to link to.

- If set, it will navigate to the location specified by `href` after executing the `click` event.

- If a `commandFor` is set, the `command` will be executed instead of the navigation.

[Anchor to inlineSize](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-inlinesize)inlineSize**inlineSize**SizeUnitsOrAutoSizeUnitsOrAuto**SizeUnitsOrAutoSizeUnitsOrAuto**Default: 'auto'**Default: 'auto'**Adjust the [inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/inline-size).

[Anchor to interestFor](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-interestfor)interestFor**interestFor**string**string**Sets the element the [interestFor](https://open-ui.org/components/interest-invokers.explainer/#the-pitch-in-code) should act on when this clickable is activated.

[Anchor to loading](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-loading)loading**loading**boolean**boolean**Disables the clickable, and indicates to assistive technology that the loading is in progress.

This also disables the clickable.

[Anchor to maxBlockSize](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-maxblocksize)maxBlockSize**maxBlockSize**SizeUnitsOrNoneSizeUnitsOrNone**SizeUnitsOrNoneSizeUnitsOrNone**Default: 'none'**Default: 'none'**Adjust the [maximum block size](https://developer.mozilla.org/en-US/docs/Web/CSS/max-block-size).

[Anchor to maxInlineSize](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-maxinlinesize)maxInlineSize**maxInlineSize**SizeUnitsOrNoneSizeUnitsOrNone**SizeUnitsOrNoneSizeUnitsOrNone**Default: 'none'**Default: 'none'**Adjust the [maximum inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/max-inline-size).

[Anchor to minBlockSize](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-minblocksize)minBlockSize**minBlockSize**SizeUnitsSizeUnits**SizeUnitsSizeUnits**Default: '0'**Default: '0'**Adjust the [minimum block size](https://developer.mozilla.org/en-US/docs/Web/CSS/min-block-size).

[Anchor to minInlineSize](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-mininlinesize)minInlineSize**minInlineSize**SizeUnitsSizeUnits**SizeUnitsSizeUnits**Default: '0'**Default: '0'**Adjust the [minimum inline size](https://developer.mozilla.org/en-US/docs/Web/CSS/min-inline-size).

[Anchor to overflow](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-overflow)overflow**overflow**"visible" | "hidden"**"visible" | "hidden"**Default: 'visible'**Default: 'visible'**Sets the overflow behavior of the element.

- `hidden`: clips the content when it is larger than the element’s container. The element will not be scrollable and the users will not be able to access the clipped content by dragging or using a scroll wheel on a mouse.

- `visible`: the content that extends beyond the element’s container is visible.

[Anchor to padding](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-padding)padding**padding**MaybeResponsiveMaybeResponsive<MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: 'none'**Default: 'none'**Adjust the padding of all edges.

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

[Anchor to paddingBlock](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-paddingblock)paddingBlock**paddingBlock**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-padding.

- `large none` means block-start padding is `large`, block-end padding is `none`.

This overrides the block value of `padding`.

`paddingBlock` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingBlockEnd](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-paddingblockend)paddingBlockEnd**paddingBlockEnd**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-end padding.

This overrides the block-end value of `paddingBlock`.

`paddingBlockEnd` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingBlockStart](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-paddingblockstart)paddingBlockStart**paddingBlockStart**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the block-start padding.

This overrides the block-start value of `paddingBlock`.

`paddingBlockStart` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInline](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-paddinginline)paddingInline**paddingInline**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**MaybeResponsiveMaybeResponsive<"" | MaybeTwoValuesShorthandPropertyMaybeTwoValuesShorthandProperty<PaddingKeywordPaddingKeyword>>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline padding.

- `large none` means inline-start padding is `large`, inline-end padding is `none`.

This overrides the inline value of `padding`.

`paddingInline` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInlineEnd](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-paddinginlineend)paddingInlineEnd**paddingInlineEnd**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline-end padding.

This overrides the inline-end value of `paddingInline`.

`paddingInlineEnd` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to paddingInlineStart](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-paddinginlinestart)paddingInlineStart**paddingInlineStart**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**MaybeResponsiveMaybeResponsive<"" | PaddingKeywordPaddingKeyword>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the inline-start padding.

This overrides the inline-start value of `paddingInline`.

`paddingInlineStart` also accepts a [responsive value](/docs/api/app-home/using-polaris-components#responsive-values) string with the supported PaddingKeyword as a query value.

[Anchor to target](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-target)target**target**"auto" | AnyStringAnyString | "_blank" | "_self" | "_parent" | "_top"**"auto" | AnyStringAnyString | "_blank" | "_self" | "_parent" | "_top"**Default: 'auto'**Default: 'auto'**Specifies where to display the linked URL.

[Anchor to type](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#properties-propertydetail-type)type**type**"button" | "reset" | "submit"**"button" | "reset" | "submit"**Default: 'button'**Default: 'button'**The behavior of the Button.

- `submit`: Used to indicate the component acts as a submit button, meaning it submits the closest form.

- `button`: Used to indicate the component acts as a button, meaning it has no default action.

- `reset`: Used to indicate the component acts as a reset button, meaning it resets the closest form (returning fields to their default values).

This property is ignored if the component supports `href` or `commandFor`/`command` and one of them is set.

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

```### AnyStringPrevents widening string literal types in a union to `string`.```

string & {}

```## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to blur](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#events-propertydetail-blur)blur**blur**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**[Anchor to click](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#events-propertydetail-click)click**click**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**[Anchor to focus](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#events-propertydetail-focus)focus**focus**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickable#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Clickable.

ExamplesCodejsxhtmlCopy99123456789101112<>  <s-clickable padding="base">Create Store</s-clickable>  <s-clickable    border="base"    padding="base"    background="subdued"    borderRadius="base"  >    View Shipping Settings  </s-clickable></>## Preview### Examples- #### Codejsx```

<>

<s-clickable padding="base">Create Store</s-clickable>

<s-clickable

border="base"

padding="base"

background="subdued"

borderRadius="base"

>

View Shipping Settings

</s-clickable>

</>

```html```

<s-clickable padding="base">Create Store</s-clickable>

<s-clickable

border="base"

padding="base"

background="subdued"

borderRadius="base"

>

View Shipping Settings

</s-clickable>

```- #### Basic Button UsageDescriptionA simple clickable button with a base border and padding, demonstrating the default button behavior of the Clickable component.jsx```

<s-clickable border="base" padding="base">

Click me

</s-clickable>

```html```

<s-clickable border="base" padding="base">Click me</s-clickable>

```- #### Link ModeDescriptionDemonstrates the Clickable component's ability to function as a link, opening the specified URL in a new browser tab when clicked.jsx```

<s-clickable href="javascript:void(0)" target="_blank">

Visit Shopify

</s-clickable>

```html```

<s-clickable href="javascript:void(0)" target="_blank">

Visit Shopify

</s-clickable>

```- #### Form Submit ButtonDescriptionA disabled submit button that can be used within a form, showing the component's form integration capabilities and disabled state.jsx```

<s-clickable type="submit" disabled border="base" padding="base">

Save changes

</s-clickable>

```html```

<s-clickable type="submit" disabled border="base" padding="base">

Save changes

</s-clickable>

```- #### Section with Clickable ActionDescriptionIllustrates how the Clickable component can be integrated into a section layout to provide an interactive action button.jsx```

<s-box padding="large-400" background="base" borderRadius="small-200">

<s-stack gap="large-300">

<s-heading>Product settings</s-heading>

<s-text>Configure your product inventory and pricing settings.</s-text>

<s-clickable background="base" padding="base" borderRadius="small">

<s-text type="strong">Configure settings</s-text>

</s-clickable>

</s-stack>

</s-box>

```html```

<s-box padding="large-400" background="base" borderRadius="small-200">

<s-stack gap="large-300">

<s-heading>Product settings</s-heading>

<s-text>Configure your product inventory and pricing settings.</s-text>

<s-clickable background="base" padding="base" borderRadius="small">

<s-text type="strong">Configure settings</s-text>

</s-clickable>

</s-stack>

</s-box>

```- #### Accessibility with ARIA AttributesDescriptionDemonstrates the use of an accessibility label to provide context for screen readers, enhancing the component's usability for users with assistive technologies.jsx```

<s-clickable

accessibilityLabel="Delete product winter collection jacket"

background="base"

padding="base"

borderRadius="small"

>

<s-text>Delete</s-text>

</s-clickable>

```html```

<s-clickable

accessibilityLabel="Delete product winter collection jacket"

background="base"

padding="base"

borderRadius="small"

>

<s-text>Delete</s-text>

</s-clickable>

```- #### Disabled Link with ARIADescriptionShows a disabled link with an accessibility label, explaining the unavailability of a feature to users of assistive technologies.jsx```

<s-clickable

href="javascript:void(0)"

disabled

accessibilityLabel="This link is currently unavailable"

>

<s-text>Unavailable feature</s-text>

</s-clickable>

```html```

<s-clickable

href="javascript:void(0)"

disabled

accessibilityLabel="This link is currently unavailable"

>

<s-text>Unavailable feature</s-text>

</s-clickable>

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)