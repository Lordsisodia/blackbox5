---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/forms/datefield",
    "fetched_at": "2026-02-10T13:28:37.517557",
    "status": 200,
    "size_bytes": 261565
  },
  "metadata": {
    "title": "DateField",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "datefield"
  }
}
---

# DateField

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# DateFieldAsk assistantThis is a form field that lets users select a date using the DatePicker component.

## [Anchor to datefieldprops](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops)DateFieldProps[Anchor to label](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-label)label**label**string**string**required**required**Content to use as the field label.

[Anchor to defaultYearMonth](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-defaultyearmonth)defaultYearMonth**defaultYearMonth**{year: YearYear; month: MonthMonth} | YearMonthStringYearMonthString**{year: YearYear; month: MonthMonth} | YearMonthStringYearMonthString**Default [uncontrolled](https://reactjs.org/docs/forms.html#controlled-components) year and month to display. Ignored when year/month navigation is [controlled](https://reactjs.org/docs/forms.html#controlled-components).

[Anchor to disabled](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-disabled)disabled**disabled**DisabledDisabled | DisabledDisabled[] | boolean**DisabledDisabled | DisabledDisabled[] | boolean**Disabled dates, days, and/or ranges, or the date picker. Unbound range disables all dates either from `start` date or to `end` date. `true` disables the date picker.

[Anchor to error](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to id](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-id)id**id**string**string**A unique identifier for the field.

[Anchor to name](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing `Form` component.

[Anchor to onBlur](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-onblur)onBlur**onBlur**() => void**() => void**Callback when focus is removed.

[Anchor to onChange](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-onchange)onChange**onChange**(value: string) => void**(value: string) => void**Callback when the user has **finished editing** a field. Unlike `onChange` callbacks you may be familiar with from React component libraries, this callback is **not** run on every change to the input. Text fields are “partially controlled” components, which means that while the user edits the field, its state is controlled by the component. Once the user has signalled that they have finished editing the field (typically, by blurring the field), `onChange` is called if the input actually changed from the most recent `value` property. At that point, you are expected to store this “committed value” in state, and reflect it in the text field’s `value` property.

This state management model is important given how UI Extensions are rendered. UI Extension components run on a separate thread from the UI, so they can’t respond to input synchronously. A pattern popularized by [controlled React components](https://reactjs.org/docs/forms.html#controlled-components) is to have the component be the source of truth for the input `value`, and update the `value` on every user input. The delay in responding to events from a UI extension is only a few milliseconds, but attempting to strictly store state with this delay can cause issues if a user types quickly, or if the user is using a lower-powered device. Having the UI thread take ownership for “in progress” input, and only synchronizing when the user is finished with a field, avoids this risk.

It can still sometimes be useful to be notified when the user makes any input in the field. If you need this capability, you can use the `onInput` prop. However, never use that property to create tightly controlled state for the `value`.

This callback is called with the current value of the field. If the value of a field is the same as the current `value` prop provided to the field, the `onChange` callback will not be run.

[Anchor to onFocus](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-onfocus)onFocus**onFocus**() => void**() => void**Callback when input is focused.

[Anchor to onInput](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-oninput)onInput**onInput**(value: string) => void**(value: string) => void**Callback when the user makes any changes in the field. As noted in the documentation for `onChange`, you **must not** use this to update `value` — use the `onChange` callback for that purpose. Use the `onInput` prop when you need to do something as soon as the user makes a change, like clearing validation errors that apply to the field as soon as the user begins making the necessary adjustments.

This callback is called with the current value of the field.

[Anchor to onYearMonthChange](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-onyearmonthchange)onYearMonthChange**onYearMonthChange**(yearMonth: { year: number; month: number; }) => void**(yearMonth: { year: number; month: number; }) => void**A callback that is run whenever the month is changed. This callback is called with an object indicating the year/month the UI should change to. When year/month navigation is controlled you must store these values in state and reflect it back in the `yearMonth` prop.

[Anchor to readOnly](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-readonly)readOnly**readOnly**boolean**boolean**Whether the field is read-only.

[Anchor to value](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-value)value**value**T**T**The current value for the field. If omitted, the field will be empty. You should update this value in response to the `onChange` callback.

[Anchor to yearMonth](/docs/api/admin-extensions/2025-07/ui-components/forms/datefield#datefieldprops-propertydetail-yearmonth)yearMonth**yearMonth**{year: YearYear; month: MonthMonth} | YearMonthStringYearMonthString**{year: YearYear; month: MonthMonth} | YearMonthStringYearMonthString**[Controlled](https://reactjs.org/docs/forms.html#controlled-components) year and month to display. Use in combination with `onYearMonthChange`. Makes year/month navigation [controlled](https://reactjs.org/docs/forms.html#controlled-components).

### Year```

number

```### MonthMonth in 1-12 range```

number

```### YearMonthStringA year/month string using the simplified ISO 8601 format (`YYYY-MM`)```

string

```### Disabled```

DateString | Range | Day

```### DateStringA date string using the simplified ISO 8601 format (`YYYY-MM-DD`)```

string

```### Range- endLast day (inclusive) of the selected range```

DateString

```- startFirst day (inclusive) of the selected range```

DateString

``````

export interface Range {

/**

* First day (inclusive) of the selected range

*/

start?: DateString;

/**

* Last day (inclusive) of the selected range

*/

end?: DateString;

}

```### Day```

'Sunday' | 'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday' | 'Saturday'

```ExamplesAdd a single-date DateFieldReactJSCopy9912345678910111213141516171819import React, {useState} from 'react';import {  render,  DateField,} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  const [value, setValue] =    useState('2023-11-08');  return (    <DateField      label="DateField"      value={value}      onChange={setValue}    />  );}## Preview### Examples- #### Add a single-date DateFieldReact```

import React, {useState} from 'react';

import {

render,

DateField,

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

const [value, setValue] =

useState('2023-11-08');

return (

<DateField

label="DateField"

value={value}

onChange={setValue}

/>

);

}

```JS```

import {extend, DateField} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const dateField = root.createComponent(

DateField,

{

label: 'Date',

value: '2023-11-08',

},

'DateField',

);

root.appendChild(dateField);

});

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)