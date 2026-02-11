---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/target-apis/utility-apis/resource-picker-api",
    "fetched_at": "2026-02-10T13:28:20.513633",
    "status": 200,
    "size_bytes": 257728
  },
  "metadata": {
    "title": "Resource Picker API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "utility-apis",
    "component": "resource-picker-api"
  }
}
---

# Resource Picker API

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# Resource Picker APIAsk assistantRequires an Admin [block](/docs/api/admin-extensions/2025-07/extension-targets#block-locations), [action](/docs/api/admin-extensions/2025-07/extension-targets#action-locations), or [print](/docs/api/admin-extensions/2025-07/extension-targets#print-locations) extension.**Requires an Admin [block](/docs/api/admin-extensions/2025-07/extension-targets#block-locations), [action](/docs/api/admin-extensions/2025-07/extension-targets#action-locations), or [print](/docs/api/admin-extensions/2025-07/extension-targets#print-locations) extension.:**The Resource Picker API provides a search-based interface to help users find and select one or more products, collections, or product variants, and then returns the selected resources to your app. Both the app and the user must have the necessary permissions to access the resources selected.

TipIf you are picking app resources such as product reviews, email templates, or subscription options, you should use the [Picker](/docs/api/admin-extensions/2025-07/target-apis/utility-apis/resource-picker-api/picker) API instead.**Tip:** If you are picking app resources such as product reviews, email templates, or subscription options, you should use the [Picker](/docs/api/admin-extensions/2025-07/target-apis/utility-apis/resource-picker-api/picker) API instead.**Tip:** If you are picking app resources such as product reviews, email templates, or subscription options, you should use the <a href="picker">Picker</a> API instead.## [Anchor to resource picker options](/docs/api/admin-extensions/2025-07/target-apis/utility-apis/resource-picker-api#resource picker options)Resource Picker OptionsThe `Resource Picker` accepts a variety of options to customize the picker's behavior.

