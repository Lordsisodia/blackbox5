---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/target-apis/contextual-apis/discount-function-settings-api",
    "fetched_at": "2026-02-10T13:31:09.657736",
    "status": 200,
    "size_bytes": 247225
  },
  "metadata": {
    "title": "Discount Function Settings API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "contextual-apis",
    "component": "discount-function-settings-api"
  }
}
---

# Discount Function Settings API

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# Discount Function Settings APIAsk assistantThis API is available to Discount Function Settings extensions. Refer to the [tutorial](/docs/apps/build/discounts/build-ui-extension) for more information. Note that the [`FunctionSettings`](/docs/api/admin-extensions/components/forms/functionsettings) component is required to build Discount Function Settings extensions.

## [Anchor to applyMetafieldChange](/docs/api/admin-extensions/latest/target-apis/contextual-apis/discount-function-settings-api#applyMetafieldChange)applyMetafieldChange([change](#applymetafieldchange-propertydetail-change)**[change](#applymetafieldchange-propertydetail-change)**)Applies a change to the discount function settings.

### [Anchor to applyMetafieldChange-parameters](/docs/api/admin-extensions/latest/target-apis/contextual-apis/discount-function-settings-api#applyMetafieldChange-parameters)Parameters[Anchor to change](/docs/api/admin-extensions/latest/target-apis/contextual-apis/discount-function-settings-api#applymetafieldchange-propertydetail-change)change**change**MetafieldChangeMetafieldChange**MetafieldChangeMetafieldChange**required**required**### [Anchor to applyMetafieldChange-returns](/docs/api/admin-extensions/latest/target-apis/contextual-apis/discount-function-settings-api#applyMetafieldChange-returns)ReturnsPromise<MetafieldChangeResultMetafieldChangeResult>**Promise<MetafieldChangeResultMetafieldChangeResult>**### MetafieldChange```

MetafieldUpdateChange | MetafieldRemoveChange

```### MetafieldUpdateChange- key```

string

```- namespace```

string

```- type```

'updateMetafield'

```- value```

string | number

```- valueType```

SupportedDefinitionType

``````

interface MetafieldUpdateChange {

type: 'updateMetafield';

key: string;

namespace?: string;

value: string | number;

valueType?: SupportedDefinitionType;

}

```### SupportedDefinitionType```

'boolean' | 'collection_reference' | 'color' | 'date' | 'date_time' | 'dimension' | 'file_reference' | 'json' | 'metaobject_reference' | 'mixed_reference' | 'money' | 'multi_line_text_field' | 'number_decimal' | 'number_integer' | 'page_reference' | 'product_reference' | 'rating' | 'rich_text_field' | 'single_line_text_field' | 'product_taxonomy_value_reference' | 'url' | 'variant_reference' | 'volume' | 'weight' | 'list.collection_reference' | 'list.color' | 'list.date' | 'list.date_time' | 'list.dimension' | 'list.file_reference' | 'list.metaobject_reference' | 'list.mixed_reference' | 'list.number_decimal' | 'list.number_integer' | 'list.page_reference' | 'list.product_reference' | 'list.rating' | 'list.single_line_text_field' | 'list.url' | 'list.variant_reference' | 'list.volume' | 'list.weight'

```### MetafieldRemoveChange- key```

string

```- namespace```

string

```- type```

'removeMetafield'

``````

interface MetafieldRemoveChange {

type: 'removeMetafield';

key: string;

namespace: string;

}

```### MetafieldChangeResult```

MetafieldChangeSuccess | MetafieldChangeResultError

```### MetafieldChangeSuccess- type```

'success'

``````

interface MetafieldChangeSuccess {

type: 'success';

}

```### MetafieldChangeResultError- message```

string

```- type```

'error'

``````

interface MetafieldChangeResultError {

type: 'error';

message: string;

}

