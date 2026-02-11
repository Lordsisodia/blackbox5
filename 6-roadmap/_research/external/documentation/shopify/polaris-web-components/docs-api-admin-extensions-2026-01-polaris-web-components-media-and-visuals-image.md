---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/media-and-visuals/image",
    "fetched_at": "2026-02-10T13:30:48.157028",
    "status": 200,
    "size_bytes": 305376
  },
  "metadata": {
    "title": "Image",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "media-and-visuals",
    "component": "image"
  }
}
---

# Image

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# ImageAsk assistantEmbeds an image within the interface and controls its presentation. Use to visually illustrate concepts, showcase products, or support user tasks and interactions.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties)Properties[Anchor to accessibilityRole](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-accessibilityrole)accessibilityRole**accessibilityRole**"none" | "presentation" | "img"**"none" | "presentation" | "img"**Default: 'img'**Default: 'img'**Sets the semantic meaning of the component’s content. When set, the role will be used by assistive technologies to help users navigate the page.

[Anchor to alt](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-alt)alt**alt**string**string**Default: `''`**Default: `''`**An alternative text description that describe the image for the reader to understand what it is about. It is extremely useful for both users using assistive technology and sighted users. A well written description provides people with visual impairments the ability to participate in consuming non-text content. When a screen readers encounters an `s-image`, the description is read and announced aloud. If an image fails to load, potentially due to a poor connection, the `alt` is displayed on screen instead. This has the benefit of letting a sighted buyer know an image was meant to load here, but as an alternative, they’re still able to consume the text content. Read [considerations when writing alternative text](https://www.shopify.com/ca/blog/image-alt-text#4) to learn more.

[Anchor to aspectRatio](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-aspectratio)aspectRatio**aspectRatio**`${number}` | `${number}/${number}` | `${number}/ ${number}` | `${number} /${number}` | `${number} / ${number}`**`${number}` | `${number}/${number}` | `${number}/ ${number}` | `${number} /${number}` | `${number} / ${number}`**Default: '1/1'**Default: '1/1'**The aspect ratio of the image.

The rendering of the image will depend on the `inlineSize` value:

- `inlineSize="fill"`: the aspect ratio will be respected and the image will take the necessary space.

- `inlineSize="auto"`: the image will not render until it has loaded and the aspect ratio will be ignored.

For example, if the value is set as `50 / 100`, the getter returns `50 / 100`. If the value is set as `0.5`, the getter returns `0.5 / 1`.

[Anchor to border](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-border)border**border**BorderShorthandBorderShorthand**BorderShorthandBorderShorthand**Default: 'none' - equivalent to `none base auto`.**Default: 'none' - equivalent to `none base auto`.**Set the border via the shorthand property.

This can be a size, optionally followed by a color, optionally followed by a style.

If the color is not specified, it will be `base`.

If the style is not specified, it will be `auto`.

Values can be overridden by `borderWidth`, `borderStyle`, and `borderColor`.

[Anchor to borderColor](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-bordercolor)borderColor**borderColor**"" | ColorKeywordColorKeyword**"" | ColorKeywordColorKeyword**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the color of the border.

[Anchor to borderRadius](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-borderradius)borderRadius**borderRadius**MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderRadiiBoxBorderRadii>**MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderRadiiBoxBorderRadii>**Default: 'none'**Default: 'none'**Adjust the radius of the border.

[Anchor to borderStyle](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-borderstyle)borderStyle**borderStyle**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderStylesBoxBorderStyles>**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<BoxBorderStylesBoxBorderStyles>**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the style of the border.

[Anchor to borderWidth](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-borderwidth)borderWidth**borderWidth**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<"small" | "small-100" | "base" | "large" | "large-100" | "none">**"" | MaybeAllValuesShorthandPropertyMaybeAllValuesShorthandProperty<"small" | "small-100" | "base" | "large" | "large-100" | "none">**Default: '' - meaning no override**Default: '' - meaning no override**Adjust the width of the border.

[Anchor to inlineSize](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-inlinesize)inlineSize**inlineSize**"auto" | "fill"**"auto" | "fill"**Default: 'fill'**Default: 'fill'**The displayed inline width of the image.

- `fill`: the image will takes up 100% of the available inline size.

- `auto`: the image will be displayed at its natural size.

[Anchor to loading](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-loading)loading**loading**"eager" | "lazy"**"eager" | "lazy"**Default: 'eager'**Default: 'eager'**Determines the loading behavior of the image:

- `eager`: Immediately loads the image, irrespective of its position within the visible viewport.

- `lazy`: Delays loading the image until it approaches a specified distance from the viewport.

[Anchor to objectFit](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-objectfit)objectFit**objectFit**"contain" | "cover"**"contain" | "cover"**Default: 'contain'**Default: 'contain'**Determines how the content of the image is resized to fit its container. The image is positioned in the center of the container.

[Anchor to sizes](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-sizes)sizes**sizes**string**string**A set of media conditions and their corresponding sizes.

[Anchor to src](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-src)src**src**string**string**The image source (either a remote URL or a local file resource).

When the image is loading or no `src` is provided, a placeholder will be rendered.

[Anchor to srcSet](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#properties-propertydetail-srcset)srcSet**srcSet**string**string**A set of image sources and their width or pixel density descriptors.

This overrides the `src` property.

### BorderShorthandRepresents a shorthand for defining a border. It can be a combination of size, optionally followed by color, optionally followed by style.```

BorderSizeKeyword | `${BorderSizeKeyword} ${ColorKeyword}` | `${BorderSizeKeyword} ${ColorKeyword} ${BorderStyleKeyword}`

```### BorderSizeKeyword```

SizeKeyword | 'none'

```### SizeKeyword```

'small-500' | 'small-400' | 'small-300' | 'small-200' | 'small-100' | 'small' | 'base' | 'large' | 'large-100' | 'large-200' | 'large-300' | 'large-400' | 'large-500'

```### ColorKeyword```

'subdued' | 'base' | 'strong'

```### BorderStyleKeyword```

'none' | 'solid' | 'dashed' | 'dotted' | 'auto'

```### MaybeAllValuesShorthandProperty```

T | `${T} ${T}` | `${T} ${T} ${T}` | `${T} ${T} ${T} ${T}`

```### BoxBorderRadii```

'small' | 'small-200' | 'small-100' | 'base' | 'large' | 'large-100' | 'large-200' | 'none'

```### BoxBorderStyles```

'auto' | 'none' | 'solid' | 'dashed'

```## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#events-propertydetail-error)error**error**OnErrorEventHandler**OnErrorEventHandler**[Anchor to load](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#events-propertydetail-load)load**load**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy9123456<s-image  src="https://cdn.shopify.com/static/images/polaris/image-wc_src.png"  alt="Four pixelated characters ready to build amazing Shopify apps"  aspectRatio="59/161"  inlineSize="auto" />## Preview### Examples- #### Codejsx```

<s-image

src="https://cdn.shopify.com/static/images/polaris/image-wc_src.png"

alt="Four pixelated characters ready to build amazing Shopify apps"

aspectRatio="59/161"

inlineSize="auto"

/>

```html```

<s-image

src="https://cdn.shopify.com/static/images/polaris/image-wc_src.png"

alt="Four pixelated characters ready to build amazing Shopify apps"

aspectRatio="59/161"

inlineSize="auto"

></s-image>

```- #### Basic usageDescriptionDemonstrates the simplest implementation of an image component with a source and alt text.jsx```

<s-image src="https://cdn.shopify.com/static/sample-product/House-Plant1.png" alt="Product image" />

```html```

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Product image"

></s-image>

```- #### Responsive layout with aspect ratioDescriptionShows how to create a responsive image with a fixed 16:9 aspect ratio, set to cover the container, and loaded lazily.jsx```

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Featured product"

aspectRatio="16/9"

objectFit="cover"

loading="lazy"

/>

```html```

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Featured product"

aspectRatio="16/9"

objectFit="cover"

loading="lazy"

></s-image>

```- #### Responsive images with srcsetDescriptionIllustrates how to provide multiple image sources for different screen sizes and resolutions using srcSet and sizes attributes.jsx```

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

srcSet="https://cdn.shopify.com/static/sample-product/House-Plant1.png 400w,

https://cdn.shopify.com/static/sample-product/House-Plant1.png 800w"

sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 400px"

alt="Product detail"

aspectRatio="16/9"

objectFit="cover"

/>

```html```

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

srcSet="https://cdn.shopify.com/static/sample-product/House-Plant1.png 400w,

https://cdn.shopify.com/static/sample-product/House-Plant1.png 800w"

sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 400px"

alt="Product detail"

aspectRatio="16/9"

objectFit="cover"

></s-image>

```- #### With border stylingDescriptionDemonstrates how to apply border styling to an image, including width, style, color, and radius, using border-related properties.jsx```

<s-box inlineSize="300px">

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Product thumbnail"

borderWidth="large"

borderStyle="solid"

borderColor="strong"

borderRadius="large"

objectFit="cover"

aspectRatio="1/1"

/>

</s-box>

```html```

<s-box inlineSize="300px">

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Product thumbnail"

borderWidth="large"

borderStyle="solid"

borderColor="strong"

borderRadius="large"

objectFit="cover"

aspectRatio="1/1"

></s-image>

</s-box>

```- #### Decorative imageDescriptionShows how to mark an image as decorative, which will make screen readers ignore the image by setting an empty alt text and presentation role.jsx```

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt=""

accessibilityRole="presentation"

objectFit="cover"

/>

```html```

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt=""

accessibilityRole="presentation"

objectFit="cover"

></s-image>

```- #### Auto-sized imageDescriptionDemonstrates an image with auto-sizing, which allows the image to adjust its size based on its container's width.jsx```

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Product image"

inlineSize="auto"

/>

```html```

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Product image"

inlineSize="auto"

></s-image>

```- #### Within layout componentsDescriptionShows how to use images within a grid layout, creating a consistent grid of images with equal size, aspect ratio, and styling.jsx```

<s-grid gridTemplateColumns="repeat(3, 150px)" gap="base" alignItems="center">

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Main view"

aspectRatio="1/1"

objectFit="cover"

borderRadius="base"

inlineSize="fill"

/>

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Side view"

aspectRatio="1/1"

objectFit="cover"

borderRadius="base"

inlineSize="fill"

/>

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Detail view"

aspectRatio="1/1"

objectFit="cover"

borderRadius="base"

inlineSize="fill"

/>

</s-grid>

```html```

<s-grid gridTemplateColumns="repeat(3, 150px)" gap="base" alignItems="center">

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Main view"

aspectRatio="1/1"

objectFit="cover"

borderRadius="base"

inlineSize="fill"

></s-image>

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Side view"

aspectRatio="1/1"

objectFit="cover"

borderRadius="base"

inlineSize="fill"

></s-image>

<s-image

src="https://cdn.shopify.com/static/sample-product/House-Plant1.png"

alt="Detail view"

aspectRatio="1/1"

objectFit="cover"

borderRadius="base"

inlineSize="fill"

></s-image>

</s-grid>

```## [Anchor to useful-for](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#useful-for)Useful for

- Adding illustrations and photos.

## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#best-practices)Best practices

- Use high-resolution, optimized images

- Use intentionally to add clarity and guide users

## [Anchor to content-guidelines](/docs/api/admin-extensions/latest/polaris-web-components/media-and-visuals/image#content-guidelines)Content guidelinesAlt text should be accurate, concise, and descriptive:

- Indicate it's an image: "Image of", "Photo of"

- Focus on description: "Image of a woman with curly brown hair smiling"

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)