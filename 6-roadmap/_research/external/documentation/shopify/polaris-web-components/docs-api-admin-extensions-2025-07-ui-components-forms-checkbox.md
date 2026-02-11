---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/forms/checkbox",
    "fetched_at": "2026-02-10T13:28:32.059152",
    "status": 200,
    "size_bytes": 243026
  },
  "metadata": {
    "title": "Checkbox",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "checkbox"
  }
}
---

# Checkbox

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# CheckboxAsk assistantUse this component when you want to provide users with a clear selection option, such as for agreeing to terms and conditions or selecting multiple options from a list.

## [Anchor to checkboxprops](/docs/api/admin-extensions/2025-07/ui-components/forms/checkbox#checkboxprops)CheckboxProps[Anchor to accessibilityLabel](/docs/api/admin-extensions/2025-07/ui-components/forms/checkbox#checkboxprops-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the element. When set, it will be announced to users using assistive technologies and will provide them with more context. When set, any children or `label` supplied will not be announced to screen readers.

[Anchor to checked](/docs/api/admin-extensions/2025-07/ui-components/forms/checkbox#checkboxprops-propertydetail-checked)checked**checked**boolean**boolean**Whether the checkbox is active.

[Anchor to disabled](/docs/api/admin-extensions/2025-07/ui-components/forms/checkbox#checkboxprops-propertydetail-disabled)disabled**disabled**boolean**boolean**Whether the checkbox can be changed.

[Anchor to error](/docs/api/admin-extensions/2025-07/ui-components/forms/checkbox#checkboxprops-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/forms/checkbox#checkboxprops-propertydetail-id)id**id**string**string**A unique identifier for the field. When no `id` is set, a globally unique value will be used instead.

[Anchor to label](/docs/api/admin-extensions/2025-07/ui-components/forms/checkbox#checkboxprops-propertydetail-label)label**label**string**string**Visual content to use as the checkbox label.

[Anchor to name](/docs/api/admin-extensions/2025-07/ui-components/forms/checkbox#checkboxprops-propertydetail-name)name**name**string**string**An identifier for the checkbox that is unique within the nearest containing `Form` component.

[Anchor to onChange](/docs/api/admin-extensions/2025-07/ui-components/forms/checkbox#checkboxprops-propertydetail-onchange)onChange**onChange**(value: boolean) => void**(value: boolean) => void**A callback that is run whenever the checkbox is changed. This callback is called with a boolean indicating whether the checkbox should now be active or inactive. This component is [controlled](https://reactjs.org/docs/forms.html#controlled-components), so you must store this value in state and reflect it back in the `checked` or `value` props.

[Anchor to value](/docs/api/admin-extensions/2025-07/ui-components/forms/checkbox#checkboxprops-propertydetail-value)value**value**boolean**boolean**Whether the checkbox is active. This prop is an alias for `checked`, and can be useful in form libraries that provide a normalized API for dealing with both `boolean` and `string` values. If both `value` and `checked` are set, `checked` takes precedence.

ExamplesAdd a simple CheckboxReactJSCopy991234567891011import {render, Checkbox} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  return (    <Checkbox id="checkbox" name="checkbox">      Save this information for next time    </Checkbox>  );}## Preview### Examples- #### Add a simple CheckboxReact```

import {render, Checkbox} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<Checkbox id="checkbox" name="checkbox">

Save this information for next time

</Checkbox>

);

}

```JS```

import {extend, Checkbox} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const checkbox = root.createComponent(

Checkbox,

{id: 'checkbox', name: 'checkbox'},

'Save this information for next time',

);

root.appendChild(checkbox);

});

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)