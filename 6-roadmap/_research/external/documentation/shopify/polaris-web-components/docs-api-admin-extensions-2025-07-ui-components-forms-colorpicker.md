---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/forms/colorpicker",
    "fetched_at": "2026-02-10T13:28:36.082803",
    "status": 200,
    "size_bytes": 238259
  },
  "metadata": {
    "title": "ColorPicker",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "colorpicker"
  }
}
---

# ColorPicker

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# ColorPickerAsk assistantUse this component if you need to select a color.

## [Anchor to colorpickerprops](/docs/api/admin-extensions/2025-07/ui-components/forms/colorpicker#colorpickerprops)ColorPickerProps[Anchor to allowAlpha](/docs/api/admin-extensions/2025-07/ui-components/forms/colorpicker#colorpickerprops-propertydetail-allowalpha)allowAlpha**allowAlpha**boolean**boolean**Default: false**Default: false**Allow user to select an alpha value.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/forms/colorpicker#colorpickerprops-propertydetail-id)id**id**string**string**ID for the element.

[Anchor to onChange](/docs/api/admin-extensions/2025-07/ui-components/forms/colorpicker#colorpickerprops-propertydetail-onchange)onChange**onChange**(value: string) => void**(value: string) => void**The `onChange` handler will emit the value in hex. If the `allowAlpha` prop is `true`, `onChange` will emit an 8-value hex (#RRGGBBAA). If the `allowAlpha` prop is `false`, `onChange` will emit a 6-value hex (#RRGGBB).

[Anchor to value](/docs/api/admin-extensions/2025-07/ui-components/forms/colorpicker#colorpickerprops-propertydetail-value)value**value**string**string**The currently selected color.

Supported formats include:

- RGB

ExamplesSimple ColorPicker exampleReactJSCopy991234567891011121314151617import {  render,  ColorPicker,} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  return (    <ColorPicker      value="rgba(255 0 0 / 0.5)"      onChange={(value) => {        console.log({value});      }}    />  );}## Preview### Examples- #### Simple ColorPicker exampleReact```

import {

render,

ColorPicker,

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<ColorPicker

value="rgba(255 0 0 / 0.5)"

onChange={(value) => {

console.log({value});

}}

/>

);

}

```JS```

import {

extension,

ColorPicker,

} from '@shopify/ui-extensions/admin';

export default extension(

'Playground',

(root) => {

const blockStack = root.createComponent(

ColorPicker,

{

value: "rgba(255 0 0 / 0.5)",

label: ""

},

);

root.appendChild(blockStack);

},

);

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/forms/colorpicker#related)Related[SelectSelect](/docs/api/admin-extensions/components/forms/select)[ - Select](/docs/api/admin-extensions/components/forms/select)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)