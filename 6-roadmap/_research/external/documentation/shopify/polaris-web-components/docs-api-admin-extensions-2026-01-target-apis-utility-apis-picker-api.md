---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/target-apis/utility-apis/picker-api",
    "fetched_at": "2026-02-10T13:31:34.633826",
    "status": 200,
    "size_bytes": 266718
  },
  "metadata": {
    "title": "Picker API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "utility-apis",
    "component": "picker-api"
  }
}
---

# Picker API

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# Picker APIAsk assistantRequires an Admin [block](/docs/api/admin-extensions/2026-01extension-targets#block-locations), [action](/docs/api/admin-extensions/2026-01extension-targets#action-locations), or [print](/docs/api/admin-extensions/2026-01extension-targets#print-locations) extension.**Requires an Admin [block](/docs/api/admin-extensions/2026-01extension-targets#block-locations), [action](/docs/api/admin-extensions/2026-01extension-targets#action-locations), or [print](/docs/api/admin-extensions/2026-01extension-targets#print-locations) extension.:**The Picker API provides a search-based interface to help users find and select one or more resources that you provide, such as product reviews, email templates, or subscription options, and then returns the selected resource ids to your extension.

TipIf you are picking products, product variants, or collections, you should use the [Resource Picker](/docs/api/admin-extensions/latest/target-apis/utility-apis/picker-api/resource-picker) API instead.**Tip:** If you are picking products, product variants, or collections, you should use the [Resource Picker](/docs/api/admin-extensions/latest/target-apis/utility-apis/picker-api/resource-picker) API instead.**Tip:** If you are picking products, product variants, or collections, you should use the <a href="resource-picker">Resource Picker</a> API instead.## [Anchor to picker](/docs/api/admin-extensions/latest/target-apis/utility-apis/picker-api#picker)picker([options](#picker-propertydetail-options)**[options](#picker-propertydetail-options)**)The `picker` API is a function that accepts an options argument for configuration and returns a Promise that resolves to the picker instance once the picker modal is opened.

### [Anchor to picker-parameters](/docs/api/admin-extensions/latest/target-apis/utility-apis/picker-api#picker-parameters)Parameters[Anchor to options](/docs/api/admin-extensions/latest/target-apis/utility-apis/picker-api#picker-propertydetail-options)options**options**PickerOptionsPickerOptions**PickerOptionsPickerOptions**required**required**### [Anchor to picker-returns](/docs/api/admin-extensions/latest/target-apis/utility-apis/picker-api#picker-returns)ReturnsPromise<PickerPicker>**Promise<PickerPicker>**### PickerOptions- headersThe data headers for the picker. These are used to display the table headers in the picker modal.```

Header[]

```- headingThe heading of the picker. This is displayed in the title of the picker modal.```

string

```- itemsThe items to display in the picker. These are used to display the rows in the picker modal.```

Item[]

```- multipleThe data headers for the picker. These are used to display the table headers in the picker modal.```

boolean | number

``````

interface PickerOptions {

/**

* The heading of the picker. This is displayed in the title of the picker modal.

*/

heading: string;

/**

* The data headers for the picker. These are used to display the table headers in the picker modal.

*/

multiple?: boolean | number;

/**

* The items to display in the picker. These are used to display the rows in the picker modal.

*/

items: Item[];

/**

* The data headers for the picker. These are used to display the table headers in the picker modal.

*/

headers?: Header[];

}

```### Header- contentThe content to display in the table column header.```

string

```- typeThe type of data to display in the column. The type is used to format the data in the column. If the type is 'number', the data in the column will be right-aligned, this should be used when referencing currency or numeric values. If the type is 'string', the data in the column will be left-aligned.```

'string' | 'number'

``````

interface Header {

/**

* The content to display in the table column header.

*/

content?: string;

/**

* The type of data to display in the column. The type is used to format the data in the column.

* If the type is 'number', the data in the column will be right-aligned, this should be used when referencing currency or numeric values.

* If the type is 'string', the data in the column will be left-aligned.

* @defaultValue 'string'

*/

type?: 'string' | 'number';

}

```### Item- badgesThe badges to display in the first column of the row. These are used to display additional information about the item, such as progress of an action or tone indicating the status of that item.```

PickerBadge[]

```- dataThe additional content to display in the second and third columns of the row, if provided.```

DataPoint[]

```- disabledWhether the item is disabled or not. If the item is disabled, it cannot be selected.```

boolean

```- headingThe primary content to display in the first column of the row.```

string

```- idThe unique identifier of the item. This will be returned by the picker if selected.```

string

```- selectedWhether the item is selected or not when the picker is opened. The user may deselect the item if it is preselected.```

boolean

```- thumbnailThe thumbnail to display at the start of the row. This is used to display an image or icon for the item.```

{ url: string; }

``````

interface Item {

/**

* The unique identifier of the item. This will be returned by the picker if selected.

*/

id: string;

/**

* The primary content to display in the first column of the row.

*/

heading: string;

/**

* The additional content to display in the second and third columns of the row, if provided.

*/

data?: DataPoint[];

/**

* Whether the item is disabled or not. If the item is disabled, it cannot be selected.

* @defaultValue false

*/

disabled?: boolean;

/**

* Whether the item is selected or not when the picker is opened. The user may deselect the item if it is preselected.

*/

selected?: boolean;

/**

* The badges to display in the first column of the row. These are used to display additional information about the item, such as progress of an action or tone indicating the status of that item.

*/

badges?: PickerBadge[];

/**

* The thumbnail to display at the start of the row. This is used to display an image or icon for the item.

*/

thumbnail?: {url: string};

}

