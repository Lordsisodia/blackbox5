---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/layout-and-structure/table",
    "fetched_at": "2026-02-10T13:30:38.564998",
    "status": 200,
    "size_bytes": 369110
  },
  "metadata": {
    "title": "Table",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "layout-and-structure",
    "component": "table"
  }
}
---

# Table

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# TableAsk assistantDisplay data clearly in rows and columns, helping users view, analyze, and compare information. Automatically renders as a list on small screens and a table on large ones.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#properties)Properties[Anchor to hasNextPage](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#properties-propertydetail-hasnextpage)hasNextPage**hasNextPage**boolean**boolean**Default: false**Default: false**Whether there's an additional page of data.

[Anchor to hasPreviousPage](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#properties-propertydetail-haspreviouspage)hasPreviousPage**hasPreviousPage**boolean**boolean**Default: false**Default: false**Whether there's a previous page of data.

[Anchor to loading](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#properties-propertydetail-loading)loading**loading**boolean**boolean**Default: false**Default: false**Whether the table is in a loading state, such as initial page load or loading the next page in a paginated table. When true, the table could be in an inert state, which prevents user interaction.

[Anchor to paginate](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#properties-propertydetail-paginate)paginate**paginate**boolean**boolean**Default: false**Default: false**Whether to use pagination controls.

[Anchor to variant](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#properties-propertydetail-variant)variant**variant**"auto" | "list"**"auto" | "list"**Default: 'auto'**Default: 'auto'**Sets the layout of the Table.

- `list`: The Table is always displayed as a list.

- `table`: The Table is always displayed as a table.

- `auto`: The Table is displayed as a table on wide devices and as a list on narrow devices.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the Table.

[Anchor to filters](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#slots-propertydetail-filters)filters**filters**HTMLElement**HTMLElement**Additional filters to display in the table. For example, the `s-search-field` component can be used to filter the table data.

## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to nextpage](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#events-propertydetail-nextpage)nextpage**nextpage**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**[Anchor to previouspage](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#events-propertydetail-previouspage)previouspage**previouspage**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```## [Anchor to tablebody](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#tablebody)TableBodyDefine the main content area of a table, containing rows and cells that display data.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The body of the table. May not have any semantic meaning in the Table's `list` variant.

## [Anchor to tablecell](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#tablecell)TableCellDisplay data within a cell in a table row.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of the table cell.

## [Anchor to tableheader](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#tableheader)TableHeaderDisplay column names at the top of a table.

[Anchor to format](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#tableheader-propertydetail-format)format**format**HeaderFormatHeaderFormat**HeaderFormatHeaderFormat**The format of the column. Will automatically apply styling and alignment to cell content based on the value.

- `base`: The base format for columns.

- `currency`: Formats the column as currency.

- `numeric`: Formats the column as a number.

[Anchor to listSlot](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#tableheader-propertydetail-listslot)listSlot**listSlot**ListSlotTypeListSlotType**ListSlotTypeListSlotType**Default: 'labeled'**Default: 'labeled'**Content designation for the table's `list` variant.

- `primary`: The most important content. Only one column can have this designation.

- `secondary`: The secondary content. Only one column can have this designation.

- `kicker`: Content that is displayed before primary and secondary content, but with less visual prominence. Only one column can have this designation.

- `inline`: Content that is displayed inline.

- `labeled`: Each column with this designation displays as a heading-content pair.

### HeaderFormat```

'base' | 'numeric' | 'currency'

```### ListSlotType```

'primary' | 'secondary' | 'kicker' | 'inline' | 'labeled'

```## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The heading of the column in the `table` variant, and the label of its data in `list` variant.

## [Anchor to tableheaderrow](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#tableheaderrow)TableHeaderRowDefine a header row in a table, displaying column names and enabling sorting.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**Contents of the table heading row; children should be `TableHeading` components.

## [Anchor to tablerow](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#tablerow)TableRowDisplay a row of data within the body of a table.

[Anchor to clickDelegate](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#tablerow-propertydetail-clickdelegate)clickDelegate**clickDelegate**string**string**The ID of an interactive element (e.g. `s-link`) in the row that will be the target of the click when the row is clicked. This is the primary action for the row; it should not be used for secondary actions.

This is a click-only affordance, and does not introduce any keyboard or screen reader affordances. Which is why the target element must be in the table; so that keyboard and screen reader users can interact with it normally.

## [Anchor to slots](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#slots)Slots[Anchor to children](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#slots-propertydetail-children)children**children**HTMLElement**HTMLElement**The content of a TableRow, which should be `TableCell` components.

ExamplesCodejsxhtmlCopy99123456789101112131415161718192021222324252627282930<s-section padding="none">  <s-table>    <s-table-header-row>      <s-table-header>Name</s-table-header>      <s-table-header>Email</s-table-header>      <s-table-header format="numeric">Orders placed</s-table-header>      <s-table-header>Phone</s-table-header>    </s-table-header-row>    <s-table-body>      <s-table-row>        <s-table-cell>John Smith</s-table-cell>        <s-table-cell>john@example.com</s-table-cell>        <s-table-cell>23</s-table-cell>        <s-table-cell>123-456-7890</s-table-cell>      </s-table-row>      <s-table-row>        <s-table-cell>Jane Johnson</s-table-cell>        <s-table-cell>jane@example.com</s-table-cell>        <s-table-cell>15</s-table-cell>        <s-table-cell>234-567-8901</s-table-cell>      </s-table-row>      <s-table-row>        <s-table-cell>Brandon Williams</s-table-cell>        <s-table-cell>brandon@example.com</s-table-cell>        <s-table-cell>42</s-table-cell>        <s-table-cell>345-678-9012</s-table-cell>      </s-table-row>    </s-table-body>  </s-table></s-section>## Preview### Examples- #### Codejsx```

<s-section padding="none">

<s-table>

<s-table-header-row>

<s-table-header>Name</s-table-header>

<s-table-header>Email</s-table-header>

<s-table-header format="numeric">Orders placed</s-table-header>

<s-table-header>Phone</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>John Smith</s-table-cell>

<s-table-cell>john@example.com</s-table-cell>

<s-table-cell>23</s-table-cell>

<s-table-cell>123-456-7890</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Jane Johnson</s-table-cell>

<s-table-cell>jane@example.com</s-table-cell>

<s-table-cell>15</s-table-cell>

<s-table-cell>234-567-8901</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Brandon Williams</s-table-cell>

<s-table-cell>brandon@example.com</s-table-cell>

<s-table-cell>42</s-table-cell>

<s-table-cell>345-678-9012</s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```html```

<s-section padding="none">

<s-table>

<s-table-header-row>

<s-table-header>Name</s-table-header>

<s-table-header>Email</s-table-header>

<s-table-header format="numeric">Orders placed</s-table-header>

<s-table-header>Phone</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>John Smith</s-table-cell>

<s-table-cell>john@example.com</s-table-cell>

<s-table-cell>23</s-table-cell>

<s-table-cell>123-456-7890</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Jane Johnson</s-table-cell>

<s-table-cell>jane@example.com</s-table-cell>

<s-table-cell>15</s-table-cell>

<s-table-cell>234-567-8901</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Brandon Williams</s-table-cell>

<s-table-cell>brandon@example.com</s-table-cell>

<s-table-cell>42</s-table-cell>

<s-table-cell>345-678-9012</s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```- #### Basic UsageDescriptionTables expand to full width by default.jsx```

<s-section padding="none">

<s-table>

<s-table-header-row>

<s-table-header listSlot="primary">Product</s-table-header>

<s-table-header listSlot="inline">Status</s-table-header>

<s-table-header listSlot="labeled">Inventory</s-table-header>

<s-table-header listSlot="labeled">Price</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>Water bottle</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>128</s-table-cell>

<s-table-cell>$24.99</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>T-shirt</s-table-cell>

<s-table-cell>

<s-badge tone="warning">Low stock</s-badge>

</s-table-cell>

<s-table-cell>15</s-table-cell>

<s-table-cell>$19.99</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Cutting board</s-table-cell>

<s-table-cell>

<s-badge tone="critical">Out of stock</s-badge>

</s-table-cell>

<s-table-cell>0</s-table-cell>

<s-table-cell>$34.99</s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```html```

<s-section padding="none">

<s-table>

<s-table-header-row>

<s-table-header listSlot="primary">Product</s-table-header>

<s-table-header listSlot="inline">Status</s-table-header>

<s-table-header listSlot="labeled">Inventory</s-table-header>

<s-table-header listSlot="labeled">Price</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>Water bottle</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>128</s-table-cell>

<s-table-cell>$24.99</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>T-shirt</s-table-cell>

<s-table-cell>

<s-badge tone="warning">Low stock</s-badge>

</s-table-cell>

<s-table-cell>15</s-table-cell>

<s-table-cell>$19.99</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Cutting board</s-table-cell>

<s-table-cell>

<s-badge tone="critical">Out of stock</s-badge>

</s-table-cell>

<s-table-cell>0</s-table-cell>

<s-table-cell>$34.99</s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```- #### With PaginationDescriptionAdd pagination controls for navigating large datasets.jsx```

<s-section padding="none">

<s-table paginate hasPreviousPage hasNextPage>

<s-table-header-row>

<s-table-header listSlot="primary">Product</s-table-header>

<s-table-header listSlot="inline">Status</s-table-header>

<s-table-header listSlot="secondary" format="numeric">Sales</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>Product 1</s-table-cell>

<s-table-cell>Active</s-table-cell>

<s-table-cell>250</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Product 2</s-table-cell>

<s-table-cell>Active</s-table-cell>

<s-table-cell>180</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Product 3</s-table-cell>

<s-table-cell>Paused</s-table-cell>

<s-table-cell>95</s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```html```

<s-section padding="none">

<s-table paginate hasPreviousPage hasNextPage>

<s-table-header-row>

<s-table-header listSlot="primary">Product</s-table-header>

<s-table-header listSlot="inline">Status</s-table-header>

<s-table-header listSlot="secondary" format="numeric">Sales</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>Product 1</s-table-cell>

<s-table-cell>Active</s-table-cell>

<s-table-cell>250</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Product 2</s-table-cell>

<s-table-cell>Active</s-table-cell>

<s-table-cell>180</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Product 3</s-table-cell>

<s-table-cell>Paused</s-table-cell>

<s-table-cell>95</s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```- #### With Loading StateDescriptionDisplay a loading state while fetching data.jsx```

<s-section padding="none">

<s-table loading>

<s-table-header-row>

<s-table-header listSlot="primary">Product</s-table-header>

<s-table-header listSlot="inline">Status</s-table-header>

<s-table-header listSlot="labeled">Inventory</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>Water bottle</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>128</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>T-shirt</s-table-cell>

<s-table-cell>

<s-badge tone="warning">Low stock</s-badge>

</s-table-cell>

<s-table-cell>15</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Cutting board</s-table-cell>

<s-table-cell>

<s-badge tone="critical">Out of stock</s-badge>

</s-table-cell>

<s-table-cell>0</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Notebook set</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>245</s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```html```

<s-section padding="none">

<s-table loading>

<s-table-header-row>

<s-table-header listSlot="primary">Product</s-table-header>

<s-table-header listSlot="inline">Status</s-table-header>

<s-table-header listSlot="labeled">Inventory</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>Water bottle</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>128</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>T-shirt</s-table-cell>

<s-table-cell>

<s-badge tone="warning">Low stock</s-badge>

</s-table-cell>

<s-table-cell>15</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Cutting board</s-table-cell>

<s-table-cell>

<s-badge tone="critical">Out of stock</s-badge>

</s-table-cell>

<s-table-cell>0</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Notebook set</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>245</s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```- #### Full-width table with multiple columnsDescriptionDisplay multiple columns in a full-width table.jsx```

<s-section padding="none">

<s-table>

<s-table-header-row>

<s-table-header listSlot="primary">Product</s-table-header>

<s-table-header listSlot="kicker">SKU</s-table-header>

<s-table-header listSlot="inline">Status</s-table-header>

<s-table-header listSlot="labeled" format="numeric">Inventory</s-table-header>

<s-table-header listSlot="labeled" format="currency">Price</s-table-header>

<s-table-header listSlot="labeled">Last updated</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>Water bottle</s-table-cell>

<s-table-cell>WB-001</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>128</s-table-cell>

<s-table-cell>$24.99</s-table-cell>

<s-table-cell>2 hours ago</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>T-shirt</s-table-cell>

<s-table-cell>TS-002</s-table-cell>

<s-table-cell>

<s-badge tone="warning">Low stock</s-badge>

</s-table-cell>

<s-table-cell>15</s-table-cell>

<s-table-cell>$19.99</s-table-cell>

<s-table-cell>1 day ago</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Cutting board</s-table-cell>

<s-table-cell>CB-003</s-table-cell>

<s-table-cell>

<s-badge tone="critical">Out of stock</s-badge>

</s-table-cell>

<s-table-cell>0</s-table-cell>

<s-table-cell>$34.99</s-table-cell>

<s-table-cell>3 days ago</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Notebook set</s-table-cell>

<s-table-cell>NB-004</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>245</s-table-cell>

<s-table-cell>$12.99</s-table-cell>

<s-table-cell>5 hours ago</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Stainless steel straws</s-table-cell>

<s-table-cell>SS-005</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>89</s-table-cell>

<s-table-cell>$9.99</s-table-cell>

<s-table-cell>1 hour ago</s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```html```

<s-section padding="none">

<s-table>

<s-table-header-row>

<s-table-header listSlot="primary">Product</s-table-header>

<s-table-header listSlot="kicker">SKU</s-table-header>

<s-table-header listSlot="inline">Status</s-table-header>

<s-table-header listSlot="labeled" format="numeric">Inventory</s-table-header>

<s-table-header listSlot="labeled" format="currency">Price</s-table-header>

<s-table-header listSlot="labeled">Last updated</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>Water bottle</s-table-cell>

<s-table-cell>WB-001</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>128</s-table-cell>

<s-table-cell>$24.99</s-table-cell>

<s-table-cell>2 hours ago</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>T-shirt</s-table-cell>

<s-table-cell>TS-002</s-table-cell>

<s-table-cell>

<s-badge tone="warning">Low stock</s-badge>

</s-table-cell>

<s-table-cell>15</s-table-cell>

<s-table-cell>$19.99</s-table-cell>

<s-table-cell>1 day ago</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Cutting board</s-table-cell>

<s-table-cell>CB-003</s-table-cell>

<s-table-cell>

<s-badge tone="critical">Out of stock</s-badge>

</s-table-cell>

<s-table-cell>0</s-table-cell>

<s-table-cell>$34.99</s-table-cell>

<s-table-cell>3 days ago</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Notebook set</s-table-cell>

<s-table-cell>NB-004</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>245</s-table-cell>

<s-table-cell>$12.99</s-table-cell>

<s-table-cell>5 hours ago</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>Stainless steel straws</s-table-cell>

<s-table-cell>SS-005</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>89</s-table-cell>

<s-table-cell>$9.99</s-table-cell>

<s-table-cell>1 hour ago</s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```- #### List VariantDescriptionDisplay data using the list variant with specialized slot types. List is the default variant on mobile devices.jsx```

<s-section padding="none">

<s-table variant="list">

<s-table-header-row>

<s-table-header listSlot="kicker">ID</s-table-header>

<s-table-header listSlot="primary">Customer</s-table-header>

<s-table-header listSlot="secondary">Email</s-table-header>

<s-table-header listSlot="inline">Status</s-table-header>

<s-table-header listSlot="labeled" format="numeric">Orders</s-table-header>

<s-table-header listSlot="labeled" format="currency">Total spent</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>#1001</s-table-cell>

<s-table-cell>Sarah Johnson</s-table-cell>

<s-table-cell>sarah@example.com</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>23</s-table-cell>

<s-table-cell>$1,245.50</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>#1002</s-table-cell>

<s-table-cell>Mike Chen</s-table-cell>

<s-table-cell>mike@example.com</s-table-cell>

<s-table-cell>

<s-badge tone="neutral">Inactive</s-badge>

</s-table-cell>

<s-table-cell>7</s-table-cell>

<s-table-cell>$432.75</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>#1003</s-table-cell>

<s-table-cell>Emma Davis</s-table-cell>

<s-table-cell>emma@example.com</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>15</s-table-cell>

<s-table-cell>$892.25</s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```html```

<s-section padding="none">

<s-table variant="list">

<s-table-header-row>

<s-table-header listSlot="kicker">ID</s-table-header>

<s-table-header listSlot="primary">Customer</s-table-header>

<s-table-header listSlot="secondary">Email</s-table-header>

<s-table-header listSlot="inline">Status</s-table-header>

<s-table-header listSlot="labeled" format="numeric">

Orders

</s-table-header>

<s-table-header listSlot="labeled" format="currency">

Total spent

</s-table-header>

</s-table-header-row>

<s-table-body>

<s-table-row>

<s-table-cell>#1001</s-table-cell>

<s-table-cell>Sarah Johnson</s-table-cell>

<s-table-cell>sarah@example.com</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>23</s-table-cell>

<s-table-cell>$1,245.50</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>#1002</s-table-cell>

<s-table-cell>Mike Chen</s-table-cell>

<s-table-cell>mike@example.com</s-table-cell>

<s-table-cell>

<s-badge tone="neutral">Inactive</s-badge>

</s-table-cell>

<s-table-cell>7</s-table-cell>

<s-table-cell>$432.75</s-table-cell>

</s-table-row>

<s-table-row>

<s-table-cell>#1003</s-table-cell>

<s-table-cell>Emma Davis</s-table-cell>

<s-table-cell>emma@example.com</s-table-cell>

<s-table-cell>

<s-badge tone="success">Active</s-badge>

</s-table-cell>

<s-table-cell>15</s-table-cell>

<s-table-cell>$892.25</s-table-cell>

</s-table-row>

</s-table-body>

</s-table>

</s-section>

```## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#best-practices)Best practices

- Use when displaying data with 3 or more attributes per item

- All items should share the same structure and attributes

- Don't use when data varies significantly between items (use a list instead)

- Tables automatically transform into lists on mobile devices

## [Anchor to related](/docs/api/admin-extensions/latest/polaris-web-components/layout-and-structure/table#related)Related[CompositionIndex tableCompositionIndex table](/docs/api/app-home/patterns/compositions/index-table)[Composition - Index table](/docs/api/app-home/patterns/compositions/index-table)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)