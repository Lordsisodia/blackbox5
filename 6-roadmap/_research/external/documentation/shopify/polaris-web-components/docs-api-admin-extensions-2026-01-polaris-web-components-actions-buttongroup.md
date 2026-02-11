---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/actions/buttongroup",
    "fetched_at": "2026-02-10T13:29:20.415997",
    "status": 200,
    "size_bytes": 266958
  },
  "metadata": {
    "title": "ButtonGroup",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "actions",
    "component": "buttongroup"
  }
}
---

# ButtonGroup

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# ButtonGroupAsk assistantDisplays multiple buttons in a layout.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/actions/buttongroup#properties)Properties[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/actions/buttongroup#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**Label for the button group that describes the content of the group for screen reader users to understand what's included.

[Anchor to gap](/docs/api/admin-extensions/latest/polaris-web-components/actions/buttongroup#properties-propertydetail-gap)gap**gap**"base" | "none"**"base" | "none"**Default: 'base'**Default: 'base'**The gap between elements.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/actions/buttongroup#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/actions/buttongroup#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the ButtonGroup.

[Anchor to primary-action](/docs/api/admin-extensions/latest/polaris-web-components/actions/buttongroup#slots-propertydetail-primaryaction)primary-action**primary-action**HTMLElement**HTMLElement**The primary action button for the group. Accepts a single Button element with a `variant` of `primary`. Cannot be used when gap="none".

[Anchor to secondary-actions](/docs/api/admin-extensions/latest/polaris-web-components/actions/buttongroup#slots-propertydetail-secondaryactions)secondary-actions**secondary-actions**HTMLElement**HTMLElement**Secondary action buttons for the group. Accepts Button or PressButton elements with a `variant` of `secondary` or `auto`.

ExamplesCodejsxhtmlCopy91234<s-button-group>  <s-button slot="primary-action">Save</s-button>  <s-button slot="secondary-actions">Cancel</s-button></s-button-group>## Preview### Examples- #### Codejsx```

<s-button-group>

<s-button slot="primary-action">Save</s-button>

<s-button slot="secondary-actions">Cancel</s-button>

</s-button-group>

```html```

<s-button-group>

<s-button slot="primary-action">Save</s-button>

<s-button slot="secondary-actions">Cancel</s-button>

</s-button-group>

```- #### Basic usageDescriptionStandard button group with cancel and primary action for form workflows.jsx```

<s-button-group>

<s-button slot="secondary-actions">Cancel</s-button>

<s-button slot="primary-action" variant="primary">

Save

</s-button>

</s-button-group>

```html```

<s-button-group>

<s-button slot="secondary-actions">Cancel</s-button>

<s-button slot="primary-action" variant="primary">Save</s-button>

</s-button-group>

```- #### Bulk action buttonsDescriptionAction buttons for selected items with destructive option.jsx```

<s-button-group>

<s-button slot="secondary-actions">Archive</s-button>

<s-button slot="secondary-actions">Export</s-button>

<s-button slot="secondary-actions" tone="critical">

Delete

</s-button>

</s-button-group>

```html```

<s-button-group>

<s-button slot="secondary-actions">Archive</s-button>

<s-button slot="secondary-actions">Export</s-button>

<s-button slot="secondary-actions" tone="critical">Delete</s-button>

</s-button-group>

```- #### Form action buttonsDescriptionTypical form completion actions with clear visual hierarchy.jsx```

<s-button-group>

<s-button slot="secondary-actions">Cancel</s-button>

<s-button slot="primary-action" variant="primary">

Save product

</s-button>

</s-button-group>

```html```

<s-button-group>

<s-button slot="secondary-actions">Cancel</s-button>

<s-button slot="primary-action" variant="primary">Save product</s-button>

</s-button-group>

```- #### Buttons with iconsDescriptionIcon-labeled buttons for common actions.jsx```

<s-button-group>

<s-button slot="secondary-actions" icon="duplicate">

Duplicate

</s-button>

<s-button slot="secondary-actions" icon="archive">

Archive

</s-button>

<s-button slot="secondary-actions" icon="delete" tone="critical">

Delete

</s-button>

</s-button-group>

```html```

<s-button-group>

<s-button slot="secondary-actions" icon="duplicate">Duplicate</s-button>

<s-button slot="secondary-actions" icon="archive">Archive</s-button>

<s-button slot="secondary-actions" icon="delete" tone="critical">

Delete

</s-button>

</s-button-group>

```- #### Segmented appearanceDescriptionTightly grouped buttons for view switching and filter options.jsx```

<s-button-group gap="none">

<s-button slot="secondary-actions">Day</s-button>

<s-button slot="secondary-actions">Week</s-button>

<s-button slot="secondary-actions">Month</s-button>

</s-button-group>

```html```

<s-button-group gap="none">

<s-button slot="secondary-actions">Day</s-button>

<s-button slot="secondary-actions">Week</s-button>

<s-button slot="secondary-actions">Month</s-button>

</s-button-group>

```- #### Destructive actions patternDescriptionConfirmation dialog style with cancel option and destructive action.jsx```

<s-button-group>

<s-button slot="secondary-actions">Cancel</s-button>

<s-button slot="secondary-actions" tone="critical">

Delete product

</s-button>

</s-button-group>

```html```

<s-button-group>

<s-button slot="secondary-actions">Cancel</s-button>

<s-button slot="secondary-actions" tone="critical">Delete product</s-button>

</s-button-group>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/actions/buttongroup#useful-for)Useful for

- Accessing related actions in a consistent layout

- Making secondary actions visible alongside primary actions

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/actions/buttongroup#best-practices)Best practices

- Group together related calls to action

- Avoid too many actions that may cause uncertainty

- Consider how buttons will work on small screens

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)