---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image",
    "fetched_at": "2026-02-10T13:29:02.074911",
    "status": 200,
    "size_bytes": 269790
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

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# ImageAsk assistantUse this when you want to display an image.

## [Anchor to imageprops](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops)ImageProps`([ImageAccessibilityLabelProp](#ImageAccessibilityLabelProp) | [ImageAltProp](#ImageAltProp)) & ([ImageSourceProp](#ImageSourceProp) | [ImageSrcProp](#ImageSrcProp)) & [ImageBaseProps](#ImageBaseProps)`**`([ImageAccessibilityLabelProp](#ImageAccessibilityLabelProp) | [ImageAltProp](#ImageAltProp)) & ([ImageSourceProp](#ImageSourceProp) | [ImageSrcProp](#ImageSrcProp)) & [ImageBaseProps](#ImageBaseProps)`**[Anchor to ImageAccessibilityLabelProp](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-imageaccessibilitylabelprop)### ImageAccessibilityLabelProp[Anchor to accessibilityLabel](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**Default: `''`**Default: `''`**required**required**An alternative text description that describe the image for the reader to understand what it is about. It is extremely useful for both users using assistive technology and sighted users. A well written `description` provides people with visual impairments the ability to participate in consuming non-text content. When a screen readers encounters an `Image`, the description is read and announced aloud. If an image fails to load, potentially due to a poor connection, the `description` is displayed on screen instead. This has the benefit of letting a sighted user know an image was meant to load here, but as an alternative, they’re still able to consume the text content. Read [considerations when writing alternative text](https://ux.shopify.com/considerations-when-writing-alt-text-a9c1985a8204) to learn more.

An `alt` property is available as an alias for this for compatibility with the HTML specification. When both are specified, `accessibilityLabel` takes precedence.

[Anchor to alt](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-propertydetail-alt)alt**alt**never**never**[Anchor to ImageAltProp](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-imagealtprop)### ImageAltProp[Anchor to alt](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-propertydetail-alt)alt**alt**string**string**required**required**An alternative text description that describe the image for the reader to understand what it is about. It is extremely useful for both users using assistive technology and sighted users. A well written `description` provides people with visual impairments the ability to participate in consuming non-text content. When a screen readers encounters an `Image`, the description is read and announced aloud. If an image fails to load, potentially due to a poor connection, the `description` is displayed on screen instead. This has the benefit of letting a sighted user know an image was meant to load here, but as an alternative, they’re still able to consume the text content. Read [considerations when writing alternative text](https://ux.shopify.com/considerations-when-writing-alt-text-a9c1985a8204) to learn more.

This property is an alias for `accessibilityLabel` for compatibility with the HTML specification. When both are specified `accessibilityLabel` takes precedence.

