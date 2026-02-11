---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/actions/menu",
    "fetched_at": "2026-02-10T13:29:29.440050",
    "status": 200,
    "size_bytes": 282109
  },
  "metadata": {
    "title": "Menu",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "actions",
    "component": "menu"
  }
}
---

# Menu

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# MenuAsk assistantUse Menu to display a list of actions that can be performed on a resource.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/actions/menu#properties)Properties[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/actions/menu#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the element. When set, it will be announced using assistive technologies and provide additional context.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/actions/menu#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/actions/menu#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The Menu items.

Only accepts `Button` and `Section` components.

ExamplesCodejsxhtmlCopy991234567891011<>  <s-button commandFor="customer-menu">Edit customer</s-button>  <s-menu id="customer-menu" accessibilityLabel="Customer actions">    <s-button icon="merge">Merge customer</s-button>    <s-button icon="incoming">Request customer data</s-button>    <s-button icon="delete" tone="critical">      Delete customer    </s-button>  </s-menu></>## Preview### Examples- #### Codejsx```

<>

<s-button commandFor="customer-menu">Edit customer</s-button>

<s-menu id="customer-menu" accessibilityLabel="Customer actions">

<s-button icon="merge">Merge customer</s-button>

<s-button icon="incoming">Request customer data</s-button>

<s-button icon="delete" tone="critical">

Delete customer

</s-button>

</s-menu>

</>

```html```

<s-button commandFor="customer-menu">Edit customer</s-button>

<s-menu id="customer-menu" accessibilityLabel="Customer actions">

<s-button icon="merge">Merge customer</s-button>

<s-button icon="incoming">Request customer data</s-button>

<s-button icon="delete" tone="critical">Delete customer</s-button>

</s-menu>

```- #### Basic MenuDescriptionDemonstrates a simple menu with basic action buttons and shows how to link it to a trigger button.jsx```

<>

<s-button commandFor="product-menu">Product actions</s-button>

<s-menu id="product-menu" accessibilityLabel="Product actions">

<s-button icon="edit">Edit product</s-button>

<s-button icon="duplicate">Duplicate product</s-button>

<s-button icon="archive">Archive product</s-button>

</s-menu>

</>

```html```

<s-button commandFor="product-menu">Product actions</s-button>

<s-menu id="product-menu" accessibilityLabel="Product actions">

<s-button icon="edit">Edit product</s-button>

<s-button icon="duplicate">Duplicate product</s-button>

<s-button icon="archive">Archive product</s-button>

</s-menu>

```- #### Menu with IconsDescriptionIllustrates a menu with icons for each action, providing visual context for different menu items and showing how to use the caret-down icon on the trigger button.jsx```

<>

<s-button icon="caret-down" commandFor="actions-menu">

More actions

</s-button>

<s-menu id="actions-menu" accessibilityLabel="Product actions menu">

<s-button icon="edit">Edit product</s-button>

<s-button icon="duplicate">Duplicate product</s-button>

<s-button icon="archive">Archive product</s-button>

<s-button icon="delete" tone="critical">

Delete product

</s-button>

</s-menu>

</>

```html```

<s-button icon="caret-down" commandFor="actions-menu">More actions</s-button>

<s-menu id="actions-menu" accessibilityLabel="Product actions menu">

<s-button icon="edit">Edit product</s-button>

<s-button icon="duplicate">Duplicate product</s-button>

<s-button icon="archive">Archive product</s-button>

<s-button icon="delete" tone="critical">Delete product</s-button>

</s-menu>

```- #### Menu with SectionsDescriptionShows how to organize menu items into logical sections with headings, helping to group related actions and improve menu readability.jsx```

<>

<s-button commandFor="organized-menu">Bulk actions</s-button>

<s-menu id="organized-menu" accessibilityLabel="Organized menu">

<s-section heading="Product actions">

<s-button icon="edit">Edit selected</s-button>

<s-button icon="duplicate">Duplicate selected</s-button>

<s-button icon="archive">Archive selected</s-button>

</s-section>

<s-section heading="Export options">

<s-button icon="export">Export as CSV</s-button>

<s-button icon="print">Print barcodes</s-button>

</s-section>

</s-menu>

</>

```html```

<s-button commandFor="organized-menu">Bulk actions</s-button>

<s-menu id="organized-menu" accessibilityLabel="Organized menu">

<s-section heading="Product actions">

<s-button icon="edit">Edit selected</s-button>

<s-button icon="duplicate">Duplicate selected</s-button>

<s-button icon="archive">Archive selected</s-button>

</s-section>