[Anchor to type](/docs/api/admin-extensions/2025-07/target-apis/utility-apis/resource-picker-api#resourcepickeroptions-propertydetail-type)type**type**'product' | 'variant' | 'collection'**'product' | 'variant' | 'collection'**required**required**The type of resource you want to pick.

[Anchor to action](/docs/api/admin-extensions/2025-07/target-apis/utility-apis/resource-picker-api#resourcepickeroptions-propertydetail-action)action**action**'add' | 'select'**'add' | 'select'**Default: 'add'**Default: 'add'**The action verb appears in the title and as the primary action of the Resource Picker.

[Anchor to filter](/docs/api/admin-extensions/2025-07/target-apis/utility-apis/resource-picker-api#resourcepickeroptions-propertydetail-filter)filter**filter**FiltersFilters**FiltersFilters**Filters for what resource to show.

[Anchor to multiple](/docs/api/admin-extensions/2025-07/target-apis/utility-apis/resource-picker-api#resourcepickeroptions-propertydetail-multiple)multiple**multiple**boolean | number**boolean | number**Default: false**Default: false**Whether to allow selecting multiple items of a specific type or not. If a number is provided, then limit the selections to a maximum of that number of items. When type is Product, the user may still select multiple variants of a single product, even if multiple is false.

[Anchor to query](/docs/api/admin-extensions/2025-07/target-apis/utility-apis/resource-picker-api#resourcepickeroptions-propertydetail-query)query**query**string**string**Default: ''**Default: ''**GraphQL initial search query for filtering resources available in the picker. See [search syntax](/docs/api/usage/search-syntax) for more information. This is displayed in the search bar when the picker is opened and can be edited by users. For most use cases, you should use the `filter.query` option instead which doesn't show the query in the UI.

[Anchor to selectionIds](/docs/api/admin-extensions/2025-07/target-apis/utility-apis/resource-picker-api#resourcepickeroptions-propertydetail-selectionids)selectionIds**selectionIds**BaseResourceBaseResource[]**BaseResourceBaseResource[]**Default: []**Default: []**Resources that should be preselected when the picker is opened.

### Filters- archivedWhether to show [archived products](https://help.shopify.com/en/manual/products/details?shpxid=70af7d87-E0F2-4973-8B09-B972AAF0ADFD#product-availability). Only applies to the Product resource type picker. Setting this to undefined will show a badge on draft products.```

boolean | undefined

```- draftWhether to show [draft products](https://help.shopify.com/en/manual/products/details?shpxid=70af7d87-E0F2-4973-8B09-B972AAF0ADFD#product-availability). Only applies to the Product resource type picker. Setting this to undefined will show a badge on draft products.```

boolean | undefined

```- hiddenWhether to show hidden resources, referring to products that are not published on any sales channels.```

boolean

```- queryGraphQL initial search query for filtering resources available in the picker. See [search syntax](/docs/api/usage/search-syntax) for more information. This is not displayed in the search bar when the picker is opened.```

string

```- variantsWhether to show product variants. Only applies to the Product resource type picker.```

boolean

``````

interface Filters {

/**

* Whether to show hidden resources, referring to products that are not published on any sales channels.

* @defaultValue true

*/

hidden?: boolean;

/**

* Whether to show product variants. Only applies to the Product resource type picker.

* @defaultValue true

*/

variants?: boolean;

/**

* Whether to show [draft products](https://help.shopify.com/en/manual/products/details?shpxid=70af7d87-E0F2-4973-8B09-B972AAF0ADFD#product-availability).

* Only applies to the Product resource type picker.

* Setting this to undefined will show a badge on draft products.

* @defaultValue true

*/

draft?: boolean | undefined;

/**

* Whether to show [archived products](https://help.shopify.com/en/manual/products/details?shpxid=70af7d87-E0F2-4973-8B09-B972AAF0ADFD#product-availability).

* Only applies to the Product resource type picker.

* Setting this to undefined will show a badge on draft products.

* @defaultValue true

*/

archived?: boolean | undefined;

/**

* GraphQL initial search query for filtering resources available in the picker.

* See [search syntax](/docs/api/usage/search-syntax) for more information.

* This is not displayed in the search bar when the picker is opened.

*/

query?: string;

}

```### BaseResource- idin GraphQL id format, ie 'gid://shopify/Product/1'```

string

```- variants```

Resource[]

``````

interface BaseResource extends Resource {

variants?: Resource[];

}

```### Resource- idin GraphQL id format, ie 'gid://shopify/Product/1'```

string

``````

interface Resource {

/** in GraphQL id format, ie 'gid://shopify/Product/1' */

id: string;

}

```## [Anchor to resource picker return payload](/docs/api/admin-extensions/2025-07/target-apis/utility-apis/resource-picker-api#resource picker return payload)Resource Picker Return PayloadThe `Resource Picker` returns a Promise with an array of the selected resources. The object type in the array varies based on the provided `type` option.

If the picker is cancelled, the Promise resolves to `undefined`

`[SelectPayload](#SelectPayload)<Type>`**`[SelectPayload](#SelectPayload)<Type>`**[Anchor to SelectPayload](/docs/api/admin-extensions/2025-07/target-apis/utility-apis/resource-picker-api#resourcepickerreturnpayload-selectpayload)### SelectPayloadSelectPayloadSelectPayload<Type>**SelectPayloadSelectPayload<Type>**ExamplesProduct pickerCopy9123const {resourcePicker} = useApi(TARGET);const selected = await resourcePicker({type: 'product'});## Preview### Examples- #### Product pickerDefault```

const {resourcePicker} = useApi(TARGET);

const selected = await resourcePicker({type: 'product'});

```- #### Alternate resourcesDescriptionAlternate resourcesCollection picker```

const selected = await resourcePicker({type: 'collection'});

```Product variant picker```

const selected = await resourcePicker({type: 'variant'});

```- #### Product picker with preselected resourcesDescriptionPreselected resourcesDefault```

const selected = await resourcePicker({

type: 'product',

selectionIds: [

{

id: 'gid://shopify/Product/12345',

variants: [

{

id: 'gid://shopify/ProductVariant/1',

},

],

},

{

id: 'gid://shopify/Product/67890',

},

],

});

```- #### Product picker with action verbDescriptionAction verbDefault```

const selected = await resourcePicker({

type: 'product',

action: 'select',

});

```- #### Product picker with multiple selectionDescriptionMultiple selectionUnlimited selectable items```

const selected = await resourcePicker({

type: 'product',

multiple: true,

});

```Maximum selectable items```

const selected = await resourcePicker({

type: 'product',

multiple: 5,

});

```- #### Product picker with filtersDescriptionFiltersDefault```

const selected = await resourcePicker({

type: 'product',

filter: {

hidden: true,

variants: false,

draft: false,

archived: false,

},

});

```- #### Product picker with a custom filter queryDescriptionFilter queryDefault```

const selected = await resourcePicker({

type: 'product',

filter: {

query: 'Sweater',

},

});

```- #### Product picker using returned selection payloadDescriptionSelectionDefault```

const selected = await resourcePicker({type: 'product'});

if (selected) {

console.log(selected);

} else {

console.log('Picker was cancelled by the user');

}

```- #### Product picker with initial query providedDescriptionInitial queryDefault```

const selected = await resourcePicker({

type: 'product',

query: 'Sweater',

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/target-apis/utility-apis/resource-picker-api#related)Related[APIsPicker APIAPIsPicker API](/docs/api/admin-extensions/2025-07/target-apis/utility-apis/picker)[APIs - Picker API](picker)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)