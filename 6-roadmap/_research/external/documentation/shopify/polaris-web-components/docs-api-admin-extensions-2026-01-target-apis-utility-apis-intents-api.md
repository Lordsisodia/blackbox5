---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/target-apis/utility-apis/intents-api",
    "fetched_at": "2026-02-10T13:31:32.559036",
    "status": 200,
    "size_bytes": 302110
  },
  "metadata": {
    "title": "Intents API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "utility-apis",
    "component": "intents-api"
  }
}
---

# Intents API

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# Intents APIAsk assistantRequires an Admin [block](/docs/api/admin-extensions/2026-01extension-targets#block-locations) or [action](/docs/api/admin-extensions/2026-01extension-targets#action-locations) extension.**Requires an Admin [block](/docs/api/admin-extensions/2026-01extension-targets#block-locations) or [action](/docs/api/admin-extensions/2026-01extension-targets#action-locations) extension.:**The Intents API provides a way to invoke existing admin workflows for creating, editing, and managing Shopify resources.

## [Anchor to invoke](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#invoke)invokeThe `invoke` API is a function that accepts either a string query or an options object describing the intent to invoke and returns a Promise that resolves to an activity handle for the workflow.

## Intent Format

Intents are invoked using a string query format: `${action}:${type},${value}`

Where:

- `action` - The operation to perform (`create` or `edit`)

- `type` - The resource type (e.g., `shopify/Product`)

- `value` - The resource identifier (only for edit actions)

## Supported Resources

### Article

| Action | Type | Value | Data || `create` | `shopify/Article` | — | — || `edit` | `shopify/Article` | `gid://shopify/Article/{id}` | — |### Catalog

| Action | Type | Value | Data || `create` | `shopify/Catalog` | — | — || `edit` | `shopify/Catalog` | `gid://shopify/Catalog/{id}` | — |### Collection

| Action | Type | Value | Data || `create` | `shopify/Collection` | — | — || `edit` | `shopify/Collection` | `gid://shopify/Collection/{id}` | — |### Customer

| Action | Type | Value | Data || `create` | `shopify/Customer` | — | — || `edit` | `shopify/Customer` | `gid://shopify/Customer/{id}` | — |### Discount

| Action | Type | Value | Data || `create` | `shopify/Discount` | — | `{ type: 'amount-off-product' | 'amount-off-order' | 'buy-x-get-y' | 'free-shipping' }` || `edit` | `shopify/Discount` | `gid://shopify/Discount/{id}` | — |### Market

| Action | Type | Value | Data || `create` | `shopify/Market` | — | — || `edit` | `shopify/Market` | `gid://shopify/Market/{id}` | — |### Menu

| Action | Type | Value | Data || `create` | `shopify/Menu` | — | — || `edit` | `shopify/Menu` | `gid://shopify/Menu/{id}` | — |### Metafield Definition

| Action | Type | Value | Data || `create` | `shopify/MetafieldDefinition` | — | { ownerType: 'Product' } || `edit` | `shopify/MetafieldDefinition` | `gid://shopify/MetafieldDefinition/{id}` | { ownerType: 'Product' } |### Metaobject

| Action | Type | Value | Data || `create` | `shopify/Metaobject` | — | `{ type: 'shopify--color-pattern' }` || `edit` | `shopify/Metaobject` | `gid://shopify/Metaobject/{id}` | `{ type: 'shopify--color-pattern' }` |### Metaobject Definition

| Action | Type | Value | Data || `create` | `shopify/MetaobjectDefinition` | — | — || `edit` | `shopify/MetaobjectDefinition` | — | { type: 'my_metaobject_definition_type' } |### Page

| Action | Type | Value | Data || `create` | `shopify/Page` | — | — || `edit` | `shopify/Page` | `gid://shopify/Page/{id}` | — |### Product

| Action | Type | Value | Data || `create` | `shopify/Product` | — | — || `edit` | `shopify/Product` | `gid://shopify/Product/{id}` | — |### Product Variant

| Action | Type | Value | Data || `create` | `shopify/ProductVariant` | — | `{ productId: 'gid://shopify/Product/{id}' }` || `edit` | `shopify/ProductVariant` | `gid://shopify/ProductVariant/{id}` | `{ productId: 'gid://shopify/Product/{id}' }` |

**Note**: To determine whether to use the `shopify/ProductVariant` `edit` intent or the `shopify/Product` `edit` intent, query the [`product.hasOnlyDefaultVariant`](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.hasOnlyDefaultVariant) field. If the product has only the default variant (`hasOnlyDefaultVariant` is `true`), use the `shopify/Product` `edit` intent.

## [Anchor to intentaction](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentaction)IntentActionSupported actions that can be performed on resources.

- `create`: Opens a creation workflow for a new resource

- `edit`: Opens an editing workflow for an existing resource (requires `value` parameter)

