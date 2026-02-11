---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/forms/choicelist",
    "fetched_at": "2026-02-10T13:28:33.314421",
    "status": 200,
    "size_bytes": 251696
  },
  "metadata": {
    "title": "ChoiceList",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "choicelist"
  }
}
---

# ChoiceList

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# ChoiceListAsk assistantUse this component if you need to group together a related list of interactive choices as radio buttons or checkboxes.

## [Anchor to choicelistprops](/docs/api/admin-extensions/2025-07/ui-components/forms/choicelist#choicelistprops)ChoiceListProps[Anchor to choices](/docs/api/admin-extensions/2025-07/ui-components/forms/choicelist#choicelistprops-propertydetail-choices)choices**choices**ChoicePropsChoiceProps[]**ChoicePropsChoiceProps[]**[Anchor to defaultValue](/docs/api/admin-extensions/2025-07/ui-components/forms/choicelist#choicelistprops-propertydetail-defaultvalue)defaultValue**defaultValue**string | string[]**string | string[]**A default value to populate for uncontrolled components.

[Anchor to disabled](/docs/api/admin-extensions/2025-07/ui-components/forms/choicelist#choicelistprops-propertydetail-disabled)disabled**disabled**boolean**boolean**Whether the field can be modified.

[Anchor to error](/docs/api/admin-extensions/2025-07/ui-components/forms/choicelist#choicelistprops-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to multiple](/docs/api/admin-extensions/2025-07/ui-components/forms/choicelist#choicelistprops-propertydetail-multiple)multiple**multiple**boolean**boolean**Whether to allow selection of multiple choices

[Anchor to name](/docs/api/admin-extensions/2025-07/ui-components/forms/choicelist#choicelistprops-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing `Form` component.

[Anchor to onChange](/docs/api/admin-extensions/2025-07/ui-components/forms/choicelist#choicelistprops-propertydetail-onchange)onChange**onChange**(value: string | string[]) => void**(value: string | string[]) => void**Callback when the user has **finished editing** a field. Unlike `onChange` callbacks you may be familiar with from React component libraries, this callback is **not** run on every change to the input. Text fields are “partially controlled” components, which means that while the user edits the field, its state is controlled by the component. Once the user has signalled that they have finished editing the field (typically, by blurring the field), `onChange` is called if the input actually changed from the most recent `value` property. At that point, you are expected to store this “committed value” in state, and reflect it in the text field’s `value` property.

This state management model is important given how UI Extensions are rendered. UI Extension components run on a separate thread from the UI, so they can’t respond to input synchronously. A pattern popularized by [controlled React components](https://reactjs.org/docs/forms.html#controlled-components) is to have the component be the source of truth for the input `value`, and update the `value` on every user input. The delay in responding to events from a UI extension is only a few milliseconds, but attempting to strictly store state with this delay can cause issues if a user types quickly, or if the user is using a lower-powered device. Having the UI thread take ownership for “in progress” input, and only synchronizing when the user is finished with a field, avoids this risk.

It can still sometimes be useful to be notified when the user makes any input in the field. If you need this capability, you can use the `onInput` prop. However, never use that property to create tightly controlled state for the `value`.

This callback is called with the current value of the field. If the value of a field is the same as the current `value` prop provided to the field, the `onChange` callback will not be run.

[Anchor to readOnly](/docs/api/admin-extensions/2025-07/ui-components/forms/choicelist#choicelistprops-propertydetail-readonly)readOnly**readOnly**boolean**boolean**Whether the field is read-only.

[Anchor to value](/docs/api/admin-extensions/2025-07/ui-components/forms/choicelist#choicelistprops-propertydetail-value)value**value**T**T**The current value for the field. If omitted, the field will be empty. You should update this value in response to the `onChange` callback.

### ChoiceProps- accessibilityLabelA label that describes the purpose or contents of the element. When set, it will be announced to users using assistive technologies and will provide them with more context. When set, any children or `label` supplied will not be announced to screen readers.```

string

```- checkedWhether the choice is checked or not```

boolean

```- disabledWhether the field can be modified.```

boolean

```- errorIndicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.```

string

```- idA unique identifier for the field.```

string

```- labelContent to use as the field label.```

string

```- readOnlyWhether the field is read-only.```

boolean

``````

export interface ChoiceProps

extends AccessibilityLabelProps,

Pick<

InputProps<string>,

'disabled' | 'label' | 'id' | 'readOnly' | 'error'

> {

/**

* Whether the choice is checked or not

*/

checked?: boolean;

}

```ExamplesSimple ChoiceList exampleReactJSCopy9912345678910111213141516import {render, ChoiceList} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  return (    <ChoiceList      name="Company name"      choices={[        {label: 'Hidden', id: '1'},        {label: 'Optional', id: '2'},        {label: 'Required', id: '3'},      ]}    />  );}## Preview### Examples- #### Simple ChoiceList exampleReact```

import {render, ChoiceList} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

return (

<ChoiceList

name="Company name"

choices={[

{label: 'Hidden', id: '1'},

{label: 'Optional', id: '2'},

{label: 'Required', id: '3'},

]}

/>

);

}

```JS```

import {

extension,

ChoiceList,

} from '@shopify/ui-extensions/admin';

export default extension(

'Playground',

(root) => {

const blockStack = root.createComponent(

ChoiceList,

{

name: 'Company name',

choices: [

{label: 'Hidden', id: '1'},

{label: 'Optional', id: '2'},

{label: 'Required', id: '3'},

]

},

);

root.appendChild(blockStack);

},

);

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/forms/choicelist#related)Related[SelectSelect](/docs/api/admin-extensions/components/forms/select)[ - Select](/docs/api/admin-extensions/components/forms/select)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)