---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/storefront/latest/objects/Product",
    "fetched_at": "2026-02-10T13:41:00.211293",
    "status": 200,
    "size_bytes": 490796
  },
  "metadata": {
    "title": "Product - Storefront API",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "objects",
    "component": "Product"
  }
}
---

# Product - Storefront API

Choose a version:unstable 2026-04 release candidate2026-01 latest2025-10 2025-07 2025-04 2026-01latest[Anchor to Product](/docs/api/storefront/latest/objects/Product#top)# ProductobjectAsk assistantRequires `unauthenticated_read_product_listings` access scope.

The `Product` object lets you manage products in a merchant’s store.

Products are the goods and services that merchants offer to customers.

They can include various details such as title, description, price, images, and options such as size or color.

You can use [product variants](/docs/api/storefront/latest/objects/ProductVariant)

to create or update different versions of the same product.

You can also add or update product [media](/docs/api/storefront/latest/interfaces/Media).

Products can be organized by grouping them into a [collection](/docs/api/storefront/latest/objects/Collection).

Learn more about working with [products and collections](/docs/storefronts/headless/building-with-the-storefront-api/products-collections).

## [Anchor to Fields](/docs/api/storefront/latest/objects/Product#fields)Fields- adjacentVariants ([ProductVariant!]!)- availableForSale (Boolean!)- category (TaxonomyCategory)- collections (CollectionConnection!)- compareAtPriceRange (ProductPriceRange!)- createdAt (DateTime!)- description (String!)- descriptionHtml (HTML!)- encodedVariantAvailability (String)- encodedVariantExistence (String)- featuredImage (Image)- handle (String!)- id (ID!)- images (ImageConnection!)- isGiftCard (Boolean!)- media (MediaConnection!)- metafield (Metafield)- metafields ([Metafield]!)- onlineStoreUrl (URL)- options ([ProductOption!]!)- priceRange (ProductPriceRange!)- productType (String!)- publishedAt (DateTime!)- requiresSellingPlan (Boolean!)- selectedOrFirstAvailableVariant (ProductVariant)- sellingPlanGroups (SellingPlanGroupConnection!)- seo (SEO!)- tags ([String!]!)- title (String!)- totalInventory (Int)- trackingParameters (String)- updatedAt (DateTime!)- variantBySelectedOptions (ProductVariant)- variants (ProductVariantConnection!)- variantsCount (Count)- vendor (String!)[Anchor to adjacentVariants](/docs/api/storefront/latest/objects/Product#field-Product.fields.adjacentVariants)adjacentVariants•[[ProductVariant!]!](/docs/api/storefront/latest/objects/ProductVariant)non-nullA list of variants whose selected options differ with the provided selected options by one, ordered by variant id.

If selected options are not provided, adjacent variants to the first available variant is returned.

Note that this field returns an array of variants. In most cases, the number of variants in this array will be low.

However, with a low number of options and a high number of values per option, the number of variants returned

here can be high. In such cases, it recommended to avoid using this field.

This list of variants can be used in combination with the `options` field to build a rich variant picker that

includes variant availability or other variant information.

Show fields### Arguments[Anchor to selectedOptions](/docs/api/storefront/latest/objects/Product#field-Product.fields.adjacentVariants.arguments.selectedOptions)selectedOptions•[[SelectedOptionInput!]](/docs/api/storefront/latest/input-objects/SelectedOptionInput)The input fields used for a selected option.

The input must not contain more than `250` values.

Show input fields[Anchor to ignoreUnknownOptions](/docs/api/storefront/latest/objects/Product#field-Product.fields.adjacentVariants.arguments.ignoreUnknownOptions)ignoreUnknownOptions•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:trueWhether to ignore product options that are not present on the requested product.

[Anchor to caseInsensitiveMatch](/docs/api/storefront/latest/objects/Product#field-Product.fields.adjacentVariants.arguments.caseInsensitiveMatch)caseInsensitiveMatch•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseWhether to perform case insensitive match on option names and values.

[Anchor to availableForSale](/docs/api/storefront/latest/objects/Product#field-Product.fields.availableForSale)availableForSale•[Boolean!](/docs/api/storefront/latest/scalars/Boolean)non-nullIndicates if at least one product variant is available for sale.

[Anchor to category](/docs/api/storefront/latest/objects/Product#field-Product.fields.category)category•[TaxonomyCategory](/docs/api/storefront/latest/objects/TaxonomyCategory)The category of a product from [Shopify's Standard Product Taxonomy](https://shopify.github.io/product-taxonomy/releases/unstable/?categoryId=sg-4-17-2-17).

Show fields[Anchor to collections](/docs/api/storefront/latest/objects/Product#field-Product.fields.collections)collections•[CollectionConnection!](/docs/api/storefront/latest/connections/CollectionConnection)non-nullA list of [collections](/docs/api/storefront/latest/objects/Collection) that include the product.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/objects/Product#field-Product.fields.collections.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/objects/Product#field-Product.fields.collections.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/objects/Product#field-Product.fields.collections.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/objects/Product#field-Product.fields.collections.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/objects/Product#field-Product.fields.collections.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to compareAtPriceRange](/docs/api/storefront/latest/objects/Product#field-Product.fields.compareAtPriceRange)compareAtPriceRange•[ProductPriceRange!](/docs/api/storefront/latest/objects/ProductPriceRange)non-nullThe [compare-at price range](https://help.shopify.com/manual/products/details/product-pricing/sale-pricing) of the product in the shop's default currency.

Show fields[Anchor to createdAt](/docs/api/storefront/latest/objects/Product#field-Product.fields.createdAt)createdAt•[DateTime!](/docs/api/storefront/latest/scalars/DateTime)non-nullThe date and time when the product was created.

[Anchor to description](/docs/api/storefront/latest/objects/Product#field-Product.fields.description)description•[String!](/docs/api/storefront/latest/scalars/String)non-nullA single-line description of the product, with [HTML tags](https://developer.mozilla.org/en-US/docs/Web/HTML) removed.

Show arguments### Arguments[Anchor to truncateAt](/docs/api/storefront/latest/objects/Product#field-Product.fields.description.arguments.truncateAt)truncateAt•[Int](/docs/api/storefront/latest/scalars/Int)Truncates a string after the given length.

[Anchor to descriptionHtml](/docs/api/storefront/latest/objects/Product#field-Product.fields.descriptionHtml)descriptionHtml•[HTML!](/docs/api/storefront/latest/scalars/HTML)non-nullThe description of the product, with

HTML tags. For example, the description might include

bold `<strong></strong>` and italic `<i></i>` text.

[Anchor to encodedVariantAvailability](/docs/api/storefront/latest/objects/Product#field-Product.fields.encodedVariantAvailability)encodedVariantAvailability•[String](/docs/api/storefront/latest/scalars/String)An encoded string containing all option value combinations

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

[Anchor to encodedVariantExistence](/docs/api/storefront/latest/objects/Product#field-Product.fields.encodedVariantExistence)encodedVariantExistence•[String](/docs/api/storefront/latest/scalars/String)An encoded string containing all option value combinations with a corresponding variant.

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

[Anchor to featuredImage](/docs/api/storefront/latest/objects/Product#field-Product.fields.featuredImage)featuredImage•[Image](/docs/api/storefront/latest/objects/Image)The featured image for the product.

This field is functionally equivalent to `images(first: 1)`.

Show fields[Anchor to handle](/docs/api/storefront/latest/objects/Product#field-Product.fields.handle)handle•[String!](/docs/api/storefront/latest/scalars/String)non-nullA unique, human-readable string of the product's title.

A handle can contain letters, hyphens (`-`), and numbers, but no spaces.

The handle is used in the online store URL for the product.

[Anchor to id](/docs/api/storefront/latest/objects/Product#field-Product.fields.id)id•[ID!](/docs/api/storefront/latest/scalars/ID)non-nullA globally-unique ID.

[Anchor to images](/docs/api/storefront/latest/objects/Product#field-Product.fields.images)images•[ImageConnection!](/docs/api/storefront/latest/connections/ImageConnection)non-nullList of images associated with the product.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/objects/Product#field-Product.fields.images.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/objects/Product#field-Product.fields.images.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/objects/Product#field-Product.fields.images.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/objects/Product#field-Product.fields.images.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/objects/Product#field-Product.fields.images.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/storefront/latest/objects/Product#field-Product.fields.images.arguments.sortKey)sortKey•[ProductImageSortKeys](/docs/api/storefront/latest/enums/ProductImageSortKeys)Default:POSITIONSort the underlying list by the given key.

Show enum values[Anchor to isGiftCard](/docs/api/storefront/latest/objects/Product#field-Product.fields.isGiftCard)isGiftCard•[Boolean!](/docs/api/storefront/latest/scalars/Boolean)non-nullWhether the product is a gift card.

[Anchor to media](/docs/api/storefront/latest/objects/Product#field-Product.fields.media)media•[MediaConnection!](/docs/api/storefront/latest/connections/MediaConnection)non-nullThe [media](/docs/apps/build/online-store/product-media) that are associated with the product. Valid media are images, 3D models, videos.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/objects/Product#field-Product.fields.media.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/objects/Product#field-Product.fields.media.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/objects/Product#field-Product.fields.media.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/objects/Product#field-Product.fields.media.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/objects/Product#field-Product.fields.media.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/storefront/latest/objects/Product#field-Product.fields.media.arguments.sortKey)sortKey•[ProductMediaSortKeys](/docs/api/storefront/latest/enums/ProductMediaSortKeys)Default:POSITIONSort the underlying list by the given key.

Show enum values[Anchor to metafield](/docs/api/storefront/latest/objects/Product#field-Product.fields.metafield)metafield•[Metafield](/docs/api/storefront/latest/objects/Metafield) Token access requiredA [custom field](https://shopify.dev/docs/apps/build/custom-data), including its `namespace` and `key`, that's associated with a Shopify resource for the purposes of adding and storing additional information.

Show fields### Arguments[Anchor to namespace](/docs/api/storefront/latest/objects/Product#field-Product.fields.metafield.arguments.namespace)namespace•[String](/docs/api/storefront/latest/scalars/String)The container the metafield belongs to. If omitted, the app-reserved namespace will be used.

[Anchor to key](/docs/api/storefront/latest/objects/Product#field-Product.fields.metafield.arguments.key)key•[String!](/docs/api/storefront/latest/scalars/String)requiredThe identifier for the metafield.

[Anchor to metafields](/docs/api/storefront/latest/objects/Product#field-Product.fields.metafields)metafields•[[Metafield]!](/docs/api/storefront/latest/objects/Metafield)non-null Token access requiredA list of [custom fields](/docs/apps/build/custom-data) that a merchant associates with a Shopify resource.

Show fields### Arguments[Anchor to identifiers](/docs/api/storefront/latest/objects/Product#field-Product.fields.metafields.arguments.identifiers)identifiers•[[HasMetafieldsIdentifier!]!](/docs/api/storefront/latest/input-objects/HasMetafieldsIdentifier)requiredThe list of metafields to retrieve by namespace and key.

The input must not contain more than `250` values.

Show input fields[Anchor to onlineStoreUrl](/docs/api/storefront/latest/objects/Product#field-Product.fields.onlineStoreUrl)onlineStoreUrl•[URL](/docs/api/storefront/latest/scalars/URL)The product's URL on the online store.

If `null`, then the product isn't published to the online store sales channel.

[Anchor to options](/docs/api/storefront/latest/objects/Product#field-Product.fields.options)options•[[ProductOption!]!](/docs/api/storefront/latest/objects/ProductOption)non-nullA list of product options. The limit is defined by the [shop's resource limits for product options](/docs/api/admin-graphql/latest/objects/Shop#field-resourcelimits) (`Shop.resourceLimits.maxProductOptions`).

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/objects/Product#field-Product.fields.options.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Truncate the array result to this size.

[Anchor to priceRange](/docs/api/storefront/latest/objects/Product#field-Product.fields.priceRange)priceRange•[ProductPriceRange!](/docs/api/storefront/latest/objects/ProductPriceRange)non-nullThe minimum and maximum prices of a product, expressed in decimal numbers.

For example, if the product is priced between $10.00 and $50.00,

then the price range is $10.00 - $50.00.

Show fields[Anchor to productType](/docs/api/storefront/latest/objects/Product#field-Product.fields.productType)productType•[String!](/docs/api/storefront/latest/scalars/String)non-nullThe [product type](https://help.shopify.com/manual/products/details/product-type)

that merchants define.

[Anchor to publishedAt](/docs/api/storefront/latest/objects/Product#field-Product.fields.publishedAt)publishedAt•[DateTime!](/docs/api/storefront/latest/scalars/DateTime)non-nullThe date and time when the product was published to the channel.

[Anchor to requiresSellingPlan](/docs/api/storefront/latest/objects/Product#field-Product.fields.requiresSellingPlan)requiresSellingPlan•[Boolean!](/docs/api/storefront/latest/scalars/Boolean)non-nullWhether the product can only be purchased with a [selling plan](/docs/apps/build/purchase-options/subscriptions/selling-plans). Products that are sold on subscription (`requiresSellingPlan: true`) can be updated only for online stores. If you update a product to be subscription-only (`requiresSellingPlan:false`), then the product is unpublished from all channels, except the online store.

[Anchor to selectedOrFirstAvailableVariant](/docs/api/storefront/latest/objects/Product#field-Product.fields.selectedOrFirstAvailableVariant)selectedOrFirstAvailableVariant•[ProductVariant](/docs/api/storefront/latest/objects/ProductVariant)Find an active product variant based on selected options, availability or the first variant.

All arguments are optional. If no selected options are provided, the first available variant is returned.

If no variants are available, the first variant is returned.

Show fields### Arguments[Anchor to selectedOptions](/docs/api/storefront/latest/objects/Product#field-Product.fields.selectedOrFirstAvailableVariant.arguments.selectedOptions)selectedOptions•[[SelectedOptionInput!]](/docs/api/storefront/latest/input-objects/SelectedOptionInput)The input fields used for a selected option.

The input must not contain more than `250` values.

Show input fields[Anchor to ignoreUnknownOptions](/docs/api/storefront/latest/objects/Product#field-Product.fields.selectedOrFirstAvailableVariant.arguments.ignoreUnknownOptions)ignoreUnknownOptions•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:trueWhether to ignore unknown product options.

[Anchor to caseInsensitiveMatch](/docs/api/storefront/latest/objects/Product#field-Product.fields.selectedOrFirstAvailableVariant.arguments.caseInsensitiveMatch)caseInsensitiveMatch•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseWhether to perform case insensitive match on option names and values.

[Anchor to sellingPlanGroups](/docs/api/storefront/latest/objects/Product#field-Product.fields.sellingPlanGroups)sellingPlanGroups•[SellingPlanGroupConnection!](/docs/api/storefront/latest/connections/SellingPlanGroupConnection)non-nullA list of all [selling plan groups](/docs/apps/build/purchase-options/subscriptions/selling-plans/build-a-selling-plan) that are associated with the product either directly, or through the product's variants.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/objects/Product#field-Product.fields.sellingPlanGroups.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/objects/Product#field-Product.fields.sellingPlanGroups.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/objects/Product#field-Product.fields.sellingPlanGroups.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/objects/Product#field-Product.fields.sellingPlanGroups.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/objects/Product#field-Product.fields.sellingPlanGroups.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to seo](/docs/api/storefront/latest/objects/Product#field-Product.fields.seo)seo•[SEO!](/docs/api/storefront/latest/objects/SEO)non-nullThe [SEO title and description](https://help.shopify.com/manual/promoting-marketing/seo/adding-keywords)

that are associated with a product.

Show fields[Anchor to tags](/docs/api/storefront/latest/objects/Product#field-Product.fields.tags)tags•[[String!]!](/docs/api/storefront/latest/scalars/String)non-nullA comma-separated list of searchable keywords that are

associated with the product. For example, a merchant might apply the `sports`

and `summer` tags to products that are associated with sportwear for summer.

Updating `tags` overwrites any existing tags that were previously added to the product.

To add new tags without overwriting existing tags,

use the GraphQL Admin API's [`tagsAdd`](/docs/api/admin-graphql/latest/mutations/tagsadd)

mutation.

[Anchor to title](/docs/api/storefront/latest/objects/Product#field-Product.fields.title)title•[String!](/docs/api/storefront/latest/scalars/String)non-nullThe name for the product that displays to customers. The title is used to construct the product's handle.

For example, if a product is titled "Black Sunglasses", then the handle is `black-sunglasses`.

[Anchor to totalInventory](/docs/api/storefront/latest/objects/Product#field-Product.fields.totalInventory)totalInventory•[Int](/docs/api/storefront/latest/scalars/Int) Token access requiredThe quantity of inventory that's in stock.

[Anchor to trackingParameters](/docs/api/storefront/latest/objects/Product#field-Product.fields.trackingParameters)trackingParameters•[String](/docs/api/storefront/latest/scalars/String)URL parameters to be added to a page URL to track the origin of on-site search traffic for [analytics reporting](https://help.shopify.com/manual/reports-and-analytics/shopify-reports/report-types/default-reports/behaviour-reports). Returns a result when accessed through the [search](/docs/api/storefront/2026-01/queries/search) or [predictiveSearch](/docs/api/storefront/2026-01/queries/predictiveSearch) queries, otherwise returns null.

[Anchor to updatedAt](/docs/api/storefront/latest/objects/Product#field-Product.fields.updatedAt)updatedAt•[DateTime!](/docs/api/storefront/latest/scalars/DateTime)non-nullThe date and time when the product was last modified.

A product's `updatedAt` value can change for different reasons. For example, if an order

is placed for a product that has inventory tracking set up, then the inventory adjustment

is counted as an update.

[Anchor to variantBySelectedOptions](/docs/api/storefront/latest/objects/Product#field-Product.fields.variantBySelectedOptions)variantBySelectedOptions•[ProductVariant](/docs/api/storefront/latest/objects/ProductVariant)Find a product’s variant based on its selected options.

This is useful for converting a user’s selection of product options into a single matching variant.

If there is not a variant for the selected options, `null` will be returned.

Show fields### Arguments[Anchor to selectedOptions](/docs/api/storefront/latest/objects/Product#field-Product.fields.variantBySelectedOptions.arguments.selectedOptions)selectedOptions•[[SelectedOptionInput!]!](/docs/api/storefront/latest/input-objects/SelectedOptionInput)requiredThe input fields used for a selected option.

The input must not contain more than `250` values.

Show input fields[Anchor to ignoreUnknownOptions](/docs/api/storefront/latest/objects/Product#field-Product.fields.variantBySelectedOptions.arguments.ignoreUnknownOptions)ignoreUnknownOptions•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseWhether to ignore unknown product options.

[Anchor to caseInsensitiveMatch](/docs/api/storefront/latest/objects/Product#field-Product.fields.variantBySelectedOptions.arguments.caseInsensitiveMatch)caseInsensitiveMatch•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseWhether to perform case insensitive match on option names and values.

[Anchor to variants](/docs/api/storefront/latest/objects/Product#field-Product.fields.variants)variants•[ProductVariantConnection!](/docs/api/storefront/latest/connections/ProductVariantConnection)non-nullA list of [variants](/docs/api/storefront/latest/objects/ProductVariant) that are associated with the product.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/objects/Product#field-Product.fields.variants.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/objects/Product#field-Product.fields.variants.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/objects/Product#field-Product.fields.variants.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/objects/Product#field-Product.fields.variants.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/objects/Product#field-Product.fields.variants.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/storefront/latest/objects/Product#field-Product.fields.variants.arguments.sortKey)sortKey•[ProductVariantSortKeys](/docs/api/storefront/latest/enums/ProductVariantSortKeys)Default:POSITIONSort the underlying list by the given key.

Show enum values[Anchor to variantsCount](/docs/api/storefront/latest/objects/Product#field-Product.fields.variantsCount)variantsCount•[Count](/docs/api/storefront/latest/objects/Count)The number of [variants](/docs/api/storefront/latest/objects/ProductVariant) that are associated with the product.

Show fields[Anchor to vendor](/docs/api/storefront/latest/objects/Product#field-Product.fields.vendor)vendor•[String!](/docs/api/storefront/latest/scalars/String)non-nullThe name of the product's vendor.

Was this section helpful?YesNo## Map### Fields and connections with this object- {}[Collection.products](/docs/api/storefront/latest/objects/Collection#field-Collection.fields.products)- {}[PredictiveSearchResult.products](/docs/api/storefront/latest/objects/PredictiveSearchResult#field-PredictiveSearchResult.fields.products)- <->[ProductConnection.nodes](/docs/api/storefront/latest/connections/ProductConnection#returns-nodes)- {}[ProductEdge.node](/docs/api/storefront/latest/objects/ProductEdge#field-ProductEdge.fields.node)- {}[ProductVariant.product](/docs/api/storefront/latest/objects/ProductVariant#field-ProductVariant.fields.product)### Possible type in- [MenuItemResource](/docs/api/storefront/latest/unions/MenuItemResource)- [MetafieldParentResource](/docs/api/storefront/latest/unions/MetafieldParentResource)- [MetafieldReference](/docs/api/storefront/latest/unions/MetafieldReference)- [SearchResultItem](/docs/api/storefront/latest/unions/SearchResultItem)## [Anchor to Queries](/docs/api/storefront/latest/objects/Product#queries)Queries- product (Product)- productRecommendations ([Product!])- products (ProductConnection!)- productByHandle (Product): deprecated[Anchor to product](/docs/api/storefront/latest/objects/Product#query-product)[product](/docs/api/storefront/latest/queries/product)•queryFetch a specific `Product` by one of its unique attributes.

Show fields### Arguments[Anchor to id](/docs/api/storefront/latest/objects/Product#query-product.arguments.id)id•[ID](/docs/api/storefront/latest/scalars/ID)The ID of the `Product`.

[Anchor to handle](/docs/api/storefront/latest/objects/Product#query-product.arguments.handle)handle•[String](/docs/api/storefront/latest/scalars/String)The handle of the `Product`.

[Anchor to productRecommendations](/docs/api/storefront/latest/objects/Product#query-productRecommendations)[productRecommendations](/docs/api/storefront/latest/queries/productRecommendations)•queryFind recommended products related to a given `product_id`.

To learn more about how recommendations are generated, see

[*Showing product recommendations on product pages*](https://help.shopify.com/themes/development/recommended-products).

Show fields### Arguments[Anchor to productId](/docs/api/storefront/latest/objects/Product#query-productRecommendations.arguments.productId)productId•[ID](/docs/api/storefront/latest/scalars/ID)The id of the product.

[Anchor to productHandle](/docs/api/storefront/latest/objects/Product#query-productRecommendations.arguments.productHandle)productHandle•[String](/docs/api/storefront/latest/scalars/String)The handle of the product.

[Anchor to intent](/docs/api/storefront/latest/objects/Product#query-productRecommendations.arguments.intent)intent•[ProductRecommendationIntent](/docs/api/storefront/latest/enums/ProductRecommendationIntent)Default:RELATEDThe recommendation intent that is used to generate product recommendations. You can use intent to generate product recommendations on various pages across the channels, according to different strategies.

Show enum values[Anchor to products](/docs/api/storefront/latest/objects/Product#query-products)[products](/docs/api/storefront/latest/queries/products)•queryReturns a list of the shop's products. For storefront search, use the [`search`](https://shopify.dev/docs/api/storefront/latest/queries/search) query.

Show fields### Arguments[Anchor to first](/docs/api/storefront/latest/objects/Product#query-products.arguments.first)first•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the first `n` elements from the list.

[Anchor to after](/docs/api/storefront/latest/objects/Product#query-products.arguments.after)after•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come after the specified cursor.

[Anchor to last](/docs/api/storefront/latest/objects/Product#query-products.arguments.last)last•[Int](/docs/api/storefront/latest/scalars/Int)Returns up to the last `n` elements from the list.

[Anchor to before](/docs/api/storefront/latest/objects/Product#query-products.arguments.before)before•[String](/docs/api/storefront/latest/scalars/String)Returns the elements that come before the specified cursor.

[Anchor to reverse](/docs/api/storefront/latest/objects/Product#query-products.arguments.reverse)reverse•[Boolean](/docs/api/storefront/latest/scalars/Boolean)Default:falseReverse the order of the underlying list.

[Anchor to sortKey](/docs/api/storefront/latest/objects/Product#query-products.arguments.sortKey)sortKey•[ProductSortKeys](/docs/api/storefront/latest/enums/ProductSortKeys)Default:IDSort the underlying list by the given key.

Show enum values[Anchor to query](/docs/api/storefront/latest/objects/Product#query-products.arguments.query)query•[String](/docs/api/storefront/latest/scalars/String)You can apply one or multiple filters to a query.

Learn more about [Shopify API search syntax](https://shopify.dev/api/usage/search-syntax).

Show filters[Anchor to ](/docs/api/storefront/latest/objects/Product#argument-query-filter-available_for_sale)available_for_sale•Filter by products that have at least one product variant available for sale.

[Anchor to ](/docs/api/storefront/latest/objects/Product#argument-query-filter-created_at)created_at•Filter by the date and time when the product was created.

Example:- `created_at:>'2020-10-21T23:39:20Z'`- `created_at:<now`- `created_at:<=2024`[Anchor to ](/docs/api/storefront/latest/objects/Product#argument-query-filter-product_type)product_type•Filter by a comma-separated list of [product types](https://help.shopify.com/en/manual/products/details/product-type).

Example:- `product_type:snowboard`[Anchor to ](/docs/api/storefront/latest/objects/Product#argument-query-filter-tag)tag•Filter products by the product [`tags`](https://shopify.dev/docs/api/storefront/latest/objects/Product#field-tags) field.

Example:- `tag:my_tag`[Anchor to ](/docs/api/storefront/latest/objects/Product#argument-query-filter-tag_not)tag_not•Filter by products that don't have the specified product [tags](https://shopify.dev/docs/api/storefront/latest/objects/Product#field-tags).

Example:- `tag_not:my_tag`[Anchor to ](/docs/api/storefront/latest/objects/Product#argument-query-filter-title)title•Filter by the product [`title`](https://shopify.dev/docs/api/storefront/latest/objects/Product#field-title) field.

Example:- `title:The Minimal Snowboard`[Anchor to ](/docs/api/storefront/latest/objects/Product#argument-query-filter-updated_at)updated_at•Filter by the date and time when the product was last updated.

Example:- `updated_at:>'2020-10-21T23:39:20Z'`- `updated_at:<now`- `updated_at:<=2024`[Anchor to ](/docs/api/storefront/latest/objects/Product#argument-query-filter-variants.price)variants.price•Filter by the price of the product's variants.

[Anchor to ](/docs/api/storefront/latest/objects/Product#argument-query-filter-vendor)vendor•Filter by the product [`vendor`](https://shopify.dev/docs/api/storefront/latest/objects/Product#field-vendor) field.

Example:- `vendor:Snowdevil`- `vendor:Snowdevil OR vendor:Icedevil`[Anchor to productByHandle](/docs/api/storefront/latest/objects/Product#query-productByHandle)[productByHandle](/docs/api/storefront/latest/queries/productByHandle)•queryDeprecatedShow fields### Arguments[Anchor to handle](/docs/api/storefront/latest/objects/Product#query-productByHandle.arguments.handle)handle•[String!](/docs/api/storefront/latest/scalars/String)requiredA unique, human-readable string of the product's title.

A handle can contain letters, hyphens (`-`), and numbers, but no spaces.

The handle is used in the online store URL for the product.

Was this section helpful?YesNo## <?>Product Queries### Queried by- <?>[product](/docs/api/storefront/latest/queries/product)- <?>[productRecommendations](/docs/api/storefront/latest/queries/productRecommendations)- <?>[products](/docs/api/storefront/latest/queries/products)Show deprecations## [Anchor to Interfaces](/docs/api/storefront/latest/objects/Product#interfaces)Interfaces- HasMetafields- Node- OnlineStorePublishable- Trackable[Anchor to HasMetafields](/docs/api/storefront/latest/objects/Product#interface-HasMetafields)[HasMetafields](/docs/api/storefront/latest/interfaces/HasMetafields)•interface[Anchor to Node](/docs/api/storefront/latest/objects/Product#interface-Node)[Node](/docs/api/storefront/latest/interfaces/Node)•interface[Anchor to OnlineStorePublishable](/docs/api/storefront/latest/objects/Product#interface-OnlineStorePublishable)[OnlineStorePublishable](/docs/api/storefront/latest/interfaces/OnlineStorePublishable)•interface[Anchor to Trackable](/docs/api/storefront/latest/objects/Product#interface-Trackable)[Trackable](/docs/api/storefront/latest/interfaces/Trackable)•interfaceWas this section helpful?YesNo## ||-Product Implements### Implements- ||-[HasMetafields](/docs/api/storefront/latest/interfaces/HasMetafields)- ||-[Node](/docs/api/storefront/latest/interfaces/Node)- ||-[OnlineStorePublishable](/docs/api/storefront/latest/interfaces/OnlineStorePublishable)- ||-[Trackable](/docs/api/storefront/latest/interfaces/Trackable)### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)