```### PickerBadge- content```

string

```- progress```

Progress

```- tone```

Tone

``````

interface PickerBadge {

content: string;

tone?: Tone;

progress?: Progress;

}

```### Progress```

'incomplete' | 'partiallyComplete' | 'complete'

```### Tone```

'info' | 'success' | 'warning' | 'critical'

```### DataPoint```

string | number | undefined

```### Picker- selectedA Promise that resolves with the selected item IDs when the user presses the "Select" button in the picker.```

Promise<string[] | undefined>

``````

interface Picker {

/**

* A Promise that resolves with the selected item IDs when the user presses the "Select" button in the picker.

*/

selected: Promise<string[] | undefined>;

}

```ExamplesPicker## js Copy9912345678910111213141516171819202122232425262728293031323334353637const {picker} = useApi(TARGET);const pickerInstance = await picker({  heading: 'Select a template',  multiple: false,  headers: [    {title: 'Templates'},    {title: 'Created by'},    {title: 'Times used', type: 'number'},  ],  items: [    {      id: '1',      heading: 'Full width, 1 column',      data: ['Karine Ruby', '0'],      badges: [{content: 'Draft', tone: 'info'}, {content: 'Marketing'}],    },    {      id: '2',      heading: 'Large graphic, 3 column',      data: ['Russell Winfield', '5'],      badges: [        {content: 'Published', tone: 'success'},        {content: 'New feature'},      ],      selected: true,    },    {      id: '3',      heading: 'Promo header, 2 column',      data: ['Russel Winfield', '10'],      badges: [{content: 'Published', tone: 'success'}],    },  ],});const selected = await pickerInstance.selected;## Preview### Examples- #### Pickerjs```

const {picker} = useApi(TARGET);

const pickerInstance = await picker({

heading: 'Select a template',

multiple: false,

headers: [

{title: 'Templates'},

{title: 'Created by'},

{title: 'Times used', type: 'number'},

],

items: [

{

id: '1',

heading: 'Full width, 1 column',

data: ['Karine Ruby', '0'],

badges: [{content: 'Draft', tone: 'info'}, {content: 'Marketing'}],

},

{

id: '2',

heading: 'Large graphic, 3 column',

data: ['Russell Winfield', '5'],

badges: [

{content: 'Published', tone: 'success'},

{content: 'New feature'},

],

selected: true,

},

{

id: '3',

heading: 'Promo header, 2 column',

data: ['Russel Winfield', '10'],

badges: [{content: 'Published', tone: 'success'}],

},

],

});

const selected = await pickerInstance.selected;

```- #### Simple pickerDescriptionMinimal required fields picker configuration.

If you don't provide the required options (`heading` and `items`), the picker will not open and an error will be logged.Default```

const pickerInstance = await picker({

heading: 'Select an item',

headers: [{title: 'Main heading'}],

items: [

{

id: '1',

heading: 'Item 1',

},

{

id: '2',

heading: 'Item 2',

},

],

});

const selected = await pickerInstance.selected;

```- #### Limited selectable itemsDescriptionSetting a specific number of selectable items. In this example, the user can select up to 2 items.Default```

const pickerInstance = await picker({

heading: 'Select items (up to 2)',

multiple: 2,

headers: [{title: 'Main heading'}],

items: [

{

id: '1',

heading: 'Item 1',

},

{

id: '2',

heading: 'Item 2',

},

{

id: '3',

heading: 'Item 3',

},

],

});

const selected = await pickerInstance.selected;

```- #### Unlimited selectable itemsDescriptionSetting an unlimited number of selectable items.Default```

const pickerInstance = await picker({

heading: 'Select items',

multiple: true,

headers: [{title: 'Main heading'}],

items: [

{

id: '1',

heading: 'Item 1',

},

{

id: '2',

heading: 'Item 2',

},

{

id: '3',

heading: 'Item 3',

},

],

});

const selected = await pickerInstance.selected;

```- #### Preselected itemsDescriptionProviding preselected items in the picker. These will be selected when the picker opens but can be deselected by the user.Default```

const pickerInstance = await picker({

heading: 'Preselected items',

items: [

{

id: '1',

heading: 'Item 1',

selected: true,

},

{

id: '2',

heading: 'Item 2',

},

],

});

const selected = await pickerInstance.selected;

```- #### Disabled itemsDescriptionProviding disabled items in the picker. These will be disabled and cannot be selected by the user.Default```

const pickerInstance = await picker({

heading: 'Disabled items',

items: [

{

id: '1',

heading: 'Item 1',

disabled: true,

},

{

id: '2',

heading: 'Item 2',

},

],

});

const selected = await pickerInstance.selected;

```## [Anchor to related](/docs/api/admin-extensions/latest/target-apis/utility-apis/picker-api#related)Related[APIsResource Picker APIAPIsResource Picker API](/docs/api/admin-extensions/latest/target-apis/utility-apis/resource-picker)[APIs - Resource Picker API](resource-picker)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)