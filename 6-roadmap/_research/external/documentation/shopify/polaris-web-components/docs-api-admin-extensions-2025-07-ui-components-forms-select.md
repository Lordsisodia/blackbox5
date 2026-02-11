---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/forms/select",
    "fetched_at": "2026-02-10T13:28:47.977045",
    "status": 200,
    "size_bytes": 263141
  },
  "metadata": {
    "title": "Select",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "select"
  }
}
---

# Select

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# SelectAsk assistantUse this when you want to give users a predefined list of options to choose from.

## [Anchor to selectprops](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops)SelectProps[Anchor to label](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops-propertydetail-label)label**label**string**string**required**required**Content to use as the field label.

[Anchor to options](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops-propertydetail-options)options**options**(OptionDescriptionOptionDescription | OptionGroupDescriptionOptionGroupDescription)[]**(OptionDescriptionOptionDescription | OptionGroupDescriptionOptionGroupDescription)[]**required**required**The options a user can select from.

When both `options` and children `Option` or `OptionGroup` are provided, the options will be merged together, with the `options` property taking precedence.

[Anchor to disabled](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops-propertydetail-disabled)disabled**disabled**boolean**boolean**Whether the select can be changed.

[Anchor to error](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops-propertydetail-id)id**id**string**string**A unique identifier for the field. When no `id` is set, a globally unique value will be used instead.

[Anchor to name](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing `Form` component.

[Anchor to onBlur](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops-propertydetail-onblur)onBlur**onBlur**() => void**() => void**Callback when focus is removed.

[Anchor to onChange](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops-propertydetail-onchange)onChange**onChange**(value: string) => void**(value: string) => void**A callback that is run whenever the selected option changes. This callback is called with the string `value` of the selected `option`. This component is [controlled](https://reactjs.org/docs/forms.html#controlled-components), so you must store this value in state and reflect it back in the `value` prop of the select.

[Anchor to onFocus](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops-propertydetail-onfocus)onFocus**onFocus**() => void**() => void**Callback when input is focused.

[Anchor to placeholder](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops-propertydetail-placeholder)placeholder**placeholder**string**string**A short hint that describes the expected value of the field.

[Anchor to readOnly](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops-propertydetail-readonly)readOnly**readOnly**boolean**boolean**Whether the field is read-only.

[Anchor to required](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops-propertydetail-required)required**required**boolean**boolean**Whether the field needs a value. This requirement adds semantic value to the field, but it will not cause an error to appear automatically. If you want to present an error when this field is empty, you can do so with the `error` prop.

[Anchor to value](/docs/api/admin-extensions/2025-07/ui-components/forms/select#selectprops-propertydetail-value)value**value**string**string**The active option for the select. This should match to one of the `value` properties in the `options` property or one of the `<Option>`. When not set, the value will default to an empty string, which will show the `placeholder` text as the "selected value".

### OptionDescription- disabledWhether this option can be selected or not.```

boolean

```- labelThe user-facing label for this option.```

string

```- valueThe value that will be passed to the select’s `onChange` callback when this option is selected.```

string

``````

export interface OptionDescription {

/**

* Whether this option can be selected or not.

*/

disabled?: boolean;

/**

* The user-facing label for this option.

*/

label: string;

/**

* The value that will be passed to the select’s `onChange` callback

* when this option is selected.

*/

value: string;

}

```### OptionGroupDescription- disabledWhether the options within this group can be selected or not.```

boolean

```- labelThe user-facing label for this group of options.```

string

```- optionsThe options a user can select from.```

OptionDescription[]

``````

export interface OptionGroupDescription {

/**

* Whether the options within this group can be selected or not.

*/

disabled?: boolean;

/**

* The user-facing label for this group of options.

*/

label: string;

/**

* The options a user can select from.

*/

options?: OptionDescription[];

}

```ExamplesSimple Select exampleReactJSCopy99123456789101112131415161718192021222324252627282930313233343536373839404142434445import React from 'react';import {  render,  Select,} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  const [value, setValue] = React.useState('2');  return (    <Select      label="Country"      value={value}      onChange={setValue}      options={[        {          value: '1',          label: 'Australia',        },        {          value: '2',          label: 'Canada',        },        {          value: '3',          label: 'France',        },        {          value: '4',          label: 'Japan',        },        {          value: '5',          label: 'Nigeria',        },        {          value: '6',          label: 'United States',        },      ]}    />  );}## Preview### Examples- #### Simple Select exampleReact```

import React from 'react';

import {

render,

Select,

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

const [value, setValue] = React.useState('2');

return (

<Select

label="Country"

value={value}

onChange={setValue}

options={[

{

value: '1',

label: 'Australia',

},

{

value: '2',

label: 'Canada',

},

{

value: '3',

label: 'France',

},

{

value: '4',

label: 'Japan',

},

{

value: '5',

label: 'Nigeria',

},

{

value: '6',

label: 'United States',

},

]}

/>

);

}

```JS```

import {

extension,

Select,

} from '@shopify/ui-extensions/admin';

export default extension(

'Playground',

(root) => {

let value = '2';

const select = root.createComponent(Select, {

value,

label: 'Country',

onChange(nextValue) {

value = nextValue;

select.updateProps({value});

},

options: [

{

value: '1',

label: 'Australia',

},

{

value: '2',

label: 'Canada',

},

{

value: '3',

label: 'France',

},

{

value: '4',

label: 'Japan',

},

{

value: '5',

label: 'Nigeria',

},

{

value: '6',

label: 'United States',

},

],

});

root.appendChild(select);

},

);

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)