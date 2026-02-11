---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/actions/button",
    "fetched_at": "2026-02-10T13:28:24.497444",
    "status": 200,
    "size_bytes": 282982
  },
  "metadata": {
    "title": "Button",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "actions",
    "component": "button"
  }
}
---

# Button

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# ButtonAsk assistantUse this component when you want to provide users the ability to perform specific actions, like saving data.

## [Anchor to buttonprops](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops)ButtonProps`[ButtonBaseProps](#ButtonBaseProps) | [ButtonAnchorProps](#ButtonAnchorProps)`**`[ButtonBaseProps](#ButtonBaseProps) | [ButtonAnchorProps](#ButtonAnchorProps)`**[Anchor to ButtonAnchorProps](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-buttonanchorprops)### ButtonAnchorProps[Anchor to href](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-href)href**href**string**string**required**required**The URL to link to. If set, it will navigate to the location specified by `href` after executing the `onClick` callback.

[Anchor to accessibilityLabel](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the Button. It will be read to users using assistive technologies such as screen readers.

Use this when using only an icon or the button text is not enough context for users using assistive technologies.

[Anchor to disabled](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-disabled)disabled**disabled**boolean**boolean**Disables the button, disallowing any interaction.

[Anchor to download](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-download)download**download**boolean | string**boolean | string**Tells browsers to download the linked resource instead of navigating to it. Optionally accepts filename value to rename file.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-id)id**id**string**string**A unique identifier for the button.

[Anchor to lang](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-lang)lang**lang**string**string**Alias for `language`

[Anchor to language](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-language)language**language**string**string**Indicate the text language. Useful when the text is in a different language than the rest of the page. It will allow assistive technologies such as screen readers to invoke the correct pronunciation. [Reference of values](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) ("subtag" label)

[Anchor to onBlur](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-onblur)onBlur**onBlur**() => void**() => void**Callback when focus is removed.

[Anchor to onClick](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-onclick)onClick**onClick**() => void**() => void**Callback when a link is pressed. If `href` is set, it will execute the callback and then navigate to the location specified by `href`.

[Anchor to onFocus](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-onfocus)onFocus**onFocus**() => void**() => void**Callback when input is focused.

[Anchor to onPress](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-onpress)onPress**onPress**() => void**() => void**Alias for `onClick` Callback when a link is pressed. If `href` is set, it will execute the callback and then navigate to the location specified by `href`.

[Anchor to target](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-target)target**target**'_blank' | '_self'**'_blank' | '_self'**Default: '_self'**Default: '_self'**Specifies where to display the linked URL

[Anchor to to](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-to)to**to**string**string**Alias for `href` If set, it will navigate to the location specified by `to` after executing the `onClick` callback.

[Anchor to tone](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-tone)tone**tone**'default' | 'critical'**'default' | 'critical'**Sets the color treatment of the Button.

[Anchor to variant](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-variant)variant**variant**'primary' | 'secondary' | 'tertiary'**'primary' | 'secondary' | 'tertiary'**Changes the visual appearance of the Button.

[Anchor to ButtonBaseProps](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-buttonbaseprops)### ButtonBaseProps[Anchor to accessibilityLabel](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the Button. It will be read to users using assistive technologies such as screen readers.

Use this when using only an icon or the button text is not enough context for users using assistive technologies.

[Anchor to accessibilityRole](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-accessibilityrole)accessibilityRole**accessibilityRole**Sets the semantic meaning of the component’s content. When set, the role will be used by assistive technologies to help users navigate the page.

[Anchor to disabled](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-disabled)disabled**disabled**boolean**boolean**Disables the button, disallowing any interaction.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-id)id**id**string**string**A unique identifier for the button.

[Anchor to lang](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-lang)lang**lang**string**string**Alias for `language`

[Anchor to language](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-language)language**language**string**string**Indicate the text language. Useful when the text is in a different language than the rest of the page. It will allow assistive technologies such as screen readers to invoke the correct pronunciation. [Reference of values](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) ("subtag" label)

[Anchor to onBlur](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-onblur)onBlur**onBlur**() => void**() => void**Callback when focus is removed.

[Anchor to onClick](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-onclick)onClick**onClick**() => void**() => void**Callback when a link is pressed. If `href` is set, it will execute the callback and then navigate to the location specified by `href`.

[Anchor to onFocus](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-onfocus)onFocus**onFocus**() => void**() => void**Callback when input is focused.

[Anchor to onPress](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-onpress)onPress**onPress**() => void**() => void**Alias for `onClick` Callback when a button is pressed. If `href` is set, it will execute the callback and then navigate to the location specified by `href`.

[Anchor to tone](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-tone)tone**tone**'default' | 'critical'**'default' | 'critical'**Sets the color treatment of the Button.