<s-section heading="Export options">

<s-button icon="export">Export as CSV</s-button>

<s-button icon="print">Print barcodes</s-button>

</s-section>

</s-menu>

```- #### Menu with Links and Disabled ItemsDescriptionDemonstrates a menu with a mix of link-based buttons, standard buttons, and a disabled button, showcasing the menu's flexibility in handling different interaction states.jsx```

<>

<s-button commandFor="mixed-menu">Options</s-button>

<s-menu id="mixed-menu" accessibilityLabel="Mixed menu options">

<s-button href="javascript:void(0)" target="_blank">

View product page

</s-button>

<s-button disabled>Unavailable action</s-button>

<s-button download="sales-report.csv" href="/reports/sales-report.csv">

Download report

</s-button>

</s-menu>

</>

```html```

<s-button commandFor="mixed-menu">Options</s-button>

<s-menu id="mixed-menu" accessibilityLabel="Mixed menu options">

<s-button href="javascript:void(0)" target="_blank">

View product page

</s-button>

<s-button disabled>Unavailable action</s-button>

<s-button download href="javascript:void(0)">Download report</s-button>

</s-menu>

```- #### Actions menu with sectionsDescriptionPresents a comprehensive menu showing how to create sections with different action groups and include a critical action at the menu's root level.jsx```

<>

<s-button commandFor="customer-menu">Edit customer</s-button>

<s-menu id="customer-menu" accessibilityLabel="Customer actions">

<s-section heading="Customer management">

<s-button icon="edit">Edit customer</s-button>

<s-button icon="email">Send email</s-button>

<s-button icon="order">View orders</s-button>

</s-section>

<s-section heading="Account actions">

<s-button icon="reset">Reset password</s-button>

<s-button icon="lock">Disable account</s-button>

</s-section>

<s-button tone="critical" icon="delete">

Delete customer

</s-button>

</s-menu>

</>

```html```

<s-button commandFor="customer-menu">Edit customer</s-button>

<s-menu id="customer-menu" accessibilityLabel="Customer actions">

<s-section heading="Customer management">

<s-button icon="edit">Edit customer</s-button>

<s-button icon="email">Send email</s-button>

<s-button icon="order">View orders</s-button>

</s-section>

<s-section heading="Account actions">

<s-button icon="reset">Reset password</s-button>

<s-button icon="lock">Disable account</s-button>

</s-section>

<s-button tone="critical" icon="delete">Delete customer</s-button>

</s-menu>

```- #### Menu with nested sectionsDescriptionIllustrates a complex menu with nested sections, demonstrating how to organize multiple related actions with icons.jsx```

<>

<s-button icon="settings" commandFor="admin-settings">

Settings

</s-button>

<s-menu id="admin-settings" accessibilityLabel="Settings menu">

<s-section heading="Account">

<s-button icon="profile">Profile settings</s-button>

<s-button icon="lock">Security</s-button>

<s-button>Billing information</s-button>

</s-section>

<s-section heading="Store">

<s-button icon="store">Store settings</s-button>

<s-button>Payment providers</s-button>

<s-button icon="delivery">Shipping rates</s-button>

</s-section>

<s-button href="javascript:void(0)" icon="person-exit">Sign out</s-button>

</s-menu>

</>

```html```

<s-button icon="settings" commandFor="admin-settings">Settings</s-button>

<s-menu id="admin-settings" accessibilityLabel="Settings menu">

<s-section heading="Account">

<s-button icon="profile">Profile settings</s-button>

<s-button icon="lock">Security</s-button>

<s-button>Billing information</s-button>

</s-section>

<s-section heading="Store">

<s-button icon="store">Store settings</s-button>

<s-button>Payment providers</s-button>

<s-button icon="delivery">Shipping rates</s-button>

</s-section>

<s-button href="javascript:void(0)" icon="person-exit">Sign out</s-button>

</s-menu>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/actions/menu#useful-for)Useful for

- Presenting a set of actions or selectable options to merchants

- Creating dropdown menus with related actions

- Organizing actions into logical groupings using sections

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/actions/menu#best-practices)Best practices

- Use for secondary or less important actions since they're hidden until merchants open them

- Contain actions that are related to each other

## [Anchor to content-guidelines](/docs/api/admin-extensions/latest/polaris-web-components/actions/menu#content-guidelines)Content guidelines

- Each item should be clear and predictable

- Lead with a strong verb using the {verb}+{noun} format (e.g., "Buy shipping label", "Edit HTML")

- Avoid unnecessary words and articles like "the", "an", or "a"

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)