```## [Anchor to data](/docs/api/admin-extensions/latest/target-apis/contextual-apis/discount-function-settings-api#data)dataThe object exposed to the extension that contains the discount function settings.

[Anchor to id](/docs/api/admin-extensions/latest/target-apis/contextual-apis/discount-function-settings-api#data-propertydetail-id)id**id**string**string**required**required**The unique identifier for the discount.

[Anchor to metafields](/docs/api/admin-extensions/latest/target-apis/contextual-apis/discount-function-settings-api#data-propertydetail-metafields)metafields**metafields**MetafieldMetafield[]**MetafieldMetafield[]**required**required**The discount metafields.

### Metafield- description```

string

```- id```

string

```- key```

string

```- namespace```

string

```- type```

string

```- value```

string

``````

interface Metafield {

description?: string;

id: string;

namespace: string;

key: string;

value: string;

type: string;

}

```## [Anchor to discounts](/docs/api/admin-extensions/latest/target-apis/contextual-apis/discount-function-settings-api#discounts)discountsThe reactive API for managing discount function configuration.

[Anchor to discountClasses](/docs/api/admin-extensions/latest/target-apis/contextual-apis/discount-function-settings-api#discounts-propertydetail-discountclasses)discountClasses**discountClasses**ReadonlySignalLikeReadonlySignalLike<DiscountClassDiscountClass[]>**ReadonlySignalLikeReadonlySignalLike<DiscountClassDiscountClass[]>**required**required**A signal that contains the discount classes.

[Anchor to discountMethod](/docs/api/admin-extensions/latest/target-apis/contextual-apis/discount-function-settings-api#discounts-propertydetail-discountmethod)discountMethod**discountMethod**ReadonlySignalLikeReadonlySignalLike<DiscountMethodDiscountMethod>**ReadonlySignalLikeReadonlySignalLike<DiscountMethodDiscountMethod>**required**required**A signal that contains the discount method.

[Anchor to updateDiscountClasses](/docs/api/admin-extensions/latest/target-apis/contextual-apis/discount-function-settings-api#discounts-propertydetail-updatediscountclasses)updateDiscountClasses**updateDiscountClasses**UpdateSignalFunctionUpdateSignalFunction<DiscountClassDiscountClass[]>**UpdateSignalFunctionUpdateSignalFunction<DiscountClassDiscountClass[]>**required**required**A function that updates the discount classes.

### ReadonlySignalLikeRepresents a reactive signal interface that provides both immediate value access and subscription-based updates. Enables real-time synchronization with changing data through the observer pattern.- subscribeSubscribes to value changes and calls the provided function whenever the value updates. Returns an unsubscribe function to clean up the subscription. Use to automatically react to changes in the signal's value.```

(fn: (value: T) => void) => () => void

```- valueThe current value of the signal. This property provides immediate access to the current value without requiring subscription setup. Use for one-time value checks or initial setup.```

T

``````

export interface ReadonlySignalLike<T> {

/**

* The current value of the signal. This property provides immediate access to the current value without requiring subscription setup. Use for one-time value checks or initial setup.

*/

readonly value: T;

/**

* Subscribes to value changes and calls the provided function whenever the value updates. Returns an unsubscribe function to clean up the subscription. Use to automatically react to changes in the signal's value.

*/

subscribe(fn: (value: T) => void): () => void;

}

```### DiscountClass```

'product' | 'order' | 'shipping'

```### DiscountMethod```

'automatic' | 'code'

```### UpdateSignalFunctionA function that updates a signal and returns a result indicating success or failure. The function is typically used alongisde a ReadonlySignalLike object.- value```

T

```Result<T>```

Result<T>

``````

(value: T) => Result<T>

```### ResultA result type that indicates the success or failure of an operation.```

{success: true; value: T} | {success: false; errors: ValidationError[]}

```### ValidationErrorA validation error object that is returned when an operation fails.- codeA code identifier for the error.```

string

```- issuesField-level validation issues```

{ message: string; path: string[]; }[]

```- messageA message describing the error.```

string

```- type```

'error'

``````

interface ValidationError {

type: 'error';

/**

* A message describing the error.

*/

message: string;

/**

* A code identifier for the error.

*/

code: string;

/**

* Field-level validation issues

*/

issues?: {

message: string;

path: string[];

}[];

}

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)