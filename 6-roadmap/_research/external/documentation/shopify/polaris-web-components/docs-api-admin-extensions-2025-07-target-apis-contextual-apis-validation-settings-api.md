---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/target-apis/contextual-apis/validation-settings-api",
    "fetched_at": "2026-02-10T13:28:11.856963",
    "status": 200,
    "size_bytes": 230353
  },
  "metadata": {
    "title": "Validation Settings API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "contextual-apis",
    "component": "validation-settings-api"
  }
}
---

# Validation Settings API

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# Validation Settings APIAsk assistantThis API is available to Validation Settings extensions. Refer to the [tutorial](/docs/apps/checkout/validation/create-complex-validation-rules) for more information. Note that the [`FunctionSettings`](/docs/api/admin-extensions/components/forms/functionsettings) component is required to build Validation Settings extensions.

## [Anchor to applyMetafieldChange](/docs/api/admin-extensions/2025-07/target-apis/contextual-apis/validation-settings-api#applyMetafieldChange)applyMetafieldChange([change](#applymetafieldchange-propertydetail-change)**[change](#applymetafieldchange-propertydetail-change)**)Applies a change to the validation settings.

### [Anchor to applyMetafieldChange-parameters](/docs/api/admin-extensions/2025-07/target-apis/contextual-apis/validation-settings-api#applyMetafieldChange-parameters)Parameters[Anchor to change](/docs/api/admin-extensions/2025-07/target-apis/contextual-apis/validation-settings-api#applymetafieldchange-propertydetail-change)change**change**MetafieldChangeMetafieldChange**MetafieldChangeMetafieldChange**required**required**### [Anchor to applyMetafieldChange-returns](/docs/api/admin-extensions/2025-07/target-apis/contextual-apis/validation-settings-api#applyMetafieldChange-returns)ReturnsPromise<MetafieldChangeResultMetafieldChangeResult>**Promise<MetafieldChangeResultMetafieldChangeResult>**### MetafieldChange```

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

```## [Anchor to data](/docs/api/admin-extensions/2025-07/target-apis/contextual-apis/validation-settings-api#data)dataThe object that exposes the validation with its settings.

[Anchor to shopifyFunction](/docs/api/admin-extensions/2025-07/target-apis/contextual-apis/validation-settings-api#data-propertydetail-shopifyfunction)shopifyFunction**shopifyFunction**ShopifyFunctionShopifyFunction**ShopifyFunctionShopifyFunction**required**required**[Anchor to validation](/docs/api/admin-extensions/2025-07/target-apis/contextual-apis/validation-settings-api#data-propertydetail-validation)validation**validation**ValidationValidation**ValidationValidation**### ShopifyFunction- idthe validation function's unique identifier```

string

``````

interface ShopifyFunction {

/**

* the validation function's unique identifier

*/

id: string;

}

```### Validation- idthe validation's gid when active in a shop```

string

```- metafieldsthe metafields owned by the validation```

Metafield[]

``````

interface Validation {

/**

* the validation's gid when active in a shop

*/

id: string;

/**

* the metafields owned by the validation

*/

metafields: Metafield[];

}

```### Metafield- description```

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

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)