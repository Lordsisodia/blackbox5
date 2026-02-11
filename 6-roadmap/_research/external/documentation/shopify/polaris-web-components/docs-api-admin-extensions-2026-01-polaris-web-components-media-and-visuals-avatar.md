---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/media-and-visuals/avatar",
    "fetched_at": "2026-02-10T13:30:43.064788",
    "status": 200,
    "size_bytes": 300784
  },
  "metadata": {
    "title": "Avatar",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "media-and-visuals",
    "component": "avatar"
  }
}
---

# Avatar

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# AvatarAsk assistantShow a user’s profile image or initials in a compact, visual element.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/avatar#properties)Properties[Anchor to alt](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/avatar#properties-propertydetail-alt)alt**alt**string**string**An alternative text that describes the avatar for the reader to understand what it is about or identify the user the avatar belongs to.

[Anchor to initials](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/avatar#properties-propertydetail-initials)initials**initials**string**string**Initials to display in the avatar.

[Anchor to size](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/avatar#properties-propertydetail-size)size**size**"small" | "small-200" | "base" | "large" | "large-200"**"small" | "small-200" | "base" | "large" | "large-200"**Default: 'base'**Default: 'base'**Size of the avatar.

[Anchor to src](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/avatar#properties-propertydetail-src)src**src**string**string**The URL or path to the image.

Initials will be rendered as a fallback if `src` is not provided, fails to load or does not load quickly

## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/avatar#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/avatar#events-propertydetail-error)error**error**OnErrorEventHandler**OnErrorEventHandler**[Anchor to load](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/avatar#events-propertydetail-load)load**load**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy91<s-avatar alt="John Doe" initials="JD" />## Preview### Examples- #### Codejsx```

<s-avatar alt="John Doe" initials="JD" />

```html```

<s-avatar alt="John Doe" initials="JD"></s-avatar>

```- #### Basic usageDescriptionDisplays a customer avatar with their initials when no profile image is available.jsx```

<s-avatar initials="SC" alt="Sarah Chen" />

```html```

<s-avatar initials="SC" alt="Sarah Chen"></s-avatar>

```- #### Default avatar (no props)DescriptionShows a generic person icon placeholder when no user information is available.jsx```

<s-avatar alt="Customer" />

```html```

<s-avatar alt="Customer"></s-avatar>

```- #### With image source and fallbackDescriptionLoads a customer profile image with automatic fallback to initials if the image fails to load.jsx```

<s-avatar

src="/customers/profile-123.jpg"

initials="MR"

alt="Maria Rodriguez"

size="base"

/>

```html```

<s-avatar

src="/customers/profile-123.jpg"

initials="MR"

alt="Maria Rodriguez"

size="base"

></s-avatar>

```- #### Size variationsDescriptionDisplays customer and merchant avatars in different sizes for various interface contexts.jsx```

<s-stack direction="inline" gap="base">

<s-avatar initials="SC" alt="Store customer" size="small-200" />

<s-avatar initials="MR" alt="Merchant representative" size="small" />

<s-avatar initials="SM" alt="Store manager" size="base" />

<s-avatar initials="SF" alt="Staff member" size="large" />

<s-avatar initials="SO" alt="Store owner" size="large-200" />

</s-stack>

```html```

<s-stack direction="inline" gap="base">

<s-avatar initials="SC" alt="Store customer" size="small-200"></s-avatar>

<s-avatar initials="MR" alt="Merchant representative" size="small"></s-avatar>

<s-avatar initials="SM" alt="Store manager" size="base"></s-avatar>

<s-avatar initials="SF" alt="Staff member" size="large"></s-avatar>

<s-avatar initials="SO" alt="Store owner" size="large-200"></s-avatar>

</s-stack>

```- #### Long initials handlingDescriptionShows how the component handles store and business names of varying lengths in commerce contexts.jsx```

<s-stack direction="inline" gap="base">

<s-avatar initials="TC" alt="Tech customer" size="base" />

<s-avatar initials="VIP" alt="VIP customer store" size="base" />

<s-avatar initials="SHOP" alt="Shopify partner store" size="base" />

</s-stack>

```html```

<s-stack direction="inline" gap="base">

<s-avatar initials="TC" alt="Tech customer" size="base"></s-avatar>

<s-avatar initials="VIP" alt="VIP customer store" size="base"></s-avatar>

<s-avatar initials="SHOP" alt="Shopify partner store" size="base"></s-avatar>

</s-stack>

```- #### Color consistency demoDescriptionDemonstrates that identical initials always receive the same color assignment across different store types.jsx```

<s-stack direction="inline" gap="base">

<s-avatar initials="AB" alt="Apparel boutique" size="base" />

<s-avatar initials="CD" alt="Coffee direct" size="base" />

<s-avatar initials="EF" alt="Electronics franchise" size="base" />

<s-avatar initials="AB" alt="Art books store" size="base" />

{/* Note: Both AB avatars will have the same color */}

</s-stack>

```html```

<s-stack direction="inline" gap="base">

<s-avatar initials="AB" alt="Apparel boutique" size="base"></s-avatar>

<s-avatar initials="CD" alt="Coffee direct" size="base"></s-avatar>

<s-avatar initials="EF" alt="Electronics franchise" size="base"></s-avatar>

<s-avatar initials="AB" alt="Art books store" size="base"></s-avatar>

<!-- Note: Both AB avatars will have the same color -->

</s-stack>

```- #### Error handling exampleDescriptionShows automatic fallback to initials when customer or merchant profile images fail to load.jsx```

<s-avatar

src="/invalid-customer-photo.jpg"

initials="CS"

alt="Customer support"

/>

```html```

<s-avatar

src="/invalid-customer-photo.jpg"

initials="CS"

alt="Customer support"

></s-avatar>

<!-- Will display "CS" initials when image fails -->

```- #### In customer list contextDescriptionTypical usage pattern for displaying customer avatars in order lists or customer listings.jsx```

<s-stack gap="base">

<s-stack direction="inline" gap="small">

<s-avatar

src="/customers/merchant-alice.jpg"

initials="AJ"

alt="Alice's jewelry store"

size="small"

/>

<s-text>Alice's jewelry store</s-text>

</s-stack>

<s-stack direction="inline" gap="small">

<s-avatar initials="BP" alt="Bob's pet supplies" size="small" />

<s-text>Bob's pet supplies</s-text>

</s-stack>

<s-stack direction="inline" gap="small">

<s-avatar

src="/customers/charlie-cafe.jpg"

initials="CC"

alt="Charlie's coffee corner"

size="small"

/>

<s-text>Charlie's coffee corner</s-text>

</s-stack>

</s-stack>

```html```

<s-stack gap="base">

<s-stack direction="inline" gap="small">

<s-avatar

src="/customers/merchant-alice.jpg"

initials="AJ"

alt="Alice's jewelry store"

size="small"

></s-avatar>

<s-text>Alice's jewelry store</s-text>

</s-stack>

<s-stack direction="inline" gap="small">

<s-avatar initials="BP" alt="Bob's pet supplies" size="small"></s-avatar>

<s-text>Bob's pet supplies</s-text>

</s-stack>

<s-stack direction="inline" gap="small">

<s-avatar

src="/customers/charlie-cafe.jpg"

initials="CC"

alt="Charlie's coffee corner"

size="small"

></s-avatar>

<s-text>Charlie's coffee corner</s-text>

</s-stack>

</s-stack>

```- #### Staff member profilesDescriptionShows staff member avatars in different admin interface contexts.jsx```

<s-stack direction="inline" gap="large">

<s-avatar

src="/staff/manager-profile.jpg"

initials="SM"

alt="Store manager"

size="large"

/>

<s-avatar initials="CS" alt="Customer service rep" size="base" />

<s-avatar initials="FT" alt="Fulfillment team lead" size="small" />

</s-stack>

```html```

<s-stack direction="inline" gap="large">

<s-avatar

src="/staff/manager-profile.jpg"

initials="SM"

alt="Store manager"

size="large"

></s-avatar>

<s-avatar initials="CS" alt="Customer service rep" size="base"></s-avatar>

<s-avatar initials="FT" alt="Fulfillment team lead" size="small"></s-avatar>

</s-stack>

```- #### With Section componentDescriptionDemonstrates avatar integration with other admin-ui components in a merchant section layout.jsx```

<s-section>

<s-stack gap="base">

<s-stack direction="inline" gap="small">

<s-avatar

src="/merchants/premium-store.jpg"

initials="PS"

alt="Premium store"

size="base"

/>

<s-stack gap="small-400">

<s-heading>Premium store</s-heading>

<s-text color="subdued">Shopify Plus merchant</s-text>

</s-stack>

</s-stack>

<s-text>Monthly revenue: $45,000</s-text>

</s-stack>

</s-section>

```html```

<s-section>

<s-stack gap="base">

<s-stack direction="inline" gap="small">

<s-avatar

src="/merchants/premium-store.jpg"

initials="PS"

alt="Premium store"

size="base"

></s-avatar>

<s-stack gap="small-400">

<s-heading>Premium store</s-heading>

<s-text color="subdued">Shopify Plus merchant</s-text>

</s-stack>

</s-stack>

<s-text>Monthly revenue: $45,000</s-text>

</s-stack>

</s-section>

```- #### Fulfillment partner avatarsDescriptionShows avatars for different types of fulfillment partners in the Shopify ecosystem.jsx```

<s-stack gap="small">

<s-stack direction="inline" gap="small">

<s-avatar initials="3P" alt="3PL partner" size="small" />

<s-text>Third-party logistics</s-text>

</s-stack>

<s-stack direction="inline" gap="small">

<s-avatar initials="DS" alt="Dropship supplier" size="small" />

<s-text>Dropship supplier</s-text>

</s-stack>

<s-stack direction="inline" gap="small">

<s-avatar initials="WH" alt="Warehouse hub" size="small" />

<s-text>Warehouse hub</s-text>

</s-stack>

</s-stack>

```html```

<s-stack gap="small">

<s-stack direction="inline" gap="small">

<s-avatar initials="3P" alt="3PL partner" size="small"></s-avatar>

<s-text>Third-party logistics</s-text>

</s-stack>

<s-stack direction="inline" gap="small">

<s-avatar initials="DS" alt="Dropship supplier" size="small"></s-avatar>

<s-text>Dropship supplier</s-text>

</s-stack>

<s-stack direction="inline" gap="small">

<s-avatar initials="WH" alt="Warehouse hub" size="small"></s-avatar>

<s-text>Warehouse hub</s-text>

</s-stack>

</s-stack>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/avatar#useful-for)Useful for

- Identifying individuals or businesses

- Representing merchants, customers, or other entities visually

- Seeing visual indicators of people or businesses in lists, tables, or cards

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/avatar#best-practices)Best practices

- `small-200`: use in tightly condensed layouts

- `small`: use when the base size is too big for the layout, or when the avatar has less importance

- `base`: use as the default size

- `large`: use when an avatar is a focal point, such as on a single customer card

- `large-200`: use when extra emphasis is required

## [Anchor to content-guidelines](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/avatar#content-guidelines)Content guidelinesFor avatars, we recommend using a format that describes what will show in the image:

- alt="Person's name" if avatar represents a person

- alt="Business's name" if avatar represents a business

- alt="" if the name appears next to the avatar as text

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)