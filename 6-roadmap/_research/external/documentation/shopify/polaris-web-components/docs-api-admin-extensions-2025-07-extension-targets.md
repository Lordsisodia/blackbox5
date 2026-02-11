---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/extension-targets",
    "fetched_at": "2026-02-10T13:27:50.831599",
    "status": 200,
    "size_bytes": 353089
  },
  "metadata": {
    "title": "Targets",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "2025-07",
    "component": "extension-targets"
  }
}
---

# Targets

# TargetsA [target](/docs/apps/app-extensions/configuration#targets) represents where your admin UI extension will appear.You register targets in your `shopify.extension.toml` and inside the Javascript file denoted by your toml's `module` property.Ask assistant

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07

## [Anchor to Admin action locations](/docs/api/admin-extensions/2025-07/targets#admin-action-locations)Admin action locationsAdmin action extensions appear on resource pages throughout the admin. Learn more about [admin actions](/docs/apps/admin/admin-actions-and-blocks#admin-actions). Each target has a companion target that supports [controlling the visibility of the admin action menu item](/docs/apps/build/admin/actions-blocks/hide-extensions?extension=react).Abandoned checkout details

This page shows information about a single abandoned checkout. The `admin.abandoned-checkout-details.action.render` target is available on this page. You can control the visibility of the action by using the `admin.abandoned-checkout-details.action.should-render` target.Catalog details

This page shows information about a single catalog. The `admin.catalog-details.action.render` target is available on this page. You can control the visibility of the action by using the `admin.catalog-details.action.should-render` target.Collection details

This page shows information about a single collection. The `admin.collection-details.action.render` target is available on this page. You can control the visibility of the action by using the `admin.collection-details.action.should-render` target.Collection index

This page shows a table of multiple collections. The `admin.collection-index.action.render` target is available on this page. You can control the visibility of the action by using the `admin.collection-index.action.should-render` target.Company details

This page shows information about a single company. The `admin.company-details.action.render` target is available on this page. You can control the visibility of the action by using the `admin.company-details.action.should-render` target.Customer details

This page shows information about a single customer. The `admin.customer-details.action.render` target is available on this page. You can control the visibility of the action by using the `admin.customer-details.action.should-render` target.Customer index

This page shows a table of multiple customers. The `admin.customer-index.action.render` target is available on this page. You can control the visibility of the action by using the `admin.customer-index.action.should-render` target.Customer index selection

This page shows a table of multiple customers. The `admin.customer-index.selection-action.render` target is available on this page when multiple customers are selected. You can control the visibility of the action by using the `admin.customer-index.selection-action.should-render` target.Customer segment details

This page shows information about a single customer segment. The `admin.customer-segment-details.action.render` target is available on this page. You can control the visibility of the action by using the `admin.customer-segment-details.action.should-render` target.Discount details

This page shows information about a single discount. The `admin.discount-details.action.render` target is available on this page. You can control the visibility of the action by using the `admin.discount-details.action.should-render` target.Discount index

This page shows a table of multiple discounts. The `admin.discount-index.action.render` target is available on this page. You can control the visibility of the action by using the `admin.discount-index.action.should-render` target.Draft order details

This page shows information about a single draft order. The `admin.draft-order-details.action.render` target is available on this page. You can control the visibility of the action by using the `admin.draft-order-details.action.should-render` target.Draft order index

This page shows a table of multiple draft orders. The `admin.draft-order-index.action.render` target is available on this page. You can control the visibility of the action by using the `admin.draft-order-index.action.should-render` target.Draft order index selection

This page shows a table of multiple draft orders. The `admin.draft-order-index.selection-action.render` target is available on this page when multiple draft orders are selected. You can control the visibility of the action by using the `admin.draft-order-index.selection-action.should-render` target.Gift card details

This page shows information about a single gift card. The `admin.gift-card-details.action.render` target is available on this page. You can control the visibility of the action by using the `admin.gift-card-details.action.should-render` target.Order details

This page shows information about a single order. The `admin.order-details.action.render` target is available on this page. You can control the visibility of the action by using the `admin.order-details.action.should-render` target.Order details fulfilled card

