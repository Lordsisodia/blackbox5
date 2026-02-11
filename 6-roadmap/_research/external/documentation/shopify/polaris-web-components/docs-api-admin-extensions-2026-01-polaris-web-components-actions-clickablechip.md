---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/actions/clickablechip",
    "fetched_at": "2026-02-10T13:29:26.038860",
    "status": 200,
    "size_bytes": 283598
  },
  "metadata": {
    "title": "ClickableChip",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "actions",
    "component": "clickablechip"
  }
}
---

# ClickableChip

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# ClickableChipAsk assistantInteractive button used to categorize or highlight content attributes. They are often displayed near the content they classify, enhancing discoverability by allowing users to identify items with similar properties.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#properties)Properties[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the Chip. It will be read to users using assistive technologies such as screen readers.

[Anchor to color](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#properties-propertydetail-color)color**color**ColorKeywordColorKeyword**ColorKeywordColorKeyword**Default: 'base'**Default: 'base'**Modify the color to be more or less intense.

[Anchor to command](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#properties-propertydetail-command)command**command**'--auto' | '--show' | '--hide' | '--toggle'**'--auto' | '--show' | '--hide' | '--toggle'**Default: '--auto'**Default: '--auto'**Sets the action the [command](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#command) should take when this clickable is activated.

See the documentation of particular components for the actions they support.

- `--auto`: a default action for the target component.

- `--show`: shows the target component.

- `--hide`: hides the target component.

- `--toggle`: toggles the target component.

[Anchor to commandFor](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#properties-propertydetail-commandfor)commandFor**commandFor**string**string**Sets the element the [commandFor](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#commandfor) should act on when this clickable is activated.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#properties-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the chip, disallowing any interaction.

[Anchor to hidden](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#properties-propertydetail-hidden)hidden**hidden**boolean**boolean**Default: false**Default: false**Determines whether the chip is hidden.

If this property is being set on each framework render (as in 'controlled' usage), and the chip is `removable`, ensure you update app state for this property when the `remove` event fires.

If the chip is not `removable`, it can still be hidden by setting this property.

[Anchor to href](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#properties-propertydetail-href)href**href**string**string**The URL to link to.

- If set, it will navigate to the location specified by `href` after executing the `click` event.

- If a `commandFor` is set, the `command` will be executed instead of the navigation.

[Anchor to interestFor](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#properties-propertydetail-interestfor)interestFor**interestFor**string**string**Sets the element the [interestFor](https://open-ui.org/components/interest-invokers.explainer/#the-pitch-in-code) should act on when this clickable is activated.

[Anchor to removable](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#properties-propertydetail-removable)removable**removable**boolean**boolean**Default: false**Default: false**Whether the chip is removable.

### ColorKeyword```

'subdued' | 'base' | 'strong'

```## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to afterhide](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#events-propertydetail-afterhide)afterhide**afterhide**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**[Anchor to click](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#events-propertydetail-click)click**click**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**[Anchor to remove](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#events-propertydetail-remove)remove**remove**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the clickable chip.

[Anchor to graphic](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#slots-propertydetail-graphic)graphic**graphic**HTMLElement**HTMLElement**The graphic to display in the clickable chip.

Only accepts `Icon` components.

ExamplesCodejsxhtmlCopy91<s-clickable-chip>Clickable chip</s-clickable-chip>## Preview### Examples- #### Codejsx```

<s-clickable-chip>Clickable chip</s-clickable-chip>

```html```

<s-clickable-chip>Clickable chip</s-clickable-chip>

```- #### Basic UsageDescriptionDemonstrates a simple clickable chip with a base color and interactive functionality.jsx```

<s-stack direction="inline" gap="base">

<s-clickable-chip color="base" accessibilityLabel="Filter by active products">

Active

</s-clickable-chip>

<s-clickable-chip

color="subdued"

accessibilityLabel="Filter by draft products"

>

Draft

</s-clickable-chip>

<s-clickable-chip

color="strong"

accessibilityLabel="Filter by archived products"

>

Archived

</s-clickable-chip>

</s-stack>

```html```

<s-stack direction="inline" gap="base">

<s-clickable-chip color="base" accessibilityLabel="Filter by active products">

Active

</s-clickable-chip>

<s-clickable-chip

color="subdued"

accessibilityLabel="Filter by draft products"

>

Draft

</s-clickable-chip>

<s-clickable-chip

color="strong"

accessibilityLabel="Filter by archived products"

>

Archived

</s-clickable-chip>

</s-stack>

```- #### With Icon and Remove ButtonDescriptionShowcases a strong-colored clickable chip with a check circle icon and a removable state.jsx```

<s-clickable-chip

color="strong"

accessibilityLabel="Remove status filter"

removable

>

<s-icon slot="graphic" type="check-circle" />

In progress

</s-clickable-chip>

```html```

<s-clickable-chip

color="strong"

accessibilityLabel="Remove status filter"

removable

>

<s-icon slot="graphic" type="check-circle"></s-icon>

In progress

</s-clickable-chip>

```- #### As a LinkDescriptionDemonstrates a subdued clickable chip configured as a link with a product icon.jsx```

<s-clickable-chip

color="subdued"

href="javascript:void(0)"

accessibilityLabel="View T-shirt product"

>

<s-icon slot="graphic" type="product" />

T-shirt

</s-clickable-chip>

```html```

<s-clickable-chip

color="subdued"

href="javascript:void(0)"

accessibilityLabel="View T-shirt product"

>

<s-icon slot="graphic" type="product"></s-icon>

T-shirt

</s-clickable-chip>

```- #### Disabled StateDescriptionIllustrates a clickable chip in a disabled state, preventing interaction while displaying an inactive status.jsx```

<s-clickable-chip

color="base"

disabled

accessibilityLabel="Status filter (disabled)"

>

Inactive

</s-clickable-chip>

```html```

<s-clickable-chip

color="base"

disabled

accessibilityLabel="Status filter (disabled)"

>

Inactive

</s-clickable-chip>

```- #### Multiple Chips with Proper SpacingDescriptionDemonstrates how multiple clickable chips with different colors, icons, and states can be arranged using an inline stack for consistent layout and spacing.jsx```

<s-stack direction="inline" gap="base">

<s-clickable-chip accessibilityLabel="Filter by status">

Active

</s-clickable-chip>

<s-clickable-chip

color="strong"

accessibilityLabel="Remove status filter"

removable

>

<s-icon slot="graphic" type="check-circle" />

In progress

</s-clickable-chip>

<s-clickable-chip color="subdued" accessibilityLabel="Filter by category">

<s-icon slot="graphic" type="filter" />

Category

</s-clickable-chip>

</s-stack>

```html```

<s-stack direction="inline" gap="base">

<s-clickable-chip accessibilityLabel="Filter by status">

Active

</s-clickable-chip>

<s-clickable-chip

color="strong"

accessibilityLabel="Remove status filter"

removable

>

<s-icon slot="graphic" type="check-circle"></s-icon>

In progress

</s-clickable-chip>

<s-clickable-chip color="subdued" accessibilityLabel="Filter by category">

<s-icon slot="graphic" type="filter"></s-icon>

Category

</s-clickable-chip>

</s-stack>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#useful-for)Useful for

- Creating interactive filters or tags that can be clicked or removed

- Navigating to related content when configured as a link

- Allowing merchants to dismiss or remove applied filters or selections

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/actions/clickablechip#best-practices)Best practices

- Use for interactive chips that merchants can click or dismiss

- Use Chip component instead for static, non-interactive indicators

- Keep labels short to avoid truncation

- Use color variants to indicate importance (subdued, base, strong)

- Add icons to provide visual context

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)