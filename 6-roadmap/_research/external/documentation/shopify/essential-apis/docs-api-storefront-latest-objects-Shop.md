---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront/latest/objects/Shop",
    "fetched_at": "2026-02-10T13:41:07.996038",
    "status": 200,
    "size_bytes": 329267
  },
  "metadata": {
    "title": "Shop - Storefront API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "objects",
    "component": "Shop"
  }
}
---

# Shop - Storefront API

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to Shop](/docs/api/storefront/latest/objects/Shop#top)# ShopobjectAsk assistantRequires `unauthenticated_read_product_listings` access scope.

Shop represents a collection of the general settings and information about the shop.

## [Anchor to Fields](/docs/api/storefront/latest/objects/Shop#fields)Fields- brand (Brand)- customerAccountTranslations ([Translation!])- customerAccountUrl (String)- description (String)- id (ID!)- metafield (Metafield)- metafields ([Metafield]!)- moneyFormat (String!)- name (String!)- paymentSettings (PaymentSettings!)- primaryDomain (Domain!)- privacyPolicy (ShopPolicy)- refundPolicy (ShopPolicy)- shippingPolicy (ShopPolicy)- shipsToCountries ([CountryCode!]!)- shopPayInstallmentsPricing (ShopPayInstallmentsPricing)- socialLoginProviders ([SocialLoginProvider!]!)- subscriptionPolicy (ShopPolicyWithDefault)- termsOfService (ShopPolicy)[Anchor to brand](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.brand)brand•[Brand](/docs/api/storefront/latest/objects/Brand)The shop's branding configuration.

Show fields[Anchor to customerAccountTranslations](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.customerAccountTranslations)customerAccountTranslations•[[Translation!]](/docs/api/storefront/latest/objects/Translation)Translations for customer accounts.

Show fields[Anchor to customerAccountUrl](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.customerAccountUrl)customerAccountUrl•[String](/docs/api/storefront/latest/scalars/String)The URL for the customer account (only present if shop has a customer account vanity domain).

[Anchor to description](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.description)description•[String](/docs/api/storefront/latest/scalars/String)A description of the shop.

[Anchor to id](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.id)id•[ID!](/docs/api/storefront/latest/scalars/ID)non-nullA globally-unique ID.

[Anchor to metafield](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.metafield)metafield•[Metafield](/docs/api/storefront/latest/objects/Metafield) Token access requiredA [custom field](https://shopify.dev/docs/apps/build/custom-data), including its `namespace` and `key`, that's associated with a Shopify resource for the purposes of adding and storing additional information.

Show fields### Arguments[Anchor to namespace](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.metafield.arguments.namespace)namespace•[String](/docs/api/storefront/latest/scalars/String)The container the metafield belongs to. If omitted, the app-reserved namespace will be used.

[Anchor to key](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.metafield.arguments.key)key•[String!](/docs/api/storefront/latest/scalars/String)requiredThe identifier for the metafield.

[Anchor to metafields](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.metafields)metafields•[[Metafield]!](/docs/api/storefront/latest/objects/Metafield)non-null Token access requiredA list of [custom fields](/docs/apps/build/custom-data) that a merchant associates with a Shopify resource.

Show fields### Arguments[Anchor to identifiers](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.metafields.arguments.identifiers)identifiers•[[HasMetafieldsIdentifier!]!](/docs/api/storefront/latest/input-objects/HasMetafieldsIdentifier)requiredThe list of metafields to retrieve by namespace and key.

The input must not contain more than `250` values.

Show input fields[Anchor to moneyFormat](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.moneyFormat)moneyFormat•[String!](/docs/api/storefront/latest/scalars/String)non-nullA string representing the way currency is formatted when the currency isn’t specified.

[Anchor to name](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.name)name•[String!](/docs/api/storefront/latest/scalars/String)non-nullThe shop’s name.

[Anchor to paymentSettings](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.paymentSettings)paymentSettings•[PaymentSettings!](/docs/api/storefront/latest/objects/PaymentSettings)non-nullSettings related to payments.

Show fields[Anchor to primaryDomain](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.primaryDomain)primaryDomain•[Domain!](/docs/api/storefront/latest/objects/Domain)non-nullThe primary domain of the shop’s Online Store.

Show fields[Anchor to privacyPolicy](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.privacyPolicy)privacyPolicy•[ShopPolicy](/docs/api/storefront/latest/objects/ShopPolicy)The shop’s privacy policy.

Show fields[Anchor to refundPolicy](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.refundPolicy)refundPolicy•[ShopPolicy](/docs/api/storefront/latest/objects/ShopPolicy)The shop’s refund policy.

Show fields[Anchor to shippingPolicy](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.shippingPolicy)shippingPolicy•[ShopPolicy](/docs/api/storefront/latest/objects/ShopPolicy)The shop’s shipping policy.

Show fields[Anchor to shipsToCountries](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.shipsToCountries)shipsToCountries•[[CountryCode!]!](/docs/api/storefront/latest/enums/CountryCode)non-nullCountries that the shop ships to.

Show enum values[Anchor to shopPayInstallmentsPricing](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.shopPayInstallmentsPricing)shopPayInstallmentsPricing•[ShopPayInstallmentsPricing](/docs/api/storefront/latest/objects/ShopPayInstallmentsPricing) Token access requiredThe Shop Pay Installments pricing information for the shop.

Show fields[Anchor to socialLoginProviders](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.socialLoginProviders)socialLoginProviders•[[SocialLoginProvider!]!](/docs/api/storefront/latest/objects/SocialLoginProvider)non-nullThe social login providers for customer accounts.

Show fields[Anchor to subscriptionPolicy](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.subscriptionPolicy)subscriptionPolicy•[ShopPolicyWithDefault](/docs/api/storefront/latest/objects/ShopPolicyWithDefault)The shop’s subscription policy.

Show fields[Anchor to termsOfService](/docs/api/storefront/latest/objects/Shop#field-Shop.fields.termsOfService)termsOfService•[ShopPolicy](/docs/api/storefront/latest/objects/ShopPolicy)The shop’s terms of service.

Show fieldsWas this section helpful?YesNo## Map### Possible type in- [MetafieldParentResource](/docs/api/storefront/latest/unions/MetafieldParentResource)## [Anchor to Queries](/docs/api/storefront/latest/objects/Shop#queries)Queries- shop (Shop!)[Anchor to shop](/docs/api/storefront/latest/objects/Shop#query-shop)[shop](/docs/api/storefront/latest/queries/shop)•queryThe shop associated with the storefront access token.

Show fieldsWas this section helpful?YesNo## <?>Shop Queries### Queried by- <?>[shop](/docs/api/storefront/latest/queries/shop)## [Anchor to Interfaces](/docs/api/storefront/latest/objects/Shop#interfaces)Interfaces- HasMetafields- Node[Anchor to HasMetafields](/docs/api/storefront/latest/objects/Shop#interface-HasMetafields)[HasMetafields](/docs/api/storefront/latest/interfaces/HasMetafields)•interface[Anchor to Node](/docs/api/storefront/latest/objects/Shop#interface-Node)[Node](/docs/api/storefront/latest/interfaces/Node)•interfaceWas this section helpful?YesNo## ||-Shop Implements### Implements- ||-[HasMetafields](/docs/api/storefront/latest/interfaces/HasMetafields)- ||-[Node](/docs/api/storefront/latest/interfaces/Node)### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)