This page shows information about a single order, including a card showing the fulfillment details. The `admin.order-fulfilled-card.action.render` target is available on this page, but only if your app is selected as the fulfillment app for that order. You can control the visibility of the action by using the `admin.order-fulfilled-card.action.should-render` target.Order index

This page shows a table of multiple orders. The `admin.order-index.action.render` target is available on this page. You can control the visibility of the action by using the `admin.order-index.action.should-render` target.Order index selection

This page shows a table of multiple orders. The `admin.order-index.selection-action.render` target is available on this page when multiple orders are selected. You can control the visibility of the action by using the `admin.order-index.selection-action.should-render` target.Product details

This page shows information about a single product. The `admin.product-details.action.render` target is available on this page. You can control the visibility of the action by using the `admin.product-details.action.should-render` target.Product index

This page shows a table of multiple products. The `admin.product-index.action.render` target is available on this page. You can control the visibility of the action by using the `admin.product-index.action.should-render` target.Product index selection

This page shows a table of multiple products. The `admin.product-index.selection-action.render` target is available on this page when multiple products are selected. You can control the visibility of the action by using the `admin.product-index.selection-action.should-render` target.Product variant details

This page shows information about a single product variant. The `admin.product-variant-details.action.render` target is available on this page. You can control the visibility of the action by using the `admin.product-variant-details.action.should-render` target.Product detail purchase options card

This page shows information about a single product, including a card showing purchase options. The `admin.product-purchase-option.action.render` target is available on this page when selling plans exists. You can control the visibility of the action by using the `admin.product-purchase-option.action.should-render` target.Product variant detail purchase options card

This page shows information about a single product variant, including a card showing purchase options. The `admin.product-variant-purchase-option.action.render` target is available on this page when selling plans exists. You can control the visibility of the action by using the `admin.product-variant-purchase-option.action.should-render` target.

## [Anchor to Admin block locations](/docs/api/admin-extensions/2025-07/targets#admin-block-locations)Admin block locationsAdmin block extensions appear on resource detail pages throughout the admin. Learn more about [admin blocks](/docs/apps/admin/admin-actions-and-blocks#admin-blocks).Abandoned checkout details

This page shows information about a single abandoned checkout. The `admin.abandoned-checkout-details.block.render` target is available on this page.Catalog details

This page shows information about a single catalog. The `admin.catalog-details.block.render` target is available on this page.Collection details

This page shows information about a single collection. The `admin.collection-details.block.render` target is available on this page.Company details

This page shows information about a single company. The `admin.company-details.block.render` target is available on this page.Company location details

This page shows information about a location for a company. The `admin.company-location-details.block.render` target is available on this page.Customer details

This page shows information about a single customer. The `admin.customer-details.block.render` target is available on this page.Draft order details

This page shows information about a single draft order. The `admin.draft-order-details.block.render` target is available on this page.Gift card details

This page shows information about a single gift card. The `admin.gift-card-details.block.render` target is available on this page.Discount details function settings

This page shows information about a single discount. The `admin.discount-details.function-settings.render` target is available on this page.Order details

This page shows information about a single order. The `admin.order-details.block.render` target is available on this page.Product details

This page shows information about a single product. The `admin.product-details.block.render` target is available on this page.Product variant details

This page shows information about a single product variant. The `admin.product-variant-details.block.render` target is available on this page.

## [Anchor to Admin print action locations](/docs/api/admin-extensions/2025-07/targets#admin-print-action-locations)Admin print action locationsAdmin print action extensions appear on order and product pages in the admin.Order details

This page shows information about a single order. The `admin.order-details.print-action.render` target is available on this page. You can control the visibility of the print action by using the `admin.order-details.print-action.should-render` targetProduct details

This page shows information about a single product. The `admin.product-details.print-action.render` target is available on this page. You can control the visibility of the print action by using the `admin.product-details.print-action.should-render` targetOrder index selection

This page shows a table of multiple orders. The `admin.order-index.selection-print-action.render` target is available on this page when multiple orders are selected. You can control the visibility of the print action by using the `admin.order-index.selection-print-action.should-render` targetProduct index selection

This page shows a table of multiple products. The `admin.product-index.selection-print-action.render` target is available on this page when multiple products are selected. You can control the visibility of the print action by using the `admin.product-index.selection-print-action.should-render` target

