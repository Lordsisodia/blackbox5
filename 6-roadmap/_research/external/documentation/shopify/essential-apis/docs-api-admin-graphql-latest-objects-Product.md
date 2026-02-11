---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-graphql/latest/objects/Product",
    "fetched_at": "2026-02-10T13:40:54.739133",
    "status": 200,
    "size_bytes": 1141469
  },
  "metadata": {
    "title": "Product - GraphQL Admin",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "objects",
    "component": "Product"
  }
}
---

# Product - GraphQL Admin

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to Product](/docs/api/admin-graphql/latest/objects/Product#top)# ProductobjectAsk assistantRequires `read_products` access scope.

The `Product` object lets you manage products in a merchant’s store.

Products are the goods and services that merchants offer to customers. They can include various details such as title, description, price, images, and options such as size or color.

You can use [product variants](https://shopify.dev/docs/api/admin-graphql/latest/objects/productvariant) to create or update different versions of the same product.

You can also add or update product [media](https://shopify.dev/docs/api/admin-graphql/latest/interfaces/media).

Products can be organized by grouping them into a [collection](https://shopify.dev/docs/api/admin-graphql/latest/objects/collection).

Learn more about working with [Shopify's product model](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model/product-model-components),

including limitations and considerations.

## [Anchor to Fields](/docs/api/admin-graphql/latest/objects/Product#fields)Fields- availablePublicationsCount (Count)- bundleComponents (ProductBundleComponentConnection!)- bundleConsolidatedOptions ([ComponentizedProductsBundleConsolidatedOption!])- category (TaxonomyCategory)- collections (CollectionConnection!)- combinedListing (CombinedListing)- combinedListingRole (CombinedListingsRole)- compareAtPriceRange (ProductCompareAtPriceRange)- contextualPricing (ProductContextualPricing!)- createdAt (DateTime!)- defaultCursor (String!)- description (String!)- descriptionHtml (HTML!)- events (EventConnection!)- featuredMedia (Media)- feedback (ResourceFeedback)- giftCardTemplateSuffix (String)- handle (String!)- hasOnlyDefaultVariant (Boolean!)- hasOutOfStockVariants (Boolean!)- hasVariantsThatRequiresComponents (Boolean!)- id (ID!)- inCollection (Boolean!)- isGiftCard (Boolean!)- legacyResourceId (UnsignedInt64!)- media (MediaConnection!)- mediaCount (Count)- metafield (Metafield)- metafields (MetafieldConnection!)- onlineStorePreviewUrl (URL)- onlineStoreUrl (URL)- options ([ProductOption!]!)- priceRangeV2 (ProductPriceRangeV2!)- productComponents (ProductComponentTypeConnection!)- productComponentsCount (Count)- productParents (ProductConnection!)- productType (String!)- publishedAt (DateTime)- publishedInContext (Boolean!)- publishedOnCurrentPublication (Boolean!)- publishedOnPublication (Boolean!)- requiresSellingPlan (Boolean!)- resourcePublicationOnCurrentPublication (ResourcePublicationV2)- resourcePublications (ResourcePublicationConnection!)- resourcePublicationsCount (Count)- resourcePublicationsV2 (ResourcePublicationV2Connection!)- restrictedForResource (RestrictedForResource)- sellingPlanGroups (SellingPlanGroupConnection!)- sellingPlanGroupsCount (Count)- seo (SEO!)- status (ProductStatus!)- tags ([String!]!)- templateSuffix (String)- title (String!)- totalInventory (Int!)- tracksInventory (Boolean!)- translations ([Translation!]!)- unpublishedPublications (PublicationConnection!)- updatedAt (DateTime!)- variants (ProductVariantConnection!)- variantsCount (Count)- vendor (String!)[Anchor to availablePublicationsCount](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.availablePublicationsCount)availablePublicationsCount•[Count](/docs/api/admin-graphql/latest/objects/Count)The number of

[publications](https://shopify.dev/docs/api/admin-graphql/latest/objects/Publication)

that a resource is published to, without

[feedback errors](https://shopify.dev/docs/api/admin-graphql/latest/objects/ResourceFeedback).

Show fields[Anchor to bundleComponents](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.bundleComponents)bundleComponents•[ProductBundleComponentConnection!](/docs/api/admin-graphql/latest/connections/ProductBundleComponentConnection)non-nullA list of [components](https://shopify.dev/docs/apps/build/product-merchandising/bundles/add-product-fixed-bundle)

that are associated with a product in a bundle.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.bundleComponents.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.bundleComponents.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.bundleComponents.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.bundleComponents.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.bundleComponents.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to bundleConsolidatedOptions](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.bundleConsolidatedOptions)bundleConsolidatedOptions•[[ComponentizedProductsBundleConsolidatedOption!]](/docs/api/admin-graphql/latest/objects/ComponentizedProductsBundleConsolidatedOption)A list of consolidated options for a product in a bundle.

Show fields[Anchor to category](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.category)category•[TaxonomyCategory](/docs/api/admin-graphql/latest/objects/TaxonomyCategory)The category of a product

from [Shopify's Standard Product Taxonomy](https://shopify.github.io/product-taxonomy/releases/unstable/?categoryId=sg-4-17-2-17).

Show fields[Anchor to collections](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.collections)collections•[CollectionConnection!](/docs/api/admin-graphql/latest/connections/CollectionConnection)non-nullA list of [collections](https://shopify.dev/docs/api/admin-graphql/latest/objects/Collection)

that include the product.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.collections.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.collections.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.collections.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.collections.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.collections.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.collections.arguments.sortKey)sortKey•[CollectionSortKeys](/docs/api/admin-graphql/latest/enums/CollectionSortKeys)Default:IDSort the underlying list using a key. If your query is slow or returns an error, then [try specifying a sort key that matches the field used in the search](https://shopify.dev/api/usage/pagination-graphql#search-performance-considerations).

Show enum values[Anchor to query](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.collections.arguments.query)query•[String](/docs/api/admin-graphql/latest/scalars/String)A filter made up of terms, connectives, modifiers, and comparators.

You can apply one or more filters to a query. Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-default)default•stringFilter by a case-insensitive search of multiple fields in a document.

Example:- `query=Bob Norman`- `query=title:green hoodie`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-collection_type)collection_type•stringValid values:- `custom` - `smart` [Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-handle)handle•string[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-id)id•idFilter by `id` range.

Example:- `id:1234`- `id:>=1234`- `id:<=1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-product_id)product_id•idFilter by collections containing a product by its ID.

[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-product_publication_status)product_publication_status•stringFilter by channel approval process status of the resource on a channel, such as the online store. The value is a composite of the [channel `app` ID](https://shopify.dev/api/admin-graphql/latest/objects/Channel#field-Channel.fields.app) (`Channel.app.id`) and one of the valid values. For simple visibility checks, use [published_status](https://shopify.dev/api/admin-graphql/latest/queries/products#argument-query-filter-publishable_status) instead.

Valid values:- `* {channel_app_id}-approved` - `* {channel_app_id}-rejected` - `* {channel_app_id}-needs_action` - `* {channel_app_id}-awaiting_review` - `* {channel_app_id}-published` - `* {channel_app_id}-demoted` - `* {channel_app_id}-scheduled` - `* {channel_app_id}-provisionally_published` Example:- `product_publication_status:189769876-approved`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-publishable_status)publishable_status•string**Deprecated:** This parameter is deprecated as of 2025-12 and will be removed in a future API version. Use [published_status](https://shopify.dev/api/admin-graphql/latest/queries/products#argument-query-filter-publishable_status) for visibility checks. Filter by the publishable status of the resource on a channel. The value is a composite of the [channel `app` ID](https://shopify.dev/api/admin-graphql/latest/objects/Channel#app-price) (`Channel.app.id`) and one of the valid status values.

Valid values:- `* {channel_app_id}-unset` - `* {channel_app_id}-pending` - `* {channel_app_id}-approved` - `* {channel_app_id}-not_approved` Example:- `publishable_status:580111-unset`- `publishable_status:580111-pending`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-published_at)published_at•timeFilter by the date and time when the collection was published to the Online Store.

[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-published_status)published_status•stringFilter resources by their visibility and publication state on a channel. Online store channel filtering: - `online_store_channel`: Returns all resources in the online store channel, regardless of publication status. - `published`/`visible`: Returns resources that are published to the online store. - `unpublished`: Returns resources that are not published to the online store. Channel-specific filtering using the [channel `app` ID](https://shopify.dev/api/admin-graphql/latest/objects/Channel#app-price) (`Channel.app.id`) with suffixes: - `{channel_app_id}-published`: Returns resources published to the specified channel. - `{channel_app_id}-visible`: Same as `{channel_app_id}-published` (kept for backwards compatibility). - `{channel_app_id}-intended`: Returns resources added to the channel but not yet published. - `{channel_app_id}-hidden`: Returns resources not added to the channel or not published. Other: - `unavailable`: Returns resources not published to any channel.

Valid values:- `online_store_channel` - `published` - `visible` - `unpublished` - `* {channel_app_id}-published` - `* {channel_app_id}-visible` - `* {channel_app_id}-intended` - `* {channel_app_id}-hidden` - `unavailable` Example:- `published_status:online_store_channel`- `published_status:published`- `published_status:580111-published`- `published_status:580111-hidden`- `published_status:unavailable`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-title)title•string[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-updated_at)updated_at•time[Anchor to combinedListing](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.combinedListing)combinedListing•[CombinedListing](/docs/api/admin-graphql/latest/objects/CombinedListing)A special product type that combines separate products from a store into a single product listing.

[Combined listings](https://shopify.dev/apps/build/product-merchandising/combined-listings) are connected

by a shared option, such as color, model, or dimension.

Show fields[Anchor to combinedListingRole](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.combinedListingRole)combinedListingRole•[CombinedListingsRole](/docs/api/admin-graphql/latest/enums/CombinedListingsRole)The [role of the product](https://shopify.dev/docs/apps/build/product-merchandising/combined-listings/build-for-combined-listings)

in a combined listing.

If `null`, then the product isn't part of any combined listing.

Show enum values[Anchor to compareAtPriceRange](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.compareAtPriceRange)compareAtPriceRange•[ProductCompareAtPriceRange](/docs/api/admin-graphql/latest/objects/ProductCompareAtPriceRange)The [compare-at price range](https://help.shopify.com/manual/products/details/product-pricing/sale-pricing)

of the product in the shop's default currency.

Show fields[Anchor to contextualPricing](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.contextualPricing)contextualPricing•[ProductContextualPricing!](/docs/api/admin-graphql/latest/objects/ProductContextualPricing)non-nullThe pricing that applies to a customer in a specific context. For example, a price might vary depending on the customer's location. Only active markets are considered in the price resolution.

Show fields### Arguments[Anchor to context](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.contextualPricing.arguments.context)context•[ContextualPricingContext!](/docs/api/admin-graphql/latest/input-objects/ContextualPricingContext)requiredThe context used to generate contextual pricing for the variant.

Show input fields[Anchor to createdAt](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.createdAt)createdAt•[DateTime!](/docs/api/admin-graphql/latest/scalars/DateTime)non-nullThe date and time when the product was created.

[Anchor to defaultCursor](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.defaultCursor)defaultCursor•[String!](/docs/api/admin-graphql/latest/scalars/String)non-nullA default [cursor](https://shopify.dev/api/usage/pagination-graphql) that returns the single next record, sorted ascending by ID.

[Anchor to description](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.description)description•[String!](/docs/api/admin-graphql/latest/scalars/String)non-nullA single-line description of the product,

with [HTML tags](https://developer.mozilla.org/en-US/docs/Web/HTML) removed.

Show arguments### Arguments[Anchor to truncateAt](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.description.arguments.truncateAt)truncateAt•[Int](/docs/api/admin-graphql/latest/scalars/Int)Truncates a string after the given length.

[Anchor to descriptionHtml](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.descriptionHtml)descriptionHtml•[HTML!](/docs/api/admin-graphql/latest/scalars/HTML)non-nullThe description of the product, with

HTML tags. For example, the description might include

bold `<strong></strong>` and italic `<i></i>` text.

[Anchor to events](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.events)events•[EventConnection!](/docs/api/admin-graphql/latest/connections/EventConnection)non-nullThe paginated list of events associated with the host subject.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.events.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.events.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.events.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.events.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.events.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.events.arguments.sortKey)sortKey•[EventSortKeys](/docs/api/admin-graphql/latest/enums/EventSortKeys)Default:IDSort the underlying list using a key. If your query is slow or returns an error, then [try specifying a sort key that matches the field used in the search](https://shopify.dev/api/usage/pagination-graphql#search-performance-considerations).

Show enum values[Anchor to query](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.events.arguments.query)query•[String](/docs/api/admin-graphql/latest/scalars/String)A filter made up of terms, connectives, modifiers, and comparators.

You can apply one or more filters to a query. Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-action)action•stringThe action that occured.

Example:- `action:create`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-comments)comments•booleanWhether or not to include [comment-events](https://shopify.dev/api/admin-graphql/latest/objects/CommentEvent) in your search, passing `false` will exclude comment-events, any other value will include comment-events.

Example:- `false`- `true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-created_at)created_at•timeFilter by the date and time when the event occurred. Event data is retained for 1 year.

Example:- `created_at:>2025-10-21`- `created_at:<now`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-id)id•idFilter by `id` range.

Example:- `id:1234`- `id:>=1234`- `id:<=1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-subject_type)subject_type•stringThe resource type affected by this event. See [EventSubjectType](https://shopify.dev/api/admin-graphql/latest/enums/EventSubjectType) for possible values.

Example:- `PRODUCT_VARIANT`- `PRODUCT`- `COLLECTION`[Anchor to featuredMedia](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.featuredMedia)featuredMedia•[Media](/docs/api/admin-graphql/latest/interfaces/Media)The featured [media](https://shopify.dev/docs/apps/build/online-store/product-media)

associated with the product.

Show fields[Anchor to feedback](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.feedback)feedback•[ResourceFeedback](/docs/api/admin-graphql/latest/objects/ResourceFeedback)The information that lets merchants know what steps they need to take

to make sure that the app is set up correctly.

For example, if a merchant hasn't set up a product correctly in the app,

then the feedback might include a message that says "You need to add a price

to this product".

Show fields[Anchor to giftCardTemplateSuffix](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.giftCardTemplateSuffix)giftCardTemplateSuffix•[String](/docs/api/admin-graphql/latest/scalars/String)The [theme template](https://shopify.dev/docs/storefronts/themes/architecture/templates) that's used when customers view the gift card in a store.

[Anchor to handle](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.handle)handle•[String!](/docs/api/admin-graphql/latest/scalars/String)non-nullA unique, human-readable string of the product's title. A handle can contain letters, hyphens (`-`), and numbers, but no spaces.

The handle is used in the online store URL for the product.

[Anchor to hasOnlyDefaultVariant](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.hasOnlyDefaultVariant)hasOnlyDefaultVariant•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the product has only a single variant with the default option and value.

[Anchor to hasOutOfStockVariants](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.hasOutOfStockVariants)hasOutOfStockVariants•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the product has variants that are out of stock.

[Anchor to hasVariantsThatRequiresComponents](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.hasVariantsThatRequiresComponents)hasVariantsThatRequiresComponents•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether at least one of the product variants requires

[bundle components](https://shopify.dev/docs/apps/build/product-merchandising/bundles/add-product-fixed-bundle).

Learn more about

[store eligibility for bundles](https://shopify.dev/docs/apps/build/product-merchandising/bundles#store-eligibility).

[Anchor to id](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.id)id•[ID!](/docs/api/admin-graphql/latest/scalars/ID)non-nullA globally-unique ID.

[Anchor to inCollection](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.inCollection)inCollection•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the product

is in a specified

[collection](https://shopify.dev/docs/api/admin-graphql/latest/objects/collection).

Show arguments### Arguments[Anchor to id](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.inCollection.arguments.id)id•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the collection to check. For example, `id: "gid://shopify/Collection/123"`.

[Anchor to isGiftCard](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.isGiftCard)isGiftCard•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the product is a gift card.

[Anchor to legacyResourceId](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.legacyResourceId)legacyResourceId•[UnsignedInt64!](/docs/api/admin-graphql/latest/scalars/UnsignedInt64)non-nullThe ID of the corresponding resource in the REST Admin API.

[Anchor to media](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.media)media•[MediaConnection!](/docs/api/admin-graphql/latest/connections/MediaConnection)non-nullThe [media](https://shopify.dev/docs/apps/build/online-store/product-media) associated with the product. Valid media are images, 3D models, videos.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.media.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.media.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.media.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.media.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.media.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.media.arguments.sortKey)sortKey•[ProductMediaSortKeys](/docs/api/admin-graphql/latest/enums/ProductMediaSortKeys)Default:POSITIONSort the underlying list using a key. If your query is slow or returns an error, then [try specifying a sort key that matches the field used in the search](https://shopify.dev/api/usage/pagination-graphql#search-performance-considerations).

Show enum values[Anchor to query](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.media.arguments.query)query•[String](/docs/api/admin-graphql/latest/scalars/String)A filter made up of terms, connectives, modifiers, and comparators.

You can apply one or more filters to a query. Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-id)id•idFilter by `id` range.

Example:- `id:1234`- `id:>=1234`- `id:<=1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-media_type)media_type•stringValid values:- `IMAGE` - `VIDEO` - `MODEL_3D` - `EXTERNAL_VIDEO` [Anchor to mediaCount](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.mediaCount)mediaCount•[Count](/docs/api/admin-graphql/latest/objects/Count)The total count of [media](https://shopify.dev/docs/apps/build/online-store/product-media)

that's associated with a product.

Show fields[Anchor to metafield](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafield)metafield•[Metafield](/docs/api/admin-graphql/latest/objects/Metafield)A [custom field](https://shopify.dev/docs/apps/build/custom-data),

including its `namespace` and `key`, that's associated with a Shopify resource

for the purposes of adding and storing additional information.

Show fields### Arguments[Anchor to namespace](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafield.arguments.namespace)namespace•[String](/docs/api/admin-graphql/latest/scalars/String)The container the metafield belongs to. If omitted, the app-reserved namespace will be used.

[Anchor to key](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafield.arguments.key)key•[String!](/docs/api/admin-graphql/latest/scalars/String)requiredThe key for the metafield.

[Anchor to metafields](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafields)metafields•[MetafieldConnection!](/docs/api/admin-graphql/latest/connections/MetafieldConnection)non-nullA list of [custom fields](https://shopify.dev/docs/apps/build/custom-data)

that a merchant associates with a Shopify resource.

Show fields### Arguments[Anchor to namespace](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafields.arguments.namespace)namespace•[String](/docs/api/admin-graphql/latest/scalars/String)The metafield namespace to filter by. If omitted, all metafields are returned.

[Anchor to keys](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafields.arguments.keys)keys•[[String!]](/docs/api/admin-graphql/latest/scalars/String)List of keys of metafields in the format `namespace.key`, will be returned in the same format.

[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafields.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafields.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafields.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafields.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafields.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to onlineStorePreviewUrl](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.onlineStorePreviewUrl)onlineStorePreviewUrl•[URL](/docs/api/admin-graphql/latest/scalars/URL)The [preview URL](https://help.shopify.com/manual/online-store/setting-up#preview-your-store) for the online store.

[Anchor to onlineStoreUrl](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.onlineStoreUrl)onlineStoreUrl•[URL](/docs/api/admin-graphql/latest/scalars/URL)The product's URL on the online store.

If `null`, then the product isn't published to the online store sales channel.

[Anchor to options](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.options)options•[[ProductOption!]!](/docs/api/admin-graphql/latest/objects/ProductOption)non-nullA list of product options. The limit is defined by the

[shop's resource limits for product options](https://shopify.dev/docs/api/admin-graphql/latest/objects/Shop#field-resourcelimits) (`Shop.resourceLimits.maxProductOptions`).

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.options.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)Truncate the array result to this size.

[Anchor to priceRangeV2](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.priceRangeV2)priceRangeV2•[ProductPriceRangeV2!](/docs/api/admin-graphql/latest/objects/ProductPriceRangeV2)non-nullThe minimum and maximum prices of a product, expressed in decimal numbers.

For example, if the product is priced between $10.00 and $50.00,

then the price range is $10.00 - $50.00.

Show fields[Anchor to productComponents](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productComponents)productComponents•[ProductComponentTypeConnection!](/docs/api/admin-graphql/latest/connections/ProductComponentTypeConnection)non-nullA list of products that contain at least one variant associated with

at least one of the current products' variants via group relationship.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productComponents.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productComponents.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productComponents.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productComponents.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productComponents.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to productComponentsCount](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productComponentsCount)productComponentsCount•[Count](/docs/api/admin-graphql/latest/objects/Count)A count of unique products that contain at least one variant associated with

at least one of the current products' variants via group relationship.

Show fields[Anchor to productParents](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productParents)productParents•[ProductConnection!](/docs/api/admin-graphql/latest/connections/ProductConnection)non-nullA list of products that has a variant that contains any of this product's variants as a component.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productParents.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productParents.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productParents.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productParents.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productParents.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to query](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productParents.arguments.query)query•[String](/docs/api/admin-graphql/latest/scalars/String)A filter made up of terms, connectives, modifiers, and comparators.

You can apply one or more filters to a query. Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-default)default•stringFilter by a case-insensitive search of multiple fields in a document.

Example:- `query=Bob Norman`- `query=title:green hoodie`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-barcode)barcode•stringFilter by the product variant [`barcode`](https://shopify.dev/api/admin-graphql/latest/objects/ProductVariant#field-barcode) field.

Example:- `barcode:ABC-abc-1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-bundles)bundles•booleanFilter by a [product bundle](https://shopify.dev/docs/apps/build/product-merchandising/bundles). A product bundle is a set of two or more related products, which are commonly offered at a discount.

Example:- `bundles:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-category_id)category_id•stringFilter by the product [category ID](https://shopify.dev/api/admin-graphql/latest/objects/Product#field-category) (`product.category.id`). A product category is the category of a product from [Shopify's Standard Product Taxonomy](https://shopify.github.io/product-taxonomy/releases/unstable/?categoryId=sg-4-17-2-17).

Example:- `category_id:sg-4-17-2-17`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-collection_id)collection_id•idFilter by the collection [`id`](https://shopify.dev/api/admin-graphql/latest/objects/Collection#field-id) field.

Example:- `collection_id:108179161409`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-combined_listing_role)combined_listing_role•stringFilter by the role of the product in a [combined listing](https://shopify.dev/apps/build/product-merchandising/combined-listings).

Valid values:- `parent` - `child` - `no_role` Example:- `combined_listing_role:parent`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-created_at)created_at•timeFilter by the date and time when the product was created.

Example:- `created_at:>'2020-10-21T23:39:20Z'`- `created_at:<now`- `created_at:<='2024'`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-delivery_profile_id)delivery_profile_id•idFilter by the delivery profile [`id`](https://shopify.dev/api/admin-graphql/latest/objects/DeliveryProfile#field-id) field.

Example:- `delivery_profile_id:108179161409`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-error_feedback)error_feedback•stringFilter by products with publishing errors.

[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-gift_card)gift_card•booleanFilter by the product [`isGiftCard`](https://shopify.dev/api/admin-graphql/latest/objects/Product#field-isgiftcard) field.

Example:- `gift_card:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-handle)handle•stringFilter by a comma-separated list of product [handles](https://shopify.dev/api/admin-graphql/latest/queries/products#argument-query-filter-handle).

Example:- `handle:the-minimal-snowboard`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-has_only_composites)has_only_composites•booleanFilter by products that have only composite variants.

Example:- `has_only_composites:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-has_only_default_variant)has_only_default_variant•booleanFilter by products that have only a default variant. A default variant is the only variant if no other variants are specified.

Example:- `has_only_default_variant:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-has_variant_with_components)has_variant_with_components•booleanFilter by products that have variants with associated components.

Example:- `has_variant_with_components:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-id)id•idFilter by `id` range.

Example:- `id:1234`- `id:>=1234`- `id:<=1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-inventory_total)inventory_total•integerFilter by inventory count.

Example:- `inventory_total:0`- `inventory_total:>150`- `inventory_total:>=200`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-is_price_reduced)is_price_reduced•booleanFilter by products that have a reduced price. For more information, refer to the [`CollectionRule`](https://shopify.dev/api/admin-graphql/latest/objects/CollectionRule) object.

Example:- `is_price_reduced:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-metafields.{namespace}.{key})metafields.{namespace}.{key}•mixedFilters resources by metafield value. Format: `metafields.{namespace}.{key}:{value}`. Learn more about [querying by metafield value](https://shopify.dev/apps/build/custom-data/metafields/query-by-metafield-value).

Example:- `metafields.custom.on_sale:true`- `metafields.product.material:"gid://shopify/Metaobject/43458085"`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-out_of_stock_somewhere)out_of_stock_somewhere•booleanFilter by products that are out of stock in at least one location.

Example:- `out_of_stock_somewhere:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-price)price•bigdecimalFilter by the product variant [`price`](https://shopify.dev/api/admin-graphql/latest/objects/Productvariant#field-price) field.

Example:- `price:100.57`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-product_configuration_owner)product_configuration_owner•stringFilter by the app [`id`](https://shopify.dev/api/admin-graphql/latest/objects/App#field-id) field.

Example:- `product_configuration_owner:10001`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-product_publication_status)product_publication_status•stringFilter by channel approval process status of the resource on a channel, such as the online store. The value is a composite of the [channel `app` ID](https://shopify.dev/api/admin-graphql/latest/objects/Channel#field-Channel.fields.app) (`Channel.app.id`) and one of the valid values. For simple visibility checks, use [published_status](https://shopify.dev/api/admin-graphql/latest/queries/products#argument-query-filter-publishable_status) instead.

Valid values:- `* {channel_app_id}-approved` - `* {channel_app_id}-rejected` - `* {channel_app_id}-needs_action` - `* {channel_app_id}-awaiting_review` - `* {channel_app_id}-published` - `* {channel_app_id}-demoted` - `* {channel_app_id}-scheduled` - `* {channel_app_id}-provisionally_published` Example:- `product_publication_status:189769876-approved`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-product_type)product_type•stringFilter by a comma-separated list of [product types](https://help.shopify.com/manual/products/details/product-type).

Example:- `product_type:snowboard`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-publication_ids)publication_ids•stringFilter by a comma-separated list of publication IDs that are associated with the product.

Example:- `publication_ids:184111530305,184111694145`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-publishable_status)publishable_status•string**Deprecated:** This parameter is deprecated as of 2025-12 and will be removed in a future API version. Use [published_status](https://shopify.dev/api/admin-graphql/latest/queries/products#argument-query-filter-publishable_status) for visibility checks. Filter by the publishable status of the resource on a channel. The value is a composite of the [channel `app` ID](https://shopify.dev/api/admin-graphql/latest/objects/Channel#app-price) (`Channel.app.id`) and one of the valid status values.

Valid values:- `* {channel_app_id}-unset` - `* {channel_app_id}-pending` - `* {channel_app_id}-approved` - `* {channel_app_id}-not_approved` Example:- `publishable_status:580111-unset`- `publishable_status:580111-pending`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-published_at)published_at•timeFilter by the date and time when the product was published to the online store and other sales channels.

Example:- `published_at:>2020-10-21T23:39:20Z`- `published_at:<now`- `published_at:<=2024`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-published_status)published_status•stringFilter resources by their visibility and publication state on a channel. Online store channel filtering: - `online_store_channel`: Returns all resources in the online store channel, regardless of publication status. - `published`/`visible`: Returns resources that are published to the online store. - `unpublished`: Returns resources that are not published to the online store. Channel-specific filtering using the [channel `app` ID](https://shopify.dev/api/admin-graphql/latest/objects/Channel#app-price) (`Channel.app.id`) with suffixes: - `{channel_app_id}-published`: Returns resources published to the specified channel. - `{channel_app_id}-visible`: Same as `{channel_app_id}-published` (kept for backwards compatibility). - `{channel_app_id}-intended`: Returns resources added to the channel but not yet published. - `{channel_app_id}-hidden`: Returns resources not added to the channel or not published. Other: - `unavailable`: Returns resources not published to any channel.

Valid values:- `online_store_channel` - `published` - `visible` - `unpublished` - `* {channel_app_id}-published` - `* {channel_app_id}-visible` - `* {channel_app_id}-intended` - `* {channel_app_id}-hidden` - `unavailable` Example:- `published_status:online_store_channel`- `published_status:published`- `published_status:580111-published`- `published_status:580111-hidden`- `published_status:unavailable`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-sku)sku•stringFilter by the product variant [`sku`](https://shopify.dev/api/admin-graphql/latest/objects/ProductVariant#field-sku) field. [Learn more about SKUs](https://help.shopify.com/manual/products/details/sku).

Example:- `sku:XYZ-12345`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-status)status•stringFilter by a comma-separated list of statuses. You can use statuses to manage inventory. Shopify only displays products with an `ACTIVE` status in online stores, sales channels, and apps.

Valid values:- `active` Default- `archived` - `draft` Example:- `status:active,draft`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-tag)tag•stringFilter objects by the `tag` field.

Example:- `tag:my_tag`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-tag_not)tag_not•stringFilter by objects that don’t have the specified tag.

Example:- `tag_not:my_tag`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-title)title•stringFilter by the product [`title`](https://shopify.dev/api/admin-graphql/latest/objects/Product#field-title) field.

Example:- `title:The Minimal Snowboard`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-updated_at)updated_at•timeFilter by the date and time when the product was last updated.

Example:- `updated_at:>'2020-10-21T23:39:20Z'`- `updated_at:<now`- `updated_at:<='2024'`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-variant_id)variant_id•idFilter by the product variant [`id`](https://shopify.dev/api/admin-graphql/latest/objects/ProductVariant#field-id) field.

Example:- `variant_id:45779434701121`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-variant_title)variant_title•stringFilter by the product variant [`title`](https://shopify.dev/api/admin-graphql/latest/objects/ProductVariant#field-title) field.

Example:- `variant_title:'Special ski wax'`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-vendor)vendor•stringFilter by the origin or source of the product. Learn more about [vendors and managing vendor information](https://help.shopify.com/manual/products/managing-vendor-info).

Example:- `vendor:Snowdevil`- `vendor:Snowdevil OR vendor:Icedevil`[Anchor to productType](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productType)productType•[String!](/docs/api/admin-graphql/latest/scalars/String)non-nullThe [product type](https://help.shopify.com/manual/products/details/product-type)

that merchants define.

[Anchor to publishedAt](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publishedAt)publishedAt•[DateTime](/docs/api/admin-graphql/latest/scalars/DateTime)The date and time when the product was published to the online store.

[Anchor to publishedInContext](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publishedInContext)publishedInContext•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the product is published for a customer only in a specified context. For example, a product might be published for a customer only in a specific location.

Show arguments### Arguments[Anchor to context](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publishedInContext.arguments.context)context•[ContextualPublicationContext!](/docs/api/admin-graphql/latest/input-objects/ContextualPublicationContext)requiredThe context used to determine publication status.

Show input fields[Anchor to publishedOnCurrentPublication](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publishedOnCurrentPublication)publishedOnCurrentPublication•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the resource is published to the app's

[publication](https://shopify.dev/docs/api/admin-graphql/latest/objects/Publication).

For example, the resource might be published to the app's online store channel.

[Anchor to publishedOnPublication](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publishedOnPublication)publishedOnPublication•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the resource is published to a specified

[publication](https://shopify.dev/docs/api/admin-graphql/latest/objects/Publication).

Show arguments### Arguments[Anchor to publicationId](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publishedOnPublication.arguments.publicationId)publicationId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the publication to check. For example, `id: "gid://shopify/Publication/123"`.

[Anchor to requiresSellingPlan](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.requiresSellingPlan)requiresSellingPlan•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether the product can only be purchased with

a [selling plan](https://shopify.dev/docs/apps/build/purchase-options/subscriptions/selling-plans).

Products that are sold on subscription (`requiresSellingPlan: true`) can be updated only for online stores.

If you update a product to be subscription-only (`requiresSellingPlan:false`), then the product is unpublished from all channels, except the online store.

[Anchor to resourcePublicationOnCurrentPublication](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublicationOnCurrentPublication)resourcePublicationOnCurrentPublication•[ResourcePublicationV2](/docs/api/admin-graphql/latest/objects/ResourcePublicationV2)The resource that's either published or staged to be published to

the [publication](https://shopify.dev/docs/api/admin-graphql/latest/objects/Publication).

Show fields[Anchor to resourcePublications](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublications)resourcePublications•[ResourcePublicationConnection!](/docs/api/admin-graphql/latest/connections/ResourcePublicationConnection)non-nullThe list of resources that are published to a

[publication](https://shopify.dev/docs/api/admin-graphql/latest/objects/Publication).

Show fields### Arguments[Anchor to onlyPublished](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublications.arguments.onlyPublished)onlyPublished•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:trueWhether to return only the resources that are currently published. If false, then also returns the resources that are scheduled to be published.

[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublications.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublications.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublications.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublications.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublications.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to resourcePublicationsCount](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublicationsCount)resourcePublicationsCount•[Count](/docs/api/admin-graphql/latest/objects/Count)The number of

[publications](https://shopify.dev/docs/api/admin-graphql/latest/objects/Publication)

that a resource is published to, without

[feedback errors](https://shopify.dev/docs/api/admin-graphql/latest/objects/ResourceFeedback).

Show fields### Arguments[Anchor to onlyPublished](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublicationsCount.arguments.onlyPublished)onlyPublished•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:trueInclude only the resource's publications that are published. If false, then return all the resource's publications including future publications.

[Anchor to resourcePublicationsV2](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublicationsV2)resourcePublicationsV2•[ResourcePublicationV2Connection!](/docs/api/admin-graphql/latest/connections/ResourcePublicationV2Connection)non-nullThe list of resources that are either published or staged to be published to a

[publication](https://shopify.dev/docs/api/admin-graphql/latest/objects/Publication).

Show fields### Arguments[Anchor to onlyPublished](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublicationsV2.arguments.onlyPublished)onlyPublished•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:trueWhether to return only the resources that are currently published. If false, then also returns the resources that are scheduled or staged to be published.

[Anchor to catalogType](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublicationsV2.arguments.catalogType)catalogType•[CatalogType](/docs/api/admin-graphql/latest/enums/CatalogType)Filter publications by catalog type.

Show enum values[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublicationsV2.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublicationsV2.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublicationsV2.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublicationsV2.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.resourcePublicationsV2.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to restrictedForResource](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.restrictedForResource)restrictedForResource•[RestrictedForResource](/docs/api/admin-graphql/latest/objects/RestrictedForResource)Whether the merchant can make changes to the product when they

[edit the order](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps/edit-orders)

associated with the product. For example, a merchant might be restricted from changing product details when they

edit an order.

Show fields### Arguments[Anchor to calculatedOrderId](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.restrictedForResource.arguments.calculatedOrderId)calculatedOrderId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe resource Id of the order with edits applied but not saved.

[Anchor to sellingPlanGroups](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.sellingPlanGroups)sellingPlanGroups•[SellingPlanGroupConnection!](/docs/api/admin-graphql/latest/connections/SellingPlanGroupConnection)non-nullA list of all [selling plan groups](https://shopify.dev/docs/apps/build/purchase-options/subscriptions/selling-plans/build-a-selling-plan)

that are associated with the product either directly, or through the product's variants.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.sellingPlanGroups.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.sellingPlanGroups.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.sellingPlanGroups.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.sellingPlanGroups.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.sellingPlanGroups.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sellingPlanGroupsCount](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.sellingPlanGroupsCount)sellingPlanGroupsCount•[Count](/docs/api/admin-graphql/latest/objects/Count)A count of [selling plan groups](https://shopify.dev/docs/apps/build/purchase-options/subscriptions/selling-plans/build-a-selling-plan)

that are associated with the product.

Show fields[Anchor to seo](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.seo)seo•[SEO!](/docs/api/admin-graphql/latest/objects/SEO)non-nullThe [SEO title and description](https://help.shopify.com/manual/promoting-marketing/seo/adding-keywords)

that are associated with a product.

Show fields[Anchor to status](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.status)status•[ProductStatus!](/docs/api/admin-graphql/latest/enums/ProductStatus)non-nullThe [product status](https://help.shopify.com/manual/products/details/product-details-page#product-status),

which controls visibility across all sales channels.

Show enum values[Anchor to tags](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.tags)tags•[[String!]!](/docs/api/admin-graphql/latest/scalars/String)non-nullA comma-separated list of searchable keywords that are

associated with the product. For example, a merchant might apply the `sports`

and `summer` tags to products that are associated with sportwear for summer.

Updating `tags` overwrites

any existing tags that were previously added to the product. To add new tags without overwriting

existing tags, use the [`tagsAdd`](https://shopify.dev/api/admin-graphql/latest/mutations/tagsadd)

mutation.

[Anchor to templateSuffix](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.templateSuffix)templateSuffix•[String](/docs/api/admin-graphql/latest/scalars/String)The [theme template](https://shopify.dev/docs/storefronts/themes/architecture/templates) that's used when customers view the product in a store.

[Anchor to title](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.title)title•[String!](/docs/api/admin-graphql/latest/scalars/String)non-nullThe name for the product that displays to customers. The title is used to construct the product's handle.

For example, if a product is titled "Black Sunglasses", then the handle is `black-sunglasses`.

[Anchor to totalInventory](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.totalInventory)totalInventory•[Int!](/docs/api/admin-graphql/latest/scalars/Int)non-nullThe quantity of inventory that's in stock.

[Anchor to tracksInventory](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.tracksInventory)tracksInventory•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullWhether [inventory tracking](https://help.shopify.com/manual/products/inventory/getting-started-with-inventory/set-up-inventory-tracking)

has been enabled for the product.

[Anchor to translations](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.translations)translations•[[Translation!]!](/docs/api/admin-graphql/latest/objects/Translation)non-nullThe published translations associated with the resource.

Show fields### Arguments[Anchor to locale](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.translations.arguments.locale)locale•[String!](/docs/api/admin-graphql/latest/scalars/String)requiredFilters translations locale.

[Anchor to marketId](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.translations.arguments.marketId)marketId•[ID](/docs/api/admin-graphql/latest/scalars/ID)Filters translations by market ID. Use this argument to retrieve content specific to a market.

[Anchor to unpublishedPublications](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.unpublishedPublications)unpublishedPublications•[PublicationConnection!](/docs/api/admin-graphql/latest/connections/PublicationConnection)non-nullThe list of [publications](https://shopify.dev/docs/api/admin-graphql/latest/objects/Publication)

that the resource isn't published to.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.unpublishedPublications.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.unpublishedPublications.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.unpublishedPublications.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.unpublishedPublications.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.unpublishedPublications.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to updatedAt](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.updatedAt)updatedAt•[DateTime!](/docs/api/admin-graphql/latest/scalars/DateTime)non-nullThe date and time when the product was last modified.

A product's `updatedAt` value can change for different reasons. For example, if an order

is placed for a product that has inventory tracking set up, then the inventory adjustment

is counted as an update.

[Anchor to variants](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.variants)variants•[ProductVariantConnection!](/docs/api/admin-graphql/latest/connections/ProductVariantConnection)non-nullA list of [variants](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant) associated with the product.

If querying a single product at the root, you can fetch up to 2048 variants.

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.variants.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.variants.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.variants.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.variants.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.variants.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.variants.arguments.sortKey)sortKey•[ProductVariantSortKeys](/docs/api/admin-graphql/latest/enums/ProductVariantSortKeys)Default:POSITIONSort the underlying list using a key. If your query is slow or returns an error, then [try specifying a sort key that matches the field used in the search](https://shopify.dev/api/usage/pagination-graphql#search-performance-considerations).

Show enum values[Anchor to variantsCount](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.variantsCount)variantsCount•[Count](/docs/api/admin-graphql/latest/objects/Count)The number of [variants](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant)

that are associated with the product.

Show fields[Anchor to vendor](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.vendor)vendor•[String!](/docs/api/admin-graphql/latest/scalars/String)non-nullThe name of the product's vendor.

### Deprecated fields- bodyHtml (String): deprecated- customProductType (String): deprecated- descriptionPlainSummary (String!): deprecated- featuredImage (Image): deprecated- images (ImageConnection!): deprecated- metafieldDefinitions (MetafieldDefinitionConnection!): deprecated- priceRange (ProductPriceRange!): deprecated- productCategory (ProductCategory): deprecated- productPublications (ProductPublicationConnection!): deprecated- publicationCount (Int!): deprecated- publications (ProductPublicationConnection!): deprecated- publishedOnChannel (Boolean!): deprecated- publishedOnCurrentChannel (Boolean!): deprecated- sellingPlanGroupCount (Int!): deprecated- standardizedProductType (StandardizedProductType): deprecated- storefrontId (StorefrontID!): deprecated- totalVariants (Int!): deprecated- unpublishedChannels (ChannelConnection!): deprecated[Anchor to bodyHtml](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.bodyHtml)bodyHtml•[String](/docs/api/admin-graphql/latest/scalars/String)Deprecated[Anchor to customProductType](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.customProductType)customProductType•[String](/docs/api/admin-graphql/latest/scalars/String)Deprecated[Anchor to descriptionPlainSummary](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.descriptionPlainSummary)descriptionPlainSummary•[String!](/docs/api/admin-graphql/latest/scalars/String)non-nullDeprecated[Anchor to featuredImage](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.featuredImage)featuredImage•[Image](/docs/api/admin-graphql/latest/objects/Image)DeprecatedShow fields[Anchor to images](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.images)images•[ImageConnection!](/docs/api/admin-graphql/latest/connections/ImageConnection)non-nullDeprecatedShow fields### Arguments[Anchor to maxWidth](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.images.arguments.maxWidth)maxWidth•[Int](/docs/api/admin-graphql/latest/scalars/Int)Deprecated[Anchor to maxHeight](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.images.arguments.maxHeight)maxHeight•[Int](/docs/api/admin-graphql/latest/scalars/Int)Deprecated[Anchor to crop](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.images.arguments.crop)crop•[CropRegion](/docs/api/admin-graphql/latest/enums/CropRegion)DeprecatedShow enum values[Anchor to scale](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.images.arguments.scale)scale•[Int](/docs/api/admin-graphql/latest/scalars/Int)DeprecatedDefault:1[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.images.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.images.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.images.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.images.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.images.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.images.arguments.sortKey)sortKey•[ProductImageSortKeys](/docs/api/admin-graphql/latest/enums/ProductImageSortKeys)Default:POSITIONSort the underlying list using a key. If your query is slow or returns an error, then [try specifying a sort key that matches the field used in the search](https://shopify.dev/api/usage/pagination-graphql#search-performance-considerations).

Show enum values[Anchor to metafieldDefinitions](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafieldDefinitions)metafieldDefinitions•[MetafieldDefinitionConnection!](/docs/api/admin-graphql/latest/connections/MetafieldDefinitionConnection)non-nullDeprecatedShow fields### Arguments[Anchor to namespace](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafieldDefinitions.arguments.namespace)namespace•[String](/docs/api/admin-graphql/latest/scalars/String)Filter metafield definitions by namespace.

[Anchor to pinnedStatus](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafieldDefinitions.arguments.pinnedStatus)pinnedStatus•[MetafieldDefinitionPinnedStatus](/docs/api/admin-graphql/latest/enums/MetafieldDefinitionPinnedStatus)Default:ANYFilter by the definition's pinned status.

Show enum values[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafieldDefinitions.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafieldDefinitions.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafieldDefinitions.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafieldDefinitions.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafieldDefinitions.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafieldDefinitions.arguments.sortKey)sortKey•[MetafieldDefinitionSortKeys](/docs/api/admin-graphql/latest/enums/MetafieldDefinitionSortKeys)Default:IDSort the underlying list using a key. If your query is slow or returns an error, then [try specifying a sort key that matches the field used in the search](https://shopify.dev/api/usage/pagination-graphql#search-performance-considerations).

Show enum values[Anchor to query](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.metafieldDefinitions.arguments.query)query•[String](/docs/api/admin-graphql/latest/scalars/String)A filter made up of terms, connectives, modifiers, and comparators.

You can apply one or more filters to a query. Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-default)default•stringFilter by a case-insensitive search of multiple fields in a document.

Example:- `query=Bob Norman`- `query=title:green hoodie`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-created_at)created_at•timeFilter by the date and time when the metafield definition was created.

Example:- `created_at:>2020-10-21T23:39:20Z`- `created_at:<now`- `created_at:<=2024`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-id)id•idFilter by `id` range.

Example:- `id:1234`- `id:>=1234`- `id:<=1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-key)key•stringFilter by the metafield definition [`key`](https://shopify.dev/docs/api/admin-graphql/latest/objects/MetafieldDefinition#field-key) field.

Example:- `key:some-key`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-namespace)namespace•stringFilter by the metafield definition [`namespace`](https://shopify.dev/docs/api/admin-graphql/latest/objects/MetafieldDefinition#field-namespace) field.

Example:- `namespace:some-namespace`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-owner_type)owner_type•stringFilter by the metafield definition [`ownerType`](https://shopify.dev/docs/api/admin-graphql/latest/objects/MetafieldDefinition#field-ownertype) field.

Example:- `owner_type:PRODUCT`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-type)type•stringFilter by the metafield definition [`type`](https://shopify.dev/docs/api/admin-graphql/latest/objects/MetafieldDefinition#field-type) field.

Example:- `type:single_line_text_field`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-updated_at)updated_at•timeFilter by the date and time when the metafield definition was last updated.

Example:- `updated_at:>2020-10-21T23:39:20Z`- `updated_at:<now`- `updated_at:<=2024`[Anchor to priceRange](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.priceRange)priceRange•[ProductPriceRange!](/docs/api/admin-graphql/latest/objects/ProductPriceRange)non-nullDeprecatedShow fields[Anchor to productCategory](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productCategory)productCategory•[ProductCategory](/docs/api/admin-graphql/latest/objects/ProductCategory)DeprecatedShow fields[Anchor to productPublications](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productPublications)productPublications•[ProductPublicationConnection!](/docs/api/admin-graphql/latest/connections/ProductPublicationConnection)non-nullDeprecatedShow fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productPublications.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productPublications.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productPublications.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productPublications.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productPublications.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to publicationCount](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publicationCount)publicationCount•[Int!](/docs/api/admin-graphql/latest/scalars/Int)non-nullDeprecatedShow arguments### Arguments[Anchor to onlyPublished](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publicationCount.arguments.onlyPublished)onlyPublished•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:trueInclude only the resource's publications that are published. If false, then return all the resource's publications including future publications.

[Anchor to publications](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publications)publications•[ProductPublicationConnection!](/docs/api/admin-graphql/latest/connections/ProductPublicationConnection)non-nullDeprecatedShow fields### Arguments[Anchor to onlyPublished](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publications.arguments.onlyPublished)onlyPublished•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:trueReturn only the publications that are published. If false, then return all publications.

[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publications.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publications.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publications.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publications.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publications.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to publishedOnChannel](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publishedOnChannel)publishedOnChannel•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullDeprecatedShow arguments### Arguments[Anchor to channelId](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publishedOnChannel.arguments.channelId)channelId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the channel to check.

[Anchor to publishedOnCurrentChannel](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.publishedOnCurrentChannel)publishedOnCurrentChannel•[Boolean!](/docs/api/admin-graphql/latest/scalars/Boolean)non-nullDeprecated[Anchor to sellingPlanGroupCount](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.sellingPlanGroupCount)sellingPlanGroupCount•[Int!](/docs/api/admin-graphql/latest/scalars/Int)non-nullDeprecated[Anchor to standardizedProductType](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.standardizedProductType)standardizedProductType•[StandardizedProductType](/docs/api/admin-graphql/latest/objects/StandardizedProductType)DeprecatedShow fields[Anchor to storefrontId](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.storefrontId)storefrontId•[StorefrontID!](/docs/api/admin-graphql/latest/scalars/StorefrontID)non-nullDeprecated[Anchor to totalVariants](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.totalVariants)totalVariants•[Int!](/docs/api/admin-graphql/latest/scalars/Int)non-nullDeprecated[Anchor to unpublishedChannels](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.unpublishedChannels)unpublishedChannels•[ChannelConnection!](/docs/api/admin-graphql/latest/connections/ChannelConnection)non-nullDeprecatedShow fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.unpublishedChannels.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.unpublishedChannels.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.unpublishedChannels.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.unpublishedChannels.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.unpublishedChannels.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

Was this section helpful?YesNo## Map### Fields and connections with this object- {}[AbandonedCheckoutLineItem.product](/docs/api/admin-graphql/latest/objects/AbandonedCheckoutLineItem#field-AbandonedCheckoutLineItem.fields.product)- {}[CalculatedDraftOrderLineItem.product](/docs/api/admin-graphql/latest/objects/CalculatedDraftOrderLineItem#field-CalculatedDraftOrderLineItem.fields.product)- {}[Channel.products](/docs/api/admin-graphql/latest/objects/Channel#field-Channel.fields.products)- {}[Collection.products](/docs/api/admin-graphql/latest/objects/Collection#field-Collection.fields.products)- {}[CombinedListing.parentProduct](/docs/api/admin-graphql/latest/objects/CombinedListing#field-CombinedListing.fields.parentProduct)- {}[CombinedListingChild.product](/docs/api/admin-graphql/latest/objects/CombinedListingChild#field-CombinedListingChild.fields.product)- {}[CustomerVisitProductInfo.product](/docs/api/admin-graphql/latest/objects/CustomerVisitProductInfo#field-CustomerVisitProductInfo.fields.product)- {}[DeliveryProfileItem.product](/docs/api/admin-graphql/latest/objects/DeliveryProfileItem#field-DeliveryProfileItem.fields.product)- {}[DiscountProducts.products](/docs/api/admin-graphql/latest/objects/DiscountProducts#field-DiscountProducts.fields.products)- {}[DraftOrderLineItem.product](/docs/api/admin-graphql/latest/objects/DraftOrderLineItem#field-DraftOrderLineItem.fields.product)- {}[LineItem.product](/docs/api/admin-graphql/latest/objects/LineItem#field-LineItem.fields.product)- {}[PriceRuleItemEntitlements.products](/docs/api/admin-graphql/latest/objects/PriceRuleItemEntitlements#field-PriceRuleItemEntitlements.fields.products)- {}[PriceRuleLineItemPrerequisites.products](/docs/api/admin-graphql/latest/objects/PriceRuleLineItemPrerequisites#field-PriceRuleLineItemPrerequisites.fields.products)- {}[Product.productParents](/docs/api/admin-graphql/latest/objects/Product#field-Product.fields.productParents)- {}[ProductBundleComponent.componentProduct](/docs/api/admin-graphql/latest/objects/ProductBundleComponent#field-ProductBundleComponent.fields.componentProduct)- {}[ProductBundleOperation.product](/docs/api/admin-graphql/latest/objects/ProductBundleOperation#field-ProductBundleOperation.fields.product)- {}[ProductComponentType.product](/docs/api/admin-graphql/latest/objects/ProductComponentType#field-ProductComponentType.fields.product)- <->[ProductConnection.nodes](/docs/api/admin-graphql/latest/connections/ProductConnection#returns-nodes)- {}[ProductDeleteOperation.product](/docs/api/admin-graphql/latest/objects/ProductDeleteOperation#field-ProductDeleteOperation.fields.product)- {}[ProductDuplicateOperation.newProduct](/docs/api/admin-graphql/latest/objects/ProductDuplicateOperation#field-ProductDuplicateOperation.fields.newProduct)- {}[ProductDuplicateOperation.product](/docs/api/admin-graphql/latest/objects/ProductDuplicateOperation#field-ProductDuplicateOperation.fields.product)- {}[ProductEdge.node](/docs/api/admin-graphql/latest/objects/ProductEdge#field-ProductEdge.fields.node)- ||-[ProductOperation.product](/docs/api/admin-graphql/latest/interfaces/ProductOperation#fields-product)- {}[ProductPublication.product](/docs/api/admin-graphql/latest/objects/ProductPublication#field-ProductPublication.fields.product)- {}[ProductSetOperation.product](/docs/api/admin-graphql/latest/objects/ProductSetOperation#field-ProductSetOperation.fields.product)- {}[ProductVariant.product](/docs/api/admin-graphql/latest/objects/ProductVariant#field-ProductVariant.fields.product)- {}[ProductVariant.productParents](/docs/api/admin-graphql/latest/objects/ProductVariant#field-ProductVariant.fields.productParents)- {}[Publication.includedProducts](/docs/api/admin-graphql/latest/objects/Publication#field-Publication.fields.includedProducts)- {}[Publication.products](/docs/api/admin-graphql/latest/objects/Publication#field-Publication.fields.products)- {}[SellingPlanGroup.products](/docs/api/admin-graphql/latest/objects/SellingPlanGroup#field-SellingPlanGroup.fields.products)Show deprecations### Possible type in- [CommentEventEmbed](/docs/api/admin-graphql/latest/unions/CommentEventEmbed)- [MetafieldReference](/docs/api/admin-graphql/latest/unions/MetafieldReference)- [MetafieldReferencer](/docs/api/admin-graphql/latest/unions/MetafieldReferencer)## [Anchor to Queries](/docs/api/admin-graphql/latest/objects/Product#queries)Queries- product (Product)- productByIdentifier (Product)- products (ProductConnection!)- productByHandle (Product): deprecated[Anchor to product](/docs/api/admin-graphql/latest/objects/Product#query-product)[product](/docs/api/admin-graphql/latest/queries/product)•queryRetrieves a [product](https://shopify.dev/docs/api/admin-graphql/latest/objects/Product) by its ID.

A product is an item that a merchant can sell in their store.

Use the `product` query when you need to:

- Access essential product data (for example, title, description, price, images, SEO metadata, and metafields).

- Build product detail pages and manage inventory.

- Handle international sales with localized pricing and content.

- Manage product variants and product options.

Learn more about working with [Shopify's product model](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model/product-model-components).

Show fields### Arguments[Anchor to id](/docs/api/admin-graphql/latest/objects/Product#query-product.arguments.id)id•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the `Product` to return.

[Anchor to productByIdentifier](/docs/api/admin-graphql/latest/objects/Product#query-productByIdentifier)[productByIdentifier](/docs/api/admin-graphql/latest/queries/productByIdentifier)•queryReturn a product by an identifier.

Show fields### Arguments[Anchor to identifier](/docs/api/admin-graphql/latest/objects/Product#query-productByIdentifier.arguments.identifier)identifier•[ProductIdentifierInput!](/docs/api/admin-graphql/latest/input-objects/ProductIdentifierInput)requiredThe identifier of the product.

Show input fields[Anchor to products](/docs/api/admin-graphql/latest/objects/Product#query-products)[products](/docs/api/admin-graphql/latest/queries/products)•queryRetrieves a list of [products](https://shopify.dev/docs/api/admin-graphql/latest/objects/Product)

in a store. Products are the items that merchants can sell in their store.

Use the `products` query when you need to:

- Build a browsing interface for a product catalog.

- Create product [searching](https://shopify.dev/docs/api/usage/search-syntax), [sorting](https://shopify.dev/docs/api/admin-graphql/latest/queries/products#arguments-sortKey), and [filtering](https://shopify.dev/docs/api/admin-graphql/latest/queries/products#arguments-query) experiences.

- Implement product recommendations.

- Sync product data with external systems.

The `products` query supports [pagination](https://shopify.dev/docs/api/usage/pagination-graphql)

to handle large product catalogs and [saved searches](https://shopify.dev/docs/api/admin-graphql/latest/queries/products#arguments-savedSearchId)

for frequently used product queries.

The `products` query returns products with their associated metadata, including:

- Basic product information (for example, title, description, vendor, and type)

- Product options and product variants, with their prices and inventory

- Media attachments (for example, images and videos)

- SEO metadata

- Product categories and tags

- Product availability and publishing statuses

Learn more about working with [Shopify's product model](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model/product-model-components).

Show fields### Arguments[Anchor to first](/docs/api/admin-graphql/latest/objects/Product#query-products.arguments.first)first•[Int](/docs/api/admin-graphql/latest/scalars/Int)The first `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to after](/docs/api/admin-graphql/latest/objects/Product#query-products.arguments.after)after•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come after the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to last](/docs/api/admin-graphql/latest/objects/Product#query-products.arguments.last)last•[Int](/docs/api/admin-graphql/latest/scalars/Int)The last `n` elements from the [paginated list](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to before](/docs/api/admin-graphql/latest/objects/Product#query-products.arguments.before)before•[String](/docs/api/admin-graphql/latest/scalars/String)The elements that come before the specified [cursor](https://shopify.dev/api/usage/pagination-graphql).

[Anchor to reverse](/docs/api/admin-graphql/latest/objects/Product#query-products.arguments.reverse)reverse•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/admin-graphql/latest/objects/Product#query-products.arguments.sortKey)sortKey•[ProductSortKeys](/docs/api/admin-graphql/latest/enums/ProductSortKeys)Default:IDSort the underlying list using a key. If your query is slow or returns an error, then [try specifying a sort key that matches the field used in the search](https://shopify.dev/api/usage/pagination-graphql#search-performance-considerations).

Show enum values[Anchor to query](/docs/api/admin-graphql/latest/objects/Product#query-products.arguments.query)query•[String](/docs/api/admin-graphql/latest/scalars/String)A filter made up of terms, connectives, modifiers, and comparators.

You can apply one or more filters to a query. Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-default)default•stringFilter by a case-insensitive search of multiple fields in a document.

Example:- `query=Bob Norman`- `query=title:green hoodie`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-barcode)barcode•stringFilter by the product variant [`barcode`](https://shopify.dev/api/admin-graphql/latest/objects/ProductVariant#field-barcode) field.

Example:- `barcode:ABC-abc-1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-bundles)bundles•booleanFilter by a [product bundle](https://shopify.dev/docs/apps/build/product-merchandising/bundles). A product bundle is a set of two or more related products, which are commonly offered at a discount.

Example:- `bundles:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-category_id)category_id•stringFilter by the product [category ID](https://shopify.dev/api/admin-graphql/latest/objects/Product#field-category) (`product.category.id`). A product category is the category of a product from [Shopify's Standard Product Taxonomy](https://shopify.github.io/product-taxonomy/releases/unstable/?categoryId=sg-4-17-2-17).

Example:- `category_id:sg-4-17-2-17`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-collection_id)collection_id•idFilter by the collection [`id`](https://shopify.dev/api/admin-graphql/latest/objects/Collection#field-id) field.

Example:- `collection_id:108179161409`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-combined_listing_role)combined_listing_role•stringFilter by the role of the product in a [combined listing](https://shopify.dev/apps/build/product-merchandising/combined-listings).

Valid values:- `parent` - `child` - `no_role` Example:- `combined_listing_role:parent`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-created_at)created_at•timeFilter by the date and time when the product was created.

Example:- `created_at:>'2020-10-21T23:39:20Z'`- `created_at:<now`- `created_at:<='2024'`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-delivery_profile_id)delivery_profile_id•idFilter by the delivery profile [`id`](https://shopify.dev/api/admin-graphql/latest/objects/DeliveryProfile#field-id) field.

Example:- `delivery_profile_id:108179161409`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-error_feedback)error_feedback•stringFilter by products with publishing errors.

[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-gift_card)gift_card•booleanFilter by the product [`isGiftCard`](https://shopify.dev/api/admin-graphql/latest/objects/Product#field-isgiftcard) field.

Example:- `gift_card:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-handle)handle•stringFilter by a comma-separated list of product [handles](https://shopify.dev/api/admin-graphql/latest/queries/products#argument-query-filter-handle).

Example:- `handle:the-minimal-snowboard`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-has_only_composites)has_only_composites•booleanFilter by products that have only composite variants.

Example:- `has_only_composites:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-has_only_default_variant)has_only_default_variant•booleanFilter by products that have only a default variant. A default variant is the only variant if no other variants are specified.

Example:- `has_only_default_variant:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-has_variant_with_components)has_variant_with_components•booleanFilter by products that have variants with associated components.

Example:- `has_variant_with_components:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-id)id•idFilter by `id` range.

Example:- `id:1234`- `id:>=1234`- `id:<=1234`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-inventory_total)inventory_total•integerFilter by inventory count.

Example:- `inventory_total:0`- `inventory_total:>150`- `inventory_total:>=200`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-is_price_reduced)is_price_reduced•booleanFilter by products that have a reduced price. For more information, refer to the [`CollectionRule`](https://shopify.dev/api/admin-graphql/latest/objects/CollectionRule) object.

Example:- `is_price_reduced:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-metafields.{namespace}.{key})metafields.{namespace}.{key}•mixedFilters resources by metafield value. Format: `metafields.{namespace}.{key}:{value}`. Learn more about [querying by metafield value](https://shopify.dev/apps/build/custom-data/metafields/query-by-metafield-value).

Example:- `metafields.custom.on_sale:true`- `metafields.product.material:"gid://shopify/Metaobject/43458085"`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-out_of_stock_somewhere)out_of_stock_somewhere•booleanFilter by products that are out of stock in at least one location.

Example:- `out_of_stock_somewhere:true`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-price)price•bigdecimalFilter by the product variant [`price`](https://shopify.dev/api/admin-graphql/latest/objects/Productvariant#field-price) field.

Example:- `price:100.57`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-product_configuration_owner)product_configuration_owner•stringFilter by the app [`id`](https://shopify.dev/api/admin-graphql/latest/objects/App#field-id) field.

Example:- `product_configuration_owner:10001`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-product_publication_status)product_publication_status•stringFilter by channel approval process status of the resource on a channel, such as the online store. The value is a composite of the [channel `app` ID](https://shopify.dev/api/admin-graphql/latest/objects/Channel#field-Channel.fields.app) (`Channel.app.id`) and one of the valid values. For simple visibility checks, use [published_status](https://shopify.dev/api/admin-graphql/latest/queries/products#argument-query-filter-publishable_status) instead.

Valid values:- `* {channel_app_id}-approved` - `* {channel_app_id}-rejected` - `* {channel_app_id}-needs_action` - `* {channel_app_id}-awaiting_review` - `* {channel_app_id}-published` - `* {channel_app_id}-demoted` - `* {channel_app_id}-scheduled` - `* {channel_app_id}-provisionally_published` Example:- `product_publication_status:189769876-approved`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-product_type)product_type•stringFilter by a comma-separated list of [product types](https://help.shopify.com/manual/products/details/product-type).

Example:- `product_type:snowboard`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-publication_ids)publication_ids•stringFilter by a comma-separated list of publication IDs that are associated with the product.

Example:- `publication_ids:184111530305,184111694145`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-publishable_status)publishable_status•string**Deprecated:** This parameter is deprecated as of 2025-12 and will be removed in a future API version. Use [published_status](https://shopify.dev/api/admin-graphql/latest/queries/products#argument-query-filter-publishable_status) for visibility checks. Filter by the publishable status of the resource on a channel. The value is a composite of the [channel `app` ID](https://shopify.dev/api/admin-graphql/latest/objects/Channel#app-price) (`Channel.app.id`) and one of the valid status values.

Valid values:- `* {channel_app_id}-unset` - `* {channel_app_id}-pending` - `* {channel_app_id}-approved` - `* {channel_app_id}-not_approved` Example:- `publishable_status:580111-unset`- `publishable_status:580111-pending`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-published_at)published_at•timeFilter by the date and time when the product was published to the online store and other sales channels.

Example:- `published_at:>2020-10-21T23:39:20Z`- `published_at:<now`- `published_at:<=2024`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-published_status)published_status•stringFilter resources by their visibility and publication state on a channel. Online store channel filtering: - `online_store_channel`: Returns all resources in the online store channel, regardless of publication status. - `published`/`visible`: Returns resources that are published to the online store. - `unpublished`: Returns resources that are not published to the online store. Channel-specific filtering using the [channel `app` ID](https://shopify.dev/api/admin-graphql/latest/objects/Channel#app-price) (`Channel.app.id`) with suffixes: - `{channel_app_id}-published`: Returns resources published to the specified channel. - `{channel_app_id}-visible`: Same as `{channel_app_id}-published` (kept for backwards compatibility). - `{channel_app_id}-intended`: Returns resources added to the channel but not yet published. - `{channel_app_id}-hidden`: Returns resources not added to the channel or not published. Other: - `unavailable`: Returns resources not published to any channel.

Valid values:- `online_store_channel` - `published` - `visible` - `unpublished` - `* {channel_app_id}-published` - `* {channel_app_id}-visible` - `* {channel_app_id}-intended` - `* {channel_app_id}-hidden` - `unavailable` Example:- `published_status:online_store_channel`- `published_status:published`- `published_status:580111-published`- `published_status:580111-hidden`- `published_status:unavailable`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-sku)sku•stringFilter by the product variant [`sku`](https://shopify.dev/api/admin-graphql/latest/objects/ProductVariant#field-sku) field. [Learn more about SKUs](https://help.shopify.com/manual/products/details/sku).

Example:- `sku:XYZ-12345`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-status)status•stringFilter by a comma-separated list of statuses. You can use statuses to manage inventory. Shopify only displays products with an `ACTIVE` status in online stores, sales channels, and apps.

Valid values:- `active` Default- `archived` - `draft` Example:- `status:active,draft`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-tag)tag•stringFilter objects by the `tag` field.

Example:- `tag:my_tag`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-tag_not)tag_not•stringFilter by objects that don’t have the specified tag.

Example:- `tag_not:my_tag`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-title)title•stringFilter by the product [`title`](https://shopify.dev/api/admin-graphql/latest/objects/Product#field-title) field.

Example:- `title:The Minimal Snowboard`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-updated_at)updated_at•timeFilter by the date and time when the product was last updated.

Example:- `updated_at:>'2020-10-21T23:39:20Z'`- `updated_at:<now`- `updated_at:<='2024'`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-variant_id)variant_id•idFilter by the product variant [`id`](https://shopify.dev/api/admin-graphql/latest/objects/ProductVariant#field-id) field.

Example:- `variant_id:45779434701121`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-variant_title)variant_title•stringFilter by the product variant [`title`](https://shopify.dev/api/admin-graphql/latest/objects/ProductVariant#field-title) field.

Example:- `variant_title:'Special ski wax'`[Anchor to ](/docs/api/admin-graphql/latest/objects/Product#argument-query-filter-vendor)vendor•stringFilter by the origin or source of the product. Learn more about [vendors and managing vendor information](https://help.shopify.com/manual/products/managing-vendor-info).

Example:- `vendor:Snowdevil`- `vendor:Snowdevil OR vendor:Icedevil`[Anchor to savedSearchId](/docs/api/admin-graphql/latest/objects/Product#query-products.arguments.savedSearchId)savedSearchId•[ID](/docs/api/admin-graphql/latest/scalars/ID)The ID of a [saved search](https://shopify.dev/api/admin-graphql/latest/objects/savedsearch#field-id).

The search’s query string is used as the query argument.

[Anchor to productByHandle](/docs/api/admin-graphql/latest/objects/Product#query-productByHandle)[productByHandle](/docs/api/admin-graphql/latest/queries/productByHandle)•queryDeprecatedShow fields### Arguments[Anchor to handle](/docs/api/admin-graphql/latest/objects/Product#query-productByHandle.arguments.handle)handle•[String!](/docs/api/admin-graphql/latest/scalars/String)requiredA unique string that identifies the product. Handles are automatically generated based on the product's title, and are always lowercase. Whitespace and special characters are replaced with a hyphen: `-`. If there are multiple consecutive whitespace or special characters, then they're replaced with a single hyphen. Whitespace or special characters at the beginning are removed. If a duplicate product title is used, then the handle is auto-incremented by one. For example, if you had two products called `Potion`, then their handles would be `potion` and `potion-1`. After a product has been created, changing the product title doesn't update the handle.

Was this section helpful?YesNo## <?>Product Queries### Queried by- <?>[product](/docs/api/admin-graphql/latest/queries/product)- <?>[productByIdentifier](/docs/api/admin-graphql/latest/queries/productByIdentifier)- <?>[products](/docs/api/admin-graphql/latest/queries/products)Show deprecations## [Anchor to Mutations](/docs/api/admin-graphql/latest/objects/Product#mutations)Mutations- combinedListingUpdate (CombinedListingUpdatePayload)- priceListFixedPricesByProductUpdate (PriceListFixedPricesByProductUpdatePayload)- productCreate (ProductCreatePayload)- productDuplicate (ProductDuplicatePayload)- productJoinSellingPlanGroups (ProductJoinSellingPlanGroupsPayload)- productLeaveSellingPlanGroups (ProductLeaveSellingPlanGroupsPayload)- productOptionsCreate (ProductOptionsCreatePayload)- productOptionsDelete (ProductOptionsDeletePayload)- productOptionsReorder (ProductOptionsReorderPayload)- productOptionUpdate (ProductOptionUpdatePayload)- productSet (ProductSetPayload)- productUpdate (ProductUpdatePayload)- productVariantAppendMedia (ProductVariantAppendMediaPayload)- productVariantDetachMedia (ProductVariantDetachMediaPayload)- productVariantsBulkCreate (ProductVariantsBulkCreatePayload)- productVariantsBulkDelete (ProductVariantsBulkDeletePayload)- productVariantsBulkReorder (ProductVariantsBulkReorderPayload)- productVariantsBulkUpdate (ProductVariantsBulkUpdatePayload)[Anchor to combinedListingUpdate](/docs/api/admin-graphql/latest/objects/Product#mutation-combinedListingUpdate)[combinedListingUpdate](/docs/api/admin-graphql/latest/mutations/combinedListingUpdate)•mutationAdd, remove and update `CombinedListing`s of a given Product.

`CombinedListing`s are comprised of multiple products to create a single listing. There are two kinds of products used in a `CombinedListing`:

- Parent products

- Child products

The parent product is created with a `productCreate` with a `CombinedListingRole` of `PARENT`. Once created, you can associate child products with the parent product using this mutation. Parent products represent the idea of a product (e.g. Shoe).

Child products represent a particular option value (or combination of option values) of a parent product. For instance, with your Shoe parent product, you may have several child products representing specific colors of the shoe (e.g. Shoe - Blue). You could also have child products representing more than a single option (e.g. Shoe - Blue/Canvas, Shoe - Blue/Leather, etc...).

The combined listing is the association of parent product to one or more child products.

Learn more about [Combined Listings](https://shopify.dev/apps/selling-strategies/combined-listings).

Show payload### Arguments[Anchor to parentProductId](/docs/api/admin-graphql/latest/objects/Product#mutation-combinedListingUpdate.arguments.parentProductId)parentProductId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the parent product.

[Anchor to title](/docs/api/admin-graphql/latest/objects/Product#mutation-combinedListingUpdate.arguments.title)title•[String](/docs/api/admin-graphql/latest/scalars/String)The updated title for the combined listing.

[Anchor to productsAdded](/docs/api/admin-graphql/latest/objects/Product#mutation-combinedListingUpdate.arguments.productsAdded)productsAdded•[[ChildProductRelationInput!]](/docs/api/admin-graphql/latest/input-objects/ChildProductRelationInput)The child products to add and their assigned options and option values.

Show input fields[Anchor to productsEdited](/docs/api/admin-graphql/latest/objects/Product#mutation-combinedListingUpdate.arguments.productsEdited)productsEdited•[[ChildProductRelationInput!]](/docs/api/admin-graphql/latest/input-objects/ChildProductRelationInput)The child products to edit and their assigned options and option values.

Show input fields[Anchor to productsRemovedIds](/docs/api/admin-graphql/latest/objects/Product#mutation-combinedListingUpdate.arguments.productsRemovedIds)productsRemovedIds•[[ID!]](/docs/api/admin-graphql/latest/scalars/ID)The IDs of products to be removed from the combined listing.

[Anchor to optionsAndValues](/docs/api/admin-graphql/latest/objects/Product#mutation-combinedListingUpdate.arguments.optionsAndValues)optionsAndValues•[[OptionAndValueInput!]](/docs/api/admin-graphql/latest/input-objects/OptionAndValueInput)The ordered options and values to be used by the combined listing. Options and values will be reordered to match the order specified here.

Show input fields[Anchor to priceListFixedPricesByProductUpdate](/docs/api/admin-graphql/latest/objects/Product#mutation-priceListFixedPricesByProductUpdate)[priceListFixedPricesByProductUpdate](/docs/api/admin-graphql/latest/mutations/priceListFixedPricesByProductUpdate)•mutationSets or removes fixed prices for all variants of a [`Product`](https://shopify.dev/docs/api/admin-graphql/latest/objects/Product) on a [`PriceList`](https://shopify.dev/docs/api/admin-graphql/latest/objects/PriceList). Simplifies pricing management when all variants of a product should have the same price on a price list, rather than setting individual variant prices.

When you add a fixed price for a product, all its [`ProductVariant`](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant) objects receive the same price on the price list. When you remove a product's fixed prices, all variant prices revert to the price list's adjustment rules.

Show payload### Arguments[Anchor to pricesToAdd](/docs/api/admin-graphql/latest/objects/Product#mutation-priceListFixedPricesByProductUpdate.arguments.pricesToAdd)pricesToAdd•[[PriceListProductPriceInput!]](/docs/api/admin-graphql/latest/input-objects/PriceListProductPriceInput)A list of `PriceListProductPriceInput` that identifies which products to update the fixed prices for.

Show input fields[Anchor to pricesToDeleteByProductIds](/docs/api/admin-graphql/latest/objects/Product#mutation-priceListFixedPricesByProductUpdate.arguments.pricesToDeleteByProductIds)pricesToDeleteByProductIds•[[ID!]](/docs/api/admin-graphql/latest/scalars/ID)A list of product IDs that identifies which products to remove the fixed prices for.

[Anchor to priceListId](/docs/api/admin-graphql/latest/objects/Product#mutation-priceListFixedPricesByProductUpdate.arguments.priceListId)priceListId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe price list to update the prices for.

[Anchor to productCreate](/docs/api/admin-graphql/latest/objects/Product#mutation-productCreate)[productCreate](/docs/api/admin-graphql/latest/mutations/productCreate)•mutationCreates a [product](https://shopify.dev/docs/api/admin-graphql/latest/objects/Product)

with attributes such as title, description, vendor, and media.

The `productCreate` mutation helps you create many products at once, avoiding the tedious or time-consuming

process of adding them one by one in the Shopify admin. Common examples include creating products for a

new collection, launching a new product line, or adding seasonal products.

You can define product

[options](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductOption) and

[values](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductOptionValue),

allowing you to create products with different variations like sizes or colors. You can also associate media

files to your products, including images and videos.

The `productCreate` mutation only supports creating a product with its initial

[product variant](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant).

To create multiple product variants for a single product and manage prices, use the

[`productVariantsBulkCreate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkCreate)

mutation.

NoteThe `productCreate` mutation has a [throttle](https://shopify.dev/docs/api/usage/rate-limits#resource-based-rate-limits)

that takes effect when a store has 50,000 product variants. After this threshold is reached, no more than

1,000 new product variants can be created per day.**Note:** The `productCreate` mutation has a [throttle](https://shopify.dev/docs/api/usage/rate-limits#resource-based-rate-limits)

that takes effect when a store has 50,000 product variants. After this threshold is reached, no more than

1,000 new product variants can be created per day.**Note:** The <code><span class="PreventFireFoxApplyingGapToWBR">product<wbr/>Create</span></code> mutation has a <a href="https://shopify.dev/docs/api/usage/rate-limits#resource-based-rate-limits">throttle</a>

that takes effect when a store has 50,000 product variants. After this threshold is reached, no more than

1,000 new product variants can be created per day.After you create a product, you can make subsequent edits to the product using one of the following mutations:

- [`publishablePublish`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/publishablePublish):

Used to publish the product and make it available to customers. The `productCreate` mutation creates products

in an unpublished state by default, so you must perform a separate operation to publish the product.

- [`productUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productUpdate):

Used to update a single product, such as changing the product's title, description, vendor, or associated media.

- [`productSet`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productSet):

Used to perform multiple operations on products, such as creating or modifying product options and variants.

Learn more about the [product model](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model)

and [adding product data](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model/add-data).

Show payload### Arguments[Anchor to input](/docs/api/admin-graphql/latest/objects/Product#mutation-productCreate.arguments.input)input•[ProductInput](/docs/api/admin-graphql/latest/input-objects/ProductInput)DeprecatedShow input fields[Anchor to product](/docs/api/admin-graphql/latest/objects/Product#mutation-productCreate.arguments.product)product•[ProductCreateInput](/docs/api/admin-graphql/latest/input-objects/ProductCreateInput)The attributes of the new product.

Show input fields[Anchor to media](/docs/api/admin-graphql/latest/objects/Product#mutation-productCreate.arguments.media)media•[[CreateMediaInput!]](/docs/api/admin-graphql/latest/input-objects/CreateMediaInput)The media to add to the product.

Show input fields[Anchor to productDuplicate](/docs/api/admin-graphql/latest/objects/Product#mutation-productDuplicate)[productDuplicate](/docs/api/admin-graphql/latest/mutations/productDuplicate)•mutationDuplicates a product.

If you need to duplicate a large product, such as one that has many

[variants](https://shopify.dev/api/admin-graphql/latest/input-objects/ProductVariantInput)

that are active at several

[locations](https://shopify.dev/api/admin-graphql/latest/input-objects/InventoryLevelInput),

you might encounter timeout errors.

To avoid these timeout errors, you can instead duplicate the product asynchronously.

In API version 2024-10 and higher, include `synchronous: false` argument in this mutation to perform the duplication asynchronously.

In API version 2024-07 and lower, use the asynchronous [`ProductDuplicateAsyncV2`](https://shopify.dev/api/admin-graphql/2024-07/mutations/productDuplicateAsyncV2).

Metafield values are not duplicated if the unique values capability is enabled.

Show payload### Arguments[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productDuplicate.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the product to be duplicated.

[Anchor to newTitle](/docs/api/admin-graphql/latest/objects/Product#mutation-productDuplicate.arguments.newTitle)newTitle•[String!](/docs/api/admin-graphql/latest/scalars/String)requiredThe new title of the product.

[Anchor to newStatus](/docs/api/admin-graphql/latest/objects/Product#mutation-productDuplicate.arguments.newStatus)newStatus•[ProductStatus](/docs/api/admin-graphql/latest/enums/ProductStatus)The new status of the product. If no value is provided the status will be inherited from the original product.

Show enum values[Anchor to includeImages](/docs/api/admin-graphql/latest/objects/Product#mutation-productDuplicate.arguments.includeImages)includeImages•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseSpecifies whether or not to duplicate images.

[Anchor to includeTranslations](/docs/api/admin-graphql/latest/objects/Product#mutation-productDuplicate.arguments.includeTranslations)includeTranslations•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseSpecifies whether or not to duplicate translations.

[Anchor to synchronous](/docs/api/admin-graphql/latest/objects/Product#mutation-productDuplicate.arguments.synchronous)synchronous•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:trueSpecifies whether or not to run the mutation synchronously.

[Anchor to productJoinSellingPlanGroups](/docs/api/admin-graphql/latest/objects/Product#mutation-productJoinSellingPlanGroups)[productJoinSellingPlanGroups](/docs/api/admin-graphql/latest/mutations/productJoinSellingPlanGroups)•mutationAdds multiple selling plan groups to a product.

Show payload### Arguments[Anchor to id](/docs/api/admin-graphql/latest/objects/Product#mutation-productJoinSellingPlanGroups.arguments.id)id•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the product.

[Anchor to sellingPlanGroupIds](/docs/api/admin-graphql/latest/objects/Product#mutation-productJoinSellingPlanGroups.arguments.sellingPlanGroupIds)sellingPlanGroupIds•[[ID!]!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe IDs of the selling plan groups to add.

[Anchor to productLeaveSellingPlanGroups](/docs/api/admin-graphql/latest/objects/Product#mutation-productLeaveSellingPlanGroups)[productLeaveSellingPlanGroups](/docs/api/admin-graphql/latest/mutations/productLeaveSellingPlanGroups)•mutationRemoves multiple groups from a product.

Show payload### Arguments[Anchor to id](/docs/api/admin-graphql/latest/objects/Product#mutation-productLeaveSellingPlanGroups.arguments.id)id•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the product.

[Anchor to sellingPlanGroupIds](/docs/api/admin-graphql/latest/objects/Product#mutation-productLeaveSellingPlanGroups.arguments.sellingPlanGroupIds)sellingPlanGroupIds•[[ID!]!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe IDs of the selling plan groups to add.

[Anchor to productOptionsCreate](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionsCreate)[productOptionsCreate](/docs/api/admin-graphql/latest/mutations/productOptionsCreate)•mutationCreates one or more [options](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductOption)

on a [product](https://shopify.dev/docs/api/admin-graphql/latest/objects/Product),

such as size, color, or material. Each option includes a name, position, and a list of values. The combination

of a product option and value creates a [product variant](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant).

Use the `productOptionsCreate` mutation for the following use cases:

- **Add product choices**: Add a new option, like "Size" (Small, Medium, Large) or

"Color" (Red, Blue, Green), to an existing product so customers can select their preferred variant.

- **Enable personalization features**: Add options such as "Engraving text" to let customers customize their purchase.

- **Offer seasonal or limited edition products**: Add a new value

(for example, "Holiday red") to an existing option to support limited-time or seasonal variants.

- **Integrate with apps that manage product configuration**: Allow third-party apps to add options, like

"Bundle size", when customers select or customize

[product bundles](https://shopify.dev/docs/apps/build/product-merchandising/bundles).

- **Link options to metafields**: Associate a product option with a custom

[metafield](https://shopify.dev/docs/apps/build/custom-data), like "Fabric code", for

richer integrations with other systems or apps.

NoteThe `productOptionsCreate` mutation enforces strict data integrity for product options and variants.

All option positions must be sequential, and every option should be used by at least one variant.

If you use the [`CREATE` variant strategy](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsCreate#arguments-variantStrategy.enums.CREATE), consider the maximum allowed number of variants for each product is 2048.**Note:** The `productOptionsCreate` mutation enforces strict data integrity for product options and variants.

All option positions must be sequential, and every option should be used by at least one variant.

If you use the [`CREATE` variant strategy](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsCreate#arguments-variantStrategy.enums.CREATE), consider the maximum allowed number of variants for each product is 2048.**Note:** The <code><span class="PreventFireFoxApplyingGapToWBR">product<wbr/>Options<wbr/>Create</span></code> mutation enforces strict data integrity for product options and variants.

All option positions must be sequential, and every option should be used by at least one variant.

If you use the <a href="https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsCreate#arguments-variantStrategy.enums.CREATE"><code><span class="PreventFireFoxApplyingGapToWBR">C<wbr/>R<wbr/>E<wbr/>A<wbr/>T<wbr/>E</span></code> variant strategy</a>, consider the maximum allowed number of variants for each product is 2048.After you create product options, you can further manage a product's configuration using related mutations:

- [`productOptionUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionUpdate)

- [`productOptionsReorder`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsReorder)

- [`productOptionsDelete`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsDelete)

- [`productVariantsBulkCreate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkCreate)

- [`productVariantsBulkUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkUpdate)

- [`productSet`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productSet)

Learn more about the [product model](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model)

and [adding product data](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model/add-data).

Show payload### Arguments[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionsCreate.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the product to update.

[Anchor to options](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionsCreate.arguments.options)options•[[OptionCreateInput!]!](/docs/api/admin-graphql/latest/input-objects/OptionCreateInput)requiredOptions to add to the product.

Show input fields[Anchor to variantStrategy](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionsCreate.arguments.variantStrategy)variantStrategy•[ProductOptionCreateVariantStrategy](/docs/api/admin-graphql/latest/enums/ProductOptionCreateVariantStrategy)Default:LEAVE_AS_ISThe strategy defines which behavior the mutation should observe regarding variants.

If not provided or set to null, the strategy `LEAVE_AS_IS` will be used.

Show enum values[Anchor to productOptionsDelete](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionsDelete)[productOptionsDelete](/docs/api/admin-graphql/latest/mutations/productOptionsDelete)•mutationDeletes one or more [options](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductOption)

from a [product](https://shopify.dev/docs/api/admin-graphql/latest/objects/Product). Product options

define the choices available for a product, such as size, color, or material.

CautionRemoving an option can affect a product's

[variants](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant) and their

configuration. Deleting an option might also delete associated option values and, depending on the chosen

[strategy](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productoptionsdelete#arguments-strategy),

might affect variants.**Caution:** Removing an option can affect a product's

[variants](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant) and their

configuration. Deleting an option might also delete associated option values and, depending on the chosen

[strategy](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productoptionsdelete#arguments-strategy),

might affect variants.**Caution:** Removing an option can affect a product&#39;s

<a href="https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant">variants</a> and their

configuration. Deleting an option might also delete associated option values and, depending on the chosen

<a href="https://shopify.dev/docs/api/admin-graphql/latest/mutations/productoptionsdelete#arguments-strategy">strategy</a>,

might affect variants.Use the `productOptionsDelete` mutation for the following use cases:

- **Simplify product configuration**: Remove obsolete or unnecessary options

(for example, discontinue "Material" if all variants are now the same material).

- **Clean up after seasonal or limited-time offerings**: Delete options that are no longer

relevant (for example, "Holiday edition").

- **Automate catalog management**: Enable apps or integrations to programmatically remove options as product

data changes.

NoteThe `productOptionsDelete` mutation enforces strict data integrity for product options and variants.

All option positions must remain sequential, and every remaining option must be used by at least one variant.**Note:** The `productOptionsDelete` mutation enforces strict data integrity for product options and variants.

All option positions must remain sequential, and every remaining option must be used by at least one variant.**Note:** The <code><span class="PreventFireFoxApplyingGapToWBR">product<wbr/>Options<wbr/>Delete</span></code> mutation enforces strict data integrity for product options and variants.

All option positions must remain sequential, and every remaining option must be used by at least one variant.After you delete a product option, you can further manage a product's configuration using related mutations:

- [`productOptionsCreate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsCreate)

- [`productOptionUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionUpdate)

- [`productOptionsReorder`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsReorder)

- [`productVariantsBulkCreate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkCreate)

- [`productVariantsBulkUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkUpdate)

- [`productSet`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productSet)

Learn more about the [product model](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model)

and [adding product data](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model/add-data).

Show payload### Arguments[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionsDelete.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredID of the product from which to delete the options.

[Anchor to options](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionsDelete.arguments.options)options•[[ID!]!](/docs/api/admin-graphql/latest/scalars/ID)requiredIDs of the options to delete from the product.

[Anchor to strategy](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionsDelete.arguments.strategy)strategy•[ProductOptionDeleteStrategy](/docs/api/admin-graphql/latest/enums/ProductOptionDeleteStrategy)Default:DEFAULTThe strategy defines which behavior the mutation should observe,such as how to handle a situation where deleting an option would result in duplicate variants.

Show enum values[Anchor to productOptionsReorder](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionsReorder)[productOptionsReorder](/docs/api/admin-graphql/latest/mutations/productOptionsReorder)•mutationReorders the [options](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductOption) and

[option values](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductOptionValue) on a

[product](https://shopify.dev/docs/api/admin-graphql/latest/objects/Product),

updating the order in which [product variants](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant)

are presented to customers.

The `productOptionsReorder` mutation accepts a list of product options, each identified by `id` or `name`, and an

optional list of values (also by `id` or `name`) specifying the new order. The order of options in the

mutation's input determines their new positions (for example, the first option becomes `option1`).

The order of values within each option determines their new positions. The mutation recalculates the order of

variants based on the new option and value order.

Suppose a product has the following variants:

- `"Red / Small"`

- `"Green / Medium"`

- `"Blue / Small"`

You reorder options and values:

```

options: [

{ name: "Size", values: [{ name: "Small" }, { name: "Medium" }] },

{ name: "Color", values: [{ name: "Green" }, { name: "Red" }, { name: "Blue" }] }

]

```

The resulting variant order will be:

- `"Small / Green"`

- `"Small / Red"`

- `"Small / Blue"`

- `"Medium / Green"`

Use the `productOptionsReorder` mutation for the following use cases:

- **Change the order of product options**: For example, display "Color" before "Size" in a store.

- **Reorder option values within an option**: For example, show "Red" before "Blue" in a color picker.

- **Control the order of product variants**: The order of options and their values determines the sequence in which variants are listed and selected.

- **Highlight best-selling options**: Present the most popular or relevant options and values first.

- **Promote merchandising strategies**: Highlight seasonal colors, limited editions, or featured sizes.

NoteThe `productOptionsReorder` mutation enforces strict data integrity for product options and variants.

All option positions must be sequential, and every option should be used by at least one variant.**Note:** The `productOptionsReorder` mutation enforces strict data integrity for product options and variants.

All option positions must be sequential, and every option should be used by at least one variant.**Note:** The <code><span class="PreventFireFoxApplyingGapToWBR">product<wbr/>Options<wbr/>Reorder</span></code> mutation enforces strict data integrity for product options and variants.

All option positions must be sequential, and every option should be used by at least one variant.After you reorder product options, you can further manage a product's configuration using related mutations:

- [`productOptionsCreate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsCreate)

- [`productOptionsDelete`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsDelete)

- [`productVariantsBulkCreate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkCreate)

- [`productVariantsBulkUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkUpdate)

- [`productSet`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productSet)

Learn more about the [product model](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model)

and [managing product data](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model/add-data).

Show payload### Arguments[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionsReorder.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the product to update.

[Anchor to options](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionsReorder.arguments.options)options•[[OptionReorderInput!]!](/docs/api/admin-graphql/latest/input-objects/OptionReorderInput)requiredOptions to reorder on the product.

Show input fields[Anchor to productOptionUpdate](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionUpdate)[productOptionUpdate](/docs/api/admin-graphql/latest/mutations/productOptionUpdate)•mutationUpdates an [option](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductOption)

on a [product](https://shopify.dev/docs/api/admin-graphql/latest/objects/Product),

such as size, color, or material. Each option includes a name, position, and a list of values. The combination

of a product option and value creates a [product variant](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant).

Use the `productOptionUpdate` mutation for the following use cases:

- **Update product choices**: Modify an existing option, like "Size" (Small, Medium, Large) or

"Color" (Red, Blue, Green), so customers can select their preferred variant.

- **Enable personalization features**: Update an option (for example, "Engraving text") to let customers customize their purchase.

- **Offer seasonal or limited edition products**: Update a value

(for example, "Holiday red") on an existing option to support limited-time or seasonal variants.

- **Integrate with apps that manage product configuration**: Allow third-party apps to update options, like

"Bundle size", when customers select or customize

[product bundles](https://shopify.dev/docs/apps/build/product-merchandising/bundles).

- **Link options to metafields**: Associate a product option with a custom

[metafield](https://shopify.dev/docs/apps/build/custom-data), like "Fabric code", for

richer integrations with other systems or apps.

NoteThe `productOptionUpdate` mutation enforces strict data integrity for product options and variants.

All option positions must be sequential, and every option should be used by at least one variant.**Note:** The `productOptionUpdate` mutation enforces strict data integrity for product options and variants.

All option positions must be sequential, and every option should be used by at least one variant.**Note:** The <code><span class="PreventFireFoxApplyingGapToWBR">product<wbr/>Option<wbr/>Update</span></code> mutation enforces strict data integrity for product options and variants.

All option positions must be sequential, and every option should be used by at least one variant.After you update a product option, you can further manage a product's configuration using related mutations:

- [`productOptionsCreate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsCreate)

- [`productOptionsDelete`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsDelete)

- [`productOptionsReorder`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsReorder)

- [`productVariantsBulkCreate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkCreate)

- [`productVariantsBulkUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkUpdate)

- [`productSet`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productSet)

Learn more about the [product model](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model)

and [adding product data](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model/add-data).

Show payload### Arguments[Anchor to option](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionUpdate.arguments.option)option•[OptionUpdateInput!](/docs/api/admin-graphql/latest/input-objects/OptionUpdateInput)requiredOption to update.

Show input fields[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionUpdate.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the Product the Option belongs to.

[Anchor to optionValuesToAdd](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionUpdate.arguments.optionValuesToAdd)optionValuesToAdd•[[OptionValueCreateInput!]](/docs/api/admin-graphql/latest/input-objects/OptionValueCreateInput)New option values to create.

Show input fields[Anchor to optionValuesToUpdate](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionUpdate.arguments.optionValuesToUpdate)optionValuesToUpdate•[[OptionValueUpdateInput!]](/docs/api/admin-graphql/latest/input-objects/OptionValueUpdateInput)Existing option values to update.

Show input fields[Anchor to optionValuesToDelete](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionUpdate.arguments.optionValuesToDelete)optionValuesToDelete•[[ID!]](/docs/api/admin-graphql/latest/scalars/ID)IDs of the existing option values to delete.

[Anchor to variantStrategy](/docs/api/admin-graphql/latest/objects/Product#mutation-productOptionUpdate.arguments.variantStrategy)variantStrategy•[ProductOptionUpdateVariantStrategy](/docs/api/admin-graphql/latest/enums/ProductOptionUpdateVariantStrategy)The strategy defines which behavior the mutation should observe regarding variants,

such as creating variants or deleting them in response to option values to add or to delete.

If not provided or set to null, the strategy `LEAVE_AS_IS` will be used.

Show enum values[Anchor to productSet](/docs/api/admin-graphql/latest/objects/Product#mutation-productSet)[productSet](/docs/api/admin-graphql/latest/mutations/productSet)•mutationPerforms multiple operations to create or update products in a single request.

Use the `productSet` mutation to sync information from an external data source into Shopify, manage large

product catalogs, and perform batch updates. The mutation is helpful for bulk product management, including price

adjustments, inventory updates, and product lifecycle management.

The behavior of `productSet` depends on the type of field it's modifying:

- **For list fields**: Creates new entries, updates existing entries, and deletes existing entries

that aren't included in the mutation's input. Common examples of list fields include

[`collections`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productSet#arguments-input.fields.collections),

[`metafields`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productSet#arguments-input.fields.metafields),

and [`variants`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productSet#arguments-input.fields.variants).

- **For all other field types**: Updates only the included fields. Any omitted fields will remain unchanged.

NoteBy default, stores have a limit of 2048 product variants for each product.**Note:** By default, stores have a limit of 2048 product variants for each product.**Note:** By default, stores have a limit of 2048 product variants for each product.You can run `productSet` in one of the following modes:

- **Synchronously**: Returns the updated product in the response.

- **Asynchronously**: Returns a [`ProductSetOperation`](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductSetOperation) object.

Use the [`productOperation`](https://shopify.dev/api/admin-graphql/latest/queries/productOperation) query to check the status of the operation and

retrieve details of the updated product and its product variants.

If you need to only manage product variants, then use one of the following mutations:

- [`productVariantsBulkCreate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkCreate)

- [`productVariantsBulkUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkUpdate)

- [`productVariantsBulkDelete`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkDelete)

If you need to only manage product options, then use one of the following mutations:

- [`productOptionsCreate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsCreate)

- [`productOptionUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionUpdate)

- [`productOptionsReorder`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsReorder)

- [`productOptionsDelete`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsDelete)

Learn more about [syncing product data from an external source](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model/sync-data).

Show payload### Arguments[Anchor to input](/docs/api/admin-graphql/latest/objects/Product#mutation-productSet.arguments.input)input•[ProductSetInput!](/docs/api/admin-graphql/latest/input-objects/ProductSetInput)requiredThe properties of the newly created or updated product.

Show input fields[Anchor to synchronous](/docs/api/admin-graphql/latest/objects/Product#mutation-productSet.arguments.synchronous)synchronous•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:trueWhether the mutation should be run synchronously or asynchronously.

If `true`, the mutation will return the updated `product`.

If `false`, the mutation will return a `productSetOperation`.

Defaults to `true`.

Setting `synchronous: false` may be desirable depending on the input complexity/size, and should be used if you are experiencing timeouts.

**Note**: When run in the context of a

[bulk operation](https://shopify.dev/api/usage/bulk-operations/imports), the mutation will

always run synchronously and this argument will be ignored.

[Anchor to identifier](/docs/api/admin-graphql/latest/objects/Product#mutation-productSet.arguments.identifier)identifier•[ProductSetIdentifiers](/docs/api/admin-graphql/latest/input-objects/ProductSetIdentifiers)Specifies the identifier that will be used to lookup the resource.

Show input fields[Anchor to productUpdate](/docs/api/admin-graphql/latest/objects/Product#mutation-productUpdate)[productUpdate](/docs/api/admin-graphql/latest/mutations/productUpdate)•mutationUpdates a [product](https://shopify.dev/docs/api/admin-graphql/latest/objects/Product)

with attributes such as title, description, vendor, and media.

The `productUpdate` mutation helps you modify many products at once, avoiding the tedious or time-consuming

process of updating them one by one in the Shopify admin. Common examples including updating

product details like status or tags.

The `productUpdate` mutation doesn't support updating

[product variants](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant).

To update multiple product variants for a single product and manage prices, use the

[`productVariantsBulkUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkUpdate)

mutation.

NoteThe `productUpdate` mutation has a [throttle](https://shopify.dev/docs/api/usage/rate-limits#resource-based-rate-limits)

that takes effect when a store has 50,000 product variants. After this threshold is reached, no more than

1,000 new product variants can be updated per day.**Note:** The `productUpdate` mutation has a [throttle](https://shopify.dev/docs/api/usage/rate-limits#resource-based-rate-limits)

that takes effect when a store has 50,000 product variants. After this threshold is reached, no more than

1,000 new product variants can be updated per day.**Note:** The <code><span class="PreventFireFoxApplyingGapToWBR">product<wbr/>Update</span></code> mutation has a <a href="https://shopify.dev/docs/api/usage/rate-limits#resource-based-rate-limits">throttle</a>

that takes effect when a store has 50,000 product variants. After this threshold is reached, no more than

1,000 new product variants can be updated per day.After updating a product, you can make additional changes using one of the following mutations:

- [`productSet`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productSet):

Used to perform multiple operations on products, such as creating or modifying product options and variants.

- [`publishablePublish`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/publishablePublish):

Used to publish the product and make it available to customers, if the product is currently unpublished.

Learn more about the [product model](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model)

and [adding product data](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model/add-data).

Show payload### Arguments[Anchor to input](/docs/api/admin-graphql/latest/objects/Product#mutation-productUpdate.arguments.input)input•[ProductInput](/docs/api/admin-graphql/latest/input-objects/ProductInput)DeprecatedShow input fields[Anchor to product](/docs/api/admin-graphql/latest/objects/Product#mutation-productUpdate.arguments.product)product•[ProductUpdateInput](/docs/api/admin-graphql/latest/input-objects/ProductUpdateInput)The updated properties for a product.

Show input fields[Anchor to media](/docs/api/admin-graphql/latest/objects/Product#mutation-productUpdate.arguments.media)media•[[CreateMediaInput!]](/docs/api/admin-graphql/latest/input-objects/CreateMediaInput)List of new media to be added to the product.

Show input fields[Anchor to productVariantAppendMedia](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantAppendMedia)[productVariantAppendMedia](/docs/api/admin-graphql/latest/mutations/productVariantAppendMedia)•mutationAppends existing media from a product to specific variants of that product, creating associations between media files and particular product options. This allows different variants to showcase relevant images or videos.

For example, a t-shirt product might have color variants where each color variant displays only the images showing that specific color, helping customers see exactly what they're purchasing.

Use `ProductVariantAppendMedia` to:

- Associate specific images with product variants for accurate display

- Build variant-specific media management in product interfaces

- Implement automated media assignment based on variant attributes

The operation links existing product media to variants without duplicating files, maintaining efficient media storage while enabling variant-specific displays.

Learn more about [product variants](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant).

Show payload### Arguments[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantAppendMedia.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredSpecifies the product associated to the media.

[Anchor to variantMedia](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantAppendMedia.arguments.variantMedia)variantMedia•[[ProductVariantAppendMediaInput!]!](/docs/api/admin-graphql/latest/input-objects/ProductVariantAppendMediaInput)requiredA list of pairs of variants and media to be attached to the variants.

Show input fields[Anchor to productVariantDetachMedia](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantDetachMedia)[productVariantDetachMedia](/docs/api/admin-graphql/latest/mutations/productVariantDetachMedia)•mutationDetaches media from product variants.

Show payload### Arguments[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantDetachMedia.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredSpecifies the product to which the variants and media are associated.

[Anchor to variantMedia](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantDetachMedia.arguments.variantMedia)variantMedia•[[ProductVariantDetachMediaInput!]!](/docs/api/admin-graphql/latest/input-objects/ProductVariantDetachMediaInput)requiredA list of pairs of variants and media to be deleted from the variants.

Show input fields[Anchor to productVariantsBulkCreate](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkCreate)[productVariantsBulkCreate](/docs/api/admin-graphql/latest/mutations/productVariantsBulkCreate)•mutationCreates multiple [product variants](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant)

for a single [product](https://shopify.dev/docs/api/admin-graphql/latest/objects/Product) in one operation.

You can run this mutation directly or as part of a [bulk operation](https://shopify.dev/docs/api/usage/bulk-operations/imports)

for large-scale catalog updates.

Use the `productVariantsBulkCreate` mutation to efficiently add new product variants—such as different sizes,

colors, or materials—to an existing product. The mutation is helpful if you need to add product variants in bulk,

such as importing from an external system.

The mutation supports:

- Creating variants with custom option values

- Associating media (for example, images, videos, and 3D models) with the product or its variants

- Handling complex product configurations

NoteBy default, stores have a limit of 2048 product variants for each product.**Note:** By default, stores have a limit of 2048 product variants for each product.**Note:** By default, stores have a limit of 2048 product variants for each product.After creating variants, you can make additional changes using one of the following mutations:

- [`productVariantsBulkUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productVariantsBulkUpdate):

Updates multiple product variants for a single product in one operation.

- [`productSet`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productSet):

Used to perform multiple operations on products, such as creating or modifying product options and variants.

You can also specifically manage product options through related mutations:

- [`productOptionsCreate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsCreate)

- [`productOptionUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionUpdate)

- [`productOptionsReorder`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsReorder)

- [`productOptionsDelete`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsDelete)

Learn more about the [product model](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model)

and [adding product data](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model/add-data).

Show payload### Arguments[Anchor to variants](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkCreate.arguments.variants)variants•[[ProductVariantsBulkInput!]!](/docs/api/admin-graphql/latest/input-objects/ProductVariantsBulkInput)requiredAn array of product variants to be created.

Show input fields[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkCreate.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the product on which to create the variants.

[Anchor to media](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkCreate.arguments.media)media•[[CreateMediaInput!]](/docs/api/admin-graphql/latest/input-objects/CreateMediaInput)List of new media to be added to the product.

Show input fields[Anchor to strategy](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkCreate.arguments.strategy)strategy•[ProductVariantsBulkCreateStrategy](/docs/api/admin-graphql/latest/enums/ProductVariantsBulkCreateStrategy)Default:DEFAULTThe strategy defines which behavior the mutation should observe, such as whether to keep or delete the standalone variant (when product has only a single or default variant) when creating new variants in bulk.

Show enum values[Anchor to productVariantsBulkDelete](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkDelete)[productVariantsBulkDelete](/docs/api/admin-graphql/latest/mutations/productVariantsBulkDelete)•mutationDeletes multiple variants in a single [`Product`](https://shopify.dev/docs/api/admin-graphql/latest/objects/Product). Specify the product ID and an array of variant IDs to remove variants in bulk. You can call this mutation directly or through the [`bulkOperationRunMutation`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/bulkOperationRunMutation) mutation. Returns the updated product and any [`UserError`](https://shopify.dev/docs/api/admin-graphql/latest/objects/UserError) objects.

Show payload### Arguments[Anchor to variantsIds](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkDelete.arguments.variantsIds)variantsIds•[[ID!]!](/docs/api/admin-graphql/latest/scalars/ID)requiredAn array of product variants IDs to delete.

[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkDelete.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the product with the variants to update.

[Anchor to productVariantsBulkReorder](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkReorder)[productVariantsBulkReorder](/docs/api/admin-graphql/latest/mutations/productVariantsBulkReorder)•mutationReorders multiple variants in a single product. This mutation can be called directly or via the bulkOperation.

Show payload### Arguments[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkReorder.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe product ID of the variants to be reordered.

[Anchor to positions](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkReorder.arguments.positions)positions•[[ProductVariantPositionInput!]!](/docs/api/admin-graphql/latest/input-objects/ProductVariantPositionInput)requiredAn array of variant positions.

Show input fields[Anchor to productVariantsBulkUpdate](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkUpdate)[productVariantsBulkUpdate](/docs/api/admin-graphql/latest/mutations/productVariantsBulkUpdate)•mutationUpdates multiple [product variants](https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant)

for a single [product](https://shopify.dev/docs/api/admin-graphql/latest/objects/Product) in one operation.

You can run this mutation directly or as part of a [bulk operation](https://shopify.dev/docs/api/usage/bulk-operations/imports)

for large-scale catalog updates.

Use the `productVariantsBulkUpdate` mutation to efficiently modify product variants—such as different sizes,

colors, or materials—associated with an existing product. The mutation is helpful if you need to update a

product's variants in bulk, such as importing from an external system.

The mutation supports:

- Updating variants with custom option values

- Associating media (for example, images, videos, and 3D models) with the product or its variants

- Handling complex product configurations

NoteBy default, stores have a limit of 2048 product variants for each product.**Note:** By default, stores have a limit of 2048 product variants for each product.**Note:** By default, stores have a limit of 2048 product variants for each product.After creating variants, you can make additional changes using the

[`productSet`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productSet) mutation,

which is used to perform multiple operations on products, such as creating or modifying product options and variants.

You can also specifically manage product options through related mutations:

- [`productOptionsCreate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsCreate)

- [`productOptionUpdate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionUpdate)

- [`productOptionsReorder`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsReorder)

- [`productOptionsDelete`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/productOptionsDelete)

Learn more about the [product model](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model)

and [adding product data](https://shopify.dev/docs/apps/build/graphql/migrate/new-product-model/add-data).

Show payload### Arguments[Anchor to variants](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkUpdate.arguments.variants)variants•[[ProductVariantsBulkInput!]!](/docs/api/admin-graphql/latest/input-objects/ProductVariantsBulkInput)requiredAn array of product variants to update.

Show input fields[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkUpdate.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the product associated with the variants to update.

[Anchor to media](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkUpdate.arguments.media)media•[[CreateMediaInput!]](/docs/api/admin-graphql/latest/input-objects/CreateMediaInput)List of new media to be added to the product.

Show input fields[Anchor to allowPartialUpdates](/docs/api/admin-graphql/latest/objects/Product#mutation-productVariantsBulkUpdate.arguments.allowPartialUpdates)allowPartialUpdates•[Boolean](/docs/api/admin-graphql/latest/scalars/Boolean)Default:falseWhen partial updates are allowed, valid variant changes may be persisted even if some of

the variants updated have invalid data and cannot be persisted.

When partial updates are not allowed, any error will prevent all variants from updating.

### Deprecated mutations- productChangeStatus (ProductChangeStatusPayload): deprecated- productCreateMedia (ProductCreateMediaPayload): deprecated- productDeleteMedia (ProductDeleteMediaPayload): deprecated- productPublish (ProductPublishPayload): deprecated- productUnpublish (ProductUnpublishPayload): deprecated- productUpdateMedia (ProductUpdateMediaPayload): deprecated[Anchor to productChangeStatus](/docs/api/admin-graphql/latest/objects/Product#mutation-productChangeStatus)[productChangeStatus](/docs/api/admin-graphql/latest/mutations/productChangeStatus)•mutationDeprecatedShow payload### Arguments[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productChangeStatus.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe ID of the product.

[Anchor to status](/docs/api/admin-graphql/latest/objects/Product#mutation-productChangeStatus.arguments.status)status•[ProductStatus!](/docs/api/admin-graphql/latest/enums/ProductStatus)requiredThe status to be assigned to the product.

Show enum values[Anchor to productCreateMedia](/docs/api/admin-graphql/latest/objects/Product#mutation-productCreateMedia)[productCreateMedia](/docs/api/admin-graphql/latest/mutations/productCreateMedia)•mutationDeprecatedShow payload### Arguments[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productCreateMedia.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredSpecifies the product associated with the media.

[Anchor to media](/docs/api/admin-graphql/latest/objects/Product#mutation-productCreateMedia.arguments.media)media•[[CreateMediaInput!]!](/docs/api/admin-graphql/latest/input-objects/CreateMediaInput)requiredList of new media to be added to a product.

Show input fields[Anchor to productDeleteMedia](/docs/api/admin-graphql/latest/objects/Product#mutation-productDeleteMedia)[productDeleteMedia](/docs/api/admin-graphql/latest/mutations/productDeleteMedia)•mutationDeprecatedShow payload### Arguments[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productDeleteMedia.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredSpecifies the product ID from which the media will be deleted.

[Anchor to mediaIds](/docs/api/admin-graphql/latest/objects/Product#mutation-productDeleteMedia.arguments.mediaIds)mediaIds•[[ID!]!](/docs/api/admin-graphql/latest/scalars/ID)requiredThe media IDs to be deleted.

[Anchor to productPublish](/docs/api/admin-graphql/latest/objects/Product#mutation-productPublish)[productPublish](/docs/api/admin-graphql/latest/mutations/productPublish)•mutationDeprecatedShow payload### Arguments[Anchor to input](/docs/api/admin-graphql/latest/objects/Product#mutation-productPublish.arguments.input)input•[ProductPublishInput!](/docs/api/admin-graphql/latest/input-objects/ProductPublishInput)requiredSpecifies the product to publish and the channels to publish it to.

Show input fields[Anchor to productUnpublish](/docs/api/admin-graphql/latest/objects/Product#mutation-productUnpublish)[productUnpublish](/docs/api/admin-graphql/latest/mutations/productUnpublish)•mutationDeprecatedShow payload### Arguments[Anchor to input](/docs/api/admin-graphql/latest/objects/Product#mutation-productUnpublish.arguments.input)input•[ProductUnpublishInput!](/docs/api/admin-graphql/latest/input-objects/ProductUnpublishInput)requiredSpecifies the product to unpublish and the channel to unpublish it from.

Show input fields[Anchor to productUpdateMedia](/docs/api/admin-graphql/latest/objects/Product#mutation-productUpdateMedia)[productUpdateMedia](/docs/api/admin-graphql/latest/mutations/productUpdateMedia)•mutationDeprecatedShow payload### Arguments[Anchor to productId](/docs/api/admin-graphql/latest/objects/Product#mutation-productUpdateMedia.arguments.productId)productId•[ID!](/docs/api/admin-graphql/latest/scalars/ID)requiredSpecifies the product on which media will be updated.

[Anchor to media](/docs/api/admin-graphql/latest/objects/Product#mutation-productUpdateMedia.arguments.media)media•[[UpdateMediaInput!]!](/docs/api/admin-graphql/latest/input-objects/UpdateMediaInput)requiredA list of media updates.

Show input fieldsWas this section helpful?YesNo## <~> Product Mutations### Mutated by- <~>[combinedListingUpdate](/docs/api/admin-graphql/latest/mutations/combinedListingUpdate)- <~>[priceListFixedPricesByProductUpdate](/docs/api/admin-graphql/latest/mutations/priceListFixedPricesByProductUpdate)- <~>[productCreate](/docs/api/admin-graphql/latest/mutations/productCreate)- <~>[productDuplicate](/docs/api/admin-graphql/latest/mutations/productDuplicate)- <~>[productJoinSellingPlanGroups](/docs/api/admin-graphql/latest/mutations/productJoinSellingPlanGroups)- <~>[productLeaveSellingPlanGroups](/docs/api/admin-graphql/latest/mutations/productLeaveSellingPlanGroups)- <~>[productOptionsCreate](/docs/api/admin-graphql/latest/mutations/productOptionsCreate)- <~>[productOptionsDelete](/docs/api/admin-graphql/latest/mutations/productOptionsDelete)- <~>[productOptionsReorder](/docs/api/admin-graphql/latest/mutations/productOptionsReorder)- <~>[productOptionUpdate](/docs/api/admin-graphql/latest/mutations/productOptionUpdate)- <~>[productSet](/docs/api/admin-graphql/latest/mutations/productSet)- <~>[productUpdate](/docs/api/admin-graphql/latest/mutations/productUpdate)- <~>[productVariantAppendMedia](/docs/api/admin-graphql/latest/mutations/productVariantAppendMedia)- <~>[productVariantDetachMedia](/docs/api/admin-graphql/latest/mutations/productVariantDetachMedia)- <~>[productVariantsBulkCreate](/docs/api/admin-graphql/latest/mutations/productVariantsBulkCreate)- <~>[productVariantsBulkDelete](/docs/api/admin-graphql/latest/mutations/productVariantsBulkDelete)- <~>[productVariantsBulkReorder](/docs/api/admin-graphql/latest/mutations/productVariantsBulkReorder)- <~>[productVariantsBulkUpdate](/docs/api/admin-graphql/latest/mutations/productVariantsBulkUpdate)Show deprecations## [Anchor to Interfaces](/docs/api/admin-graphql/latest/objects/Product#interfaces)Interfaces- HasEvents- HasMetafieldDefinitions- HasMetafields- HasPublishedTranslations- LegacyInteroperability- Navigable- Node- OnlineStorePreviewable- Publishable[Anchor to HasEvents](/docs/api/admin-graphql/latest/objects/Product#interface-HasEvents)[HasEvents](/docs/api/admin-graphql/latest/interfaces/HasEvents)•interface[Anchor to HasMetafieldDefinitions](/docs/api/admin-graphql/latest/objects/Product#interface-HasMetafieldDefinitions)[HasMetafieldDefinitions](/docs/api/admin-graphql/latest/interfaces/HasMetafieldDefinitions)•interface[Anchor to HasMetafields](/docs/api/admin-graphql/latest/objects/Product#interface-HasMetafields)[HasMetafields](/docs/api/admin-graphql/latest/interfaces/HasMetafields)•interface[Anchor to HasPublishedTranslations](/docs/api/admin-graphql/latest/objects/Product#interface-HasPublishedTranslations)[HasPublishedTranslations](/docs/api/admin-graphql/latest/interfaces/HasPublishedTranslations)•interface[Anchor to LegacyInteroperability](/docs/api/admin-graphql/latest/objects/Product#interface-LegacyInteroperability)[LegacyInteroperability](/docs/api/admin-graphql/latest/interfaces/LegacyInteroperability)•interface[Anchor to Navigable](/docs/api/admin-graphql/latest/objects/Product#interface-Navigable)[Navigable](/docs/api/admin-graphql/latest/interfaces/Navigable)•interface[Anchor to Node](/docs/api/admin-graphql/latest/objects/Product#interface-Node)[Node](/docs/api/admin-graphql/latest/interfaces/Node)•interface[Anchor to OnlineStorePreviewable](/docs/api/admin-graphql/latest/objects/Product#interface-OnlineStorePreviewable)[OnlineStorePreviewable](/docs/api/admin-graphql/latest/interfaces/OnlineStorePreviewable)•interface[Anchor to Publishable](/docs/api/admin-graphql/latest/objects/Product#interface-Publishable)[Publishable](/docs/api/admin-graphql/latest/interfaces/Publishable)•interfaceWas this section helpful?YesNo## ||-Product Implements### Implements- ||-[HasEvents](/docs/api/admin-graphql/latest/interfaces/HasEvents)- ||-[HasMetafieldDefinitions](/docs/api/admin-graphql/latest/interfaces/HasMetafieldDefinitions)- ||-[HasMetafields](/docs/api/admin-graphql/latest/interfaces/HasMetafields)- ||-[HasPublishedTranslations](/docs/api/admin-graphql/latest/interfaces/HasPublishedTranslations)- ||-[LegacyInteroperability](/docs/api/admin-graphql/latest/interfaces/LegacyInteroperability)- ||-[Navigable](/docs/api/admin-graphql/latest/interfaces/Navigable)- ||-[Node](/docs/api/admin-graphql/latest/interfaces/Node)- ||-[OnlineStorePreviewable](/docs/api/admin-graphql/latest/interfaces/OnlineStorePreviewable)- ||-[Publishable](/docs/api/admin-graphql/latest/interfaces/Publishable)### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)