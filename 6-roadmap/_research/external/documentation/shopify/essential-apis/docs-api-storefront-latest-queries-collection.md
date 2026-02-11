---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront/latest/queries/collection",
    "fetched_at": "2026-02-10T13:41:26.785512",
    "status": 200,
    "size_bytes": 347727
  },
  "metadata": {
    "title": "collection - Storefront API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "queries",
    "component": "collection"
  }
}
---

# collection - Storefront API

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to collection](/docs/api/storefront/latest/queries/collection#top)# collectionqueryAsk assistantFetch a specific `Collection` by one of its unique attributes.

[Anchor to Arguments](/docs/api/storefront/latest/queries/collection#arguments)## Arguments- handle (String)- id (ID)[Anchor to handle](/docs/api/storefront/latest/queries/collection#arguments-handle)handle•[String](/docs/api/storefront/latest/scalars/String)The handle of the `Collection`.

[Anchor to id](/docs/api/storefront/latest/queries/collection#arguments-id)id•[ID](/docs/api/storefront/latest/scalars/ID)The ID of the `Collection`.

Was this section helpful?YesNo## [Anchor to Possible returns](/docs/api/storefront/latest/queries/collection#possible-returns)Possible returns- Collection (Collection)[Anchor to Collection](/docs/api/storefront/latest/queries/collection#returns-Collection)Collection•[Collection](/docs/api/storefront/latest/objects/Collection)A collection represents a grouping of products that a shop owner can create to

organize them or make their shops easier to browse.

Show fields[Anchor to description](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.description)description•[String!](/docs/api/storefront/latest/scalars/String)non-nullStripped description of the collection, single line with HTML tags removed.

Show arguments### Arguments[Anchor to truncateAt](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.description.arguments.truncateAt)truncateAt•[Int](/docs/api/storefront/latest/scalars/Int)Truncates a string after the given length.

[Anchor to descriptionHtml](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.descriptionHtml)descriptionHtml•[HTML!](/docs/api/storefront/latest/scalars/HTML)non-nullThe description of the collection, complete with HTML formatting.

[Anchor to handle](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.handle)handle•[String!](/docs/api/storefront/latest/scalars/String)non-nullA human-friendly unique string for the collection automatically generated from its title.

Limit of 255 characters.

[Anchor to id](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.id)id•[ID!](/docs/api/storefront/latest/scalars/ID)non-nullA globally-unique ID.

[Anchor to image](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.image)image•[Image](/docs/api/storefront/latest/objects/Image)Image associated with the collection.

Show fields[Anchor to metafield](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.metafield)metafield•[Metafield](/docs/api/storefront/latest/objects/Metafield) Token access requiredA [custom field](https://shopify.dev/docs/apps/build/custom-data), including its `namespace` and `key`, that's associated with a Shopify resource for the purposes of adding and storing additional information.

Show fields### Arguments[Anchor to namespace](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.metafield.arguments.namespace)namespace•[String](/docs/api/storefront/latest/scalars/String)The container the metafield belongs to. If omitted, the app-reserved namespace will be used.

[Anchor to key](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.metafield.arguments.key)key•[String!](/docs/api/storefront/latest/scalars/String)requiredThe identifier for the metafield.

[Anchor to metafields](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.metafields)metafields•[[Metafield]!](/docs/api/storefront/latest/objects/Metafield)non-null Token access requiredA list of [custom fields](/docs/apps/build/custom-data) that a merchant associates with a Shopify resource.

Show fields### Arguments[Anchor to identifiers](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.metafields.arguments.identifiers)identifiers•[[HasMetafieldsIdentifier!]!](/docs/api/storefront/latest/input-objects/HasMetafieldsIdentifier)requiredThe list of metafields to retrieve by namespace and key.

The input must not contain more than `250` values.

Show input fields[Anchor to onlineStoreUrl](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.onlineStoreUrl)onlineStoreUrl•[URL](/docs/api/storefront/latest/scalars/URL)The URL used for viewing the resource on the shop's Online Store. Returns `null` if the resource is currently not published to the Online Store sales channel.

[Anchor to products](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.products)products•[ProductConnection!](/docs/api/storefront/latest/connections/ProductConnection)non-nullList of products in the collection.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.products.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.products.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.products.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.products.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.products.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.products.arguments.sortKey)sortKey•[ProductCollectionSortKeys](/docs/api/storefront/latest/enums/ProductCollectionSortKeys)Default:COLLECTION_DEFAULTSort the underlying list by the given key.

Show enum values[Anchor to filters](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.products.arguments.filters)filters•[[ProductFilter!]](/docs/api/storefront/latest/input-objects/ProductFilter)Returns a subset of products matching all product filters.

The input must not contain more than `250` values.

Show input fields[Anchor to seo](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.seo)seo•[SEO!](/docs/api/storefront/latest/objects/SEO)non-nullThe collection's SEO information.

Show fields[Anchor to title](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.title)title•[String!](/docs/api/storefront/latest/scalars/String)non-nullThe collection’s name. Limit of 255 characters.

[Anchor to trackingParameters](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.trackingParameters)trackingParameters•[String](/docs/api/storefront/latest/scalars/String)URL parameters to be added to a page URL to track the origin of on-site search traffic for [analytics reporting](https://help.shopify.com/manual/reports-and-analytics/shopify-reports/report-types/default-reports/behaviour-reports). Returns a result when accessed through the [search](/docs/api/storefront/2026-01/queries/search) or [predictiveSearch](/docs/api/storefront/2026-01/queries/predictiveSearch) queries, otherwise returns null.

[Anchor to updatedAt](/docs/api/storefront/latest/queries/collection#returns-Collection.fields.updatedAt)updatedAt•[DateTime!](/docs/api/storefront/latest/scalars/DateTime)non-nullThe date and time when the collection was last modified.

Was this section helpful?YesNo## Examples- ### collection referenceHide content## Query Reference Copy912345›⌄⌄{  collection {    # collection fields  }}### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)