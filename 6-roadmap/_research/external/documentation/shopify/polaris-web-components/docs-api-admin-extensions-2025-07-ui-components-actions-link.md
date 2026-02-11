---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/actions/link",
    "fetched_at": "2026-02-10T13:28:25.819744",
    "status": 200,
    "size_bytes": 252884
  },
  "metadata": {
    "title": "Link",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "actions",
    "component": "link"
  }
}
---

# Link

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# LinkAsk assistantThis is an interactive component that directs users to a specified URL. It even supports custom protocols.

## [Anchor to linkprops](/docs/api/admin-extensions/2025-07/ui-components/actions/link#linkprops)LinkProps[Anchor to accessibilityLabel](/docs/api/admin-extensions/2025-07/ui-components/actions/link#linkprops-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the element. When set, it will be announced to users using assistive technologies and will provide them with more context. When set, any children or `label` supplied will not be announced to screen readers.

[Anchor to href](/docs/api/admin-extensions/2025-07/ui-components/actions/link#linkprops-propertydetail-href)href**href**string**string**The URL to link to. If set, it will navigate to the location specified by `href` after executing the `onClick` callback.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/actions/link#linkprops-propertydetail-id)id**id**string**string**A unique identifier for the link.

[Anchor to lang](/docs/api/admin-extensions/2025-07/ui-components/actions/link#linkprops-propertydetail-lang)lang**lang**string**string**Alias for `language`

[Anchor to language](/docs/api/admin-extensions/2025-07/ui-components/actions/link#linkprops-propertydetail-language)language**language**string**string**Indicate the text language. Useful when the text is in a different language than the rest of the page. It will allow assistive technologies such as screen readers to invoke the correct pronunciation. [Reference of values](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) ("subtag" label)

[Anchor to onClick](/docs/api/admin-extensions/2025-07/ui-components/actions/link#linkprops-propertydetail-onclick)onClick**onClick**() => void**() => void**Callback when a link is pressed. If `href` is set, it will execute the callback and then navigate to the location specified by `href`.

[Anchor to onPress](/docs/api/admin-extensions/2025-07/ui-components/actions/link#linkprops-propertydetail-onpress)onPress**onPress**() => void**() => void**Alias for `onClick` Callback when a link is pressed. If `href` is set, it will execute the callback and then navigate to the location specified by `href`.

[Anchor to target](/docs/api/admin-extensions/2025-07/ui-components/actions/link#linkprops-propertydetail-target)target**target**'_blank' | '_self'**'_blank' | '_self'**Default: '_self'**Default: '_self'**Specifies where to display the linked URL

[Anchor to to](/docs/api/admin-extensions/2025-07/ui-components/actions/link#linkprops-propertydetail-to)to**to**string**string**Alias for `href` If set, it will navigate to the location specified by `to` after executing the `onClick` callback.

[Anchor to tone](/docs/api/admin-extensions/2025-07/ui-components/actions/link#linkprops-propertydetail-tone)tone**tone**'default' | 'inherit' | 'critical'**'default' | 'inherit' | 'critical'**Sets the link color.

- `inherit` will take the color value from its parent, giving the link a monochrome appearance. In some cases, its important to pair this property with another stylistic treatment, like an underline, to differentiate the link from a normal text.

ExamplesLink to an app pageReactJSCopy9912345678910111213141516import React from 'react';import {  render,  Link,} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  return (    <Link href="app:bar">      Link to app path    </Link>  );}## Preview### Examples- #### Link to an app pageReact```

import React from 'react';

import {

render,

Link,

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<Link href="app:bar">

Link to app path

</Link>

);

}

```JS```

import {

extension,

Link,

} from '@shopify/ui-extensions/admin';

export default extension(

'Playground',

(root) => {

const link = root.createComponent(

Link,

{href: 'app://baz'},

'Link to app path',

);

root.appendChild(link);

},

);

```- #### External LinkDescriptionLink to an external URLReact```

import React from 'react';

import {

render,

Link,

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<Link href="https://www.shopify.ca/climate/sustainability-fund">

Sustainability fund

</Link>

);

}

```JS```

import {

extension,

Link,

} from '@shopify/ui-extensions/admin';

export default extension(

'Playground',

(root) => {

const link = root.createComponent(

Link,

{href: 'https://www.shopify.ca/climate/sustainability-fund'},

'Sustainability fund',

);

root.appendChild(link);

},

);

```- #### Relative LinkDescriptionLink to a relative URLReact```

import React from 'react';

import {

render,

Link,

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<Link href="/baz">

Link relative to current path

</Link>

);

}

```JS```

import {

extension,

Link,

} from '@shopify/ui-extensions/admin';

export default extension(

'Playground',

(root) => {

const link = root.createComponent(

Link,

{href: '/baz'},

'Link relative to current path',

);

root.appendChild(link);

},

);

```- #### Shopify Section LinkDescriptionLink to a Shopify admin pageReact```

import React from 'react';

import {

render,

Link,

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<Link href="shopify://admin/orders">

Shop's orders

</Link>

);

}

```JS```

import {

extension,

Link,

} from '@shopify/ui-extensions/admin';

export default extension(

'Playground',

(root) => {

const link = root.createComponent(

Link,

{href: 'shopify://admin/orders'},

"Shop's orders",

);

root.appendChild(link);

},

);

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/actions/link#related)Related[ButtonButton](/docs/api/admin-extensions/components/actions/button)[ - Button](/docs/api/admin-extensions/components/actions/button)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)