`'create' | 'edit'`**`'create' | 'edit'`**## [Anchor to intenttype](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intenttype)IntentTypeSupported resource types that can be targeted by intents.

`'shopify/Article' | 'shopify/Catalog' | 'shopify/Collection' | 'shopify/Customer' | 'shopify/Discount' | 'shopify/Market' | 'shopify/Menu' | 'shopify/MetafieldDefinition' | 'shopify/Metaobject' | 'shopify/MetaobjectDefinition' | 'shopify/Page' | 'shopify/Product' | 'shopify/ProductVariant'`**`'shopify/Article' | 'shopify/Catalog' | 'shopify/Collection' | 'shopify/Customer' | 'shopify/Discount' | 'shopify/Market' | 'shopify/Menu' | 'shopify/MetafieldDefinition' | 'shopify/Metaobject' | 'shopify/MetaobjectDefinition' | 'shopify/Page' | 'shopify/Product' | 'shopify/ProductVariant'`**## [Anchor to intentqueryoptions](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentqueryoptions)IntentQueryOptionsOptions for invoking intents when using the query string format.

[Anchor to data](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentqueryoptions-propertydetail-data)data**data**{ [key: string]: unknown; }**{ [key: string]: unknown; }**Additional data required for certain intent types. For example:

- Discount creation requires { type: 'amount-off-product' | 'amount-off-order' | 'buy-x-get-y' | 'free-shipping' }

- ProductVariant creation requires { productId: 'gid://shopify/Product/123' }

- Metaobject creation requires { type: 'shopify--color-pattern' }

[Anchor to value](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentqueryoptions-propertydetail-value)value**value**string**string**The resource identifier for edit actions (e.g., 'gid://shopify/Product/123').

## [Anchor to intentresponse](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentresponse)IntentResponseResponse object returned when the intent workflow completes.

`[SuccessIntentResponse](#SuccessIntentResponse) | [ErrorIntentResponse](#ErrorIntentResponse) | [ClosedIntentResponse](#ClosedIntentResponse)`**`[SuccessIntentResponse](#SuccessIntentResponse) | [ErrorIntentResponse](#ErrorIntentResponse) | [ClosedIntentResponse](#ClosedIntentResponse)`**[Anchor to ClosedIntentResponse](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentresponse-closedintentresponse)### ClosedIntentResponse[Anchor to code](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentresponse-propertydetail-code)code**code**'closed'**'closed'**[Anchor to ErrorIntentResponse](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentresponse-errorintentresponse)### ErrorIntentResponse[Anchor to code](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentresponse-propertydetail-code)code**code**'error'**'error'**[Anchor to issues](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentresponse-propertydetail-issues)issues**issues**{ path?: string[]; message?: string; code?: string; }[]**{ path?: string[]; message?: string; code?: string; }[]**[Anchor to message](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentresponse-propertydetail-message)message**message**string**string**[Anchor to SuccessIntentResponse](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentresponse-successintentresponse)### SuccessIntentResponse[Anchor to code](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentresponse-propertydetail-code)code**code**'ok'**'ok'**[Anchor to data](/docs/api/admin-extensions/latest/target-apis/utility-apis/intents-api#intentresponse-propertydetail-data)data**data**{ [key: string]: unknown; }**{ [key: string]: unknown; }**### SuccessIntentResponseSuccessful intent completion.- code```

'ok'

```- data```

{ [key: string]: unknown; }

``````

export interface SuccessIntentResponse {

code?: 'ok';

data?: {[key: string]: unknown};

}

```### ErrorIntentResponseFailed intent completion.- code```

'error'

```- issues```

{ path?: string[]; message?: string; code?: string; }[]

```- message```

string

``````

export interface ErrorIntentResponse {

code?: 'error';

message?: string;

issues?: {

/**

* The path to the field with the issue.

*/

path?: string[];

/**

* The error message for the issue.

*/

message?: string;

/**

* A code identifier for the issue.

*/

code?: string;

}[];

}

```### ClosedIntentResponseUser dismissed or closed the workflow without completing it.- code```

'closed'

``````

export interface ClosedIntentResponse {

code?: 'closed';

}

```ExamplesCreating a collection## js Copy9123456789const {intents} = useApi(TARGET);const activity = await intents.invoke('create:shopify/Collection');const response = await activity.complete;if (response.code === 'ok') {  console.log('Collection created:', response.data);}## Preview### Examples- #### Creating a collectionjs```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/Collection');

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Collection created:', response.data);

}

```- #### Create articleDescriptionCreate a new article. Opens the article creation workflow.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/Article');

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Article created:', response.data);

}

```- #### Edit articleDescriptionEdit an existing article. Requires an article GID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('edit:shopify/Article', {

value: 'gid://shopify/Article/123456789',

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Article updated:', response.data);

}