## [Anchor to Admin link extension locations](/docs/api/admin-extensions/2025-07/targets#admin-link-extension-locations)Admin link extension locationsAdmin link extensions appear on resource pages throughout the admin. Learn more about [admin actions](/docs/apps/admin/admin-actions-and-blocks#admin-actions).Abandoned checkout details

This page shows information about a single abandoned checkout. The `admin.abandoned-checkout-details.action.link` target is available in the "More actions" on the page.Collection details

This page shows information about a single collection. The `admin.collection-details.action.link` target is available in the "More actions" on the page.Collection index

This page shows a table of multiple collections. The `admin.collection-index.action.link` target is available in the "More actions" on the page.Customer details

This page shows information about a single customer. The `admin.customer-details.action.link` target is available in the "More actions" on the page.Customer index

This page shows a table of multiple customers. The `admin.customer-index.action.link` target is available in the "More actions" on the page.Customer index selection

This page shows a table of multiple customers. The `admin.customer-index.selection-action.link` target is available on this page when multiple customers are selected.Discount index

This page shows a table of multiple discounts. The `admin.discount-index.action.link` target is available in the "More actions" on the page.Draft order details

This page shows information about a single draft order. The `admin.draft-order-details.action.link` target is available in the "More actions" on the page.Draft order index

This page shows a table of multiple draft orders. The `admin.draft-order-index.action.link` target is available in the "More actions" on the page.Draft order index selection

This page shows a table of multiple draft orders. The `admin.draft-order-index.selection-action.link` target is available on this page when multiple draft orders are selected.Order details

This page shows information about a single order. The `admin.order-details.action.link` target is available in the "More actions" on the page.Order index

This page shows a table of multiple orders. The `admin.order-index.action.link` target is available in the "More actions" on the page.Order index selection

This page shows a table of multiple orders. The `admin.order-index.selection-action.link` target is available on this page when multiple orders are selected.Product details

This page shows information about a single product. The `admin.product-details.action.link` target is available in the "More actions" on the page.Product index

This page shows a table of multiple products. The `admin.product-index.action.link` target is available in the "More actions" on the page.Product index selection

This page shows a table of multiple products. The `admin.product-index.selection-action.link` target is available on this page when multiple products are selected.Product variant details

This page shows information about a single product variant. The `admin.product-variant-details.action.link` target is available in the "More actions" on the page.

## [Anchor to Customer segmentation locations](/docs/api/admin-extensions/2025-07/targets#customer-segmentation-locations)Customer segmentation locationsCustomer segmentation extensions appear in the [customer segment editor](https://help.shopify.com/en/manual/customers/customer-segmentation/create-customer-segments). Learn more about [customer segmentation](/docs/apps/marketing/customer-segments).### [Anchor to Customer segment editor](/docs/api/admin-extensions/2025-07/targets#customer-segment-editor)Customer segment editorThis page allows editing and templating of customer segments. The `admin.customers.segmentation-templates.render` target is available on this page.

## [Anchor to Product configuration locations](/docs/api/admin-extensions/2025-07/targets#product-configuration-locations)Product configuration locationsProduct configuration extensions appear on the product details and product variant details pages, and allow configuration of product bundles. Learn more about [product configuration](/docs/apps/selling-strategies/bundles/product-config).### [Anchor to Product details configuration](/docs/api/admin-extensions/2025-07/targets#product-details-configuration)Product details configurationThis page shows information about a single product. The `admin.product-details.configuration.render` target is available on this page.### [Anchor to Product variant details configuration](/docs/api/admin-extensions/2025-07/targets#product-variant-details-configuration)Product variant details configurationThis page shows information about a single product variant. The `admin.product-variant-details.configuration.render` target is available on this page.

## [Anchor to Validation settings locations](/docs/api/admin-extensions/2025-07/targets#validation-settings-locations)Validation settings locationsValidation settings extensions appear in the checkout rules section of the settings page. They allow merchants to configure validation rules for their checkout. Learn more about [validation settings](/docs/apps/checkout/validation).### [Anchor to Checkout rules](/docs/api/admin-extensions/2025-07/targets#checkout-rules)Checkout rulesThis page allows merchants to set up rules around their checkout experience. The `admin.settings.validation.render` target is available on this page.

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)