[Anchor to accessibilityLabel](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**never**never**[Anchor to ImageBaseProps](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-imagebaseprops)### ImageBaseProps[Anchor to accessibilityRole](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-propertydetail-accessibilityrole)accessibilityRole**accessibilityRole**Sets the semantic meaning of the component’s content. When set, the role will be used by assistive technologies to help users navigate the page.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-propertydetail-id)id**id**string**string**Defines a unique identifier which must be unique in the whole document.

[Anchor to loading](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-propertydetail-loading)loading**loading**'eager' | 'lazy'**'eager' | 'lazy'**Default: `eager`**Default: `eager`**Determines the loading behavior of the image:

- `eager`: Immediately loads the image, irrespective of its position within the visible viewport.

- `lazy`: Delays loading the image until it approaches a specified distance from the viewport.

[Anchor to onError](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-propertydetail-onerror)onError**onError**() => void**() => void**Invoked on load error.

[Anchor to onLoad](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-propertydetail-onload)onLoad**onLoad**() => void**() => void**Invoked when load completes successfully.

[Anchor to ImageSourceProp](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-imagesourceprop)### ImageSourceProp[Anchor to source](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-propertydetail-source)source**source**string**string**required**required**The image source (either a remote URL or a local file resource; blob URLs are not currently supported).

A `src` property is available as an alias for this for compatibility with the HTML specification. When both are specified, `source` takes precedence.

[Anchor to src](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-propertydetail-src)src**src**never**never**[Anchor to ImageSrcProp](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-imagesrcprop)### ImageSrcProp[Anchor to src](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-propertydetail-src)src**src**string**string**required**required**The image source (either a remote URL or a local file resource; blob URLs are not currently supported).

This property is available as an alias for `source` for compatibility with the HTML specification. When both are specified, `source` takes precedence.

[Anchor to source](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#imageprops-propertydetail-source)source**source**never**never**### ImageAccessibilityLabelProp- accessibilityLabelAn alternative text description that describe the image for the reader to understand what it is about. It is extremely useful for both users using assistive technology and sighted users. A well written `description` provides people with visual impairments the ability to participate in consuming non-text content. When a screen readers encounters an `Image`, the description is read and announced aloud. If an image fails to load, potentially due to a poor connection, the `description` is displayed on screen instead. This has the benefit of letting a sighted user know an image was meant to load here, but as an alternative, they’re still able to consume the text content. Read [considerations when writing alternative text](https://ux.shopify.com/considerations-when-writing-alt-text-a9c1985a8204) to learn more.

An `alt` property is available as an alias for this for compatibility with the HTML specification. When both are specified, `accessibilityLabel` takes precedence.```

string

```- alt```

never

``````

interface ImageAccessibilityLabelProp {

/**

* An alternative text description that describe the image for the reader to

* understand what it is about. It is extremely useful for both users using

* assistive technology and sighted users. A well written `description`

* provides people with visual impairments the ability to participate in

* consuming non-text content. When a screen readers encounters an `Image`,

* the description is read and announced aloud. If an image fails to load,

* potentially due to a poor connection, the `description` is displayed on

* screen instead. This has the benefit of letting a sighted user know an

* image was meant to load here, but as an alternative, they’re still able to

* consume the text content. Read

* [considerations when writing alternative text](https://ux.shopify.com/considerations-when-writing-alt-text-a9c1985a8204)

* to learn more.

*

* An `alt` property is available as an alias for this for compatibility with the HTML

* specification. When both are specified, `accessibilityLabel` takes precedence.

*

* @defaultValue `''`

* @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#alt

*/

accessibilityLabel: string;

alt?: never;

}

```### ImageAltProp- accessibilityLabel```

never

```- altAn alternative text description that describe the image for the reader to understand what it is about. It is extremely useful for both users using assistive technology and sighted users. A well written `description` provides people with visual impairments the ability to participate in consuming non-text content. When a screen readers encounters an `Image`, the description is read and announced aloud. If an image fails to load, potentially due to a poor connection, the `description` is displayed on screen instead. This has the benefit of letting a sighted user know an image was meant to load here, but as an alternative, they’re still able to consume the text content. Read [considerations when writing alternative text](https://ux.shopify.com/considerations-when-writing-alt-text-a9c1985a8204) to learn more.

This property is an alias for `accessibilityLabel` for compatibility with the HTML specification. When both are specified `accessibilityLabel` takes precedence.```

string

``````

interface ImageAltProp {

/**

* An alternative text description that describe the image for the reader to

* understand what it is about. It is extremely useful for both users using

* assistive technology and sighted users. A well written `description`

* provides people with visual impairments the ability to participate in

* consuming non-text content. When a screen readers encounters an `Image`,

* the description is read and announced aloud. If an image fails to load,

* potentially due to a poor connection, the `description` is displayed on

* screen instead. This has the benefit of letting a sighted user know an

* image was meant to load here, but as an alternative, they’re still able to

* consume the text content. Read

* [considerations when writing alternative text](https://ux.shopify.com/considerations-when-writing-alt-text-a9c1985a8204)

* to learn more.

*

* This property is an alias for `accessibilityLabel` for compatibility with the HTML

* specification. When both are specified `accessibilityLabel` takes precedence.

*

* @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#alt

*/

alt: string;

accessibilityLabel?: never;

}

```### ImageSourceProp- sourceThe image source (either a remote URL or a local file resource; blob URLs are not currently supported).

A `src` property is available as an alias for this for compatibility with the HTML specification. When both are specified, `source` takes precedence.```

string

```- src```

never

``````

interface ImageSourceProp {

/**

* The image source (either a remote URL or a local file resource; blob URLs are not currently supported).

*

* A `src` property is available as an alias for this for compatibility with the HTML

* specification. When both are specified, `source` takes precedence.

*

* @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#src

*/

source: string;

src?: never;

}

```### ImageSrcProp- source```

never

```- srcThe image source (either a remote URL or a local file resource; blob URLs are not currently supported).

This property is available as an alias for `source` for compatibility with the HTML specification. When both are specified, `source` takes precedence.```

string

``````

interface ImageSrcProp {

/**

* The image source (either a remote URL or a local file resource; blob URLs are not currently supported).

*

* This property is available as an alias for `source` for compatibility with the HTML

* specification. When both are specified, `source` takes precedence.

*

* @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#src

*/

src: string;

source?: never;

}

```### ImageBaseProps- accessibilityRoleSets the semantic meaning of the component’s content. When set, the role will be used by assistive technologies to help users navigate the page.```

```- idDefines a unique identifier which must be unique in the whole document.```

string

```- loadingDetermines the loading behavior of the image:

- `eager`: Immediately loads the image, irrespective of its position within the visible viewport.

- `lazy`: Delays loading the image until it approaches a specified distance from the viewport.```

'eager' | 'lazy'

```- onErrorInvoked on load error.```

() => void

```- onLoadInvoked when load completes successfully.```

() => void

``````

interface ImageBaseProps {

/**

* Sets the semantic meaning of the component’s content. When set,

* the role will be used by assistive technologies to help users

* navigate the page.

*/

accessibilityRole?: Extract<AccessibilityRole, 'decorative'>;

/**

* Defines a unique identifier which must be unique in the whole document.

*

* @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id

*/

id?: string;

/**

* Determines the loading behavior of the image:

* - `eager`: Immediately loads the image, irrespective of its position within the visible viewport.

* - `lazy`: Delays loading the image until it approaches a specified distance from the viewport.

*

* @defaultValue `eager`

* @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#loading

*/

loading?: 'eager' | 'lazy';

/**

* Invoked when load completes successfully.

*

* @see https://developer.mozilla.org/en-US/docs/Web/API/GlobalEventHandlers/onload

*/

onLoad?(): void;

/**

* Invoked on load error.

*

* @see https://developer.mozilla.org/en-US/docs/Web/API/GlobalEventHandlers/onerror

*/

onError?(): void;

}

```ExamplesSimple Image exampleReactJSCopy9123456789import {render, Image} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  return (    <Image alt="Pickaxe" source="/assets/icons/64/pickaxe-1.png" />  );}## Preview### Examples- #### Simple Image exampleReact```

import {render, Image} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<Image alt="Pickaxe" source="/assets/icons/64/pickaxe-1.png" />

);

}

```JS```

import {extend, Image} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const image = root.createComponent(Image, {

alt: 'Pickaxe',

source: '/assets/icons/64/pickaxe-1.png',

});

root.appendChild(image);

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/media-and-visuals/image#related)Related[IconIcon](/docs/api/admin-extensions/components/media/icon)[ - Icon](/docs/api/admin-extensions/components/media/icon)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)