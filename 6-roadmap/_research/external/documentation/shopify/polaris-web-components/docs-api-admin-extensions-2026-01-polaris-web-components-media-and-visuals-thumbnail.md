---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/media-and-visuals/thumbnail",
    "fetched_at": "2026-02-10T13:30:50.192638",
    "status": 200,
    "size_bytes": 264239
  },
  "metadata": {
    "title": "Thumbnail",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "media-and-visuals",
    "component": "thumbnail"
  }
}
---

# Thumbnail

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# ThumbnailAsk assistantDisplay a small preview image representing content, products, or media.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/thumbnail#properties)Properties[Anchor to alt](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/thumbnail#properties-propertydetail-alt)alt**alt**string**string**Default: `''`**Default: `''`**An alternative text description that describe the image for the reader to understand what it is about. It is extremely useful for both users using assistive technology and sighted users. A well written description provides people with visual impairments the ability to participate in consuming non-text content. When a screen readers encounters an `s-image`, the description is read and announced aloud. If an image fails to load, potentially due to a poor connection, the `alt` is displayed on screen instead. This has the benefit of letting a sighted buyer know an image was meant to load here, but as an alternative, they’re still able to consume the text content. Read [considerations when writing alternative text](https://www.shopify.com/ca/blog/image-alt-text#4) to learn more.

[Anchor to size](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/thumbnail#properties-propertydetail-size)size**size**"small" | "small-200" | "small-100" | "base" | "large" | "large-100"**"small" | "small-200" | "small-100" | "base" | "large" | "large-100"**Default: 'base'**Default: 'base'**Adjusts the size the product thumbnail image.

[Anchor to src](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/thumbnail#properties-propertydetail-src)src**src**string**string**The image source (either a remote URL or a local file resource).

When the image is loading or no `src` is provided, a placeholder will be rendered.

## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/thumbnail#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/thumbnail#events-propertydetail-error)error**error**OnErrorEventHandler**OnErrorEventHandler**[Anchor to load](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/thumbnail#events-propertydetail-load)load**load**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy91234<s-thumbnail  alt="White sneakers"  src="https://cdn.shopify.com/static/images/polaris/thumbnail-wc_src.jpg" />## Preview### Examples- #### Codejsx```

<s-thumbnail

alt="White sneakers"

src="https://cdn.shopify.com/static/images/polaris/thumbnail-wc_src.jpg"

/>

```html```

<s-thumbnail

alt="White sneakers"

src="https://cdn.shopify.com/static/images/polaris/thumbnail-wc_src.jpg"

></s-thumbnail>

```- #### Basic usageDescriptionDemonstrates a basic thumbnail component with a product image, showing the default base size and an alt text for accessibility.jsx```

<s-thumbnail

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Product preview"

size="base"

/>

```html```

<s-thumbnail

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Product preview"

size="base"

></s-thumbnail>

```- #### Empty stateDescriptionShows the thumbnail component in an empty state, displaying a placeholder icon when no image source is provided.jsx```

<s-thumbnail alt="No image available" size="base" />

```html```

<s-thumbnail alt="No image available" size="base"></s-thumbnail>

```- #### Different sizesDescriptionIllustrates the various size options for the thumbnail component, showcasing small-200, base, and large sizes in a stack layout.jsx```

<s-stack gap="large-100">

<s-thumbnail

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Small thumbnail"

size="small-200"

/>

<s-thumbnail

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Base thumbnail"

size="base"

/>

<s-thumbnail

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Large thumbnail"

size="large"

/>

</s-stack>

```html```

<s-stack gap="large-100">

<s-thumbnail

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Small thumbnail"

size="small-200"

></s-thumbnail>

<s-thumbnail

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Base thumbnail"

size="base"

></s-thumbnail>

<s-thumbnail

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Large thumbnail"

size="large"

></s-thumbnail>

</s-stack>

```- #### With event handlingDescriptionDemonstrates how event handlers like onload or onerror can be attached to the thumbnail component via JavaScript to handle image loading states.jsx```

const [loading, setLoading] = useState(true)

return (

<s-stack direction="inline" gap="base" alignItems="center">

<s-thumbnail

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Product"

size="small-200"

onLoad={() => setLoading(false)}

/>

<s-paragraph>{loading ? 'Loading...' : 'Image loaded'}</s-paragraph>

</s-stack>

)

```html```

<s-stack direction="inline" gap="base">

<s-thumbnail

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Product"

size="small-200"

onLoad="setLoading(false)"

/>

<s-paragraph>Image loaded</s-paragraph>

</s-stack>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/thumbnail#useful-for)Useful for

- Identifying items visually in lists, tables, or cards

- Seeing a preview of images before uploading or publishing

- Distinguishing between similar items by their appearance

- Confirming the correct item is selected

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/thumbnail#best-practices)Best practices

- `small-200`: use in very small areas

- `small`: use in small areas

- `base`: use as the default size

- `large`: use when thumbnail is a focal point

## [Anchor to content-guidelines](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/thumbnail#content-guidelines)Content guidelinesAlternative text should be accurate, concise, and descriptive:

- Use "Image of", "Photo of" prefix

- Be primary visual content: "Image of a woman with curly brown hair smiling"

- Include relevant emotions: "Image of a woman laughing with her hand on her face"

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)