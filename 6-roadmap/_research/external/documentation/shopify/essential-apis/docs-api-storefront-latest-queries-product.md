---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront/latest/queries/product",
    "fetched_at": "2026-02-10T13:41:24.318601",
    "status": 200,
    "size_bytes": 492347
  },
  "metadata": {
    "title": "product - Storefront API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "queries",
    "component": "product"
  }
}
---

# product - Storefront API

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to product](/docs/api/storefront/latest/queries/product#top)# productqueryAsk assistantFetch a specific `Product` by one of its unique attributes.

[Anchor to Arguments](/docs/api/storefront/latest/queries/product#arguments)## Arguments- handle (String)- id (ID)[Anchor to handle](/docs/api/storefront/latest/queries/product#arguments-handle)handle•[String](/docs/api/storefront/latest/scalars/String)The handle of the `Product`.

[Anchor to id](/docs/api/storefront/latest/queries/product#arguments-id)id•[ID](/docs/api/storefront/latest/scalars/ID)The ID of the `Product`.

Was this section helpful?YesNo## [Anchor to Possible returns](/docs/api/storefront/latest/queries/product#possible-returns)Possible returns- Product (Product)[Anchor to Product](/docs/api/storefront/latest/queries/product#returns-Product)Product•[Product](/docs/api/storefront/latest/objects/Product)The `Product` object lets you manage products in a merchant’s store.

Products are the goods and services that merchants offer to customers.

They can include various details such as title, description, price, images, and options such as size or color.

You can use [product variants](/docs/api/storefront/latest/objects/ProductVariant)

to create or update different versions of the same product.

You can also add or update product [media](/docs/api/storefront/latest/interfaces/Media).

Products can be organized by grouping them into a [collection](/docs/api/storefront/latest/objects/Collection).

Learn more about working with [products and collections](/docs/storefronts/headless/building-with-the-storefront-api/products-collections).

Show fields[Anchor to adjacentVariants](/docs/api/storefront/latest/queries/product#returns-Product.fields.adjacentVariants)adjacentVariants•[[ProductVariant!]!](/docs/api/storefront/latest/objects/ProductVariant)non-nullA list of variants whose selected options differ with the provided selected options by one, ordered by variant id.

If selected options are not provided, adjacent variants to the first available variant is returned.

Note that this field returns an array of variants. In most cases, the number of variants in this array will be low.

However, with a low number of options and a high number of values per option, the number of variants returned

here can be high. In such cases, it recommended to avoid using this field.

This list of variants can be used in combination with the `options` field to build a rich variant picker that

includes variant availability or other variant information.

Show fields### Arguments[Anchor to selectedOptions](/docs/api/storefront/latest/queries/product#returns-Product.fields.adjacentVariants.arguments.selectedOptions)selectedOptions•[[SelectedOptionInput!]](/docs/api/storefront/latest/input-objects/SelectedOptionInput)The input fields used for a selected option.

The input must not contain more than `250` values.

Show input fields[Anchor to ignoreUnknownOptions](/docs/api/storefront/latest/queries/product#returns-Product.fields.adjacentVariants.arguments.ignoreUnknownOptions)ignoreUnknownOptions•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:trueWhether to ignore product options that are not present on the requested product.

[Anchor to caseInsensitiveMatch](/docs/api/storefront/latest/queries/product#returns-Product.fields.adjacentVariants.arguments.caseInsensitiveMatch)caseInsensitiveMatch•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseWhether to perform case insensitive match on option names and values.

[Anchor to availableForSale](/docs/api/storefront/latest/queries/product#returns-Product.fields.availableForSale)availableForSale•[Boolean!](/docs/api/storefront/latest/scalars/Boolean)non-nullIndicates if at least one product variant is available for sale.

[Anchor to category](/docs/api/storefront/latest/queries/product#returns-Product.fields.category)category•[TaxonomyCategory](/docs/api/storefront/latest/objects/TaxonomyCategory)The category of a product from [Shopify's Standard Product Taxonomy](https://shopify.github.io/product-taxonomy/releases/unstable/?categoryId=sg-4-17-2-17).

Show fields[Anchor to collections](/docs/api/storefront/latest/queries/product#returns-Product.fields.collections)collections•[CollectionConnection!](/docs/api/storefront/latest/connections/CollectionConnection)non-nullA list of [collections](/docs/api/storefront/latest/objects/Collection) that include the product.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/queries/product#returns-Product.fields.collections.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/queries/product#returns-Product.fields.collections.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/queries/product#returns-Product.fields.collections.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/queries/product#returns-Product.fields.collections.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/queries/product#returns-Product.fields.collections.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to compareAtPriceRange](/docs/api/storefront/latest/queries/product#returns-Product.fields.compareAtPriceRange)compareAtPriceRange•[ProductPriceRange!](/docs/api/storefront/latest/objects/ProductPriceRange)non-nullThe [compare-at price range](https://help.shopify.com/manual/products/details/product-pricing/sale-pricing) of the product in the shop's default currency.

Show fields[Anchor to createdAt](/docs/api/storefront/latest/queries/product#returns-Product.fields.createdAt)createdAt•[DateTime!](/docs/api/storefront/latest/scalars/DateTime)non-nullThe date and time when the product was created.

[Anchor to description](/docs/api/storefront/latest/queries/product#returns-Product.fields.description)description•[String!](/docs/api/storefront/latest/scalars/String)non-nullA single-line description of the product, with [HTML tags](https://developer.mozilla.org/en-US/docs/Web/HTML) removed.

Show arguments### Arguments[Anchor to truncateAt](/docs/api/storefront/latest/queries/product#returns-Product.fields.description.arguments.truncateAt)truncateAt•[Int](/docs/api/storefront/latest/scalars/Int)Truncates a string after the given length.

[Anchor to descriptionHtml](/docs/api/storefront/latest/queries/product#returns-Product.fields.descriptionHtml)descriptionHtml•[HTML!](/docs/api/storefront/latest/scalars/HTML)non-nullThe description of the product, with

HTML tags. For example, the description might include

bold `<strong></strong>` and italic `<i></i>` text.

[Anchor to encodedVariantAvailability](/docs/api/storefront/latest/queries/product#returns-Product.fields.encodedVariantAvailability)encodedVariantAvailability•[String](/docs/api/storefront/latest/scalars/String)An encoded string containing all option value combinations

with a corresponding variant that is currently available for sale.

Integers represent option and values:

[0,1] represents option_value at array index 0 for the option at array index 0

`:`, `,`, ` ` and `-` are control characters.

`:` indicates a new option. ex: 0:1 indicates value 0 for the option in position 1, value 1 for the option in position 2.

`,` indicates the end of a repeated prefix, mulitple consecutive commas indicate the end of multiple repeated prefixes.

` ` indicates a gap in the sequence of option values. ex: 0 4 indicates option values in position 0 and 4 are present.

`-` indicates a continuous range of option values. ex: 0 1-3 4

Decoding process:

Example options: [Size, Color, Material]

Example values: [[Small, Medium, Large], [Red, Blue], [Cotton, Wool]]

Example encoded string: "0:0:0,1:0-1,,1:0:0-1,1:1,,2:0:1,1:0,,"

Step 1: Expand ranges into the numbers they represent: "0:0:0,1:0 1,,1:0:0 1,1:1,,2:0:1,1:0,,"

Step 2: Expand repeated prefixes: "0:0:0,0:1:0 1,1:0:0 1,1:1:1,2:0:1,2:1:0,"

Step 3: Expand shared prefixes so data is encoded as a string: "0:0:0,0:1:0,0:1:1,1:0:0,1:0:1,1:1:1,2:0:1,2:1:0,"

Step 4: Map to options + option values to determine existing variants:

[Small, Red, Cotton] (0:0:0), [Small, Blue, Cotton] (0:1:0), [Small, Blue, Wool] (0:1:1),

[Medium, Red, Cotton] (1:0:0), [Medium, Red, Wool] (1:0:1), [Medium, Blue, Wool] (1:1:1),

[Large, Red, Wool] (2:0:1), [Large, Blue, Cotton] (2:1:0).

[Anchor to encodedVariantExistence](/docs/api/storefront/latest/queries/product#returns-Product.fields.encodedVariantExistence)encodedVariantExistence•[String](/docs/api/storefront/latest/scalars/String)An encoded string containing all option value combinations with a corresponding variant.

Integers represent option and values:

[0,1] represents option_value at array index 0 for the option at array index 0

`:`, `,`, ` ` and `-` are control characters.

`:` indicates a new option. ex: 0:1 indicates value 0 for the option in position 1, value 1 for the option in position 2.

`,` indicates the end of a repeated prefix, mulitple consecutive commas indicate the end of multiple repeated prefixes.

` ` indicates a gap in the sequence of option values. ex: 0 4 indicates option values in position 0 and 4 are present.

`-` indicates a continuous range of option values. ex: 0 1-3 4

Decoding process:

Example options: [Size, Color, Material]

Example values: [[Small, Medium, Large], [Red, Blue], [Cotton, Wool]]

Example encoded string: "0:0:0,1:0-1,,1:0:0-1,1:1,,2:0:1,1:0,,"

Step 1: Expand ranges into the numbers they represent: "0:0:0,1:0 1,,1:0:0 1,1:1,,2:0:1,1:0,,"

Step 2: Expand repeated prefixes: "0:0:0,0:1:0 1,1:0:0 1,1:1:1,2:0:1,2:1:0,"

Step 3: Expand shared prefixes so data is encoded as a string: "0:0:0,0:1:0,0:1:1,1:0:0,1:0:1,1:1:1,2:0:1,2:1:0,"

Step 4: Map to options + option values to determine existing variants:

[Small, Red, Cotton] (0:0:0), [Small, Blue, Cotton] (0:1:0), [Small, Blue, Wool] (0:1:1),

[Medium, Red, Cotton] (1:0:0), [Medium, Red, Wool] (1:0:1), [Medium, Blue, Wool] (1:1:1),

[Large, Red, Wool] (2:0:1), [Large, Blue, Cotton] (2:1:0).

[Anchor to featuredImage](/docs/api/storefront/latest/queries/product#returns-Product.fields.featuredImage)featuredImage•[Image](/docs/api/storefront/latest/objects/Image)The featured image for the product.

This field is functionally equivalent to `images(first: 1)`.

Show fields[Anchor to handle](/docs/api/storefront/latest/queries/product#returns-Product.fields.handle)handle•[String!](/docs/api/storefront/latest/scalars/String)non-nullA unique, human-readable string of the product's title.

A handle can contain letters, hyphens (`-`), and numbers, but no spaces.

The handle is used in the online store URL for the product.

[Anchor to id](/docs/api/storefront/latest/queries/product#returns-Product.fields.id)id•[ID!](/docs/api/storefront/latest/scalars/ID)non-nullA globally-unique ID.

[Anchor to images](/docs/api/storefront/latest/queries/product#returns-Product.fields.images)images•[ImageConnection!](/docs/api/storefront/latest/connections/ImageConnection)non-nullList of images associated with the product.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/queries/product#returns-Product.fields.images.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/queries/product#returns-Product.fields.images.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/queries/product#returns-Product.fields.images.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/queries/product#returns-Product.fields.images.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/queries/product#returns-Product.fields.images.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/storefront/latest/queries/product#returns-Product.fields.images.arguments.sortKey)sortKey•[ProductImageSortKeys](/docs/api/storefront/latest/enums/ProductImageSortKeys)Default:POSITIONSort the underlying list by the given key.

Show enum values[Anchor to isGiftCard](/docs/api/storefront/latest/queries/product#returns-Product.fields.isGiftCard)isGiftCard•[Boolean!](/docs/api/storefront/latest/scalars/Boolean)non-nullWhether the product is a gift card.

[Anchor to media](/docs/api/storefront/latest/queries/product#returns-Product.fields.media)media•[MediaConnection!](/docs/api/storefront/latest/connections/MediaConnection)non-nullThe [media](/docs/apps/build/online-store/product-media) that are associated with the product. Valid media are images, 3D models, videos.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/queries/product#returns-Product.fields.media.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/queries/product#returns-Product.fields.media.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/queries/product#returns-Product.fields.media.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/queries/product#returns-Product.fields.media.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/queries/product#returns-Product.fields.media.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/storefront/latest/queries/product#returns-Product.fields.media.arguments.sortKey)sortKey•[ProductMediaSortKeys](/docs/api/storefront/latest/enums/ProductMediaSortKeys)Default:POSITIONSort the underlying list by the given key.

Show enum values[Anchor to metafield](/docs/api/storefront/latest/queries/product#returns-Product.fields.metafield)metafield•[Metafield](/docs/api/storefront/latest/objects/Metafield) Token access requiredA [custom field](https://shopify.dev/docs/apps/build/custom-data), including its `namespace` and `key`, that's associated with a Shopify resource for the purposes of adding and storing additional information.

Show fields### Arguments[Anchor to namespace](/docs/api/storefront/latest/queries/product#returns-Product.fields.metafield.arguments.namespace)namespace•[String](/docs/api/storefront/latest/scalars/String)The container the metafield belongs to. If omitted, the app-reserved namespace will be used.

[Anchor to key](/docs/api/storefront/latest/queries/product#returns-Product.fields.metafield.arguments.key)key•[String!](/docs/api/storefront/latest/scalars/String)requiredThe identifier for the metafield.

[Anchor to metafields](/docs/api/storefront/latest/queries/product#returns-Product.fields.metafields)metafields•[[Metafield]!](/docs/api/storefront/latest/objects/Metafield)non-null Token access requiredA list of [custom fields](/docs/apps/build/custom-data) that a merchant associates with a Shopify resource.

Show fields### Arguments[Anchor to identifiers](/docs/api/storefront/latest/queries/product#returns-Product.fields.metafields.arguments.identifiers)identifiers•[[HasMetafieldsIdentifier!]!](/docs/api/storefront/latest/input-objects/HasMetafieldsIdentifier)requiredThe list of metafields to retrieve by namespace and key.

The input must not contain more than `250` values.

Show input fields[Anchor to onlineStoreUrl](/docs/api/storefront/latest/queries/product#returns-Product.fields.onlineStoreUrl)onlineStoreUrl•[URL](/docs/api/storefront/latest/scalars/URL)The product's URL on the online store.

If `null`, then the product isn't published to the online store sales channel.

[Anchor to options](/docs/api/storefront/latest/queries/product#returns-Product.fields.options)options•[[ProductOption!]!](/docs/api/storefront/latest/objects/ProductOption)non-nullA list of product options. The limit is defined by the [shop's resource limits for product options](/docs/api/admin-graphql/latest/objects/Shop#field-resourcelimits) (`Shop.resourceLimits.maxProductOptions`).

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/queries/product#returns-Product.fields.options.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Truncate the array result to this size.

[Anchor to priceRange](/docs/api/storefront/latest/queries/product#returns-Product.fields.priceRange)priceRange•[ProductPriceRange!](/docs/api/storefront/latest/objects/ProductPriceRange)non-nullThe minimum and maximum prices of a product, expressed in decimal numbers.

For example, if the product is priced between $10.00 and $50.00,

then the price range is $10.00 - $50.00.

Show fields[Anchor to productType](/docs/api/storefront/latest/queries/product#returns-Product.fields.productType)productType•[String!](/docs/api/storefront/latest/scalars/String)non-nullThe [product type](https://help.shopify.com/manual/products/details/product-type)

that merchants define.

[Anchor to publishedAt](/docs/api/storefront/latest/queries/product#returns-Product.fields.publishedAt)publishedAt•[DateTime!](/docs/api/storefront/latest/scalars/DateTime)non-nullThe date and time when the product was published to the channel.

[Anchor to requiresSellingPlan](/docs/api/storefront/latest/queries/product#returns-Product.fields.requiresSellingPlan)requiresSellingPlan•[Boolean!](/docs/api/storefront/latest/scalars/Boolean)non-nullWhether the product can only be purchased with a [selling plan](/docs/apps/build/purchase-options/subscriptions/selling-plans). Products that are sold on subscription (`requiresSellingPlan: true`) can be updated only for online stores. If you update a product to be subscription-only (`requiresSellingPlan:false`), then the product is unpublished from all channels, except the online store.

[Anchor to selectedOrFirstAvailableVariant](/docs/api/storefront/latest/queries/product#returns-Product.fields.selectedOrFirstAvailableVariant)selectedOrFirstAvailableVariant•[ProductVariant](/docs/api/storefront/latest/objects/ProductVariant)Find an active product variant based on selected options, availability or the first variant.

All arguments are optional. If no selected options are provided, the first available variant is returned.

If no variants are available, the first variant is returned.

Show fields### Arguments[Anchor to selectedOptions](/docs/api/storefront/latest/queries/product#returns-Product.fields.selectedOrFirstAvailableVariant.arguments.selectedOptions)selectedOptions•[[SelectedOptionInput!]](/docs/api/storefront/latest/input-objects/SelectedOptionInput)The input fields used for a selected option.

The input must not contain more than `250` values.

Show input fields[Anchor to ignoreUnknownOptions](/docs/api/storefront/latest/queries/product#returns-Product.fields.selectedOrFirstAvailableVariant.arguments.ignoreUnknownOptions)ignoreUnknownOptions•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:trueWhether to ignore unknown product options.

[Anchor to caseInsensitiveMatch](/docs/api/storefront/latest/queries/product#returns-Product.fields.selectedOrFirstAvailableVariant.arguments.caseInsensitiveMatch)caseInsensitiveMatch•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseWhether to perform case insensitive match on option names and values.

[Anchor to sellingPlanGroups](/docs/api/storefront/latest/queries/product#returns-Product.fields.sellingPlanGroups)sellingPlanGroups•[SellingPlanGroupConnection!](/docs/api/storefront/latest/connections/SellingPlanGroupConnection)non-nullA list of all [selling plan groups](/docs/apps/build/purchase-options/subscriptions/selling-plans/build-a-selling-plan) that are associated with the product either directly, or through the product's variants.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/queries/product#returns-Product.fields.sellingPlanGroups.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/queries/product#returns-Product.fields.sellingPlanGroups.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/queries/product#returns-Product.fields.sellingPlanGroups.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/queries/product#returns-Product.fields.sellingPlanGroups.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/queries/product#returns-Product.fields.sellingPlanGroups.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to seo](/docs/api/storefront/latest/queries/product#returns-Product.fields.seo)seo•[SEO!](/docs/api/storefront/latest/objects/SEO)non-nullThe [SEO title and description](https://help.shopify.com/manual/promoting-marketing/seo/adding-keywords)

that are associated with a product.

Show fields[Anchor to tags](/docs/api/storefront/latest/queries/product#returns-Product.fields.tags)tags•[[String!]!](/docs/api/storefront/latest/scalars/String)non-nullA comma-separated list of searchable keywords that are

associated with the product. For example, a merchant might apply the `sports`

and `summer` tags to products that are associated with sportwear for summer.

Updating `tags` overwrites any existing tags that were previously added to the product.

To add new tags without overwriting existing tags,

use the GraphQL Admin API's [`tagsAdd`](/docs/api/admin-graphql/latest/mutations/tagsadd)

mutation.

[Anchor to title](/docs/api/storefront/latest/queries/product#returns-Product.fields.title)title•[String!](/docs/api/storefront/latest/scalars/String)non-nullThe name for the product that displays to customers. The title is used to construct the product's handle.

For example, if a product is titled "Black Sunglasses", then the handle is `black-sunglasses`.

[Anchor to totalInventory](/docs/api/storefront/latest/queries/product#returns-Product.fields.totalInventory)totalInventory•[Int](/docs/api/storefront/latest/scalars/Int) Token access requiredThe quantity of inventory that's in stock.

[Anchor to trackingParameters](/docs/api/storefront/latest/queries/product#returns-Product.fields.trackingParameters)trackingParameters•[String](/docs/api/storefront/latest/scalars/String)URL parameters to be added to a page URL to track the origin of on-site search traffic for [analytics reporting](https://help.shopify.com/manual/reports-and-analytics/shopify-reports/report-types/default-reports/behaviour-reports). Returns a result when accessed through the [search](/docs/api/storefront/2026-01/queries/search) or [predictiveSearch](/docs/api/storefront/2026-01/queries/predictiveSearch) queries, otherwise returns null.

[Anchor to updatedAt](/docs/api/storefront/latest/queries/product#returns-Product.fields.updatedAt)updatedAt•[DateTime!](/docs/api/storefront/latest/scalars/DateTime)non-nullThe date and time when the product was last modified.

A product's `updatedAt` value can change for different reasons. For example, if an order

is placed for a product that has inventory tracking set up, then the inventory adjustment

is counted as an update.

[Anchor to variantBySelectedOptions](/docs/api/storefront/latest/queries/product#returns-Product.fields.variantBySelectedOptions)variantBySelectedOptions•[ProductVariant](/docs/api/storefront/latest/objects/ProductVariant)Find a product’s variant based on its selected options.

This is useful for converting a user’s selection of product options into a single matching variant.

If there is not a variant for the selected options, `null` will be returned.

Show fields### Arguments[Anchor to selectedOptions](/docs/api/storefront/latest/queries/product#returns-Product.fields.variantBySelectedOptions.arguments.selectedOptions)selectedOptions•[[SelectedOptionInput!]!](/docs/api/storefront/latest/input-objects/SelectedOptionInput)requiredThe input fields used for a selected option.

The input must not contain more than `250` values.

Show input fields[Anchor to ignoreUnknownOptions](/docs/api/storefront/latest/queries/product#returns-Product.fields.variantBySelectedOptions.arguments.ignoreUnknownOptions)ignoreUnknownOptions•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseWhether to ignore unknown product options.

[Anchor to caseInsensitiveMatch](/docs/api/storefront/latest/queries/product#returns-Product.fields.variantBySelectedOptions.arguments.caseInsensitiveMatch)caseInsensitiveMatch•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseWhether to perform case insensitive match on option names and values.

[Anchor to variants](/docs/api/storefront/latest/queries/product#returns-Product.fields.variants)variants•[ProductVariantConnection!](/docs/api/storefront/latest/connections/ProductVariantConnection)non-nullA list of [variants](/docs/api/storefront/latest/objects/ProductVariant) that are associated with the product.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/queries/product#returns-Product.fields.variants.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/queries/product#returns-Product.fields.variants.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/queries/product#returns-Product.fields.variants.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/queries/product#returns-Product.fields.variants.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/queries/product#returns-Product.fields.variants.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/storefront/latest/queries/product#returns-Product.fields.variants.arguments.sortKey)sortKey•[ProductVariantSortKeys](/docs/api/storefront/latest/enums/ProductVariantSortKeys)Default:POSITIONSort the underlying list by the given key.

Show enum values[Anchor to variantsCount](/docs/api/storefront/latest/queries/product#returns-Product.fields.variantsCount)variantsCount•[Count](/docs/api/storefront/latest/objects/Count)The number of [variants](/docs/api/storefront/latest/objects/ProductVariant) that are associated with the product.

Show fields[Anchor to vendor](/docs/api/storefront/latest/queries/product#returns-Product.fields.vendor)vendor•[String!](/docs/api/storefront/latest/scalars/String)non-nullThe name of the product's vendor.

Was this section helpful?YesNo## Examples- ### Load products which are published in a given context#### DescriptionThe Storefront API will automatically limit your query to products

that are published in any applicable catalogs. Unpublished

products will behave just like they were archived or deleted: they

will be omitted from connections and not found when queried by

handle or ID. Use the `@inContext` directive to set the context

explicitly; if omitted, the primary market will be used.

> Note:

If your app is a sales channel to which products can be published,

then the Storefront API will only return products that are

published both to your sales channel _and_ the market you’re

querying for.

In this example, the merchant has restricted their alarm clock

from sale in the United Kingdom by unpublishing it from that

market’s catalog. That product field returns `null` and that

product is not included in the `products` connection response.

#### Query```

query Products @inContext(country: GB) {

woolSweater: product(handle: "wool-sweater") {

title

}

alarmClock: product(handle: "alarm-clock") {

title

}

products(first: 2) {

nodes {

title

}

}

}

```#### cURL```

curl -X POST \

https://your-development-store.myshopify.com/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

-H 'X-Shopify-Storefront-Access-Token: {storefront_access_token}' \

-d '{

"query": "query Products @inContext(country: GB) { woolSweater: product(handle: \"wool-sweater\") { title } alarmClock: product(handle: \"alarm-clock\") { title } products(first: 2) { nodes { title } } }"

}'

```#### React Router```

import { unauthenticated } from "../shopify.server";

export const loader = async () => {

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query Products @inContext(country: GB) {

woolSweater: product(handle: "wool-sweater") {

title

}

alarmClock: product(handle: "alarm-clock") {

title

}

products(first: 2) {

nodes {

title

}

}

}`,

);

const json = await response.json();

return json.data;

}

```#### Node.js```

const client = new shopify.clients.Storefront({

domain: 'your-development-store.myshopify.com',

storefrontAccessToken,

});

const data = await client.query({

data: `query Products @inContext(country: GB) {

woolSweater: product(handle: "wool-sweater") {

title

}

alarmClock: product(handle: "alarm-clock") {

title

}

products(first: 2) {

nodes {

title

}

}

}`,

});

```#### Response```

{

"woolSweater": {

"title": "Wool sweater"

},

"alarmClock": null,

"products": {

"nodes": [

{

"title": "Wool sweater"

}

]

}

}

```- ### Load translated and localized content for a product#### DescriptionBy adding the `@inContext` directive to your query, you can access localized and translated content.#### Query```

query ProductTitle @inContext(country: CA, language: FR) {

product(handle: "wool-sweater") {

title

description

}

}

```#### cURL```

curl -X POST \

https://your-development-store.myshopify.com/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

-H 'X-Shopify-Storefront-Access-Token: {storefront_access_token}' \

-d '{

"query": "query ProductTitle @inContext(country: CA, language: FR) { product(handle: \"wool-sweater\") { title description } }"

}'

```#### React Router```

import { unauthenticated } from "../shopify.server";

export const loader = async () => {

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query ProductTitle @inContext(country: CA, language: FR) {

product(handle: "wool-sweater") {

title

description

}

}`,

);

const json = await response.json();

return json.data;

}

```#### Node.js```

const client = new shopify.clients.Storefront({

domain: 'your-development-store.myshopify.com',

storefrontAccessToken,

});

const data = await client.query({

data: `query ProductTitle @inContext(country: CA, language: FR) {

product(handle: "wool-sweater") {

title

description

}

}`,

});

```#### Response```

{

"product": {

"title": "Chandail en laine",

"description": "C’est très chaud!"

}

}

```- ### Retrieve local prices for a product#### DescriptionBy adding the `@inContext` directive to your query, you can access local pricing for a specified country. These prices are returned in the currency configured for the country in Markets settings. They may be calculated from the base variant prices, or provided by the merchant as fixed local prices.#### Query```

query ProductPricing @inContext(country: CA) {

product(handle: "wool-sweater") {

variants(first: 1) {

nodes {

price {

amount

currencyCode

}

}

}

}

}

```#### cURL```

curl -X POST \

https://your-development-store.myshopify.com/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

-H 'X-Shopify-Storefront-Access-Token: {storefront_access_token}' \

-d '{

"query": "query ProductPricing @inContext(country: CA) { product(handle: \"wool-sweater\") { variants(first: 1) { nodes { price { amount currencyCode } } } } }"

}'

```#### React Router```

import { unauthenticated } from "../shopify.server";

export const loader = async () => {

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query ProductPricing @inContext(country: CA) {

product(handle: "wool-sweater") {

variants(first: 1) {

nodes {

price {

amount

currencyCode

}

}

}

}

}`,

);

const json = await response.json();

return json.data;

}

```#### Node.js```

const client = new shopify.clients.Storefront({

domain: 'your-development-store.myshopify.com',

storefrontAccessToken,

});

const data = await client.query({

data: `query ProductPricing @inContext(country: CA) {

product(handle: "wool-sweater") {

variants(first: 1) {

nodes {

price {

amount

currencyCode

}

}

}

}

}`,

});

```#### Response```

{

"product": {

"variants": {

"nodes": [

{

"price": {

"amount": "90.0",

"currencyCode": "CAD"

}

}

]

}

}

}

```## ExamplesLoad products which are published in a given contextHide contentGQLcURLReact RouterNode.jsShow description[Open in GraphiQL](http://localhost:3457/graphiql?query=query%20Products%20%40inContext(country%3A%20GB)%20%7B%0A%20%20woolSweater%3A%20product(handle%3A%20%22wool-sweater%22)%20%7B%0A%20%20%20%20title%0A%20%20%7D%0A%20%20alarmClock%3A%20product(handle%3A%20%22alarm-clock%22)%20%7B%0A%20%20%20%20title%0A%20%20%7D%0A%20%20products(first%3A%202)%20%7B%0A%20%20%20%20nodes%20%7B%0A%20%20%20%20%20%20title%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D)Copy9912345678910111213141516171819202122232425›⌄import { unauthenticated } from "../shopify.server";export const loader = async () => {  const { storefront } = await unauthenticated.storefront(    'your-development-store.myshopify.com'  );  const response = await storefront.graphql(    `#graphql  query Products @inContext(country: GB) {    woolSweater: product(handle: "wool-sweater") {      title    }    alarmClock: product(handle: "alarm-clock") {      title    }    products(first: 2) {      nodes {        title      }    }  }`,  );  const json = await response.json();  return json.data;}GQL```

query Products @inContext(country: GB) {

woolSweater: product(handle: "wool-sweater") {

title

}

alarmClock: product(handle: "alarm-clock") {

title

}

products(first: 2) {

nodes {

title

}

}

}

```cURL```

curl -X POST \

https://your-development-store.myshopify.com/api/2026-01/graphql.json \

-H 'Content-Type: application/json' \

-H 'X-Shopify-Storefront-Access-Token: {storefront_access_token}' \

-d '{

"query": "query Products @inContext(country: GB) { woolSweater: product(handle: \"wool-sweater\") { title } alarmClock: product(handle: \"alarm-clock\") { title } products(first: 2) { nodes { title } } }"

}'

```React Router```

import { unauthenticated } from "../shopify.server";

export const loader = async () => {

const { storefront } = await unauthenticated.storefront(

'your-development-store.myshopify.com'

);

const response = await storefront.graphql(

`#graphql

query Products @inContext(country: GB) {

woolSweater: product(handle: "wool-sweater") {

title

}

alarmClock: product(handle: "alarm-clock") {

title

}

products(first: 2) {

nodes {

title

}

}

}`,

);

const json = await response.json();

return json.data;

}

```Node.js```

const client = new shopify.clients.Storefront({

domain: 'your-development-store.myshopify.com',

storefrontAccessToken,

});

const data = await client.query({

data: `query Products @inContext(country: GB) {

woolSweater: product(handle: "wool-sweater") {

title

}

alarmClock: product(handle: "alarm-clock") {

title

}

products(first: 2) {

nodes {

title

}

}

}`,

});

```Hide content## ResponseJSON9912345678910111213›⌄⌄⌄⌄⌄{  "woolSweater": {    "title": "Wool sweater"  },  "alarmClock": null,  "products": {    "nodes": [      {        "title": "Wool sweater"      }    ]  }}### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)