[Anchor to variant](/docs/api/admin-extensions/2025-07/ui-components/actions/button#buttonprops-propertydetail-variant)variant**variant**'primary' | 'secondary' | 'tertiary'**'primary' | 'secondary' | 'tertiary'**Changes the visual appearance of the Button.

### ButtonBaseProps- accessibilityLabelA label that describes the purpose or contents of the Button. It will be read to users using assistive technologies such as screen readers.

Use this when using only an icon or the button text is not enough context for users using assistive technologies.```

string

```- accessibilityRoleSets the semantic meaning of the component’s content. When set, the role will be used by assistive technologies to help users navigate the page.```

```- disabledDisables the button, disallowing any interaction.```

boolean

```- idA unique identifier for the button.```

string

```- langAlias for `language````

string

```- languageIndicate the text language. Useful when the text is in a different language than the rest of the page. It will allow assistive technologies such as screen readers to invoke the correct pronunciation. [Reference of values](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) ("subtag" label)```

string

```- onBlurCallback when focus is removed.```

() => void

```- onClickCallback when a link is pressed. If `href` is set, it will execute the callback and then navigate to the location specified by `href`.```

() => void

```- onFocusCallback when input is focused.```

() => void

```- onPressAlias for `onClick` Callback when a button is pressed. If `href` is set, it will execute the callback and then navigate to the location specified by `href`.```

() => void

```- toneSets the color treatment of the Button.```

'default' | 'critical'

```- variantChanges the visual appearance of the Button.```

'primary' | 'secondary' | 'tertiary'

``````

interface ButtonBaseProps extends CommonProps {

/**

* Sets the semantic meaning of the component’s content. When set,

* the role will be used by assistive technologies to help users

* navigate the page.

*/

accessibilityRole?: Extract<AccessibilityRole, 'submit' | 'button' | 'reset'>;

}

```### ButtonAnchorProps- accessibilityLabelA label that describes the purpose or contents of the Button. It will be read to users using assistive technologies such as screen readers.

Use this when using only an icon or the button text is not enough context for users using assistive technologies.```

string

```- disabledDisables the button, disallowing any interaction.```

boolean

```- downloadTells browsers to download the linked resource instead of navigating to it. Optionally accepts filename value to rename file.```

boolean | string

```- hrefThe URL to link to. If set, it will navigate to the location specified by `href` after executing the `onClick` callback.```

string

```- idA unique identifier for the button.```

string

```- langAlias for `language````

string

```- languageIndicate the text language. Useful when the text is in a different language than the rest of the page. It will allow assistive technologies such as screen readers to invoke the correct pronunciation. [Reference of values](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) ("subtag" label)```

string

```- onBlurCallback when focus is removed.```

() => void

```- onClickCallback when a link is pressed. If `href` is set, it will execute the callback and then navigate to the location specified by `href`.```

() => void

```- onFocusCallback when input is focused.```

() => void

```- onPressAlias for `onClick` Callback when a link is pressed. If `href` is set, it will execute the callback and then navigate to the location specified by `href`.```

() => void

```- targetSpecifies where to display the linked URL```

'_blank' | '_self'

```- toAlias for `href` If set, it will navigate to the location specified by `to` after executing the `onClick` callback.```

string

```- toneSets the color treatment of the Button.```

'default' | 'critical'

```- variantChanges the visual appearance of the Button.```

'primary' | 'secondary' | 'tertiary'

``````

interface ButtonAnchorProps extends CommonProps {

/**

* The URL to link to.

* If set, it will navigate to the location specified by `href` after executing the `onClick` callback.

*/

href: AnchorProps['href'];

/**

* Alias for `href`

* If set, it will navigate to the location specified by `to` after executing the `onClick` callback.

*/

to?: AnchorProps['href'];

/**

* Tells browsers to download the linked resource instead of navigating to it.

* Optionally accepts filename value to rename file.

*/

download?: boolean | string;

/**

* Specifies where to display the linked URL

* @default '_self'

*/

target?: '_blank' | '_self';

/**

* Callback when a link is pressed. If `href` is set,

* it will execute the callback and then navigate to the location specified by `href`.

*/

onClick?: AnchorProps['onClick'];

/**

* Alias for `onClick`

* Callback when a link is pressed. If `href` is set,

* it will execute the callback and then navigate to the location specified by `href`.

*/

onPress?: AnchorProps['onClick'];

}

```ExamplesAdd a simple button to your app.ReactJSCopy99123456789101112131415import {render, Button} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  return (    <Button      onPress={() => {        console.log('onPress event');      }}    >      Click here    </Button>  );}## Preview### Examples- #### Add a simple button to your app.React```

import {render, Button} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<Button

onPress={() => {

console.log('onPress event');

}}

>

Click here

</Button>

);

}

```JS```

import {extend, Button} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const button = root.createComponent(

Button,

{onPress: () => console.log('onPress event')},

'Click here',

);

root.appendChild(button);

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/actions/button#related)Related[PressablePressable](/docs/api/admin-extensions/components/actions/pressable)[ - Pressable](/docs/api/admin-extensions/components/actions/pressable)[LinkLink](/docs/api/admin-extensions/components/actions/link)[ - Link](/docs/api/admin-extensions/components/actions/link)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)