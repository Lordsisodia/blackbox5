---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/target-apis/core-apis/action-extension-api",
    "fetched_at": "2026-02-10T13:28:13.432577",
    "status": 200,
    "size_bytes": 463444
  },
  "metadata": {
    "title": "Action Extension API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "core-apis",
    "component": "action-extension-api"
  }
}
---

# Action Extension API

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# Action Extension APIAsk assistantThis API is available to all action extension types. Refer to the [tutorial](/docs/apps/admin/admin-actions-and-blocks/build-an-admin-action) for more information. Note that the [`AdminAction`](/docs/api/admin-extensions/components/other/adminaction) component is required to build Admin action extensions.

## [Anchor to actionextensionapi](/docs/api/admin-extensions/2025-07/target-apis/core-apis/action-extension-api#actionextensionapi)ActionExtensionApi[Anchor to auth](/docs/api/admin-extensions/2025-07/target-apis/core-apis/action-extension-api#actionextensionapi-propertydetail-auth)auth**auth**AuthAuth**AuthAuth**required**required**Provides methods for authenticating calls to an app backend.

[Anchor to close](/docs/api/admin-extensions/2025-07/target-apis/core-apis/action-extension-api#actionextensionapi-propertydetail-close)close**close**() => void**() => void**required**required**Closes the extension. Calling this method is equivalent to the merchant clicking the "x" in the corner of the overlay.

[Anchor to data](/docs/api/admin-extensions/2025-07/target-apis/core-apis/action-extension-api#actionextensionapi-propertydetail-data)data**data**DataData**DataData**required**required**Information about the currently viewed or selected items.

[Anchor to extension](/docs/api/admin-extensions/2025-07/target-apis/core-apis/action-extension-api#actionextensionapi-propertydetail-extension)extension**extension**{ target: ExtensionTargetExtensionTarget; }**{ target: ExtensionTargetExtensionTarget; }**required**required**The identifier of the running extension target.

[Anchor to i18n](/docs/api/admin-extensions/2025-07/target-apis/core-apis/action-extension-api#actionextensionapi-propertydetail-i18n)i18n**i18n**I18nI18n**I18nI18n**required**required**Utilities for translating content according to the current localization of the admin. More info - /docs/apps/checkout/best-practices/localizing-ui-extensions

[Anchor to intents](/docs/api/admin-extensions/2025-07/target-apis/core-apis/action-extension-api#actionextensionapi-propertydetail-intents)intents**intents**IntentsIntents**IntentsIntents**required**required**Provides information to the receiver the of an intent.

[Anchor to picker](/docs/api/admin-extensions/2025-07/target-apis/core-apis/action-extension-api#actionextensionapi-propertydetail-picker)picker**picker**PickerApiPickerApi**PickerApiPickerApi**required**required**Renders a custom [Picker](/docs/api/admin-extensions/2025-07/target-apis/core-apis/action-extension-api/picker) dialog allowing users to select values from a list.

[Anchor to query](/docs/api/admin-extensions/2025-07/target-apis/core-apis/action-extension-api#actionextensionapi-propertydetail-query)query**query**<DataData = unknown, Variables = { [key: string]: unknown; }>(query: string, options?: { variables?: Variables; version?: Omit<ApiVersionApiVersion, "2023-04">; }) => Promise<{ data?: DataData; errors?: GraphQLErrorGraphQLError[]; }>**<DataData = unknown, Variables = { [key: string]: unknown; }>(query: string, options?: { variables?: Variables; version?: Omit<ApiVersionApiVersion, "2023-04">; }) => Promise<{ data?: DataData; errors?: GraphQLErrorGraphQLError[]; }>**required**required**Used to query the Admin GraphQL API

[Anchor to resourcePicker](/docs/api/admin-extensions/2025-07/target-apis/core-apis/action-extension-api#actionextensionapi-propertydetail-resourcepicker)resourcePicker**resourcePicker**ResourcePickerApiResourcePickerApi**ResourcePickerApiResourcePickerApi**required**required**Renders the [Resource Picker](/docs/api/admin-extensions/2025-07/target-apis/core-apis/action-extension-api/resource-picker), allowing users to select a resource for the extension to use as part of its flow.

### Auth- idTokenRetrieves a Shopify OpenID Connect ID token for the current user.```

() => Promise<string>

``````

interface Auth {

/**

* Retrieves a Shopify OpenID Connect ID token for the current user.

*/

idToken: () => Promise<string | null>;

}

```### Data- selectedInformation about the currently viewed or selected items.```

{ id: string; }[]

``````

export interface Data {

/**

* Information about the currently viewed or selected items.

*/

selected: {id: string}[];

}

```### ExtensionTarget```

keyof ExtensionTargets

```### ExtensionTargets- admin.abandoned-checkout-details.action.renderRenders an admin action extension in the abandoned checkout page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.abandoned-checkout-details.action.render'>,

AllComponents

>

```- admin.abandoned-checkout-details.action.should-renderControls the render state of an admin action extension in the abandoned checkout page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.abandoned-checkout-details.action.should-render'>,

ShouldRenderOutput

>

```- admin.abandoned-checkout-details.block.renderRenders an admin block in the abandoned checkout details page.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

BlockExtensionApi<'admin.abandoned-checkout-details.block.render'>,

AllComponents

>

```- admin.catalog-details.action.renderRenders an admin action extension in the catalog details page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.catalog-details.action.render'>,

AllComponents

>

```- admin.catalog-details.action.should-renderControls the render state of an admin action extension in the catalog details page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.catalog-details.action.should-render'>,

ShouldRenderOutput

>

```- admin.catalog-details.block.renderRenders an admin block in the catalog details page.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

BlockExtensionApi<'admin.catalog-details.block.render'>,

AllComponents

>

```- admin.collection-details.action.renderRenders an admin action extension in the collection details page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.collection-details.action.render'>,

AllComponents

>

```- admin.collection-details.action.should-renderControls the render state of an admin action extension in the collection details page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.collection-details.action.should-render'>,

ShouldRenderOutput

>

```- admin.collection-details.block.renderRenders an admin block in the collection details page.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

BlockExtensionApi<'admin.collection-details.block.render'>,

AllComponents

>

```- admin.collection-index.action.renderRenders an admin action extension in the collection index page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.collection-index.action.render'>,

AllComponents

>

```- admin.collection-index.action.should-renderControls the render state of an admin action extension in the collection index page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.collection-index.action.should-render'>,

ShouldRenderOutput

>

```- admin.company-details.action.renderRenders an admin action extension in the company details page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.company-details.action.render'>,

AllComponents

>

```- admin.company-details.action.should-renderControls the render state of an admin action extension in the company details page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.company-details.action.should-render'>,

ShouldRenderOutput

>

```- admin.company-details.block.renderRenders an admin block in the company details page.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

BlockExtensionApi<'admin.company-details.block.render'>,

AllComponents

>

```- admin.company-location-details.block.renderRenders an admin block in the company location details page.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

BlockExtensionApi<'admin.company-location-details.block.render'>,

AllComponents

>

```- admin.customer-details.action.renderRenders an admin action extension in the customer details page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.customer-details.action.render'>,

AllComponents

>

```- admin.customer-details.action.should-renderControls the render state of an admin action extension in the customer details page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.customer-details.action.should-render'>,

ShouldRenderOutput

>

```- admin.customer-details.block.renderRenders an admin block in the customer details page.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

BlockExtensionApi<'admin.customer-details.block.render'>,

AllComponents

>

```- admin.customer-index.action.renderRenders an admin action extension in the customer index page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.customer-index.action.render'>,

AllComponents

>

```- admin.customer-index.action.should-renderControls the render state of an admin action extension in the customer index page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.customer-index.action.should-render'>,

ShouldRenderOutput

>

```- admin.customer-index.selection-action.renderRenders an admin action extension in the customer index page when multiple resources are selected. Open this extension from the "More Actions" menu of the resource list. The resource ids are available to this extension at runtime.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.customer-index.selection-action.render'>,

AllComponents

>

```- admin.customer-index.selection-action.should-renderControls the render state of an admin action extension in the customer index page when multiple resources are selected. Open this extension from the "More Actions" menu of the resource list. The resource ids are available to this extension at runtime.```

RunnableExtension<

ShouldRenderApi<'admin.customer-index.selection-action.should-render'>,

ShouldRenderOutput

>

```- admin.customer-segment-details.action.renderRenders an admin action extension in the customer segment details page. Open this extension from the "Use segment" button.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.customer-segment-details.action.render'>,

AllComponents

>

```- admin.customer-segment-details.action.should-renderControls the render state of an admin action extension in the customer segment details page. Open this extension from the "Use segment" button.```

RunnableExtension<

ShouldRenderApi<'admin.customer-segment-details.action.should-render'>,

ShouldRenderOutput

>

```- admin.customers.segmentation-templates.renderRenders a [`CustomerSegmentTemplate`](/docs/api/admin-extensions/components/customersegmenttemplate) in the [customer segment editor](https://help.shopify.com/en/manual/customers/customer-segmentation/customer-segments).```

RenderExtension<

CustomerSegmentTemplateApi<'admin.customers.segmentation-templates.render'>,

CustomerSegmentTemplateComponent

>

```- admin.discount-details.action.renderRenders an admin action extension in the discount details page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.discount-details.action.render'>,

AllComponents

>

```- admin.discount-details.action.should-renderControls the render state of an admin action extension in the discount details page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.discount-details.action.should-render'>,

ShouldRenderOutput

>

```- admin.discount-details.function-settings.renderRenders an admin block in the discount details page.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

DiscountFunctionSettingsApi<'admin.discount-details.function-settings.render'>,

AllComponents

>

```- admin.discount-index.action.renderRenders an admin action extension in the discount index page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.discount-index.action.render'>,

AllComponents

>

```- admin.discount-index.action.should-renderControls the render state of an admin action extension in the discount index page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.discount-index.action.should-render'>,

ShouldRenderOutput

>

```- admin.draft-order-details.action.renderRenders an admin action extension in the draft order details page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.draft-order-details.action.render'>,

AllComponents

>

```- admin.draft-order-details.action.should-renderControls the render state of an admin action extension in the draft order details page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.draft-order-details.action.should-render'>,

ShouldRenderOutput

>

```- admin.draft-order-details.block.renderRenders an admin block in the draft order details page.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

BlockExtensionApi<'admin.draft-order-details.block.render'>,

AllComponents

>

```- admin.draft-order-index.action.renderRenders an admin action extension in the draft orders page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.draft-order-index.action.render'>,

AllComponents

>

```- admin.draft-order-index.action.should-renderControls the render state of an admin action extension in the draft orders page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.draft-order-index.action.should-render'>,

ShouldRenderOutput

>

```- admin.draft-order-index.selection-action.renderRenders an admin action extension in the draft order page when multiple resources are selected. Open this extension from the "3-dot" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.draft-order-index.selection-action.render'>,

AllComponents

>

```- admin.draft-order-index.selection-action.should-renderControls the render state of an admin action extension in the draft order page when multiple resources are selected. Open this extension from the "3-dot" menu.```

RunnableExtension<

ShouldRenderApi<'admin.draft-order-index.selection-action.should-render'>,

ShouldRenderOutput

>

```- admin.gift-card-details.action.renderRenders an admin action extension in the gift card details page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.gift-card-details.action.render'>,

AllComponents

>

```- admin.gift-card-details.action.should-renderControls the render state of an admin action extension in the gift card details page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.gift-card-details.action.should-render'>,

ShouldRenderOutput

>

```- admin.gift-card-details.block.renderRenders an admin block in the gift card details page.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

BlockExtensionApi<'admin.gift-card-details.block.render'>,

AllComponents

>

```- admin.order-details.action.renderRenders an admin action extension in the order details page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.order-details.action.render'>,

AllComponents

>

```- admin.order-details.action.should-renderControls the render state of an admin action extension in the order details page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.order-details.action.should-render'>,

ShouldRenderOutput

>

```- admin.order-details.block.renderRenders an admin block in the order details page.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

BlockExtensionApi<'admin.order-details.block.render'>,

AllComponents

>

```- admin.order-details.print-action.renderRenders an admin print action extension in the order index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

PrintActionExtensionApi<'admin.order-details.print-action.render'>,

AllComponents

>

```- admin.order-details.print-action.should-renderControls the render state of an admin print action extension in the order index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.```

RunnableExtension<

ShouldRenderApi<'admin.order-details.print-action.should-render'>,

ShouldRenderOutput

>

```- admin.order-fulfilled-card.action.renderRenders an admin action extension in the order fulfilled card. Open this extension from the "3-dot" menu inside the order fulfilled card. Note: This extension will only be visible on orders which were fulfilled by your app.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.order-fulfilled-card.action.render'>,

AllComponents

>

```- admin.order-fulfilled-card.action.should-renderControls the render state of an admin action extension in the order fulfilled card. Open this extension from the "3-dot" menu inside the order fulfilled card. Note: This extension will only be visible on orders which were fulfilled by your app.```

RunnableExtension<

ShouldRenderApi<'admin.order-fulfilled-card.action.should-render'>,

ShouldRenderOutput

>

```- admin.order-index.action.renderRenders an admin action extension in the order index page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.order-index.action.render'>,

AllComponents

>

```- admin.order-index.action.should-renderControls the render state of an admin action extension in the order index page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.order-index.action.should-render'>,

ShouldRenderOutput

>

```- admin.order-index.selection-action.renderRenders an admin action extension in the order index page when multiple resources are selected. Open this extension from the "More Actions"  menu of the resource list. The resource ids are available to this extension at runtime.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.order-index.selection-action.render'>,

AllComponents

>

```- admin.order-index.selection-action.should-renderControls the render state of an admin action extension in the order index page when multiple resources are selected. Open this extension from the "More Actions"  menu of the resource list. The resource ids are available to this extension at runtime.```

RunnableExtension<

ShouldRenderApi<'admin.order-index.selection-action.should-render'>,

ShouldRenderOutput

>

```- admin.order-index.selection-print-action.renderRenders an admin print action extension in the order index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

PrintActionExtensionApi<'admin.order-index.selection-print-action.render'>,

AllComponents

>

```- admin.order-index.selection-print-action.should-renderControls the render state of an admin print action extension in the order index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.```

RunnableExtension<

ShouldRenderApi<'admin.order-index.selection-print-action.should-render'>,

ShouldRenderOutput

>

```- admin.product-details.action.renderRenders an admin action extension in the product details page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.product-details.action.render'>,

AllComponents

>

```- admin.product-details.action.should-renderControls the render state of an admin action extension in the product details page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.product-details.action.should-render'>,

ShouldRenderOutput

>

```- admin.product-details.block.renderRenders an admin block in the product details page.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

BlockExtensionApi<'admin.product-details.block.render'>,

AllComponents

>

```- admin.product-details.configuration.renderRenders Product Configuration on product details and product variant details

See the [tutorial](/docs/apps/selling-strategies/bundles/product-config) for more information```

RenderExtension<

ProductDetailsConfigurationApi<'admin.product-details.configuration.render'>,

AllComponents

>

```- admin.product-details.print-action.renderRenders an admin print action extension in the product index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

PrintActionExtensionApi<'admin.product-details.print-action.render'>,

AllComponents

>

```- admin.product-details.print-action.should-renderControls the render state of an admin print action extension in the product index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.```

RunnableExtension<

ShouldRenderApi<'admin.product-details.print-action.should-render'>,

ShouldRenderOutput

>

```- admin.product-details.reorder.renderRenders an admin block in the product details page.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

BlockExtensionApi<'admin.product-details.reorder.render'>,

AllComponents

>

```- admin.product-index.action.renderRenders an admin action extension in the product index page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.product-index.action.render'>,

AllComponents

>

```- admin.product-index.action.should-renderControls the render state of an admin action extension in the product index page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.product-index.action.should-render'>,

ShouldRenderOutput

>

```- admin.product-index.selection-action.renderRenders an admin action extension in the product index page when multiple resources are selected. Open this extension from the "More Actions"  menu of the resource list. The resource ids are available to this extension at runtime.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.product-index.selection-action.render'>,

AllComponents

>

```- admin.product-index.selection-action.should-renderControls the render state of an admin action extension in the product index page when multiple resources are selected. Open this extension from the "More Actions"  menu of the resource list. The resource ids are available to this extension at runtime.```

RunnableExtension<

ShouldRenderApi<'admin.product-index.selection-action.should-render'>,

ShouldRenderOutput

>

```- admin.product-index.selection-print-action.renderRenders an admin print action extension in the product index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

PrintActionExtensionApi<'admin.product-index.selection-print-action.render'>,

AllComponents

>

```- admin.product-index.selection-print-action.should-renderControls the render state of an admin print action extension in the product index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.```

RunnableExtension<

ShouldRenderApi<'admin.product-index.selection-print-action.should-render'>,

ShouldRenderOutput

>

```- admin.product-purchase-option.action.renderRenders an admin action extension in the product details page when a selling plan group is present. Open this extension from the "Purchase Options card".

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

PurchaseOptionsCardConfigurationApi<'admin.product-purchase-option.action.render'>,

AllComponents

>

```- admin.product-variant-details.action.renderRenders an admin action extension in the product variant details page. Open this extension from the "More Actions" menu.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ActionExtensionApi<'admin.product-variant-details.action.render'>,

AllComponents

>

```- admin.product-variant-details.action.should-renderControls the render state of an admin action extension in the product variant details page. Open this extension from the "More Actions" menu.```

RunnableExtension<

ShouldRenderApi<'admin.product-variant-details.action.should-render'>,

ShouldRenderOutput

>

```- admin.product-variant-details.block.renderRenders an admin block in the product variant details page.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

BlockExtensionApi<'admin.product-variant-details.block.render'>,

AllComponents

>

```- admin.product-variant-details.configuration.renderRenders Product Configuration on product details and product variant details

See the [tutorial](/docs/apps/selling-strategies/bundles/product-config) for more information```

RenderExtension<

ProductVariantDetailsConfigurationApi<'admin.product-variant-details.configuration.render'>,

AllComponents

>

```- admin.product-variant-purchase-option.action.renderRenders an admin action extension in the product variant details page when a selling plan group is present. Open this extension from the "Purchase Options card".

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

PurchaseOptionsCardConfigurationApi<'admin.product-variant-purchase-option.action.render'>,

AllComponents

>

```- admin.settings.internal-order-routing-rule.renderRenders Order Routing Rule Configuration on order routing settings.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

OrderRoutingRuleApi<'admin.settings.internal-order-routing-rule.render'>,

AllComponents | OrderRoutingComponents

>

```- admin.settings.order-routing-rule.render```

RenderExtension<

OrderRoutingRuleApi<'admin.settings.order-routing-rule.render'>,

AllComponents

>

```- admin.settings.validation.renderRenders Validation Settings within a given validation's add and edit views.

See the [list of available components](/docs/api/admin-extensions/components).```

RenderExtension<

ValidationSettingsApi<'admin.settings.validation.render'>,

AllComponents

>

```- Playground```

RenderExtension<StandardApi<'Playground'>, AllComponents>

``````

export interface ExtensionTargets {

/**

* @private

*/

Playground: RenderExtension<StandardApi<'Playground'>, AllComponents>;

/**

* Renders a [`CustomerSegmentTemplate`](/docs/api/admin-extensions/components/customersegmenttemplate) in the [customer segment editor](https://help.shopify.com/en/manual/customers/customer-segmentation/customer-segments).

*/

'admin.customers.segmentation-templates.render': RenderExtension<

CustomerSegmentTemplateApi<'admin.customers.segmentation-templates.render'>,

CustomerSegmentTemplateComponent

>;

// Blocks

/**

* Renders an admin block in the product details page.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.product-details.block.render': RenderExtension<

BlockExtensionApi<'admin.product-details.block.render'>,

AllComponents

>;

/**

* Renders an admin block in the order details page.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.order-details.block.render': RenderExtension<

BlockExtensionApi<'admin.order-details.block.render'>,

AllComponents

>;

/**

* Renders an admin block in the discount details page.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.discount-details.function-settings.render': RenderExtension<

DiscountFunctionSettingsApi<'admin.discount-details.function-settings.render'>,

AllComponents

>;

/**

* Renders an admin block in the customer details page.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.customer-details.block.render': RenderExtension<

BlockExtensionApi<'admin.customer-details.block.render'>,

AllComponents

>;

/**

* Renders an admin block in the collection details page.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.collection-details.block.render': RenderExtension<

BlockExtensionApi<'admin.collection-details.block.render'>,

AllComponents

>;

/**

* Renders an admin block in the draft order details page.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.draft-order-details.block.render': RenderExtension<

BlockExtensionApi<'admin.draft-order-details.block.render'>,

AllComponents

>;

/**

* Renders an admin block in the abandoned checkout details page.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.abandoned-checkout-details.block.render': RenderExtension<

BlockExtensionApi<'admin.abandoned-checkout-details.block.render'>,

AllComponents

>;

/**

* Renders an admin block in the catalog details page.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.catalog-details.block.render': RenderExtension<

BlockExtensionApi<'admin.catalog-details.block.render'>,

AllComponents

>;

/**

* Renders an admin block in the company details page.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.company-details.block.render': RenderExtension<

BlockExtensionApi<'admin.company-details.block.render'>,

AllComponents

>;

/**

* Renders an admin block in the company location details page.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.company-location-details.block.render': RenderExtension<

BlockExtensionApi<'admin.company-location-details.block.render'>,

AllComponents

>;

/**

* Renders an admin block in the gift card details page.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.gift-card-details.block.render': RenderExtension<

BlockExtensionApi<'admin.gift-card-details.block.render'>,

AllComponents

>;

/**

* Renders an admin block in the product variant details page.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.product-variant-details.block.render': RenderExtension<

BlockExtensionApi<'admin.product-variant-details.block.render'>,

AllComponents

>;

/**

* Renders an admin block in the product details page.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.product-details.reorder.render': RenderExtension<

BlockExtensionApi<'admin.product-details.reorder.render'>,

AllComponents

>;

// Actions

/**

* Renders an admin action extension in the product details page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.product-details.action.render': RenderExtension<

ActionExtensionApi<'admin.product-details.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the catalog details page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.catalog-details.action.render': RenderExtension<

ActionExtensionApi<'admin.catalog-details.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the company details page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.company-details.action.render': RenderExtension<

ActionExtensionApi<'admin.company-details.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the gift card details page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.gift-card-details.action.render': RenderExtension<

ActionExtensionApi<'admin.gift-card-details.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the order details page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.order-details.action.render': RenderExtension<

ActionExtensionApi<'admin.order-details.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the customer details page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.customer-details.action.render': RenderExtension<

ActionExtensionApi<'admin.customer-details.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the customer segment details page. Open this extension from the "Use segment" button.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.customer-segment-details.action.render': RenderExtension<

ActionExtensionApi<'admin.customer-segment-details.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the product index page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.product-index.action.render': RenderExtension<

ActionExtensionApi<'admin.product-index.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the order index page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.order-index.action.render': RenderExtension<

ActionExtensionApi<'admin.order-index.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the customer index page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.customer-index.action.render': RenderExtension<

ActionExtensionApi<'admin.customer-index.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the discount index page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.discount-index.action.render': RenderExtension<

ActionExtensionApi<'admin.discount-index.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the collection details page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.collection-details.action.render': RenderExtension<

ActionExtensionApi<'admin.collection-details.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the collection index page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.collection-index.action.render': RenderExtension<

ActionExtensionApi<'admin.collection-index.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the abandoned checkout page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.abandoned-checkout-details.action.render': RenderExtension<

ActionExtensionApi<'admin.abandoned-checkout-details.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the product variant details page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.product-variant-details.action.render': RenderExtension<

ActionExtensionApi<'admin.product-variant-details.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the draft order details page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.draft-order-details.action.render': RenderExtension<

ActionExtensionApi<'admin.draft-order-details.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the draft orders page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.draft-order-index.action.render': RenderExtension<

ActionExtensionApi<'admin.draft-order-index.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the discount details page. Open this extension from the "More Actions" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.discount-details.action.render': RenderExtension<

ActionExtensionApi<'admin.discount-details.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the order fulfilled card. Open this extension from the "3-dot" menu inside the order fulfilled card.

* Note: This extension will only be visible on orders which were fulfilled by your app.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.order-fulfilled-card.action.render': RenderExtension<

ActionExtensionApi<'admin.order-fulfilled-card.action.render'>,

AllComponents

>;

// Bulk Actions

/**

* Renders an admin action extension in the product index page when multiple resources are selected. Open this extension from the "More Actions"  menu of the resource list. The resource ids are available to this extension at runtime.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.product-index.selection-action.render': RenderExtension<

ActionExtensionApi<'admin.product-index.selection-action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the order index page when multiple resources are selected. Open this extension from the "More Actions"  menu of the resource list. The resource ids are available to this extension at runtime.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.order-index.selection-action.render': RenderExtension<

ActionExtensionApi<'admin.order-index.selection-action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the customer index page when multiple resources are selected. Open this extension from the "More Actions" menu of the resource list. The resource ids are available to this extension at runtime.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.customer-index.selection-action.render': RenderExtension<

ActionExtensionApi<'admin.customer-index.selection-action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the draft order page when multiple resources are selected. Open this extension from the "3-dot" menu.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.draft-order-index.selection-action.render': RenderExtension<

ActionExtensionApi<'admin.draft-order-index.selection-action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the product details page when a selling plan group is present. Open this extension from the "Purchase Options card".

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.product-purchase-option.action.render': RenderExtension<

PurchaseOptionsCardConfigurationApi<'admin.product-purchase-option.action.render'>,

AllComponents

>;

/**

* Renders an admin action extension in the product variant details page when a selling plan group is present. Open this extension from the "Purchase Options card".

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.product-variant-purchase-option.action.render': RenderExtension<

PurchaseOptionsCardConfigurationApi<'admin.product-variant-purchase-option.action.render'>,

AllComponents

>;

// Print actions and bulk print actions

/**

* Renders an admin print action extension in the order index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.order-details.print-action.render': RenderExtension<

PrintActionExtensionApi<'admin.order-details.print-action.render'>,

AllComponents

>;

/**

* Renders an admin print action extension in the product index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.product-details.print-action.render': RenderExtension<

PrintActionExtensionApi<'admin.product-details.print-action.render'>,

AllComponents

>;

/**

* Renders an admin print action extension in the order index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.order-index.selection-print-action.render': RenderExtension<

PrintActionExtensionApi<'admin.order-index.selection-print-action.render'>,

AllComponents

>;

/**

* Renders an admin print action extension in the product index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.product-index.selection-print-action.render': RenderExtension<

PrintActionExtensionApi<'admin.product-index.selection-print-action.render'>,

AllComponents

>;

// Other

/**

* Renders Product Configuration on product details and product variant details

*

* See the [tutorial](/docs/apps/selling-strategies/bundles/product-config) for more information

*/

'admin.product-details.configuration.render': RenderExtension<

ProductDetailsConfigurationApi<'admin.product-details.configuration.render'>,

AllComponents

>;

/**

* Renders Product Configuration on product details and product variant details

*

* See the [tutorial](/docs/apps/selling-strategies/bundles/product-config) for more information

*/

'admin.product-variant-details.configuration.render': RenderExtension<

ProductVariantDetailsConfigurationApi<'admin.product-variant-details.configuration.render'>,

AllComponents

>;

/**

* Renders Order Routing Rule Configuration on order routing settings.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.settings.internal-order-routing-rule.render': RenderExtension<

OrderRoutingRuleApi<'admin.settings.internal-order-routing-rule.render'>,

AllComponents | OrderRoutingComponents

>;

'admin.settings.order-routing-rule.render': RenderExtension<

OrderRoutingRuleApi<'admin.settings.order-routing-rule.render'>,

AllComponents

>;

/**

* Renders Validation Settings within a given validation's add and edit views.

*

* See the [list of available components](/docs/api/admin-extensions/components).

*/

'admin.settings.validation.render': RenderExtension<

ValidationSettingsApi<'admin.settings.validation.render'>,

AllComponents

>;

// Admin action shouldRender targets

/**

* Controls the render state of an admin action extension in the product details page. Open this extension from the "More Actions" menu.

*/

'admin.product-details.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.product-details.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the catalog details page. Open this extension from the "More Actions" menu.

*/

'admin.catalog-details.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.catalog-details.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the company details page. Open this extension from the "More Actions" menu.

*/

'admin.company-details.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.company-details.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the gift card details page. Open this extension from the "More Actions" menu.

*/

'admin.gift-card-details.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.gift-card-details.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the order details page. Open this extension from the "More Actions" menu.

*/

'admin.order-details.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.order-details.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the customer details page. Open this extension from the "More Actions" menu.

*/

'admin.customer-details.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.customer-details.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the customer segment details page. Open this extension from the "Use segment" button.

*/

'admin.customer-segment-details.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.customer-segment-details.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the product index page. Open this extension from the "More Actions" menu.

*/

'admin.product-index.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.product-index.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the order index page. Open this extension from the "More Actions" menu.

*/

'admin.order-index.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.order-index.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the customer index page. Open this extension from the "More Actions" menu.

*/

'admin.customer-index.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.customer-index.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the discount index page. Open this extension from the "More Actions" menu.

*/

'admin.discount-index.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.discount-index.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the collection details page. Open this extension from the "More Actions" menu.

*/

'admin.collection-details.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.collection-details.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the collection index page. Open this extension from the "More Actions" menu.

*/

'admin.collection-index.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.collection-index.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the abandoned checkout page. Open this extension from the "More Actions" menu.

*/

'admin.abandoned-checkout-details.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.abandoned-checkout-details.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the product variant details page. Open this extension from the "More Actions" menu.

*/

'admin.product-variant-details.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.product-variant-details.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the draft order details page. Open this extension from the "More Actions" menu.

*/

'admin.draft-order-details.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.draft-order-details.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the draft orders page. Open this extension from the "More Actions" menu.

*/

'admin.draft-order-index.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.draft-order-index.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the discount details page. Open this extension from the "More Actions" menu.

*/

'admin.discount-details.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.discount-details.action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the order fulfilled card. Open this extension from the "3-dot" menu inside the order fulfilled card.

* Note: This extension will only be visible on orders which were fulfilled by your app.

*/

'admin.order-fulfilled-card.action.should-render': RunnableExtension<

ShouldRenderApi<'admin.order-fulfilled-card.action.should-render'>,

ShouldRenderOutput

>;

// Admin bulk action shouldRender targets

/**

* Controls the render state of an admin action extension in the product index page when multiple resources are selected. Open this extension from the "More Actions"  menu of the resource list. The resource ids are available to this extension at runtime.

*/

'admin.product-index.selection-action.should-render': RunnableExtension<

ShouldRenderApi<'admin.product-index.selection-action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the order index page when multiple resources are selected. Open this extension from the "More Actions"  menu of the resource list. The resource ids are available to this extension at runtime.

*/

'admin.order-index.selection-action.should-render': RunnableExtension<

ShouldRenderApi<'admin.order-index.selection-action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the customer index page when multiple resources are selected. Open this extension from the "More Actions" menu of the resource list. The resource ids are available to this extension at runtime.

*/

'admin.customer-index.selection-action.should-render': RunnableExtension<

ShouldRenderApi<'admin.customer-index.selection-action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin action extension in the draft order page when multiple resources are selected. Open this extension from the "3-dot" menu.

*/

'admin.draft-order-index.selection-action.should-render': RunnableExtension<

ShouldRenderApi<'admin.draft-order-index.selection-action.should-render'>,

ShouldRenderOutput

>;

// Admin print action and bulk print action shouldRender targets

/**

* Controls the render state of an admin print action extension in the order index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.

*/

'admin.order-details.print-action.should-render': RunnableExtension<

ShouldRenderApi<'admin.order-details.print-action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin print action extension in the product index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.

*/

'admin.product-details.print-action.should-render': RunnableExtension<

ShouldRenderApi<'admin.product-details.print-action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin print action extension in the order index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.

*/

'admin.order-index.selection-print-action.should-render': RunnableExtension<

ShouldRenderApi<'admin.order-index.selection-print-action.should-render'>,

ShouldRenderOutput

>;

/**

* Controls the render state of an admin print action extension in the product index page when multiple resources are selected. Open this extension from the "Print" menu of the resource list. The resource ids are available to this extension at runtime.

*/

'admin.product-index.selection-print-action.should-render': RunnableExtension<

ShouldRenderApi<'admin.product-index.selection-print-action.should-render'>,

ShouldRenderOutput

>;

}

```### RenderExtension```

export interface RenderExtension<

Api,

AllowedComponents extends RemoteComponentType<

string,

any,

any

> = RemoteComponentType<any, any, any>,

> {

(

connection: RenderExtensionConnection<AllowedComponents>,

api: Api,

): void | Promise<void>;

}

```### AllComponentsSee the [list of available components](/docs/api/admin-extensions/components).```

any

```### RunnableExtension```

export interface RunnableExtension<Api, Output> {

(api: Api): Output | Promise<Output>;

}

```### ShouldRenderApi- authProvides methods for authenticating calls to an app backend.```

Auth

```- dataInformation about the currently viewed or selected items.```

Data

```- extensionThe identifier of the running extension target.```

{ target: ExtensionTarget; }

```- i18nUtilities for translating content according to the current localization of the admin. More info - /docs/apps/checkout/best-practices/localizing-ui-extensions```

I18n

```- intentsProvides information to the receiver the of an intent.```

Intents

```- queryUsed to query the Admin GraphQL API```

<Data = unknown, Variables = { [key: string]: unknown; }>(query: string, options?: { variables?: Variables; version?: Omit<ApiVersion, "2023-04">; }) => Promise<{ data?: Data; errors?: GraphQLError[]; }>

``````

export interface ShouldRenderApi<ExtensionTarget extends AnyExtensionTarget>

extends StandardApi<ExtensionTarget> {

/**

* Information about the currently viewed or selected items.

*/

data: Data;

}

```### I18n- formatCurrencyReturns a localized currency value.

This function behaves like the standard `Intl.NumberFormat()` with a style of `currency` applied. It uses the buyer's locale by default.```

(number: number | bigint, options?: { inExtensionLocale?: boolean; } & NumberFormatOptions) => string

```- formatDateReturns a localized date value.

This function behaves like the standard `Intl.DateTimeFormatOptions()` and uses the buyer's locale by default. Formatting options can be passed in as options.```

(date: Date, options?: { inExtensionLocale?: boolean; } & DateTimeFormatOptions) => string

```- formatNumberReturns a localized number.

This function behaves like the standard `Intl.NumberFormat()` with a style of `decimal` applied. It uses the buyer's locale by default.```

(number: number | bigint, options?: { inExtensionLocale?: boolean; } & NumberFormatOptions) => string

```- translateReturns translated content in the buyer's locale, as supported by the extension.

- `options.count` is a special numeric value used in pluralization.

- The other option keys and values are treated as replacements for interpolation.

- If the replacements are all primitives, then `translate()` returns a single string.

- If replacements contain UI components, then `translate()` returns an array of elements.```

I18nTranslate

``````

export interface I18n {

/**

* Returns a localized number.

*

* This function behaves like the standard `Intl.NumberFormat()`

* with a style of `decimal` applied. It uses the buyer's locale by default.

*

* @param options.inExtensionLocale - if true, use the extension's locale

*/

formatNumber: (

number: number | bigint,

options?: {inExtensionLocale?: boolean} & Intl.NumberFormatOptions,

) => string;

/**

* Returns a localized currency value.

*

* This function behaves like the standard `Intl.NumberFormat()`

* with a style of `currency` applied. It uses the buyer's locale by default.

*

* @param options.inExtensionLocale - if true, use the extension's locale

*/

formatCurrency: (

number: number | bigint,

options?: {inExtensionLocale?: boolean} & Intl.NumberFormatOptions,

) => string;

/**

* Returns a localized date value.

*

* This function behaves like the standard `Intl.DateTimeFormatOptions()` and uses

* the buyer's locale by default. Formatting options can be passed in as

* options.

*

* @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat0

* @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat#using_options

*

* @param options.inExtensionLocale - if true, use the extension's locale

*/

formatDate: (

date: Date,

options?: {inExtensionLocale?: boolean} & Intl.DateTimeFormatOptions,

) => string;

/**

* Returns translated content in the buyer's locale,

* as supported by the extension.

*

* - `options.count` is a special numeric value used in pluralization.

* - The other option keys and values are treated as replacements for interpolation.

* - If the replacements are all primitives, then `translate()` returns a single string.

* - If replacements contain UI components, then `translate()` returns an array of elements.

*/

translate: I18nTranslate;

}

```### I18nTranslateThis defines the i18n.translate() signature.```

export interface I18nTranslate {

/**

* This returns a translated string matching a key in a locale file.

*

* @example translate("banner.title")

*/

<ReplacementType = string>(

key: string,

options?: Record<string, ReplacementType | string | number>,

): ReplacementType extends string | number

? string

: (string | ReplacementType)[];

}

```### Intents- launchUrlThe URL that was used to launch the intent.```

string | URL

``````

export interface Intents {

/**

* The URL that was used to launch the intent.

*/

launchUrl?: string | URL;

}

```### ApiVersionUnion of supported API versions```

'2023-04' | '2023-07' | '2023-10' | '2024-01' | '2024-04' | '2024-07' | '2024-10' | '2025-01' | '2025-04' | 'unstable'

```### GraphQLErrorGraphQL error returned by the Shopify Admin API.- locations```

{ line: number; column: string; }

```- message```

string

``````

export interface GraphQLError {

message: string;

locations: {

line: number;

column: string;

};

}

```### ShouldRenderOutput- display```

boolean

``````

interface ShouldRenderOutput {

display: boolean;

}

```### BlockExtensionApi- authProvides methods for authenticating calls to an app backend.```

Auth

```- dataInformation about the currently viewed or selected items.```

Data

```- extensionThe identifier of the running extension target.```

{ target: ExtensionTarget; }

```- i18nUtilities for translating content according to the current localization of the admin. More info - /docs/apps/checkout/best-practices/localizing-ui-extensions```

I18n

```- intentsProvides information to the receiver the of an intent.```

Intents

```- navigationProvides methods to navigate to other features in the Admin. Currently, only navigation from an admin block to an admin action extension *on the same resource page* is supported. For example, you can navigate from an admin block on the product details page (`admin.product-details.block.render`) to an admin action on the product details page (`admin.product-details.action.render`).```

Navigation

```- pickerRenders a custom [Picker](picker) dialog allowing users to select values from a list.```

PickerApi

```- queryUsed to query the Admin GraphQL API```

<Data = unknown, Variables = { [key: string]: unknown; }>(query: string, options?: { variables?: Variables; version?: Omit<ApiVersion, "2023-04">; }) => Promise<{ data?: Data; errors?: GraphQLError[]; }>

```- resourcePickerRenders the [Resource Picker](resource-picker), allowing users to select a resource for the extension to use as part of its flow.```

ResourcePickerApi

``````

export interface BlockExtensionApi<ExtensionTarget extends AnyExtensionTarget>

extends StandardApi<ExtensionTarget> {

/**

* Information about the currently viewed or selected items.

*/

data: Data;

/**

* Provides methods to navigate to other features in the Admin. Currently, only navigation from an admin block to an admin action extension *on the same resource page* is supported.

* For example, you can navigate from an admin block on the product details page (`admin.product-details.block.render`) to an admin action on the product details page (`admin.product-details.action.render`).

*/

navigation: Navigation;

/**

* Renders the [Resource Picker](resource-picker), allowing users to select a resource for the extension to use as part of its flow.

*/

resourcePicker: ResourcePickerApi;

/**

* Renders a custom [Picker](picker) dialog allowing users to select values from a list.

*/

picker: PickerApi;

}

```### Navigation- navigateNavigate to a specific route.```

(url: string | URL) => void

``````

export interface Navigation {

/**

* Navigate to a specific route.

*

* @example navigation.navigate('extension://my-admin-action-extension-handle')

*/

navigate: (url: string | URL) => void;

}

```### PickerApi- options```

PickerOptions

```Promise<Picker>```

Promise<Picker>

``````

(options: PickerOptions) => Promise<Picker>

```### PickerOptions- headersThe data headers for the picker. These are used to display the table headers in the picker modal.```

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

Badge[]

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

badges?: Badge[];

/**

* The thumbnail to display at the start of the row. This is used to display an image or icon for the item.

*/

thumbnail?: {url: string};

}

```### Badge- content```

string

```- progress```

Progress

```- tone```

Tone

``````

interface Badge {

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

```### ResourcePickerApi- options```

ResourcePickerOptions

```Promise<SelectPayload<ResourcePickerOptions['type']> | undefined>```

Promise<SelectPayload<ResourcePickerOptions['type']> | undefined>

``````

(

options: ResourcePickerOptions,

) => Promise<SelectPayload<ResourcePickerOptions['type']> | undefined>

```### ResourcePickerOptions- actionThe action verb appears in the title and as the primary action of the Resource Picker.```

'add' | 'select'

```- filterFilters for what resource to show.```

Filters

```- multipleWhether to allow selecting multiple items of a specific type or not. If a number is provided, then limit the selections to a maximum of that number of items. When type is Product, the user may still select multiple variants of a single product, even if multiple is false.```

boolean | number

```- queryGraphQL initial search query for filtering resources available in the picker. See [search syntax](/docs/api/usage/search-syntax) for more information. This is displayed in the search bar when the picker is opened and can be edited by users. For most use cases, you should use the `filter.query` option instead which doesn't show the query in the UI.```

string

```- selectionIdsResources that should be preselected when the picker is opened.```

BaseResource[]

```- typeThe type of resource you want to pick.```

'product' | 'variant' | 'collection'

``````

export interface ResourcePickerOptions {

/**

* The type of resource you want to pick.

*/

type: 'product' | 'variant' | 'collection';

/**

*  The action verb appears in the title and as the primary action of the Resource Picker.

* @defaultValue 'add'

*/

action?: 'add' | 'select';

/**

* Filters for what resource to show.

*/

filter?: Filters;

/**

* Whether to allow selecting multiple items of a specific type or not. If a number is provided, then limit the selections to a maximum of that number of items. When type is Product, the user may still select multiple variants of a single product, even if multiple is false.

* @defaultValue false

*/

multiple?: boolean | number;

/**

* GraphQL initial search query for filtering resources available in the picker. See [search syntax](/docs/api/usage/search-syntax) for more information.

* This is displayed in the search bar when the picker is opened and can be edited by users.

* For most use cases, you should use the `filter.query` option instead which doesn't show the query in the UI.

* @defaultValue ''

*/

query?: string;

/**

* Resources that should be preselected when the picker is opened.

* @defaultValue []

*/

selectionIds?: BaseResource[];

}

```### Filters- archivedWhether to show [archived products](https://help.shopify.com/en/manual/products/details?shpxid=70af7d87-E0F2-4973-8B09-B972AAF0ADFD#product-availability). Only applies to the Product resource type picker. Setting this to undefined will show a badge on draft products.```

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

```### SelectPayload```

SelectPayload<Type>

```### CustomerSegmentTemplateApi- __enabledFeatures```

string[]

```- authProvides methods for authenticating calls to an app backend.```

Auth

```- extensionThe identifier of the running extension target.```

{ target: ExtensionTarget; }

```- i18nUtilities for translating content according to the current localization of the admin. More info - /docs/apps/checkout/best-practices/localizing-ui-extensions```

I18n

```- intentsProvides information to the receiver the of an intent.```

Intents

```- queryUsed to query the Admin GraphQL API```

<Data = unknown, Variables = { [key: string]: unknown; }>(query: string, options?: { variables?: Variables; version?: Omit<ApiVersion, "2023-04">; }) => Promise<{ data?: Data; errors?: GraphQLError[]; }>

``````

export interface CustomerSegmentTemplateApi<

ExtensionTarget extends AnyExtensionTarget,

> extends StandardApi<ExtensionTarget> {

/* Utilities for translating content according to the current `localization` of the admin. */

i18n: I18n;

/** @private */

__enabledFeatures: string[];

}

```### CustomerSegmentTemplateComponent```

any

```### DiscountFunctionSettingsApi- applyMetafieldChangeApplies a change to the discount function settings.```

ApplyMetafieldChange

```- authProvides methods for authenticating calls to an app backend.```

Auth

```- data```

DiscountFunctionSettingsData

```- extensionThe identifier of the running extension target.```

{ target: ExtensionTarget; }

```- i18nUtilities for translating content according to the current localization of the admin. More info - /docs/apps/checkout/best-practices/localizing-ui-extensions```

I18n

```- intentsProvides information to the receiver the of an intent.```

Intents

```- navigationProvides methods to navigate to other features in the Admin. Currently, only navigation from an admin block to an admin action extension *on the same resource page* is supported. For example, you can navigate from an admin block on the product details page (`admin.product-details.block.render`) to an admin action on the product details page (`admin.product-details.action.render`).```

Navigation

```- pickerRenders a custom [Picker](picker) dialog allowing users to select values from a list.```

PickerApi

```- queryUsed to query the Admin GraphQL API```

<Data = unknown, Variables = { [key: string]: unknown; }>(query: string, options?: { variables?: Variables; version?: Omit<ApiVersion, "2023-04">; }) => Promise<{ data?: Data; errors?: GraphQLError[]; }>

```- resourcePickerRenders the [Resource Picker](resource-picker), allowing users to select a resource for the extension to use as part of its flow.```

ResourcePickerApi

``````

export interface DiscountFunctionSettingsApi<

ExtensionTarget extends AnyExtensionTarget,

> extends Omit<BlockExtensionApi<ExtensionTarget>, 'data'> {

/**

* Applies a change to the discount function settings.

*/

applyMetafieldChange: ApplyMetafieldChange;

data: DiscountFunctionSettingsData;

}

```### ApplyMetafieldChange- change```

MetafieldChange

```Promise<MetafieldChangeResult>```

Promise<MetafieldChangeResult>

``````

(

change: MetafieldChange,

) => Promise<MetafieldChangeResult>

```### MetafieldChange```

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

```### DiscountFunctionSettingsDataThe object that exposes the validation with its settings.- id```

Discount

```- metafields```

Metafield[]

``````

export interface DiscountFunctionSettingsData {

id: Discount;

metafields: Metafield[];

}

```### Discount- idthe discount's gid```

string

``````

interface Discount {

/**

* the discount's gid

*/

id: string;

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

```### PrintActionExtensionApi- authProvides methods for authenticating calls to an app backend.```

Auth

```- dataInformation about the currently viewed or selected items.```

Data

```- extensionThe identifier of the running extension target.```

{ target: ExtensionTarget; }

```- i18nUtilities for translating content according to the current localization of the admin. More info - /docs/apps/checkout/best-practices/localizing-ui-extensions```

I18n

```- intentsProvides information to the receiver the of an intent.```

Intents

```- pickerRenders a custom [Picker](picker) dialog allowing users to select values from a list.```

PickerApi

```- queryUsed to query the Admin GraphQL API```

<Data = unknown, Variables = { [key: string]: unknown; }>(query: string, options?: { variables?: Variables; version?: Omit<ApiVersion, "2023-04">; }) => Promise<{ data?: Data; errors?: GraphQLError[]; }>

```- resourcePickerRenders the [Resource Picker](resource-picker), allowing users to select a resource for the extension to use as part of its flow.```

ResourcePickerApi

``````

export interface PrintActionExtensionApi<

ExtensionTarget extends AnyExtensionTarget,

> extends StandardApi<ExtensionTarget> {

/**

* Information about the currently viewed or selected items.

*/

data: Data;

/**

* Renders the [Resource Picker](resource-picker), allowing users to select a resource for the extension to use as part of its flow.

*/

resourcePicker: ResourcePickerApi;

/**

* Renders a custom [Picker](picker) dialog allowing users to select values from a list.

*/

picker: PickerApi;

}

```### ProductDetailsConfigurationApi- authProvides methods for authenticating calls to an app backend.```

Auth

```- dataInformation about the currently viewed or selected items.```

Data & { product: Product; app: { launchUrl: string; applicationUrl: string; }; }

```- extensionThe identifier of the running extension target.```

{ target: ExtensionTarget; }

```- i18nUtilities for translating content according to the current localization of the admin. More info - /docs/apps/checkout/best-practices/localizing-ui-extensions```

I18n

```- intentsProvides information to the receiver the of an intent.```

Intents

```- navigationProvides methods to navigate to other features in the Admin. Currently, only navigation from an admin block to an admin action extension *on the same resource page* is supported. For example, you can navigate from an admin block on the product details page (`admin.product-details.block.render`) to an admin action on the product details page (`admin.product-details.action.render`).```

Navigation

```- pickerRenders a custom [Picker](picker) dialog allowing users to select values from a list.```

PickerApi

```- queryUsed to query the Admin GraphQL API```

<Data = unknown, Variables = { [key: string]: unknown; }>(query: string, options?: { variables?: Variables; version?: Omit<ApiVersion, "2023-04">; }) => Promise<{ data?: Data; errors?: GraphQLError[]; }>

```- resourcePickerRenders the [Resource Picker](resource-picker), allowing users to select a resource for the extension to use as part of its flow.```

ResourcePickerApi

``````

export interface ProductDetailsConfigurationApi<

ExtensionTarget extends AnyExtensionTarget,

> extends BlockExtensionApi<ExtensionTarget> {

data: Data & {

/*

@deprecated

The product currently being viewed in the admin.

*/

product: Product;

app: {

launchUrl: string;

applicationUrl: string;

};

};

}

```### Product- handle```

string

```- hasOnlyDefaultVariant```

boolean

```- id```

string

```- onlineStoreUrl```

string

```- options```

{ id: string; name: string; position: number; values: string[]; }[]

```- productCategory```

string

```- productComponents```

ProductComponent[]

```- productType```

string

```- status```

'ACTIVE' | 'ARCHIVED' | 'DRAFT'

```- title```

string

```- totalInventory```

number

```- totalVariants```

number

``````

interface Product {

id: string;

title: string;

handle: string;

status: 'ACTIVE' | 'ARCHIVED' | 'DRAFT';

totalVariants: number;

totalInventory: number;

hasOnlyDefaultVariant: boolean;

onlineStoreUrl?: string;

options: {

id: string;

name: string;

position: number;

values: string[];

}[];

productType: string;

productCategory?: string;

productComponents: ProductComponent[];

}

```### ProductComponent- componentVariantsCount```

number

```- featuredImage```

{

id?: string | null;

url?: string | null;

altText?: string | null;

} | null

```- id```

string

```- nonComponentVariantsCount```

number

```- productUrl```

string

```- title```

string

```- totalVariants```

number

``````

export interface ProductComponent {

id: string;

title: string;

featuredImage?: {

id?: string | null;

url?: string | null;

altText?: string | null;

} | null;

totalVariants: number;

productUrl: string;

componentVariantsCount: number;

nonComponentVariantsCount: number;

}

```### PurchaseOptionsCardConfigurationApi- authProvides methods for authenticating calls to an app backend.```

Auth

```- closeCloses the extension. Calling this method is equivalent to the merchant clicking the "x" in the corner of the overlay.```

() => void

```- dataInformation about the currently viewed or selected items.```

{ selected: { id: string; sellingPlanId?: string; }[]; }

```- extensionThe identifier of the running extension target.```

{ target: ExtensionTarget; }

```- i18nUtilities for translating content according to the current localization of the admin. More info - /docs/apps/checkout/best-practices/localizing-ui-extensions```

I18n

```- intentsProvides information to the receiver the of an intent.```

Intents

```- pickerRenders a custom [Picker](picker) dialog allowing users to select values from a list.```

PickerApi

```- queryUsed to query the Admin GraphQL API```

<Data = unknown, Variables = { [key: string]: unknown; }>(query: string, options?: { variables?: Variables; version?: Omit<ApiVersion, "2023-04">; }) => Promise<{ data?: Data; errors?: GraphQLError[]; }>

```- resourcePickerRenders the [Resource Picker](resource-picker), allowing users to select a resource for the extension to use as part of its flow.```

ResourcePickerApi

``````

export interface PurchaseOptionsCardConfigurationApi<

ExtensionTarget extends AnyExtensionTarget,

> extends ActionExtensionApi<ExtensionTarget> {

data: {

selected: {id: string; sellingPlanId?: string}[];

};

}

```### ProductVariantDetailsConfigurationApi- authProvides methods for authenticating calls to an app backend.```

Auth

```- dataInformation about the currently viewed or selected items.```

Data & { variant: ProductVariant; app: { launchUrl: string; applicationUrl: string; }; }

```- extensionThe identifier of the running extension target.```

{ target: ExtensionTarget; }

```- i18nUtilities for translating content according to the current localization of the admin. More info - /docs/apps/checkout/best-practices/localizing-ui-extensions```

I18n

```- intentsProvides information to the receiver the of an intent.```

Intents

```- navigationProvides methods to navigate to other features in the Admin. Currently, only navigation from an admin block to an admin action extension *on the same resource page* is supported. For example, you can navigate from an admin block on the product details page (`admin.product-details.block.render`) to an admin action on the product details page (`admin.product-details.action.render`).```

Navigation

```- pickerRenders a custom [Picker](picker) dialog allowing users to select values from a list.```

PickerApi

```- queryUsed to query the Admin GraphQL API```

<Data = unknown, Variables = { [key: string]: unknown; }>(query: string, options?: { variables?: Variables; version?: Omit<ApiVersion, "2023-04">; }) => Promise<{ data?: Data; errors?: GraphQLError[]; }>

```- resourcePickerRenders the [Resource Picker](resource-picker), allowing users to select a resource for the extension to use as part of its flow.```

ResourcePickerApi

``````

export interface ProductVariantDetailsConfigurationApi<

ExtensionTarget extends AnyExtensionTarget,

> extends BlockExtensionApi<ExtensionTarget> {

data: Data & {

/*

@deprecated

The product variant currently being viewed in the admin.

*/

variant: ProductVariant;

app: {

launchUrl: string;

applicationUrl: string;

};

};

}

```### ProductVariant- barcode```

string

```- compareAtPrice```

string

```- displayName```

string

```- id```

string

```- price```

string

```- productVariantComponents```

ProductVariantComponent[]

```- selectedOptions```

{ name: string; value: string; }[]

```- sku```

string

```- taxable```

boolean

```- taxCode```

string

```- title```

string

```- weight```

number

``````

interface ProductVariant {

id: string;

sku: string;

barcode: string;

title: string;

displayName: string;

price: string;

compareAtPrice: string;

taxable: boolean;

taxCode: string;

weight: number;

selectedOptions: {

name: string;

value: string;

}[];

productVariantComponents: ProductVariantComponent[];

}

```### ProductVariantComponent- displayName```

string

```- id```

string

```- image```

{

id?: string | null;

url?: string | null;

altText?: string | null;

} | null

```- productVariantUrl```

string

```- selectedOptions```

{ name: string; value: string; }[]

```- sku```

string

```- title```

string

``````

export interface ProductVariantComponent {

id: string;

displayName: string;

title: string;

sku?: string;

image?: {

id?: string | null;

url?: string | null;

altText?: string | null;

} | null;

productVariantUrl: string;

selectedOptions: {

name: string;

value: string;

}[];

}

```### OrderRoutingRuleApi- applyMetafieldsChange```

ApplyMetafieldsChange

```- authProvides methods for authenticating calls to an app backend.```

Auth

```- data```

Data

```- extensionThe identifier of the running extension target.```

{ target: ExtensionTarget; }

```- i18nUtilities for translating content according to the current localization of the admin. More info - /docs/apps/checkout/best-practices/localizing-ui-extensions```

I18n

```- intentsProvides information to the receiver the of an intent.```

Intents

```- queryUsed to query the Admin GraphQL API```

<Data = unknown, Variables = { [key: string]: unknown; }>(query: string, options?: { variables?: Variables; version?: Omit<ApiVersion, "2023-04">; }) => Promise<{ data?: Data; errors?: GraphQLError[]; }>

``````

export interface OrderRoutingRuleApi<ExtensionTarget extends AnyExtensionTarget>

extends StandardApi<ExtensionTarget> {

applyMetafieldsChange: ApplyMetafieldsChange;

data: Data;

}

```### ApplyMetafieldsChange- changes```

MetafieldsChange[]

```void```

void

``````

(changes: MetafieldsChange[]) => void

```### MetafieldsChange```

MetafieldUpdateChange | MetafieldRemoveChange | MetafieldUpdateChange[] | MetafieldRemoveChange[]

```### OrderRoutingComponents```

any

```### ValidationSettingsApi- applyMetafieldChangeApplies a change to the validation settings.```

ApplyMetafieldChange

```- authProvides methods for authenticating calls to an app backend.```

Auth

```- data```

ValidationData

```- extensionThe identifier of the running extension target.```

{ target: ExtensionTarget; }

```- i18nUtilities for translating content according to the current localization of the admin. More info - /docs/apps/checkout/best-practices/localizing-ui-extensions```

I18n

```- intentsProvides information to the receiver the of an intent.```

Intents

```- queryUsed to query the Admin GraphQL API```

<Data = unknown, Variables = { [key: string]: unknown; }>(query: string, options?: { variables?: Variables; version?: Omit<ApiVersion, "2023-04">; }) => Promise<{ data?: Data; errors?: GraphQLError[]; }>

``````

export interface ValidationSettingsApi<

ExtensionTarget extends AnyExtensionTarget,

> extends StandardApi<ExtensionTarget> {

/**

* Applies a change to the validation settings.

*/

applyMetafieldChange: ApplyMetafieldChange;

data: ValidationData;

}

```### ValidationDataThe object that exposes the validation with its settings.- shopifyFunction```

ShopifyFunction

```- validation```

Validation

``````

export interface ValidationData {

validation?: Validation;

shopifyFunction: ShopifyFunction;

}

```### ShopifyFunction- idthe validation function's unique identifier```

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

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)