```- #### Create catalogDescriptionCreate a new catalog. Opens the catalog creation workflow.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/Catalog');

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Catalog created:', response.data);

}

```- #### Edit catalogDescriptionEdit an existing catalog. Requires a catalog GID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('edit:shopify/Catalog', {

value: 'gid://shopify/Catalog/123456789',

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Catalog updated:', response.data);

}

```- #### Create collectionDescriptionCreate a new collection. Opens the collection creation workflow.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/Collection');

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Collection created:', response.data);

}

```- #### Edit collectionDescriptionEdit an existing collection. Requires a collection GID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('edit:shopify/Collection', {

value: 'gid://shopify/Collection/987654321',

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Collection updated:', response.data);

}

```- #### Create customerDescriptionCreate a new customer. Opens the customer creation workflow.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/Customer');

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Customer created:', response.data);

}

```- #### Edit customerDescriptionEdit an existing customer. Requires a customer GID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('edit:shopify/Customer', {

value: 'gid://shopify/Customer/456789123',

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Customer updated:', response.data);

}

```- #### Create discountDescriptionCreate a new discount. Opens the discount creation workflow. Requires a discount type.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/Discount', {

data: {type: 'amount-off-product'},

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Discount created:', response.data);

}

```- #### Edit discountDescriptionEdit an existing discount. Requires a discount GID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('edit:shopify/Discount', {

value: 'gid://shopify/Discount/123456789',

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Discount updated:', response.data);

}

```- #### Create marketDescriptionCreate a new market. Opens the market creation workflow.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/Market');

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Market created:', response.data);

}

```- #### Edit marketDescriptionEdit an existing market. Requires a market GID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('edit:shopify/Market', {

value: 'gid://shopify/Market/123456789',

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Market updated:', response.data);

}

```- #### Create menuDescriptionCreate a new menu. Opens the menu creation workflow.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/Menu');

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Menu created:', response.data);

}

```- #### Edit menuDescriptionEdit an existing menu. Requires a menu GID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('edit:shopify/Menu', {

value: 'gid://shopify/Menu/123456789',

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Menu updated:', response.data);

}

```- #### Create metafield definitionDescriptionCreate a new metafield definition. Opens the metafield definition creation workflow.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/MetafieldDefinition', {

data: {ownerType: 'product'},

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Metafield definition created:', response.data);

}

```- #### Edit metafield definitionDescriptionEdit an existing metafield definition. Requires a metafield definition GID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('edit:shopify/MetafieldDefinition', {

value: 'gid://shopify/MetafieldDefinition/123456789',

data: {ownerType: 'product'},

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Metafield definition updated:', response.data);

}

```- #### Create metaobjectDescriptionCreate a new metaobject. Opens the metaobject creation workflow. Requires a type.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/Metaobject', {

data: {type: 'shopify--color-pattern'},

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Metaobject created:', response.data);

}

```- #### Edit metaobjectDescriptionEdit an existing metaobject. Requires a metaobject GID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('edit:shopify/Metaobject', {

value: 'gid://shopify/Metaobject/123456789',

data: {type: 'shopify--color-pattern'},

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Metaobject updated:', response.data);

}

```- #### Create metaobject definitionDescriptionCreate a new metaobject definition. Opens the metaobject definition creation workflow.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/MetaobjectDefinition');

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Metaobject definition created:', response.data);

}

```- #### Edit metaobject definitionDescriptionEdit an existing metaobject definition. Requires a metaobject definition GID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('edit:shopify/MetaobjectDefinition', {

data: {type: 'my_metaobject_definition_type'},

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Metaobject definition updated:', response.data);

}

```- #### Create pageDescriptionCreate a new page. Opens the page creation workflow.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/Page');

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Page created:', response.data);

}

```- #### Edit pageDescriptionEdit an existing page. Requires a page GID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('edit:shopify/Page', {

value: 'gid://shopify/Page/123456789',

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Page updated:', response.data);

}

```- #### Create productDescriptionCreate a new product. Opens the product creation workflow.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/Product');

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Product created:', response.data);

}

```- #### Edit productDescriptionEdit an existing product. Requires a product GID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('edit:shopify/Product', {

value: 'gid://shopify/Product/123456789',

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Product updated:', response.data);

}

```- #### Create variantDescriptionCreate a new product variant. Opens the variant creation workflow. Requires a product ID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('create:shopify/ProductVariant', {

data: {productId: 'gid://shopify/Product/123456789'},

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Product variant created:', response.data);

}

```- #### Edit variantDescriptionEdit an existing product variant. Requires a variant GID.js```

const {intents} = useApi(TARGET);

const activity = await intents.invoke('edit:shopify/ProductVariant', {

value: 'gid://shopify/ProductVariant/123456789',

data: {productId: 'gid://shopify/Product/123456789'},

});

const response = await activity.complete;

if (response.code === 'ok') {

console.log('Product variant updated:', response.data);

}

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)